// Data-driven Typst template for yaml-reisekosten-tool.

#let data = json(sys.inputs.data)
#let abrechnung = data.at("abrechnung")
#let mitarbeiter = data.at("mitarbeiter")
#let arbeitgeber = data.at("arbeitgeber")
#let reise = data.at("reise")
#let kosten = data.at("kosten")
#let unterschriften = data.at("unterschriften")
#let antragsteller = unterschriften.at("antragsteller")
#let vorgesetzter = unterschriften.at("vorgesetzter")

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
#let filled-field(x, y, w, body, value) = {
  place(top + left, dx: x, dy: y)[#line(length: w, stroke: 0.55pt)]
  place(top + left, dx: x, dy: y - 4.6mm)[
    #text(size: 8.8pt, weight: "medium")[#value]
  ]
  label(x, y + 2mm, body)
}
#let compact-filled-field(x, y, w, body, value) = {
  place(top + left, dx: x, dy: y)[#line(length: w, stroke: 0.55pt)]
  place(top + left, dx: x, dy: y - 4.6mm)[
    #box(width: w, clip: true)[#text(size: 7.4pt, weight: "medium")[#value]]
  ]
  label(x, y + 2mm, body)
}
#let checkbox(x, y, body) = {
  place(top + left, dx: x, dy: y)[#rect(width: 3mm, height: 3mm, stroke: red + 0.55pt)]
  place(top + left, dx: x + 5.8mm, dy: y - 0.1mm)[#text(size: 8.8pt, weight: "medium")[#body]]
}
#let checked-checkbox(x, y, body, checked) = {
  checkbox(x, y, body)
  if checked {
    place(top + left, dx: x + 0.55mm, dy: y - 0.3mm)[#text(size: 8pt, fill: red)[x]]
  }
}
#let radio(x, y, body) = {
  place(top + left, dx: x, dy: y)[#circle(radius: 1.5mm, stroke: red + 0.55pt)]
  place(top + left, dx: x + 5.8mm, dy: y - 1.4mm)[#text(size: 8.8pt, weight: "medium")[#body]]
}
#let selected-radio(x, y, body, selected) = {
  radio(x, y, body)
  if selected {
    place(top + left, dx: x, dy: y)[#circle(radius: 0.85mm, fill: red)]
  }
}
#let signature-field(x, y, w, body, signature) = {
  let meta = (signature.at("ort"), signature.at("datum"), signature.at("name"))
    .filter(item => item != "")
    .join(", ")
  place(top + left, dx: x, dy: y)[#line(length: w, stroke: 0.55pt)]
  place(top + left, dx: x, dy: y - 5.2mm)[
    #text(size: 8.4pt, weight: "medium")[#meta]
  ]
  if signature.at("unterschrift_asset") != "" {
    place(top + left, dx: x + w - 62mm, dy: y - 14mm)[
      #image(signature.at("unterschrift_asset"), width: 58mm, fit: "contain")
    ]
  }
  label(x, y + 2mm, body)
}

#place(top + left, dx: 15mm, dy: 13.1mm)[
  #text(size: 22.7pt, weight: "bold")[Reisekostenabrechnung]
]
#place(top + left, dx: 178.9mm, dy: 18.3mm)[
  #text(size: 6.7pt, weight: "bold")[(Stand 01.2026)]
]

#section(15mm, 30.9mm, [Mitarbeiterdaten])
#filled-field(15mm, 44.5mm, 83.8mm, [Name d. Arbeitgebers], arbeitgeber.at("name"))
#filled-field(111.1mm, 44.5mm, 84mm, [Anschrift d. Arbeitgebers], arbeitgeber.at("anschrift"))
#filled-field(15mm, 57.2mm, 83.8mm, [Vorname], mitarbeiter.at("vorname"))
#filled-field(111.1mm, 57.2mm, 84mm, [Nachname], mitarbeiter.at("nachname"))
#filled-field(15mm, 69.9mm, 83.8mm, [Personalnummer], mitarbeiter.at("personalnummer"))
#filled-field(111.1mm, 69.9mm, 84mm, [Abteilung], mitarbeiter.at("abteilung"))

