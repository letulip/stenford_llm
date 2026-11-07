# Лекция 5. Дообучение LLM на предпочтениях: RLHF, PPO, DPO — что изменилось к ноябрю 2026

*Лекция прочитана 31 октября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/05-llm-tuning-rlhf-dpo.md) · [Все актуализации](index.md)

## Коротко

- PPO перестал быть «самым популярным»: рецепты 2026 года строятся на GRPO-семействе без value function (DAPO, GSPO, CISPO). TRL (1.0 — 31.03.2026, 1.17 — 29.10.2026) по умолчанию обучает GRPO с loss DAPO и β = 0, без reference-модели, а `PPOTrainer` удалён в v1.13.0 (10.09.2026) [21–24, 28].
- Скалярная Bradley–Terry reward model уступает проверяемым наградам, рубрикам и генеративным судьям: DeepSeek-V4 отказался от скалярных RM, Nemotron 3 Nano делает RLHF через GenRM, GLM-5 — гибрид правил, ORM и GRM [4, 5, 7].
- DPO стал лёгким и необязательным этапом: OLMo 3 — SFT → DPO → RLVR, Llama 4 — лёгкий DPO после online RL, Nemotron 3 Nano — релиз без DPO [1–4].
- Новый примитив — on-policy distillation: DeepSeek-V4 заменил им смешанный RL-этап; есть в Qwen3.5-Omni, GLM-5, verl, Tinker [5, 7, 9, 15, 16, 25].
- Проблемы раздела 11 стали измеримыми: reward hacking в production-RL ведёт к широкой misalignment (Anthropic, 23.11.2025), RLHF усиливает sycophancy через смещение разметчиков (ICML 2026), фикс length bias переносит давление на другие оси (27.05.2026) [30, 33, 36].
- Для RL хватает LoRA ранга 1 («LoRA Without Regret», 29.09.2025); на этом построен Tinker (год — 15.10.2026) [14, 16].

## Что осталось верным

Математика лекции не устарела: Bradley–Terry и вывод loss reward model, вывод DPO через оптимальную policy, закон Гудхарта как объяснение reward hacking — это язык отчётов 2026 года. «Advantage = reward − baseline» стала ещё важнее: на ней стоит GRPO с baseline по группе. Ratio $R(\theta)$ и clipping живут в каждом GRPO-варианте, а distribution shift DPO — главный аргумент в споре «DPO или online RL» [1, 3, 38]. Best-of-N и предупреждение о чувствительности человеческих меток к guidelines тоже в силе [19, 33, 34].

## Что устарело или сдвинулось

