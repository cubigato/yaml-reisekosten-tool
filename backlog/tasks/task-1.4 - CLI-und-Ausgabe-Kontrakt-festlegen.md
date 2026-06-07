---
id: TASK-1.4
title: CLI- und Ausgabe-Kontrakt festlegen
status: Done
assignee:
  - Codex
created_date: '2026-06-07 15:18'
updated_date: '2026-06-07 20:26'
labels:
  - architecture
  - cli
dependencies:
  - TASK-1.1
  - TASK-1.3
modified_files:
  - ARCHITECTURE.md
  - README.md
parent_task_id: TASK-1
priority: medium
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Definiert das erwartete Verhalten des einfachen CLI-Interfaces fuer die erste nutzbare Version. Ohne Zusatzargumente soll `yaml-reisekosten-tool foo.yml` im aktuellen Verzeichnis PDF-Dateien mit sinnvollen Namen erzeugen und keinen unnoetigen Output hinterlassen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Der Standardaufruf mit einer YAML-Datei und das erwartete Ausgabeverzeichnis sind festgelegt.
- [x] #2 Regeln fuer PDF-Dateinamen sind definiert, inklusive Verhalten bei mehreren Abrechnungen oder Namenskollisionen.
- [x] #3 Das Verhalten bei ungueltiger Eingabe, fehlender Datei und Render-Fehlern ist grob entschieden.
- [x] #4 Es ist entschieden, welche optionalen CLI-Argumente fuer die erste Version aufgenommen oder bewusst weggelassen werden.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. `ARCHITECTURE.md` um einen Abschnitt `CLI- und Ausgabe-Kontrakt` erweitern.
2. Den Standardaufruf festlegen: `yaml-reisekosten-tool foo.yml`, genau eine YAML-Datei als Eingabe, Ausgabe standardmaessig ins aktuelle Arbeitsverzeichnis.
3. Regeln fuer PDF-Dateinamen definieren, inklusive stabiler Slugs, mehreren Abrechnungen und Namenskollisionen.
4. Fehlerverhalten fuer fehlende Datei, ungueltiges YAML/Schema, fachliche Fehler, Render-Fehler und Ausgabekollisionen grob festlegen.
5. Optionale CLI-Argumente fuer den MVP entscheiden und bewusst ausgelassenen CLI-Scope dokumentieren.
6. `README.md` knapp um die Nutzerperspektive fuer CLI-Aufruf, Ausgabe und Fehlerverhalten ergaenzen.
7. Backlog-Task mit geaenderten Dateien, Implementation Notes und erfuellten Acceptance Criteria aktualisieren; Status bleibt fuer Nutzerreview `In Progress`.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
CLI- und Ausgabe-Kontrakt dokumentiert: Standardaufruf ist `yaml-reisekosten-tool foo.yml` mit genau einer YAML-Datei und Standardausgabe ins aktuelle Arbeitsverzeichnis. PDF-Dateinamen basieren auf Zeitraum/Titel-Slug oder Eingabename, mehrere Abrechnungen erhalten nummerierte Suffixe, vorhandene PDFs werden ohne `--force` nicht ueberschrieben. Fehlerverhalten fuer fehlende Datei, YAML-/Schema-/Fachfehler, Render-Fehler und Ausgabekollisionen ist grob festgelegt. Fuer den MVP sind `--output-dir DIR` und `--force` vorgesehen; weitere CLI-Komplexitaet ist bewusst ausgeschlossen. `README.md` enthaelt die kurze Nutzerfassung. Status bleibt fuer Nutzerreview `In Progress`.
<!-- SECTION:NOTES:END -->
