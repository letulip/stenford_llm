# Лекция 6. Рассуждающие модели: RL для reasoning, GRPO, DeepSeek R1 — что изменилось к ноябрю 2026

*Лекция прочитана 7 ноября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/06-llm-reasoning.md) · [Все актуализации](index.md)

## Коротко

- «Reasoning-модель» как отдельный класс почти исчезла: у флагманов размышление встроено и управляется уровнем усилия (effort), а не бюджетом токенов. На Claude Opus 5.5 thinking нельзя отключить, ручной `budget_tokens` возвращает ошибку (сентябрь 2026) [2]; DeepSeek с выходом V4 (24.04.2026) объявил об отказе от отдельного имени `deepseek-reasoner` [13]; OpenAI добавил effort `none` (GPT-5.1, 13.11.2025) и `max` (GPT-5.6, 09.07.2026) [4].
- GRPO остался базовым алгоритмом, но в исправленном виде: DeepSeek-V3.2 (02.12.2025) — без деления на std, с несмещённым KL и off-policy masking, RL-компьют больше 10 % от претрейна [15]; DeepSeek-V4 (апрель 2026) — GRPO по доменам плюс on-policy distillation в единую модель [14]. Sequence-level варианты GSPO и CISPO вошли в TRL и в рецепт ScaleRL (Meta, 15.10.2025) [21][22][23][33].
- Спор «учит ли RLVR новому или только обостряет сэмплирование» не закрыт: Yue et al. [25] против CoT-Pass@K (ICLR 2026) [26] и работы о diversity collapse как overtraining (13.06.2026) [27].
- Бенчмарки лекции насыщены: AIME/HMMT — 95–99 % (07.03.2026) [38]; SWE-bench Verified заархивирован при 97 % (01.09.2026) [7], OpenAI перестала по нему отчитываться (февраль 2026) [6]. Замены — SWE-bench Pro (Verified) [9][10], HLE-Diamond (22.09.2026) [37], FrontierMath v2 (12.06.2026) [36].
- Дистилляция стала on-policy: по данным Thinking Machines (27.10.2025) она примерно в десять раз дешевле RL [30]; но студенты 0,6–4B учатся решать, а не останавливаться (29.09.2026) [32].
- Главный фронт — agentic RL: V3.2 обучалась в 1 800+ средах [15], Kimi K2 Thinking (06.11.2025) держит 200–300 последовательных вызовов инструментов [19], рецепты long-horizon RL систематизированы (23.03.2026) [28].

## Что осталось верным

- Ядро лекции: проверяемая награда поверх базовой модели, advantage относительно группы без value function, PPO-подобный clip. DeepSeek-V3.2 и V4 по-прежнему обучают RL-стадию через GRPO [14][15]; `GRPOTrainer` в TRL — стандартный инструмент [33].
- Length bias и правки DAPO/Dr. GRPO подтвердились: в TRL `loss_type="dapo"` — значение по умолчанию, отказ от std (Dr. GRPO) и clip-higher (DAPO) — штатные опции [33]; ScaleRL использует асимметричный clip и zero-variance filtering (тот же dynamic sampling) [23].
- Reasoning-токены тарифицируются как выходные, причём по полному объёму, даже если API показывает лишь summary или ничего [1][5][12].
- Рецепт R1 отрецензирован: статья вышла в Nature 17.09.2025 — R1-Zero поднял pass@1 на AIME 2024 с 15,6 % до 77,9 % [16]. Награды V3.2 — те же: rule-based outcome, length penalty, language consistency [15].
- Дистилляция в малые модели эффективнее RL с нуля: Qwen3 строит малые модели дистилляцией из флагманов [18]; Yue et al. показывают, что дистилляция добавляет новые паттерны рассуждения, а RLVR — нет [25].
- Метрика pass@k жива и стала главным инструментом спора о RLVR [25][26][27].

## Что устарело или сдвинулось

