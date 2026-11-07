# Лекция 4. Обучение LLM: предобучение, оптимизации, SFT и LoRA — что изменилось к ноябрю 2026

*Лекция прочитана 17 октября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/04-llm-training.md) · [Все актуализации](index.md)

## Коротко

- Оптимизатор предобучения — больше не обязательно Adam: Muon стоит в Kimi K2 (июль 2025), GLM-4.5 (август 2025), DeepSeek-V4 (2026) и Kimi K3 (июль 2026); NVIDIA в июле 2026 подтвердила преимущество Muon и SOAP над AdamW на триллионах токенов [5–10].
- Точность обучения ушла ниже FP8: Nemotron 3 Super (10 марта 2026) и Ultra предобучены в NVFP4 (4-битный float) на 25 и ~20 трлн токенов [14, 15, 36]; DeepSeek-V4 обучен в FP8, инстракт-версии выпущены в FP4+FP8 [8].
- «20 токенов на параметр» стали нижней границей: scaling laws 2026 года с учётом инференса (T², апрель 2026) и повторов данных (COLM 2026) советуют «перекармливать» модели [18, 19]; флагманы 2026 обучены на 25–33 трлн токенов [7, 15].
- FlashAttention-4 (март 2026) — ядро для Blackwell: до 1605 TFLOPS/s на B200 [22, 23]; H100 с 80 ГБ уступил место B200 (192 ГБ) и B300 (288 ГБ) [31, 32].
- Fine-tuning закрытых моделей сжимается: OpenAI сворачивает self-serve fine-tuning к 6 января 2027 [27], у Anthropic его нет, Google оставляет LoRA-тюнинг Gemini [28]; в enterprise fine-tuning «по-прежнему нишевый» (Menlo, декабрь 2025) [29].
- У LoRA появился канон — «LoRA Without Regret» (29 сентября 2025), тот самый «блог за несколько недель до лекции»: все слои, LR ≈10× от full fine-tuning, для RL хватает ранга 1 [1]; Tinker и Vertex AI строят fine-tuning только на LoRA [3, 28].

## Что осталось верным

- Картина памяти при обучении (веса, градиенты, моменты оптимизатора, активации) и ответ на неё — ZeRO/FSDP, tensor/pipeline/expert parallelism — не изменились [17].
- Идея FlashAttention (tiling в SRAM, recomputation, точный результат) та же: FA4 — очередная адаптация к новому GPU, как и FA2/FA3 [22].
- Mixed precision по схеме «master-веса в высокой точности, арифметика в низкой» остаётся основой; «низкая» теперь FP8 или NVFP4, и даже рецепт NVFP4 держит часть слоёв в высокой точности [12].
- SFT как next-token prediction с loss только на ответе и малые качественные данные — всё так; изменилось то, что идёт после SFT.
- Предупреждения о Chatbot Arena подтвердились: «The Leaderboard Illusion» (29 апреля 2025) описала приватное тестирование десятков вариантов (27 у Meta перед Llama 4) и перекос выборки [26].
- Эмпирика LoRA из лекции (главный эффект в feed-forward, LR в ~10 раз выше, хуже с большим батчем) совпадает с «LoRA Without Regret» вплоть до множителя 9,8 [1].

## Что устарело или сдвинулось

