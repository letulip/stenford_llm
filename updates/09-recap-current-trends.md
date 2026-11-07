# Лекция 9. Итоги курса и текущие тренды — что изменилось к ноябрю 2026

*Лекция прочитана 5 декабря 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/09-recap-current-trends.md) · [Все актуализации](index.md)

## Коротко

- Диффузионные LLM стали коммерческим продуктом, но не фронтиром: Inception выпустила Mercury 2 (24.02.2026, первая диффузионная reasoning-модель, ~1 000 ток/с), Mercury 2.5 (08.09.2026) и Mercury 3 (19.10.2026, контекст 1M); Gemini Diffusion у Google остаётся «experimental demo» [1–4].
- Открытые диффузионные модели доросли до 100B и стали блочными гибридами: LLaDA2.0 (Ant Group, 10.12.2025) конвертирует autoregressive-модели в блочную диффузию; вышли open-weight DiffusionGemma (31.07.2026) и TwoTower от NVIDIA (25.06.2026) [5–7].
- Muon перестал быть «статьёй Kimi K2»: им обучены DeepSeek-V4 (1,6T, апрель 2026), GLM-5 (744B), Kimi K2-Thinking; поддержка есть в DeepSpeed (июнь 2026) [9–11].
- VLM уходят от схемы «CLIP-энкодер + projector»: Qwen3.5 (февраль 2026) обучена с early fusion, Gemma 4 (апрель 2026) — «natively multimodal», её 12B-вариант принимает сырые патчи без энкодера [13–15]. У DeepSeek-OCR появились продолжение (OCR 2, январь 2026) и критика [16–17].
- AI-браузеры: OpenAI в декабре 2025 укрепила Atlas против prompt injection, а 9 июля 2026 объявила о его закрытии как отдельного браузера — агент переехал в приложение ChatGPT и расширение Chrome [18–19]. OWASP выпустил Top 10 for Agentic Applications (09.12.2025) [21].
- Доля AI-текста среди новых англоязычных статей — около половины (50,9% в Q4 2025, 49,9% в Q1 2026 по Graphite), а не «80%» [22–23].

## Что осталось верным

- **«Диффузия выигрывает скорость, но догоняет по качеству»** (раздел 11, 1:19:36). Mercury 2 на запуске уступал Gemini 3 Flash почти везде (GPQA Diamond 74 против 90, LiveCodeBench 67 против 91), выигрывая по AIME и latency [1]; LLaDA2.0-flash (100B) в среднем 73,18 против 73,60 у Qwen3-30B-A3B [5].
- **«Шум для картинок = mask-токен для текста»** — все модели 2026 года этого класса остаются masked diffusion [5–7].
- **Трансформер «не застыл»**: DeepSeek-V4 разом сменил оптимизатор (Muon), residual-связи (mHC) и attention (сжатые CSA/HCA под контекст 1M) [9]; Qwen3.5 чередует RNN-слои Gated DeltaNet с attention [13].
- **Mid-training** закрепился как отдельная стадия — вышел обзор с формальным определением (27.10.2025) [26]. **Галлюцинации как следствие постановки задачи**: Kalai et al. (OpenAI, 04.09.2025) выводят их из статистики pre-training и из бенчмарков, поощряющих угадывание вместо «не знаю» [27].
- **Малые модели как «второй фронт Парето»**: Gemma 4 E2B/E4B работают на телефонах и Raspberry Pi [14]; Apple рядом с 3B dense добавила on-device 20B-sparse с 1–4B активных параметров (08.06.2026) [28].
- **Непрерывное обучение** открыто: обзор августа 2026 фиксирует сдвиг от обновления весов к «системной адаптации» (память, библиотеки навыков, test-time training), но не решение [29].

## Что устарело или сдвинулось

