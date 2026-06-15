"""Typst-Rendering fuer berechnete Reisekostenabrechnungen."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Sequence
from copy import deepcopy
from datetime import date, time
from decimal import Decimal
from importlib import resources
from pathlib import Path
from typing import Any

from yaml_reisekosten_tool.models import BerechneteAbrechnung, BerechneteFahrt

TEMPLATE_PACKAGE = "yaml_reisekosten_tool.templates"
TEMPLATE_NAME = "reisekosten.typ"


class RenderingError(RuntimeError):
    """Kontrollierter Fehler beim Rendern einer Reisekostenabrechnung."""


Runner = Callable[..., subprocess.CompletedProcess[str]]


def build_render_context(abrechnung: BerechneteAbrechnung) -> dict[str, Any]:
    """Baue den JSON-kompatiblen Kontext fuer das Typst-Template."""

    eingabe = abrechnung.eingabe
    fahrten = tuple(sorted(abrechnung.fahrten, key=lambda item: (item.fahrt.datum, item.index)))
    first = fahrten[0] if fahrten else None
    last = fahrten[-1] if fahrten else None
    arbeitgeber = eingabe.arbeitgeber
    anschrift = arbeitgeber.anschrift

    return {
        "abrechnung": {
            "titel": eingabe.abrechnung.titel or "",
            "zeitraum": {
                "von": _format_date(eingabe.abrechnung.zeitraum.von),
                "bis": _format_date(eingabe.abrechnung.zeitraum.bis),
            },
            "waehrung": eingabe.abrechnung.waehrung or "EUR",
        },
        "mitarbeiter": {
            "name": eingabe.mitarbeiter.name or "",
            "vorname": _split_name(eingabe.mitarbeiter.name)[0],
            "nachname": _split_name(eingabe.mitarbeiter.name)[1],
            "personalnummer": eingabe.mitarbeiter.personalnummer or "",
            "abteilung": eingabe.mitarbeiter.abteilung or "",
        },
        "arbeitgeber": {
            "name": arbeitgeber.name or "",
            "anschrift": _join_non_empty(
                [
                    anschrift.strasse if anschrift else None,
                    _join_non_empty(
                        [
                            anschrift.plz if anschrift else None,
                            anschrift.ort if anschrift else None,
                        ],
                        separator=" ",
                    ),
                ]
            ),
        },
        "reise": {
            "beginn_datum": _format_date(first.fahrt.datum) if first else "",
            "beginn_uhrzeit": _format_time(first.fahrt.startzeit) if first else "",
            "ende_datum": _format_date(last.fahrt.datum) if last else "",
            "ende_uhrzeit": _format_time(last.fahrt.endzeit) if last else "",
            "ziele": _unique_join(fahrt.fahrt.ziel for fahrt in fahrten),
            "anlaesse": _unique_join(fahrt.fahrt.anlass for fahrt in fahrten),
            "verkehrsmittel": _unique_join(fahrt.fahrt.verkehrsmittel for fahrt in fahrten),
            "privater_pkw": any(fahrt.fahrt.verkehrsmittel == "privater_pkw" for fahrt in fahrten),
            "fahrzeug": _unique_join(
                _join_non_empty(
                    [
                        fahrt.fahrt.fahrzeug.beschreibung,
                        fahrt.fahrt.fahrzeug.kennzeichen,
                    ],
                    separator=", ",
                )
                for fahrt in fahrten
                if fahrt.fahrt.fahrzeug is not None
            ),
            "notizen": _unique_join(fahrt.fahrt.notiz for fahrt in fahrten),
            "fahrten": [_fahrt_context(fahrt) for fahrt in fahrten],
        },
        "kosten": {
            "fahrtkosten": _format_money(abrechnung.summen.fahrtkosten_eur),
            "verpflegung": _format_money(abrechnung.summen.verpflegungspauschalen_eur),
            "auslagen": _format_money(abrechnung.summen.auslagen_eur),
            "reisenebenkosten": _format_reisenebenkosten(abrechnung, fahrten),
            "gesamt": _format_money(abrechnung.summen.gesamt_eur),
            "verpflegung_tage_acht_bis_vierundzwanzig": sum(
                1
                for fahrt in fahrten
                if fahrt.verpflegungspauschale_eur > Decimal("0.00")
                and fahrt.abwesenheit_minuten < 24 * 60
            ),
            "verpflegung_tage_vierundzwanzig": sum(
                1 for fahrt in fahrten if fahrt.abwesenheit_minuten >= 24 * 60
            ),
        },
        "unterschriften": {
            "antragsteller": _signature_context(
                eingabe.unterschriften.antragsteller,
                default_name=eingabe.mitarbeiter.name,
                default_date=eingabe.abrechnung.zeitraum.bis,
            ),
            "vorgesetzter": _signature_context(eingabe.unterschriften.vorgesetzter),
        },
    }


def resolve_template_path() -> Path:
    """Liefere den Pfad zum paketierten Typst-Template."""

    template = resources.files(TEMPLATE_PACKAGE).joinpath(TEMPLATE_NAME)
    with resources.as_file(template) as path:
        resolved = Path(path)
        if not resolved.is_file():
            raise RenderingError(f"Typst-Template fehlt: {TEMPLATE_NAME}")
        return resolved


def render_pdf(
    abrechnung: BerechneteAbrechnung,
    output_path: Path,
    *,
    typst_binary: str = "typst",
    template_path: Path | None = None,
    asset_base_dir: Path | None = None,
    runner: Runner = subprocess.run,
) -> Path:
    """Rendere eine berechnete Abrechnung per Typst an einen expliziten PDF-Zielpfad."""

    output_path = Path(output_path)
    template = template_path or resolve_template_path()
    if not template.is_file():
        raise RenderingError(f"Typst-Template fehlt: {template}")

    context = build_render_context(abrechnung)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="yaml-reisekosten-render-") as temp_dir:
        temp_path = Path(temp_dir)
        context_path = Path(temp_dir) / "context.json"
        context = _prepare_signature_assets(
            context,
            temp_path,
            asset_base_dir=asset_base_dir or Path.cwd(),
        )
        context_path.write_text(
            json.dumps(context, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        render_template = temp_path / template.name
        render_template.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
        command = [
            typst_binary,
            "compile",
            "--root",
            str(temp_path),
            str(render_template),
            str(output_path.resolve()),
            "--input",
            f"data={context_path.name}",
        ]
        try:
            completed = runner(
                command,
                check=False,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise RenderingError(
                f"Typst ist nicht installiert oder nicht im PATH: {typst_binary}"
            ) from exc

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        message = "Typst-Rendering ist fehlgeschlagen"
        if detail:
            message = f"{message}: {detail}"
        raise RenderingError(message)

    return output_path


def _fahrt_context(fahrt: BerechneteFahrt) -> dict[str, Any]:
    return {
        "datum": _format_date(fahrt.fahrt.datum),
        "startzeit": _format_time(fahrt.fahrt.startzeit),
        "endzeit": _format_time(fahrt.fahrt.endzeit),
        "start": fahrt.fahrt.start or "",
        "ziel": fahrt.fahrt.ziel or "",
        "anlass": fahrt.fahrt.anlass or "",
        "gesamt_km": _format_number(fahrt.fahrt.gesamt_km),
        "kilometerpauschale": _format_money(fahrt.kilometerpauschale_eur),
        "fahrtkosten": _format_money(fahrt.fahrtkosten_eur),
        "verpflegung": _format_money(fahrt.verpflegungspauschale_eur),
        "auslage": _format_money(fahrt.auslage.betrag_eur) if fahrt.auslage else "0,00",
        "gesamt": _format_money(fahrt.gesamt_eur),
        "notiz": fahrt.fahrt.notiz or "",
    }


def _signature_context(
    signature, *, default_name: str | None = None, default_date: date | None = None
):
    return {
        "ort": signature.ort if signature and signature.ort else "",
        "datum": _format_date(signature.datum if signature and signature.datum else default_date),
        "name": signature.name if signature and signature.name else default_name or "",
        "unterschrift": signature.unterschrift if signature and signature.unterschrift else "",
        "unterschrift_asset": "",
    }


def _prepare_signature_assets(
    context: dict[str, Any],
    temp_path: Path,
    *,
    asset_base_dir: Path,
) -> dict[str, Any]:
    prepared = deepcopy(context)
    asset_dir = temp_path / "assets"

    for role, signature in prepared["unterschriften"].items():
        source_value = signature.get("unterschrift")
        if not source_value:
            continue
        source = Path(source_value)
        if not source.is_absolute():
            source = asset_base_dir / source
        if not source.is_file():
            raise RenderingError(f"Unterschrift-Datei fehlt fuer {role}: {source}")

        asset_dir.mkdir(exist_ok=True)
        target = asset_dir / f"{role}{source.suffix.lower()}"
        shutil.copyfile(source, target)
        signature["unterschrift_asset"] = str(target.relative_to(temp_path))

    return prepared


def _format_date(value: date | None) -> str:
    if value is None:
        return ""
    return value.strftime("%d.%m.%Y")


def _format_time(value: time | None) -> str:
    if value is None:
        return ""
    return value.strftime("%H:%M")


def _format_money(value: Decimal | None) -> str:
    if value is None:
        return "0,00"
    return f"{value:.2f}".replace(".", ",")


def _format_reisenebenkosten(
    abrechnung: BerechneteAbrechnung,
    fahrten: Sequence[BerechneteFahrt],
) -> str:
    amount = f"{_format_money(abrechnung.summen.auslagen_eur)} EUR"
    if len(fahrten) != 1 or fahrten[0].auslage is None:
        return amount
    return f"{amount} ({fahrten[0].auslage.beschreibung})"


def _format_number(value: Decimal | None) -> str:
    if value is None:
        return ""
    formatted = f"{value.normalize():f}"
    return formatted.replace(".", ",")


def _split_name(value: str | None) -> tuple[str, str]:
    if not value:
        return "", ""
    parts = value.strip().split(maxsplit=1)
    if len(parts) == 1:
        return "", parts[0]
    return parts[0], parts[1]


def _unique_join(values: Sequence[str | None] | Any, *, separator: str = "; ") -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return separator.join(seen)


def _join_non_empty(values: Sequence[str | None], *, separator: str = ", ") -> str:
    return separator.join(value for value in values if value)
