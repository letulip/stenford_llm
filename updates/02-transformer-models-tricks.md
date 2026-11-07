# Лекция 2. Модели на базе трансформера и инженерные приёмы — что изменилось к ноябрю 2026

*Лекция прочитана 3 октября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/02-transformer-models-tricks.md) · [Все актуализации](index.md)

## Коротко

- Квадратичный attention в проде обходят тремя путями сразу: локально-глобальные окна (Gemma 4, схема 5:1, апрель 2026 [9]), выученный разреженный отбор токенов (DeepSeek-V3.2, декабрь 2025 [1]; GLM-5 [7]) и гибриды с линейным attention (Qwen3.5, февраль 2026 [6]; Kimi K3, июль 2026 [4]).
- RoPE перестал быть безальтернативным: Kimi K3 вовсе без RoPE — NoPE во всех MLA-слоях при контексте 1M [4]; Qwen3-Next/3.5 поворачивают четверть размерностей головы [5][6]; Gemma 4 ввела p-RoPE в глобальных слоях [9].
- MLA вышла за пределы DeepSeek: Kimi K2/K3, GLM-5, Mistral Large 3, Sarvam [7]. DeepSeek-V4 (2026) заявляет при 1M контекста 10 % KV-кэша и 27 % FLOPs на токен от уровня V3.2 [3].
- RMSNorm остался, «pre-norm как стандарт» — нет: OLMo 2/3 нормируют после подслоя, Gemma 3/4 — до и после; почти везде добавился QK-norm [7]. «Cracks in the Foundation» (август 2026): такие «мелочи» меняют расширяемость контекста до 47 % [11].
- Encoder-only модели живы: UltraBERT (октябрь 2026) — 150M/380M с нативными 32K [13]; Ettin (ICLR 2026): при одинаковом рецепте encoder сильнее decoder'а в классификации и поиске [14].
- Дистилляция сместилась к on-policy: учитель потокенно оценивает собственные выборки ученика (Thinking Machines, октябрь 2025 [17]); к лету 2026 это типичный этап post-training открытых моделей [19].

## Что осталось верным

- Каркас 2017 года — основа всех моделей из источников; менялись те же три узла: позиции, нормализация, attention.
- RoPE — умолчание: в галерее из 119 архитектур альтернатива ему только NoPE-гибриды; ALiBi и T5-bias в моделях 2025–2026 не встретились. RMSNorm вместо LayerNorm — без исключений [7].
- GQA — типичный выбор плотных моделей среднего размера: Llama 3, Gemma 3/4, Qwen3, gpt-oss [7]. Формула KV-кэша и связь с prompt caching верны: Claude API отдаёт кэшированные входные токены за 10 % базовой цены (2,5–5 % у моделей 5.x) [20].
- BERT-подобные encoder'ы остаются рабочей лошадкой классификации; авторы UltraBERT называют их самым экономичным способом обрабатывать текст в объёме [13]. Предел 512 у BERT, MLM 15 % и 80/10/10, RoBERTa без NSP — пересматривать нечего.

## Что устарело или сдвинулось

