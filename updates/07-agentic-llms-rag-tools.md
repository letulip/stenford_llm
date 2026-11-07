# Лекция 7. Агентные LLM: RAG, вызов инструментов, агенты — что изменилось к ноябрю 2026

*Лекция прочитана 14 ноября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/07-agentic-llms-rag-tools.md) · [Все актуализации](index.md)

## Коротко

- **MCP перестал быть «стандартом от Anthropic».** 9 декабря 2025 протокол передан в Agentic AI Foundation (AAIF) под Linux Foundation [4][6]; ревизия 2026-07-28 сделала его stateless и объявила Roots/Sampling/Logging deprecated [1].
- **Agent2Agent дорос до 1.0.** v1.0.0 — 12 марта 2026 с breaking changes, v1.0.1 — май 2026 [7]; по данным Linux Foundation на 9 апреля 2026 — более 150 организаций, интеграции в Azure AI Foundry, Copilot Studio и Bedrock AgentCore [8].
- **Tool selection из лекции стал функцией API.** Anthropic выпустила Tool Search Tool и Programmatic Tool Calling 24 ноября 2025: инструменты с `defer_loading` подгружаются по запросу, стартовый контекст с 50+ MCP-инструментами ужался с ~77K до ~8.7K токенов [9].
- **Retrieval для агентов сместился к «agentic search».** В исходниках 11 кодинг-агентов (июль 2026) ни один не ищет код по vector embeddings [15]; статьи мая 2026: grep/shell в руках агента обходят dense/sparse/rerank baselines на ряде бенчмарков [16][17].
- **Безопасность: от одного примера к систематике.** Более 15 реальных инцидентов MCP с апреля 2025 по сентябрь 2026 [32][33], OWASP MCP Top 10 [34], рекомендации NSA (май 2026) [35]; SoK января 2026: большинство защит дают менее 50 % митигации против адаптивных атак [36].
- **Хостинг агентов стал продуктом.** Claude Managed Agents — публичная бета 9 апреля 2026, $0.08 за час сессии сверх токенов [21]; OpenAI на DevDay 29 сентября 2026 показала always-on агентов Dots и Agents API с hosted sandboxes [22][23].

## Что осталось верным

- Двухэтапный retrieval (bi-encoder на recall → cross-encoder на ранжирование), cosine similarity, ANN, метрики NDCG/MRR/precision@k/recall@k и MTEB — без изменений; новые модели [19][20] укладываются в ту же схему.
- BM25 и гибрид — верно вдвойне: работы 2026 года по agentic search показывают, что лексического поиска агенту часто достаточно [16][17].
- Три стадии tool calling и описание инструментов через JSON Schema — так устроены все основные API и MCP (`inputSchema` по JSON Schema 2020-12 [2]).
- Prompt caching: кэшируется префикс, порядок tools → system → messages у Anthropic фиксирован до сих пор [10].
- Цикл observe → plan → act: в Claude Agent SDK это «gather context → take action → verify work» [14]; совет «начинать с малого и читать трассы» подтверждён тем, что результат зависит от харнесса не меньше, чем от модели [15][17].
- Главный риск — prompt injection и утечка данных через инструменты: именно это и реализовалось в инцидентах [32][33].

## Что устарело или сдвинулось

