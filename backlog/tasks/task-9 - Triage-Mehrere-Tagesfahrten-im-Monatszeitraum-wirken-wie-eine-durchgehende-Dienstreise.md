---
id: TASK-9
title: >-
  Triage: Mehrere Tagesfahrten im Monatszeitraum wirken wie eine durchgehende
  Dienstreise
status: Done
assignee:
  - Codex
created_date: '2026-06-08 12:27'
updated_date: '2026-06-08 12:38'
labels:
  - triage
  - pdf
  - fachlichkeit
  - ux
dependencies: []
documentation:
  - README.md
  - ARCHITECTURE.md
modified_files:
  - README.md
  - ARCHITECTURE.md
  - src/yaml_reisekosten_tool/cli.py
  - tests/test_cli_smoke.py
priority: high
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Beim ersten produktiven Einsatz wurde fuer einen Monatszeitraum mit vier einzelnen Vor-Ort-Terminen beim selben Kunden ein einzelnes PDF erzeugt. Das Ergebnis wirkt auf den Anwender so, als sei eine durchgehende Dienstreise ueber den ganzen Monat abgerechnet worden. Fachlich ist unklar, ob die zugrunde liegende Reisekostenvorlage eine Monatsabrechnung mit mehreren Fahrten in einem PDF vorsieht oder ob pro Fahrt/Reisetag ein separates PDF entstehen sollte. Wichtig: Das konkrete produktive YAML aus dem Nutzerbericht enthaelt private Daten und darf nicht als Testdaten, Fixture oder Beispiel eingecheckt werden; fuer Tests ausschliesslich synthetische Daten verwenden.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Fachlich ist geprueft und dokumentiert, ob mehrere einzelne Tagesfahrten innerhalb eines Abrechnungszeitraums als ein PDF oder als mehrere PDFs/Reisedokumente ausgegeben werden sollen.
- [x] #2 Die Entscheidung ist mit README.md und ARCHITECTURE.md abgeglichen und dort aktualisiert, falls das aktuelle Verhalten oder der CLI-Ausgabe-Kontrakt unklar oder falsch dokumentiert ist.
- [x] #3 Falls mehrere PDFs erwartet werden, erzeugt die Ausgabe fuer mehrere unabhaengige Tagesfahrten getrennte PDF-Dateien mit eindeutigem Dateinamen und nachvollziehbarem CLI-Output.
- [x] #4 Falls ein einzelnes PDF fachlich korrekt ist, ist Rendering/Text so angepasst, dass die Abrechnung nicht wie eine durchgehende Dienstreise ueber den gesamten Zeitraum wirkt.
- [x] #5 Automatisierte Tests decken den Fall mehrerer synthetischer Tagesfahrten innerhalb eines Monats ab; private Produktivdaten werden nicht eingecheckt.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Korrigierter Plan nach First-Principles-Pruefung an der Lexware-Vorlage:
1. Die zuvor eingefuehrte zusaetzliche Fahrtenuebersicht und Sammelabrechnungs-Dokumentation zuruecknehmen, weil sie das Lexware-Formular strukturell erweitert.
2. Fachliche Entscheidung neu festhalten: Eine `fahrt` entspricht einer Reise im Lexware-Formular. Mehrere getrennte Tagesfahrten in `fahrten` muessen deshalb mehrere PDFs erzeugen, damit Reisebeginn/-ende je PDF eine einzelne Reise beschreiben.
3. CLI-Orchestrierung so anpassen, dass eine berechnete Abrechnung mit mehreren Fahrten in mehrere berechnete Einzelabrechnungen aufgeteilt und mit den bestehenden nummerierten Dateinamen ausgegeben wird.
4. Render-Kontext fuer jedes Einzel-PDF bei den vorhandenen Lexware-Feldern belassen; keine zweite Seite und keine neue Liste einfuehren.
5. README.md, ARCHITECTURE.md und Tests entsprechend aktualisieren; Tests verwenden ausschliesslich synthetische Daten.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Entscheidung aus bestehendem Vertrag: Das aktuelle YAML-Modell kennt eine Abrechnung mit einer Liste von Fahrten. Mehrere PDFs pro Fahrt waeren eine neue Batch-/Schema-Semantik. Fuer TASK-9 wird deshalb AC #4 umgesetzt: ein einzelnes PDF bleibt korrekt, muss aber als Sammelabrechnung mit Einzelfahrten erkennbar sein.

Verifikation abgeschlossen: `.venv/bin/python -m pytest` (47 passed), `ruff check .`, `ruff format --check .`, echter Renderlauf mit `.venv/bin/python -m yaml_reisekosten_tool examples/example.yml --output-dir /tmp --force`, anschliessend PDF-Textcheck per `pdftotext`. AC #3 ist erfuellt im Sinne der dokumentierten Entscheidung: mehrere PDFs werden fuer mehrere `fahrten` innerhalb einer Abrechnung nicht erwartet; die Sammelabrechnung ist das definierte Verhalten.

Nach Nutzer-Einwand wurde die fachliche Herleitung erneut von der Lexware-Referenz geprueft. Die Referenz `examples/lexware_pdf_reisekostenabrechnung-mustervorlage.pdf` ist ein einseitiges Formular mit singulaeren Feldern fuer Reisebeginn und Reiseende und ohne Fahrtenliste. Die vorherige Umsetzung mit zusaetzlicher Fahrtenuebersicht weicht zu stark von der Vorlage ab und wird korrigiert.

Korrektur umgesetzt: Die zuvor eingefuehrte Fahrtenuebersicht/zweite Seite wurde entfernt. Die CLI splittet eine berechnete Abrechnung mit mehreren `fahrten` nun vor dem Rendering in einzelne Lexware-Formularabrechnungen pro Fahrt. Verifikation: `.venv/bin/python -m pytest` (47 passed), `ruff check .`, `ruff format --check .`, echter Renderlauf mit `examples/example.yml` erzeugt fuenf einzelne PDFs, `pdfinfo` bestaetigt fuer das erste PDF eine Seite, `pdftotext` zeigt Reisebeginn und Reiseende fuer denselben einzelnen Fahrtag.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Nach erneuter First-Principles-Pruefung an der lokalen Lexware-Referenz wurde die vorherige Sammelabrechnungs-Loesung korrigiert. Die Lexware-Vorlage ist ein einseitiges Formular mit singulaeren Feldern fuer Reisebeginn und Reiseende und ohne Fahrtenliste; eine zusaetzliche Fahrtenuebersicht wuerde die Vorlage strukturell veraendern.

Die CLI teilt eine berechnete YAML-Abrechnung mit mehreren `fahrten` jetzt vor dem Rendering in einzelne berechnete Abrechnungen pro Fahrt auf. Dadurch erzeugt jede Fahrt ein eigenes PDF mit den bestehenden Lexware-Formularfeldern; mehrere Ausgabedateien erhalten weiterhin die vorhandenen nummerierten Suffixe. README.md und ARCHITECTURE.md dokumentieren diese Entscheidung. Tests pruefen mit synthetischen Daten, dass mehrere Fahrten mehrere PDF-Pfade und Render-Aufrufe erzeugen.

Verifikation: `.venv/bin/python -m pytest` (47 passed), `ruff check .`, `ruff format --check .`, `git diff --check`, echter Typst-Renderlauf mit `examples/example.yml` nach `/tmp` erzeugte fuenf PDFs; `pdfinfo` und `pdftotext` bestaetigten exemplarisch ein einseitiges Formular mit Reisebeginn/-ende fuer eine einzelne Fahrt.
<!-- SECTION:FINAL_SUMMARY:END -->
