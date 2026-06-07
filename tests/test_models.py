from __future__ import annotations

from datetime import date, time
from decimal import Decimal
from pathlib import Path

from yaml_reisekosten_tool.models import ReisekostenEingabe
from yaml_reisekosten_tool.normalization import normalize_reisekosten_input
from yaml_reisekosten_tool.yaml_io import load_yaml_mapping


def test_example_yaml_loads_to_domain_models() -> None:
    data = load_yaml_mapping(Path("examples/example.yml"))

    reisekosten = normalize_reisekosten_input(data)

    assert isinstance(reisekosten, ReisekostenEingabe)
    assert reisekosten.abrechnung.titel == "Reisekostenabrechnung"
    assert reisekosten.abrechnung.zeitraum.von == date(2026, 1, 1)
    assert reisekosten.abrechnung.waehrung == "EUR"
    assert reisekosten.mitarbeiter.name == "Max Mustermann"
    assert reisekosten.arbeitgeber.anschrift is not None
    assert reisekosten.arbeitgeber.anschrift.plz == "54321"
    assert reisekosten.defaults.fahrt is not None
    assert reisekosten.defaults.fahrt.fahrzeug is not None
    assert reisekosten.defaults.fahrt.fahrzeug.kennzeichen == "MS-MM 123"
    assert reisekosten.defaults.auslage is not None
    assert reisekosten.defaults.auslage.betrag_eur == Decimal("12.0")
    assert reisekosten.unterschriften.antragsteller is not None
    assert reisekosten.unterschriften.antragsteller.unterschrift == (
        "examples/signatures/max-mustermann.png"
    )
    assert reisekosten.unterschriften.vorgesetzter is not None
    assert reisekosten.unterschriften.vorgesetzter.name == "Erika Leitung"
    assert len(reisekosten.fahrten) == 5
    assert reisekosten.fahrten[0].datum == date(2026, 1, 8)
    assert reisekosten.fahrten[0].startzeit == time(7, 45)
    assert reisekosten.fahrten[2].gesamt_km == Decimal("98")
    assert reisekosten.fahrten[3].auslage is not None
    assert reisekosten.fahrten[3].auslage.betrag_eur == Decimal("14.0")
