from __future__ import annotations

import stat

import pytest

from yaml_reisekosten_tool.yaml_io import (
    EmptyYamlFileError,
    InvalidYamlError,
    YamlFileMissingError,
    YamlFileUnreadableError,
    YamlRootNotMappingError,
    load_yaml_mapping,
)


def test_load_yaml_mapping_returns_raw_mapping(tmp_path) -> None:
    input_file = tmp_path / "reise.yml"
    input_file.write_text("abrechnung:\n  titel: Test\n", encoding="utf-8")

    data = load_yaml_mapping(input_file)

    assert data == {"abrechnung": {"titel": "Test"}}


def test_load_yaml_mapping_distinguishes_missing_file(tmp_path) -> None:
    with pytest.raises(YamlFileMissingError):
        load_yaml_mapping(tmp_path / "missing.yml")


def test_load_yaml_mapping_distinguishes_unreadable_file(tmp_path) -> None:
    input_file = tmp_path / "unreadable.yml"
    input_file.write_text("abrechnung: {}\n", encoding="utf-8")
    input_file.chmod(0)

    try:
        with pytest.raises(YamlFileUnreadableError):
            load_yaml_mapping(input_file)
    finally:
        input_file.chmod(stat.S_IRUSR | stat.S_IWUSR)


def test_load_yaml_mapping_distinguishes_empty_file(tmp_path) -> None:
    input_file = tmp_path / "empty.yml"
    input_file.write_text("   \n", encoding="utf-8")

    with pytest.raises(EmptyYamlFileError):
        load_yaml_mapping(input_file)


def test_load_yaml_mapping_distinguishes_yaml_null(tmp_path) -> None:
    input_file = tmp_path / "null.yml"
    input_file.write_text("null\n", encoding="utf-8")

    with pytest.raises(EmptyYamlFileError):
        load_yaml_mapping(input_file)


def test_load_yaml_mapping_distinguishes_invalid_yaml(tmp_path) -> None:
    input_file = tmp_path / "invalid.yml"
    input_file.write_text("abrechnung: [\n", encoding="utf-8")

    with pytest.raises(InvalidYamlError):
        load_yaml_mapping(input_file)


def test_load_yaml_mapping_distinguishes_non_mapping_root(tmp_path) -> None:
    input_file = tmp_path / "list.yml"
    input_file.write_text("- one\n- two\n", encoding="utf-8")

    with pytest.raises(YamlRootNotMappingError):
        load_yaml_mapping(input_file)
