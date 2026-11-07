# Лекция 1. Трансформер — что изменилось к ноябрю 2026

*Лекция прочитана 26 сентября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/01-transformer.md) · [Все актуализации](index.md)

## Коротко

- **Рекуррентность вернулась в production — в виде гибридов.** Qwen3.5-397B-A17B (17.02.2026) чередует слои Gated DeltaNet и обычного attention 3:1 и декодирует в 8,6×/19× быстрее Qwen3-Max на 32k/256k [1][2]; Nemotron 3 (с 15.12.2025) построен на Mamba-2 [3]; Kimi Linear (30.10.2025) — на KDA [4]. Контрпример: MiniMax M2 (29.10.2025) остался на full attention [5].
- **Sparse attention дошло до фронтира.** DeepSeek V3.2 с DSA (01.12.2025) и DeepSeek V4 (превью 24.04.2026): контекст 1M токенов по умолчанию; на 1M V4-Pro тратит около 27 % FLOPs и 10 % KV cache от V3.2 [6][7].
- **Токенизация: словари растут, byte-level пока в лаборатории.** Qwen3.5 расширил словарь со 150k до 250k токенов [1]; Cartesia (28.10.2026) показала, что byte-level H-Net с dynamic chunking обгоняет BPE по compute-efficiency, но веса не выпущены [8].
- **Decoder-only по-прежнему главный, но не единственный.** T5Gemma 2 (18.12.2025) — encoder-decoder, собранный из Gemma 3 [9]; Ettin (ICLR 2026): encoder-only всё ещё лучше для классификации и retrieval [10]; diffusion LLM Mercury 2 (24.02.2026) продаётся как API [11].
- **Embedding-модели стали мультимодальными и MoE:** Gemini Embedding 2 (10.03.2026), Voyage 4 (15.01.2026), Cohere Embed 5 (30.09.2026) [13][14][15].
- **Сама лекция 1 в редакции 2026 года** (25.09.2026) добавила слайды про residual connections, layer normalization, dropout и «agentic era» [20].

## Что осталось верным

Ядро лекции не устарело. Production-модели по-прежнему работают с subword-токенами, токен остаётся единицей тарификации и лимита контекста [1][8]. Формула $\mathrm{softmax}(QK^\top/\sqrt{d_k})V$, обучаемые проекции Q/K/V, multi-head, masked self-attention и positional encoding реализованы и в гибридных, и в sparse-моделях 2026 года: в Qwen3.5 и Nemotron 3 каждый четвёртый–шестой слой — обычный attention [2], а DSA лишь выбирает, на какие ключи смотреть [7]. Объяснение, почему RNN/LSTM проигрывают (vanishing gradient, последовательные вычисления), верно исторически; новое — линейные рекуррентные слои обучают параллельно по чанкам [18]. Decoder-only остаётся архитектурой почти всех chat-моделей [2][5]. Precision/recall/F1 и perplexity никуда не делись.

## Что устарело или сдвинулось

