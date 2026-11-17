"""Project-root and data-path resolution helpers."""

from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """Find the repository root by locating its pyproject.toml marker."""
    current = (start or Path(__file__)).expanduser().resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate

    raise FileNotFoundError(f"Could not locate project root from: {current}")


def resolve_data_dir(configured_path: Path, project_root: Path | None = None) -> Path:
    """Resolve a configured data path relative to the project root if not absolute."""
    if configured_path.is_absolute():
        return configured_path.resolve()

    root = (project_root or find_project_root()).resolve()
    return (root / configured_path).resolve()
