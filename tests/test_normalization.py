from __future__ import annotations

from copy import deepcopy
from datetime import date, time
from decimal import Decimal

import pytest

from yaml_reisekosten_tool.normalization import normalize_reisekosten_input
from yaml_reisekosten_tool.validation import ValidationError


def _valid_input() -> dict:
    return {
        "abrechnung": {
            "titel": "Reisekosten",
            "zeitraum": {"von": "2026-01-01", "bis": "2026-01-31"},
            "waehrung": "EUR",
        },
        "mitarbeiter": {"name": "Max Mustermann"},
        "arbeitgeber": {
            "name": "Beispiel GmbH",
            "anschrift": {"strasse": "Stadtweg 8", "plz": "54321", "ort": "Musterstadt"},
        },
        "defaults": {
            "fahrt": {
                "start": "Zuhause",
                "ziel": "Beispiel GmbH",
                "anlass": "Kundentermin",
                "verkehrsmittel": "privater_pkw",
                "fahrzeug": {"kennzeichen": "MS-MM 123", "beschreibung": "Privater PKW"},
                "gesamt_km": 84,
                "startzeit": "07:45",
                "endzeit": "19:00",
            },
            "auslage": {
                "art": "parken",
                "betrag_eur": "12.00",
                "beschreibung": "Parkhaus",
            },
        },
        "fahrten": [{"datum": "2026-01-08"}],
    }


def test_normalize_applies_defaults_and_converts_stable_types() -> None:
    reisekosten = normalize_reisekosten_input(_valid_input())

    fahrt = reisekosten.fahrten[0]
    assert fahrt.datum == date(2026, 1, 8)
    assert fahrt.start == "Zuhause"
    assert fahrt.gesamt_km == Decimal("84")
    assert fahrt.startzeit == time(7, 45)
    assert fahrt.endzeit == time(19, 0)
    assert fahrt.auslage is not None
    assert fahrt.auslage.betrag_eur == Decimal("12.00")


def test_normalize_keeps_fahrt_and_auslage_overrides() -> None:
    data = _valid_input()
    data["fahrten"] = [
        {
            "datum": "2026-01-08",
            "gesamt_km": "98.5",
            "auslage": {"betrag_eur": "14.50", "beschreibung": "Ausweichparkhaus"},
        }
    ]

    reisekosten = normalize_reisekosten_input(data)

    fahrt = reisekosten.fahrten[0]
    assert fahrt.gesamt_km == Decimal("98.5")
    assert fahrt.auslage is not None
    assert fahrt.auslage.art == "parken"
    assert fahrt.auslage.betrag_eur == Decimal("14.50")
    assert fahrt.auslage.beschreibung == "Ausweichparkhaus"


def test_normalize_accepts_digital_signature_data() -> None:
    data = _valid_input()
    data["unterschriften"] = {
        "antragsteller": {
            "ort": "Musterstadt",
            "datum": "2026-01-31",
            "name": "Max Mustermann",
            "unterschrift": "signatures/max.png",
        },
        "vorgesetzter": {"name": "Erika Leitung", "unterschrift": "signatures/erika.jpg"},
    }

    reisekosten = normalize_reisekosten_input(data)

    assert reisekosten.unterschriften.antragsteller is not None
    assert reisekosten.unterschriften.antragsteller.unterschrift == "signatures/max.png"
    assert reisekosten.unterschriften.vorgesetzter is not None
    assert reisekosten.unterschriften.vorgesetzter.unterschrift == "signatures/erika.jpg"


def test_normalize_reports_missing_required_field_with_path() -> None:
    data = _valid_input()
    del data["arbeitgeber"]["anschrift"]["plz"]

    with pytest.raises(ValidationError) as exc_info:
        normalize_reisekosten_input(data)

    assert exc_info.value.field_path == "arbeitgeber.anschrift.plz"
    assert "arbeitgeber.anschrift.plz" in str(exc_info.value)


@pytest.mark.parametrize(
    ("mutate", "field_path"),
    [
        (lambda data: data["fahrten"][0].update({"datum": "08.01.2026"}), "fahrten[0].datum"),
        (lambda data: data["fahrten"][0].update({"startzeit": "7:45"}), "fahrten[0].startzeit"),
        (lambda data: data["fahrten"][0].update({"gesamt_km": -1}), "fahrten[0].gesamt_km"),
        (lambda data: data["fahrten"][0].update({"endzeit": "06:45"}), "fahrten[0].endzeit"),
    ],
)
def test_normalize_reports_invalid_values_with_field_path(mutate, field_path: str) -> None:
    data = deepcopy(_valid_input())
    mutate(data)

    with pytest.raises(ValidationError) as exc_info:
        normalize_reisekosten_input(data)

    assert exc_info.value.field_path == field_path


def test_normalize_rejects_missing_fahrten() -> None:
    data = _valid_input()
    del data["fahrten"]

    with pytest.raises(ValidationError) as exc_info:
        normalize_reisekosten_input(data)

    assert exc_info.value.field_path == "fahrten"


def test_normalize_rejects_unsupported_signature_image_suffix() -> None:
    data = _valid_input()
    data["unterschriften"] = {
        "antragsteller": {"unterschrift": "signatures/max.svg"},
    }

    with pytest.raises(ValidationError) as exc_info:
        normalize_reisekosten_input(data)

    assert exc_info.value.field_path == "unterschriften.antragsteller.unterschrift"