- **Лекция говорит:** символьная токенизация — «вычисления намного медленнее», представление буквы неинтерпретируемо (раздел 4, 23:52) → **Сейчас:** byte-level модели с выучиваемым разбиением (H-Net) при равном compute обгоняют BPE: 1,28× по validation loss и 2,06× по OLMES, а byte-level Transformer без чанкинга — в 9,2× [8, 28.10.2026]; Fast BLT (08.05.2026) ускоряет побайтовую генерацию диффузионным декодированием [21]. Production-модели всё ещё subword: сдвиг в аргументации, не в практике.
- **Лекция говорит:** словарь мультиязычных моделей — «сотни тысяч» (раздел 5, 34:53) → **Сейчас:** Qwen3.5 — 250k вместо 150k, по заявлению Alibaba это +10–60 % эффективности кодирования для большинства языков [1]; low-resource языкам по-прежнему нужно в несколько раз больше токенов, чем английскому [22, 19.01.2026].
- **Лекция говорит:** RNN медленные из-за последовательных вычислений; «про RNN сейчас не слышно» (раздел 6, 1:02:54) → **Сейчас:** линейные рекуррентные слои (Gated DeltaNet, KDA, Mamba-2) вернулись в production-гибриды с фиксированным состоянием вместо растущего KV cache; Kimi Linear сокращает KV cache до 75 % и ускоряет декодирование до 6× на 1M [4]; Mamba-3 (16.03.2026) и Gated DeltaNet-2 (21.05.2026) продолжают линию [17][18].
- **Лекция говорит:** каждый токен смотрит на все остальные; матрица $QK^\top$ — $n\times n$ (раздел 7, 1:10:41) → **Сейчас:** у DeepSeek V4 — Compressed Sparse Attention и Heavily Compressed Attention, индексатор выбирает top-k ключей [7]; точный full attention тоже ускорился — FlashAttention-4 даёт до 1613 TFLOPs/s на B200 [16]. Но MiniMax M2 отказался от гибридов: проигрыш на multi-hop reasoning и агентных задачах, чувствительность linear attention к точности [5].
- **Лекция говорит:** трансформер — encoder + decoder для перевода (раздел 8, 1:13:57) → **Сейчас:** encoder-decoder возвращается как производная от decoder-only: T5Gemma 2 строится из Gemma 3, делит embeddings между encoder и decoder и сливает self- и cross-attention в один слой; контекст 128k; по Google, после post-training она «в целом лучше» decoder-only аналогов [9]. Ettin: encoder 400M обходит decoder 1B на MNLI [10].
- **Лекция говорит:** позиция кодируется синусами и косинусами (раздел 9, 1:29:57) → **Сейчас:** стандарт — RoPE, спор идёт о его пределах: обзор (09.08.2026) — вычислимость позиций за пределами обучающей длины не гарантирует качества [23]; DaRoPE (28.09.2026) заменяет абсолютную позицию в медленных частотах на выученные из контекста координаты [24]. В курсе 2026 года тема лекции 2 — «RoPE and variants» [12].
- **Лекция говорит:** генерация идёт токен за токеном до EOS (раздел 9, 1:40:12) → **Сейчас:** Qwen3.5 обучен с multi-token prediction [1]; diffusion LLM Mercury 2 генерирует параллельно — по данным вендора около 1000 токенов/с [11]; в CME 295 осени 2026 — лекция 8 «Diffusion LLMs» (20.11.2026) [12].
- **Лекция говорит:** про residual connections и layer norm ничего (раздел 9; см. «Чем можно дополнить») → **Сейчас:** редакция 2026 добавила слайды «Computational trick: residual connections / layer normalization / masking» и dropout [20]; residual уже пересматривают — Attention Residuals (Kimi, 03.2026) заменяют сложение выходов слоёв на softmax-взвешивание [19], DeepSeek V4 — на Manifold-Constrained Hyper-Connections [7].
- **Лекция говорит:** оценка генерации — BLEU/ROUGE с эталоном (раздел 3, 17:44) → **Сейчас:** в «карте аббревиатур» курса 2026 метрики — «PPL, LaaJ, KL, Pass@k, Elo, TTFT, TPOT», бенчмарки — «AIME, HLE, MMLU, SWE-bench, GPQA» [20].

## Новое, о чём лекция не знала

- **Qwen3.5 (17.02.2026)** — 397B параметров, 17B активных, гибрид Gated DeltaNet + Gated Attention поверх sparse MoE, multi-token prediction, 201 язык; наследник Qwen3-Next (сентябрь 2025). Первый флагман крупного открытого семейства не на чистом softmax-attention [1][2].
- **DeepSeek V4 (превью 24.04.2026)** — V4-Pro 1.6T/49B и V4-Flash 284B/13B, контекст 1M, гибрид CSA + HCA, mHC вместо обычных residual [6][7]. GA-дата не подтверждена первичным источником.
- **Nemotron 3 (Nano 15.12.2025, Super апрель 2026)** — открытые MoE-гибриды NVIDIA: в Super 40 слоёв Mamba-2 на 8 слоёв attention; опубликованы веса, рецепт и данные [3][2][28].
- **Kimi Linear, Mamba-3, Gated DeltaNet-2** — три шага линейного внимания: KDA с канальным гейтом (30.10.2025) [4]; Mamba-3 с комплексным состоянием и MIMO, +1,8 пункта к Gated DeltaNet на 1.5B [17]; GDN-2 разделяет «стирание» и «запись» в delta rule [18].
- **FlashAttention-4 (05.03.2026)** — ядро под Blackwell: 1,3× против cuDNN, 2,7× против Triton, 71 % утилизации [16].
- **Byte-level без токенизатора** — Cartesia (28.10.2026): H-Net с dynamic chunking как замена BPE [8]; Fast BLT (08.05.2026) — параллельная генерация байтов [21]. Production-использование не удалось подтвердить источником.
- **Mercury 2 (24.02.2026)** — первый коммерческий reasoning diffusion LLM с OpenAI-совместимым API; цифры скорости — от вендора [11].
- **Embedding-модели:** Gemini Embedding 2 — текст, изображения, видео, аудио и PDF в одном пространстве, 3072 измерения с Matryoshka, public preview [13]; Voyage 4 — embedding-модель на MoE с общим пространством для large/lite [14]; Cohere Embed 5 — Pro и Fast в одном пространстве [15].

