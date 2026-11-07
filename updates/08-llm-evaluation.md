# Лекция 8. Оценка LLM: метрики, LLM-as-a-judge, бенчмарки — что изменилось к ноябрю 2026

*Лекция прочитана 21 ноября 2025. Сверено с источниками 7 ноября 2026.*

← [Конспект лекции](../lectures/08-llm-evaluation.md) · [Все актуализации](index.md)

## Коротко

- SWE-bench Verified, «бенчмарк кода» лекции, фактически списан: 23 февраля 2026 OpenAI перестала по нему отчитываться из-за насыщения, контаминации и дефектных тестов и рекомендует SWE-bench Pro [1][2]; соавтор бенчмарка Ofir Press называет потолок 93,9% [3].
- AIME и GPQA исчерпаны фронтиром: на AIME 2026 (прогон MathArena 31 октября 2026) лучшие модели дают 100% [8], Claude Mythos Preview — 94,5% на GPQA Diamond (7 апреля 2026) [19]. Роль «трудного экзамена» перешла к Humanity's Last Exam (54,8% у лидера на 17 сентября 2026) и HLE-Diamond (22 сентября 2026) [9][10].
- Появились интерактивные и «экономические» бенчмарки: ARC-AGI-3 (25 марта 2026; фронтир на старте 0,51%, в сентябре 62,7%) [11][12] и GDPval от OpenAI (октябрь 2025, ICLR 2026) с экспертной рубричной проверкой [13].
- Исследования LLM-as-a-judge 2026 года сместили фокус с position bias на style bias и артефакты рубрик: в сравнении девяти стратегий дебиасинга position bias ≤0,04, style bias до 0,76 [14]; self-preference сохраняется даже при объективных критериях [15].
- Anthropic опубликовала (9 января 2026) практическое руководство по оценке агентов: task/trial/grader/transcript/outcome, capability- против regression-evals, pass@k против pass^k [17]; трассы агентов стандартизируются в OpenTelemetry GenAI conventions [18].
- Chatbot Arena, которую лекция называла «ближе к реальности», получила системную критику («The Leaderboard Illusion», апрель 2025) [5]; платформа стала компанией Arena (ребрендинг 28 января 2026) [6].

## Что осталось верным

- Вся первая половина лекции — kappa, ограничения BLEU/ROUGE, судья «rationale → score», structured output, бинарная шкала, калибровка по людям — не устарела. Руководство Anthropic 2026 года повторяет те же правила: калибровать судью по экспертам, одна размерность на рубрику, отдельный судья на каждую [17].
- Три смещения судьи реальны; position bias по-прежнему лечится перестановкой, но оказался малым на фоне стилевого [14]. Self-enhancement bias подтверждён и в рубричной оценке [15].
- Семь отказов агентного цикла и совет «инструмент всегда возвращает структурированный ответ» — именно то, что теперь формализуют трассами [18]; Anthropic тоже советует грейдить конечное состояние, а не путь [17].
- pass^k из τ-bench стал общепринятым: Anthropic использует его там, где важна стабильность агента [17].
- Data contamination и закон Гудхарта — главный сюжет года: история SWE-bench Verified иллюстрирует оба буквально [1][2][4].

## Что устарело или сдвинулось

