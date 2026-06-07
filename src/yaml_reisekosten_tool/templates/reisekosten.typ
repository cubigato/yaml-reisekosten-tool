// Static Typst prototype based on the Lexware reference.
// Turning this into a data-driven template is tracked separately.

#set page(
  paper: "a4",
  margin: 0mm,
)
#set text(font: "Lato", size: 8.3pt, weight: "medium")

#let red = rgb("#ff3850")
#let section(x, y, body) = place(top + left, dx: x, dy: y)[
  #text(size: 12.2pt, weight: "bold")[#body]
]
#let label(x, y, body) = place(top + left, dx: x, dy: y)[
  #text(size: 8.3pt, weight: "medium")[#body]
]
#let field(x, y, w, body) = {
  place(top + left, dx: x, dy: y)[#line(length: w, stroke: 0.55pt)]
  label(x, y + 2mm, body)
}
#let checkbox(x, y, body) = {
  place(top + left, dx: x, dy: y)[#rect(width: 3mm, height: 3mm, stroke: red + 0.55pt)]
  place(top + left, dx: x + 5.8mm, dy: y - 0.1mm)[#text(size: 8.8pt, weight: "medium")[#body]]
}
#let radio(x, y, body) = {
  place(top + left, dx: x, dy: y)[#circle(radius: 1.5mm, stroke: red + 0.55pt)]
  place(top + left, dx: x + 5.8mm, dy: y - 1.4mm)[#text(size: 8.8pt, weight: "medium")[#body]]
}

#place(top + left, dx: 15mm, dy: 13.1mm)[
  #text(size: 22.7pt, weight: "bold")[Reisekostenabrechnung]
]
#place(top + left, dx: 178.9mm, dy: 18.3mm)[
  #text(size: 6.7pt, weight: "bold")[(Stand 01.2026)]
]

#section(15mm, 30.9mm, [Mitarbeiterdaten])
#field(15mm, 44.5mm, 83.8mm, [Name d. Arbeitgebers])
#field(111.1mm, 44.5mm, 84mm, [Anschrift d. Arbeitgebers])
#field(15mm, 57.2mm, 83.8mm, [Vorname])
#field(111.1mm, 57.2mm, 84mm, [Nachname])
#field(15mm, 69.9mm, 83.8mm, [Personalnummer])
#field(111.1mm, 69.9mm, 84mm, [Abteilung])

#section(15mm, 85.9mm, [Reisedaten])
#radio(16.5mm, 101.5mm, [Inlandsreise])
#radio(45.9mm, 101.5mm, [Auslandsreise])
#field(15mm, 112.3mm, 33.7mm, [Reisebeginn (Datum)])
#field(61mm, 112.3mm, 33.7mm, [Reisebeginn (Uhrzeit)])
#field(106.8mm, 112.3mm, 37.9mm, [Reiseende (Datum)])
#field(157.2mm, 112.3mm, 37.9mm, [Reiseende (Uhrzeit)])
#field(15mm, 125mm, 180.2mm, [Reiseziel(e)])
#field(15mm, 137.7mm, 180.2mm, [Anlass der Reise])
#checkbox(15mm, 150.8mm, [Dienstwagen])
#checkbox(49.4mm, 150.8mm, [Privater PKW])
#checkbox(83.3mm, 150.8mm, [Bahn])
#checkbox(107.2mm, 150.8mm, [Flugzeug])
#checkbox(136.2mm, 150.8mm, [Sonstiges:])
#place(top + left, dx: 157.2mm, dy: 153.2mm)[#line(length: 37.9mm, stroke: 0.55pt)]

#section(15mm, 166.3mm, [Kosten])
#field(15mm, 180mm, 180.2mm, [Fahrtkosten])
#place(top + left, dx: 15mm, dy: 191.2mm)[
  #text(size: 8.3pt, weight: "medium")[Verpflegungsmehraufwand:] \
  #text(size: 7.4pt, weight: "medium")[(8-24 Std. / An- & Abreise)]
]
#place(top + left, dx: 56.2mm, dy: 195.2mm)[#line(length: 19.8mm, stroke: 0.55pt)]
#label(56.2mm, 197.9mm, [Tage])
#place(top + left, dx: 80.3mm, dy: 195.2mm)[#line(length: 19.7mm, stroke: 0.55pt)]
#place(top + left, dx: 97.4mm, dy: 191.2mm)[#text(size: 8.3pt, weight: "medium")[€]]
#label(80.3mm, 197.9mm, [pro Tag])
#place(top + left, dx: 109.6mm, dy: 191.2mm)[
  #text(size: 8.3pt, weight: "medium")[Verpflegungsmehraufwand:] \
  #text(size: 7.4pt, weight: "medium")[(ab 24 Std.)]
]
#place(top + left, dx: 151.3mm, dy: 195.2mm)[#line(length: 19.8mm, stroke: 0.55pt)]
#label(151.3mm, 197.9mm, [Tage])
#place(top + left, dx: 175.3mm, dy: 195.2mm)[#line(length: 19.8mm, stroke: 0.55pt)]
#place(top + left, dx: 192.6mm, dy: 191.2mm)[#text(size: 8.3pt, weight: "medium")[€]]
#label(175.3mm, 197.9mm, [pro Tag])
#field(15mm, 209.6mm, 180.2mm, [Abzüge für Frühstück, Mittag- oder Abendessen])
#field(15mm, 222.3mm, 83.8mm, [Übernachtungskosten])
#field(111.1mm, 222.3mm, 84mm, [Reisenebenkosten])
#field(15mm, 235mm, 180.2mm, [Gesamtkosten])

#field(15mm, 256.2mm, 62.9mm, [Ort, Datum Antragsteller])
#field(83.5mm, 256.2mm, 111.6mm, [Unterschrift Antragsteller])
#field(15mm, 268.9mm, 62.9mm, [Ort, Datum Vorgesetzter])
#field(83.5mm, 268.9mm, 111.6mm, [Unterschrift Vorgesetzter])
#place(top + left, dx: 152mm, dy: 280.1mm)[
  #text(size: 6.3pt, weight: "medium")[Diese Vorlage wurde erstellt von]
]
#place(top + left, dx: 187mm, dy: 280.1mm)[
  #text(size: 6.3pt, weight: "bold", fill: red)[Lexware]
]