- **Лекция говорит:** reasoning-модель — отдельный тип модели, хронология заканчивается на R1 (раздел 2, 21:58) → **Сейчас:** категория растворилась в режимах одного чекпойнта: Opus 5.5 — thinking всегда включён [2]; DeepSeek V4 — Non-think/High/Max [13][14]; Qwen3.5 (февраль 2026) — обе моды через `enable_thinking` [17]; Kimi K3 — thinking всегда включён, effort low/high/max [20]; GPT-6 Astra (03.09.2026) не поддерживает effort `none` [4]. Отдельными остались только «Pro»-варианты OpenAI [4].
- **Лекция говорит:** «сколько думать» — открытая проблема, вариант — классификатор промпта (раздел 5, 54:01) → **Сейчас:** модель сама решает на каждом запросе, разработчик задаёт effort от `low` до `max` [1][5]; в документации Gemini остался только `thinking_level`, бюджет токенов в ней больше не фигурирует [12]; у Anthropic `budget_tokens` — legacy [1][2]. В DeepSeek V4 три режима обучены разными RL-конфигурациями с разными length penalty и окнами 8K/128K/384K [14].
- **Лекция говорит:** качество меряют на AIME и SWE-bench (раздел 3, 27:51) → **Сейчас:** AIME 2025 — 98–99 % у топ-моделей, benchlm вывел AIME/HMMT из рейтинга [38]; SWE-bench Verified — 97,0 % у Claude Opus 5, Vals его больше не запускает [7]; соавтор бенчмарка назвал его насыщенным на 93,9 % [8]; OpenAI отказалась от него из-за контаминации [6]. Замены: SWE-bench Pro — 1 865 задач из 41 репозитория (21.09.2025) [9] и SWE-Bench Pro Verified (08.09.2026) — после обнаружения reward hacking через утёкшие gold-решения [10]; HLE-Diamond [37]; FrontierMath v2 с исправлением ошибок в 42 % задач [36]; ARC-AGI-2 (Gemini 3.1 Pro — 77,1 %, 19.02.2026) [11].
- **Лекция говорит:** advantage делится на std группы, KL к reference — член целевой функции (раздел 7, 1:06:56) → **Сейчас:** в продакшн-рецептах деление на std убрано (V3.2 — формула без std [15]; ScaleRL — std по батчу [23]), KL выключен (TRL: `beta=0.0` по умолчанию, reference-модель не загружается [33]; ScaleRL — без KL [23]) или сделан несмещённым (V3.2 [15]).
- **Лекция говорит:** RL сначала на reasoning-доменах, потом отдельный RL на helpfulness (раздел 10, 1:37:26) → **Сейчас:** V3.2 слила reasoning, агентные и alignment-данные в один RL-этап, чтобы избежать забывания [15]; V4 обучает специалистов по доменам (SFT → GRPO) и сливает их on-policy distillation [14].
- **Лекция говорит:** дистилляция — SFT на выходах учителя (раздел 10, 1:44:44) → **Сейчас:** on-policy distillation — reverse KL на траекториях самого студента: около 1 800 GPU-часов против 17 920 у RL на AIME'24 [30]; в V4 — полнословарные логиты от десятка учителей [14].

## Новое, о чём лекция не знала