- **Лекция говорит:** SWE-bench — рабочий бенчмарк кода, лаборатории отчитываются по нему (раздел 15, 1:34:00) → **Сейчас:** OpenAI с 23 февраля 2026 не публикует SWE-bench Verified: зонд контаминации нашёл воспроизведение gold-патчей по одному ID задачи, а среди 138 проблемных задач 49 имели слишком узкие тесты, 26 — слишком широкие [1][2]. Ещё раньше «The SWE-Bench Illusion» показала, что модели угадывают путь к файлу по тексту issue в 76% случаев [4]. Anthropic в апреле 2026 ещё приводит Verified (93,9%), но рядом SWE-bench Pro (77,8%) и Terminal-Bench 2.0 [19]. Преемники: SWE-bench Pro (1 865 задач, 41 репозиторий, скрытый и коммерческий сплиты) [7], Terminal-Bench 2.0/2.1/3.0 [20].
- **Лекция говорит:** AIME — «очень трудный» экзамен с жёсткой проверкой (раздел 14, 1:29:35) → **Сейчас:** формат исчерпан: на AIME 2026 GPT-5.5 и Claude Opus 4.8 — 100%, ещё десяток моделей ≥96,7% (MathArena, 31 октября 2026, без инструментов; данные через агрегатор) [8]. Для математики лаборатории переходят на задачи с доказательствами (USAMO 2026 в карте Mythos) [19].
- **Лекция говорит:** MMLU — показательный бенчмарк знаний (раздел 13, 1:25:12) → **Сейчас:** в системной карте Claude Mythos Preview из семейства MMLU остался только многоязычный MMMLU (92,7%), а «знания уровня PhD» меряют GPQA Diamond (94,5%, почти потолок) и HLE (56,8% без инструментов) [19]. HLE (2 500 вопросов, публикация в Nature 28 января 2026) из-за приближения к шумовому потолку получил форки HLE-Rolling и HLE-Diamond — 1 000 очищенных вопросов, лучший результат 59,9% без инструментов и 82,9% с поиском и кодом [9][10].
- **Лекция говорит:** Chatbot Arena ближе к «реальной» производительности (раздел 17, 1:48:08) → **Сейчас:** «The Leaderboard Illusion» (29 апреля 2025) задокументировала приватное тестирование 27 вариантов Llama 4 перед релизом, неравный доступ к данным (Google 19,2%, OpenAI 20,4% всех данных арены) и выигрыш до 112% от дообучения на них [5]. Арена остаётся сигналом, но не «истиной» [6].
- **Лекция говорит:** главные смещения судьи — position, verbosity, self-enhancement (раздел 8, 38:48) → **Сейчас:** «Judging the Judges» (25 апреля 2026, TMLR): position bias ≤0,04 у всех пяти судей, verbosity зависит от модели (Claude предпочитает краткость, Gemini и Llama — длину), а доминирует style bias — предпочтение markdown-оформления (0,10–0,76). Дешёвый судья с дебиасингом (Gemini 2.5 Flash: 71,0% согласия, κ=0,549, ≈$0,001) обошёл фронтирного (Claude Sonnet 4: 69,5%, ≈$0,015) [14].
- **Лекция говорит:** τ-bench — две области, airline и retail (раздел 17, 1:40:52) → **Сейчас:** τ³-bench 1.0 (18 марта 2026) добавил голосовую модальность, домен banking_knowledge и 75+ исправлений задач; τ-bench 2.0 (19 октября 2026) — шесть языков, домен intake и пост-хок судей; результаты 2.0 несопоставимы с 1.x [16].

## Новое, о чём лекция не знала

- **Руководство Anthropic по оценке агентов** (9 января 2026). Вводит словарь (task, trial, grader, transcript, outcome, harness), делит evals на capability (стартуют с низкого pass rate) и regression (держатся у 100%), советует начинать с 20–50 задач из реальных отказов, изолировать trials, грейдить конечное состояние, давать судье вариант «Unknown» и регулярно читать транскрипты [17].
- **Рубричная оценка и её патологии.** Списки бинарных критериев стали основным способом грейдить открытые ответы: так устроен GDPval [13], так советует Anthropic [17]. Но 2026 год принёс три предупреждения: self-preference bias сохраняется даже при объективных критериях — судья более чем на 50% чаще засчитывает провальный критерий собственному ответу, сдвиг до 10 пунктов на HealthBench [15]; «rubric interference» — вердикт по критерию меняется от состава остальных, полностью согласованы лишь треть примеров [21]; «rubric artifacts» — классификатор по одному тексту рубрики предсказывает вердикт, а при инверсии ответа судья часто не меняет решения (EMNLP 2026) [22].
- **GDPval** (OpenAI, октябрь 2025, ICLR 2026): 44 профессии из 9 крупнейших секторов экономики США, задачи от практиков со стажем в среднем 14 лет, открытый gold-набор из 220 задач; по выводу авторов, лучшие модели приближаются к отраслевым экспертам [13].
- **ARC-AGI-3** (25 марта 2026): первый полностью интерактивный бенчмарк — сотни игровых сред без инструкций; люди 100%, фронтир на старте 0,51% [11]. 3 сентября 2026 GPT-6 Astra показала 62,7% в стандартном харнессе (≈$26 тыс. за прогон) и 99,9% с provider adapter — результат зависит от харнесса не меньше, чем от модели [12]. ARC-AGI-2 доведён до 95,0% [12].
- **Композитные индексы.** Epoch Capabilities Index (октябрь 2025) сшивает более 50 бенчмарков в одну шкалу (Claude 3.5 Sonnet = 130, GPT-5 = 150), потому что отдельные тесты насыщаются за месяцы [23]. METR Time Horizon 1.1 (29 января 2026): 228 задач, удвоение «горизонта» каждые 131 день с 2023 года; выше 16 часов измерения ненадёжны [24][25].
- **Поведенческие evals с LLM-судьёй.** Bloom от Anthropic (19 декабря 2025) генерирует сценарии под заданное поведение (сикофантия, самосохранение), прогоняет 16 моделей и валидирует судью по 40 размеченным транскриптам (Spearman 0,86 у Claude Opus 4.1) — подход HarmBench, где классификатор заменён судьёй с проверкой на людях [26].
- **Стандарт трасс.** OpenTelemetry вынес GenAI semantic conventions в отдельный репозиторий: span'ы `invoke_agent`, `create_agent`, `execute_tool`, атрибуты `gen_ai.agent.name`, `gen_ai.provider.name`, `gen_ai.usage.*`; статус пока Development [18].
- **Контаминация как процедура.** OpenAI описала «аудитор-агента», ищущего регургитацию решений по ID задач [2]; Anthropic применяет корпусную деконтаминацию, но признаёт «некоторые признаки запоминания» и не публикует MMMU-Pro, где контаминацию не удаётся оценить [19].