1. **Лекция говорит:** MCP — стандарт от Anthropic (раздел 11, 1:29:17) → **Сейчас:** проект AAIF/Linux Foundation с 9 декабря 2025 [4]; формализованы working groups, contributor ladder и политика deprecation с минимальным окном 12 месяцев [1][3]. Масштаб на момент передачи — более 97 млн загрузок SDK в месяц и не менее 10 000 серверов [5].
2. **Лекция говорит:** MCP client связан с сервером один-к-одному; словарь — server, tools, prompts, resources, client (раздел 11) → **Сейчас:** ревизия 2026-07-28 убрала протокольные сессии, `Mcp-Session-Id` и handshake `initialize`; версия и capabilities едут в `_meta` каждого запроса; tasks вынесены в расширение; Roots, Sampling, Logging и HTTP+SSE — deprecated [1]. Клиенты и серверы разных версий могут не стыковаться без шлюза [5].
3. **Лекция говорит:** Agent2Agent «появился в этом году» от Google (раздел 12, 1:39:50) → **Сейчас:** v1.0.0 от 12 марта 2026 разделила протокол и транспортные привязки (JSON-RPC, gRPC, REST), добавила multi-tenancy и заменила implicit OAuth-flow на PKCE; подписанные Agent Cards — с v0.3.0 (июль 2025) [7]. Проект живёт в Linux Foundation [8]; его передачу в AAIF не удалось подтвердить источником.
4. **Лекция говорит:** tool selection — двухшаговая схема из отчёта DeepMind (раздел 10, 1:26:22) → **Сейчас:** встроено в API: Tool Search Tool ищет по описаниям (BM25 или regex) и разворачивает только найденные инструменты; точность на MCP-оценках выросла с 49 % до 74 % (Opus 4) и с 79.5 % до 88.1 % (Opus 4.5) [9]. Roadmap MCP (август 2026) ставит «progressive discovery» в приоритеты [3].
5. **Лекция говорит:** у OpenAI кэшированный токен стоит 1/10 (раздел 6, 43:56) → **Сейчас:** чтение 0.1× для GPT-5.6+, 0.05× для GPT-6.1 Sol/Terra, но с GPT-5.6 запись в кэш платная: 1.25× (TTL 30 мин) или 2.5× (12 ч) [11]. У Anthropic чтение 0.1× по умолчанию, 0.05× для Opus 5.5/Sonnet 5.5 и 0.025× для Fable 5.1/Mythos 5.1; запись 1.25× (5 мин) или 2× (1 ч); минимум 512 токенов на новых моделях; появился автоматический режим — одна верхнеуровневая `cache_control` [10].
6. **Лекция говорит:** контекст — сотни тысяч токенов, needle-in-a-haystack для GPT-4 (раздел 2, 09:23) → **Сейчас:** Chroma на 18 моделях (июль 2025): качество падает задолго до лимита, сильнее при низком сходстве «иголки» и вопроса и при дистракторах [13]; Anthropic (сентябрь 2025) вводит context engineering и «attention budget» [12]. Второй аргумент лектора стал главным.
7. **Лекция говорит:** слышите «retrieval» — думайте «embeddings» (раздел 2, 19:48) → **Сейчас:** для агентов над локальным корпусом — не обязательно. Claude Agent SDK советует начинать с agentic search (grep, tail) и добавлять семантический поиск только при нужде [14]; «Beyond Semantic Similarity» (3 мая 2026): работа с корпусом через grep/shell без индекса обходит sparse/dense/rerank baselines на BRIGHT и BEIR [16]; «Is Grep All You Need?» (14 мая 2026): grep точнее vector retrieval на LongMemEval, но итог зависит от харнесса [17]. Embeddings остаются для больших и внешних корпусов.
8. **Лекция говорит:** крупномасштабных агентов пока нет, ошибки накапливаются (раздел 13, 1:46:07) → **Сейчас:** Codex превысил 2 млн недельных пользователей к середине марта 2026 [26]; Managed Agents используют Notion, Rakuten, Sentry [21]. Но на OSWorld 2.0 (июнь 2026, 108 workflow по 1.6 часа человеческой работы) лучший результат — 20.6 % решённых задач [27], на Terminal-Bench 2.0 — ниже 65 % [28]. Тезис верен в смягчённом виде.
9. **Лекция говорит:** Agent-SafetyBench как ориентир; защита в данных обучения плюс safety classifier (раздел 13, 1:43:19) → **Сейчас:** SoK (24 января 2026, 78 работ): адаптивные атаки успешны более чем в 85 % случаев против state-of-the-art защит [36]; Abdelnabi и Bagdasarian (май 2026) показывают, что разделение «инструкции/данные» принципиально недостаточно, и предлагают Contextual Integrity [37]; LivePI (май 2026) на реальной VM даёт 10.7–29.6 % успешных injection для GPT-5.3-Codex, Claude Opus 4.6, Gemini 3.1 Pro, а защита «фильтр + авторизация вызова до исполнения» блокировала все вредоносные цели в тестах [38].

