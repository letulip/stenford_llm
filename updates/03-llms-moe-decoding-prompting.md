# Лекция 3. Большие языковые модели: MoE, декодирование, промптинг — что изменилось к ноябрю 2026

*Лекция прочитана 10 октября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/03-llms-moe-decoding-prompting.md) · [Все актуализации](index.md)

## Коротко

- **Ручки сэмплирования исчезли из фронтирных API.** Anthropic в гиде по миграции на Claude Opus 5.5 просит не передавать `temperature`, `top_p` и `top_k` [11]; Google для Gemini 3.6 объявил их «deprecated and ignored» и обещает ошибку 400 в следующих поколениях [15]; OpenAI требует убирать `temperature`, `top_p` и `top_logprobs`, если reasoning effort не равен `none`, а GPT-6 Astra и GPT-6.1 Sol режим `none` не поддерживают [10] (документация на 7 ноября 2026).
- **MoE ушёл в триллионы.** DeepSeek-V4-Pro — 1,6T всего / 49B активных, V4-Flash — 284B/13B (апрель 2026) [1]; Kimi K3 — 2,8T/104B, 896 экспертов, 16 + 2 общих (июль 2026) [22]; Qwen3.8-2.4T-A95B (12 августа 2026) [21]; Meta Muse Spark Open — 816B (15 октября 2026) [3].
- **Attention перестроили ради 1M токенов.** Qwen3.5/3.8 и Kimi K3 — гибриды линейного внимания с MoE; DeepSeek-V4 заменил attention сжато-разреженными CSA/HCA и держит KV-кэш на уровне 7–10 % от V3.2 при 1M [1, 21, 22]. Окно 1M — умолчание у Claude Opus 5.5 и Gemini 3.6 Flash [11, 15].
- **Prefill/decode-дезагрегация — штатный режим.** SGLang в roadmap на Q4 2026 называет её «the default way people run SGLang at scale» (11 октября 2026) [18]; у vLLM год прошёл под знаком P/D-коннекторов, KV-offloading и параллельных draft-моделей P-EAGLE, DFlash, DSpark [3, 4, 17].
- **Context rot подтверждён на 800K.** Opus 4.6, GPT 5.4 и Gemini 3.1 как классификаторы пропускают опасное действие в 2–30 раз чаще после 800K токенов безобидной активности (12 мая 2026) [5].
- **Цена фиксированной способности падает ~47 % в квартал, ~13× в год** (Epoch AI, 22 сентября 2026) [19]; DeepSeek-V4.1-Flash — ¥2/¥8 за 1M входных/выходных токенов в пик, попадание в кэш — ¥0,04 [16].

## Что осталось верным

- Определение LLM и decoder-only с next-token prediction; модели 2026 года описывают теми же словами — всего/активных параметров, router, top-k экспертов [1, 22].
- Логика MoE: эксперты на месте FFN, потокенная маршрутизация, борьба с routing collapse. DeepSeek-V4 по-прежнему строится на fine-grained и shared experts с auxiliary-loss-free балансировкой (плюс небольшой sequence-wise loss) [1].
- Математика greedy / beam search / сэмплирования и вывод про температуру — неизменны; изменилось лишь то, кто крутит ручку.
- Guided decoding гарантирует только синтаксис: Anthropic перечисляет исключения — refusal, обрезка по `max_tokens`, регистр enum [14].
- Инференс memory-bound; KV cache, GQA, PagedAttention, prefix caching и speculative decoding остаются основой, новые приёмы (FP8-кэш, offloading, P/D) бьют в ту же память [3].
- Недетерминизм при $T=0$: Anthropic пишет, что `temperature = 0` «never guaranteed identical outputs» [11]; vLLM добавил режим `VLLM_BATCH_INVARIANT=1` ценой скорости [25].
- Замечание Shervine (1:16:42), что сильной модели инструкция важнее примеров, стало официальной рекомендацией OpenAI для reasoning-моделей [9].

## Что устарело или сдвинулось

