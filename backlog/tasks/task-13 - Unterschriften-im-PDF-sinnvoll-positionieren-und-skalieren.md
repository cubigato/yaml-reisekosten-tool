---
id: TASK-13
title: Unterschriften im PDF sinnvoll positionieren und skalieren
status: Done
assignee:
  - codex
created_date: '2026-06-15 10:38'
updated_date: '2026-06-15 10:40'
labels:
  - bug
  - rendering
dependencies: []
documentation:
  - README.md
  - ARCHITECTURE.md
modified_files:
  - src/yaml_reisekosten_tool/templates/reisekosten.typ
  - tests/test_rendering.py
priority: high
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Digitale Unterschriften werden zwar korrekt eingebettet, sind im Lexware-Formular aber zu groß, überlappen beide Unterschriftszeilen und ragen in den unteren Seitenbereich. Das Signaturlayout soll für typische breite PNG-Unterschriften lesbar und eindeutig der jeweiligen Zeile zugeordnet sein.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Antragsteller- und Vorgesetztenunterschrift überlappen sich im gerenderten PDF nicht
- [x] #2 Jede Unterschrift ist visuell ihrer jeweiligen Unterschriftszeile zugeordnet und bleibt innerhalb des Seitenbereichs
- [x] #3 Breite Unterschrifts-PNGs werden proportional und in sinnvoller Größe dargestellt
- [x] #4 Automatisierte Tests sichern die relevanten Layoutvorgaben ab
- [x] #5 Ein mit 160 DPI konvertiertes Kontrollbild bestätigt das korrigierte Layout
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Das aktuelle Beispiel-PDF mit `convert -density 160` in PNG umwandeln und den Signaturbereich visuell vermessen. 2. Die Signaturdarstellung im Typst-Template so begrenzen und positionieren, dass breite PNGs proportional innerhalb der jeweiligen Zeile bleiben. 3. Einen fokussierten Template-Test für Größen- und Positionsvorgaben ergänzen. 4. Rendering-Tests und vollständige Testsuite ausführen. 5. Das Beispiel neu rendern, erneut bei 160 DPI konvertieren und visuell prüfen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Auftraggeber hat die direkte Bearbeitung einschließlich visueller Prüfung mit `convert -density 160` angefordert.

Die Signaturbilder werden nun in einem rechtsbündigen 40 x 10 mm großen Rahmen proportional mit `fit: contain` dargestellt. Der Rahmen liegt vollständig oberhalb der jeweiligen Unterschriftslinie.

Visuelle Kontrolle erfolgte mit `convert -density 160` und weißem Hintergrund. Beide Signaturen bleiben getrennt, die Metadaten und Zeilenbeschriftungen lesbar, der Footer frei.

Verifikation: 55 Pytest-Tests bestanden; `ruff check .` und `ruff format --check .` bestanden. Keine Dokumentationsänderung erforderlich, da das YAML-Format unverändert bleibt.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Die übergroße Signaturdarstellung im Typst-Template wurde korrigiert. Statt einer festen Bildbreite von 58 mm, die bei breiten PNGs etwa 30 mm Höhe erzeugte, nutzt jede Signatur jetzt einen rechtsbündigen 40 x 10 mm Rahmen mit proportionaler `contain`-Skalierung. Dadurch bleibt jede Signatur innerhalb ihrer eigenen 12,7-mm-Zeile und überdeckt weder die zweite Signatur noch den Footer. Ein fokussierter Template-Test sichert Größe, Position und proportionale Skalierung ab. Das produktive Beispiel wurde lokal neu gerendert und mit ImageMagick bei 160 DPI visuell geprüft. Tests: 55 passed; Ruff-Lint und Formatprüfung bestanden.
<!-- SECTION:FINAL_SUMMARY:END -->