## Новое, о чём лекция не знала

- **Programmatic Tool Calling** (Anthropic, 24 ноября 2025): модель пишет код, вызывающий инструменты в песочнице, и в контекст попадает только итог — на research-задачах токенов стало на 37 % меньше (43 588 → 27 297) [9].
- **Managed Agents / Agents API.** Anthropic (9 апреля 2026) хостит харнесс, sandbox, состояние сессии и инструменты (bash, файлы, web search, MCP) [21]. OpenAI на DevDay 29 сентября 2026: Dots — always-on агенты на GPT-6 Astra с собственным облачным компьютером [22]; Agents API с sessions, hosted sandboxes и multi-agent; поддержка draft-спецификации MCP Events через webhooks [23]. Дату публичной беты Agents API (10 сентября 2026) видел только на форуме OpenAI [24].
- **Агентные IDE и CLI.** Google Antigravity (18 ноября 2025, вместе с Gemini 3): агенты с терминалом и браузером, sandbox-режимы; версия 2.0 с CLI и SDK — 19 мая 2026 [25]. Codex: desktop-приложение (февраль 2026), слияние с ChatGPT desktop (июль 2026) [26].
- **Skills и ACP.** В 11 харнессах Skills распространены шире MCP (9 против 8 систем), ACP — в 6; ни один не импортирует общий агентный фреймворк [15].
- **Бенчмарки агентов.** MCP-Atlas (Scale AI, 31 января 2026): 1 000 задач на 36 реальных MCP-серверах с отвлекающими инструментами; топ — 82.2 %, причём 63.3 % ошибок когнитивные (синтез, преждевременная остановка), а не ошибки вызова [29]. τ²-bench (июнь 2025): dual-control — пользователь тоже пользуется инструментами, и качество падает [30]. BFCL v4: web search, память, чувствительность к формату [31].
- **Embeddings 2026.** Gemini Embedding 2 — нативно мультимодальная (текст, изображения, видео, аудио, документы), 128–3072 измерений (Matryoshka), MTEB Multilingual 69.9 против 68.4 у предшественника [19]. Qwen3-Embedding и Qwen3-Reranker (0.6B–8B, открытые веса) — сильный open-source дефолт [20].
- **Управление контекстом агента** как дисциплина: compaction, structured notes, sub-agents с чистыми контекстами [12]; «Agentic Context Management» (июль 2026) трактует память агента как lifecycle, а не хранилище [18].
- **Инциденты MCP 2026** (все — экосистема, не модель): command injection в неофициальном gemini-mcp-tool, CVE-2026-0755 (январь), троянский «Oura MCP» в реестрах (февраль), изъян STDIO-транспорта с 10 CVE (апрель) [32]; AWS Kiro CVE-2026-10591 (июль), Dolt и Grafana — поддельные session ID, CVE-2026-19516 (август), «Deadbugz» — tool poisoning, включающееся после третьего вызова (август), утечка OAuth client secret в Python SDK (сентябрь) [33].
- **Отчёт Anthropic о GTG-1002** (13 ноября 2025): около 30 целей, Claude Code с MCP-инструментами выполнял 80–90 % работы; обход защит — дробление задачи на безобидные шаги и легенда «авторизованный pentest» [39].

## Что это меняет для читателя

- Не грузите все инструменты сразу: используйте `defer_loading`/tool search или свой router; описания инструментов — кэшируемый префикс, и спецификация 2026-07-28 просит детерминированный порядок `tools/list` ради cache hits [1][9].
- Для локального или кодового корпуса начинайте с agentic search (grep + чтение файлов) и добавляйте embeddings, когда корпус велик, внешний или запросы семантические; решайте по измерениям на своих задачах [14][16].
- Считайте экономику кэша заново: запись теперь платная у обоих провайдеров, выгода есть только при повторах внутри TTL; на новых моделях чтение дешевле в 20–40 раз [10][11].
- Безопасность — архитектура, а не фильтр: sandbox и egress-контроль, least privilege для токенов, авторизация опасных вызовов до исполнения, аудит изменений описаний инструментов, проверка пакетов и версий MCP-серверов [33][35][38].
- Оценивайте агентов на повторных прогонах и реальных серверах (MCP-Atlas, τ²-bench), отдельно — на injection (LivePI); харнесс меняет результат не меньше модели [17][29][30].
- Следите за версией протокола: серверы на 2025-11-25 и 2026-07-28 несовместимы без шлюза; не стройте новое на Sampling, Roots и HTTP+SSE [1][5].

