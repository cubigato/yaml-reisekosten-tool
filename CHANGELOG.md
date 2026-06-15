# Changelog

Alle nennenswerten Aenderungen an diesem Projekt werden in dieser Datei dokumentiert.

## 0.3.0 - 2026-06-15

### Hinzugefuegt

- Je Fahrt wird ein eigenes Lexware-konformes PDF erzeugt.
- Zusaetzliche Markdown-Zusammenfassung mit Einzelbetraegen und Gesamtsumme.
- Stabile, datumsbasierte PDF-Dateinamen mit eindeutigen Suffixen fuer Fahrten am selben Tag.
- Digitale Unterschriften fuer Antragsteller und Vorgesetzten aus PNG-, JPG- oder JPEG-Dateien.
- Reisenebenkosten zeigen neben dem Betrag auch die normalisierte Beschreibung der Auslage.

### Geaendert

- Breite Unterschriftsbilder werden proportional in einem begrenzten Bereich dargestellt und
  eindeutig der jeweiligen Unterschriftszeile zugeordnet.
- Vorhandene Ausgabedateien werden nur noch mit `--force` ueberschrieben.

### Behoben

- Antragsteller- und Vorgesetztenunterschriften ueberlappen sich nicht mehr und ragen nicht mehr
  in den Footer oder ueber den Seitenrand hinaus.

## 0.2.0 - 2026-06-08

Erstes faktisches Release des YAML Reisekosten Tools.

### Enthalten

- CLI zum Erzeugen von Reisekostenabrechnungen als PDF aus YAML-Dateien.
- YAML-Laden, Validierung, Normalisierung, Defaults und Overrides.
- Berechnung von Kilometerkosten, Verpflegungspauschalen und Auslagen fuer 2026.
- Typst-Rendering mit paketiertem Template.
- Beispiel-YAMLs fuer Hauptfall, Minimalfall, Auslagen/Overrides und Verpflegungsgrenzfaelle.
