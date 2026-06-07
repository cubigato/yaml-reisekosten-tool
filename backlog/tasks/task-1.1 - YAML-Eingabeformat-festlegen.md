---
id: TASK-1.1
title: YAML-Eingabeformat festlegen
status: Done
assignee:
  - Codex
created_date: '2026-06-07 15:18'
updated_date: '2026-06-07 20:26'
labels:
  - architecture
  - yaml
dependencies: []
modified_files:
  - examples/example.yml
  - README.md
parent_task_id: TASK-1
priority: high
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Definiert das konkrete YAML-Format fuer Reisekostenabrechnungen als stabile Grundlage fuer Parser, Validierung und Beispiele. Ausgangspunkt ist `examples/example.yml`; das Format soll fuer reale Reisekostenfaelle klar, deutsch benannt und gut von Hand editierbar sein.

Wichtige Produktanforderung: Das YAML muss mit wenig Aufwand nebenbei pflegbar sein. Wiederkehrende Daten wie Kunde, Abrechnungssteller, privater PKW, Strecke und Standard-km sollen einmal oben als Defaults stehen. Einzelne Fahrten sollen darunter knapp erfasst werden koennen, typischerweise nur mit Datum und Zweck/Termin; seltene Abweichungen wie andere km wegen Umfahrung sollen pro Fahrt als Override moeglich sein.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Das geplante YAML-Schema beschreibt die benoetigten Pflicht- und optionalen Felder fuer Reise, Person/Absender, Arbeitgeber/Empfaenger, Zeitraeume, Kostenpositionen, Pauschalen und Belege.
- [x] #2 Mindestens ein repraesentatives Beispiel-YAML ist aktualisiert oder dokumentiert und deckt einen realistischen Abrechnungsfall ab.
- [x] #3 Offene Validierungsregeln sind entschieden oder als bewusst spaeterer Scope dokumentiert.
- [x] #4 Die Entscheidung ist so festgehalten, dass Parser- und PDF-Implementierung ohne weitere Formatklaerung beginnen koennen.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. `examples/example.yml` als ersten Formatentwurf mit deutschen Feldnamen anlegen.
2. Oben gemeinsame Stammdaten und Defaults modellieren: Abrechnung, Person, Kunde, Fahrzeug, Standardfahrt.
3. Darunter eine knappe Fahrtenliste modellieren, in der jede Fahrt Defaults erbt und nur Abweichungen wie `km` oder `notiz` ueberschreibt.
4. Kommentare sparsam nutzen, um offene Schemaentscheidungen wie Validierung, Belege und Pauschalen sichtbar zu machen, ohne das Beispiel zu ueberfrachten.
5. Task-Notiz mit der getroffenen Default/Override-Idee ergaenzen.

Ueberarbeitung nach Nutzerkommentaren: Schema vereinfachen, keine impliziten Verknuepfungen zwischen `abrechnender`/`kunde` und Fahrten vorsehen, Kundendaten auf fuer die Vorlage nuetzliche Angaben reduzieren, km als Gesamtstrecke modellieren, Zeiten als Strings schreiben und Verpflegungspauschale als automatische Ableitung aus Start-/Endzeit skizzieren.

Auslagen ebenfalls defaultfaehig modellieren: wiederkehrende Angaben wie Art, Betrag, Beschreibung und optional Belegmuster koennen unter `defaults.auslage` stehen; einzelne Auslagen referenzieren oder erben diese Defaults und ueberschreiben nur Datum oder Abweichungen.

README fuer das YAML-Format anlegen: `examples/example.yml` soll reine Eingabedatei bleiben; Schemaentscheidungen, Default/Override-Regeln und Pauschalenentscheidung werden in `README.md` dokumentiert.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Erster Entwurf in `examples/example.yml` angelegt. Kernidee: wiederkehrende Werte stehen unter `defaults.fahrt`; Eintraege in `fahrten` sind minimal und ueberschreiben nur Abweichungen wie `entfernung_km`, `zweck` oder `notiz`. Syntax wurde mit `python3 -c "import yaml; ..."` erfolgreich geprueft. Task bleibt offen, weil der Nutzer den Entwurf manuell weiter anpassen moechte.

Entwurf nach Nutzeranmerkungen ueberarbeitet: `kunde` durch vorlagennaeheres `arbeitgeber` ersetzt, keine implizite Verknuepfung zwischen Arbeitgeber und Fahrtziel vorgesehen, Fahrtdefaults auf `start`, `ziel`, `anlass`, `verkehrsmittel`, `fahrzeug`, `gesamt_km`, Zeiten und Pauschalen reduziert. `gesamt_km` ist als tatsaechlich gefahrene Gesamtstrecke dokumentiert. Uhrzeiten werden als Strings im Format HH:MM modelliert. Verpflegungspauschale ist als `automatisch` skizziert und soll aus Start-/Endzeit ableitbar sein. YAML-Syntax erneut erfolgreich geprueft.

Auslagen jetzt ebenfalls defaultfaehig im Beispiel modelliert. `defaults.auslage` enthaelt wiederkehrende Parkhausdaten; Eintraege in `auslagen` koennen nur mit `datum` auskommen oder Abweichungen wie anderen Betrag bzw. Belegpfad ueberschreiben. YAML-Syntax erfolgreich geprueft.

Entscheidung: Gesetzliche bzw. jahresabhaengige Pauschalen werden nicht als regulaere YAML-Eingabe modelliert. `kilometerpauschale_eur` wurde aus `examples/example.yml` entfernt. Die Software soll eine versionierte Jahrestabelle fuer pauschale Kilometersaetze anhand des Reisedatums verwenden. Gleiches Prinzip fuer Verpflegungspauschalen: Regeln und Betraege werden aus Datum, Start-/Endzeit und Kalenderjahr bzw. Reiseziel ermittelt. YAML enthaelt die beobachtbaren Reisedaten, nicht die jeweils geltenden steuerlichen Saetze. Grundlage: BMF/LStH verweist bei Fahrtkosten auf pauschale Kilometersaetze nach EStG; § 9 Abs. 4a EStG regelt inlaendische Verpflegungspauschalen, BMF-Schreiben veroeffentlichen Auslandsbetraege je Jahr.

Schema-Notizen aus `examples/example.yml` entfernt und als erste `README.md` dokumentiert. README beschreibt aktuelle YAML-Bereiche, Felder, Default/Override-Regeln, optionale Mitarbeiterfelder, Auslagen an Fahrten sowie Entscheidungen zu `gesamt_km`, Uhrzeit-Strings und softwareseitigen Pauschalentabellen. `examples/example.yml` bleibt reine Eingabedatei. YAML-Syntax erfolgreich geprueft.
<!-- SECTION:NOTES:END -->