- **Лекция говорит:** Llama 3 на 15 трлн токенов — верхний ориентир (раздел 2, 12:42) → **Сейчас:** DeepSeek-V4 — больше 32 трлн токенов (Flash 284B/13B активных, Pro 1,6T/49B) [7, 8]; Nemotron 3 Super (120B/12B) — 25 трлн [15]; Kimi K2 (1T/32B) — 15,5 трлн [5].
- **Лекция говорит:** при фиксированном compute оптимально ≈20 токенов на параметр (раздел 4, 19:33) → **Сейчас:** T²-законы (1 апреля 2026): с учётом стоимости инференса и test-time sampling compute-оптимум сдвигается к сильному перекармливанию [18]; законы для data-constrained режима (COLM 2026) штрафуют повторы: после порога лучше увеличивать модель, а оптимальный weight decay на порядок выше обычного [19]; «Pre-training under infinite compute» (сентябрь 2025): weight decay в ~30× выше обычного, ансамбли и дистилляция дают в 5,17 раза меньше данных до той же loss [20].
- **Лекция говорит:** оптимизатор — Adam с двумя моментами (раздел 5, 29:19) → **Сейчас:** Muon (один момент плюс ортогонализация обновления) стоит в Kimi K2/K3, GLM-4.5, DeepSeek-V4 [5–9]; по NVIDIA, Muon и SOAP сохраняют качество при батчах до 100 млн токенов, где AdamW деградирует [10]. Оговорка: full fine-tuning Adam-предобученной модели Muon'ом ухудшает качество (optimizer mismatch), LoRA разрыв сужает [11].
- **Лекция говорит:** H100 с 80 ГБ — «очень хороший GPU» (раздел 5, 30:09) → **Сейчас:** B200 — 192 ГБ HBM3e, B300 — 288 ГБ [31]; Vera Rubin «выходит на полное производство» по квартальному отчёту NVIDIA 2026 года [32].
- **Лекция говорит:** Flash Attention 2 и 3 — адаптации к новым GPU (раздел 8, 50:15) → **Сейчас:** FlashAttention-4 для Blackwell (5 марта 2026): до 1605 TFLOPS/s, 71 % утилизации B200, до 1,3× быстрее cuDNN 9.13; на Hopper остаётся FA3; пакет flash-attn-4 на PyPI всё ещё beta (4.0.0b38 от 4 ноября 2026) [22–24].
- **Лекция говорит:** forward/backward в FP16, веса в FP32 (раздел 10, 56:00) → **Сейчас:** bf16 — базовый уровень; FP8 — норма для крупных открытых моделей (DeepSeek-V4 base — «FP8 mixed») [8]; в NVFP4 предобучены Nemotron 3 Super/Ultra, а 12B-модель на 10 трлн токенов в NVFP4 сходится как FP8-baseline [12–15].
- **Лекция говорит:** MMLU и GSM8K — основные бенчмарки (раздел 12, 1:26:03) → **Сейчас:** для фронтира они насыщены (по вторичной сводке — около 93 % и 99 %; не удалось подтвердить первоисточником), в карточках моделей — GPQA Diamond, HLE, SWE-bench Verified, AIME [33].
- **Лекция говорит:** Chatbot Arena (раздел 12, 1:30:40) → **Сейчас:** с 28 января 2026 проект называется Arena (arena.ai); 8 октября 2026 компания привлекла $200 млн при оценке $3,1 млрд [25].

## Новое, о чём лекция не знала

- **LoRA Without Regret (Thinking Machines, 29 сентября 2025).** На малых и средних SFT-наборах LoRA равна full FT, если стоит на всех слоях (attention-only хуже даже при равном числе параметров); отстаёт, когда данных больше её ёмкости; оптимальный LR ≈10× от full FT и почти не зависит от ранга; в policy-gradient RL хватает ранга 1 [1].
- **Tinker (Thinking Machines, 1 октября 2025).** Training loop пишется на Python (forward_backward, optim_step, sample), счёт идёт на распределённых GPU; только LoRA, открытые модели от 1B до 1T+ (Qwen3.5-397B, Kimi K2.6), веса можно скачать [3, 4].
- **On-policy distillation (Thinking Machines, 27 октября 2025).** Ученик сэмплирует сам, учитель оценивает каждый токен (reverse KL): Qwen3-8B с 60 % до 70 % на AIME'24 за ~150 шагов; против RL из отчёта Qwen3 — 1 800 GPU-часов вместо 17 920 [2]. Третий путь между SFT и RL.
- **Olmo 3 (Ai2, 20 ноября 2025) и Olmo-core 3 (1 октября 2026).** Полностью открытый «model flow» 7B и 32B: Dolma 3 (микс 5,9 трлн токенов), midtraining Dolmino (100 млрд), long-context, затем SFT → DPO → RLVR на наборах Dolci; открыты все данные, код и чекпоинты каждой стадии [16]. Olmo-core 3 — открытый стек для MoE до триллиона параметров: эксперты резидентны на GPU (DDP вместо FSDP), 2,7× throughput, MXFP8 даёт +21 % к BF16 [17].
- **Nemotron 3 (NVIDIA, декабрь 2025 — 2026).** Nano 30B/3B (15 декабря 2025), Super 120B/12B (10 марта 2026), Ultra 550B/55B; Super и Ultra предобучены в NVFP4; открыты веса, ~3 трлн токенов pretraining-данных, синтетический корпус почти 10 трлн и 13 млн примеров post-training [12–15, 36].
- **Данные.** Epoch AI (июнь 2024): ~300 трлн токенов публичного текста, исчерпание в 2026–2032 [21]; ответ — синтетика в предобучении (Nemotron) и регуляризация при повторах [19, 20].
- **Инференс в 4-битных float.** gpt-oss (август 2025) обучен с MXFP4 в MoE-слоях, 120B помещается на один 80-ГБ GPU [30]; DeepSeek-V4 и Kimi K3 — FP4-эксперты через QAT [8, 9]; Nemotron 3 выходит в NVFP4-чекпоинтах [14].
- **Рынок fine-tuning.** OpenAI поэтапно закрывает self-serve fine-tuning (7 мая 2026, 2 июля 2026, 6 января 2027); дообученные модели работают до deprecation базовой [27]. Vertex AI: SFT для Gemini 3.5 Flash/Flash-Lite, 3.1 Flash-Lite и 2.5 через адаптеры размера 1–16, thinking на MINIMAL, для рассуждений — RL fine-tuning [28]. Claude: только Claude 3 Haiku в Bedrock (GA с ноября 2024) [35]; вывод модели 10 сентября 2026 не удалось подтвердить первоисточником [34]. Menlo (9 декабря 2025, 495 респондентов): prompt design — главный метод, RAG второй, fine-tuning «нишевый, в основном у frontier-команд», доля open-source упала с 19 % до 11 % [29].