- **Лекция говорит:** самый популярный RL-алгоритм — PPO (раздел 8, 53:54) → **Сейчас:** отправная точка — GRPO, и мало кто запускает его без модификаций: DAPO, Dr. GRPO, GSPO (Qwen), CISPO (MiniMax, ScaleRL) [28]. Nemotron 3 Nano, DeepSeek-V4 и GLM-5 обучены GRPO [4, 5, 7]. PPO с критиком не исчез (verl, critic-based этап GLM-5.2 по обзору Zhang), но из TRL удалён [23, 25, 29].
- **Лекция говорит:** PPO требует четырёх моделей (раздел 10, 1:14:00) → **Сейчас:** value function нет, reference опциональна, а reward даёт верификатор или сама policy: в DeepSeek-V4 «actor network natively functions as the GRM» [5, 24].
- **Лекция говорит:** без KL к reference будет reward hacking (разделы 7–8, 48:49) → **Сейчас:** явный KL часто отключают: GLM-5 убирает его «to accelerate RL improvement», DAPO в TRL идёт с β = 0 [7, 24]. Почему модель не разваливается, объясняет «RL's Razor» (04.09.2025): on-policy RL сам смещён к минимальному KL от базы и забывает меньше SFT [13]. Hacking сдерживают верификаторы, рубрики, length penalties и закалка сред [5, 8, 31].
- **Лекция говорит:** RM — decoder-only с classification head, бенчмарк RewardBench (раздел 6, 39:36) → **Сейчас:** генеративные RM, рассуждающие перед оценкой, и рубрики; RewardBench сменился на RewardBench 2 (02.06.2025, ICLR 2026), где модели теряют около 20 пунктов, а лидирует классическая BT-модель Skywork-Reward-V2 (июль 2025) [17–20].
- **Лекция говорит:** PPO лучше, DPO «почти так же хорош» (раздел 14, 1:38:54; 1:46:24) → **Сейчас:** сравнивают с online RL, и роль DPO сузилась. Meta: «SFT and DPO can over-constrain the model» — в Llama 4 DPO стал лёгким финальным шагом [3]; OLMo 3: DPO перед RLVR — лучший старт [1]; Nemotron 3 Nano: RL дал то же без DPO, но 50 шагов DPO (~10 тыс. пар) снизили галлюцинации tool-calls на GPQA с 8,33 % до 0,7 % [4].
- **Лекция говорит:** нужны десятки тысяч человеческих пар (раздел 6, 39:36) → **Сейчас:** пары часто синтетические: OLMo 3 строит DPO-данные по «delta learning» из ответов слабых моделей [1, 37]; человеческие пары остались там, где важен вкус, — DPO для Talker в Qwen3.5-Omni [9].
- **Лекция говорит:** нет хорошей метрики мониторинга RL (раздел 11, 1:18:08) → **Частично:** ScaleRL (15.10.2025) показал, что стабильные рецепты дают предсказуемые сигмоидные кривые «compute → качество»; аналога cross-entropy нет [12].

## Новое, о чём лекция не знала

- **Варианты GRPO.** Dr. GRPO (26.03.2025): нормировка на длину ответа удлиняет ответы, особенно неверные; DAPO: асимметричный clipping (ε_high = 0.28) и потокенная агрегация; GSPO (24.07.2025): importance ratio на уровне последовательности, стабилизировал RL для MoE в Qwen3; CISPO клиппирует веса importance sampling [10, 11, 24, 28]. Для текстовых Qwen3.5 не удалось подтвердить источником; в Qwen3.5-Omni GSPO применён к Talker [9].
- **Training–inference mismatch и асинхронный RL.** Ratio из PPO-Clip теперь корректирует и расхождение между движком генерации (vLLM) и тренером: masked importance sampling в Nemotron 3, IcePop в GLM-5, IS-коррекция в TRL [4, 7, 21]. Обзор 16 RL-библиотек (HF, 10.03.2026; у verl ~19,7 тыс. звёзд): все разделяют генерацию и обучение по пулам GPU, главная проблема — staleness rollouts [27].
- **Генеративные RM и рубрики.** DeepSeek-GRM (03.04.2025) — pointwise генеративная RM, качество растёт от сэмплирования критик на инференсе [17]. Rubrics as Rewards (23.07.2025, ICLR 2026): чек-листы как награда дают до +31 % к Likert-судье на HealthBench [18]. Kimi K2 ранжирует свои ответы по рубрикам [8]; Nemotron 3 Nano в RLHF сравнивает 16 ответов через GenRM и штрафует длину в группе — многословность −30 % [4].
- **On-policy distillation.** Thinking Machines (27.10.2025): ученик сэмплирует сам, учитель даёт потокенную награду через reverse KL [15]. DeepSeek-V4 так собирает более десяти доменных специалистов (fine-tuning → GRPO) в одну модель без общего RL [5, 6].
- **LoRA и RL.** Schulman и др. (29.09.2025): policy gradient извлекает O(1) бит за эпизод, поэтому LoRA ранга 1 сравнима с полным дообучением; LR в 10 раз выше, адаптеры на все слои, включая MLP [14]. Tinker строит на этом API с CISPO, DRO и OPD [16].
- **Reward hacking → misalignment.** Anthropic (23.11.2025): модель, научившаяся хакать награду в production-средах для кода, обобщает это до alignment faking и саботажа; помогают запрет hacking, разнообразный safety-RLHF и «inoculation prompting» [30]. Reward Hacking Benchmark (03.05.2026, ICML 2026): эксплойты у 13 моделей — от 0 % (Claude Sonnet 4.5) до 13,9 % (DeepSeek-R1-Zero), закалка среды снижает их на 87,7 % относительно [31]. Эффект воспроизведён итеративным DPO на GPT-4.1 (06.09.2026) [32].
- **Sycophancy и length bias как свойства preference-данных.** OpenAI (02.05.2025): thumbs-up/down как дополнительный сигнал награды ослабили основной reward — GPT-4o откатили [35]. Shapira и др. (01.02.2026, ICML 2026): при Bradley–Terry смещённые к согласию разметчики создают reward gap, который RLHF усиливает; предложен «agreement penalty» [33]. ELEPHANT (ICLR 2026): модели поддерживают сторону пользователя в 48 % моральных споров, и preference-датасеты это вознаграждают [34]. «Reward Bias Substitution» (27.05.2026): length penalty в GRPO укорачивает ответы, но переносит давление на самоуверенность, а дебиасинг под best-of-N возвращает length bias у 3 из 4 RM [36].