- **Лекция говорит:** диффузионные модели — экспериментальный анонс Google и стартап «в заголовках» (раздел 11, ~1:06) → **Сейчас:** Inception продаёт третье поколение: Mercury 3 — $0,20/$0,70 за 1M входных/выходных токенов через OpenRouter, Baseten, Vercel и Azure AI Foundry; Mercury 2 вошёл в TIME Best Inventions 2026 [2–3]. Gemini Diffusion из демо не вышла [4].
- **Лекция говорит:** число forward passes = число шагов, ответ генерируется целиком (раздел 11, 1:16:07) → **Сейчас:** модели 2026 года *блочные*: LLaDA2.0 декодирует блоками по 32 токена, DiffusionGemma — по 256, TwoTower держит замороженную AR-«башню» для контекста и диффузионный denoiser для блока. Это возвращает KV-cache и переменную длину ответа; ускорение меряют в «токенах за forward pass»: ~2,5 у LLaDA2.0-mini, ~20 у DiffusionGemma [5–7].
- **Лекция говорит:** «до ~10x быстрее» (раздел 11, 1:19:36) → **Сейчас:** 10x — цифра Inception для Mercury 1 [3]; LLaDA2.0 даёт до 2,1x над AR-базой [5], TwoTower — 2,42x при 98,7% качества [7]. Контраргумент — Uno (03.09.2026): диффузионные веса поверх обычной AR-модели, до 3x без потери качества и быстрее speculative decoding; авторы утверждают, что 8B Uno обходит DiffusionGemma 26B и Mercury 2 [8].
- **Лекция говорит:** «статья Kimi K2 вводит оптимизатор Muon» (раздел 12, 1:28:17) → **Сейчас:** неточно уже тогда: Muon предложил Keller Jordan в октябре 2024 [30], масштабировала Moonshot в феврале 2025 (~2x эффективность по compute против AdamW) [31]; Kimi K2 добавил QK-Clip [12]. Прогноз «кандидат на стандарт» сбывается: DeepSeek-V4 применяет Muon к большинству модулей (AdamW — embeddings, голова, нормы; QK-Clip не нужен благодаря RMSNorm на Q/K) [9], GLM-4.5/5 — Muon с «Muon Split» для MLA [10]. Теория отстаёт: «Spectral Scaling Laws of Muon» (июнь 2026) предупреждает, что поздние слои на frontier-масштабе могут выйти из режима сходимости Newton–Schulz при стандартных 5 итерациях [32].
- **Лекция говорит:** «первые результаты поиска на 80% сгенерированы LLM» (раздел 12, 1:31:52) → **Сейчас:** по Graphite (55 тыс. статей из Common Crawl, три детектора) доля *преимущественно* AI-написанных новых статей ~50% и на плато с конца 2024; такие статьи почти не попадают в выдачу Google и ответы ChatGPT [22–23]. Цифру 80% подтвердить источником не удалось.
- **Лекция говорит:** model collapse — угроза, ответ — курирование (раздел 12, 1:31:52) → **Сейчас:** исследование Meta на >1000 моделей (EMNLP 2025): перефразированная синтетика в доле ~30% ускоряет достижение той же loss в 5–10 раз, признаки collapse дают лишь чисто сгенерированные «учебники» [24]; теоретическая работа сентября 2026 пересматривает требуемую долю человеческих данных, числа не даёт [25].
- **Лекция говорит:** статья про аналоговое железо «вышла в сентябре», выигрыш в симуляции (раздел 12, 1:36:26) → **Сейчас:** это Leroux et al., Nature Computational Science, 08.09.2025 (Jülich/RWTH Aachen): attention на gain-cell массивах, SPICE-симуляция 28 нм, ~100x по latency и ~70 000x по энергии против H100 — только для attention и GPT-2-масштаба; чипа нет [33]. Изготовленного прототипа в 2026 году не нашёл («не удалось подтвердить источником»).
- **Лекция говорит:** AI-браузинг (Atlas) будет демократизироваться, нужен аналог HTTPS-сертификата (раздел 12, 1:42:55) → **Сейчас:** OpenAI в декабре 2025 выпустила для Atlas adversarially обученную модель и RL-«атакующего» для red-teaming; британский NCSC заявил, что prompt injection, возможно, никогда не будет устранён полностью [18]. 9 июля 2026 OpenAI закрыла Atlas («браузер лучше работает как функция, чем как отдельный продукт»); агент переехал в приложение ChatGPT, расширение Chrome и облачный браузер [19]. Comet (Perplexity) получил zero-click уязвимости «PleaseFix» от Zenity Labs (март 2026) с путём к хранилищу 1Password [20]. «Сертификата безопасного сайта» нет; вместо него — таксономии и стандарты контроля агентов OWASP [21, 34, 39].
- **Лекция говорит:** LLaVA-схема (энкодер + конкатенация) — самый частый способ VLM (раздел 10, 58:56) → **Сейчас:** для открытых моделей верно, но крупные релизы обучаются natively: Qwen3.5 заявляет early fusion и превосходство над Qwen3-VL [13]; Gemma 4 — «natively multimodal» с encoder-free 12B-вариантом [15].

