---
id: TASK-11
title: 'Follow-up: PDF-Dateinamen auf Fahrtdatum und Titel kuerzen'
status: Done
assignee:
  - Codex
created_date: '2026-06-08 12:56'
updated_date: '2026-06-08 12:57'
labels:
  - cli
  - output
dependencies: []
documentation:
  - README.md
  - ARCHITECTURE.md
modified_files:
  - README.md
  - ARCHITECTURE.md
  - src/yaml_reisekosten_tool/cli.py
  - tests/test_cli_smoke.py
priority: low
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die datumsbasierten PDF-Dateinamen enthalten aktuell Fahrtdatum und Abrechnungszeitraum, z.B. `2026-01-08_2026-01_reisekostenabrechnung.pdf`. Das ist zu sperrig. Fuer PDF-Dateien soll das konkrete Fahrtdatum als Prefix reichen; bei mehrtaegigen Reisen waere der Starttag massgeblich. Die Markdown-Zusammenfassung kann weiterhin den Abrechnungszeitraum im Namen tragen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 PDF-Dateinamen verwenden `YYYY-MM-DD_<titel-oder-input>.pdf` ohne zusaetzlichen Abrechnungszeitraum.
- [x] #2 Bei mehrtaegigen bzw. zusammengefassten Render-Abrechnungen wird der erste Reisetag als Dateiprefix verwendet.
- [x] #3 Same-Day-Kollisionen bleiben mit stabilem Suffix wie `-02` eindeutig.
- [x] #4 Markdown-Zusammenfassung behaelt einen nachvollziehbaren Zeitraum-/Titel-Dateinamen.
- [x] #5 README.md und ARCHITECTURE.md dokumentieren das vereinfachte PDF-Namensschema.
- [x] #6 Automatisierte Tests decken das vereinfachte Namensschema ab.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. PDF-Dateinamenbasis in `cli.py` von Zeitraum+Titel auf Titel bzw. Input-Stem umstellen; das Fahrtdatum bleibt als Prefix. Die Summary-Funktion behaelt weiterhin Zeitraum+Titel.
2. Datums-Prefix robuster machen: Bei einer Render-Abrechnung mit mehreren Fahrten wird der frueheste Fahrtag als Starttag verwendet.
3. Tests in `tests/test_cli_smoke.py` auf `YYYY-MM-DD_<titel>.pdf` aktualisieren und einen Mehrfahrten-Starttag-Fall fuer `build_output_paths` ergaenzen.
4. README.md und ARCHITECTURE.md entsprechend kuerzen.
5. Tests, Ruff und echten Renderlauf ausfuehren; Task abschliessen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Umgesetzt: PDF-Dateien nutzen nun nur noch den Start-/Fahrttag plus Titel/Input-Stem, z.B. `2026-01-08_reisekostenabrechnung.pdf`. Die Markdown-Zusammenfassung behaelt den Zeitraum im Dateinamen. Same-Day-Deduplizierung bleibt erhalten. Verifikation: `.venv/bin/python -m pytest` (50 passed), `ruff check .`, `ruff format --check .`, `git diff --check`, echter Renderlauf mit `examples/example.yml --output-dir /tmp --force` erzeugte PDF-Pfade ohne doppeltes Datum.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
PDF-Dateinamen wurden von `YYYY-MM-DD_YYYY-MM_<titel>.pdf` auf `YYYY-MM-DD_<titel>.pdf` gekuerzt. Fuer gruppierte bzw. potenziell mehrtaegige Render-Abrechnungen wird der frueheste Fahrtag als Starttag-Prefix verwendet. Same-Day-Kollisionen behalten stabile Suffixe wie `-02`.

Die Markdown-Zusammenfassung behaelt weiterhin den Zeitraum-/Titel-Namen, z.B. `2026-01_reisekostenabrechnung_zusammenfassung.md`, weil sie mehrere Abrechnungen zusammenfasst. README.md und ARCHITECTURE.md dokumentieren das vereinfachte PDF-Namensschema.

Verifikation: `.venv/bin/python -m pytest` (50 passed), `ruff check .`, `ruff format --check .`, `git diff --check`, echter Typst-Renderlauf mit `examples/example.yml` nach `/tmp`.
<!-- SECTION:FINAL_SUMMARY:END -->
