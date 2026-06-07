---
id: TASK-6
title: Typst-Rendering aus berechneter Abrechnung implementieren
status: Done
assignee:
  - Codex
created_date: '2026-06-07 19:11'
updated_date: '2026-06-07 20:26'
labels:
  - implementation
  - rendering
  - typst
dependencies:
  - TASK-5
documentation:
  - ARCHITECTURE.md
  - src/yaml_reisekosten_tool/templates/reisekosten.typ
  - examples/rendered/reisekosten_typst.pdf
modified_files:
  - LICENSE
  - README.md
  - examples/example.yml
  - examples/rendered/task-6-review.pdf
  - examples/signatures/max-mustermann.png
  - examples/signatures/erika-leitung.png
  - src/yaml_reisekosten_tool/models.py
  - src/yaml_reisekosten_tool/normalization.py
  - src/yaml_reisekosten_tool/rendering.py
  - src/yaml_reisekosten_tool/templates/reisekosten.typ
  - tests/test_models.py
  - tests/test_normalization.py
  - tests/test_rendering.py
priority: high
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Schliesst die berechnete Abrechnung an das vorhandene Typst-Template `src/yaml_reisekosten_tool/templates/reisekosten.typ` an. Die Aufgabe baut einen Render-Kontext, findet das Template als Package-Daten und ruft Typst so auf, dass ein PDF entsteht. Die CLI-Orchestrierung und Dateinamenlogik werden erst im folgenden CLI-Task final verdrahtet.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `rendering.py` baut aus einer berechneten Abrechnung einen stabilen Typst-Render-Kontext mit allen fuer das Template noetigen Werten.
- [x] #2 Das vorhandene Template wird als Package-Daten gefunden, ohne vom aktuellen Arbeitsverzeichnis abzuhaengen.
- [x] #3 Der Typst-Aufruf ist gekapselt und gibt kontrollierte Fehler fuer fehlendes Typst, fehlendes Template oder fehlgeschlagenes Rendering zurueck.
- [x] #4 Das Rendering schreibt ein PDF an einen explizit uebergebenen Zielpfad oder erzeugt eine klar testbare Zwischenausgabe fuer den finalen Schreibschritt.
- [x] #5 Unit-Tests pruefen Render-Kontext, Template-Aufloesung und Typst-Aufruf mit gefaktem Prozessaufruf.
- [x] #6 Wenn Typst lokal installiert ist, gibt es optional einen Integrationstest oder dokumentierten manuellen Check mit `examples/example.yml`.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. `src/yaml_reisekosten_tool/rendering.py` neu anlegen: JSON-kompatiblen Render-Kontext aus `BerechneteAbrechnung` bauen, stabile Formatter fuer Datum/Zeit/Geld/Kilometer nutzen, Template via `importlib.resources.files(...)` unabhaengig vom CWD aufloesen und `render_pdf(...)` mit kontrollierten `RenderingError`-Faellen fuer fehlendes Typst, fehlendes Template und Typst-Prozessfehler kapseln.
2. `src/yaml_reisekosten_tool/templates/reisekosten.typ` datengetrieben machen: Kontext ueber Typst-Input einlesen, die vorhandene Lexware-nahe Vorlage erhalten und Felder mit aggregierten/berechneten Werten fuellen. Mehrere Fahrten werden fuer den MVP aggregiert: erste/letzte Fahrt fuer Reisebeginn/-ende, Ziele/Anlaesse zusammengefasst, Kostenfelder aus Summen.
3. Unit-Tests ergaenzen: Render-Kontext aus `examples/example.yml`, Template-Aufloesung unabhaengig vom CWD, Typst-Aufruf mit gefaktem Runner inklusive JSON-Input und Zielpfad, sowie Fehlerfaelle fuer fehlendes Typst, fehlendes Template und fehlgeschlagenes Rendering.
4. Optionalen Typst-Check ausfuehren: wenn `typst` lokal verfuegbar ist, mit `examples/example.yml` ein Review-PDF erzeugen; falls nicht, Runtime-Verfuegbarkeit im Task dokumentieren.
5. Verifikation mit `pytest`, `ruff check .` und `ruff format --check .`. Task bleibt nach Implementierung fuer User-Review offen; YAML und passendes PDF werden zur Pruefung bereitgestellt, bevor auf Done gesetzt wird.