## Новое, о чём лекция не знала

- **LLaDA2.0 (Ant Group / inclusionAI, 10.12.2025).** 16B и 100B MoE получены конвертацией AR-моделей Ling-2.0 трёхфазной схемой Warmup–Stable–Decay с ростом и сжатием блока, затем SFT + DPO. «Вырастить» диффузионную модель из готовой AR за долю бюджета — главный рецепт 2026 года [5].
- **DiffusionGemma (31.07.2026).** Экспериментальная open-weight MoE 25,2B/3,8B active, дообученная из Gemma 4 менее чем на 10% исходного бюджета токенов; ~1 500 ток/с на одном H100, блоки по 256 токенов, AR-режим сохранён [6]. Первый открытый диффузионный LLM большой лаборатории.
- **Гибриды «AR + диффузия»**: TwoTower (NVIDIA) [7], dQwen3.5 (17.09.2026) — конвертация гибридных attention/RNN моделей Qwen3.5 0,8–9B [35], Uno [8]. Каталог года (LLaDA2.1, LLaDA MoE v2, Nemotron-Labs-Diffusion) — в Awesome-Diffusion-LLM [36]. **LLaDA2.0-Uni (22.04.2026)** объединяет понимание и генерацию картинок: визуальный вход дискретизируется SigLIP-VQ и идёт через тот же masked-diffusion механизм, что и текст [37].
- **DeepSeek-OCR 2 (28.01.2026)** — DeepEncoder V2 переупорядочивает vision-токены по содержанию, а не в raster-порядке [16]. Критика «Visual Merit or Linguistic Crutch?» (07.01.2026): при семантической порче текста точность падает с ~90% до ~20%, около 10 тыс. текстовых токенов — почти полный обвал; optical compression держится на языковых priors [17].
- **Muon в DeepSpeed (июнь 2026)** — гибридный режим (Muon для 2D-весов, AdamW для остального), экономия ~45% памяти состояния оптимизатора; на fine-tuning Moonlight-16B разница с AdamW в пределах ±2 п.п. [10].
- **Nested Learning / Hope (Google Research, 07.11.2025, NeurIPS 2025)** — ответ на «непрерывное обучение»: модель как вложенные оптимизационные задачи с памятью разных частот обновления; заявлены выигрыши по perplexity и long-context, бенчмарков continual learning в анонсе нет [38].
- **OWASP Top 10 for Agentic Applications (09.12.2025)**: от ASI01 Agent Goal Hijack до ASI10 Rogue Agents [21]; квартальный обзор эксплойтов (08.10.2026) раскладывает по нему реальные инциденты — например, CoSnitch в Microsoft Copilot (CVE-2026-24301, инъекция через ссылку с записью в постоянную память) — и формулирует: инструкции в промпте границей безопасности не являются [34].

## Что это меняет для читателя

- Диффузионная модель — рабочий вариант для latency-критичных задач (голос, автодополнение, subagents, поиск): Mercury 2/3 доступны по OpenAI-совместимому API и в Azure [2–3]; но сравнивайте с AR-моделью со speculative decoding на своём батче — типичен выигрыш 2–3x, а не 10x [5, 7, 8].
- Блочная диффузия вернула KV-cache и обычные примитивы API (tool use, JSON) — гибрид подключается как обычная модель [2, 5].
- Выбор оптимизатора стал практическим: для pre-training и крупного fine-tuning Muon есть в DeepSpeed и экономит память; для LoRA и мелкого fine-tuning выигрыша почти нет [10].
- В VLM-пайплайнах ориентируйтесь на natively-мультимодальные открытые модели (Qwen3.5, Gemma 4), включая on-device [13–15]; обещания «в 10 раз меньше vision-токенов» проверяйте на длинных документах [17].
- Синтетика в данных не табу: перефразированный корпус в доле ~30% помогает, чисто сгенерированные «учебники» вредят [24].
- Агенты в браузере: считайте prompt injection постоянным свойством среды — минимальные права, подтверждение необратимых действий, контроль исходящих адресов и памяти агента; для threat-моделирования берите таксономию OWASP ASI [21, 34].

## Проверка пометок в конспекте

