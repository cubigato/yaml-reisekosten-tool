---
id: TASK-12
title: Beschreibung von Reisenebenkosten im PDF anzeigen
status: Done
assignee:
  - Codex
created_date: '2026-06-15 09:54'
updated_date: '2026-06-15 10:02'
labels: []
dependencies: []
documentation:
  - README.md
  - ARCHITECTURE.md
modified_files:
  - src/yaml_reisekosten_tool/rendering.py
  - src/yaml_reisekosten_tool/templates/reisekosten.typ
  - tests/test_rendering.py
  - README.md
priority: medium
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Im Feld „Reisenebenkosten“ des erzeugten Lexware-PDFs wird derzeit nur die Summe der Auslage angezeigt. Zur fachlichen Nachvollziehbarkeit soll bei jeder einzelnen Reise zusätzlich die zugehörige Beschreibung aus `fahrten[].auslage.beschreibung` erscheinen. Da der MVP pro Fahrt ein eigenes PDF erzeugt und pro Fahrt höchstens eine Auslage modelliert, wird Betrag und Beschreibung gemeinsam in diesem Feld dargestellt. Das festgelegte Format lautet `<Betrag> EUR (<Beschreibung>)`, zum Beispiel `12,00 EUR (Parkhaus am Kundenstandort)`. Die Berechnung der Auslagensumme und die Markdown-Zusammenfassung sind nicht Teil dieser Änderung.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Enthält eine Fahrt eine Auslage, zeigt das Feld „Reisenebenkosten“ im zugehörigen PDF den formatierten Betrag und die Beschreibung im Format `<Betrag> EUR (<Beschreibung>)` an.
- [x] #2 Die angezeigte Beschreibung entspricht dem nach Defaults und Fahrt-Overrides normalisierten Wert der jeweiligen Fahrt.
- [x] #3 Enthält eine Fahrt keine Auslage, zeigt das Feld weiterhin `0,00 EUR` und enthält weder leere Klammern noch einen Platzhaltertext.
- [x] #4 Die Beschreibungen aus den vorhandenen Beispieldateien werden im PDF lesbar dargestellt und überlagern keine benachbarten Formularfelder.
- [x] #5 Automatisierte Rendering-Tests decken mindestens eine Fahrt mit Auslage sowie eine Fahrt ohne Auslage ab und prüfen Betrag und Beschreibung im Render-Kontext beziehungsweise in der Template-Ausgabe.
- [x] #6 Die Benutzerdokumentation beschreibt, dass die Auslagenbeschreibung zusammen mit dem Betrag im PDF-Feld „Reisenebenkosten“ erscheint.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Den Render-Kontext pro Fahrt um die normalisierte Auslagenbeschreibung und einen fertig formatierten Reisenebenkosten-Anzeigewert erweitern.
2. Das Typst-Feld „Reisenebenkosten“ auf den kombinierten Anzeigewert umstellen und die Darstellung auf lange Beispielbeschreibungen prüfen.
3. Rendering-Tests für Fahrt mit Auslage, Default/Override-Beschreibung und Fahrt ohne Auslage ergänzen.
4. README um das PDF-Ausgabeformat der Auslagenbeschreibung ergänzen.
5. Fokussierte und vollständige Tests sowie Ruff ausführen und ein Beispiel-PDF unter examples/rendered/ für das Review erzeugen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Render-Kontext liefert pro Einzelabrechnung den Wert `<Betrag> EUR (<Beschreibung>)` aus der berechneten, zuvor normalisierten Auslagenposition; ohne Auslage bleibt es bei `0,00 EUR`.

Das Typst-Feld nutzt eine kompakte, auf 84 mm begrenzte Darstellung. Die längste vorhandene Beispielbeschreibung `Tagesparkplatz Workshopzentrum` wurde im erzeugten PDF visuell und per pdftotext ohne Überlagerung geprüft.

Verifikation: 54 Pytest-Tests bestanden; `ruff check .` und `ruff format --check .` bestanden. Review-PDF: examples/rendered/task-12-review.pdf.

Review durch den Benutzer bestätigt. Temporäres Review-PDF nach Freigabe aus `examples/rendered/` entfernt; Task bleibt abgeschlossen.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Umsetzung
- Das PDF-Feld `Reisenebenkosten` zeigt bei Einzelabrechnungen jetzt Betrag und normalisierte Auslagenbeschreibung im Format `<Betrag> EUR (<Beschreibung>)`.
- Ohne Auslage bleibt die Ausgabe `0,00 EUR`; Mehrfahrten-Kontexte behalten aus Kompatibilitätsgründen die reine Summe.
- Das Typst-Layout verwendet für das 84-mm-Feld eine kompakte, begrenzte Textdarstellung, damit vorhandene Beispielbeschreibungen nicht in Nachbarfelder laufen.
- Rendering-Tests decken Default-Beschreibung, Fahrt-Override, Nullfall und Template-Anbindung ab; README wurde ergänzt.

## Verifikation
- `.venv/bin/python -m pytest`: 54 bestanden
- `ruff check .`: bestanden
- `ruff format --check .`: bestanden
- Review-PDF visuell und per `pdftotext` geprüft: `examples/rendered/task-12-review.pdf`
<!-- SECTION:FINAL_SUMMARY:END -->
