---
id: TASK-4
title: Validierung und Normalisierung der Eingabedaten implementieren
status: Done
assignee:
  - Codex
created_date: '2026-06-07 19:10'
updated_date: '2026-06-07 20:26'
labels:
  - implementation
  - validation
  - normalization
dependencies:
  - TASK-3
documentation:
  - README.md
  - ARCHITECTURE.md
  - examples/example.yml
modified_files:
  - .gitignore
  - src/yaml_reisekosten_tool/models.py
  - src/yaml_reisekosten_tool/normalization.py
  - src/yaml_reisekosten_tool/validation.py
  - tests/test_models.py
  - tests/test_normalization.py
priority: high
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ergaenzt die fachliche Eingangspruefung und Normalisierung nach dem in `README.md` dokumentierten YAML-Format. Defaults aus `defaults.fahrt` und `defaults.auslage` werden auf einzelne Eintraege angewendet, Overrides bleiben erhalten, und Datums-, Zeit-, Geld- und Kilometerwerte werden in stabile Python-Werte ueberfuehrt. Fehler sollen Feldpfade enthalten, damit die CLI spaeter nutzbare deutsche Meldungen ausgeben kann.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Pflichtbereiche und Pflichtfelder aus dem README werden validiert, inklusive `abrechnung`, `mitarbeiter`, `arbeitgeber` und `fahrten`.
- [x] #2 Defaults fuer Fahrten und Auslagen werden korrekt angewendet; ein einzelner Fahrt- oder Auslagenwert ueberschreibt den Default.
- [x] #3 Datumswerte, Uhrzeiten im Format `HH:MM`, Euro-Betraege und Kilometer werden in stabile Python-Typen normalisiert.
- [x] #4 Fehler fuer fehlende oder ungueltige Felder enthalten einen nachvollziehbaren Feldpfad wie `fahrten[3].datum`.
- [x] #5 Fachlich unplausible Basisdaten wie negative Kilometer oder Endzeit vor Startzeit werden kontrolliert abgelehnt.
- [x] #6 Unit-Tests decken Default/Override-Verhalten, gueltige Normalisierung und mehrere Fehlerfaelle ab.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Bestehende Modellgrenzen beibehalten: `models.py` bleibt fuer Dataclasses und Mapping-Aufbau zustaendig; neue Module `validation.py` und `normalization.py` liefern die fachliche Vorstufe.
2. In `validation.py` eine `ValidationError` mit Feldpfad einfuehren und Root-Struktur, Pflichtbereiche, Pflichtfelder, erwartete Mapping-/Listen-Typen, erlaubte Waehrung sowie Basiswertebereiche pruefen.
3. In `normalization.py` Defaults fuer `defaults.fahrt` und `defaults.auslage` tief genug auf einzelne `fahrten` anwenden, Overrides erhalten und Datum/Uhrzeit/Decimal/Kilometer in stabile Python-Typen wandeln.
4. Eine oeffentliche Funktion wie `normalize_reisekosten_input(data)` bereitstellen, die Validierung, Default-Anwendung und Typnormalisierung ausfuehrt und anschliessend ein `ReisekostenEingabe`-Modell zurueckgibt.
5. Tests fuer Beispiel-YAML, Default/Override-Verhalten, Datums-/Zeit-/Geld-/Kilometertypen und mehrere Fehlerpfade ergaenzen; bestehende Modell-/YAML-I/O-Tests nur soweit noetig anpassen.
6. Relevante Checks ausfuehren: fokussierte Pytest-Suite, danach nach Moeglichkeit gesamte Testsuite und Ruff.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementiert wurden Validierung und Normalisierung als eigene Vorstufe vor `models_from_mapping`: Pflichtstruktur, Feldpfade, Default-Merge, striktes HH:MM, nicht-negative Decimal-Werte sowie Plausibilitaetspruefung fuer Zeitreihenfolge. Nach Nutzerhinweis wurden getrackte `__pycache__`-Artefakte aus dem Arbeitsbaum entfernt und `.gitignore` ergaenzt, damit neue Cache-Dateien ignoriert werden. Verifikation: `.venv/bin/python -m pytest` (19 passed), `.venv/bin/ruff check .`, `.venv/bin/ruff format --check .`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Validierung und Normalisierung fuer die dokumentierte YAML-Eingabe wurden ergaenzt. `normalize_reisekosten_input` prueft Root- und Pflichtfelder mit nachvollziehbaren Feldpfaden, wendet Fahrt- und Auslagen-Defaults mit Override-Unterstuetzung an und wandelt Datum, Uhrzeit, Euro-Betraege und Kilometer in stabile Python-Typen um. Fachlich unplausible Werte wie negative Kilometer oder Endzeit vor Startzeit werden kontrolliert als `ValidationError` abgelehnt.

Die Domain-Typen wurden fuer normalisierte Werte konkretisiert, und Tests decken Beispiel-YAML, Default/Override-Verhalten, gueltige Typnormalisierung sowie mehrere Fehlerfaelle ab. Zusaetzlich wurde `.gitignore` fuer Python-Cache-Artefakte ergaenzt und bereits getrackter Cache aus dem Arbeitsbaum entfernt.

Verifikation: `.venv/bin/python -m pytest` (19 passed), `.venv/bin/ruff check .`, `.venv/bin/ruff format --check .`.
<!-- SECTION:FINAL_SUMMARY:END -->
