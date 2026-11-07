#!/usr/bin/env python3
"""Build updates/index.md from the per-lecture update files and link each digest to its update.

  python3 -I tools/build_updates_index.py

* updates/index.md: intro + for every lecture the first bullets of its «## Коротко» section + links.
* lectures/NN-slug.md: a line «**Актуализация (ноябрь 2026):** …» is inserted right after the
  navigation line (once); tools/build_docs.py turns that line into a banner on the site.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from build_docs import SLUGS, RU_TITLES  # noqa: E402

FULL_TITLES = {
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
DATE_LINE = "ноябрь 2026"


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(1).strip() if m else ""


def bullets(text, n):
    out = []
    for l in text.splitlines():
        if re.match(r"^\s*[-*•]\s+", l):
            out.append(re.sub(r"^\s*[-*•]\s+", "", l).strip())
    return out[:n]


def main():
    upd = os.path.join(ROOT, "updates")
    present = [s for s in SLUGS if os.path.exists(os.path.join(upd, f"{s}.md"))]
    if not present:
        print("no updates/*.md yet"); return
    L = []
    L.append("# Актуализация: что изменилось к ноябрю 2026")
    L.append("")
    L.append("Лекции курса прочитаны с 26 сентября по 5 декабря 2025 года. Поле меняется быстро, поэтому по каждой лекции отдельно сверено с открытыми источниками (статьи, model cards, документация, блоги лабораторий), что из сказанного осталось верным, что устарело или сдвинулось, что появилось нового и что это меняет на практике. Дата сверки: 7 ноября 2026.")
    L.append("")
    L.append("Как читать: сначала конспект лекции, затем её актуализацию. В каждой актуализации есть раздел «Проверка пометок в конспекте»: там перечислены пометки 💡, которые пришлось уточнить по источникам. Всё, что не удалось подтвердить источником, помечено прямо в тексте.")
    L.append("")
    L.append("| № | Лекция | Актуализация | Конспект |")
    L.append("|---|---|---|---|")
    for s in present:
        n = SLUGS.index(s) + 1
        L.append(f"| {n} | {FULL_TITLES[s]} | [что изменилось]({s}.md) | [конспект](../lectures/{s}.md) |")
    L.append("")
    L.append("## Главное по лекциям")
    L.append("")
    for s in present:
        n = SLUGS.index(s) + 1
        text = open(os.path.join(upd, f"{s}.md"), encoding="utf-8").read()
        L.append(f"### [Лекция {n}. {FULL_TITLES[s]}]({s}.md)")
        L.append("")
        bl = bullets(section(text, "Коротко"), 3)
        if bl:
            for b in bl:
                L.append(f"- {b}")
        else:
            L.append("- (раздел «Коротко» не найден)")
        L.append("")
    L.append("## Метод и ограничения")
    L.append("")
    L.append("- Каждую актуализацию готовил отдельный проход с веб-поиском по теме лекции (8–15 запросов), с приоритетом первоисточников: arXiv, официальные блоги и model cards, документация. Утверждения о 2026 годе опираются только на найденные источники, а не на память модели.")
    L.append("- Это срез на дату сверки, а не непрерывно обновляемый документ: для повторной проверки удобно начинать с раздела «Источники» каждой страницы.")
    L.append("- Конспекты лекций при этом не переписаны: они по-прежнему пересказывают то, что говорили лекторы осенью 2025, а актуализация лежит рядом.")
    with open(os.path.join(upd, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"updates/index.md written for {len(present)} lectures")

    # --- link line in each digest ---
    for s in present:
        p = os.path.join(ROOT, "lectures", f"{s}.md")
        t = open(p, encoding="utf-8").read()
        if "**Актуализация (ноябрь 2026):**" in t:
            continue
        lines = t.splitlines()
        for k, l in enumerate(lines):
            if "](../README.md)" in l:
                lines[k:k + 1] = [l, "", f"**Актуализация (ноябрь 2026):** что в этой теме изменилось с момента лекции — [читать](../updates/{s}.md)."]
                break
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("linked", s)


if __name__ == "__main__":
    main()
