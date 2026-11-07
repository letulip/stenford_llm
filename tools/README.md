# Скрипты сборки

Как пересобрать базу (или добавить новую лекцию: допиши её id и slug в список `LECTURES` в `vtt2md.py` и в `RU_TITLES` в `build_readme.py`):

```bash
# 1. метаданные и ручные субтитры en-US
mkdir -p /tmp/cme295/meta /tmp/cme295/raw
for id in Ub3GoFaUcds yT84Y5zCnaA Q5baLehv5So VlA_jt_3Qc4 PmW_TMQ3l0I k5Fh-UgTuCo h-7S6HNq0Vg 8fNP4N46RRo Q86qzJ1K1Ss; do
  yt-dlp -J --skip-download "https://youtu.be/$id" > /tmp/cme295/meta/$id.json
  (cd /tmp/cme295/raw && yt-dlp --skip-download --write-subs --sub-langs en-US --sub-format vtt -o "%(id)s.%(ext)s" "https://youtu.be/$id")
done

# 2. транскрипты по главам + raw/ + raw/index.json
python3 -I tools/vtt2md.py /tmp/cme295/raw /tmp/cme295/meta .

# 3. README (summaries.json — необязательный файл {"01-transformer": "абзац", ...})
python3 -I tools/build_readme.py . summaries.json
```

Конспекты в `lectures/` написаны вручную (с помощью Claude) по транскриптам и скриптами не генерируются.

Проверка конспектов (якоря оглавления, относительные ссылки, блоки `💡`, пустые строки вокруг цитат):

```bash
python3 -I tools/check_lecture.py lectures/*.md
```

Сайт (MkDocs + Material): `tools/build_docs.py` генерирует `docs/` и `mkdocs.yml` из README, `lectures/`, `transcripts/` и `updates/` (пометки `> 💡` превращаются в admonition-блоки), затем `.venv/bin/mkdocs build` или `mkdocs serve`. Подробнее в разделе «Сайт» главного README.
