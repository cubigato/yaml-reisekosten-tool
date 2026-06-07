from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import yaml_reisekosten_tool
from yaml_reisekosten_tool import cli
from yaml_reisekosten_tool.cli import build_output_paths, main
from yaml_reisekosten_tool.rendering import RenderingError


def _valid_yaml() -> str:
    return """
abrechnung:
  titel: Reisekosten Max Mustermann
  zeitraum:
    von: 2026-01-01
    bis: 2026-01-31
  waehrung: EUR
mitarbeiter:
  name: Max Mustermann
arbeitgeber:
  name: Beispiel GmbH
  anschrift:
    strasse: Stadtweg 8
    plz: "54321"
    ort: Musterstadt
defaults:
  fahrt:
    start: Zuhause
    ziel: Beispiel GmbH
    anlass: Kundentermin
    verkehrsmittel: privater_pkw
    gesamt_km: 84
    startzeit: "07:45"
    endzeit: "19:00"
fahrten:
  - datum: 2026-01-08
"""


def _write_valid_yaml(path: Path) -> Path:
    path.write_text(_valid_yaml(), encoding="utf-8")
    return path


@pytest.fixture
def fake_renderer(monkeypatch: pytest.MonkeyPatch):
    calls = []

    def render(abrechnung, output_path, **kwargs):
        calls.append((abrechnung, Path(output_path), kwargs))
        Path(output_path).write_bytes(b"%PDF-1.7")
        return Path(output_path)

    monkeypatch.setattr(cli, "render_pdf", render)
    return calls


def test_package_importable() -> None:
    assert yaml_reisekosten_tool.__doc__


def test_cli_help_is_reachable(capsys) -> None:
    exit_code = main([])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "yaml-reisekosten-tool" in captured.out
    assert "EINGABE.yml" in captured.out


def test_module_entrypoint_is_reachable() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "yaml_reisekosten_tool", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "yaml-reisekosten-tool" in result.stdout


def test_cli_renders_valid_input_to_current_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fake_renderer,
    capsys,
) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(input_file)])

    output_path = tmp_path / "2026-01_reisekosten-max-mustermann.pdf"
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == str(output_path)
    assert captured.err == ""
    assert output_path.read_bytes() == b"%PDF-1.7"
    assert fake_renderer[0][1] == output_path


def test_cli_output_dir_writes_to_existing_directory(
    tmp_path: Path,
    fake_renderer,
    capsys,
) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    exit_code = main([str(input_file), "--output-dir", str(output_dir)])

    output_path = output_dir / "2026-01_reisekosten-max-mustermann.pdf"
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == str(output_path)
    assert output_path.is_file()


def test_cli_rejects_invalid_output_dir(tmp_path: Path, capsys) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")

    exit_code = main([str(input_file), "--output-dir", str(tmp_path / "missing")])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Ausgabeverzeichnis existiert nicht" in captured.err


def test_cli_rejects_existing_pdf_without_force(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fake_renderer,
    capsys,
) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    existing_pdf = tmp_path / "2026-01_reisekosten-max-mustermann.pdf"
    existing_pdf.write_bytes(b"old")
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(input_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Ziel-PDF existiert bereits" in captured.err
    assert existing_pdf.read_bytes() == b"old"
    assert fake_renderer == []


def test_cli_force_allows_overwriting_existing_pdf(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fake_renderer,
) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    existing_pdf = tmp_path / "2026-01_reisekosten-max-mustermann.pdf"
    existing_pdf.write_bytes(b"old")
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(input_file), "--force"])

    assert exit_code == 0
    assert existing_pdf.read_bytes() == b"%PDF-1.7"
    assert len(fake_renderer) == 1


def test_build_output_paths_adds_suffix_for_multiple_abrechnungen(tmp_path: Path) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    data = cli.load_yaml_mapping(input_file)
    eingabe = cli.normalize_reisekosten_input(data)
    abrechnung = cli.calculate_reisekosten(eingabe)

    paths = build_output_paths(
        (abrechnung, abrechnung),
        output_dir=tmp_path,
        input_file=input_file,
    )

    assert paths == (
        tmp_path / "2026-01_reisekosten-max-mustermann-01.pdf",
        tmp_path / "2026-01_reisekosten-max-mustermann-02.pdf",
    )


def test_cli_reports_missing_input_file(tmp_path: Path, capsys) -> None:
    exit_code = main([str(tmp_path / "missing.yml")])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "YAML-Datei nicht gefunden" in captured.err


def test_cli_reports_invalid_yaml(tmp_path: Path, capsys) -> None:
    input_file = tmp_path / "broken.yml"
    input_file.write_text("abrechnung: [", encoding="utf-8")

    exit_code = main([str(input_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "YAML-Datei ist ungueltig" in captured.err


def test_cli_reports_validation_error(tmp_path: Path, capsys) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    content = input_file.read_text(encoding="utf-8").replace("  waehrung: EUR\n", "")
    input_file.write_text(content, encoding="utf-8")

    exit_code = main([str(input_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "abrechnung.waehrung" in captured.err


def test_cli_reports_calculation_error(tmp_path: Path, capsys) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    input_file.write_text(_valid_yaml().replace("2026-01", "2027-01"), encoding="utf-8")

    exit_code = main([str(input_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Keine Pauschalentabelle fuer 2027 hinterlegt" in captured.err


def test_cli_reports_render_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    input_file = _write_valid_yaml(tmp_path / "foo.yml")
    monkeypatch.chdir(tmp_path)

    def fail_render(*_args, **_kwargs):
        raise RenderingError("Typst-Rendering ist fehlgeschlagen")

    monkeypatch.setattr(cli, "render_pdf", fail_render)

    exit_code = main([str(input_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Typst-Rendering ist fehlgeschlagen" in captured.err