- **Лекция говорит:** top-k, top-p и температура — параметры генерации, которыми управляет пользователь (разделы 9–10, 46:36–1:04:53) → **Сейчас:** у текущих моделей трёх крупнейших провайдеров они убраны или игнорируются; вместо них `effort` (Anthropic), `thinking_level` (Google), `reasoning_effort` (OpenAI) — ручка «сколько думать», а не «насколько острый softmax» [10, 11, 15]. Для открытых моделей в vLLM/SGLang все ручки на месте.
- **Лекция говорит:** в sparse MoE активируется один, иногда два эксперта (раздел 6, 15:47) → **Сейчас:** сотни мелких экспертов с top-8…16 плюс общие: Kimi K3 — 896 экспертов, 16 + 2 shared [22]; Muse Spark Open — 256 экспертов, top-8 (вторичный источник) [26]. DeepSeek-V4 добавил hash-маршрутизацию в первых блоках [1].
- **Лекция говорит:** «сотни миллиардов параметров», Switch Transformer как пример триллиона (разделы 3, 6) → **Сейчас:** открытые 1,6T, 2,4T и 2,8T при 49B, 95B и 104B активных — доля активных 3–4 % [1, 21, 22].
- **Лекция говорит:** GQA — стандарт, MLA — способ DeepSeek сжать кэш (разделы 15–16, 1:37:56) → **Сейчас:** DeepSeek-V4 описывает CSA (сжатие KV каждые m токенов плюс разреженный отбор) и HCA (сильное сжатие при плотном attention), хранит KV в FP8 и оценивает кэш примерно в 2 % от базы BF16-GQA8 [1]; Kimi K3 оставил MLA в 24 из 93 слоёв, остальные 69 — линейное KDA [22]; Qwen3.5/3.8 — Gated DeltaNet + MoE [21].
- **Лекция говорит:** speculative decoding — отдельная draft-модель, MTP — её встроенный вариант (раздел 16, 1:42:36) → **Сейчас:** драфты стали параллельными: P-EAGLE выдаёт несколько draft-токенов за проход (vLLM, 13 марта 2026; до 1,69× к EAGLE-3 на B200 по бенчмарку самого vLLM) [4]; DSpark (DeepSeek, 6 июля 2026) подбирает длину проверки по уверенности и в production DeepSeek-V4 заменил MTP-1, ускорив генерацию на пользователя на 60–85 % при той же пропускной способности [17]. Правило accept/reject из лекции внутри то же.
- **Лекция говорит:** vLLM — PagedAttention в одном сервере (раздел 16, 1:33:09) → **Сейчас:** prefill и decode живут на разных узлах, KV передаётся по RDMA (push-based NIXL-коннектор, 14 октября 2026), кэш вытесняется в host-память и object store (10 сентября 2026), экспертов масштабируют без рестарта (Elastic EP, 14 мая 2026) [3]; SGLang считает P/D умолчанием для больших инсталляций [18].
- **Лекция говорит:** guided decoding — FSM и грамматики, в API «попросить JSON и перепроверить» (раздел 11, 1:04:53) → **Сейчас:** structured outputs у Anthropic прошли путь от беты (`structured-outputs-2025-11-13`) до стабильного `output_config.format`: схема компилируется в грамматику, кэш грамматики живёт 24 часа, рекурсивные схемы и числовые ограничения не поддерживаются [14]; prefill ответа на Opus 5.5 отклоняется, замена — structured outputs [11]. В vLLM они включены по умолчанию, lm-format-enforcer deprecated с v0.33.0 [24].

## Новое, о чём лекция не знала

- **DeepSeek-V4 (апрель 2026; отчёт arXiv 2606.19348).** Два MoE с контекстом 1M, обученные на 33T и 32T токенов; кроме CSA/HCA — Manifold-Constrained Hyper-Connections и оптимизатор Muon; MTP-модули из V3 без изменений. На 1M токенов Pro тратит 27 % FLOPs и 10 % KV-кэша от V3.2, Flash — 10 % и 7 % [1]. Веса под MIT [2].
- **Гибриды линейного внимания с MoE.** Qwen3.5 (16 февраля 2026, первая модель 397B-A17B) строится на Gated DeltaNet и sparse MoE, Qwen3.8-2.4T-A95B вышел 12 августа 2026 под Apache-2.0 [21]; Kimi K3 — 2,8T/104B с quantization-aware training в MXFP4 [22]; Nemotron 3 Ultra — 550B/55B на Mamba-2 + Transformer, MiniMax M3 — 428B/23B, оба с 1M [2]. Вопрос «как уменьшить KV-кэш» (раздел 15) теперь решают заменой части слоёв на состояние постоянного размера.
- **Meta Muse Spark Open (15 октября 2026).** 816B MoE с контекстом 1M (день-0 пост vLLM) [3]; около 42B активных и 256 экспертов top-8 — по вторичным источникам, карточкой модели не удалось подтвердить [26].
- **Context rot как свойство агентов.** Martin и Roger (12 мая 2026): напоминания в транскрипте помогают частично, дообучение GPT-4.1 на длинном контексте — нет [5]. Xia et al. (29 июня 2026): в долгом поиске модели сдаются на решаемых задачах задолго до заполнения окна; снижение пикового контекста (compaction, offloading) работает как test-time scaling [6].
- **CoT после «точки commitment».** Scalena et al. (11 июня 2026): в reasoning-моделях ответ фиксируется в один шаг задолго до конца рассуждения; ранний выход сокращает CoT до 55 % без потери качества [7]. Вместе с отчётом Wharton (июнь 2025: CoT-промпт у reasoning-моделей даёт незначительный прирост, у старых и малых — заметный) [8] это закрывает вопрос «нужен ли CoT-промпт».
- **Экономика.** Epoch AI: при первом достижении SOTA цена падает ~66 % в квартал, через два года — ~32 %; задача GPQA Diamond на уровне 75 % подешевела с ~$0,30 до ~$0,0004 за полтора года [19]. Du (30 марта 2026): ~600× за 2020–2026, но у флагманов экспоненты нет из-за «reasoning premium» ~31,5× [20]. Открытый Mistral Large 3 (675B/41B, 2 декабря 2025) стоит $0,5/$1,5 за 1M [23].

