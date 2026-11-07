#!/usr/bin/env python3
"""Generate the MkDocs source tree (docs/) and mkdocs.yml from the markdown sources.

  python3 -I tools/build_docs.py          # regenerates docs/ and mkdocs.yml
  .venv/bin/mkdocs build                  # -> site/
  .venv/bin/mkdocs serve                  # live preview

Sources stay GitHub-flavoured markdown; this script only adapts them for the site:
  * `> 💡 **Дополнение — тип:** …` blockquotes become Material admonitions,
  * `../README.md` links become `../index.md`,
  * README links into raw/ and tools/ are turned into plain text,
  * a banner linking to updates/<lecture>.md is inserted into each digest when it exists.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SRC = os.path.join(ROOT, "site_src")

RU_TITLES = {
    "01-transformer": "Трансформер",
    "02-transformer-models-tricks": "Модели на базе трансформера и приёмы",
    "03-llms-moe-decoding-prompting": "LLM: MoE, декодирование, промптинг",
    "04-llm-training": "Обучение LLM",
    "05-llm-tuning-rlhf-dpo": "Дообучение: RLHF, PPO, DPO",
    "06-llm-reasoning": "Reasoning-модели и GRPO",
    "07-agentic-llms-rag-tools": "Агенты: RAG, инструменты, MCP",
    "08-llm-evaluation": "Оценка LLM",
    "09-recap-current-trends": "Итоги и тренды: ViT, диффузионные LLM",
}
EN_TITLES = {
    "01-transformer": "Transformer",
    "02-transformer-models-tricks": "Transformer-Based Models & Tricks",
    "03-llms-moe-decoding-prompting": "Transformers & LLMs",
    "04-llm-training": "LLM Training",
    "05-llm-tuning-rlhf-dpo": "LLM Tuning",
    "06-llm-reasoning": "LLM Reasoning",
    "07-agentic-llms-rag-tools": "Agentic LLMs",
    "08-llm-evaluation": "LLM Evaluation",
    "09-recap-current-trends": "Recap & Current Trends",
}
SLUGS = list(RU_TITLES)

NOTE_RE = re.compile(r"^> 💡 \*\*Дополнение(?:\s*[—–-]\s*([^*]*?))?\s*:?\*\*:?\s*(.*)$")


def convert_notes(text: str) -> str:
    """Turn `> 💡 **Дополнение — тип:** …` blockquotes (with optional `> ` continuation lines)
    into `!!! tip` admonitions."""
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        m = NOTE_RE.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        kind = (m.group(1) or "").strip()
        body = [m.group(2)]
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            body.append(re.sub(r"^>\s?", "", lines[i])); i += 1
        title = f"💡 Дополнение — {kind}" if kind else "💡 Дополнение"
        out.append(f'!!! tip "{title}"')
        for b in body:
            out.append("    " + b if b.strip() else "")
        out.append("")
    return "\n".join(out)


def write(path: str, text: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text if text.endswith("\n") else text + "\n")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)

    # --- index.md from README.md ---
    readme = read(os.path.join(ROOT, "README.md"))
    readme = re.sub(r"\[`?([^\]`]+)`?\]\(((?:raw|tools)/?[^)]*)\)", r"`\2`", readme)  # de-link raw/ and tools/
    readme = readme.replace("](lectures/)", "](lectures/01-transformer.md)")
    readme = readme.replace("](transcripts/)", "](transcripts/01-transformer.md)")
    write(os.path.join(DOCS, "index.md"), readme)

    # --- lectures ---
    has_update = {}
    for slug in SLUGS:
        src = os.path.join(ROOT, "lectures", f"{slug}.md")
        if not os.path.exists(src):
            continue
        text = read(src).replace("](../README.md)", "](../index.md)")
        text = convert_notes(text)
        upd = os.path.join(ROOT, "updates", f"{slug}.md")
        has_update[slug] = os.path.exists(upd)
        if has_update[slug]:
            banner = ('!!! info "Актуализация к ноябрю 2026"\n'
                      f'    Лекция прочитана осенью 2025. Что в этой теме изменилось с тех пор: '
                      f'[читать актуализацию](../updates/{slug}.md).\n')
            lines = text.splitlines()
            # prefer replacing the source link line (inserted by build_updates_index.py) …
            idx = next((k for k, l in enumerate(lines) if l.startswith("**Актуализация (ноябрь 2026):**")), None)
            if idx is not None:
                lines[idx] = banner
            else:  # … otherwise insert after the navigation line
                for k, l in enumerate(lines):
                    if "](../index.md)" in l:
                        lines[k:k + 1] = [l, "", banner]
                        break
            text = "\n".join(lines)
        write(os.path.join(DOCS, "lectures", f"{slug}.md"), text)

    # --- transcripts ---
    for slug in SLUGS:
        src = os.path.join(ROOT, "transcripts", f"{slug}.md")
        if os.path.exists(src):
            write(os.path.join(DOCS, "transcripts", f"{slug}.md"), read(src))

    # --- updates ---
    upd_dir = os.path.join(ROOT, "updates")
    upd_slugs = [s for s in SLUGS if os.path.exists(os.path.join(upd_dir, f"{s}.md"))]
    if os.path.isdir(upd_dir):
        for name in sorted(os.listdir(upd_dir)):
            if name.endswith(".md"):
                write(os.path.join(DOCS, "updates", name), convert_notes(read(os.path.join(upd_dir, name))))

    # --- static assets ---
    if os.path.isdir(SRC):
        shutil.copytree(SRC, os.path.join(DOCS, "assets"))

    # --- mkdocs.yml ---
    def nav_items(folder, titles):
        return "".join(f'      - "{n}. {titles[s]}": {folder}/{s}.md\n' for n, s in enumerate(SLUGS, 1)
                       if os.path.exists(os.path.join(DOCS, folder, f"{s}.md")))

    nav = "nav:\n  - Главная: index.md\n  - Конспекты:\n" + nav_items("lectures", RU_TITLES)
    if upd_slugs:
        nav += "  - Актуализация 2026:\n"
        if os.path.exists(os.path.join(DOCS, "updates", "index.md")):
            nav += "      - updates/index.md\n"
        nav += "".join(f'      - "{SLUGS.index(s)+1}. {RU_TITLES[s]}": updates/{s}.md\n' for s in upd_slugs)
    nav += "  - Транскрипты (EN):\n" + nav_items("transcripts", EN_TITLES)

    cfg = f"""# Generated by tools/build_docs.py — edit the template there, not this file.
