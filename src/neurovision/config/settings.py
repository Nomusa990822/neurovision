"""Validated environment-backed application settings.

The initial configuration layer uses only the Python standard library. This keeps
the engineering scaffold small; richer validation can be introduced when a real
configuration schema requires it.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Environment = Literal["development", "testing", "production"]
_ALLOWED_LOG_LEVELS = frozenset({"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"})


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable application settings loaded from the process environment."""

    environment: Environment = "development"
    log_level: str = "INFO"
    data_dir: Path = Path("data")

    @classmethod
    def from_environment(cls) -> Settings:
        """Build settings from NEUROVISION_* variables and validate their values."""
        raw_environment = os.getenv("NEUROVISION_ENVIRONMENT", "development").strip().lower()
        if raw_environment not in {"development", "testing", "production"}:
            raise ValueError("NEUROVISION_ENVIRONMENT must be development, testing or production")

        log_level = os.getenv("NEUROVISION_LOG_LEVEL", "INFO").strip().upper()
        if log_level not in _ALLOWED_LOG_LEVELS:
            allowed = ", ".join(sorted(_ALLOWED_LOG_LEVELS))
            raise ValueError(f"NEUROVISION_LOG_LEVEL must be one of: {allowed}")

        raw_data_dir = os.getenv("NEUROVISION_DATA_DIR", "data").strip()
        if not raw_data_dir:
            raise ValueError("NEUROVISION_DATA_DIR must not be empty")

        return cls(
            environment=raw_environment,  # type: ignore[arg-type]
            log_level=log_level,
            data_dir=Path(raw_data_dir).expanduser(),
        )


def get_settings() -> Settings:
    """Return settings for the current process."""
    return Settings.from_environment()