## Что это меняет для читателя

- Квадратичная цена attention больше не абсолют: через API доступны контексты 1M [6], но счёт идёт по токенам — пользуйтесь prompt caching: Anthropic — чтение из кэша 0,1× базовой цены, минимум 512–4096 токенов [25]; OpenAI — включено по умолчанию, чтение 0,1× на GPT-5.6+ [26]; Gemini — implicit caching с порога 2048–4096 токенов [27].
- Проверяйте токенизатор под свой язык: премия для не-английских текстов остаётся кратной [22], новые словари (250k у Qwen3.5) её снижают [1].
- При fine-tuning открытых моделей учитывайте архитектуру: гибриды (Qwen3.5, Nemotron 3) требуют специальных ядер и чувствительнее к точности [5].
- Для классификации и retrieval encoder-only модели по-прежнему выгоднее decoder-only того же размера [10]; для embedding выбирайте семейства с общим пространством: индексировать большой моделью, запросы считать маленькой [14][15].
- Оценку генерации стройте на LLM-as-a-judge и pass@k, а не на BLEU — так теперь делает и курс [20]; размеченный набор и precision/recall по классам остаются обязательными.

## Проверка пометок в конспекте

- **«Все современные LLM используют subword-токенизаторы…»** (раздел 4) — верно на ноябрь 2026: tokenizer-free модели остаются исследовательскими [8][21]; словари при этом выросли до 250k [1].
- **«Рекуррентная идея не умерла… встречаются гибриды, где часть attention-слоёв заменена такими state-space-слоями»** (раздел 6) — неточно. Основной механизм гибридов 2026 года — linear attention семейства Gated DeltaNet/KDA (Qwen3.5, Kimi Linear), Mamba-2 — у Nemotron 3; типичная пропорция 3:1 [2]. И «встречаются» занижает: это флагманы открытых весов. Второй путь — sparse attention (DeepSeek) [7]. Про закрытые фронтир-модели — не удалось подтвердить источником.
- **«…время и память self-attention растут квадратично… ограничение на размер контекста»** (раздел 7) — верно для full attention; стоит оговорить, что sparse attention делает стоимость шага фиксированной (top-k), и 1M контекст у DeepSeek V4 — норма [6][7].
- **«decoder-only (GPT и почти все современные chat-модели)»** (раздел 8) — верно; исключения — T5Gemma 2 и diffusion LLM [9][11].
- **«по состоянию на 2026 год такое prompt caching предлагают основные провайдеры»** (раздел 9) — подтверждено официальной документацией Anthropic, OpenAI и Google [25][26][27].
- **«многие embedding-модели… возвращают векторы, уже нормированные»** (раздел 5) — в этой актуализации не проверялось.

## Источники