## Что это меняет для читателя

- Не выбирайте модель по SWE-bench Verified, AIME или MMLU: у фронтира они на потолке и контаминированы. Смотрите SWE-bench Pro, Terminal-Bench, τ-bench 2.0, HLE-Diamond — всегда с датой и харнессом [1][12][16].
- Проверяйте судью на стилевое смещение: выровняйте форматирование ответов (plain text против markdown), прежде чем сравнивать версии промпта [14]. Перестановка A/B остаётся дешёвой гигиеной, но не главной защитой.
- Рубрики — не панацея: по одному критерию на судью, контрфактический тест (меняется ли вердикт при порче ответа) и никакой самооценки моделью собственных генераций даже по «объективным» пунктам [15][21][22].
- Для агентов: пишите трассы в OTel-совместимом формате, заведите 20–50 задач из реальных отказов, считайте pass^k, грейдите состояние системы, а не финальную реплику [17][18].
- Дешёвый судья с отладкой может быть лучше дорогого: измерьте kappa с людьми для двух-трёх кандидатов, прежде чем платить за фронтирную модель [14].
- Любой публичный бенчмарк временный: планируйте ротацию внутреннего набора, как HLE завёл HLE-Rolling [9].

## Проверка пометок в конспекте

- «**Дополнение — на практике:** В коде судья обычно выглядит так…» (раздел 6). Две неточности. (1) Structured outputs у Anthropic появились не «позже», а 14 ноября 2025 — за неделю до лекции (бета, заголовок `structured-outputs-2025-11-13`); 29 января 2026 вышли из беты, параметр переехал в `output_config.format` [27][28]. (2) Приём «tool use с принудительным `tool_choice`» на новейших моделях не работает: с 1 сентября 2026 Claude Fable 5.1 и Mythos 5.1 возвращают 400 на `tool_choice: any/tool`; рекомендованы strict tool use или structured outputs [28].
- «**Дополнение — что изменилось с тех пор:** Точное число задач в MMLU — 57…» (раздел 13). Верно, но отстало на год: GPQA Diamond у фронтира ~94–95% и моделей уже не различает [19]; стоит добавить HLE и HLE-Diamond [9][10].
- «**Дополнение — уточнение:** Критерий успеха в SWE-bench формализован…» (раздел 15). «Лаборатории сейчас отчитываются по SWE-bench Verified» — устарело: OpenAI прекратила в феврале 2026, соавтор считает бенчмарк насыщенным при 93,9% [1][3]; описание FAIL_TO_PASS / PASS_TO_PASS верно, но, по данным OpenAI, часть тестов отвергает корректные решения [2].
- «**Дополнение — уточнение:** Оценка pass^k в статье о τ-bench…» (раздел 17). Формула и описание τ²-bench верны; добавить τ³ и τ-bench 2.0 [16].
- Остальные 💡-блоки (kappa, пример BLEU, RLAIF, воспроизводимость при temperature 0, FActScore/SAFE, трассы агентов, перемешивание A/B) противоречий с источниками не содержат. Заметных открытых judge-моделей 2026 года найти не удалось (не удалось подтвердить источником).

## Источники