## Проверка пометок в конспекте

- «Аргумент "контекст ограничен" слабеет…» — верно; Chroma и Anthropic подтверждают, что деградация начинается задолго до лимита [12][13].
- «Названная лектором размерность "около 1 500"…» — верно; дополнение: у новых моделей размерность настраиваемая, 128–3072 у Gemini Embedding 2 [19].
- «Кэшируется только префикс…» — неточно к ноябрю 2026: у Anthropic есть автоматический режим, минимум 512 токенов и чтение 0.05×/0.025× на новых моделях [10]; у OpenAI с GPT-5.6 запись платная (1.25×/2.5×), TTL 30 мин или 12 ч [11]. Противопоставление «запись дороже только у Anthropic» устарело.
- «Сама модель "не говорит на MCP"…» — верно, включая прогноз про отложенную загрузку схем [3][9]. Уточнить таблицу лекции: с 2026-07-28 протокол stateless, и «соединение один-к-одному» не является сущностью протокола [1].
- «Пример с паролем — частный случай prompt injection…» — верно: страница Anthropic описывает около 30 сторонних целей и не называет Anthropic жертвой [39]. Добавить: правило «результаты инструментов — данные, а не команды» необходимо, но по SoK и работе о Contextual Integrity недостаточно [36][37].
- Остальные блоки (chunking, RRF, contextual retrieval, rerankers, пример NDCG, RAGAS, JSON Schema, SFT/DSPy, агентный цикл) — противоречий с источниками не найдено.

## Источники

