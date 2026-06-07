"""Validierung, Default-Anwendung und Typnormalisierung der Eingabedaten."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import Any

from yaml_reisekosten_tool.models import ReisekostenEingabe, models_from_mapping
from yaml_reisekosten_tool.validation import ValidationError

_REQUIRED_ROOT_MAPPINGS = ("abrechnung", "mitarbeiter", "arbeitgeber")
_REQUIRED_ABRECHNUNG = ("titel", "zeitraum", "waehrung")
_REQUIRED_ZEITRAUM = ("von", "bis")
_REQUIRED_MITARBEITER = ("name",)
_REQUIRED_ARBEITGEBER = ("name", "anschrift")
_REQUIRED_ANSCHRIFT = ("strasse", "plz", "ort")
_REQUIRED_FAHRT = (
    "datum",
    "start",
    "ziel",
    "anlass",
    "verkehrsmittel",
    "gesamt_km",
    "startzeit",
    "endzeit",
)
_REQUIRED_AUSLAGE = ("art", "betrag_eur", "beschreibung")
_TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")
_SIGNATURE_SUFFIXES = (".png", ".jpg", ".jpeg")


def normalize_reisekosten_input(data: Mapping[str, Any]) -> ReisekostenEingabe:
    """Pruefe rohe YAML-Daten und liefere ein normalisiertes Domain-Modell."""

    normalized = _normalize_root(data)
    return models_from_mapping(normalized)


def _normalize_root(data: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(data, Mapping):
        raise ValidationError("<root>", "muss ein Mapping sein")

    root = dict(data)
    for key in _REQUIRED_ROOT_MAPPINGS:
        _require_mapping(root, key, key)

    if "fahrten" not in root:
        raise ValidationError("fahrten", "Pflichtfeld fehlt")
    fahrten = _require_sequence(root, "fahrten", "fahrten")
    if len(fahrten) == 0:
        raise ValidationError("fahrten", "muss mindestens eine Fahrt enthalten")

    defaults = _optional_mapping(root, "defaults", "defaults")
    default_fahrt = _optional_mapping(defaults, "fahrt", "defaults.fahrt")
    default_auslage = _optional_mapping(defaults, "auslage", "defaults.auslage")
    unterschriften = _optional_mapping(root, "unterschriften", "unterschriften")

    normalized = {
        "abrechnung": _normalize_abrechnung(_require_mapping(root, "abrechnung", "abrechnung")),
        "mitarbeiter": _normalize_mitarbeiter(_require_mapping(root, "mitarbeiter", "mitarbeiter")),
        "arbeitgeber": _normalize_arbeitgeber(_require_mapping(root, "arbeitgeber", "arbeitgeber")),
        "defaults": _normalize_defaults(default_fahrt, default_auslage),
        "unterschriften": _normalize_unterschriften(unterschriften),
        "fahrten": [],
    }

    normalized["fahrten"] = [
        _normalize_fahrt(item, index, default_fahrt, default_auslage)
        for index, item in enumerate(fahrten)
    ]
    return normalized


def _normalize_abrechnung(data: Mapping[str, Any]) -> dict[str, Any]:
    _require_fields(data, _REQUIRED_ABRECHNUNG, "abrechnung")
    zeitraum = _require_mapping(data, "zeitraum", "abrechnung.zeitraum")
    _require_fields(zeitraum, _REQUIRED_ZEITRAUM, "abrechnung.zeitraum")

    waehrung = _normalize_required_string(data.get("waehrung"), "abrechnung.waehrung")
    if waehrung != "EUR":
        raise ValidationError("abrechnung.waehrung", "muss EUR sein")

    von = _normalize_date(zeitraum.get("von"), "abrechnung.zeitraum.von")
    bis = _normalize_date(zeitraum.get("bis"), "abrechnung.zeitraum.bis")
    if bis < von:
        raise ValidationError("abrechnung.zeitraum.bis", "darf nicht vor von liegen")

    return {
        "titel": _normalize_required_string(data.get("titel"), "abrechnung.titel"),
        "zeitraum": {"von": von, "bis": bis},
        "waehrung": waehrung,
    }


def _normalize_mitarbeiter(data: Mapping[str, Any]) -> dict[str, Any]:
    _require_fields(data, _REQUIRED_MITARBEITER, "mitarbeiter")
    return {
        "name": _normalize_required_string(data.get("name"), "mitarbeiter.name"),
        "personalnummer": _normalize_optional_string(
            data.get("personalnummer"), "mitarbeiter.personalnummer"
        ),
        "abteilung": _normalize_optional_string(data.get("abteilung"), "mitarbeiter.abteilung"),
    }


def _normalize_arbeitgeber(data: Mapping[str, Any]) -> dict[str, Any]:
    _require_fields(data, _REQUIRED_ARBEITGEBER, "arbeitgeber")
    anschrift = _require_mapping(data, "anschrift", "arbeitgeber.anschrift")
    _require_fields(anschrift, _REQUIRED_ANSCHRIFT, "arbeitgeber.anschrift")
    return {
        "name": _normalize_required_string(data.get("name"), "arbeitgeber.name"),
        "anschrift": {
            "strasse": _normalize_required_string(
                anschrift.get("strasse"), "arbeitgeber.anschrift.strasse"
            ),
            "plz": _normalize_required_string(anschrift.get("plz"), "arbeitgeber.anschrift.plz"),
            "ort": _normalize_required_string(anschrift.get("ort"), "arbeitgeber.anschrift.ort"),
        },
    }


def _normalize_defaults(
    default_fahrt: Mapping[str, Any],
    default_auslage: Mapping[str, Any],
) -> dict[str, Any]:
    defaults: dict[str, Any] = {}
    if default_fahrt:
        defaults["fahrt"] = _normalize_fahrt_defaults(default_fahrt, "defaults.fahrt")
    if default_auslage:
        defaults["auslage"] = _normalize_auslage(default_auslage, "defaults.auslage")
    return defaults


def _normalize_fahrt_defaults(data: Mapping[str, Any], path: str) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key in ("start", "ziel", "anlass", "verkehrsmittel"):
        if key in data:
            normalized[key] = _normalize_optional_string(data.get(key), f"{path}.{key}")
    if "fahrzeug" in data:
        normalized["fahrzeug"] = _normalize_fahrzeug(
            _require_mapping(data, "fahrzeug", f"{path}.fahrzeug"), f"{path}.fahrzeug"
        )
    if "gesamt_km" in data:
        normalized["gesamt_km"] = _normalize_non_negative_decimal(
            data.get("gesamt_km"), f"{path}.gesamt_km"
        )
    if "startzeit" in data:
        normalized["startzeit"] = _normalize_time(data.get("startzeit"), f"{path}.startzeit")
    if "endzeit" in data:
        normalized["endzeit"] = _normalize_time(data.get("endzeit"), f"{path}.endzeit")
    return normalized


def _normalize_fahrt(
    item: Any,
    index: int,
    default_fahrt: Mapping[str, Any],
    default_auslage: Mapping[str, Any],
) -> dict[str, Any]:
    path = f"fahrten[{index}]"
    if not isinstance(item, Mapping):
        raise ValidationError(path, "muss ein Mapping sein")

    merged = _deep_merge(default_fahrt, item)
    _require_fields(merged, _REQUIRED_FAHRT, path)

    normalized: dict[str, Any] = {
        "datum": _normalize_date(merged.get("datum"), f"{path}.datum"),
        "start": _normalize_required_string(merged.get("start"), f"{path}.start"),
        "ziel": _normalize_required_string(merged.get("ziel"), f"{path}.ziel"),
        "anlass": _normalize_required_string(merged.get("anlass"), f"{path}.anlass"),
        "verkehrsmittel": _normalize_required_string(
            merged.get("verkehrsmittel"), f"{path}.verkehrsmittel"
        ),
        "gesamt_km": _normalize_non_negative_decimal(merged.get("gesamt_km"), f"{path}.gesamt_km"),
        "startzeit": _normalize_time(merged.get("startzeit"), f"{path}.startzeit"),
        "endzeit": _normalize_time(merged.get("endzeit"), f"{path}.endzeit"),
        "notiz": _normalize_optional_string(merged.get("notiz"), f"{path}.notiz"),
    }
    if normalized["endzeit"] <= normalized["startzeit"]:
        raise ValidationError(f"{path}.endzeit", "muss nach startzeit liegen")

    if "fahrzeug" in merged:
        normalized["fahrzeug"] = _normalize_fahrzeug(
            _require_mapping(merged, "fahrzeug", f"{path}.fahrzeug"), f"{path}.fahrzeug"
        )

    auslage = _normalize_fahrt_auslage(merged, default_auslage, path)
    if auslage is not None:
        normalized["auslage"] = auslage

    return normalized


def _normalize_fahrt_auslage(
    fahrt: Mapping[str, Any],
    default_auslage: Mapping[str, Any],
    path: str,
) -> dict[str, Any] | None:
    has_fahrt_auslage = "auslage" in fahrt
    if not default_auslage and not has_fahrt_auslage:
        return None

    fahrt_auslage = _optional_mapping(fahrt, "auslage", f"{path}.auslage")
    merged = _deep_merge(default_auslage, fahrt_auslage)
    return _normalize_auslage(merged, f"{path}.auslage")


def _normalize_auslage(data: Mapping[str, Any], path: str) -> dict[str, Any]:
    _require_fields(data, _REQUIRED_AUSLAGE, path)
    return {
        "art": _normalize_required_string(data.get("art"), f"{path}.art"),
        "betrag_eur": _normalize_non_negative_decimal(data.get("betrag_eur"), f"{path}.betrag_eur"),
        "beschreibung": _normalize_required_string(
            data.get("beschreibung"), f"{path}.beschreibung"
        ),
        "beleg": _normalize_optional_string(data.get("beleg"), f"{path}.beleg"),
    }


def _normalize_fahrzeug(data: Mapping[str, Any], path: str) -> dict[str, Any]:
    return {
        "kennzeichen": _normalize_optional_string(data.get("kennzeichen"), f"{path}.kennzeichen"),
        "beschreibung": _normalize_optional_string(
            data.get("beschreibung"), f"{path}.beschreibung"
        ),
    }


def _normalize_unterschriften(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    if "antragsteller" in data:
        normalized["antragsteller"] = _normalize_digitale_unterschrift(
            _require_mapping(data, "antragsteller", "unterschriften.antragsteller"),
            "unterschriften.antragsteller",
        )
    if "vorgesetzter" in data:
        normalized["vorgesetzter"] = _normalize_digitale_unterschrift(
            _require_mapping(data, "vorgesetzter", "unterschriften.vorgesetzter"),
            "unterschriften.vorgesetzter",
        )
    return normalized


def _normalize_digitale_unterschrift(data: Mapping[str, Any], path: str) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key in ("ort", "name"):
        if key in data:
            normalized[key] = _normalize_optional_string(data.get(key), f"{path}.{key}")
    if "datum" in data:
        normalized["datum"] = _normalize_date(data.get("datum"), f"{path}.datum")
    if "unterschrift" in data:
        normalized["unterschrift"] = _normalize_signature_path(
            data.get("unterschrift"), f"{path}.unterschrift"
        )
    return normalized


def _normalize_signature_path(value: Any, path: str) -> str | None:
    normalized = _normalize_optional_string(value, path)
    if normalized is None:
        return None
    if not normalized.lower().endswith(_SIGNATURE_SUFFIXES):
        raise ValidationError(path, "muss auf .png, .jpg oder .jpeg enden")
    return normalized


def _require_fields(data: Mapping[str, Any], fields: tuple[str, ...], path: str) -> None:
    for field in fields:
        if field not in data or _is_blank(data.get(field)):
            raise ValidationError(f"{path}.{field}", "Pflichtfeld fehlt")


def _require_mapping(data: Mapping[str, Any], key: str, path: str) -> Mapping[str, Any]:
    value = data.get(key)
    if value is None:
        raise ValidationError(path, "Pflichtbereich fehlt")
    if not isinstance(value, Mapping):
        raise ValidationError(path, "muss ein Mapping sein")
    return value


def _optional_mapping(data: Mapping[str, Any], key: str, path: str) -> Mapping[str, Any]:
    if key not in data or data.get(key) is None:
        return {}
    value = data.get(key)
    if not isinstance(value, Mapping):
        raise ValidationError(path, "muss ein Mapping sein")
    return value


def _require_sequence(data: Mapping[str, Any], key: str, path: str) -> Sequence[Any]:
    value = data.get(key)
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        raise ValidationError(path, "muss eine Liste sein")
    return value


def _normalize_required_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(path, "muss ein nicht leerer String sein")
    return value.strip()


def _normalize_optional_string(value: Any, path: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError(path, "muss ein String sein")
    normalized = value.strip()
    return normalized or None


def _normalize_date(value: Any, path: str) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise ValidationError(path, "muss ein Datum im Format YYYY-MM-DD sein") from exc
    raise ValidationError(path, "muss ein Datum im Format YYYY-MM-DD sein")


def _normalize_time(value: Any, path: str) -> time:
    if isinstance(value, time):
        return value.replace(second=0, microsecond=0)
    if isinstance(value, str):
        if not _TIME_PATTERN.fullmatch(value):
            raise ValidationError(path, "muss eine Uhrzeit im Format HH:MM sein")
        try:
            parsed = datetime.strptime(value, "%H:%M").time()
        except ValueError as exc:
            raise ValidationError(path, "muss eine Uhrzeit im Format HH:MM sein") from exc
        return parsed
    raise ValidationError(path, "muss eine Uhrzeit im Format HH:MM sein")


def _normalize_non_negative_decimal(value: Any, path: str) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(path, "muss eine Zahl sein") from exc
    if amount < 0:
        raise ValidationError(path, "darf nicht negativ sein")
    return amount


def _deep_merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = deepcopy(dict(defaults))
    for key, value in overrides.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())
