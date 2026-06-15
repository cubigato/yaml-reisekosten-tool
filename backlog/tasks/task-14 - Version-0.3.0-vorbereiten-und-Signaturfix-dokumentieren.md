---
id: TASK-14
title: Version 0.3.0 vorbereiten und Signaturfix dokumentieren
status: Done
assignee:
  - codex
created_date: '2026-06-15 10:42'
updated_date: '2026-06-15 10:47'
labels:
  - release
  - documentation
dependencies: []
documentation:
  - CHANGELOG.md
  - README.md
  - ARCHITECTURE.md
modified_files:
  - pyproject.toml
  - CHANGELOG.md
  - .gitignore
priority: medium
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Den abgeschlossenen Signaturlayout-Fix als Minor-Release vorbereiten. Dazu gehören eine konsistente Versionsanhebung, ein vollständiger Changelog-Eintrag für bisher undokumentierte Änderungen seit dem letzten Release sowie das Entfernen beziehungsweise Ignorieren lokaler Render-Artefakte.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Die Projektversion ist konsistent von 0.2.0 auf 0.3.0 angehoben
- [x] #2 Der Changelog dokumentiert den Signaturlayout-Fix und weitere seit 0.2.0 fehlende nutzerrelevante Änderungen
- [x] #3 Generierte lokale Beispielausgaben werden nicht als Release-Dateien geführt
- [x] #4 Tests, Linting, Formatprüfung und Paket-Build sind erfolgreich
- [x] #5 Der Release-Arbeitsstand enthält nur beabsichtigte Quell-, Test-, Dokumentations- und Backlog-Änderungen
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Bestehenden Changelog, Paketmetadaten, Lockfile und Ignore-Regeln prüfen. 2. Version auf 0.3.0 an allen maßgeblichen Stellen anheben. 3. Changelog aus den Änderungen seit dem dokumentierten 0.2.0-Stand ergänzen, einschließlich getrennter Fahrt-PDFs, Reisenebenkosten und korrigiertem Signaturlayout. 4. Lokale Render-Ausgaben entfernen und dauerhaft ignorieren, sofern dies zur bestehenden Repository-Struktur passt. 5. Tests, Ruff, Paket-Build und Metadaten des gebauten Artefakts prüfen. 6. Arbeitsbaum kontrollieren und Ticket abschließen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Der Auftraggeber hat Versionserhöhung, Changelog-Pflege, Aufräumen und direkten Abschluss ausdrücklich beauftragt.

Version in `pyproject.toml` auf 0.3.0 angehoben. Changelog um die nutzerrelevanten Änderungen seit 0.2.0 ergänzt. Lokale Render-Ausgaben entfernt und `examples/output/` sowie übliche Build-Artefakte in `.gitignore` aufgenommen.

Das optionale Modul `build` ist in der Projekt-Venv nicht installiert; der Paket-Build wird mit dem vorhandenen `uv build` durchgeführt.

Paket-Build mit `uv build` erfolgreich: Wheel und Source-Distribution tragen Version 0.3.0. Die Source-Distribution schließt interne Backlog-/Agent-Dateien und historische Render-/Spike-Artefakte aus.

Die lokale editable Installation wurde von veralteten Metadaten 0.1.0 auf 0.3.0 aktualisiert. CLI-Hilfe funktioniert.

Abschlussprüfung: 55 Tests bestanden; Ruff-Lint und Formatprüfung bestanden; `git diff --check` ohne Befund; `dist/` und `examples/output/` entfernt. Der Arbeitsbaum enthält ausschließlich die beabsichtigten Release-, Signaturfix-, Test- und Backlog-Änderungen.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Version 0.3.0 ist vorbereitet. `pyproject.toml` wurde von 0.2.0 auf 0.3.0 angehoben und der Changelog dokumentiert Einzelfahrt-PDFs, Markdown-Zusammenfassung, stabile Dateinamen, digitale Unterschriften, Reisenebenkosten-Beschreibungen sowie den korrigierten Signaturbereich. Generierte Ausgabe- und Build-Verzeichnisse werden ignoriert; lokale Render-Ausgaben wurden entfernt. Die Source-Distribution wurde zusätzlich von internen Backlog-/Agent-Dateien und historischen Render-/LaTeX-Artefakten bereinigt. Wheel und Source-Distribution wurden erfolgreich gebaut und als Version 0.3.0 geprüft. Verifikation: 55 Pytest-Tests, Ruff-Lint, Ruff-Formatprüfung und `git diff --check` erfolgreich.
<!-- SECTION:FINAL_SUMMARY:END -->