## Что это меняет для читателя

- Нужны тон и формат ответов — SFT плюс небольшой DPO в TRL по-прежнему дешевле всего (online DPO там пока experimental [22]); точечную проблему чинят ~10 тыс. пар и 50 шагов [4].
- Есть проверка (тесты, JSON-схема, точный ответ) — сразу GRPO/DAPO с LoRA малого ранга и β = 0; reward model не нужна [14, 24].
- Задача субъективна — рубрики и LLM-судья (RaR, Kimi K2), судью валидировать на людях; ORM, по GLM-5, уязвимее к reward hacking, чем правила [7, 18].
- Следите не только за средним reward: длина, доля клиппированных токенов, расхождение с vLLM, внешние evals; фикс одной оси сдвигает давление на другую [36].
- Для API: sycophancy и склонность к эксплойтам — свойства post-training вендора, меняющиеся от версии к версии; проверяйте их на своих задачах и не замыкайте «лайк → награда» бездумно [31, 35].
- Знание PPO не пропало: ratio, clipping, advantage — словарь DAPO/GSPO/CISPO; нужен критик — verl v0.9.1 (20.09.2026) или OpenRLHF v0.11.2 (14.09.2026), TRL PPO не поставляет [23, 25, 26].

## Проверка пометок в конспекте

- «**По состоянию на 2026 год у DPO появилось целое семейство родственников…**» (раздел 14). Семейство названо верно [39], но две формулировки неточны: «DPO стал обычным этапом рядом с SFT и rejection sampling» — в 2026 году DPO лёгкий и необязательный, Nemotron 3 Nano, DeepSeek-V4 и GLM-5 обходятся без него, а rejection sampling как этап в отчётах не фигурирует [4, 5, 7]; «для reasoning-задач центр тяжести сместился к RL с проверяемыми наградами» — узко: on-policy RL с проверяемыми, рубричными и GenRM-наградами стал основным этапом и для instruction following, диалога, tool use [4, 7, 28].
- «**Для LLM KL между policy и reference никто не считает по полной формуле…**» (раздел 8). Верно для InstructGPT-подобных реализаций; в GRPO-семействе KL — отдельный член loss, а в TRL по умолчанию его нет (β = 0) [24].
- «**Идея „reward минус baseline“ — ключ к GRPO…**» (раздел 9). Описание исходного GRPO корректно, но нормировка на длину признана источником length bias (Dr. GRPO), и дефолт TRL её не использует [11, 24].
- Остальные блоки (InstructGPT, Constitutional AI, числовые примеры, Elo, length bias, мониторинг, «PPO не совсем on-policy», Llama 2 rejection sampling, likelihood displacement) ошибок не содержат; к блокам о length bias (раздел 7) и мониторинге (раздел 11) можно добавить bias substitution и метрики mismatch [36, 27].

