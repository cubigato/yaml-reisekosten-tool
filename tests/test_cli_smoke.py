from __future__ import annotations

import subprocess
import sys

import yaml_reisekosten_tool
from yaml_reisekosten_tool.cli import main


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
