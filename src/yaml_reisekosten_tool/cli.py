"""Kommandozeilen-Einstieg fuer das YAML Reisekosten Tool."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path


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

    print(
        "Platzhalter: Die YAML-zu-PDF-Pipeline ist noch nicht implementiert. "
        f"Eingabe: {args.input_file}; Ausgabe: {args.output_dir}; "
        f"Ueberschreiben: {'ja' if args.force else 'nein'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
