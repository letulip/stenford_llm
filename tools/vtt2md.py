#!/usr/bin/env python3
"""Convert yt-dlp VTT captions + info.json into readable markdown transcripts
with chapter headings and paragraph timestamps. Usage:
  python3 -I vtt2md.py <raw_dir> <meta_dir> <project_dir>
"""
import json, os, re, sys, shutil

RAW, META, PROJ = sys.argv[1], sys.argv[2], sys.argv[3]

LECTURES = [
    ("Ub3GoFaUcds", "01-transformer"),
    ("yT84Y5zCnaA", "02-transformer-models-tricks"),
    ("Q5baLehv5So", "03-llms-moe-decoding-prompting"),
    ("VlA_jt_3Qc4", "04-llm-training"),
    ("PmW_TMQ3l0I", "05-llm-tuning-rlhf-dpo"),
    ("k5Fh-UgTuCo", "06-llm-reasoning"),
    ("h-7S6HNq0Vg", "07-agentic-llms-rag-tools"),
    ("8fNP4N46RRo", "08-llm-evaluation"),
    ("Q86qzJ1K1Ss", "09-recap-current-trends"),
]

def parse_ts(s):
    h, m, rest = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)

def fmt(sec):
    sec = int(sec)
    if sec >= 3600:
        return f"{sec//3600}:{(sec%3600)//60:02d}:{sec%60:02d}"
    return f"{sec//60:02d}:{sec%60:02d}"

def parse_vtt(path):
    cues = []
    with open(path, encoding="utf-8") as f:
        block = []
        for line in f.read().splitlines() + [""]:
            if line.strip() == "":
                if block:
                    # find timing line
                    ti = next((i for i, l in enumerate(block) if "-->" in l), None)
                    if ti is not None:
                        a, b = [x.strip().split(" ")[0] for x in block[ti].split("-->")]
                        text = " ".join(l.strip() for l in block[ti+1:] if l.strip())
                        text = re.sub(r"<[^>]+>", "", text)
                        text = re.sub(r"\s+", " ", text).strip()
                        if text:
                            cues.append((parse_ts(a), parse_ts(b), text))
                    block = []
            else:
                block.append(line)
    return cues

def build_paragraphs(cues, chapters):
    """Group cues into paragraphs; break on chapter boundaries, ~50s + sentence end, or 100s hard."""
    out = []  # list of (chapter_index or None, start, text)
    ch_starts = [c["start_time"] for c in chapters]
    ci = -1
    para_start, para_text, para_dur = None, [], 0.0
    def flush():
        nonlocal para_start, para_text
        if para_text:
            out.append(("p", para_start, " ".join(para_text)))
        para_start, para_text = None, []
    for (a, b, t) in cues:
        # chapter change?
        while ci + 1 < len(ch_starts) and a >= ch_starts[ci + 1] - 0.5:
            flush()
            ci += 1
            out.append(("h", ch_starts[ci], chapters[ci]["title"]))
        if para_start is None:
            para_start = a
        para_text.append(t)
        dur = b - para_start
        ends_sentence = t.endswith((".", "?", "!"))
        if (dur >= 50 and ends_sentence) or dur >= 100:
            flush()
    flush()
    return out

def main():
    os.makedirs(os.path.join(PROJ, "transcripts"), exist_ok=True)
    os.makedirs(os.path.join(PROJ, "raw"), exist_ok=True)
    index = []
    for n, (vid, slug) in enumerate(LECTURES, 1):
        meta = json.load(open(os.path.join(META, vid + ".json")))
        vtt = os.path.join(RAW, f"{vid}.en-US.vtt")
        cues = parse_vtt(vtt)
        chapters = meta.get("chapters") or []
        title = meta["title"]
        short = title.split("Lecture")[-1].strip()  # e.g. "1 - Transformer"
        short = re.sub(r"^\d+\s*-\s*", "", short)
        short = short.replace("Tranformers", "Transformers")  # typo in the YouTube title of lecture 3
        dur = meta["duration"]
        # lecture date from description (first line like "September 26, 2025")
        desc = meta.get("description") or ""
        m = re.search(r"\n((January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})", desc)
        lec_date = m.group(1) if m else ""
        covers = re.findall(r"•\s*(.+)", desc)
        url = f"https://youtu.be/{vid}"
        # --- transcript markdown ---
        lines = []
        lines.append(f"# Лекция {n}. {short}")
        lines.append("")
        lines.append(f"**Курс:** Stanford CME295 Transformers & LLMs, Autumn 2025  ")
        lines.append(f"**Видео:** {url}  ")
        if lec_date:
            lines.append(f"**Дата лекции:** {lec_date}  ")
        lines.append(f"**Длительность:** {dur//60} мин  ")
        lines.append(f"**Конспект:** [../lectures/{slug}.md](../lectures/{slug}.md)")
        lines.append("")
        lines.append("Полный текст английских субтитров (ручные субтитры Stanford Online), разбитый по главам видео. Таймкод в начале абзаца кликабелен и открывает это место на YouTube.")
        lines.append("")
        lines.append("## Оглавление")
        lines.append("")
        for i, c in enumerate(chapters, 1):
            anchor = re.sub(r"[^a-z0-9\- ]", "", c["title"].lower()).strip().replace(" ", "-")
            lines.append(f"{i}. [{fmt(c['start_time'])} — {c['title']}](#{i}-{anchor})")
        lines.append("")
        paras = build_paragraphs(cues, chapters)
        hi = 0
        for kind, start, text in paras:
            if kind == "h":
                hi += 1
                lines.append("")
                lines.append(f"## {hi}. {text}")
                lines.append("")
                lines.append(f"*Начало: [{fmt(start)}]({url}?t={int(start)})*")
                lines.append("")
            else:
                lines.append(f"[**{fmt(start)}**]({url}?t={int(start)}) {text}")
                lines.append("")
        tpath = os.path.join(PROJ, "transcripts", f"{slug}.md")
        with open(tpath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines).rstrip() + "\n")
        # --- raw copies ---
        shutil.copy(vtt, os.path.join(PROJ, "raw", f"{slug}.en-US.vtt"))
        slim = {k: meta.get(k) for k in ["id", "title", "webpage_url", "uploader", "upload_date", "duration", "description", "chapters", "view_count", "like_count"]}
        with open(os.path.join(PROJ, "raw", f"{slug}.info.json"), "w", encoding="utf-8") as f:
            json.dump(slim, f, ensure_ascii=False, indent=2)
        words = sum(len(t.split()) for _, _, t in cues)
        index.append({"n": n, "id": vid, "slug": slug, "title": title, "short": short, "url": url,
                      "date": lec_date, "duration_min": dur // 60, "chapters": chapters, "covers": covers, "words": words})
        print(f"L{n} {slug}: {len(cues)} cues, {words} words, {len(chapters)} chapters -> {tpath}")
    with open(os.path.join(PROJ, "raw", "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

main()