## Что это меняет для читателя

- Дообучая открытую модель, ставьте LoRA на все слои, включая MLP/MoE, берите LR в ~10 раз выше, чем для full FT, не раздувайте батч, а ранг выбирайте по объёму данных; для RL хватит ранга 1 [1].
- Fine-tuning закрытых моделей — не долгосрочная стратегия: OpenAI закрывает, Anthropic не предлагает; остаются Google (LoRA) и хостинг открытых моделей вроде Tinker [3, 27, 28].
- Для большинства продуктовых задач по-прежнему промптинг плюс RAG фронтир-модели [29]; дообучение оправдано для формата, латентности и стоимости на объёме или on-prem.
- Для рассуждений SFT — не финал: дальше дистилляция (в том числе on-policy) или RLVR; при тюнинге thinking-моделей Google советует отключать thinking или идти в RL fine-tuning [2, 28].
- Выбирая открытую модель, смотрите на нативный формат весов: FP8/FP4-чекпоинты рассчитаны на Blackwell-класс железа, на H100 выигрыша в скорости от FP4 нет [30].
- Muon при дообучении Adam-предобученной модели даёт просадку; LoRA её смягчает [11].

## Проверка пометок в конспекте

- «Дополнение — связь с лекцией 8» (раздел 12): «по состоянию на 2026 год проект называется LMArena» — неточно: с 28 января 2026 он называется Arena, сайт arena.ai [25].
- «Низкие точности за пределами bf16» («Чем можно дополнить»): «уже обучают с FP8 в части операций, а для инференса стандартом стали int8 и int4» — неполно: есть предобучение в NVFP4 (Nemotron 3 Super/Ultra) и FP4-QAT (DeepSeek-V4, Kimi K3), а в инференсе наряду с int4/int8 стандартом стали FP8 и 4-битные float (MXFP4 у gpt-oss, NVFP4 у Nemotron) [8, 9, 14, 30].
- «Дополнение — уточнение» (раздел 10): «современные модели обучают в bf16» — верно как базовый уровень, но крупные модели 2025–2026 обучают в FP8 и NVFP4 [8, 15].
- «Дополнение — связь с лекцией 5» (раздел 12): конвейер pretraining → (mid-training) → SFT → preference tuning — верно, но после DPO у открытых моделей теперь стоит RLVR, а рядом с SFT — on-policy distillation [2, 16].
- Остальные пометки (FLOPs H100, 16 байт на параметр, ZeRO/FSDP, 3D parallelism, SDPA, GPTQ/AWQ/GGUF, метка -100, Alpaca, арифметика LoRA, QLoRA) противоречий с источниками не имеют.

## Источники