- **DeepSeek-V3.2 и V3.2-Speciale (02.12.2025).** GRPO с unbiased KL, off-policy sequence masking, Keep Routing для MoE; агентный синтез — 1 800+ сред, около 85 тыс. промптов; Speciale — золото IMO 2025 (35/42) и IOI 2025, AIME 2025 — 96,0 [15]. Это прямое продолжение рецепта R1, где RL стал десятой частью бюджета претрейна.
- **DeepSeek-V4 (24.04.2026).** MoE 1,6T/49B (Pro) и 284B/13B (Flash), контекст 1M, лицензия MIT. Для трудно проверяемых задач актор сам служит generative reward model по рубрикам; sandbox DSec держит сотни тысяч инстансов; прерванные rollout'ы дописываются, а не перегенерируются — иначе выборка смещается к коротким ответам [14].
- **ScaleRL (Meta, 15.10.2025).** 400 тыс. GPU-часов на изучение масштабирования RL: кривые сигмоидальны и предсказуемы по малым запускам; тип loss (CISPO/GSPO лучше DAPO) и FP32 на LM-head меняют асимптоту, а агрегация, нормировка и curriculum — только эффективность [23].
- **GSPO (24.07.2025) и CISPO (16.06.2025).** Sequence-level importance ratio стабилизирует RL для MoE (Qwen3) [21]; CISPO обрезает IS-веса, а не обновления токенов (MiniMax-M1) [22]; обе доступны в TRL [33]. Обзор 2026 года добавляет DHPO, EP-GRPO, DPPO, ARPO [34].
- **Bias групповой нормировки.** HA-DW (13.01.2026): mean-centering недооценивает advantage на трудных промптах и переоценивает на лёгких [24].
- **RLVR-дебаты.** Yue et al. (апрель 2025, v5 ноябрь 2025): при большом k база обгоняет RL-модель [25]; CoT-Pass@K (ICLR 2026): если требовать верной цепочки, RLVR расширяет границу [26]; BBG (13.06.2026): падение pass@k — overtraining на уже решённых задачах, часть нерешаемых задач становится решаемой [27].
- **Agentic RL.** Kimi K2 Thinking (1T/32B, HLE с инструментами 44,9) [19]; «Demystifying…» (23.03.2026): около 1K примеров достаточно, стабильность среды критична [28]; «Rethinking Agentic RL» (30.04.2026) [29]; Qwen3.5 — RL в «million-agent environments» [17]; Kimi K3 (2,8T/104B, июль 2026) [20].
- **OPD для малых моделей.** Сигнал учителя полезен на неверных rollout'ах и шумен на верных (11.05.2026) [31]; студенты 0,6–4B из Qwen3-8B теряют умение останавливаться (29.09.2026) [32].
- **Фронтир 2026.** GPT-5.5 (24.04), GPT-5.6 (09.07), GPT-6 Astra/Sol/Luna (сентябрь), GPT-6.1 Sol (29.09) [4]; Claude Opus 5 (24.07) [3] и Opus 5.5 [2]; Gemini 3.1 Pro (19.02) [11]; на MathArena лучший открытый — Kimi K3.1 Pro, 59,6 % против 84,0 % у GPT-6.1 Sol [35].

## Что это меняет для читателя

