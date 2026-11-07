# Stanford CME295 — Transformers & Large Language Models (осень 2025)

Конспекты девяти лекций курса Stanford CME295 «Transformers & LLMs» на русском языке, собранные из официальных субтитров видео Stanford Online на YouTube. Курс читают **Afshine Amidi** и **Shervine Amidi** (братья-близнецы; работают над LLM в Netflix, до этого Google и Uber; adjunct lecturers в Stanford). Курс идёт от устройства трансформера через обучение и дообучение LLM к reasoning-моделям, агентам и оценке качества.

- **Плейлист:** https://www.youtube.com/playlist?list=PLoROMvodv4rOCXd21gf0CF4xr35yINeOy
- **Сайт курса и программа:** https://cme295.stanford.edu/syllabus/
- **Канал:** Stanford Online
- **Репозиторий:** https://github.com/letulip/stenford_llm
- **Сайт (GitHub Pages):** https://letulip.github.io/stenford_llm/

## Как пользоваться

| Папка | Что внутри | Когда открывать |
|---|---|---|
| [`lectures/`](lectures/) | Конспекты на русском: по одному файлу на лекцию, разделы повторяют главы видео, у каждого раздела таймкод и ссылка на YouTube, в конце термины, выводы и вопросы из зала | Начинать отсюда |
| [`transcripts/`](transcripts/) | Полный английский текст субтитров, разбитый по главам; каждый абзац начинается с кликабельного таймкода | Когда нужно прочитать, что именно сказал лектор |
| [`raw/`](raw/) | Исходные VTT-субтитры и метаданные видео (json), включая [`raw/index.json`](raw/index.json) со списком глав | Если захочется переобработать |

Все таймкоды в конспектах и транскриптах кликабельны и открывают нужный момент видео.

### Пометки-дополнения в конспектах

Внутри конспектов встречаются блоки вида

> 💡 **Дополнение — пример:** …

Это **не слова лекторов**, а добавления составителя конспекта: дополнительный пример, более сильная интуиция или аналогия, связь с другой лекцией курса, практическое следствие для разработчика, оговорка или уточнение. Всё, что вне таких блоков, пересказывает содержание лекции. В конце каждого конспекта есть раздел «Чем можно дополнить» со списком тем, которых лекция не касается, но которые стоит знать рядом с ней.

## Лекции

### [Лекция 1. Трансформер](lectures/01-transformer.md)

