"""Safe image-path indexing for dataset audit manifests."""

from __future__ import annotations

from pathlib import Path


def build_image_index(root: Path) -> dict[str, list[Path]]:
    """Index extracted files by both exact filename and extensionless stem."""
    resolved_root = root.resolve()
    if not resolved_root.is_dir():
        raise FileNotFoundError("Image root is missing or is not a directory")

    index: dict[str, list[Path]] = {}
    for path in resolved_root.rglob("*"):
        if not path.is_file():
            continue
        resolved = path.resolve()
        try:
            resolved.relative_to(resolved_root)
        except ValueError as exc:
            raise RuntimeError("Image path escaped extracted root") from exc

        for key in {path.name, path.stem}:
            index.setdefault(key, []).append(resolved)
    return index


def resolve_image_path(
    filename: str,
    root: Path,
    index: dict[str, list[Path]],
) -> Path:
    """Resolve exact paths first, then unique extensionless manifest stems."""
    relative = Path(filename)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Unsafe manifest image path")

    resolved_root = root.resolve()
    direct = (resolved_root / relative).resolve()
    try:
        direct.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("Unsafe manifest image path") from exc
    if direct.is_file():
        return direct

    matches = index.get(relative.name, [])
    if not matches and relative.suffix:
        matches = index.get(relative.stem, [])
    if len(matches) != 1:
        raise FileNotFoundError("Image missing or ambiguous in extracted archive")
    return matches[0]
