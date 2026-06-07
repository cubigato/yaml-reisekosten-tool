---
id: TASK-1.3
title: Modul- und Datenfluss-Architektur festlegen
status: Done
assignee:
  - Codex
created_date: '2026-06-07 15:18'
updated_date: '2026-06-07 20:26'
labels:
  - architecture
  - python
dependencies:
  - TASK-1.1
  - TASK-1.2
modified_files:
  - ARCHITECTURE.md
  - README.md
  - AGENTS.md
parent_task_id: TASK-1
priority: high
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Schneidet die erste Implementierungsarchitektur fuer das Python-Projekt zu: YAML laden, validieren/normalisieren, Abrechnungsmodell bilden und PDF rendern. Ziel ist eine kleine, testbare Struktur, die zur fruehen CLI-Implementierung passt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Die vorgesehenen Module oder Pakete fuer CLI, YAML-I/O, Validierung/Domain-Modell und Rendering sind benannt.
- [x] #2 Der Datenfluss von Eingabe-YAML bis erzeugtem PDF ist beschrieben, inklusive der wichtigsten Fehlerpunkte.
- [x] #3 Die Architektur vermeidet vorzeitige Framework-Komplexitaet und benennt bewusst ausgelassenen Scope.
- [x] #4 Die Entscheidung ist konkret genug, um das Projektgeruest und erste Tests anzulegen.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Bestehende Projektstruktur, `README.md`, `examples/example.yml`, `AGENTS.md` und den Typst-Template-Pfad aus `TASK-1.2` pruefen.
2. Ein neues `ARCHITECTURE.md` als zentrale Architekturentscheidung fuer die fruehe Python-Implementierung anlegen.
3. Darin Module/Pakete fuer CLI, YAML-I/O, Validierung/Domain-Modell, Normalisierung/Berechnung und Typst-Rendering benennen.
4. Den Datenfluss von Eingabe-YAML bis erzeugtem PDF inklusive wichtiger Fehlerpunkte dokumentieren.
5. Bewusst ausgelassenen MVP-Scope dokumentieren, damit keine vorzeitige Framework-Komplexitaet entsteht.
6. `README.md` knapp auf die Architekturentscheidung verweisen und ggf. den Projektueberblick angleichen.
7. `AGENTS.md` so ergaenzen, dass Agents vor Arbeit am Projekt `README.md` und `ARCHITECTURE.md` lesen sollen.
8. Relevante Syntax-/Plausibilitaetschecks ausfuehren und erfuellte Acceptance Criteria im Task markieren, den Task aber gemaess Nutzerwunsch nicht auf `Done` setzen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Architekturentscheidung dokumentiert: `ARCHITECTURE.md` beschreibt den MVP als lineare Pipeline von CLI ueber YAML-I/O, Validierung, Normalisierung, Domain-Modell, Pauschalen-/Summenberechnung bis Typst-Rendering. Die vorgesehenen Module unter `src/yaml_reisekosten_tool/` sind benannt, Fehlerpunkte und bewusst ausgelassener Scope sind festgehalten. `README.md` verweist auf die Architekturdatei. `AGENTS.md` weist Agents an, vor Aenderungen `README.md` und `ARCHITECTURE.md` zu lesen. Status bleibt gemaess Nutzerwunsch `In Progress` bis Review abgeschlossen ist.
<!-- SECTION:NOTES:END -->
