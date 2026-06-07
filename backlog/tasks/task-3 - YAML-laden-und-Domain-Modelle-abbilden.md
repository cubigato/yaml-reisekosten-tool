---
id: TASK-3
title: YAML laden und Domain-Modelle abbilden
status: Done
assignee:
  - Codex
created_date: '2026-06-07 19:10'
updated_date: '2026-06-07 20:26'
labels:
  - implementation
  - yaml
  - domain
dependencies:
  - TASK-2
documentation:
  - README.md
  - ARCHITECTURE.md
  - examples/example.yml
modified_files:
  - src/yaml_reisekosten_tool/yaml_io.py
  - src/yaml_reisekosten_tool/models.py
  - tests/test_yaml_io.py
  - tests/test_models.py
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implementiert den ersten fachlichen Eingang der Pipeline aus `ARCHITECTURE.md`: YAML-Datei sicher laden, Ladefehler von fachlichen Fehlern trennen und die erwartete Eingabestruktur in Python-Domain-Objekte ueberfuehren. Die Aufgabe orientiert sich am dokumentierten YAML-Format in `README.md` und am Beispiel `examples/example.yml`. Noch nicht Ziel dieser Aufgabe sind Pauschalenberechnung, Typst-Rendering und vollstaendige CLI-Orchestrierung.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `yaml_io.py` liest YAML-Dateien mit sicherem Loader und liefert fuer gueltige Dateien ein rohes Mapping.
- [x] #2 Fehlende Datei, unlesbare Datei, leere Datei und ungueltiges YAML werden als kontrollierte, testbare Fehler unterschieden.
- [x] #3 `models.py` enthaelt typisierte Domain-Modelle fuer Abrechnung, Mitarbeiter, Arbeitgeber, Fahrzeug, Fahrt, Auslage und die fuer weitere Pipeline-Schritte noetigen Werte.
- [x] #4 Das Beispiel `examples/example.yml` kann bis zu Domain-Objekten geladen werden, ohne Berechnung oder Rendering auszufuehren.
- [x] #5 Unit-Tests decken gueltiges Laden sowie typische Ladefehler ab.
- [x] #6 Die oeffentlichen Funktionen sind klein genug, dass nachfolgende Validierungs- und Normalisierungstasks daran anschliessen koennen.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. `src/yaml_reisekosten_tool/yaml_io.py` anlegen mit `load_yaml_mapping(path)`, `yaml.safe_load` und spezifischen Ladefehler-Exceptions fuer fehlende Datei, unlesbare Datei, leere Datei, ungueltiges YAML und nicht-Mapping.
2. `src/yaml_reisekosten_tool/models.py` anlegen mit Dataclasses fuer Abrechnung, Zeitraum, Mitarbeiter, Anschrift, Arbeitgeber, Fahrzeug, Auslage, Fahrt, Defaults und ReisekostenEingabe. Die Modelle bilden Struktur ab; Validierung, Normalisierung, Default-Merge und Berechnung bleiben Folge-Tasks.
3. Eine kleine Builder-Funktion `models_from_mapping(data)` implementieren, die das dokumentierte YAML-Format einschliesslich `examples/example.yml` in Domain-Objekte ueberfuehrt, ohne Berechnung oder Rendering auszufuehren.
4. Unit-Tests fuer erfolgreiches YAML-Laden, typische Ladefehler und das Laden von `examples/example.yml` bis zu Domain-Objekten ergaenzen.
5. Verifikation mit `pytest`, danach falls verfuegbar `ruff check .` und `ruff format --check .`.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented the first YAML/domain pipeline boundary without validation, normalization, default merging, calculation, rendering, or CLI orchestration. `yaml_io.load_yaml_mapping` uses `yaml.safe_load` and exposes specific testable exceptions for missing, unreadable, empty/null, invalid YAML, and non-mapping root inputs. `models.models_from_mapping` maps the documented YAML structure and example file into immutable dataclasses while preserving raw scalar values for follow-up validation/normalization tasks. Verification: `.venv/bin/python -m pytest` passed with 11 tests; `ruff check .` passed; `ruff format --check .` passed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Summary:
- Added `yaml_io.py` with safe YAML loading and explicit exception classes for controlled load failures.
- Added `models.py` with immutable dataclasses for the documented Reisekosten input structure plus a small `models_from_mapping` builder.
- Added unit coverage for successful YAML loading, missing/unreadable/empty/invalid/non-mapping YAML failures, and loading `examples/example.yml` into domain objects.

Tests:
- `.venv/bin/python -m pytest` -> 11 passed
- `ruff check .` -> passed
- `ruff format --check .` -> passed

Scope notes:
- Validation, default merging, normalization, calculation, rendering, and CLI orchestration remain intentionally out of this task and ready for follow-up tasks.
<!-- SECTION:FINAL_SUMMARY:END -->
