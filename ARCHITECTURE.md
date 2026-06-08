# Architektur

Dieses Dokument legt die erste Implementierungsarchitektur fuer das Python-Projekt fest. Ziel ist ein kleines, testbares Kommandozeilenwerkzeug: YAML laden, validieren und normalisieren, ein Abrechnungsmodell bilden und daraus per Typst ein PDF erzeugen.

## Zielbild fuer den MVP

Der MVP bleibt bewusst linear:

1. CLI nimmt Eingabe- und Ausgabepfad entgegen.
2. YAML wird sicher geladen.
3. Defaults aus der Eingabe werden auf Fahrten und Auslagen angewendet.
4. Die normalisierten Daten werden in Python-Domain-Objekte ueberfuehrt.
5. Pauschalen und Summen werden anhand interner Regeln berechnet.
6. Ein Typst-Template wird mit den berechneten Daten gerendert.
7. Je Fahrt wird ein Lexware-konformes PDF an den gewuenschten Ausgabepfad geschrieben.

Die Lexware-Vorlage modelliert ein einzelnes Reisekostenformular mit Reisebeginn und Reiseende, aber keine Fahrtenliste. Deshalb entspricht im MVP jeder Eintrag unter `fahrten` einer eigenen Reise und wird als eigenes PDF gerendert.

Es gibt keine Datenbank, keine Web- oder GUI-Schicht und keine parallele Renderer-Abstraktion. Typst ist der Renderer fuer den MVP.

## Vorgesehene Module

Die Implementierung soll unter `src/yaml_reisekosten_tool/` wachsen. Die folgenden Module sind der vorgesehene Zuschnitt fuer die ersten Code-Tasks:

- `cli.py`: Argumente parsen, Eingabe-/Ausgabepfade pruefen, Hauptablauf starten und Exit-Codes setzen.
- `yaml_io.py`: YAML-Datei lesen, `safe_load` verwenden und reine Ladefehler von fachlicher Validierung trennen.
- `models.py`: Domain-Dataclasses fuer Abrechnung, Mitarbeiter, Arbeitgeber, Fahrzeug, Fahrt, Auslage und berechnete Abrechnung.
- `validation.py`: Pflichtfelder, Typen, Wertebereiche und fachliche Konsistenz pruefen.
- `normalization.py`: Defaults und Overrides anwenden, Datums-/Zeit-/Geldwerte in stabile Python-Typen ueberfuehren.
- `rates.py`: Interne Jahrestabellen und Regeln fuer Kilometer- und Verpflegungspauschalen.
- `calculation.py`: Fahrtkosten, Verpflegungsmehraufwand, Auslagen und Gesamtsummen berechnen.
- `rendering.py`: Render-Kontext fuer Typst bauen, Template-Datei finden und `typst compile` ausfuehren.
- `templates/`: Typst-Templates als Package-Daten, aktuell `templates/reisekosten.typ`.

`__main__.py` kann spaeter ergaenzt werden, damit `python -m yaml_reisekosten_tool` denselben Einstieg wie die CLI nutzt. Ein separates `app.py` oder Service-Layer ist fuer den MVP nicht noetig; die CLI darf den linearen Ablauf direkt orchestrieren.

## Datenfluss

Der Datenfluss ist absichtlich eine Pipeline mit klaren Fehlergrenzen:

1. `cli.py` ermittelt `input.yml` und die PDF-Ausgabepfade.
2. `yaml_io.py` liest die Datei und liefert ein rohes Mapping.
3. `validation.py` prueft die grobe Struktur und meldet fehlende oder unerwartete Felder.
4. `normalization.py` merged `defaults.fahrt` und `defaults.auslage` in die einzelnen Eintraege.
5. `normalization.py` wandelt Datumswerte, Uhrzeiten und Geldbetraege in stabile Python-Werte um.
6. `models.py` nimmt die normalisierten Daten als Dataclasses auf.
7. `rates.py` liefert die fuer das Reisedatum gueltigen Pauschalwerte.
8. `calculation.py` bildet aus Domain-Modell und Pauschalen die berechnete Abrechnung.
9. `cli.py` teilt die berechnete Abrechnung in einzelne Render-Abrechnungen pro Fahrt auf.
10. `rendering.py` uebersetzt jede einzelne Render-Abrechnung in einen Typst-Render-Kontext.
11. `rendering.py` ruft Typst auf und schreibt die PDFs.

