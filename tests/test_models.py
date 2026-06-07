from __future__ import annotations

from pathlib import Path

from yaml_reisekosten_tool.models import ReisekostenEingabe, models_from_mapping
from yaml_reisekosten_tool.yaml_io import load_yaml_mapping


def test_example_yaml_loads_to_domain_models() -> None:
    data = load_yaml_mapping(Path("examples/example.yml"))

    reisekosten = models_from_mapping(data)

    assert isinstance(reisekosten, ReisekostenEingabe)
    assert reisekosten.abrechnung.titel == "Reisekostenabrechnung"
    assert reisekosten.abrechnung.waehrung == "EUR"
    assert reisekosten.mitarbeiter.name == "Max Mustermann"
    assert reisekosten.arbeitgeber.anschrift is not None
    assert reisekosten.arbeitgeber.anschrift.plz == "54321"
    assert reisekosten.defaults.fahrt is not None
    assert reisekosten.defaults.fahrt.fahrzeug is not None
    assert reisekosten.defaults.fahrt.fahrzeug.kennzeichen == "MS-MM 123"
    assert reisekosten.defaults.auslage is not None
    assert reisekosten.defaults.auslage.betrag_eur == 12.00
    assert len(reisekosten.fahrten) == 5
    assert reisekosten.fahrten[2].gesamt_km == 98
    assert reisekosten.fahrten[3].auslage is not None
    assert reisekosten.fahrten[3].auslage.betrag_eur == 14.00