- **Лекция говорит:** RoPE используют «почти все современные модели» (раздел 6, 37:26) → **Сейчас:** доминирует, но появились гибриды: SmolLM3 (июнь 2025) убирает RoPE в каждом четвёртом слое; Kimi Linear, Tiny Aya, Trinity, Sarvam (2025–2026) держат RoPE в локальных слоях, NoPE — в глобальных; Kimi K3 (2,8T параметров, 1M контекста) применяет NoPE ко всем MLA-слоям, позицию даёт рекуррентность KDA-слоёв [4][7]. Qwen3-Next/3.5 вращают лишь 64 из 256 размерностей головы [5][6].
- **Лекция говорит:** окно sliding window — «порядка нескольких тысяч» токенов, Mistral — SWA на каждом слое (раздел 8, 53:24–54:22) → **Сейчас:** окна меньше, слои чередуются: Gemma 3/4 — 1024 токена (512 у E2B/E4B) при 5 локальных : 1 глобальный [9]; gpt-oss — 128 токенов в каждом втором слое [10]. Сама Mistral от SWA ушла: Small 3.1 его убрала, Large 3 (декабрь 2025) построена на MLA [7].
- **Лекция говорит:** в недавних моделях «типично GQA» (раздел 9, 1:01:01) → **Сейчас:** у флагманских открытых MoE типичнее MLA (DeepSeek, Kimi K2/K3, GLM-5, Mistral Large 3) [7]; в Qwen3.5 attention-слоёв 15 из 60, остальные — Gated DeltaNet [6]. GQA остался в плотных моделях.
- **Лекция говорит:** pre-norm + RMSNorm — стандарт (раздел 7, 45:38) → **Сейчас:** RMSNorm — да, размещение разошлось: OLMo 2/3 — post-norm внутри residual, Gemma 3/4 — RMSNorm до и после подслоя [7][9]. Добавился QK-norm (RMSNorm на query и key перед RoPE): OLMo 2/3, Gemma 3/4, Qwen3, GLM-4.5, MiniMax M2; Cohere в Tiny Aya от него отказалась из-за взаимодействия с длинным контекстом [7].
- **Лекция говорит:** sparse attention — это фиксированное окно (раздел 8, 50:39) → **Сейчас:** DeepSeek-V3.2 заменила окно выученным отбором: лёгкий lightning indexer (ReLU, мало голов, FP8) оценивает все предыдущие токены, и в основную MLA-attention (режим MQA) попадают 2048 лучших; ядро — O(L·k) при 128K [1]. GLM-5 взяла DSA [7]; статья от 2 ноября 2026: узким местом стал сам индексатор, переиспользование его выбора между соседними слоями даёт до +14,5 % к декодированию [2].
- **Лекция говорит:** окно контекста задают RoPE и длина обучения (💡 к разделу 3) → **Сейчас:** 1M токенов у всех текущих моделей Claude [20], Gemini 4 Argon [21], DeepSeek-V4 [3], Kimi K3 [4]; Qwen3.5 — 262K нативно и ~1,01M через YaRN с предупреждением, что статический YaRN портит короткие тексты [6]. Обзоры оценивают рабочую долю окна в 60–70 % от заявленного [22]; обзор позиционного кодирования (август 2026): умение посчитать позицию за пределами обучения не гарантирует надёжной работы там [12].

## Новое, о чём лекция не знала

- **DeepSeek-V4.** Preview (V4-Pro 1,6T/49B активных, V4-Flash 284B/13B, 1M контекста) заменяет DSA гибридом Compressed Sparse Attention и Heavily Compressed Attention, добавляет Manifold-Constrained Hyper-Connections вместо residual и оптимизатор Muon; заявлено 10 % KV-кэша и 27 % FLOPs на токен относительно V3.2 на 1M [3]. Дату (апрель или июнь 2026) подтвердить не удалось.
- **Гибриды с линейным attention.** Qwen3-Next (сентябрь 2025, 80B-A3B): три слоя Gated DeltaNet на один слой gated attention, 262K нативно [5]; Qwen3.5 (16 февраля 2026) перенёс схему во флагман [6]. Kimi K3: 3 Kimi Delta Attention : 1 gated MLA (69 + 24 слоя), «Attention Residuals» — attention по глубине вместо единого residual-потока, ~2,5× эффективности масштабирования против K2, контекст доращивался 8K→64K→256K→1M [4]. Nemotron 3 (Mamba-2), Ling 2.5 — та же идея [7]; без парных абляций выигрыш нельзя приписать схеме [8].
- **Gemma 4** (2 апреля 2026; от E2B до 31B, 128K/256K, Apache 2.0): 5:1, последний слой всегда глобальный; в глобальных слоях 4 KV-головы с «unified keys and values» и Proportional RoPE (p-RoPE) — механизм в карте модели не раскрыт [9].
- **Что мешает длинному контексту.** «Cracks in the Foundation» (AI2/CMU, 10 августа 2026, COLM): четыре «мелких» решения — нормализация, GQA, длина предобучения, sliding window — порознь незаметны, а втроём снижают качество на длинном контексте до 47 % [11]. Контртренд: MiniMax M2.5 сознательно избегает и окон, и линейных гибридов [7].
- **Encoder'ы 2025–2026.** mmBERT (сентябрь 2025): мультиязычный encoder, 3T токенов, 1800+ языков [15]. Ettin (июль 2025, ICLR 2026): парные encoder/decoder 17M–1B на одном рецепте — encoder'ы сильнее в классификации и поиске, decoder'ы в генерации, а «переделка» одного в другой хуже обучения с нужной целью [14]. UltraBERT (14 октября 2026): 150M/380M, нативные 32K, два режима маскирования и дистилляция от 1,3B учителя; GLUE 89,5 против 88,4 у ModernBERT; UltraBERT-Embed-150M — 67,24 на MTEB(eng, v2) [13].
- **Embeddings.** Верх рейтингов — модели на decoder-основе: Qwen3-Embedding (0.6B/4B/8B на Qwen3, июнь 2025) [16], NV-Embed-v2 на Mistral-7B, Gemini Embedding [23][24]; компактные encoder'ы (UltraBERT-Embed, nomic, MiniLM) остаются выбором по цене [13][24].
- **On-policy distillation.** Thinking Machines (27 октября 2025): ученик генерирует сам, учитель даёт потокенный reverse-KL; на AIME'24 — 74,4 % за ~1800 GPU-часов против 67,6 % у RL за 17 920 (RL-цифры из отчёта Qwen3) [17]. Обзор OPD — апрель 2026 [18]; к июлю 2026 Xiaomi, Zhipu (GLM-5), Ant обучают специалистов через RL и сливают их через OPD [19]. Ограничения: далёкий учитель вызывает коллапс энтропии [19]; ученики 0.6–4B не умеют вовремя остановиться [25].
- **KV-кэш как инфраструктура.** Prefix caching, выгрузка блоков в CPU/NVMe (vLLM, SGLang HiCache, LMCache с ярусами CPU/FS/S3), FP8-кэш, разнесение prefill/decode по машинам [26][27].