1. Why we no longer evaluate SWE-bench Verified — OpenAI — 23 февраля 2026 — https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ (страница отдаёт 403; дата и тезисы — по поисковому сниппету и [2])
2. The End of SWE-Bench Verified — Mia Glaese, Olivia Watkins (OpenAI) — Latent Space — 23 февраля 2026 — https://www.latent.space/p/swe-bench-dead
3. «I'm a co-creator of SWE-bench…» — Ofir Press — Hacker News — ≈май 2026 — https://news.ycombinator.com/item?id=47912620
4. The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason — Liang, Garg, Zilouchian Moghaddam — arXiv — 14 июня 2025 (v4 1 декабря 2025) — https://arxiv.org/abs/2506.12286
5. The Leaderboard Illusion — Singh et al. — arXiv — 29 апреля 2025 — https://arxiv.org/abs/2504.20879
6. Arena (AI platform) — Wikipedia — просмотрено 7 ноября 2026 — https://en.wikipedia.org/wiki/Arena_(AI_platform)
7. SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks? — Deng et al. (Scale AI) — arXiv — 21 сентября 2025 — https://arxiv.org/abs/2509.16941
8. AIME 2026 (MathArena) leaderboard — respan.ai, по прогону matharena.ai от 31 октября 2026 — https://www.respan.ai/models/benchmarks/aime-2026-matharena
9. Humanity's Last Exam — lastexam.ai (CAIS, Scale AI) — просмотрено 7 ноября 2026 — https://lastexam.ai/
10. HLE leaderboard — Scale AI Labs — обновлено 17 сентября 2026 — https://labs.scale.com/leaderboard/humanitys_last_exam ; Introducing HLE-Diamond — CAIS, Scale AI — 22 сентября 2026 — https://lastexam.ai/blog/hle-diamond
11. Announcing ARC-AGI-3 — ARC Prize (Greg Kamradt) — 25 марта 2026 — https://arcprize.org/blog/arc-agi-3-launch
12. OpenAI's GPT-6 Astra on ARC-AGI-3 — ARC Prize — 3 сентября 2026 — https://arcprize.org/blog/astra ; ARC Prize Leaderboard — https://arcprize.org/leaderboard
13. GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks — Patwardhan et al. (OpenAI) — arXiv — 5 октября 2025 — https://arxiv.org/abs/2510.04374
14. Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines — S. K. Soumik — arXiv / TMLR — 25 апреля 2026 — https://arxiv.org/abs/2604.23178
15. Self-Preference Bias in Rubric-Based Evaluation of Large Language Models — Pombal, Rei, Martins — arXiv — 8 апреля 2026 — https://arxiv.org/abs/2604.06996
16. sierra-research/tau2-bench — README и Releases — GitHub — τ³ 1.0.0 18 марта 2026, 2.0.0 19 октября 2026 — https://github.com/sierra-research/tau2-bench/releases
17. Demystifying evals for AI agents — Anthropic Engineering — 9 января 2026 — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
18. Semantic conventions for GenAI agent spans — OpenTelemetry, semantic-conventions-genai — просмотрено 7 ноября 2026 — https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md
19. Claude Mythos Preview System Card — Anthropic — 7 апреля 2026 (Markdown-копия) — https://gist.github.com/Michaelliv/0677ab6a64312211e38b7a99a03c5f61 ; сводная таблица — R&D World — 8 апреля 2026 — https://www.rdworldonline.com/claude-mythos-leads-17-of-18-benchmarks-anthropic-measured-muse-spark-put-meta-back-in-the-frontier-club-and-openais-spud-model-is-reportedly-near-launch/
20. Terminal-Bench benchmarks (2.0 — 7 ноября 2025, 2.1 — 6 мая 2026, 3.0 — 30 июля 2026) — tbench.ai — https://www.tbench.ai/benchmarks
21. Mitigating Rubric Interference in LLM Judges via On-Policy Self-Distillation — Yu et al. — arXiv — 5 августа 2026 — https://arxiv.org/abs/2608.14684
22. Judging LLM-as-a-Judge: Concerning Rubric Artifacts in LLM-based Automated Text Generation Evaluation — Bagaria et al. — arXiv, EMNLP 2026 — 31 августа 2026 — https://arxiv.org/abs/2609.02942
23. Epoch Capabilities Index — Epoch AI — октябрь 2025 — https://epoch.ai/eci
24. Time Horizon 1.1 — METR — 29 января 2026 — https://metr.org/blog/2026-01-29-time-horizon-1-1/
25. Time horizons — METR — обновлено 8 сентября 2026 — https://metr.org/time-horizons/
26. Bloom: an open source tool for automated behavioral evaluations — Anthropic Alignment Science — 19 декабря 2025 — https://alignment.anthropic.com/2025/bloom-auto-evals/
27. Structured outputs — Claude Platform Docs — просмотрено 7 ноября 2026 — https://platform.claude.com/docs/en/build-with-claude/structured-outputs
28. API release notes — Claude Platform Docs — записи от 14 ноября 2025, 29 января 2026 и 1 сентября 2026 — https://platform.claude.com/docs/en/release-notes/api
