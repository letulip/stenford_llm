#!/usr/bin/env python3
"""Build README.md for the course folder from raw/index.json.
Usage: python3 -I build_readme.py <project_dir> [summaries.json]
summaries.json: {"01-transformer": "…", …} — optional per-lecture summary paragraphs."""
import json, os, sys, re

PROJ = sys.argv[1]
SUMS = json.load(open(sys.argv[2])) if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else {}
index = json.load(open(os.path.join(PROJ, "raw", "index.json")))

RU_TITLES = {
    "01-transformer": "Трансформер",
    "02-transformer-models-tricks": "Модели на базе трансформера и инженерные приёмы",
    "03-llms-moe-decoding-prompting": "Большие языковые модели: MoE, декодирование, промптинг",
    "04-llm-training": "Обучение LLM: предобучение, оптимизации, SFT и LoRA",
    "05-llm-tuning-rlhf-dpo": "Дообучение LLM на предпочтениях: RLHF, PPO, DPO",
    "06-llm-reasoning": "Рассуждающие модели: RL для reasoning, GRPO, DeepSeek R1",
    "07-agentic-llms-rag-tools": "Агентные LLM: RAG, вызов инструментов, агенты",
    "08-llm-evaluation": "Оценка LLM: метрики, LLM-as-a-judge, бенчмарки",
    "09-recap-current-trends": "Итоги курса и текущие тренды: ViT, диффузионные LLM",
}
MONTHS = {"January": "января", "February": "февраля", "March": "марта", "April": "апреля", "May": "мая", "June": "июня",
          "July": "июля", "August": "августа", "September": "сентября", "October": "октября", "November": "ноября", "December": "декабря"}

def ru_date(d):
    m = re.match(r"(\w+) (\d+), (\d+)", d or "")
    return f"{int(m.group(2))} {MONTHS[m.group(1)]} {m.group(3)}" if m else d

def fmt(sec):
    sec = int(sec)
    return f"{sec//3600}:{(sec%3600)//60:02d}:{sec%60:02d}" if sec >= 3600 else f"{sec//60:02d}:{sec%60:02d}"

L = []
L.append("# Stanford CME295 — Transformers & Large Language Models (осень 2025)")
L.append("")
L.append("Конспекты девяти лекций курса Stanford CME295 «Transformers & LLMs» на русском языке, собранные из официальных субтитров видео Stanford Online на YouTube. Курс читают **Afshine Amidi** и **Shervine Amidi** (братья-близнецы; работают над LLM в Netflix, до этого Google и Uber; adjunct lecturers в Stanford). Курс идёт от устройства трансформера через обучение и дообучение LLM к reasoning-моделям, агентам и оценке качества.")
L.append("")
L.append("- **Плейлист:** https://www.youtube.com/playlist?list=PLoROMvodv4rOCXd21gf0CF4xr35yINeOy")
L.append("- **Сайт курса и программа:** https://cme295.stanford.edu/syllabus/")
L.append("- **Канал:** Stanford Online")
L.append("- **Репозиторий:** https://github.com/letulip/stenford_llm")
L.append("- **Сайт (GitHub Pages):** https://letulip.github.io/stenford_llm/")
L.append("")
L.append("## Как пользоваться")
L.append("")
L.append("| Папка | Что внутри | Когда открывать |")
L.append("|---|---|---|")
L.append("| [`lectures/`](lectures/) | Конспекты на русском: по одному файлу на лекцию, разделы повторяют главы видео, у каждого раздела таймкод и ссылка на YouTube, в конце термины, выводы и вопросы из зала | Начинать отсюда |")
L.append("| [`transcripts/`](transcripts/) | Полный английский текст субтитров, разбитый по главам; каждый абзац начинается с кликабельного таймкода | Когда нужно прочитать, что именно сказал лектор |")
L.append("| [`raw/`](raw/) | Исходные VTT-субтитры и метаданные видео (json), включая [`raw/index.json`](raw/index.json) со списком глав | Если захочется переобработать |")
L.append("")
L.append("Все таймкоды в конспектах и транскриптах кликабельны и открывают нужный момент видео.")
L.append("")
L.append("### Пометки-дополнения в конспектах")
L.append("")
L.append("Внутри конспектов встречаются блоки вида")
L.append("")
L.append("> 💡 **Дополнение — пример:** …")
L.append("")
L.append("Это **не слова лекторов**, а добавления составителя конспекта: дополнительный пример, более сильная интуиция или аналогия, связь с другой лекцией курса, практическое следствие для разработчика, оговорка или уточнение. Всё, что вне таких блоков, пересказывает содержание лекции. В конце каждого конспекта есть раздел «Чем можно дополнить» со списком тем, которых лекция не касается, но которые стоит знать рядом с ней.")
L.append("")
L.append("## Лекции")
L.append("")
total_min = 0
for it in index:
    slug, n = it["slug"], it["n"]
    total_min += it["duration_min"]
    L.append(f"### [Лекция {n}. {RU_TITLES[slug]}](lectures/{slug}.md)")
    L.append("")
    L.append(f"*{it['short']}* · {ru_date(it['date'])} · {it['duration_min']} мин · [видео]({it['url']}) · [транскрипт](transcripts/{slug}.md)")
    L.append("")
    s = SUMS.get(slug)
    if s:
        L.append(s.strip())
        L.append("")
    chs = " · ".join(f"[{c['title']}]({it['url']}?t={int(c['start_time'])}) ({fmt(c['start_time'])})" for c in it["chapters"])
    L.append(f"**Главы:** {chs}")
    L.append("")
