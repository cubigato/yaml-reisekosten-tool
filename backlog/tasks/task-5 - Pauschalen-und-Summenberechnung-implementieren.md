---
id: TASK-5
title: Pauschalen und Summenberechnung implementieren
status: To Do
assignee: []
created_date: '2026-06-07 19:11'
updated_date: '2026-06-07 19:47'
labels:
  - implementation
  - calculation
dependencies:
  - TASK-4
documentation:
  - README.md
  - ARCHITECTURE.md
  - examples/example.yml
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implementiert die fachliche Berechnungsschicht der Reisekostenabrechnung. Aus den normalisierten Fahrten und Auslagen werden Kilometerkosten, Verpflegungsmehraufwand und Gesamtsummen berechnet. Die Software verwendet interne Jahrestabellen statt Werte aus dem YAML; fehlende Tabellenjahre werden als fachlicher Fehler gemeldet. Rendering und CLI-Ausgabe sind nicht Bestandteil dieser Aufgabe.

Für die Implementierung werden im ersten Schritt fachliche Werte für 2026 und falls verfügbar 2027 recherchiert.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `rates.py` enthaelt interne Regeln oder Tabellen fuer Kilometerpauschalen und Verpflegungspauschalen fuer die im Beispiel benoetigten Jahre.
- [ ] #2 `calculation.py` berechnet Fahrtkosten aus Gesamt-Kilometern und Kilometerpauschale.
- [ ] #3 Verpflegungspauschalen werden aus Datum, Startzeit und Endzeit anhand der internen Regeln berechnet oder kontrolliert als nicht berechenbar gemeldet.
- [ ] #4 Auslagen werden in die Abrechnungssummen uebernommen und separat ausweisbar gehalten.
- [ ] #5 Das Ergebnis enthaelt eine berechnete Abrechnung mit Einzelpositionen und Gesamtsummen, die fuer den Render-Kontext nutzbar ist.
- [ ] #6 Unit-Tests decken Kilometerkosten, Verpflegungspauschale, Auslagen, Rundung und fehlende Pauschalentabellen ab.
<!-- AC:END -->
