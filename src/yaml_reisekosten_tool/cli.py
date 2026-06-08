"""Kommandozeilen-Einstieg fuer das YAML Reisekosten Tool."""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from collections.abc import Sequence
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from yaml_reisekosten_tool.calculation import CalculationError, calculate_reisekosten
from yaml_reisekosten_tool.models import BerechneteAbrechnung, BerechnungsSummen
from yaml_reisekosten_tool.normalization import normalize_reisekosten_input
from yaml_reisekosten_tool.rates import RatesError
from yaml_reisekosten_tool.rendering import RenderingError, render_pdf
from yaml_reisekosten_tool.validation import ValidationError
from yaml_reisekosten_tool.yaml_io import YamlLoadError, load_yaml_mapping

EXIT_ERROR = 1


class CliError(RuntimeError):
    """Kontrollierter CLI-Fehler fuer erwartbare Abbrueche."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yaml-reisekosten-tool",
        description="Erzeugt Reisekostenabrechnungen als PDF aus einer YAML-Datei.",
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        type=Path,
        metavar="EINGABE.yml",
        help="YAML-Datei mit den Reisekostendaten.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        metavar="DIR",
        help="Bestehendes Ausgabeverzeichnis fuer erzeugte PDFs.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Vorhandene Zieldateien ueberschreiben.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.input_file is None:
        parser.print_help()
        return 0

    try:
        output_dir = _validate_output_dir(args.output_dir)
        data = load_yaml_mapping(args.input_file)
        eingabe = normalize_reisekosten_input(data)
        abrechnung = calculate_reisekosten(eingabe)
        abrechnungen = split_abrechnung_by_fahrt(abrechnung)
        output_paths = build_output_paths(
            abrechnungen,
            output_dir=output_dir,
            input_file=args.input_file,
        )
        summary_path = build_summary_path(
            abrechnung,
            output_dir=output_dir,
            input_file=args.input_file,
        )
        _ensure_no_collisions((*output_paths, summary_path), force=args.force)

        rendered_paths = [
            render_pdf(
                item,
                output_path,
                asset_base_dir=Path.cwd(),
            )
            for item, output_path in zip(abrechnungen, output_paths, strict=True)
        ]
        write_summary_markdown(abrechnungen, rendered_paths, summary_path)
    except (
        CliError,
        YamlLoadError,
        ValidationError,
        CalculationError,
        RatesError,
        RenderingError,
    ) as exc:
        _print_error(exc)
        return EXIT_ERROR

    for path in rendered_paths:
        print(path)
    print(summary_path)
    return 0


def build_output_paths(
    abrechnungen: Sequence[BerechneteAbrechnung],
    *,
    output_dir: Path,
    input_file: Path,
) -> tuple[Path, ...]:
    """Bilde stabile PDF-Zielpfade fuer eine oder mehrere berechnete Abrechnungen."""

    filenames = [_output_filename(abrechnung, input_file=input_file) for abrechnung in abrechnungen]
    return tuple(output_dir / filename for filename in _deduplicate_filenames(filenames))


def build_summary_path(
    abrechnung: BerechneteAbrechnung,
    *,
    output_dir: Path,
    input_file: Path,
) -> Path:
    """Bilde den Zielpfad fuer die interne Markdown-Zusammenfassung."""

    base = _summary_base_name(abrechnung, input_file=input_file)
    return output_dir / f"{base}_zusammenfassung.md"


def write_summary_markdown(
    abrechnungen: Sequence[BerechneteAbrechnung],
    pdf_paths: Sequence[Path],
    summary_path: Path,
) -> Path:
    """Schreibe eine interne Markdown-Zusammenfassung aller erzeugten PDFs."""

    if len(abrechnungen) != len(pdf_paths):
        raise CliError("Interner Fehler: Anzahl Abrechnungen und PDFs passt nicht zusammen")

    currency = abrechnungen[0].eingabe.abrechnung.waehrung if abrechnungen else "EUR"
    total = sum((item.summen.gesamt_eur for item in abrechnungen), Decimal("0.00"))
    lines = [
        f"# {_markdown_text(_summary_title(abrechnungen))}",
        "",
        f"- Anzahl Abrechnungen: {len(abrechnungen)}",
        f"- Gesamtbetrag: {_format_money(total)} {currency or 'EUR'}",
        "",
        "| PDF | Datum | Zeit | Ziel | Anlass | Fahrtkosten | Verpflegung | Auslagen | Gesamt |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]

    for abrechnung, pdf_path in zip(abrechnungen, pdf_paths, strict=True):
        fahrt = abrechnung.fahrten[0].fahrt if abrechnung.fahrten else None
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_text(pdf_path.name),
                    _markdown_text(_format_date_for_filename(abrechnung) or ""),
                    _markdown_text(_time_range(abrechnung)),
                    _markdown_text(fahrt.ziel if fahrt else ""),
                    _markdown_text(fahrt.anlass if fahrt else ""),
                    f"{_format_money(abrechnung.summen.fahrtkosten_eur)} {currency or 'EUR'}",
                    (
                        f"{_format_money(abrechnung.summen.verpflegungspauschalen_eur)} "
                        f"{currency or 'EUR'}"
                    ),
                    f"{_format_money(abrechnung.summen.auslagen_eur)} {currency or 'EUR'}",
                    f"{_format_money(abrechnung.summen.gesamt_eur)} {currency or 'EUR'}",
                ]
            )
            + " |"
        )

    lines.extend(["", f"**Gesamtbetrag:** {_format_money(total)} {currency or 'EUR'}", ""])
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def split_abrechnung_by_fahrt(
    abrechnung: BerechneteAbrechnung,
) -> tuple[BerechneteAbrechnung, ...]:
    """Teile mehrere Fahrten in einzelne Lexware-Formularabrechnungen auf."""

    if len(abrechnung.fahrten) <= 1:
        return (abrechnung,)

    einzelabrechnungen = []
    for berechnete_fahrt in abrechnung.fahrten:
        auslage = (
            replace(berechnete_fahrt.auslage, fahrt_index=0)
            if berechnete_fahrt.auslage is not None
            else None
        )
        einzel_fahrt = replace(berechnete_fahrt, index=0, auslage=auslage)
        einzelabrechnungen.append(
            BerechneteAbrechnung(
                eingabe=replace(abrechnung.eingabe, fahrten=(berechnete_fahrt.fahrt,)),
                fahrten=(einzel_fahrt,),
                auslagen=(auslage,) if auslage is not None else (),
                summen=BerechnungsSummen(
                    fahrtkosten_eur=einzel_fahrt.fahrtkosten_eur,
                    verpflegungspauschalen_eur=einzel_fahrt.verpflegungspauschale_eur,
                    auslagen_eur=auslage.betrag_eur if auslage is not None else Decimal("0.00"),
                    gesamt_eur=einzel_fahrt.gesamt_eur,
                ),
            )
        )
    return tuple(einzelabrechnungen)


def _validate_output_dir(path: Path) -> Path:
    output_dir = Path(path)
    if not output_dir.exists():
        raise CliError(f"Ausgabeverzeichnis existiert nicht: {output_dir}")
    if not output_dir.is_dir():
        raise CliError(f"Ausgabepfad ist kein Verzeichnis: {output_dir}")
    if not os.access(output_dir, os.W_OK):
        raise CliError(f"Ausgabeverzeichnis ist nicht beschreibbar: {output_dir}")
    return output_dir


def _output_filename(
    abrechnung: BerechneteAbrechnung,
    *,
    input_file: Path,
) -> str:
    base = _pdf_base_name(abrechnung, input_file=input_file)
    date_prefix = _format_date_for_filename(abrechnung)
    if date_prefix:
        base = f"{date_prefix}_{base}"
    return f"{base}.pdf"


def _pdf_base_name(abrechnung: BerechneteAbrechnung, *, input_file: Path) -> str:
    title_slug = _slug(abrechnung.eingabe.abrechnung.titel or "")
    return title_slug or _slug(Path(input_file).stem) or "abrechnung"


def _summary_base_name(abrechnung: BerechneteAbrechnung, *, input_file: Path) -> str:
    eingabe = abrechnung.eingabe
    title_slug = _slug(eingabe.abrechnung.titel or "")
    if not title_slug:
        return _slug(Path(input_file).stem) or "abrechnung"

    period = _period_slug(eingabe.abrechnung.zeitraum.von, eingabe.abrechnung.zeitraum.bis)
    return f"{period}_{title_slug}" if period else title_slug


def _deduplicate_filenames(filenames: Sequence[str]) -> tuple[str, ...]:
    seen: dict[str, int] = {}
    deduplicated = []
    for filename in filenames:
        count = seen.get(filename, 0) + 1
        seen[filename] = count
        if count == 1:
            deduplicated.append(filename)
            continue

        stem = Path(filename).stem
        suffix = Path(filename).suffix
        deduplicated.append(f"{stem}-{count:02d}{suffix}")
    return tuple(deduplicated)


def _period_slug(von, bis) -> str:
    if von is None:
        return ""
    if bis is not None and von.year != bis.year:
        return f"{von:%Y-%m}_{bis:%Y-%m}"
    return f"{von:%Y-%m}"


def _slug(value: str) -> str:
    ascii_value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    )
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value)
    return slug.strip("-")


def _format_date_for_filename(abrechnung: BerechneteAbrechnung) -> str | None:
    dates = [fahrt.fahrt.datum for fahrt in abrechnung.fahrten if fahrt.fahrt.datum is not None]
    if not dates:
        return None
    return f"{min(dates):%Y-%m-%d}"


def _format_money(value: Decimal) -> str:
    return f"{value:.2f}".replace(".", ",")


def _time_range(abrechnung: BerechneteAbrechnung) -> str:
    if len(abrechnung.fahrten) != 1:
        return ""
    fahrt = abrechnung.fahrten[0].fahrt
    if fahrt.startzeit is None or fahrt.endzeit is None:
        return ""
    return f"{fahrt.startzeit:%H:%M}-{fahrt.endzeit:%H:%M}"


def _summary_title(abrechnungen: Sequence[BerechneteAbrechnung]) -> str:
    if not abrechnungen:
        return "Reisekosten-Zusammenfassung"
    title = abrechnungen[0].eingabe.abrechnung.titel
    return f"Reisekosten-Zusammenfassung: {title}" if title else "Reisekosten-Zusammenfassung"


def _markdown_text(value: str | None) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ")


def _ensure_no_collisions(output_paths: Sequence[Path], *, force: bool) -> None:
    if force:
        return
    for path in output_paths:
        if path.exists():
            raise CliError(f"Zieldatei existiert bereits: {path}")


def _print_error(error: Exception) -> None:
    print(f"Fehler: {error}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
