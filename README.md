# YAML Reisekosten Tool

Dieses Projekt erzeugt aus einer YAML-Datei Reisekostenabrechnungen als PDF. Das YAML-Format ist darauf ausgelegt, wiederkehrende Kundentermine mit moeglichst wenig Schreibaufwand zu erfassen.

Die geplante Modulstruktur und der Datenfluss fuer die erste Python-Implementierung sind in `ARCHITECTURE.md` festgelegt.

## Nutzung

Der Standardaufruf fuer die erste nutzbare Version ist:

```sh
yaml-reisekosten-tool foo.yml
```

Ohne Zusatzargumente liest das Werkzeug genau diese YAML-Datei und schreibt die erzeugten PDF-Dateien in das aktuelle Arbeitsverzeichnis. Die Eingabedatei wird dabei nicht veraendert.

PDF-Dateinamen werden aus Abrechnungszeitraum und Titel gebildet, zum Beispiel `2026-05-reisekosten-max-mustermann.pdf`. Wenn mehrere Abrechnungen in einer YAML-Datei erzeugt werden, erhalten sie nummerierte Suffixe wie `-01` und `-02`. Vorhandene PDFs werden standardmaessig nicht ueberschrieben; bei einer Namenskollision bricht die CLI mit einer klaren Fehlermeldung ab.

Fuer den MVP sind nur wenige Optionen vorgesehen:

- `--output-dir DIR`: PDF-Ausgabe in ein bestehendes, beschreibbares Verzeichnis schreiben.
- `--force`: Bereits vorhandene Ziel-PDFs ueberschreiben.

Fehlende Dateien, ungueltiges YAML, Schemafehler und Render-Fehler werden kurz auf stderr gemeldet und fuehren zu einem Exit-Code ungleich `0`. Details zum CLI- und Ausgabe-Kontrakt stehen in `ARCHITECTURE.md`.

## Entwicklung

Empfohlen ist eine lokale Installation in eine virtuelle Umgebung, zum Beispiel mit `uv`:

```sh
uv venv
uv pip install -e ".[dev]"
```

Alternativ funktioniert auch `python -m pip install -e ".[dev]"` in einer bereits aktivierten virtuellen Umgebung.

Lokale Pruefbefehle:

```sh
pytest
ruff check .
ruff format --check .
```

Die paketierte CLI ist nach der Installation als `yaml-reisekosten-tool` erreichbar. Der gleichwertige Modulaufruf nutzt denselben Einstieg:

```sh
python -m yaml_reisekosten_tool
```

## YAML-Format

Ein Beispiel liegt unter `examples/example.yml`.

Die Eingabedatei besteht aktuell aus diesen Bereichen:

- `abrechnung`: Titel, Zeitraum und Waehrung der Abrechnung.
- `mitarbeiter`: Angaben zur abrechnenden Person.
- `arbeitgeber`: Angaben zum Arbeitgeber aus der Reisekostenabrechnung.
- `defaults`: Wiederkehrende Werte fuer Fahrten und Auslagen.
- `unterschriften`: Optionale Angaben fuer digitale Unterschriftsfelder.
- `fahrten`: Liste der einzelnen Reisen oder Kundenfahrten.

### Defaults und Overrides

Wiederkehrende Angaben stehen unter `defaults`. Einzelne Fahrten und Auslagen erben diese Werte und ueberschreiben nur Abweichungen.

Beispiel: Wenn alle Fahrten zum selben Kunden gehen, stehen `start`, `ziel`, `anlass`, `fahrzeug`, `gesamt_km`, `startzeit` und `endzeit` unter `defaults.fahrt`. Eine einzelne Fahrt braucht dann nur noch ein `datum`. Bei Stau oder Umfahrung kann diese Fahrt `gesamt_km` ueberschreiben.

Gleiches gilt fuer Auslagen: Wiederkehrendes Parken kann unter `defaults.auslage` stehen. Eine Fahrt kann mit `auslage` nur die abweichenden Werte setzen, zum Beispiel einen anderen Betrag oder ein anderes Parkhaus.

### Felder

`abrechnung`:

- `titel`: Titel fuer das PDF.
- `zeitraum.von`: Beginn des Abrechnungszeitraums.
- `zeitraum.bis`: Ende des Abrechnungszeitraums.
- `waehrung`: Waehrung der Geldbetraege, aktuell `EUR`.

`mitarbeiter`:

- `name`: Name der abrechnenden Person.
- `personalnummer`: Optional. Wird nicht gerendert, wenn leer oder nicht vorhanden.
- `abteilung`: Optional. Wird nicht gerendert, wenn leer oder nicht vorhanden.

`arbeitgeber`:

- `name`: Name des Arbeitgebers.
- `anschrift.strasse`: Strasse und Hausnummer.
- `anschrift.plz`: Postleitzahl als String.
- `anschrift.ort`: Ort.

`defaults.fahrt` und einzelne Eintraege in `fahrten`:

- `datum`: Datum der Fahrt. Nur in `fahrten` erforderlich.
- `start`: Startort.
- `ziel`: Zielort.
- `anlass`: Anlass der Reise.
- `verkehrsmittel`: Zum Beispiel `privater_pkw`.
- `fahrzeug.kennzeichen`: Optionales Kennzeichen.
- `fahrzeug.beschreibung`: Optionale Fahrzeugbeschreibung.
- `gesamt_km`: Tatsaechlich gefahrene Gesamtstrecke, nicht einfache Entfernung.
- `startzeit`: Uhrzeit als String im Format `HH:MM`.
- `endzeit`: Uhrzeit als String im Format `HH:MM`.
- `notiz`: Optionaler Hinweis fuer Sonderfaelle.
- `auslage`: Optionale Auslage direkt an einer Fahrt.

`defaults.auslage` und `auslage` an einer Fahrt:

- `art`: Art der Auslage, zum Beispiel `parken`.
- `betrag_eur`: Betrag in Euro.
- `beschreibung`: Beschreibung der Auslage.
- `beleg`: Optionaler Pfad zu einem Beleg.

`unterschriften`:

- `antragsteller.ort`: Optionaler Ort fuer die digitale Antragstellerzeile.
- `antragsteller.datum`: Optionales Datum im Format `YYYY-MM-DD`. Ohne Angabe wird das Ende des Abrechnungszeitraums gerendert.
- `antragsteller.name`: Optionaler Name. Ohne Angabe wird `mitarbeiter.name` gerendert.
- `antragsteller.unterschrift`: Optionaler Pfad zu einer Unterschrift als PNG, JPG oder JPEG.
- `vorgesetzter.ort`: Optionaler Ort fuer die digitale Vorgesetztenzeile.
- `vorgesetzter.datum`: Optionales Datum im Format `YYYY-MM-DD`.
- `vorgesetzter.name`: Optionaler Name.
- `vorgesetzter.unterschrift`: Optionaler Pfad zu einer Unterschrift als PNG, JPG oder JPEG.

## Entscheidungen

Es gibt keine automatische Verknuepfung zwischen `arbeitgeber` und `defaults.fahrt.ziel`. Der Arbeitgeber ist ein Feld der Abrechnung; das Fahrtziel ist eine explizite Eingabe.

`gesamt_km` meint immer die tatsaechlich gefahrene Gesamtstrecke. Hin- und Rueckweg werden nicht automatisch aus einer einfachen Entfernung verdoppelt, weil Umwege, Einbahnstrassen oder Stauumfahrungen sonst falsch abgebildet werden koennen.

Uhrzeiten bleiben Strings im Format `HH:MM`, damit YAML sie nicht als Sondertyp interpretiert.

Kilometerpauschalen werden nicht im YAML gepflegt. Die Software soll eine interne Jahrestabelle anhand des Reisedatums verwenden.

Verpflegungspauschalen werden ebenfalls nicht im YAML gepflegt. Die Software soll sie aus Datum, Startzeit, Endzeit und den fuer das Kalenderjahr geltenden Regeln ermitteln.

## Berechnungsregeln

Die erste Berechnungsschicht verwendet interne Jahrestabellen. Fuer den MVP ist 2026 hinterlegt; fuer nicht hinterlegte Jahre bricht die Berechnung mit einem fachlichen Fehler ab, statt still falsche Werte zu verwenden.

Fuer `verkehrsmittel: privater_pkw` gilt 2026 eine Kilometerpauschale von `0.30 EUR` pro tatsaechlich gefahrenem Kilometer. Die Berechnung nutzt `gesamt_km`, also die Gesamtstrecke inklusive Hin- und Rueckweg, und rundet Geldwerte kaufmaennisch auf Cent.

Fuer eintagige Inlandsfahrten gilt 2026 eine Verpflegungspauschale von `14.00 EUR`, wenn die Abwesenheit mehr als acht Stunden betraegt. Der Grenzfall ist strikt: Genau `08:00` Stunden Abwesenheit ergeben keine Verpflegungspauschale; erst `08:01` Stunden ergeben `14.00 EUR`. Fuer 24 Stunden waeren `28.00 EUR` hinterlegt, auch wenn mehrtaegige Reisen im YAML-MVP noch nicht modelliert sind.

Auslagen an Fahrten werden separat als Auslagenpositionen gehalten und zusaetzlich in die Gesamtsumme uebernommen.

## Architektur

Siehe `ARCHITECTURE.md` fuer den geplanten Zuschnitt von CLI, YAML-I/O, Validierung, Normalisierung, Berechnung und Typst-Rendering.

## Lizenzhinweis

Der Projektcode steht unter der Lizenz in `LICENSE`. Diese Projektlizenz gilt nicht fuer die originale Lexware-Vorlage bzw. Lexware-Referenzdateien unter `examples/`; diese bleiben urheberrechtlich Lexware zugeordnet.