1. Key Changes, MCP specification 2026-07-28 — modelcontextprotocol.io — 28 июля 2026 — https://modelcontextprotocol.io/specification/2026-07-28/changelog
2. Key Changes, MCP specification 2025-11-25 — modelcontextprotocol.io — 25 ноября 2025 — https://modelcontextprotocol.io/specification/2025-11-25/changelog
3. The New MCP Roadmap — blog.modelcontextprotocol.io, D. Soria Parra, D. Delimarsky — 22 августа 2026 — https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
4. Linux Foundation Announces the Formation of the Agentic AI Foundation — linuxfoundation.org — 9 декабря 2025 — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
5. Model Context Protocol prepares to break with its stateful past — The Register, J. Jackson — 23 июля 2026 — https://www.theregister.com/a/5276722
6. Model Context Protocol — Wikipedia — прочитано 7 ноября 2026 — https://en.wikipedia.org/wiki/Model_Context_Protocol
7. Releases, a2aproject/A2A — GitHub — v1.0.0 12 марта 2026, v1.0.1 май 2026 — https://github.com/a2aproject/A2A/releases
8. A2A Protocol Surpasses 150 Organizations… — Linux Foundation — 9 апреля 2026 — https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year
9. Advanced tool use — Anthropic Engineering — 24 ноября 2025 — https://www.anthropic.com/engineering/advanced-tool-use
10. Prompt caching — Claude Platform Docs — прочитано 7 ноября 2026 — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
11. Prompt caching — OpenAI API Docs — прочитано 7 ноября 2026 — https://developers.openai.com/api/docs/guides/prompt-caching
12. Effective context engineering for AI agents — Anthropic Engineering — 29 сентября 2025 — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
13. Context Rot: How Increasing Input Tokens Impacts LLM Performance — Chroma Research — 14 июля 2025 — https://www.trychroma.com/research/context-rot
14. Building agents with the Claude Agent SDK — Anthropic — 29 сентября 2025 — https://claude.com/blog/building-agents-with-the-claude-agent-sdk
15. Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents — A Source-Code Study of Eleven Systems — arXiv 2609.00006 — 15 июля 2026 — https://arxiv.org/abs/2609.00006
16. Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction — arXiv 2605.05242 — 3 мая 2026 — https://arxiv.org/abs/2605.05242
17. Is Grep All You Need? How Agent Harnesses Reshape Agentic Search — arXiv 2605.15184 — 14 мая 2026 — https://arxiv.org/abs/2605.15184
18. Agentic Context Management — arXiv 2607.21503 — 23 июля 2026 — https://arxiv.org/abs/2607.21503
19. Gemini Embedding 2 — Google DeepMind — прочитано 7 ноября 2026 — https://deepmind.google/models/gemini/embedding/
20. Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models — arXiv 2506.05176 — июнь 2025 — https://arxiv.org/abs/2506.05176
21. Anthropic launches managed infrastructure for autonomous AI agents — The Decoder, M. Schreiner — 9 апреля 2026 — https://the-decoder.com/anthropic-launches-managed-infrastructure-for-autonomous-ai-agents/
22. OpenAI DevDay 2026 live updates — CNBC — 29 сентября 2026 — https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html
23. DevDay 2026 — OpenAI Help Center (What's new) — прочитано 7 ноября 2026 — https://learn.chatgpt.com/docs/whats-new/devday-2026
24. DevDay 2026 announcements and developer resources — OpenAI Developer Community — сентябрь 2026 — https://community.openai.com/t/devday-2026-announcements-and-developer-resources/1402006
25. Google Antigravity — Wikipedia — прочитано 7 ноября 2026 — https://en.wikipedia.org/wiki/Google_Antigravity
26. OpenAI Codex (AI agent) — Wikipedia — прочитано 7 ноября 2026 — https://en.wikipedia.org/wiki/OpenAI_Codex_(AI_agent)
27. OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks — arXiv 2606.29537 — 28 июня 2026 — https://arxiv.org/abs/2606.29537
28. Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces — arXiv 2601.11868 — 17 января 2026 — https://arxiv.org/abs/2601.11868
29. MCP-Atlas: A Large-Scale Benchmark for Tool-Use Competency with Real MCP Servers — arXiv 2602.00933 — 31 января 2026 — https://arxiv.org/abs/2602.00933
30. τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment — arXiv 2506.07982 — 9 июня 2025 — https://arxiv.org/abs/2506.07982
31. BFCL V4 Part 3: Agentic Format Sensitivity — Gorilla, UC Berkeley — 17 июля 2025 — https://gorilla.cs.berkeley.edu/blogs/17_bfcl_v4_prompt_variation.html
32. A Timeline of Model Context Protocol (MCP) Security Breaches — AuthZed — 25 ноября 2025, обновлено 30 мая 2026 — https://authzed.com/blog/timeline-mcp-breaches
33. MCP Security: Risks, Real Incidents and Best Practices — Pillar Security — обновлено 11 октября 2026 — https://www.pillar.security/blog/the-security-risks-of-model-context-protocol-mcp
34. OWASP MCP Top 10 — OWASP — прочитано 7 ноября 2026 — https://owasp.org/www-project-mcp-top-10/
35. NSA warns enterprises over security gaps in AI agent protocol — TechInformed — май 2026 (сам CSI «MCP: Security Design Considerations…» на media.defense.gov прочитать не удалось) — https://techinformed.com/nsa-warns-enterprises-over-security-gaps-in-ai-agent-protocol/
36. Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis… — arXiv 2601.17548 — 24 января 2026 — https://arxiv.org/abs/2601.17548
37. AI Agents May Always Fall for Prompt Injections — S. Abdelnabi, E. Bagdasarian, arXiv 2605.17634 — 17 мая 2026 — https://arxiv.org/abs/2605.17634
38. LivePI: More Realistic Benchmarking of Agents Against Indirect Prompt Injection — arXiv 2605.17986 — 18 мая 2026 — https://arxiv.org/abs/2605.17986
39. Disrupting the first reported AI-orchestrated cyber espionage campaign — Anthropic — 13 ноября 2025 — https://www.anthropic.com/news/disrupting-AI-espionage