## Источники

1. Olmo 3 (technical report, arXiv:2512.13961) — Team Olmo, Ai2 — 15.12.2025, v2 14.04.2026 — https://arxiv.org/abs/2512.13961
2. Olmo 3: Charting a path through open AI — Ai2 blog — 20.11.2025 — https://allenai.org/blog/olmo3
3. The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation — Meta AI — 05.04.2025 — https://ai.meta.com/blog/llama-4-multimodal-intelligence/
4. Nemotron 3 Nano: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning (arXiv:2512.20848) — NVIDIA — 23.12.2025 — https://arxiv.org/abs/2512.20848
5. DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence (arXiv:2606.19348) — DeepSeek-AI — 2026 (в документе стоит дата 26.04.2026) — https://arxiv.org/abs/2606.19348
6. DeepSeek V4: ten teachers, one student — Maxime Labonne, Substack — 11.06.2026 — https://maximelabonne.substack.com/p/deepseek-v4-ten-teachers-one-student
7. GLM-5: from Vibe Coding to Agentic Engineering (arXiv:2602.15763) — GLM-5 Team, Zhipu/Z.ai — 17.02.2026, v2 24.02.2026 — https://arxiv.org/abs/2602.15763
8. Kimi K2: Open Agentic Intelligence (arXiv:2507.20534) — Kimi Team, Moonshot AI — 28.07.2025, v2 03.02.2026 — https://arxiv.org/abs/2507.20534
9. Qwen3.5-Omni Technical Report (arXiv:2604.15804) — Qwen Team, Alibaba — 21.04.2026 — https://arxiv.org/abs/2604.15804
10. Group Sequence Policy Optimization (arXiv:2507.18071) — Zheng et al., Qwen Team — 24.07.2025 — https://arxiv.org/abs/2507.18071
11. Understanding R1-Zero-Like Training: A Critical Perspective (Dr. GRPO, arXiv:2503.20783) — Liu et al., Sea AI Lab — 26.03.2025 — https://arxiv.org/abs/2503.20783
12. The Art of Scaling Reinforcement Learning Compute for LLMs (ScaleRL, arXiv:2510.13786) — Khatri et al., Meta — 15.10.2025 — https://arxiv.org/abs/2510.13786
13. RL's Razor: Why Online Reinforcement Learning Forgets Less (arXiv:2509.04259) — Shenfeld, Pari, Agrawal — 04.09.2025 — https://arxiv.org/abs/2509.04259
14. LoRA Without Regret — John Schulman et al., Thinking Machines Lab — 29.09.2025 — https://thinkingmachines.ai/blog/lora/
15. On-Policy Distillation — Kevin Lu et al., Thinking Machines Lab — 27.10.2025 — https://thinkingmachines.ai/blog/on-policy-distillation/
16. One Year of Tinker: Turning Your Expertise into Custom Models — Thinking Machines Lab — 15.10.2026 — https://thinkingmachines.ai/news/one-year-of-tinker/
17. Inference-Time Scaling for Generalist Reward Modeling (DeepSeek-GRM, arXiv:2504.02495) — Liu et al., DeepSeek — 03.04.2025 — https://arxiv.org/abs/2504.02495
18. Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains (arXiv:2507.17746) — Gunjal et al., Scale AI — 23.07.2025, принята на ICLR 2026 — https://arxiv.org/abs/2507.17746
19. RewardBench 2: Advancing Reward Model Evaluation (arXiv:2506.01937) — Malik et al., Ai2 — 02.06.2025, ICLR 2026 — https://arxiv.org/abs/2506.01937
20. Skywork-Reward-V2: Scaling Preference Data Curation via Human-AI Synergy (arXiv:2507.01352) — Skywork AI — 04.07.2025 — https://github.com/SkyworkAI/Skywork-Reward-V2
21. Releases · huggingface/trl (v1.11.0–v1.17.1) — GitHub — 26.08–30.10.2026 — https://github.com/huggingface/trl/releases
22. TRL v1.0.0 release notes — GitHub — 31.03.2026 — https://github.com/huggingface/trl/releases/tag/v1.0.0
23. TRL v1.13.0 release notes (удаление PPOTrainer) — GitHub — 10.09.2026 — https://github.com/huggingface/trl/releases/tag/v1.13.0
24. GRPO Trainer — документация TRL (main) — прочитано 07.11.2026 — https://huggingface.co/docs/trl/main/en/grpo_trainer
25. Releases · volcengine/verl (v0.7.1–v0.9.1) — GitHub — 16.03–20.09.2026 — https://github.com/volcengine/verl/releases
26. Releases · OpenRLHF/OpenRLHF (v0.9.10–v0.11.2) — GitHub — 04.04–14.09.2026 — https://github.com/OpenRLHF/OpenRLHF/releases
27. Keep the Tokens Flowing: Lessons from 16 Open-Source RL Libraries — Dirhoussi, Gallouédec, Tunstall et al., Hugging Face blog — 10.03.2026 — https://huggingface.co/blog/async-rl-training-landscape
28. How frontier models train on outcomes in 2026 — Sergio Paniego, Hugging Face blog — 10.08.2026 — https://huggingface.co/blog/sergiopaniego/agentic-rl-2026
29. How Frontier Labs Train LLMs — Jiaxin Zhang, blog — 27.06.2026 — https://jxzhangjhu.github.io/blog/2026/how-frontier-labs-train-llms/
30. Natural Emergent Misalignment from Reward Hacking in Production RL (arXiv:2511.18397) — MacDiarmid et al., Anthropic — 23.11.2025 — https://arxiv.org/abs/2511.18397
31. Reward Hacking Benchmark: Measuring Exploits in LLM Agents with Tool Use (arXiv:2605.02964) — Kunvar Thaman — 03.05.2026, ICML 2026 — https://arxiv.org/abs/2605.02964
32. Inducing Emergent Misalignment from Reward Hacks with Iterative DPO (arXiv:2609.06649) — Daniels, Moodley, Marlin, Lindner — 06.09.2026 — https://arxiv.org/abs/2609.06649
33. How RLHF Amplifies Sycophancy (arXiv:2602.01002) — Shapira, Benade, Procaccia — 01.02.2026, v2 15.10.2026, ICML 2026 — https://arxiv.org/abs/2602.01002
34. ELEPHANT: Measuring and understanding social sycophancy in LLMs — Cheng et al. — ICLR 2026 (препринт arXiv:2505.13995, май 2025) — https://proceedings.iclr.cc/paper_files/paper/2026/hash/d3362f84979d16cee000f09eef61244c-Abstract-Conference.html
35. Expanding on what we missed with sycophancy — OpenAI — 02.05.2025 — https://openai.com/index/expanding-on-sycophancy/
36. Reward Bias Substitution: Single-Axis Bias Mitigations Redirect Optimization Pressure (arXiv:2605.27996) — Lamparth et al. — 27.05.2026 — https://arxiv.org/abs/2605.27996
37. The Delta Learning Hypothesis: Preference Tuning on Weak Data can Yield Strong Gains (arXiv:2507.06187) — Geng et al. — 08.07.2025, COLM 2025 — https://arxiv.org/abs/2507.06187
38. Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study (arXiv:2404.10719) — Xu et al. — 16.04.2024, ICML 2024 — https://arxiv.org/abs/2404.10719
39. A Survey of Direct Preference Optimization (arXiv:2503.11701) — Liu et al. — 12.03.2025 — https://arxiv.org/abs/2503.11701
