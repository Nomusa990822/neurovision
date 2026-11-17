"""Shared pytest fixtures for NeuroVision tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def clean_neurovision_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove NeuroVision environment overrides for isolated settings tests."""
    for key in (
        "NEUROVISION_ENVIRONMENT",
        "NEUROVISION_LOG_LEVEL",
        "NEUROVISION_DATA_DIR",
    ):
        monkeypatch.delenv(key, raising=False)