L.append("## Карта курса")
L.append("")
L.append("| № | Лекция | О чём (по программе курса) |")
L.append("|---|---|---|")
for it in index:
    slug, n = it["slug"], it["n"]
    L.append(f"| {n} | [{RU_TITLES[slug]}](lectures/{slug}.md) | {'; '.join(c.strip() for c in it['covers'])} |")
L.append("")
L.append(f"Итого {len(index)} лекций, {total_min} минут видео (≈{total_min/60:.1f} часа).")
L.append("")
upd_index = os.path.join(PROJ, "updates", "index.md")
if os.path.exists(upd_index):
    L.append("## Актуализация к ноябрю 2026")
    L.append("")
    L.append("Лекции прочитаны осенью 2025 года. В папке [`updates/`](updates/index.md) по каждой лекции сверено с источниками, что с тех пор осталось верным, что устарело и что появилось нового; у каждого конспекта есть ссылка на свою актуализацию.")
    L.append("")
L.append("## Сайт")
L.append("")
L.append("Те же материалы собраны в статический сайт с навигацией, поиском, тёмной темой и формулами (MkDocs + Material):")
L.append("")
L.append("```bash")
L.append("python3 -m venv .venv && .venv/bin/pip install mkdocs-material   # один раз")
L.append("python3 -I tools/build_docs.py                                    # md -> docs/ + mkdocs.yml")
L.append(".venv/bin/mkdocs serve                                            # http://127.0.0.1:8000")
L.append("```")
L.append("")
L.append("`.venv/bin/mkdocs build` кладёт готовый сайт в `site/`; его можно открыть и без сервера (`site/index.html`), не будет работать только поиск. Стили, скрипты и локальная копия KaTeX лежат в `site_src/`.")
L.append("")
L.append("Публикация: `.venv/bin/mkdocs gh-deploy` собирает сайт и отправляет его в ветку `gh-pages`, откуда его раздаёт GitHub Pages.")
L.append("")
L.append("## Как это собрано")
L.append("")
L.append("1. Метаданные и ручные английские субтитры (en-US) каждого видео выгружены через `yt-dlp`.")
L.append("2. VTT-субтитры склеены в абзацы (~1 минута речи) и разбиты по главам видео, таймкоды превращены в ссылки `youtu.be/<id>?t=<сек>` — это папка `transcripts/`.")
L.append("3. По каждому транскрипту написан конспект на русском по единому шаблону: краткое содержание, оглавление, раздел на каждую главу видео, ключевые термины, главные выводы, вопросы из зала — это папка `lectures/`.")
L.append("4. Вторым проходом в конспекты добавлены пометки `> 💡 Дополнение` (примеры, интуиция, связи, практика) и раздел «Чем можно дополнить»; они явно отделены от пересказа лекции.")
L.append("")
L.append("Дата сборки: 7 ноября 2026.")
with open(os.path.join(PROJ, "README.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("README written:", os.path.join(PROJ, "README.md"), len("\n".join(L)), "chars")