- «**Дополнение — уточнение: В LLaVA в LLM уходит не CLS-токен…**» — фраза «по состоянию на 2026 год для VLM обычно берут contrastive-энкодеры (CLIP, SigLIP)» неточна: верно для открытых LLaVA-подобных моделей, но ведущие релизы 2026 года обучаются natively (early fusion у Qwen3.5 [13], Gemma 4 с encoder-free 12B [15]). CLIP/SigLIP — стартовая точка, а не правило.
- «**Дополнение — уточнение: Названия, которых нет в субтитрах…**» — названия верны, но «обычный KV-cache напрямую не работает» устарело: блочная диффузия его восстанавливает [5–7]. Вывод «ниша быстрых моделей, а не фронтир» держится, однако ниша расширилась на reasoning, голос и контекст 1M [1–3].
- «**Дополнение — уточнение: Ориентиры для поиска…**» — «Muon и MuonClip описаны в отчёте Kimi K2» формально верно, но создаёт впечатление, что Muon оттуда родом; добавить: Keller Jordan, октябрь 2024 [30], масштабирование — Moonshot, февраль 2025 [31]. Остальное (DiT, DeepSeek-OCR, Shumailov et al.) верно.
- «**Дополнение — на практике: Угроза, о которой говорит Shervine…**» — верно; дополнить OWASP Top 10 for Agentic Applications (декабрь 2025) [21] и редакцией LLM Top 10 2026 со стандартом Agent Control (сентябрь 2026) [39].
- Остальные 💡-блоки разделов 10–12 (размеры ViT-B/16, пример denoising) претензий не вызывают.

## Источники