## Что это меняет для читателя

- Заявленный 1M контекста — не гарантия: проверяйте качество на своих длинах; оценка рабочей доли окна — 60–70 % [22].
- Prompt caching стал дешевле и важнее: держите стабильный префикс; на Claude чтение из кэша — 2,5–10 % цены входа [20].
- Выбирая открытую модель, читайте config: число KV-голов, тип attention (GQA/MLA/гибрид), окно SWA и RoPE/YaRN-настройки определяют память и поведение на длине; статический YaRN включайте, только когда вход превышает нативное окно [6].
- Для классификации и поиска берите encoder (UltraBERT, ModernBERT, mmBERT): дообучается на CPU-бюджете и выигрывает у decoder'а того же размера [13][14]; за максимальным качеством embeddings — к decoder-моделям вроде Qwen3-Embedding [16].
- Рецепт «дорогая модель размечает данные» работает, но on-policy вариант даёт больше за меньший compute [17][19]. Архитектурные «мелочи» решают, расширится ли контекст при дообучении [11] — аргумент за семейства с проверенной расширяемостью.

## Проверка пометок в конспекте

- «**Дополнение — что изменилось с тех пор:** „Фиксированный“ θ…» (раздел 6): «основной способ… контекст в сотни тысяч токенов» — слишком сильно. YaRN используют (Qwen3-Next/3.5 [5][6]), но 1M у Kimi K3 и DeepSeek-V4 получены обучением до 1M [3][4], а K3 обходится без RoPE. Точнее — «один из основных способов».
- «**Дополнение — уточнение:** Лектор не объяснил, почему pre-norm победил…» (раздел 7): история верна, но «pre-norm — стандарт» уже не универсально: OLMo 2/3 — post-norm, Gemma 3/4 — pre+post; не упомянут QK-norm [7][9].
- «**Дополнение — на практике:** Разработчику, который работает с моделями через API…» (раздел 9): «почти поголовно GQA… MLA в моделях DeepSeek» — устарело: MLA в Kimi K2/K3, GLM-5, Mistral Large 3 [7], флагманы Qwen — гибриды [6]. Про GQA верно только для плотных моделей.
- «**Дополнение — на практике:** „Хитрости с tiling“…» (раздел 8): FlashAttention и rolling-кэш описаны верно, но это Mistral 7B 2023 года — новые модели Mistral SWA не используют [7].
- «**Дополнение — на практике:** Для инженера эта карта…» (раздел 10): «модели embeddings для поиска» как пример encoder-only неточно — лидеры MTEB построены на decoder'ах [16][23][24]; encoder'ы — в компактном сегменте [13].
- «**Дополнение — что изменилось с тех пор:** Дистилляция давно вышла…» (раздел 13): верно, но не хватает on-policy distillation как основного рецепта 2026 года [17][19].
- Остальные пометки (разделы 3, 4, 5, пример в 9, 11, 12) противоречий с источниками не имеют.

## Источники

1. DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models — DeepSeek-AI, arXiv 2512.02556 — 2 декабря 2025 — https://arxiv.org/abs/2512.02556 (разбор DSA по https://arxiv.org/html/2512.02556)
2. Multi-layer Indexer: Overlapping Selection and Attention in DeepSeek Sparse Attention — Dilbaz et al., arXiv 2611.03768 — 2 ноября 2026 — https://arxiv.org/abs/2611.03768
3. DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence — DeepSeek-AI, arXiv 2606.19348 — 2026 (на странице: 26 апреля 2026) — https://arxiv.org/abs/2606.19348
4. Kimi K3: Open Frontier Intelligence — Kimi Team, arXiv 2607.24653 — 27 июля 2026 (v2 7 августа 2026) — https://arxiv.org/abs/2607.24653 и https://arxiv.org/html/2607.24653v1
5. Qwen3-Next-80B-A3B-Instruct, карта модели — Qwen / Hugging Face — сентябрь 2025 — https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct
6. Qwen3.5-397B-A17B, карта модели — Qwen / Hugging Face — февраль 2026 — https://huggingface.co/Qwen/Qwen3.5-397B-A17B
7. LLM Architecture Gallery (индекс, страницы NoPE, QK-Norm, Hybrid Attention) — Sebastian Raschka — 2026 — https://sebastianraschka.com/llm-architecture-gallery/
8. Hybrid Attention — Sebastian Raschka, LLM Architecture Gallery — 2026 — https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/
9. Gemma 4 Architecture and Benchmark Notes — Sebastian Raschka — 2 апреля 2026 — https://sebastianraschka.com/blog/2026/gemma-4-release-notes.html; Gemma 4 model card — Google AI for Developers — 2026 — https://ai.google.dev/gemma/docs/core/model_card_4
10. From GPT-2 to gpt-oss: Analyzing the Architectural Advances — Sebastian Raschka — 9 августа 2025 — https://magazine.sebastianraschka.com/p/from-gpt-2-to-gpt-oss-analyzing-the
11. Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension — Bertsch et al. (AI2/CMU), arXiv 2608.10296 — 10 августа 2026 — https://arxiv.org/abs/2608.10296
12. Position Encoding in Transformers: From Absolute and Relative Methods to Rotary Position Embeddings and Long-Context Scaling — Jiguo Li, arXiv 2608.10021 — 9 августа 2026 — https://arxiv.org/abs/2608.10021
13. UltraBERT: One Encoder for Classification and Retrieval — dmis-lab, блог Hugging Face — 14 октября 2026 — https://huggingface.co/blog/dmis-lab/ultrabert
14. Seq vs Seq: An Open Suite of Paired Encoders and Decoders (Ettin) — Weller et al., arXiv 2507.11412 — 15 июля 2025 (v2 12 марта 2026, ICLR 2026) — https://arxiv.org/abs/2507.11412
15. mmBERT: A Modern Multilingual Encoder with Annealed Language Learning — Marone et al., arXiv 2509.06888 — 8 сентября 2025 — https://arxiv.org/abs/2509.06888
16. Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models — Zhang et al., arXiv 2506.05176 — 5 июня 2025 — https://arxiv.org/abs/2506.05176
17. On-Policy Distillation — Kevin Lu, Thinking Machines Lab — 27 октября 2025 — https://thinkingmachines.ai/blog/on-policy-distillation/
18. A Survey of On-Policy Distillation for Large Language Models — Song, Zheng, arXiv 2604.00626 — 1 апреля 2026 (v5 21 октября 2026) — https://arxiv.org/abs/2604.00626
19. On-policy distillation, part 1: the 2026 open-model post-training shift — VESSL AI — 8 июля 2026 — https://vessl.ai/en/blog/on-policy-distillation-part-1
20. Models overview — Claude Platform docs (Anthropic) — прочитано 7 ноября 2026 — https://platform.claude.com/docs/en/about-claude/models/overview
21. Models — Google AI Studio docs — прочитано 7 ноября 2026 — https://aistudio.google.com/docs/models
22. AI Model Context Window Comparison 2026: Advertised vs. Real — elvex — 13 августа 2026 — https://www.elvex.com/blog/context-length-comparison-ai-models-2026
23. Best Embedding Models for RAG (2026) — PremAI — 17 марта 2026 — https://www.premai.io/blog/best-embedding-models-for-rag-2026-ranked-by-mteb-score-cost-and-self-hosting/
24. Top 10 Embedding Models for RAG in 2026 — Hussain Nazary — 8 августа 2026 — https://hussain-nazary.github.io/top-10-embedding-models-2026.html
25. Solving Without Stopping: On-Policy Distillation at Small Scale — arXiv 2609.37326 — сентябрь 2026 — https://arxiv.org/pdf/2609.37326
26. KV Cache Offloading — vLLM production-stack docs — 2026 — https://docs.vllm.ai/projects/production-stack/en/vllm-stack-0.1.2/tutorials/kv_cache.html
27. KV cache offloading — LLM Inference Handbook, Modular — 2026 — https://handbook.modular.com/inference-optimization/kv-cache-offloading/
