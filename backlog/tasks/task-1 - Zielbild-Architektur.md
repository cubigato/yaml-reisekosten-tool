---
id: TASK-1
title: Zielbild / Architektur
status: Done
assignee: []
created_date: '2026-06-07 15:11'
updated_date: '2026-06-07 20:26'
labels: []
dependencies: []
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Zielbild der Software:
liest eine yaml datei (beispiel in examples/example.yml) und derstell daraus saubere Reisekostenabrechnungen im PDF format.
Orientierung an der lexware vorlage ebenfalls unter examples.

Tech stack
python
uv + .venv
pyproject.toml
ruff mit vernünftigen regeln
wo geht type hints
pytest

Einfaches klares CLI interface. Ohne weitere argumente "yaml-reisekosten-tool foo.yml" erzeugt direkt im current directory die PDFs mit sinnvollen dateinamen ohne weiteren clutter.

dokumentenerstellung: wir machen einen spike ob "typst" viable ist, sonst fallback auf latex.

Projektsprache ist Deutsch.
<!-- SECTION:DESCRIPTION:END -->
