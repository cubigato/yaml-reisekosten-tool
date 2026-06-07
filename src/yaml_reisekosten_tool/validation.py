"""Fachliche Validierung der rohen YAML-Struktur."""

from __future__ import annotations


class ValidationError(ValueError):
    """Ein erwartbarer Validierungsfehler mit YAML-Feldpfad."""

    def __init__(self, field_path: str, problem: str) -> None:
        self.field_path = field_path
        self.problem = problem
        super().__init__(f"{field_path}: {problem}")
