from pathlib import Path

import pytest

from neurovision.config import Settings, get_settings


def test_settings_use_safe_defaults(clean_neurovision_environment: None) -> None:
    settings = Settings.from_environment()

    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.data_dir == Path("data")


def test_environment_overrides_settings(
    clean_neurovision_environment: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NEUROVISION_ENVIRONMENT", "testing")
    monkeypatch.setenv("NEUROVISION_LOG_LEVEL", "debug")
    monkeypatch.setenv("NEUROVISION_DATA_DIR", "/tmp/neurovision-data")

    settings = get_settings()

    assert settings.environment == "testing"
    assert settings.log_level == "DEBUG"
    assert settings.data_dir == Path("/tmp/neurovision-data")


@pytest.mark.parametrize("value", ["", "staging", "prod", "Development!"])
def test_invalid_environment_is_rejected(
    clean_neurovision_environment: None, monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    monkeypatch.setenv("NEUROVISION_ENVIRONMENT", value)

    with pytest.raises(ValueError, match="NEUROVISION_ENVIRONMENT"):
        Settings.from_environment()


def test_invalid_log_level_is_rejected(
    clean_neurovision_environment: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NEUROVISION_LOG_LEVEL", "TRACE")

    with pytest.raises(ValueError, match="NEUROVISION_LOG_LEVEL"):
        Settings.from_environment()


def test_empty_data_directory_is_rejected(
    clean_neurovision_environment: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NEUROVISION_DATA_DIR", "   ")

    with pytest.raises(ValueError, match="NEUROVISION_DATA_DIR"):
        Settings.from_environment()
