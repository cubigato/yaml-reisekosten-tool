"""Domain-Modelle fuer die Eingabedaten der Reisekostenabrechnung."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class Zeitraum:
    von: date
    bis: date


@dataclass(frozen=True)
class Abrechnung:
    titel: str | None
    zeitraum: Zeitraum
    waehrung: str | None


@dataclass(frozen=True)
class Mitarbeiter:
    name: str | None
    personalnummer: str | None = None
    abteilung: str | None = None


@dataclass(frozen=True)
class Anschrift:
    strasse: str | None
    plz: str | None
    ort: str | None


@dataclass(frozen=True)
class Arbeitgeber:
    name: str | None
    anschrift: Anschrift | None


@dataclass(frozen=True)
class Fahrzeug:
    kennzeichen: str | None = None
    beschreibung: str | None = None


@dataclass(frozen=True)
class Auslage:
    art: str | None
    betrag_eur: Decimal | None
    beschreibung: str | None
    beleg: str | None = None


@dataclass(frozen=True)
class Fahrt:
    datum: date | None
    start: str | None = None
    ziel: str | None = None
    anlass: str | None = None
    verkehrsmittel: str | None = None
    fahrzeug: Fahrzeug | None = None
    gesamt_km: Decimal | None = None
    startzeit: time | None = None
    endzeit: time | None = None
    notiz: str | None = None
    auslage: Auslage | None = None


@dataclass(frozen=True)
class FahrtDefaults:
    start: str | None = None
    ziel: str | None = None
    anlass: str | None = None
    verkehrsmittel: str | None = None
    fahrzeug: Fahrzeug | None = None
    gesamt_km: Decimal | None = None
    startzeit: time | None = None
    endzeit: time | None = None


@dataclass(frozen=True)
class Defaults:
    fahrt: FahrtDefaults | None = None
    auslage: Auslage | None = None


@dataclass(frozen=True)
class ReisekostenEingabe:
    abrechnung: Abrechnung
    mitarbeiter: Mitarbeiter
    arbeitgeber: Arbeitgeber
    defaults: Defaults
    fahrten: tuple[Fahrt, ...]


def models_from_mapping(data: Mapping[str, Any]) -> ReisekostenEingabe:
    """Bilde das dokumentierte YAML-Root-Mapping in Domain-Objekte ab."""

    return ReisekostenEingabe(
        abrechnung=_build_abrechnung(_mapping(data.get("abrechnung"))),
        mitarbeiter=_build_mitarbeiter(_mapping(data.get("mitarbeiter"))),
        arbeitgeber=_build_arbeitgeber(_mapping(data.get("arbeitgeber"))),
        defaults=_build_defaults(_mapping(data.get("defaults"))),
        fahrten=tuple(_build_fahrt(_mapping(item)) for item in _sequence(data.get("fahrten"))),
    )


def _build_abrechnung(data: Mapping[str, Any]) -> Abrechnung:
    zeitraum = _mapping(data.get("zeitraum"))
    return Abrechnung(
        titel=data.get("titel"),
        zeitraum=Zeitraum(von=zeitraum.get("von"), bis=zeitraum.get("bis")),
        waehrung=data.get("waehrung"),
    )


def _build_mitarbeiter(data: Mapping[str, Any]) -> Mitarbeiter:
    return Mitarbeiter(
        name=data.get("name"),
        personalnummer=data.get("personalnummer"),
        abteilung=data.get("abteilung"),
    )


def _build_arbeitgeber(data: Mapping[str, Any]) -> Arbeitgeber:
    anschrift = _mapping(data.get("anschrift"))
    return Arbeitgeber(
        name=data.get("name"),
        anschrift=Anschrift(
            strasse=anschrift.get("strasse"),
            plz=anschrift.get("plz"),
            ort=anschrift.get("ort"),
        ),
    )


def _build_defaults(data: Mapping[str, Any]) -> Defaults:
    return Defaults(
        fahrt=_build_fahrt_defaults(_mapping(data.get("fahrt"))) if "fahrt" in data else None,
        auslage=_build_auslage(_mapping(data.get("auslage"))) if "auslage" in data else None,
    )


def _build_fahrt_defaults(data: Mapping[str, Any]) -> FahrtDefaults:
    return FahrtDefaults(
        start=data.get("start"),
        ziel=data.get("ziel"),
        anlass=data.get("anlass"),
        verkehrsmittel=data.get("verkehrsmittel"),
        fahrzeug=_build_fahrzeug(_mapping(data.get("fahrzeug"))) if "fahrzeug" in data else None,
        gesamt_km=data.get("gesamt_km"),
        startzeit=data.get("startzeit"),
        endzeit=data.get("endzeit"),
    )


def _build_fahrt(data: Mapping[str, Any]) -> Fahrt:
    return Fahrt(
        datum=data.get("datum"),
        start=data.get("start"),
        ziel=data.get("ziel"),
        anlass=data.get("anlass"),
        verkehrsmittel=data.get("verkehrsmittel"),
        fahrzeug=_build_fahrzeug(_mapping(data.get("fahrzeug"))) if "fahrzeug" in data else None,
        gesamt_km=data.get("gesamt_km"),
        startzeit=data.get("startzeit"),
        endzeit=data.get("endzeit"),
        notiz=data.get("notiz"),
        auslage=_build_auslage(_mapping(data.get("auslage"))) if "auslage" in data else None,
    )


def _build_fahrzeug(data: Mapping[str, Any]) -> Fahrzeug:
    return Fahrzeug(
        kennzeichen=data.get("kennzeichen"),
        beschreibung=data.get("beschreibung"),
    )


def _build_auslage(data: Mapping[str, Any]) -> Auslage:
    return Auslage(
        art=data.get("art"),
        betrag_eur=data.get("betrag_eur"),
        beschreibung=data.get("beschreibung"),
        beleg=data.get("beleg"),
    )


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _sequence(value: Any) -> Sequence[Any]:
    if isinstance(value, Sequence) and not isinstance(value, str | bytes):
        return value
    return ()