*Transformer* · 26 сентября 2025 · 101 мин · [видео](https://youtu.be/Ub3GoFaUcds) · [транскрипт](transcripts/01-transformer.md)

Путь от сырого текста до трансформера: три класса задач NLP и их метрики (precision/recall/F1, BLEU/ROUGE, perplexity), токенизация (слова, подслова, символы, OOV), представление токенов от one-hot до обучаемых embeddings через proxy-задачу Word2vec, затем RNN/LSTM и их проблемы (vanishing gradient, дальние зависимости, последовательность вычислений). Отсюда выводится attention как прямая связь с прошлым и self-attention с query/key/value, а в финале Shervine по шагам разбирает encoder–decoder архитектуру «Attention is All You Need»: формулу softmax(QKᵀ/√d_k)V, multi-head, masked и cross-attention, positional encoding, label smoothing и генерацию токен за токеном до EOS. Сквозной пример курса — фраза «a cute teddy bear is reading».

**Главы:** [Introduction](https://youtu.be/Ub3GoFaUcds?t=0) (00:00) · [Class logistics](https://youtu.be/Ub3GoFaUcds?t=234) (03:54) · [NLP overview](https://youtu.be/Ub3GoFaUcds?t=580) (09:40) · [Tokenization](https://youtu.be/Ub3GoFaUcds?t=1377) (22:57) · [Word representation](https://youtu.be/Ub3GoFaUcds?t=1828) (30:28) · [Recurrent neural networks](https://youtu.be/Ub3GoFaUcds?t=3203) (53:23) · [Self-attention mechanism](https://youtu.be/Ub3GoFaUcds?t=4007) (1:06:47) · [Transformer architecture](https://youtu.be/Ub3GoFaUcds?t=4433) (1:13:53) · [Detailed example](https://youtu.be/Ub3GoFaUcds?t=5393) (1:29:53)

### [Лекция 2. Модели на базе трансформера и инженерные приёмы](lectures/02-transformer-models-tricks.md)

*Transformer-Based Models & Tricks* · 3 октября 2025 · 107 мин · [видео](https://youtu.be/yT84Y5zCnaA) · [транскрипт](transcripts/02-transformer-models-tricks.md)

Какие части трансформера 2017 года изменились в современных моделях: позиционное кодирование (от выученных и синусоидальных embeddings к T5 bias, ALiBi и RoPE), нормализация (pre-norm и RMSNorm вместо post-norm и LayerNorm) и приёмы удешевления attention — sliding window attention и общие проекции key/value (MQA, GQA) ради меньшего KV-кэша. Во второй части — карта семейств encoder-decoder / encoder-only / decoder-only (T5 и span corruption, почему победили decoder-only) и подробный разбор BERT: двунаправленность, токены [CLS]/[SEP], предобучение на MLM и NSP, fine-tuning под классификацию и QA, затем DistilBERT (дистилляция) и RoBERTa (отказ от NSP, динамическое маскирование).

**Главы:** [Introduction](https://youtu.be/yT84Y5zCnaA?t=0) (00:00) · [Recap of Transformers](https://youtu.be/yT84Y5zCnaA?t=90) (01:30) · [Overview of position embeddings](https://youtu.be/yT84Y5zCnaA?t=637) (10:37) · [Sinusoidal embeddings](https://youtu.be/yT84Y5zCnaA?t=936) (15:36) · [T5 bias, ALiBi](https://youtu.be/yT84Y5zCnaA?t=1556) (25:56) · [RoPE](https://youtu.be/yT84Y5zCnaA?t=1862) (31:02) · [Layer normalization](https://youtu.be/yT84Y5zCnaA?t=2622) (43:42) · [Sparse attention](https://youtu.be/yT84Y5zCnaA?t=3039) (50:39) · [Sharing attention heads](https://youtu.be/yT84Y5zCnaA?t=3338) (55:38) · [Transformer-based models](https://youtu.be/yT84Y5zCnaA?t=3762) (1:02:42) · [BERT deep dive](https://youtu.be/yT84Y5zCnaA?t=4298) (1:11:38) · [BERT finetuning](https://youtu.be/yT84Y5zCnaA?t=5604) (1:33:24) · [Extensions of BERT](https://youtu.be/yT84Y5zCnaA?t=6210) (1:43:30)

### [Лекция 3. Большие языковые модели: MoE, декодирование, промптинг](lectures/03-llms-moe-decoding-prompting.md)

*Transformers & Large Language Models* · 10 октября 2025 · 108 мин · [видео](https://youtu.be/Q5baLehv5So) · [транскрипт](transcripts/03-llms-moe-decoding-prompting.md)

Что такое LLM (языковая модель, «большая» по параметрам, данным и compute; почти все современные — decoder-only) и как устроен Mixture of Experts: dense и sparse MoE, замена feedforward-блока экспертами с token-level router'ом, routing collapse и балансирующий loss, активные параметры. Вторая часть — как из распределения над словарём получается текст: greedy decoding, beam search, сэмплирование с top-k/top-p, температура в softmax (с выводом на доске) и guided decoding для JSON. Третья часть (Shervine) — context length и context rot, структура prompt'а, in-context learning, chain-of-thought и self-consistency, а также оптимизации инференса: KV cache, GQA, PagedAttention/vLLM, multi-head latent attention (DeepSeek), speculative decoding и multi-token prediction.

**Главы:** [Introduction](https://youtu.be/Q5baLehv5So?t=0) (00:00) · [Recap of Transformers-based models](https://youtu.be/Q5baLehv5So?t=62) (01:02) · [LLM definition](https://youtu.be/Q5baLehv5So?t=223) (03:43) · [Mixture of Experts](https://youtu.be/Q5baLehv5So?t=457) (07:37) · [Dense & Sparse MoE](https://youtu.be/Q5baLehv5So?t=763) (12:43) · [MoE in LLMs](https://youtu.be/Q5baLehv5So?t=947) (15:47) · [Response generation](https://youtu.be/Q5baLehv5So?t=2195) (36:35) · [Greedy decoding & beam search](https://youtu.be/Q5baLehv5So?t=2314) (38:34) · [Sampling-based methods](https://youtu.be/Q5baLehv5So?t=2796) (46:36) · [Impact of temperature on predictions](https://youtu.be/Q5baLehv5So?t=3144) (52:24) · [Guided decoding](https://youtu.be/Q5baLehv5So?t=3893) (1:04:53) · [Prompting strategies](https://youtu.be/Q5baLehv5So?t=4027) (1:07:07) · [In-context learning](https://youtu.be/Q5baLehv5So?t=4449) (1:14:09) · [Chain-of-thought, self-consistency](https://youtu.be/Q5baLehv5So?t=4715) (1:18:35) · [Inference optimizations with KV cache](https://youtu.be/Q5baLehv5So?t=5100) (1:25:00) · [PagedAttention, MLA](https://youtu.be/Q5baLehv5So?t=5589) (1:33:09)

### [Лекция 4. Обучение LLM: предобучение, оптимизации, SFT и LoRA](lectures/04-llm-training.md)

*LLM Training* · 17 октября 2025 · 107 мин · [видео](https://youtu.be/VlA_jt_3Qc4) · [транскрипт](transcripts/04-llm-training.md)

Весь конвейер обучения LLM: предобучение на триллионах токенов (FLOPs, scaling laws, закон Chinchilla «20 токенов на параметр», knowledge cutoff), затем инженерия — что занимает память GPU и как её экономят через data parallelism с ZeRO, model parallelism, Flash Attention, квантизацию и mixed precision. Вторая половина (Shervine) — как из предсказателя текста сделать ассистента: SFT и instruction tuning с loss только на ответе, почему данные дороги и как оценивать модели (MMLU, GSM8K, Chatbot Arena и их слабости), и, наконец, LoRA и QLoRA — дообучение через низкоранговые добавки к замороженным (и квантизованным в NF4) весам.

**Главы:** [Introduction](https://youtu.be/VlA_jt_3Qc4?t=0) (00:00) · [Pretraining](https://youtu.be/VlA_jt_3Qc4?t=439) (07:19) · [FLOPs, FLOPS](https://youtu.be/VlA_jt_3Qc4?t=806) (13:26) · [Scaling laws, Chinchilla law](https://youtu.be/VlA_jt_3Qc4?t=994) (16:34) · [Training optimizations overview](https://youtu.be/VlA_jt_3Qc4?t=1489) (24:49) · [Data parallelism with ZeRO](https://youtu.be/VlA_jt_3Qc4?t=1869) (31:09) · [Model parallelism](https://youtu.be/VlA_jt_3Qc4?t=2151) (35:51) · [Flash Attention](https://youtu.be/VlA_jt_3Qc4?t=2306) (38:26) · [Quantization](https://youtu.be/VlA_jt_3Qc4?t=3157) (52:37) · [Mixed precision training](https://youtu.be/VlA_jt_3Qc4?t=3360) (56:00) · [Supervised finetuning](https://youtu.be/VlA_jt_3Qc4?t=3751) (1:02:31) · [Instruction tuning](https://youtu.be/VlA_jt_3Qc4?t=4161) (1:09:21) · [Parameter-efficient finetuning with LoRA](https://youtu.be/VlA_jt_3Qc4?t=5873) (1:37:53) · [QLoRA](https://youtu.be/VlA_jt_3Qc4?t=6316) (1:45:16)

### [Лекция 5. Дообучение LLM на предпочтениях: RLHF, PPO, DPO](lectures/05-llm-tuning-rlhf-dpo.md)

*LLM tuning* · 31 октября 2025 · 107 мин · [видео](https://youtu.be/PmW_TMQ3l0I) · [транскрипт](transcripts/05-llm-tuning-rlhf-dpo.md)

Третий этап обучения LLM — выравнивание с человеческими предпочтениями. Afshine разбирает конвейер RLHF: сбор pairwise-данных, обучение reward model по формулировке Bradley-Terry, RL-шаг с PPO (KL к reference-модели, advantage и value function, варианты Clip и KL-penalty), проблемы RL-подхода и best-of-N как альтернативу без обучения. Shervine выводит DPO из objective PPO — supervised-loss прямо на парах предпочтений без reward model — и сравнивает: PPO сильнее, но тяжёл в настройке, DPO проще и почти так же хорош, но страдает от distribution shift.

**Главы:** [Introduction](https://youtu.be/PmW_TMQ3l0I?t=0) (00:00) · [Preference tuning](https://youtu.be/PmW_TMQ3l0I?t=290) (04:50) · [Data collection](https://youtu.be/PmW_TMQ3l0I?t=691) (11:31) · [RLHF overview](https://youtu.be/PmW_TMQ3l0I?t=1063) (17:43) · [Reward model](https://youtu.be/PmW_TMQ3l0I?t=1704) (28:24) · [Bradley-Terry formulation](https://youtu.be/PmW_TMQ3l0I?t=1786) (29:46) · [Reinforcement learning](https://youtu.be/PmW_TMQ3l0I?t=2762) (46:02) · [PPO](https://youtu.be/PmW_TMQ3l0I?t=3234) (53:54) · [Advantage, value function](https://youtu.be/PmW_TMQ3l0I?t=3476) (57:56) · [PPO variants: Clip, KL-penalty](https://youtu.be/PmW_TMQ3l0I?t=3819) (1:03:39) · [Challenges](https://youtu.be/PmW_TMQ3l0I?t=4580) (1:16:20) · [On-policy vs off-policy](https://youtu.be/PmW_TMQ3l0I?t=4798) (1:19:58) · [Best-of-N](https://youtu.be/PmW_TMQ3l0I?t=4963) (1:22:43) · [DPO](https://youtu.be/PmW_TMQ3l0I?t=5387) (1:29:47)

### [Лекция 6. Рассуждающие модели: RL для reasoning, GRPO, DeepSeek R1](lectures/06-llm-reasoning.md)

*LLM Reasoning* · 7 ноября 2025 · 107 мин · [видео](https://youtu.be/k5Fh-UgTuCo) · [транскрипт](transcripts/06-llm-reasoning.md)

Что такое reasoning-модели (LLM, которые перед ответом выводят цепочку рассуждений — chain-of-thought, доведённый до масштаба обучения), как их измеряют (бенчмарки по коду и математике с проверяемым ответом, метрика pass@k с выводом формулы, роль температуры) и как обучают: вместо SFT — RL на проверяемых наградах за формат и правильность, алгоритм GRPO с advantage относительно группы ответов и без value function, его сравнение с PPO. Разбирается length bias (нормировка на длину ответа поощряет длинные неверные ответы) и исправления DAPO и Dr. GRPO. В финале — рецепт DeepSeek R1-Zero и R1 (cold start → RL → SFT с rejection sampling → RL на helpfulness/harmlessness) и дистилляция reasoning в малые модели через SFT на выходах учителя.

**Главы:** [Introduction](https://youtu.be/k5Fh-UgTuCo?t=0) (00:00) · [Reasoning models](https://youtu.be/k5Fh-UgTuCo?t=763) (12:43) · [Benchmarks](https://youtu.be/k5Fh-UgTuCo?t=1669) (27:49) · [Pass@k metric](https://youtu.be/k5Fh-UgTuCo?t=1924) (32:04) · [Scaling with RL](https://youtu.be/k5Fh-UgTuCo?t=2887) (48:07) · [GRPO](https://youtu.be/k5Fh-UgTuCo?t=3464) (57:44) · [Comparison between GRPO and PPO](https://youtu.be/k5Fh-UgTuCo?t=3963) (1:06:03) · [Length bias](https://youtu.be/k5Fh-UgTuCo?t=4574) (1:16:14) · [DAPO, Dr. GRPO](https://youtu.be/k5Fh-UgTuCo?t=5100) (1:25:00) · [DeepSeek R1 recipe](https://youtu.be/k5Fh-UgTuCo?t=5378) (1:29:38)

### [Лекция 7. Агентные LLM: RAG, вызов инструментов, агенты](lectures/07-agentic-llms-rag-tools.md)

*Agentic LLMs* · 14 ноября 2025 · 109 мин · [видео](https://youtu.be/h-7S6HNq0Vg) · [транскрипт](transcripts/07-agentic-llms-rag-tools.md)

Как связать LLM с внешним миром. Afshine разбирает RAG: почему ни дообучение, ни «всё в контекст» не решают проблему knowledge cutoff, как строится knowledge base из chunks и embeddings, двухэтапный retrieval (bi-encoder и cosine similarity, затем re-ranking cross-encoder'ом), BM25 и гибридный поиск, HyDE, contextual retrieval, prompt caching и метрики NDCG, MRR, precision@k и recall@k с бенчмарком MTEB. Shervine переходит к действиям: tool calling (модель видит только описание функции и предсказывает аргументы; обучение через SFT-пары или через инструкцию, которую итеративно пишет reasoning-модель), tool selection, стандарт MCP, агенты как цикл observe → plan → act по ReAct, протокол Agent2Agent и безопасность агентных систем.

**Главы:** [Introduction](https://youtu.be/h-7S6HNq0Vg?t=0) (00:00) · [RAG overview](https://youtu.be/h-7S6HNq0Vg?t=398) (06:38) · [Similarity search with SBERT and bi-encoders](https://youtu.be/h-7S6HNq0Vg?t=1659) (27:39) · [Heuristic search with BM25](https://youtu.be/h-7S6HNq0Vg?t=2065) (34:25) · [HyDE and contextual retrieval](https://youtu.be/h-7S6HNq0Vg?t=2274) (37:54) · [Prompt caching](https://youtu.be/h-7S6HNq0Vg?t=2460) (41:00) · [Re-ranking with cross-encoders](https://youtu.be/h-7S6HNq0Vg?t=2724) (45:24) · [Retrieval evaluation with NDCG, MRR](https://youtu.be/h-7S6HNq0Vg?t=2869) (47:49) · [Tool calling](https://youtu.be/h-7S6HNq0Vg?t=3568) (59:28) · [Tool selection](https://youtu.be/h-7S6HNq0Vg?t=5182) (1:26:22) · [Model Context Protocol (MCP)](https://youtu.be/h-7S6HNq0Vg?t=5357) (1:29:17) · [Agents with ReAct](https://youtu.be/h-7S6HNq0Vg?t=5516) (1:31:56) · [Safety and closing thoughts](https://youtu.be/h-7S6HNq0Vg?t=6136) (1:42:16)

### [Лекция 8. Оценка LLM: метрики, LLM-as-a-judge, бенчмарки](lectures/08-llm-evaluation.md)

*LLM Evaluation* · 21 ноября 2025 · 109 мин · [видео](https://youtu.be/8fNP4N46RRo) · [транскрипт](transcripts/08-llm-evaluation.md)

Как измерять качество ответов LLM: от человеческой разметки и метрик согласия оценщиков (Cohen's kappa) через rule-based метрики (METEOR, BLEU, ROUGE) к главному методу — LLM-as-a-judge со structured output, его смещениям (position, verbosity, self-enhancement) и лучшим практикам, включая оценку factuality по атомарным фактам. Во второй половине Shervine разбирает семь типовых отказов агентного цикла (выбор инструмента, выполнение, синтез) и категории бенчмарков — MMLU, AIME, PIQA, SWE-bench, HarmBench, τ-bench — с предостережениями о data contamination и законе Гудхарта.

**Главы:** [Introduction](https://youtu.be/8fNP4N46RRo?t=0) (00:00) · [Inter-rater agreement metrics](https://youtu.be/8fNP4N46RRo?t=428) (07:08) · [Rule-based metrics](https://youtu.be/8fNP4N46RRo?t=1104) (18:24) · [METEOR, BLEU ROUGE](https://youtu.be/8fNP4N46RRo?t=1260) (21:00) · [LLM-as-a-judge](https://youtu.be/8fNP4N46RRo?t=1680) (28:00) · [Structured outputs](https://youtu.be/8fNP4N46RRo?t=2024) (33:44) · [Variants](https://youtu.be/8fNP4N46RRo?t=2208) (36:48) · [Position, verbosity, self-enhancement bias](https://youtu.be/8fNP4N46RRo?t=2327) (38:47) · [Best practices](https://youtu.be/8fNP4N46RRo?t=2842) (47:22) · [Factuality](https://youtu.be/8fNP4N46RRo?t=3246) (54:06) · [Agent evaluation](https://youtu.be/8fNP4N46RRo?t=3615) (1:00:15) · [Benchmarks](https://youtu.be/8fNP4N46RRo?t=5030) (1:23:50) · [Knowledge with MMLU](https://youtu.be/8fNP4N46RRo?t=5112) (1:25:12) · [Reasoning AIME, PIQA](https://youtu.be/8fNP4N46RRo?t=5374) (1:29:34) · [Coding with SWE-bench](https://youtu.be/8fNP4N46RRo?t=5637) (1:33:57) · [Safety with HarmBench](https://youtu.be/8fNP4N46RRo?t=5775) (1:36:15) · [Agents with Tau-Bench](https://youtu.be/8fNP4N46RRo?t=6051) (1:40:51)

### [Лекция 9. Итоги курса и текущие тренды: ViT, диффузионные LLM](lectures/09-recap-current-trends.md)

*Recap & Current Trends* · 5 декабря 2025 · 111 мин · [видео](https://youtu.be/Q86qzJ1K1Ss) · [транскрипт](transcripts/09-recap-current-trends.md)

Заключительная лекция: Afshine за 49 минут собирает восемь предыдущих лекций в одну цепочку (трансформер → decoder-only LLM и MoE → pre-training/SFT/preference tuning → RL-тюнинг и GRPO → RAG и tool calling → оценка) и уточняет объём финального экзамена. Затем два тренда 2025 года: Vision Transformer (картинка как последовательность patch-векторов, CLS-токен как в BERT, путь к VLM вроде LLaVA) и диффузионные LLM, где роль шума играет mask-токен, а весь ответ генерируется за фиксированное число шагов. Shervine закрывает курс 27-минутным взглядом на поле: взаимное влияние модальностей, незастывший дизайн трансформера, model collapse и mid-training, малые модели и аналоговое железо, безопасность AI-браузинга, «галлюцинации» как следствие next-token prediction и как следить за областью дальше.

**Главы:** [Introduction](https://youtu.be/Q86qzJ1K1Ss?t=0) (00:00) · [Transformer](https://youtu.be/Q86qzJ1K1Ss?t=72) (01:12) · [Transformer-based models & tricks](https://youtu.be/Q86qzJ1K1Ss?t=395) (06:35) · [Large Language Models](https://youtu.be/Q86qzJ1K1Ss?t=677) (11:17) · [LLM training](https://youtu.be/Q86qzJ1K1Ss?t=905) (15:05) · [LLM tuning](https://youtu.be/Q86qzJ1K1Ss?t=1449) (24:09) · [LLM reasoning](https://youtu.be/Q86qzJ1K1Ss?t=1781) (29:41) · [Agentic LLMs (RAG, tool calling)](https://youtu.be/Q86qzJ1K1Ss?t=2317) (38:37) · [LLM evaluation](https://youtu.be/Q86qzJ1K1Ss?t=2649) (44:09) · [Vision Transformer](https://youtu.be/Q86qzJ1K1Ss?t=2937) (48:57) · [Diffusion-based LLMs](https://youtu.be/Q86qzJ1K1Ss?t=3842) (1:04:02) · [Closing thoughts](https://youtu.be/Q86qzJ1K1Ss?t=5018) (1:23:38) · [Thank you!](https://youtu.be/Q86qzJ1K1Ss?t=6616) (1:50:16)

## Карта курса

| № | Лекция | О чём (по программе курса) |
|---|---|---|
| 1 | [Трансформер](lectures/01-transformer.md) | Background on NLP and tasks; Tokenization; Embeddings; Word2vec, RNN, LSTM; Attention mechanism; Transformer architecture |
| 2 | [Модели на базе трансформера и инженерные приёмы](lectures/02-transformer-models-tricks.md) | Attention approximation; MHA, MQA, GQA; Position embeddings (regular, learned); RoPE and applications; Transformer-based architectures; BERT and its derivatives |
| 3 | [Большие языковые модели: MoE, декодирование, промптинг](lectures/03-llms-moe-decoding-prompting.md) | Definition and architecture; Mixture of experts; Context length, temperature; Sampling strategies; Prompting, in-context learning; Chain of thought; Self-consistency |
| 4 | [Обучение LLM: предобучение, оптимизации, SFT и LoRA](lectures/04-llm-training.md) | Pretraining; Quantization; Hardware optimization; Supervised finetuning (SFT); Parameter-efficient finetuning (LoRA) |
| 5 | [Дообучение LLM на предпочтениях: RLHF, PPO, DPO](lectures/05-llm-tuning-rlhf-dpo.md) | Preference tuning; RLHF overview; Reward modeling; RL approaches (PPO and variants); DPO |
| 6 | [Рассуждающие модели: RL для reasoning, GRPO, DeepSeek R1](lectures/06-llm-reasoning.md) | Reasoning models; RL for reasoning; GRPO; Scaling |
| 7 | [Агентные LLM: RAG, вызов инструментов, агенты](lectures/07-agentic-llms-rag-tools.md) | Retrieval-augmented generation; Advanced RAG techniques; Function calling; Agents; ReAct framework |
| 8 | [Оценка LLM: метрики, LLM-as-a-judge, бенчмарки](lectures/08-llm-evaluation.md) | LLM-as-a-judge overview; Best practices and benefits; Biases and pitfalls |
| 9 | [Итоги курса и текущие тренды: ViT, диффузионные LLM](lectures/09-recap-current-trends.md) | Recap; Trending topics; Closing thoughts |

Итого 9 лекций, 966 минут видео (≈16.1 часа).

## Актуализация к ноябрю 2026

Лекции прочитаны осенью 2025 года. В папке [`updates/`](updates/index.md) по каждой лекции сверено с источниками, что с тех пор осталось верным, что устарело и что появилось нового; у каждого конспекта есть ссылка на свою актуализацию.

## Сайт

Те же материалы собраны в статический сайт с навигацией, поиском, тёмной темой и формулами (MkDocs + Material):

```bash
python3 -m venv .venv && .venv/bin/pip install mkdocs-material   # один раз
python3 -I tools/build_docs.py                                    # md -> docs/ + mkdocs.yml
.venv/bin/mkdocs serve                                            # http://127.0.0.1:8000
```

`.venv/bin/mkdocs build` кладёт готовый сайт в `site/`; его можно открыть и без сервера (`site/index.html`), не будет работать только поиск. Стили, скрипты и локальная копия KaTeX лежат в `site_src/`.

Публикация: `.venv/bin/mkdocs gh-deploy` собирает сайт и отправляет его в ветку `gh-pages`, откуда его раздаёт GitHub Pages.

## Как это собрано

1. Метаданные и ручные английские субтитры (en-US) каждого видео выгружены через `yt-dlp`.
2. VTT-субтитры склеены в абзацы (~1 минута речи) и разбиты по главам видео, таймкоды превращены в ссылки `youtu.be/<id>?t=<сек>` — это папка `transcripts/`.
3. По каждому транскрипту написан конспект на русском по единому шаблону: краткое содержание, оглавление, раздел на каждую главу видео, ключевые термины, главные выводы, вопросы из зала — это папка `lectures/`.
4. Вторым проходом в конспекты добавлены пометки `> 💡 Дополнение` (примеры, интуиция, связи, практика) и раздел «Чем можно дополнить»; они явно отделены от пересказа лекции.

Дата сборки: 7 ноября 2026.
