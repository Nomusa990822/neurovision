from pathlib import Path

import pytest

from neurovision.utils.paths import find_project_root, resolve_data_dir


def test_find_project_root_from_nested_directory(tmp_path: Path) -> None:
    root = tmp_path / "project"
    nested = root / "src" / "neurovision"
    nested.mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname='sample'\n", encoding="utf-8")

    assert find_project_root(nested) == root.resolve()


def test_find_project_root_fails_without_marker(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Could not locate project root"):
        find_project_root(tmp_path)


def test_resolve_relative_data_path_from_project_root(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()

    assert resolve_data_dir(Path("data/raw"), root) == (root / "data/raw").resolve()


def test_absolute_data_path_is_preserved(tmp_path: Path) -> None:
    absolute = tmp_path / "external-data"

    assert resolve_data_dir(absolute, tmp_path / "project") == absolute.resolve()