- Не выбирайте «reasoning или нет» — выбирайте effort и измеряйте: дефолты меняются между версиями (Opus 5 — `high`, Opus 5.5 — `medium` [2]; GPT-5.1 — `none`, GPT-5.5 — `medium` [4]), при миграции перепрогоняйте eval.
- Закладывайте `max_tokens` с учётом thinking: он входит в лимит и оплачивается полностью; OpenAI советует резервировать не менее 25 тыс. токенов [1][5].
- Для RL на открытой модели берите TRL (`dapo`, `beta=0`; при необходимости `scale_rewards=False`, `epsilon_high=0.28`), для MoE — `importance_sampling_level="sequence"` [33]; фильтруйте промпты с нулевой дисперсией [23].
- Для своей малой reasoning-модели: сначала SFT-дистилляция на проверенных цепочках (как в лекции), затем on-policy distillation с открытым учителем; у студентов меньше 2B контролируйте остановку [30][32]; проверяйте pass@k при больших k, чтобы не схлопнуть разнообразие [27].
- Не цитируйте AIME и SWE-bench Verified как доказательство: берите SWE-bench Pro (Verified), HLE-Diamond и свои задачи [6][10][37].
- Основная стоимость agentic RL — инфраструктура (sandbox, асинхронные rollout'ы), а не градиентный шаг [14][23].

## Проверка пометок в конспекте

- «По состоянию на 2026 год «сколько думать»…» (раздел 5) — в целом верно, две неточности: «бюджет токенов на размышление» стал legacy (Anthropic отклоняет `budget_tokens` на Opus 5.5 [2], в документации Gemini остался только `thinking_level` [12]); у части флагманов thinking уже нельзя отключить (Opus 5.5 [2], Kimi K3 [20]).
- «Reasoning-модель стоит своих токенов…» (раздел 2) — совет начинать с минимального усилия разумен, но «без него» уже не всегда возможно; OpenAI рекомендует стартовать с `medium` [5].
- «Несколько точных цифр по названным бенчмаркам…» (раздел 3) — цифры верны, но «чаще цитируют SWE-bench Verified» устарело: заархивирован [7], OpenAI перешла на SWE-bench Pro [6].
- «Главный инженерный выигрыш GRPO — память…» (раздел 7) — верно; уточнение: в TRL по умолчанию `beta=0.0`, reference-модель вообще не загружается [33].
- «В DAPO (ByteDance Seed…) четыре приёма…» (раздел 9) — верно; уточнение: Dr. GRPO делит на константу (максимальную длину ответа), а не убирает множитель буквально [33].
- «Дистилляция «через SFT на выходах учителя» — самый доступный способ…» (раздел 10) — верно, но уже не единственный: on-policy distillation [30].
- Остальные 💡-блоки замечаний не требуют.

## Источники

1. Steering thinking (adaptive thinking, effort, pricing) — Claude Platform Docs (Anthropic) — прочитано 07.11.2026 — https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost
2. What's new in Claude Opus 5.5 — Claude Platform Docs (Anthropic) — сентябрь 2026 — https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5
3. Introducing Claude Opus 5 — Anthropic — 24.07.2026 — https://anthropic.com/news/claude-opus-5
4. API Changelog — OpenAI Developers — записи 13.11.2025–26.10.2026 — https://developers.openai.com/api/docs/changelog
5. Reasoning models guide — OpenAI Developers — прочитано 07.11.2026 — https://developers.openai.com/api/docs/guides/reasoning
6. OpenAI moves beyond SWE-bench Verified as coding benchmarks saturate (пересказ поста OpenAI «Why we no longer evaluate SWE-bench Verified», сам пост при проверке был недоступен) — Tessl — 25.02.2026 — https://tessl.io/blog/openai-moves-beyond-swe-bench-verified-as-coding-benchmarks-saturate
7. SWE-bench Verified (Archived Benchmark) — Vals AI — 01.09.2026 — https://www.vals.ai/benchmarks/swebench
8. «SWE-bench Verified is now saturated at 93.9%» — Ofir Press (соавтор SWE-bench), Hacker News — 2026 (точная дата в треде не указана) — https://news.ycombinator.com/item?id=47912620
9. SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks? — Scale AI, arXiv:2509.16941 — 21.09.2025 — https://arxiv.org/abs/2509.16941
10. SWE-Bench Pro Verified: A Reliable Benchmark for Software Engineering Agents — arXiv:2609.08149 — 08.09.2026 — https://arxiv.org/abs/2609.08149
11. Gemini 3.1 Pro: A smarter model for your most complex tasks — Google Blog — 19.02.2026 — https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/
12. Gemini thinking (thinking_level) — Google AI Studio Docs — прочитано 07.11.2026 — https://aistudio.google.com/docs/thinking
13. Change Log — DeepSeek API Docs — записи 01.12.2025–17.10.2026 — https://api-docs.deepseek.com/updates/
14. DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence — DeepSeek, arXiv:2606.19348 — 26.04.2026 — https://arxiv.org/abs/2606.19348
15. DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models — DeepSeek, arXiv:2512.02556 — 02.12.2025 — https://arxiv.org/abs/2512.02556
16. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning — Nature 645, 633–638 — 17.09.2025 — https://www.nature.com/articles/s41586-025-09422-z
17. Qwen3.5-0.8B model card — Qwen, Hugging Face — февраль 2026 — https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/main/README.md
18. Qwen3 Technical Report — Qwen, arXiv:2505.09388 — 14.05.2025 — https://arxiv.org/abs/2505.09388
19. Kimi K2 Thinking model card — Moonshot AI, Hugging Face — релиз 06.11.2025 (дата по листингам Epoch AI / OpenRouter) — https://huggingface.co/moonshotai/Kimi-K2-Thinking
20. Kimi K3 model card — Moonshot AI, Hugging Face — июль 2026 (данные бенчмарков на 23.07.2026) — https://huggingface.co/moonshotai/Kimi-K3
21. Group Sequence Policy Optimization — Qwen Team, arXiv:2507.18071 — 24.07.2025 — https://arxiv.org/abs/2507.18071
22. MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention (CISPO) — MiniMax, arXiv:2506.13585 — 16.06.2025 — https://arxiv.org/abs/2506.13585
23. The Art of Scaling Reinforcement Learning Compute for LLMs (ScaleRL) — Khatri et al. (Meta), arXiv:2510.13786 — 15.10.2025 — https://arxiv.org/abs/2510.13786
24. Your Group-Relative Advantage Is Biased — Yang et al., arXiv:2601.08521 — 13.01.2026 (v3 30.10.2026) — https://arxiv.org/abs/2601.08521
25. Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model? — Yue et al., arXiv:2504.13837 — 18.04.2025 (v5 24.11.2025) — https://arxiv.org/abs/2504.13837
26. Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs (CoT-Pass@K) — Wen et al., arXiv:2506.14245; постер ICLR 2026 — 17.06.2025 — https://arxiv.org/abs/2506.14245 · https://iclr.cc/virtual/2026/poster/10007896
27. Understanding Diversity Collapse in RLVR via the Lens of Overtraining — Yuan et al., arXiv:2606.15455 — 13.06.2026 — https://arxiv.org/abs/2606.15455
28. Demystifying Reinforcement Learning for Long-Horizon Tool-Using Agents: A Comprehensive Recipe — Wu et al., arXiv:2603.21972 (Findings of EMNLP 2026) — 23.03.2026 — https://arxiv.org/abs/2603.21972
29. Rethinking Agentic Reinforcement Learning In Large Language Models — arXiv:2604.27859 — 30.04.2026 — https://arxiv.org/abs/2604.27859
30. On-Policy Distillation — Thinking Machines Lab — 27.10.2025 — https://thinkingmachines.ai/blog/on-policy-distillation/
31. Unmasking On-Policy Distillation: Where It Helps, Where It Hurts, and Why — arXiv:2605.10889 — 11.05.2026 — https://arxiv.org/abs/2605.10889
32. Solving Without Stopping: On-Policy Distillation at Small Scale — Li et al., arXiv:2609.37326 — 29.09.2026 — https://arxiv.org/abs/2609.37326
33. GRPO Trainer (GRPOConfig: loss_type, importance_sampling_level, scale_rewards, beta) — Hugging Face TRL docs — прочитано 07.11.2026 — https://huggingface.co/docs/trl/main/en/grpo_trainer
34. Reasoning RL in 2026: GRPO, DPO, RLVR, Agentic PO & Beyond — Turing Post (Alyona Vert) — 07.06.2026 — https://www.turingpost.com/p/reasoning-rl-in-2026
35. MathArena leaderboard — ETH Zürich SRI Lab — прочитано 07.11.2026 — https://matharena.ai/
36. FrontierMath Tiers 1–4 — Epoch AI — v2 от 12.06.2026 — https://epoch.ai/frontiermath/tiers-1-4
37. Humanity's Last Exam (HLE, HLE-Rolling, HLE-Diamond) — Center for AI Safety / Scale AI — HLE-Diamond 22.09.2026 — https://lastexam.ai/
38. AIME & HMMT: Can AI Models Do Competition Math? — benchlm.ai — 07.03.2026 — https://benchlm.ai/blog/posts/aime-hmmt-competition-math