#section(15mm, 85.9mm, [Reisedaten])
#selected-radio(16.5mm, 101.5mm, [Inlandsreise], true)
#radio(45.9mm, 101.5mm, [Auslandsreise])
#filled-field(15mm, 112.3mm, 33.7mm, [Reisebeginn (Datum)], reise.at("beginn_datum"))
#filled-field(61mm, 112.3mm, 33.7mm, [Reisebeginn (Uhrzeit)], reise.at("beginn_uhrzeit"))
#filled-field(106.8mm, 112.3mm, 37.9mm, [Reiseende (Datum)], reise.at("ende_datum"))
#filled-field(157.2mm, 112.3mm, 37.9mm, [Reiseende (Uhrzeit)], reise.at("ende_uhrzeit"))
#filled-field(15mm, 125mm, 180.2mm, [Reiseziel(e)], reise.at("ziele"))
#filled-field(15mm, 137.7mm, 180.2mm, [Anlass der Reise], reise.at("anlaesse"))
#checkbox(15mm, 150.8mm, [Dienstwagen])
#checked-checkbox(49.4mm, 150.8mm, [Privater PKW], reise.at("privater_pkw"))
#checkbox(83.3mm, 150.8mm, [Bahn])
#checkbox(107.2mm, 150.8mm, [Flugzeug])
#checkbox(136.2mm, 150.8mm, [Sonstiges:])
#place(top + left, dx: 157.2mm, dy: 153.2mm)[#line(length: 37.9mm, stroke: 0.55pt)]
#place(top + left, dx: 157.2mm, dy: 148.6mm)[
  #text(size: 8.8pt, weight: "medium")[#reise.at("fahrzeug")]
]

#section(15mm, 166.3mm, [Kosten])
#filled-field(15mm, 180mm, 180.2mm, [Fahrtkosten], kosten.at("fahrtkosten") + " EUR")
#place(top + left, dx: 15mm, dy: 191.2mm)[
  #text(size: 8.3pt, weight: "medium")[Verpflegungsmehraufwand:] \
  #text(size: 7.4pt, weight: "medium")[(8-24 Std. / An- & Abreise)]
]
#place(top + left, dx: 56.2mm, dy: 195.2mm)[#line(length: 19.8mm, stroke: 0.55pt)]
#place(top + left, dx: 56.2mm, dy: 191mm)[#text(size: 8.8pt)[#str(kosten.at("verpflegung_tage_acht_bis_vierundzwanzig"))]]
#label(56.2mm, 197.9mm, [Tage])
#place(top + left, dx: 80.3mm, dy: 195.2mm)[#line(length: 19.7mm, stroke: 0.55pt)]
#place(top + left, dx: 80.3mm, dy: 191mm)[#text(size: 8.8pt)[#kosten.at("verpflegung")]]
#place(top + left, dx: 97.4mm, dy: 191.2mm)[#text(size: 8.3pt, weight: "medium")[€]]
#label(80.3mm, 197.9mm, [pro Tag])
#place(top + left, dx: 109.6mm, dy: 191.2mm)[
  #text(size: 8.3pt, weight: "medium")[Verpflegungsmehraufwand:] \
  #text(size: 7.4pt, weight: "medium")[(ab 24 Std.)]
]
#place(top + left, dx: 151.3mm, dy: 195.2mm)[#line(length: 19.8mm, stroke: 0.55pt)]
#place(top + left, dx: 151.3mm, dy: 191mm)[#text(size: 8.8pt)[#str(kosten.at("verpflegung_tage_vierundzwanzig"))]]
#label(151.3mm, 197.9mm, [Tage])
#place(top + left, dx: 175.3mm, dy: 195.2mm)[#line(length: 19.8mm, stroke: 0.55pt)]
#place(top + left, dx: 175.3mm, dy: 191mm)[#text(size: 8.8pt)[0,00]]
#place(top + left, dx: 192.6mm, dy: 191.2mm)[#text(size: 8.3pt, weight: "medium")[€]]
#label(175.3mm, 197.9mm, [pro Tag])
#field(15mm, 209.6mm, 180.2mm, [Abzüge für Frühstück, Mittag- oder Abendessen])
#field(15mm, 222.3mm, 83.8mm, [Übernachtungskosten])
#compact-filled-field(111.1mm, 222.3mm, 84mm, [Reisenebenkosten], kosten.at("reisenebenkosten"))
#filled-field(15mm, 235mm, 180.2mm, [Gesamtkosten], kosten.at("gesamt") + " EUR")

#signature-field(15mm, 256.2mm, 180.2mm, [Ort, Datum, Name und Unterschrift Antragsteller], antragsteller)
#signature-field(15mm, 268.9mm, 180.2mm, [Ort, Datum, Name und Unterschrift Vorgesetzter], vorgesetzter)
#place(top + left, dx: 152mm, dy: 280.1mm)[
  #text(size: 6.3pt, weight: "medium")[erstellt mit yaml-reisekosten-tool by cubigato]
]