Die Pipeline soll in Tests stufenweise pruefbar sein. Besonders wichtig sind Tests fuer Default/Override-Verhalten, Datums- und Uhrzeitnormalisierung, Summenbildung und die Parameter, mit denen Typst aufgerufen wird.

## Fehlerpunkte

Fehler sollen moeglichst frueh und mit klarer Ursache gemeldet werden:

- Dateisystem: Eingabedatei fehlt, ist nicht lesbar oder Ausgabeverzeichnis ist nicht beschreibbar.
- YAML-Syntax: Datei ist kein gueltiges YAML oder `safe_load` liefert kein Mapping.
- Schema: Pflichtbereiche wie `abrechnung`, `mitarbeiter`, `arbeitgeber` oder `fahrten` fehlen.
- Feldwerte: Datum, Uhrzeit, Geldbetrag, Kilometer oder Waehrung haben ein unerwartetes Format.
- Defaults: Ein Fahrt- oder Auslagen-Eintrag bleibt nach Default-Anwendung unvollstaendig.
- Fachlogik: Reisedatum liegt ausserhalb vorhandener Pauschalentabellen oder Zeiten ergeben keine plausible Dauer.
- Rendering: Typst ist nicht installiert, das Template fehlt oder `typst compile` bricht ab.
- Ausgabe: PDF kann nicht geschrieben werden oder ein vorhandener Zielpfad darf nicht ueberschrieben werden.

Die CLI soll diese Fehler spaeter in lesbare Meldungen und nicht in rohe Tracebacks uebersetzen. Interne Exceptions duerfen trotzdem spezifisch bleiben, damit Tests sie eindeutig pruefen koennen.

## CLI- und Ausgabe-Kontrakt

Der erste nutzbare CLI-Einstieg ist bewusst klein:

```sh
yaml-reisekosten-tool foo.yml
```

Der Aufruf nimmt genau eine YAML-Datei als Eingabe. Ohne weitere Optionen schreibt das Werkzeug die erzeugten PDF-Dateien und eine Markdown-Zusammenfassung in das aktuelle Arbeitsverzeichnis, also in das Verzeichnis, aus dem der Befehl gestartet wurde. Die Eingabedatei wird nie veraendert. Im Erfolgsfall soll die CLI die erzeugten PDF-Pfade und danach den Pfad der Markdown-Zusammenfassung ausgeben und keinen weiteren Arbeitsmuell im aktuellen Verzeichnis hinterlassen.

Im aktuellen YAML-MVP erzeugt eine YAML-Datei eine fachliche Eingabe mit einer Liste einzelner Reisen. Jede Fahrt wird in ein eigenes Lexware-Formular gerendert, damit Reisebeginn und Reiseende immer eine einzelne Reise beschreiben. Bei mehreren Fahrten gibt die CLI mehrere PDF-Pfade aus. Die Markdown-Zusammenfassung ist eine interne Kontrollausgabe mit Einzelbetraegen und Gesamtbetrag ueber alle erzeugten PDFs; sie ist bewusst nicht Teil der Lexware-Form.

### PDF-Dateinamen

Dateinamen sollen stabil, lesbar und shell-freundlich sein:

- Basis ist ein Slug aus Fahrtdatum und Abrechnungstitel, zum Beispiel `2026-05-04_reisekosten_max-mustermann.pdf`. Bei mehrtaegigen Reisen wird der Starttag verwendet.
- Wenn kein brauchbarer Titel vorhanden ist, wird der Basisname der Eingabedatei verwendet, zum Beispiel `foo.pdf`.
- Slugs verwenden Kleinbuchstaben, ASCII-Umschreibungen, Bindestriche statt Leerzeichen und keine Sonderzeichen, die auf ueblichen Dateisystemen Probleme machen.
- Bei mehreren Fahrten an unterschiedlichen Tagen reicht das vorangestellte Fahrtdatum zur Unterscheidung. Nur wenn mehrere Fahrten denselben Tag und denselben Basisnamen haben, bekommen die spaeteren PDF-Dateien einen eindeutigen Suffix, zum Beispiel `2026-05-04_reisekosten_max-mustermann.pdf` und `2026-05-04_reisekosten_max-mustermann-02.pdf`.
- Die Markdown-Zusammenfassung nutzt denselben Zeitraum-/Titel-Basisnamen mit `_zusammenfassung.md`, zum Beispiel `2026-05_reisekosten_max-mustermann_zusammenfassung.md`.
- Eine vorhandene Ausgabedatei wird standardmaessig nicht ueberschrieben. Bei Namenskollision bricht die CLI mit einer klaren Fehlermeldung ab und nennt den betroffenen Zielpfad.
- Automatische Suffixe zur Kollisionsvermeidung wie `-2` werden nicht stillschweigend vergeben, weil wiederholte Abrechnungslaeufe sonst unbemerkt alte und neue Ergebnisse mischen koennen.

