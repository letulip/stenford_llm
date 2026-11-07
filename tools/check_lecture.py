#!/usr/bin/env python3
"""Sanity checks for a lecture digest: TOC anchors, relative links, 💡 blocks, word count.
Usage: python3 -I check_lecture.py <file.md> [...]"""
import re, sys, os

def slug(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")

for path in sys.argv[1:]:
    txt = open(path, encoding="utf-8").read()
    lines = txt.splitlines()
    heads = [re.sub(r"^#+\s*", "", l) for l in lines if re.match(r"^#{1,6}\s", l)]
    slugs = {}
    for h in heads:
        s = slug(h); 
        # GitHub de-duplicates by appending -1, -2
        if s in slugs:
            slugs[s] += 1; s = f"{s}-{slugs[s]}"
        else:
            slugs[s] = 0
        slugs.setdefault(s, 0)
    anchors = re.findall(r"\]\(#([^)]+)\)", txt)
    bad_anchors = [a for a in anchors if a not in slugs]
    rel = re.findall(r"\]\((?!https?://|#)([^)]+)\)", txt)
    base = os.path.dirname(path)
    bad_rel = [r for r in rel if not os.path.exists(os.path.join(base, r.split("#")[0]))]
    notes = len(re.findall(r"^> 💡", txt, flags=re.M))
    # blockquote not surrounded by blank lines
    bq_issues = 0
    for i, l in enumerate(lines):
        if l.startswith("> 💡"):
            if i > 0 and lines[i-1].strip() != "" and not lines[i-1].startswith(">"): bq_issues += 1
            if i + 1 < len(lines) and lines[i+1].strip() != "" and not lines[i+1].startswith(">"): bq_issues += 1
    words = len(re.findall(r"[А-Яа-яЁёA-Za-z0-9]+", txt))
    h2 = [h for h in heads if re.match(r"^\d+\.\s", h)]
    sections_with_no_yt = sum(1 for h in h2)  # placeholder
    yt_links = len(re.findall(r"youtu\.be/[\w-]+\?t=\d+", txt))
    print(f"{os.path.basename(path)}: words={words} h2_numbered={len(h2)} toc_anchors={len(anchors)} bad_anchors={bad_anchors[:5]} bad_rel_links={bad_rel[:5]} notes={notes} bq_spacing_issues={bq_issues} yt_links={yt_links} has_dopolnit={'## Чем можно дополнить' in txt}")