1. Qwen3.5: Towards Native Multimodal Agents — Alibaba Cloud Community — 17.02.2026 — https://www.alibabacloud.com/blog/qwen3-5-towards-native-multimodal-agents_602894
2. Hybrid Attention (LLM Architecture Gallery) — Sebastian Raschka — 2026, дата обновления не указана — https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/
3. NVIDIA Debuts Nemotron 3 Family of Open Models — NVIDIA Newsroom — 15.12.2025 — https://nvidianews.nvidia.com/news/nvidia-debuts-nemotron-3-family-of-open-models
4. Kimi Linear: An Expressive, Efficient Attention Architecture — arXiv 2510.26692, Kimi Team — 30.10.2025 — https://arxiv.org/abs/2510.26692
5. Why Did M2 End Up as a Full Attention Model? — MiniMax — 29.10.2025 — https://www.minimax.io/news/why-did-m2-end-up-as-a-full-attention-model
6. DeepSeek-V4 Preview — DeepSeek — 24.04.2026 — https://www.deepseek.com/en/news/v4-preview/
7. DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence — arXiv 2606.19348, DeepSeek-AI — 26.04.2026 — https://arxiv.org/abs/2606.19348
8. From Tokens to Bytes II — Cartesia Research — 28.10.2026 — https://cartesia.ai/blog/from-tokens-to-bytes-part-2
9. T5Gemma 2: The next generation of encoder-decoder models — Google Blog — 18.12.2025 — https://blog.google/innovation-and-ai/technology/developers-tools/t5gemma-2/
10. Seq vs Seq: An Open Suite of Paired Encoders and Decoders (Ettin) — arXiv 2507.11412, Weller et al., ICLR 2026 — 15.07.2025, v2 12.03.2026 — https://arxiv.org/abs/2507.11412
11. Inception Launches Mercury 2, the First Diffusion-Based Language Reasoning Model — Business Wire — 24.02.2026 — https://www.businesswire.com/news/home/20260224034496/en
12. CME 295 Syllabus, Fall 2026 — Stanford, Afshine и Shervine Amidi — просмотрено 07.11.2026 — https://cme295.stanford.edu/syllabus/
13. Gemini Embedding 2: Our first natively multimodal embedding model — Google Blog — 10.03.2026 — https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/
14. The Voyage 4 model family: shared embedding space with MoE architecture — Voyage AI blog — 15.01.2026 — https://blog.voyageai.com/2026/01/15/voyage-4/
15. Embed 5: Frontier Embedding Models for Enterprise — Cohere — 30.09.2026 — https://cohere.com/blog/embed-5
16. FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling — arXiv 2603.05451, Zadouri, Hoehnerbach, Shah, Liu, Thakkar, Dao — 05.03.2026 — https://arxiv.org/abs/2603.05451
17. Mamba-3: Improved Sequence Modeling using State Space Principles — arXiv 2603.15569, Lahoti et al., ICLR 2026 — 16.03.2026 — https://arxiv.org/abs/2603.15569
18. Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention — arXiv 2605.22791, Hatamizadeh, Choi, Kautz (NVIDIA) — 21.05.2026 — https://arxiv.org/abs/2605.22791
19. Attention Residuals — arXiv 2603.15031, Kimi Team — март 2026 — https://arxiv.org/abs/2603.15031
20. CME 295 Lecture 1 slides, Fall 2026 (сравнены с Fall 2025) — Stanford — 25.09.2026 — https://cme295.stanford.edu/slides/fall26-cme295-lecture1.pdf и https://cme295.stanford.edu/slides/fall25-cme295-lecture1.pdf
21. Fast Byte Latent Transformer — arXiv 2605.08044, Kallini et al. — 08.05.2026 — https://arxiv.org/abs/2605.08044
22. Reducing Tokenization Premiums for Low-Resource Languages — arXiv 2601.13328, Churchill, Skiena — 19.01.2026 — https://arxiv.org/abs/2601.13328
23. Position Encoding in Transformers: From Absolute and Relative Methods to Rotary Position Embeddings and Long-Context Scaling — arXiv 2608.10021, Jiguo Li — 09.08.2026 — https://arxiv.org/abs/2608.10021
24. RoPE is Dead, Long Live RoPE: Towards Scalable Data-aware Positional Encodings — arXiv 2609.34556, Lévy et al. — 28.09.2026 — https://arxiv.org/abs/2609.34556
25. Prompt caching — Claude Developer Platform docs, Anthropic — просмотрено 07.11.2026 — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
26. Prompt caching — OpenAI API docs — просмотрено 07.11.2026 — https://developers.openai.com/api/docs/guides/prompt-caching
27. Context caching — Gemini API docs, Google — просмотрено 07.11.2026 — https://aistudio.google.com/docs/caching
28. LLM Research Papers: The 2026 List (January to May) — Sebastian Raschka — 06.06.2026 — https://magazine.sebastianraschka.com/p/llm-research-papers-2026-part1
29. DeepSeek-V3.2 model card — Hugging Face, DeepSeek-AI — коллекция обновлена 01.12.2025 — https://huggingface.co/deepseek-ai/DeepSeek-V3.2
30. Cartesia's new H-Nets learn from raw bytes without a tokenizer — AICoder (вторичный источник: статус выпуска весов) — 28.10.2026 — https://aicoder.com/news/news-20261028-cartesia-h-net-byte-level-tokenizer-free-10x-less-data-smollm3
