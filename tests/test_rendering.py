from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from yaml_reisekosten_tool.calculation import calculate_reisekosten
from yaml_reisekosten_tool.normalization import normalize_reisekosten_input
from yaml_reisekosten_tool.rendering import (
    RenderingError,
    build_render_context,
    render_pdf,
    resolve_template_path,
)
from yaml_reisekosten_tool.yaml_io import load_yaml_mapping


def _example_abrechnung():
    data = load_yaml_mapping(Path("examples/example.yml"))
    eingabe = normalize_reisekosten_input(data)
    return calculate_reisekosten(eingabe)


def test_build_render_context_contains_template_values() -> None:
    context = build_render_context(_example_abrechnung())

    assert context["abrechnung"]["titel"] == "Reisekostenabrechnung"
    assert context["abrechnung"]["zeitraum"] == {"von": "01.01.2026", "bis": "31.03.2026"}
    assert context["mitarbeiter"]["vorname"] == "Max"
    assert context["mitarbeiter"]["nachname"] == "Mustermann"
    assert context["arbeitgeber"]["anschrift"] == "Stadtweg 8, 54321 Musterstadt"
    assert context["reise"]["beginn_datum"] == "08.01.2026"
    assert context["reise"]["ende_datum"] == "05.02.2026"
    assert context["reise"]["privater_pkw"] is True
    assert context["kosten"]["fahrtkosten"] == "130,20"
    assert context["kosten"]["verpflegung"] == "56,00"
    assert context["kosten"]["auslagen"] == "62,00"
    assert context["kosten"]["gesamt"] == "248,20"
    assert context["unterschriften"]["antragsteller"]["name"] == "Max Mustermann"
    assert context["unterschriften"]["antragsteller"]["datum"] == "31.03.2026"
    assert context["unterschriften"]["vorgesetzter"]["name"] == "Erika Leitung"
    assert len(context["reise"]["fahrten"]) == 5


def test_resolve_template_path_uses_package_data_independent_from_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    template = resolve_template_path()

    assert template.name == "reisekosten.typ"
    assert template.is_file()


def test_render_pdf_invokes_typst_with_context_file(tmp_path: Path) -> None:
    output_path = tmp_path / "out.pdf"
    template_path = tmp_path / "template.typ"
    template_path.write_text("#let data = json(sys.inputs.data)", encoding="utf-8")
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        context_path = Path(command[3]) / command[-1].removeprefix("data=")
        context = json.loads(context_path.read_text(encoding="utf-8"))
        assert context["kosten"]["gesamt"] == "248,20"
        applicant_asset = context["unterschriften"]["antragsteller"]["unterschrift_asset"]
        assert applicant_asset == "assets/antragsteller.png"
        assert (Path(command[3]) / applicant_asset).is_file()
        output_path.write_bytes(b"%PDF-1.7")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    rendered = render_pdf(
        _example_abrechnung(),
        output_path,
        typst_binary="typst-test",
        template_path=template_path,
        runner=fake_runner,
    )

    assert rendered == output_path
    assert output_path.read_bytes() == b"%PDF-1.7"
    command, kwargs = calls[0]
    assert command[:2] == ["typst-test", "compile"]
    assert command[2] == "--root"
    assert Path(command[4]).name == template_path.name
    assert command[5] == str(output_path.resolve())
    assert command[6] == "--input"
    assert kwargs == {"check": False, "capture_output": True, "text": True}


def test_render_pdf_reports_missing_typst(tmp_path: Path) -> None:
    template_path = tmp_path / "template.typ"
    template_path.write_text("", encoding="utf-8")

    def missing_runner(*_args, **_kwargs):
        raise FileNotFoundError

    with pytest.raises(RenderingError, match="Typst ist nicht installiert"):
        render_pdf(
            _example_abrechnung(),
            tmp_path / "out.pdf",
            template_path=template_path,
            runner=missing_runner,
        )


def test_render_pdf_reports_missing_template(tmp_path: Path) -> None:
    with pytest.raises(RenderingError, match="Typst-Template fehlt"):
        render_pdf(
            _example_abrechnung(), tmp_path / "out.pdf", template_path=tmp_path / "missing.typ"
        )


def test_render_pdf_reports_failed_typst_process(tmp_path: Path) -> None:
    template_path = tmp_path / "template.typ"
    template_path.write_text("", encoding="utf-8")

    def failing_runner(command, **_kwargs):
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="render failed")

    with pytest.raises(RenderingError, match="render failed"):
        render_pdf(
            _example_abrechnung(),
            tmp_path / "out.pdf",
            template_path=template_path,
            runner=failing_runner,
        )
