"""Local file hashing and inventory generation (no image decoding)."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileRecord:
    """Stable metadata for one file; paths are relative to the inventory root."""

    relative_path: str
    size_bytes: int
    sha256: str
    suffix: str


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Calculate a file's SHA-256 digest using bounded memory."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_files(root: Path, *, exclude_names: set[str] | None = None) -> list[FileRecord]:
    """Inventory regular files recursively in deterministic relative-path order."""
    resolved_root = root.resolve(strict=True)
    if not resolved_root.is_dir():
        raise NotADirectoryError(resolved_root)
    excluded = exclude_names or set()
    records: list[FileRecord] = []
    for path in sorted(resolved_root.rglob("*")):
        if path.is_symlink() or not path.is_file() or path.name in excluded:
            continue
        records.append(
            FileRecord(
                relative_path=path.relative_to(resolved_root).as_posix(),
                size_bytes=path.stat().st_size,
                sha256=sha256_file(path),
                suffix=path.suffix.lower(),
            )
        )
    return records


def write_inventory_json(path: Path, records: list[FileRecord]) -> None:
    """Write inventory JSON; refuse to overwrite an existing report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump([asdict(record) for record in records], handle, indent=2)
        handle.write("\n")


def write_inventory_csv(path: Path, records: list[FileRecord]) -> None:
    """Write inventory CSV; refuse to overwrite an existing report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(FileRecord.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)
