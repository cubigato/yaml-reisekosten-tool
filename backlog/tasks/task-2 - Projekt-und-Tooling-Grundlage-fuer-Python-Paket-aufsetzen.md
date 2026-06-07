---
id: TASK-2
title: Projekt- und Tooling-Grundlage fuer Python-Paket aufsetzen
status: Done
assignee:
  - '@Codex'
created_date: '2026-06-07 19:10'
updated_date: '2026-06-07 20:26'
labels:
  - implementation
  - tooling
dependencies: []
documentation:
  - README.md
  - ARCHITECTURE.md
  - AGENTS.md
modified_files:
  - pyproject.toml
  - src/yaml_reisekosten_tool/cli.py
  - src/yaml_reisekosten_tool/__main__.py
  - tests/test_cli_smoke.py
  - README.md
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Richtet die technische Basis fuer die eigentliche Implementierung ein. Der aktuelle Stand enthaelt bereits `src/yaml_reisekosten_tool/` und ein Typst-Template, aber noch keinen sichtbaren Python-Projektvertrag wie `pyproject.toml`, CLI-Entry-Point, Test-Setup oder Ruff-Konfiguration. Grundlage sind `README.md`, `ARCHITECTURE.md` und die Architekturentscheidungen aus `TASK-1.*`. Projektsprache und Fehlermeldungen bleiben Deutsch.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `pyproject.toml` beschreibt das Paket unter `src/`, die Runtime-Abhaengigkeiten und die Entwicklungswerkzeuge fuer pytest und Ruff.
- [x] #2 Ein CLI-Entry-Point `yaml-reisekosten-tool` ist paketiert und kann mindestens eine Platzhalter-Hilfe oder kontrollierte Platzhalterausfuehrung starten.
- [x] #3 `python -m yaml_reisekosten_tool` nutzt denselben Einstieg oder ist bewusst dokumentiert gleichwertig vorbereitet.
- [x] #4 pytest- und Ruff-Konfiguration sind vorhanden und lassen sich lokal ausfuehren.
- [x] #5 Mindestens ein Smoke-Test prueft, dass Paketimport und CLI-Einstieg erreichbar sind.
- [x] #6 README oder Entwicklerhinweise nennen die lokalen Befehle fuer Installation, Tests und Linting.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. `pyproject.toml` anlegen mit `src`-Layout, Paketmetadaten, Runtime-Abhaengigkeit `PyYAML`, optionalen Dev-Abhaengigkeiten fuer `pytest` und `ruff` sowie pytest-/Ruff-Konfiguration.
2. Minimalen CLI-Einstieg in `src/yaml_reisekosten_tool/cli.py` bauen: `yaml-reisekosten-tool --help` funktioniert, ein Aufruf mit YAML-Datei endet kontrolliert mit deutscher Platzhalter-/MVP-Meldung statt Traceback.
3. `src/yaml_reisekosten_tool/__main__.py` ergaenzen, sodass `python -m yaml_reisekosten_tool` denselben Einstieg nutzt.
4. Smoke-Tests unter `tests/` hinzufuegen: Paket importierbar, CLI-Hilfe erreichbar, `python -m` Einstieg erreichbar.
5. README um Entwicklerbefehle fuer Setup, Tests und Linting ergaenzen.
6. Lokal `pytest` und `ruff` ausfuehren, sofern die Abhaengigkeiten in der Umgebung verfuegbar sind; fehlende lokale Tools werden in den Task-Notizen dokumentiert.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Projektbasis umgesetzt: `pyproject.toml` nutzt src-Layout, Hatchling-Build, Runtime-Abhaengigkeit `PyYAML`, Dev-Extras fuer pytest/Ruff sowie pytest- und Ruff-Konfiguration. CLI-Platzhalter liegt in `src/yaml_reisekosten_tool/cli.py`; `yaml-reisekosten-tool` und `python -m yaml_reisekosten_tool` nutzen denselben Einstieg. Smoke-Tests pruefen Paketimport, CLI-Hilfe und Modulaufruf. Lokale `.venv` wurde mit `uv venv` und `uv pip install -e .[dev]` erstellt; generierte Caches wurden wieder entfernt. Verifikation erfolgreich: `.venv/bin/python -m pytest` (3 passed), `.venv/bin/python -m ruff check .`, `.venv/bin/python -m ruff format --check .`, `.venv/bin/yaml-reisekosten-tool --help`, `.venv/bin/python -m yaml_reisekosten_tool --help`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Projekt- und Tooling-Grundlage fuer das Python-Paket eingerichtet.

Geaendert wurde ein neuer `pyproject.toml` mit src-Layout, Hatchling-Build, paketiertem CLI-Script, Runtime-Abhaengigkeit `PyYAML`, Dev-Extras fuer pytest/Ruff sowie zentraler pytest- und Ruff-Konfiguration. Der neue CLI-Platzhalter in `src/yaml_reisekosten_tool/cli.py` bietet Hilfe, akzeptiert den geplanten MVP-Aufruf mit Eingabedatei, `--output-dir` und `--force` und beendet kontrolliert mit deutscher Platzhaltermeldung. `src/yaml_reisekosten_tool/__main__.py` leitet `python -m yaml_reisekosten_tool` auf denselben Einstieg.

Ergaenzt wurden Smoke-Tests fuer Paketimport, CLI-Hilfe und Modulaufruf sowie README-Entwicklerbefehle fuer Installation, Tests und Linting.

Verifikation: `.venv/bin/python -m pytest` (3 passed), `.venv/bin/python -m ruff check .`, `.venv/bin/python -m ruff format --check .`, `.venv/bin/yaml-reisekosten-tool --help`, `.venv/bin/python -m yaml_reisekosten_tool --help`.
<!-- SECTION:FINAL_SUMMARY:END -->