1. LoRA Without Regret — Thinking Machines Lab (J. Schulman et al.) — 29.09.2025 — https://thinkingmachines.ai/blog/lora/
2. On-Policy Distillation — Thinking Machines Lab (K. Lu et al.) — 27.10.2025 — https://thinkingmachines.ai/blog/on-policy-distillation/
3. Tinker: a training API for researchers and developers — Tinker Documentation — 2026 — https://tinker-docs.thinkingmachines.ai/tinker/
4. Announcing Tinker — Thinking Machines Lab — 01.10.2025 — https://thinkingmachines.ai/news/announcing-tinker/
5. Kimi K2: Open Agentic Intelligence — Kimi Team, arXiv 2507.20534 — июль 2025 (v2 февраль 2026) — https://arxiv.org/abs/2507.20534
6. GLM-4.5: Agentic, Reasoning, and Coding Foundation Models — Zhipu AI, arXiv 2508.06471 — август 2025 — https://arxiv.org/abs/2508.06471
7. DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence — DeepSeek-AI, arXiv 2606.19348 — 2026 — https://arxiv.org/abs/2606.19348
8. DeepSeek-V4-Pro model card — Hugging Face — 2026 — https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro
9. Kimi K3: Open Frontier Intelligence — Kimi Team, arXiv 2607.24653 — 27.07.2026 — https://arxiv.org/abs/2607.24653
10. SOAP, Muon, and Beyond: Pushing LLM Pretraining Scales — Khona et al. (NVIDIA), arXiv 2607.20548 — 13.07.2026 — https://arxiv.org/abs/2607.20548
11. Can Muon Fine-tune Adam-Pretrained Models? — arXiv 2605.10468 — 11.05.2026 — https://arxiv.org/abs/2605.10468
12. Pretraining Large Language Models with NVFP4 — NVIDIA, arXiv 2509.25149 — 29.09.2025 (v2 04.03.2026) — https://arxiv.org/abs/2509.25149
13. Inside NVIDIA Nemotron 3: Techniques, Tools, and Data — NVIDIA Developer Blog — 15.12.2025 — https://developer.nvidia.com/blog/inside-nvidia-nemotron-3-techniques-tools-and-data-that-make-it-efficient-and-accurate/
14. NVIDIA Nemotron 3 Super — NVIDIA Research — 10.03.2026 — https://research.nvidia.com/labs/nemotron/Nemotron-3-Super/
15. Nemotron 3 Super: Open, Efficient MoE Hybrid Mamba-Transformer Model — NVIDIA, arXiv 2604.12374 — 14.04.2026 — https://arxiv.org/abs/2604.12374
16. Olmo 3: Charting a path through the model flow to lead open-source AI — Ai2 — 20.11.2025 — https://allenai.org/blog/olmo3
17. Introducing Olmo-core 3 — Ai2 — 01.10.2026 — https://allenai.org/blog/olmocore3
18. Test-Time Scaling Makes Overtraining Compute-Optimal — Roberts et al., arXiv 2604.01411 — 01.04.2026 — https://arxiv.org/abs/2604.01411
19. Prescriptive Scaling Laws for Data Constrained Training — Lovelace et al., arXiv 2605.01640 (COLM 2026) — 02.05.2026 (v2 04.11.2026) — https://arxiv.org/abs/2605.01640
20. Pre-training under infinite compute — Kim, Kotha, Liang, Hashimoto, arXiv 2509.14786 — 18.09.2025 — https://arxiv.org/abs/2509.14786
21. Will we run out of data? — Epoch AI — 06.06.2024 — https://epoch.ai/blog/will-we-run-out-of-data-limits-of-llm-scaling-based-on-human-generated-data
22. FlashAttention-4: Algorithm and Kernel Pipelining Co-Design — Tri Dao — 05.03.2026 — https://tridao.me/blog/2026/flash4/
23. FlashAttention-4 gives the NVIDIA Blackwell platform its most optimized attention kernel yet — Lambda — март 2026 — https://lambda.ai/blog/flashattention-4-gives-the-nvidia-blackwell-platform-its-most-optimized-attention-kernel-yet
24. flash-attn-4 — PyPI — 04.11.2026 (4.0.0b38) — https://pypi.org/project/flash-attn-4/
25. Arena (AI platform) — Wikipedia — просмотрено 07.11.2026 — https://en.wikipedia.org/wiki/Arena_(AI_platform)
26. The Leaderboard Illusion — Singh, Hooker et al. (Cohere Labs), arXiv 2504.20879 — 29.04.2025 — https://arxiv.org/abs/2504.20879
27. Deprecations — OpenAI API docs — 2026 — https://developers.openai.com/api/docs/deprecations
28. About supervised fine-tuning for Gemini models — Google Cloud Vertex AI docs — просмотрено 07.11.2026 — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning
29. 2025: The State of Generative AI in the Enterprise — Menlo Ventures — 09.12.2025 — https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/
30. gpt-oss-20b model card — OpenAI, Hugging Face — август 2025 — https://huggingface.co/openai/gpt-oss-20b
31. NVIDIA Data Center GPU Specs: A Complete Comparison Guide — IntuitionLabs — 2026 — https://intuitionlabs.ai/articles/nvidia-data-center-gpu-specs
32. NVIDIA Form 8-K, Q2 FY2027 results — SEC — 2026 — https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm
33. Frontier AI Models Evaluation Benchmarks — kharshit.github.io — 2026 — https://kharshit.github.io/blog/frontier-ai-models-evaluation-benchmarks/
34. Can You Fine-Tune Claude? Options and Limits in 2026 — Qlauson — 2026 — https://qlauson.com/articles/fine-tune-claude
35. Fine-tuning for Anthropic's Claude 3 Haiku in Amazon Bedrock is now generally available — AWS — ноябрь 2024 — https://aws.amazon.com/about-aws/whats-new/2024/11/fine-tuning-anthropics-claude-3-haiku-amazon-bedrock
36. Nemotron 3 Ultra: Open, Efficient MoE Hybrid Mamba-Transformer Model — NVIDIA, arXiv 2606.15007 — июнь 2026 — https://arxiv.org/abs/2606.15007
