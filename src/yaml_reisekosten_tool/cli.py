"""Kommandozeilen-Einstieg fuer das YAML Reisekosten Tool."""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from collections.abc import Sequence
from pathlib import Path

from yaml_reisekosten_tool.calculation import CalculationError, calculate_reisekosten
from yaml_reisekosten_tool.models import BerechneteAbrechnung
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
        help="Vorhandene Ziel-PDFs ueberschreiben.",
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
        output_paths = build_output_paths(
            (abrechnung,),
            output_dir=output_dir,
            input_file=args.input_file,
        )
        _ensure_no_collisions(output_paths, force=args.force)

        rendered_paths = [
            render_pdf(
                item,
                output_path,
                asset_base_dir=Path.cwd(),
            )
            for item, output_path in zip((abrechnung,), output_paths, strict=True)
        ]
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
    return 0


def build_output_paths(
    abrechnungen: Sequence[BerechneteAbrechnung],
    *,
    output_dir: Path,
    input_file: Path,
) -> tuple[Path, ...]:
    """Bilde stabile PDF-Zielpfade fuer eine oder mehrere berechnete Abrechnungen."""

    total = len(abrechnungen)
    return tuple(
        output_dir / _output_filename(abrechnung, input_file=input_file, index=index, total=total)
        for index, abrechnung in enumerate(abrechnungen, start=1)
    )


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
    index: int,
    total: int,
) -> str:
    eingabe = abrechnung.eingabe
    title_slug = _slug(eingabe.abrechnung.titel or "")
    if title_slug:
        period = _period_slug(eingabe.abrechnung.zeitraum.von, eingabe.abrechnung.zeitraum.bis)
        base = f"{period}_{title_slug}" if period else title_slug
    else:
        base = _slug(Path(input_file).stem) or "abrechnung"

    if total > 1:
        base = f"{base}-{index:02d}"
    return f"{base}.pdf"


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


def _ensure_no_collisions(output_paths: Sequence[Path], *, force: bool) -> None:
    if force:
        return
    for path in output_paths:
        if path.exists():
            raise CliError(f"Ziel-PDF existiert bereits: {path}")


def _print_error(error: Exception) -> None:
    print(f"Fehler: {error}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