### Fehlerverhalten

Alle erwartbaren Fehler werden als kurze, nutzbare Meldung auf stderr ausgegeben. Der Prozess endet dann mit einem Exit-Code ungleich `0`; rohe Python-Tracebacks erscheinen nur in einem spaeteren Debug-Modus oder bei unerwarteten Programmierfehlern.

- Fehlende oder nicht lesbare Eingabedatei: Abbruch vor YAML-Verarbeitung, Meldung nennt den Pfad.
- Ungueltiges YAML oder leere Datei: Abbruch mit YAML-/Ladefehler und Pfad.
- Ungueltige Struktur oder Feldwerte: Abbruch mit Feldpfad, Problem und nach Moeglichkeit erwartetem Format, zum Beispiel `fahrten[3].datum`.
- Fachliche Fehler: Abbruch mit konkreter Ursache, etwa fehlende Pauschalentabelle fuer ein Jahr oder unplausible Zeiten.
- Render-Fehler: Abbruch mit Hinweis auf Typst, Template oder Render-Ausgabe; falls Typst fehlt, nennt die Meldung die fehlende Runtime.
- Ausgabekollision oder nicht beschreibbares Ausgabeverzeichnis: Abbruch vor dem Rendern oder vor dem finalen Schreiben, ohne vorhandene Ausgabedateien zu veraendern.

### Optionale CLI-Argumente im MVP

Fuer die erste Version werden nur Optionen aufgenommen, die den einfachen Standardaufruf nicht verkomplizieren:

- `--output-dir DIR`: Schreibt die PDF-Dateien in `DIR` statt in das aktuelle Arbeitsverzeichnis. Das Verzeichnis muss existieren und beschreibbar sein.
- `--force`: Erlaubt das Ueberschreiben bereits vorhandener PDFs und Markdown-Zusammenfassungen. Ohne diese Option ist Ueberschreiben verboten.

Bewusst nicht Teil des MVP sind interaktive Prompts, Konfigurationsdateien, Batch-Verzeichnisse als Eingabe, mehrere Renderer, JSON-Logging, Watch-Modus, Dry-Run, Auswahl einzelner Abrechnungen und ein frei waehlbarer einzelner Output-Dateiname. Diese Optionen koennen spaeter als eigene Produktentscheidungen ergaenzt werden, wenn die einfache Pipeline stabil ist.

## Bewusst ausgelassener Scope

Folgender Scope wird fuer die erste Architektur bewusst nicht eingeplant:

- Kein Webframework, keine REST-API und keine GUI.
- Keine Datenbank und keine persistente Historie von Abrechnungen.
- Kein Plugin-System fuer Renderer oder Pauschalen.
- Kein LaTeX-Fallback parallel zu Typst.
- Keine automatische Belegverarbeitung oder OCR.
- Keine Online-Abfrage gesetzlicher Pauschalen.
- Keine komplexe Formular-Engine fuer beliebige PDF-Vorlagen.
- Keine Mehrmandanten- oder Benutzerverwaltung.

Diese Entscheidungen halten die erste Implementierung klein. Wenn spaeter Bedarf entsteht, koennen die genannten Punkte als eigene Tasks bewertet werden.

## Hinweise fuer erste Tests

Der Projektstart kann mit fokussierten Unit-Tests erfolgen:

- `yaml_io.py`: gueltige Datei laden, YAML-Syntaxfehler abfangen, leere Datei erkennen.
- `normalization.py`: Fahrtdefaults anwenden, einzelne Overrides respektieren, Auslagendefaults anwenden.
- `validation.py`: fehlende Pflichtfelder und fehlerhafte Datums-/Zeitformate melden.
- `calculation.py`: Kilometerkosten, Verpflegungspauschalen, Auslagen und Gesamtsumme berechnen.
- `rendering.py`: Template-Pfad und Typst-Aufruf mit einem gefakten `subprocess` pruefen.

Integrationstests koennen spaeter `examples/example.yml` durch die Pipeline schicken und, sofern Typst installiert ist, ein PDF erzeugen.