site_name: Stanford CME295 · Transformers & LLMs
site_description: Конспекты девяти лекций Stanford CME295 (осень 2025) на русском, английские транскрипты и актуализация к 2026 году
docs_dir: docs
site_dir: site
use_directory_urls: false
copyright: Конспекты собраны из открытых субтитров Stanford Online · лекторы Afshine Amidi и Shervine Amidi

theme:
  name: material
  language: ru
  font: false
  icon:
    logo: material/school-outline
    repo: fontawesome/brands/github
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: deep purple
      accent: deep orange
      toggle:
        icon: material/weather-night
        name: Тёмная тема
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: deep purple
      accent: deep orange
      toggle:
        icon: material/weather-sunny
        name: Светлая тема
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - navigation.footer
    - navigation.tracking
    - toc.follow
    - search.suggest
    - search.highlight
    - content.code.copy

{nav}
markdown_extensions:
  - toc:
      permalink: "¶"
      toc_depth: 3
      slugify: !!python/object/apply:pymdownx.slugs.slugify
        kwds:
          case: lower
  - tables
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.betterem
  - pymdownx.arithmatex:
      generic: true

extra_css:
  - assets/katex/katex.min.css
  - assets/css/extra.css

extra_javascript:
  - assets/katex/katex.min.js
  - assets/katex/contrib/auto-render.min.js
  - assets/js/math.js
  - assets/js/links.js

plugins:
  - search:
      lang:
        - ru
        - en
"""
    write(os.path.join(ROOT, "mkdocs.yml"), cfg)
    n_l = len([s for s in SLUGS if os.path.exists(os.path.join(DOCS, "lectures", f"{s}.md"))])
    print(f"docs/: {n_l} lectures, {len(upd_slugs)} updates, transcripts, assets -> mkdocs.yml written")


if __name__ == "__main__":
    main()