Review-Nachtrag: Footer ohne Lexware-Hinweis ausgeben und durch `erstellt mit yaml-reisekosten-tool by cubigato` ersetzen. README/Lizenzhinweis ergaenzen, dass die Projektlizenz nicht fuer die originale Lexware-Vorlage unter `examples/` gilt. YAML-Modell um `unterschriften.antragsteller` und optional `unterschriften.vorgesetzter` erweitern; Antragstellerdaten sollen immer digital in die Signaturzeile gerendert werden, Signaturbildpfade koennen als PNG/JPG/JPEG gesetzt werden. Renderer kopiert referenzierte Signaturbilder in das temporaere Typst-Root und uebergibt relative Pfade an das Template.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementierung abgeschlossen und verifiziert, Task bleibt fuer User-Review offen. Renderer baut einen JSON-kompatiblen Kontext aus `BerechneteAbrechnung`, loest das Template ueber Package-Daten auf, kopiert Template und Kontext fuer den Typst-Lauf in ein temporaeres Root-Verzeichnis und schreibt an einen expliziten Zielpfad. Fehlerfaelle fuer fehlendes Typst, fehlendes Template und Typst-Prozessfehler sind gekapselt. Tests: `.venv/bin/python -m pytest` (32 passed), `ruff check .` (passed), `ruff format --check .` (passed). Manueller Typst-Check mit lokalem `typst 0.14.2`: `examples/example.yml` nach `examples/rendered/task-6-review.pdf` gerendert; PDF-Text enthaelt die erwarteten Kernwerte und Summen.

Review-Nachtrag umgesetzt: Lexware-Footer im Template entfernt und durch `erstellt mit yaml-reisekosten-tool by cubigato` ersetzt. README und LICENSE enthalten nun einen expliziten Hinweis, dass die Projektlizenz nicht fuer die originale Lexware-Vorlage bzw. Lexware-Referenzdateien unter `examples/` gilt. YAML-Modell und Normalisierung unterstuetzen `unterschriften.antragsteller` und optional `unterschriften.vorgesetzter` mit `ort`, `datum`, `name` und `unterschrift` als PNG/JPG/JPEG-Pfad. Renderer kopiert Signaturbilder in das temporaere Typst-Root und bettet sie ein. `examples/example.yml` enthaelt Review-Daten plus Beispiel-PNGs unter `examples/signatures/`; `examples/rendered/task-6-review.pdf` wurde neu gerendert. Tests: `.venv/bin/python -m pytest` (34 passed), `ruff check .` (passed), `ruff format --check .` (passed). Typst-Render erfolgreich; PDF-Text zeigt digitale Signaturmetadaten und den neuen Footer ohne Lexware-Hinweis. Task bleibt fuer erneutes User-Review offen.

Musterunterschriften per Imagegen neu erzeugt und in `examples/signatures/max-mustermann.png` sowie `examples/signatures/erika-leitung.png` ersetzt. Chroma-Key-Hintergrund lokal mit ImageMagick entfernt, sichtbare Signaturpixel auf sauberes Schwarz despillt und transparentes PNG behalten. `examples/rendered/task-6-review.pdf` neu gerendert; PDF-Vorschau geprueft, Signaturen sind nicht abgeschnitten und ohne gruene Raender. Tests: `.venv/bin/python -m pytest` (34 passed), `ruff check .` (passed), `ruff format --check .` (passed).

Signaturplatzierung nach PDF-Sichtpruefung angepasst: Bildbreite im Typst-Template von 39mm auf 58mm erhoeht, Signaturen weiter links verankert und 2mm tiefer gesetzt. `examples/rendered/task-6-review.pdf` neu gerendert und Vorschau geprueft. Tests: `.venv/bin/python -m pytest` (34 passed), `ruff check .` (passed), `ruff format --check .` (passed).
<!-- SECTION:NOTES:END -->