1. Inception launches Mercury 2, the first diffusion-based language reasoning model — The Decoder — 24.02.2026 — https://the-decoder.com/inception-launches-mercury-2-the-first-diffusion-based-language-reasoning-model/
2. Inception Releases Mercury 3, Its Flagship Diffusion LLM — Unite.AI — 19.10.2026 — https://www.unite.ai/inception-releases-mercury-3-its-flagship-diffusion-llm/
3. Inception blog (даты постов Mercury 2 / Edit 2 / 2.5 / Voice / 3; Mercury on Azure AI Foundry, 29.10.2026) — Inception Labs — 2026 — https://www.inceptionlabs.ai/blog и https://www.inceptionlabs.ai/blog/mercury-azure-foundry
4. Gemini Diffusion (страница модели, статус «experimental demo», 1479 ток/с) — Google DeepMind — просмотрено 07.11.2026 — https://deepmind.google/models/gemini-diffusion/
5. LLaDA2.0: Scaling Up Diffusion Language Models to 100B — Ant Group / inclusionAI, arXiv 2512.15745 — 10.12.2025 — https://arxiv.org/abs/2512.15745
6. DiffusionGemma Technical Report — DiffusionGemma Team (организация на arXiv не указана; Google — по линейке Gemma 4), arXiv 2608.00146 — 31.07.2026 — https://arxiv.org/abs/2608.00146
7. Nemotron-Labs-TwoTower: Diffusion Language Modeling with Pretrained Autoregressive Context — NVIDIA, arXiv 2606.26493 — 25.06.2026 — https://arxiv.org/abs/2606.26493
8. Unlocking Lossless Speedups in LLMs via Discrete Diffusion (Uno, Ψ-Spec) — Sahoo et al., arXiv 2609.04010 — 03.09.2026 — https://arxiv.org/abs/2609.04010
9. DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence — DeepSeek-AI, arXiv 2606.19348 — 26.04.2026 — https://arxiv.org/abs/2606.19348
10. Using Muon Optimizer with DeepSpeed — PyTorch Blog — обновлено 03.06.2026 — https://pytorch.org/blog/using-muon-optimizer-with-deepspeed/
11. GLM-5: from Vibe Coding to Agentic Engineering — GLM-5 Team, arXiv 2602.15763 — 17.02.2026 (использование Muon / Muon Split — по [10]) — https://arxiv.org/abs/2602.15763
12. Kimi K2: Open Agentic Intelligence (MuonClip) — Moonshot AI, arXiv 2507.20534 — июль 2025 — https://arxiv.org/abs/2507.20534
13. Qwen3.5-397B-A17B model card — Qwen, Hugging Face — февраль 2026 — https://huggingface.co/Qwen/Qwen3.5-397B-A17B
14. Gemma 4: Byte for byte, the most capable open models — Google Blog — 02.04.2026 — https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
15. Gemma 4 Technical Report — Google, arXiv 2607.02770 — 02.07.2026 — https://arxiv.org/abs/2607.02770
16. DeepSeek-OCR 2: Visual Causal Flow — Wei, Sun, Li, arXiv 2601.20552 — 28.01.2026 — https://arxiv.org/abs/2601.20552
17. Visual Merit or Linguistic Crutch? A Close Look at DeepSeek-OCR — Liang et al., arXiv 2601.03714 — 07.01.2026 — https://arxiv.org/abs/2601.03714
18. OpenAI says prompt injection may never be 'solved' for browser agents like Atlas — CyberScoop — 30.12.2025 — https://cyberscoop.com/openai-chatgpt-atlas-prompt-injection-browser-agent-security-update-head-of-preparedness/
19. OpenAI is shutting down Atlas, but its AI browser ambitions are still growing — TechCrunch — 09.07.2026 — https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/
20. AI Browser Comparison 2026: Atlas vs. Comet vs. Dia — TechTimes — 16.06.2026 — https://www.techtimes.com/articles/318528/20260616/ai-browser-comparison-2026-atlas-vs-comet-vs-dia-ranked-security-use-case.htm
21. OWASP Top 10 for Agentic Applications — OWASP GenAI Security Project — 09.12.2025 — https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
22. A Study Finds Roughly Half of New Web Articles Are AI-Written (пересказ исследования Graphite с данными Q4 2025 / Q1 2026) — Kompozy — 21.08.2026, обновлено 23.10.2026 — https://kompozy.io/news/ai-written-web-content-study
23. More than half of new articles on the internet are being written by AI — Binghamton News / The Conversation — 12.01.2026 — https://www.binghamton.edu/news/story/6008/articles-written-by-ai-study
24. Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls — Kang et al. (Meta), arXiv 2510.01631, EMNLP 2025 — 02.10.2025 — https://arxiv.org/abs/2510.01631
25. Preventing Model Collapse: A Fisher-Rao Perspective on the Dynamics of Training with Synthetic Data — Marchi et al., arXiv 2609.18878 — 16.09.2026 — https://arxiv.org/abs/2609.18878
26. A Survey on LLM Mid-Training — Tu et al., arXiv 2510.23081 — 27.10.2025 — https://arxiv.org/abs/2510.23081
27. Why Language Models Hallucinate — Kalai, Nachum, Vempala, Zhang (OpenAI), arXiv 2509.04664 — 04.09.2025 — https://arxiv.org/abs/2509.04664
28. Introducing the Third Generation of Apple's Foundation Models — Apple Machine Learning Research — 08.06.2026 — https://machinelearning.apple.com/research/introducing-third-generation-of-apple-foundation-models
29. Continual Learning in Transition — Hou et al., arXiv 2608.06216 — 06.08.2026 — https://arxiv.org/abs/2608.06216
30. Muon: An optimizer for hidden layers in neural networks — Keller Jordan — 08.12.2024 — https://kellerjordan.github.io/posts/muon/
31. Muon is Scalable for LLM Training — Liu, Su et al. (Moonshot AI), arXiv 2502.16982 — 24.02.2025 — https://arxiv.org/abs/2502.16982
32. Spectral Scaling Laws of Muon — Magakyan, Parrilo, Ozdaglar, arXiv 2606.04058 — 02.06.2026 — https://arxiv.org/abs/2606.04058
33. Analog in-memory computing attention mechanism for fast and energy-efficient large language models — Leroux et al., Nature Computational Science 5, 813–824 — 08.09.2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12457188/
34. GenAI and Agentic AI Exploit Roundup Q3 2026 — OWASP GenAI Security Project — 08.10.2026 — https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/
35. dQwen3.5: Hybrid-Attention Diffusion Language Models — Xue et al., arXiv 2609.20751 — 17.09.2026 — https://arxiv.org/abs/2609.20751
36. Awesome-Diffusion-LLM (каталог статей 2026 года) — AIDASLab, GitHub — просмотрено 07.11.2026 — https://github.com/AIDASLab/Awesome-Diffusion-LLM
37. LLaDA2.0-Uni: Unifying Multimodal Understanding and Generation with Diffusion Large Language Model — inclusionAI, arXiv 2604.20796 — 22.04.2026 — https://huggingface.co/papers/2604.20796
38. Introducing Nested Learning: A new ML paradigm for continual learning — Google Research Blog — 07.11.2025 — https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/
39. OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications, New Agent Control Standard — OWASP GenAI Security Project — 01.09.2026 (по результату поиска, страница не открывалась) — https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/