## Что это меняет для читателя

- Не закладывайте `temperature`/`top_p` в код для фронтирных API: на Claude 5.x, Gemini 3.6+ и GPT-6 они отклоняются или игнорируются. Глубину рассуждения и цену регулирует `effort`/`thinking_level`, формат — structured outputs, воспроизводимость — промпт и проверки [10, 11, 15].
- Для открытых моделей ручки остались, но движок может включать speculative decoding и structured outputs по умолчанию — проверяйте конфигурацию [24].
- Окно 1M не отменяет context rot: в агентах планируйте compaction и retrieval, а стабильный префикс держите неизменным — у DeepSeek попадание в кэш дешевле промаха в 50 раз [5, 6, 16].
- CoT-промпт оставьте малым и не-reasoning моделям; reasoning-моделям дайте инструкцию и критерии успеха, few-shot — только при строгом формате [8, 9].
- Self-hosting MoE: память определяется суммарным размером — 2,8T весов Kimi K3 даже в 4 битах занимают ~1,4 ТБ, поэтому expert parallelism на несколько узлов, P/D-дезагрегация и draft-модель EAGLE-3/DSpark — штатный набор vLLM и SGLang [3, 18, 22].
- Бюджет считайте по токенам на задачу: цена токена падает ~13× в год, но reasoning-режимы и агентные циклы растят расход, а флагманы дешевеют медленнее [19, 20].

## Проверка пометок в конспекте

- **«В API крупных провайдеров `temperature` и `top_p` (иногда и `top_k`) — параметры каждого запроса…»** (раздел 10) — устарело для текущих моделей: Anthropic (Opus 5.5, Fable 5.1) просит их не передавать, Google для Gemini 3.6 игнорирует и обещает 400, OpenAI запрещает при reasoning effort ≠ `none` [10, 11, 15]. Часть про `temperature=0` без гарантии воспроизводимости подтверждена Anthropic [11]. «Многие API умеют возвращать `logprobs`» верно для OpenAI только при `none` и для открытых движков; у Messages API Anthropic logprobs нет [10].
- **«Полезно смотреть на генерацию как на поиск в дереве… Поэтому и API отдают именно logprobs»** (раздел 8) — та же неточность про logprobs.
- **«Guided decoding — это то, что в API называется structured outputs…»** (раздел 11) — верно; уточнение: у Anthropic это уже не бета, параметр — `output_config.format`, а lm-format-enforcer в vLLM deprecated [14, 24].
- **«Лектор не даёт формулу размера кэша…»** (раздел 15) — формула верна для GQA-моделей, но не описывает гибриды с линейным вниманием (Kimi K3, Qwen3.5/3.8) и сжатый FP8-кэш DeepSeek-V4 [1, 21, 22].
- **«Правило принятия в субтитрах искажено… Medusa и EAGLE»** (раздел 16) — верно; актуальные имена — EAGLE-3/3.1, P-EAGLE, DFlash, DSpark [3, 4, 17].
- Остальные блоки (DeepSeek-V3 без aux-loss, память MoE, prompt caching, context rot и RAG, SFT против few-shot, CoT → reasoning-модели, «Defeating Nondeterminism») источникам не противоречат; V4 сохранил auxiliary-loss-free балансировку [1].

## Источники

1. DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence — DeepSeek-AI, arXiv 2606.19348 — 2026 (модель вышла в апреле 2026) — https://arxiv.org/html/2606.19348v1
2. The Open Weight Models that Matter: June 2026 — OpenRouter, Chris Clark — 27 июня 2026 — https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026/
3. vLLM Blog (лента постов за октябрь 2025 – ноябрь 2026) — vllm.ai — просмотрено 7 ноября 2026 — https://vllm.ai/blog
4. P-EAGLE: Faster LLM inference with Parallel Speculative Decoding in vLLM — vLLM Blog — 13 марта 2026 — https://vllm.ai/blog/2026-03-13-p-eagle
5. Classifier Context Rot: Monitor Performance Degrades with Context Length — Sam Martin, Fabien Roger, arXiv 2605.12366 — 12 мая 2026 — https://arxiv.org/abs/2605.12366
6. Diagnosing and Mitigating Context Rot in Long-horizon Search — Shijie Xia et al., arXiv 2606.29718 — 29 июня 2026 (v3 от 25 октября 2026) — https://arxiv.org/abs/2606.29718
7. Beyond the Commitment Boundary: Probing Epiphenomenal Chain-of-Thought in Large Reasoning Models — Daniel Scalena et al., arXiv 2606.13603 — 11 июня 2026 — https://arxiv.org/abs/2606.13603
8. Prompting Science Report 2: The Decreasing Value of Chain of Thought in Prompting — Meincke et al. (Wharton), arXiv 2506.07142 — июнь 2025 — https://arxiv.org/pdf/2506.07142
9. Reasoning best practices — OpenAI API docs — состояние на 7 ноября 2026 — https://developers.openai.com/api/docs/guides/reasoning-best-practices
10. Latest model: migration quickstart, unsupported parameters — OpenAI API docs — состояние на 7 ноября 2026 — https://developers.openai.com/api/docs/guides/latest-model
11. Claude Opus 5.5 migration guide — Anthropic Claude Platform docs — состояние на 7 ноября 2026 — https://platform.claude.com/docs/en/models/opus-5-5/migration-guide
12. Claude Fable 5.1 and Claude Mythos 5.1 migration guide — Anthropic — состояние на 7 ноября 2026 — https://platform.claude.com/docs/en/models/fable-5-1/migration-guide
13. Troubleshooting thinking (таблица режимов thinking по моделям) — Anthropic — состояние на 7 ноября 2026 — https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting
14. Structured outputs — Anthropic Claude Platform docs — состояние на 7 ноября 2026 — https://platform.claude.com/docs/en/build-with-claude/structured-outputs
15. What's new in Gemini 3.6 (раздел «Sampling parameter deprecation») — Google AI Studio docs — состояние на 7 ноября 2026 — https://aistudio.google.com/docs/whats-new-gemini-3.6
16. Models & Pricing — DeepSeek API docs — состояние на 7 ноября 2026 — https://api-docs.deepseek.com/zh-cn/quick_start/pricing
17. DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation — Xin Cheng et al. (DeepSeek), arXiv 2607.05147 — 6 июля 2026 — https://arxiv.org/abs/2607.05147
18. [Roadmap] Prefill-Decode Disaggregation Roadmap (2026 Q4) — sgl-project/sglang, issue #43699 — 11 октября 2026 — https://github.com/sgl-project/sglang/issues/43699
19. The plunging price of thought — Luke Emberson, David Roodman, Epoch AI — 22 сентября 2026 — https://epoch.ai/publications/the-plunging-price-of-thought
20. Tiered Super-Moore's Law: Price Evolution, Production Frontiers, and Market Competition in LLM Inference Services — Mingdeng Du, arXiv 2603.28576 — 30 марта 2026 — https://arxiv.org/abs/2603.28576
21. Qwen3.8 — QwenLM, GitHub README — состояние на 7 ноября 2026 — https://github.com/QwenLM/Qwen3.8
22. Kimi-K3 model card — Moonshot AI, Hugging Face — состояние на 7 ноября 2026 — https://huggingface.co/moonshotai/Kimi-K3
23. Mistral Large 3 — Mistral AI docs — релиз 2 декабря 2025 — https://docs.mistral.ai/models/mistral-large-3-25-12.md
24. Structured Outputs — vLLM docs — состояние на 7 ноября 2026 — https://docs.vllm.ai/en/latest/features/structured_outputs/
25. Batch Invariance — vLLM docs — состояние на 7 ноября 2026 — https://docs.vllm.ai/en/stable/features/batch_invariance/
26. Muse Spark Open Weights: 816B Model, Benchmarks, and How to Run It — developersdigest.tech (вторичный источник) — октябрь 2026 — https://www.developersdigest.tech/blog/muse-spark-open-weights-816b-run-it-2026
