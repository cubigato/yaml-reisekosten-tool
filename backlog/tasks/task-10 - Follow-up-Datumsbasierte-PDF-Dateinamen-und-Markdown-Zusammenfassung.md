---
id: TASK-10
title: 'Follow-up: Datumsbasierte PDF-Dateinamen und Markdown-Zusammenfassung'
status: Done
assignee:
  - Codex
created_date: '2026-06-08 12:45'
updated_date: '2026-06-08 12:48'
labels:
  - cli
  - output
  - markdown
dependencies: []
documentation:
  - README.md
  - ARCHITECTURE.md
modified_files:
  - README.md
  - ARCHITECTURE.md
  - src/yaml_reisekosten_tool/cli.py
  - tests/test_cli_smoke.py
priority: medium
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Nach der Umstellung auf ein PDF pro Fahrt sollen die Ausgabedateien besser nutzbar werden. PDF-Dateinamen sollen das konkrete Fahrtdatum voranstellen und nur bei mehreren Reisen am selben Tag nummerieren. Zusaetzlich soll die CLI eine Markdown-Zusammenfassung aller erzeugten Abrechnungen mit Gesamtbetrag fuer interne Zwecke schreiben. Die PDFs bleiben Lexware-formkonform; die Markdown-Datei darf informativ sein.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 PDF-Dateinamen einzelner Fahrten beginnen mit dem Fahrt-Datum im Format YYYY-MM-DD und benoetigen bei unterschiedlichen Fahrtagen keine laufenden Nummern.
- [x] #2 Wenn mehrere Abrechnungen dasselbe Fahrt-Datum und denselben Basisnamen haetten, werden nur diese Kollisionen mit einem stabilen Suffix eindeutig gemacht.
- [x] #3 Die CLI erzeugt neben den PDFs eine Markdown-Zusammenfassung aller gerenderten Abrechnungen mit Einzelbetragen und Gesamtbetrag.
- [x] #4 Die CLI gibt den Pfad der Markdown-Zusammenfassung nachvollziehbar auf stdout aus und beruecksichtigt Kollisionsschutz bzw. --force.
- [x] #5 README.md und ARCHITECTURE.md dokumentieren Dateinamen und Markdown-Zusammenfassung.
- [x] #6 Automatisierte Tests decken datumsbasierte Dateinamen, Same-Day-Suffixe und Markdown-Inhalt mit synthetischen Daten ab.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Dateinamenlogik in `cli.py` aendern: PDF-Basis bleibt titel-/input-basiert, aber fuer Einzelfahrt-Abrechnungen wird `YYYY-MM-DD_` vorangestellt. Laufende Suffixe werden nur innerhalb gleicher Zielpfade vergeben, also typischerweise bei mehreren Fahrten am selben Tag.
2. Markdown-Zusammenfassung in `cli.py` ergaenzen: fester Dateiname auf Basis von Abrechnungszeitraum/Titel, Endung `.md`, Tabelle mit PDF-Datei, Datum, Zeit, Ziel/Anlass, Einzelbetraegen und Gesamtsumme.
3. Kollisionsschutz erweitern: PDFs und Markdown-Zusammenfassung werden vor dem Rendern geprueft; `--force` erlaubt Ueberschreiben.
4. stdout so erweitern, dass alle PDF-Pfade und danach der Markdown-Pfad ausgegeben werden.
5. Tests in `tests/test_cli_smoke.py` fuer datumsbasierte Namen, Same-Day-Suffixe, Markdown-Inhalt und Kollisionsschutz anpassen/ergaenzen.
6. README.md und ARCHITECTURE.md auf den neuen Ausgabe-Kontrakt aktualisieren; danach Tests, Ruff und echten Renderlauf ausfuehren.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Umsetzung abgeschlossen: PDF-Dateien erhalten bei Einzelfahrt-Abrechnungen das Fahrtdatum als Prefix, Duplikate am selben Tag werden mit `-02` usw. dedupliziert. Die CLI schreibt eine Markdown-Zusammenfassung mit Tabelle und Gesamtbetrag und gibt deren Pfad nach den PDF-Pfaden auf stdout aus. Kollisionsschutz gilt fuer PDFs und Markdown-Datei; `--force` ueberschreibt beide Arten von Zieldateien. Verifikation: `.venv/bin/python -m pytest` (49 passed), `ruff check .`, `ruff format --check .`, `git diff --check`, echter Renderlauf mit `examples/example.yml --output-dir /tmp --force`; die erzeugte Markdown-Datei enthaelt 5 Abrechnungen und Gesamtbetrag 248,20 EUR.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
PDF-Dateinamen sind jetzt fahrtdatumsbasiert, z.B. `2026-01-08_2026-01_reisekostenabrechnung.pdf`. Nur gleiche Fahrtage mit identischem Basisnamen erhalten stabile Suffixe wie `-02`.

Die CLI erzeugt zusaetzlich eine interne Markdown-Zusammenfassung neben den PDFs. Sie enthaelt Anzahl der Abrechnungen, Gesamtbetrag und eine Tabelle mit PDF-Datei, Datum, Zeit, Ziel, Anlass, Fahrtkosten, Verpflegung, Auslagen und Gesamt je Fahrt. Der Summary-Pfad wird nach den PDF-Pfaden auf stdout ausgegeben. Kollisionsschutz und `--force` gelten fuer PDFs und Markdown-Zusammenfassung.

README.md und ARCHITECTURE.md dokumentieren den neuen Ausgabe-Kontrakt. Tests decken datumsbasierte Namen, Same-Day-Suffixe, Markdown-Inhalt und Summary-Kollisionen mit synthetischen Daten ab. Verifikation: `.venv/bin/python -m pytest` (49 passed), `ruff check .`, `ruff format --check .`, `git diff --check`, echter Typst-Renderlauf mit `examples/example.yml` nach `/tmp`.
<!-- SECTION:FINAL_SUMMARY:END -->
