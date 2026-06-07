---
id: TASK-1.2
title: 'Dokumentenerzeugung entscheiden: Typst vs. LaTeX'
status: Done
assignee:
  - '@Codex'
created_date: '2026-06-07 15:18'
updated_date: '2026-06-07 20:26'
labels:
  - architecture
  - pdf
  - decision
dependencies: []
modified_files:
  - src/yaml_reisekosten_tool/templates/reisekosten.typ
  - src/yaml_reisekosten_tool/__init__.py
  - src/yaml_reisekosten_tool/templates/__init__.py
  - examples/rendered/reisekosten_typst.pdf
  - examples/rendered/reisekosten_typst.png
  - examples/rendered/lexware_reference.png
  - examples/spikes/latex-renderer/lexware_reisekosten_latex.tex
  - examples/spikes/latex-renderer/lexware_reisekosten_latex.pdf
  - examples/spikes/latex-renderer/lexware_reisekosten_latex.png
  - examples/spikes/latex-renderer/lexware_reisekosten_latex.aux
  - examples/spikes/latex-renderer/lexware_reisekosten_latex.log
parent_task_id: TASK-1
priority: high
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fuehrt einen kurzen Spike zur PDF-Erzeugung durch und entscheidet, ob Typst fuer die Reisekostenabrechnung praktikabel ist oder ob LaTeX als Fallback verwendet wird. Die Entscheidung soll Build-/Runtime-Anforderungen, Template-Wartbarkeit und PDF-Qualitaet gegen die Lexware-Vorlage abwaegen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Typst und LaTeX sind anhand derselben minimalen Abrechnungsskizze verglichen oder nachvollziehbar bewertet.
- [x] #2 Die Entscheidung benennt den gewaelten Renderer und die wichtigsten Gruende, inklusive Installations-/CI-Auswirkungen.
- [x] #3 Die Entscheidung beschreibt, wie Templates im Projekt abgelegt und aus Python heraus angesteuert werden sollen.
- [x] #4 Falls Typst gewaehlt wird, ist klar dokumentiert, unter welchen Bedingungen auf LaTeX zurueckgefallen wird oder warum kein Fallback noetig ist.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Referenz `examples/lexware_pdf_reisekostenabrechnung-mustervorlage.pdf` visuell und strukturell inspizieren.
2. Zwei kleine Nachbauten derselben Beispielabrechnung unter `examples/` anlegen: eine LaTeX-Quelle und eine Typst-Quelle.
3. Beide Quellen lokal zu PDFs kompilieren, soweit die Toolchain im Projektumfeld verfuegbar ist.
4. Beide PDFs mit `convert -density 160` zu PNGs rendern und visuell gegen die Lexware-Vorlage pruefen.
5. Ergebnisse im Task notieren, aber noch keine Renderer-Entscheidung treffen; Stop fuer Nutzerreview der Quellen und PDFs.

6. Nach Nutzerfeedback Referenz genauer vermessen: relevante X/Y-Positionen, Linienlaengen, vertikale Abstaende, Checkbox-/Radio-Groessen und Fontwirkung aus der gerenderten Vorlage ableiten.

7. LaTeX- und Typst-Nachbau auf die gemessenen Positionen und reduzierte Fontgewichte/-groessen anpassen, damit die Layoutdrift nach unten verschwindet.

8. Beide Varianten erneut kompilieren, zu PNG rendern und visuell gegen die Referenz pruefen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Spike-Stand fuer Review: Lexware-Referenz wurde mit `convert -density 160` nach `examples/lexware_reference.png` gerendert. LaTeX-Nachbau liegt unter `examples/lexware_reisekosten_latex.tex`, kompiliert zu `examples/lexware_reisekosten_latex.pdf` und gerendert zu `examples/lexware_reisekosten_latex.png`. Typst-Nachbau liegt unter `examples/lexware_reisekosten_typst.typ`, kompiliert zu `examples/lexware_reisekosten_typst.pdf` und gerendert zu `examples/lexware_reisekosten_typst.png`. Beide Outputs sind einseitig A4. Entscheidung bewusst noch offen bis Nutzerreview.

Nach Nutzerfeedback wurde die Lexware-Vorlage anhand der 160-dpi-Referenz-PNG und `pdftotext -bbox-layout` vermessen. Die Nachbauten wurden auf die gemessenen Rasterpositionen fuer Linien/Abschnitte/Checkboxen angepasst. Urbanist ist lokal nicht installiert; beide Varianten verwenden nun Lato als verfuegbaren Naeherungsfont mit Medium fuer Labels und Bold/Heavy fuer Ueberschriften. LaTeX wurde auf LuaLaTeX + fontspec + TikZ umgestellt; der lokale Lauf benoetigte `TEXMFVAR=/tmp/texmf-var`, weil luaotfload sonst keinen schreibbaren Fontcache hatte. Typst blieb bei direkter absoluter Positionierung. Beide PDFs und PNGs wurden neu erzeugt und visuell geprueft; Entscheidung weiterhin offen bis Nutzerreview.

Entscheidung nach Nutzerreview: Typst wird als Renderer verwendet. Gruende: Source ist fuer diesen Formular-Prototyp leserlicher, die PDF-Qualitaet ist nach Vermessung sehr aehnlich zur LaTeX-Variante und Typst soll bewusst produktiv verprobt werden. Template-Ablage fuer das kuenftige Python-Tool: `src/yaml_reisekosten_tool/templates/reisekosten.typ`. Die aktuelle Datei bleibt ein statischer Prototyp; Parametrisierung aus YAML wird in einem separaten Task umgesetzt. Gerenderte Typst-Referenz liegt unter `examples/rendered/`. LaTeX bleibt als reiner Spike unter `examples/spikes/latex-renderer/` erhalten. Kein LaTeX-Fallback fuer den MVP: falls Typst spaeter technisch nicht tragfaehig ist, kann der LaTeX-Spike wieder herangezogen werden; bis dahin wird kein paralleler Fallback implementiert.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Renderer-Entscheidung getroffen: Typst wird fuer die PDF-Erzeugung verwendet. Der statische Typst-Prototyp wurde als kuenftiges Python-Package-Template unter `src/yaml_reisekosten_tool/templates/reisekosten.typ` einsortiert und aus diesem Pfad erfolgreich zu `examples/rendered/reisekosten_typst.pdf` kompiliert. LaTeX wurde als Referenz-Spike nach `examples/spikes/latex-renderer/` verschoben; ein LaTeX-Fallback wird fuer den MVP nicht eingeplant.
<!-- SECTION:FINAL_SUMMARY:END -->
