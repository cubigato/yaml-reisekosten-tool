"""YAML-Dateien laden und reine Ladefehler unterscheiden."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml


class YamlLoadError(Exception):
    """Basisklasse fuer erwartbare YAML-Ladefehler."""

    def __init__(self, path: Path, message: str) -> None:
        self.path = path
        super().__init__(message)


class YamlFileMissingError(YamlLoadError):
    """Die Eingabedatei existiert nicht."""


class YamlFileUnreadableError(YamlLoadError):
    """Die Eingabedatei kann nicht gelesen werden."""


class EmptyYamlFileError(YamlLoadError):
    """Die Eingabedatei ist leer oder enthaelt nur YAML-null."""


class InvalidYamlError(YamlLoadError):
    """Die Eingabedatei enthaelt kein gueltiges YAML."""


class YamlRootNotMappingError(YamlLoadError):
    """Die YAML-Wurzel ist kein Mapping."""


def load_yaml_mapping(path: str | Path) -> Mapping[str, Any]:
    """Lade eine YAML-Datei sicher und gib das rohe Root-Mapping zurueck."""

    yaml_path = Path(path)

    try:
        content = yaml_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        msg = f"YAML-Datei nicht gefunden: {yaml_path}"
        raise YamlFileMissingError(yaml_path, msg) from exc
    except OSError as exc:
        msg = f"YAML-Datei kann nicht gelesen werden: {yaml_path}"
        raise YamlFileUnreadableError(yaml_path, msg) from exc

    if not content.strip():
        msg = f"YAML-Datei ist leer: {yaml_path}"
        raise EmptyYamlFileError(yaml_path, msg)

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        msg = f"YAML-Datei ist ungueltig: {yaml_path}"
        raise InvalidYamlError(yaml_path, msg) from exc

    if data is None:
        msg = f"YAML-Datei ist leer: {yaml_path}"
        raise EmptyYamlFileError(yaml_path, msg)

    if not isinstance(data, Mapping):
        msg = f"YAML-Wurzel muss ein Mapping sein: {yaml_path}"
        raise YamlRootNotMappingError(yaml_path, msg)

    return data
