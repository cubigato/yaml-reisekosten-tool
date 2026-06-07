---
id: TASK-3
title: YAML laden und Domain-Modelle abbilden
status: next
assignee: []
created_date: '2026-06-07 19:10'
updated_date: '2026-06-07 19:26'
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
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implementiert den ersten fachlichen Eingang der Pipeline aus `ARCHITECTURE.md`: YAML-Datei sicher laden, Ladefehler von fachlichen Fehlern trennen und die erwartete Eingabestruktur in Python-Domain-Objekte ueberfuehren. Die Aufgabe orientiert sich am dokumentierten YAML-Format in `README.md` und am Beispiel `examples/example.yml`. Noch nicht Ziel dieser Aufgabe sind Pauschalenberechnung, Typst-Rendering und vollstaendige CLI-Orchestrierung.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `yaml_io.py` liest YAML-Dateien mit sicherem Loader und liefert fuer gueltige Dateien ein rohes Mapping.
- [ ] #2 Fehlende Datei, unlesbare Datei, leere Datei und ungueltiges YAML werden als kontrollierte, testbare Fehler unterschieden.
- [ ] #3 `models.py` enthaelt typisierte Domain-Modelle fuer Abrechnung, Mitarbeiter, Arbeitgeber, Fahrzeug, Fahrt, Auslage und die fuer weitere Pipeline-Schritte noetigen Werte.
- [ ] #4 Das Beispiel `examples/example.yml` kann bis zu Domain-Objekten geladen werden, ohne Berechnung oder Rendering auszufuehren.
- [ ] #5 Unit-Tests decken gueltiges Laden sowie typische Ladefehler ab.
- [ ] #6 Die oeffentlichen Funktionen sind klein genug, dass nachfolgende Validierungs- und Normalisierungstasks daran anschliessen koennen.
<!-- AC:END -->
