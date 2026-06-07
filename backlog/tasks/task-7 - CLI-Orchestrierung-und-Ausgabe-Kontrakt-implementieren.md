---
id: TASK-7
title: CLI-Orchestrierung und Ausgabe-Kontrakt implementieren
status: Done
assignee:
  - Codex
created_date: '2026-06-07 19:11'
updated_date: '2026-06-07 20:38'
labels:
  - implementation
  - cli
dependencies:
  - TASK-6
documentation:
  - README.md
  - ARCHITECTURE.md
  - examples/example.yml
modified_files:
  - src/yaml_reisekosten_tool/cli.py
  - tests/test_cli_smoke.py
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Verdrahtet die Pipeline zum ersten nutzbaren Kommando `yaml-reisekosten-tool foo.yml`. Die CLI liest genau eine YAML-Datei, durchlaeuft Laden, Validierung, Normalisierung, Berechnung und Rendering und schreibt PDFs gemaess dem in `ARCHITECTURE.md` dokumentierten Ausgabe-Kontrakt. Fehlermeldungen sind kurz, deutsch und gehen auf stderr; erwartbare Fehler enden ohne rohen Traceback.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Der Standardaufruf `yaml-reisekosten-tool foo.yml` erzeugt fuer eine gueltige Eingabe PDF-Dateien im aktuellen Arbeitsverzeichnis.
- [x] #2 `--output-dir DIR` schreibt in ein existierendes beschreibbares Zielverzeichnis; ungueltige Zielverzeichnisse werden kontrolliert abgelehnt.
- [x] #3 `--force` erlaubt Ueberschreiben vorhandener Ziel-PDFs; ohne `--force` bricht eine Namenskollision vor dem Veraendern vorhandener PDFs ab.
- [x] #4 PDF-Dateinamen folgen dem dokumentierten Slug- und Suffix-Kontrakt fuer eine oder mehrere Abrechnungen.
- [x] #5 Fehlende Eingabedatei, YAML-/Schema-/Fachfehler, Render-Fehler und Ausgabekollisionen erzeugen nutzbare stderr-Meldungen und Exit-Code ungleich `0`.
- [x] #6 CLI-Tests pruefen Erfolgsfall, optionale Argumente, Dateinamenbildung, Kollisionsschutz und mindestens drei Fehlerklassen.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. `src/yaml_reisekosten_tool/cli.py` vom Platzhalter zur Orchestrierung umbauen: Argumente parsen, genau eine Eingabedatei erwarten, `--output-dir` als existierendes beschreibbares Verzeichnis pruefen, YAML laden, normalisieren, berechnen und per `render_pdf` ausgeben.
2. Dateinamenlogik in der CLI kapseln: Slug aus Abrechnungszeitraum und Titel bilden, ASCII-normalisieren, Sonderzeichen entfernen, Leerraeume zu Bindestrichen machen, bei leerem Titel auf Eingabebasisnamen fallen und fuer kuenftig mehrere Abrechnungen stabile `-01`/`-02`-Suffixe vorsehen.
3. Kollisionsschutz vor dem Rendering pruefen: ohne `--force` bei vorhandenen Ziel-PDFs kontrolliert abbrechen, mit `--force` Rendern erlauben. Keine stillen Ausweichnamen erzeugen.
4. Erwartbare Fehler kontrolliert auf deutsch nach stderr melden und mit Exit-Code ungleich 0 beenden: fehlende/unlesbare Eingabe, YAML-Ladefehler, Validierungsfehler, fachliche Berechnungsfehler inkl. fehlender Pauschalen, Renderfehler und Ausgabekollisionen.
5. CLI-Tests erweitern: Erfolgsfall mit gefaktem Renderer, `--output-dir`, `--force`, Slug-/Dateinamenbildung, Kollisionsschutz und mindestens drei Fehlerklassen. Bestehende Help-/Entrypoint-Tests beibehalten.
6. Verifikation mit `.venv/bin/python -m pytest`, `ruff check .` und `ruff format --check .`; falls `.venv` fehlt, auf `python -m pytest`/lokale Alternativen ausweichen und den Befund dokumentieren.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
CLI-Orchestrierung implementiert: `main()` validiert das Ausgabeverzeichnis, laedt YAML, normalisiert, berechnet, prueft Zielpfadkollisionen vor dem Rendering und ruft `render_pdf` mit stabilen Zielpfaden auf. Dateinamen werden aus Zeitraum und ASCII-Slug gebildet; mehrere Abrechnungen erhalten `-01`/`-02`-Suffixe. Erwartbare Lade-, Validierungs-, Berechnungs-, Pauschalen-, Render- und CLI-Fehler werden deutsch auf stderr gemeldet und liefern Exit-Code 1. Verifikation: `.venv/bin/python -m pytest` (45 passed), `ruff check .` (passed), `ruff format --check .` (passed). Manueller CLI-Check mit lokalem `typst 0.14.2`: `.venv/bin/python -m yaml_reisekosten_tool examples/example.yml --output-dir /tmp/yaml-reisekosten-cli-check --force` erzeugte `/tmp/yaml-reisekosten-cli-check/2026-01_reisekostenabrechnung.pdf`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implementiert die erste nutzbare CLI-Pipeline fuer `yaml-reisekosten-tool foo.yml`. Die CLI verdrahtet YAML-Laden, Normalisierung, Berechnung und Typst-Rendering, prueft `--output-dir`, verhindert vorhandene Ziel-PDFs ohne `--force` und gibt erzeugte PDF-Pfade auf stdout aus.

Die Dateinamenbildung ist in der CLI gekapselt: Zeitraum plus Titel-Slug ergeben stabile ASCII-PDF-Namen, mehrere Abrechnungen erhalten deterministische `-01`/`-02`-Suffixe. Erwartbare Fehler aus Dateisystem, YAML, Schema, Fachlogik, Pauschalentabellen und Rendering werden als kurze deutsche stderr-Meldungen mit Exit-Code 1 behandelt.

CLI-Tests decken Erfolgsfall, `--output-dir`, `--force`, Kollisionsschutz, Dateinamensuffixe und mehrere Fehlerklassen ab. Verifikation: `.venv/bin/python -m pytest` (45 passed), `ruff check .` (passed), `ruff format --check .` (passed). Zusaetzlicher echter CLI-Render mit lokalem `typst 0.14.2` erzeugte `/tmp/yaml-reisekosten-cli-check/2026-01_reisekostenabrechnung.pdf`.
<!-- SECTION:FINAL_SUMMARY:END -->
