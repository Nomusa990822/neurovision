"""Archive inspection and defensive ZIP/TAR extraction helpers."""

from __future__ import annotations

import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


@dataclass(frozen=True, slots=True)
class ArchiveMember:
    name: str
    size_bytes: int
    is_directory: bool


def _safe_relative_name(name: str) -> PurePosixPath:
    normalized = name.replace("\\", "/")
    candidate = PurePosixPath(normalized)
    if (
        candidate.is_absolute()
        or not candidate.parts
        or any(part in {"", ".", ".."} for part in candidate.parts)
    ):
        raise ValueError(f"Unsafe archive member path: {name!r}")
    if candidate.parts[0].endswith(":"):
        raise ValueError(f"Unsafe archive member path: {name!r}")
    return candidate


def inspect_archive(path: Path) -> list[ArchiveMember]:
    """List ZIP or TAR members and reject unsafe paths and special files."""
    members: list[ArchiveMember] = []
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for zip_member in archive.infolist():
                name = zip_member.filename.rstrip("/")
                if name:
                    _safe_relative_name(name)
                mode = (zip_member.external_attr >> 16) & 0o170000
                if mode == 0o120000:
                    raise ValueError(
                        f"Symbolic links are not allowed in archives: {zip_member.filename}"
                    )
                members.append(
                    ArchiveMember(zip_member.filename, zip_member.file_size, zip_member.is_dir())
                )
        return members
    if tarfile.is_tarfile(path):
        with tarfile.open(path, "r:*") as archive:
            for tar_member in archive.getmembers():
                name = tar_member.name.rstrip("/")
                if name:
                    _safe_relative_name(name)
                if not (tar_member.isfile() or tar_member.isdir()):
                    raise ValueError(f"Special TAR members are not allowed: {tar_member.name}")
                members.append(
                    ArchiveMember(tar_member.name, tar_member.size, tar_member.isdir())
                )
        return members
    raise ValueError(f"Unsupported or invalid archive: {path}")


def safe_extract_archive(
    archive_path: Path,
    destination: Path,
    *,
    max_members: int = 200_000,
    max_total_bytes: int = 100 * 1024**3,
) -> int:
    """Extract ZIP/TAR to a new empty destination after validating every member."""
    if max_members <= 0 or max_total_bytes <= 0:
        raise ValueError("Extraction limits must be positive")
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"Destination must be empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    members = inspect_archive(archive_path)
    files = [member for member in members if not member.is_directory]
    if len(members) > max_members:
        raise ValueError("Archive exceeds maximum member count")
    if sum(member.size_bytes for member in files) > max_total_bytes:
        raise ValueError("Archive exceeds maximum uncompressed size")

    root = destination.resolve()
    extracted_bytes = 0
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path) as archive:
            for zip_member in archive.infolist():
                name = zip_member.filename.rstrip("/")
                if not name:
                    continue
                target = (root / Path(*_safe_relative_name(name).parts)).resolve()
                if root not in target.parents and target != root:
                    raise ValueError(
                        f"Archive member escapes destination: {zip_member.filename}"
                    )
                if zip_member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(zip_member) as zip_source, target.open("xb") as output:
                    while chunk := zip_source.read(1024 * 1024):
                        extracted_bytes += len(chunk)
                        if extracted_bytes > max_total_bytes:
                            raise ValueError(
                                "Archive exceeds maximum uncompressed size while extracting"
                            )
                        output.write(chunk)
    else:
        with tarfile.open(archive_path, "r:*") as archive:
            for tar_member in archive.getmembers():
                name = tar_member.name.rstrip("/")
                if not name:
                    continue
                relative = _safe_relative_name(name)
                target = (root / Path(*relative.parts)).resolve()
                if root not in target.parents and target != root:
                    raise ValueError(f"Archive member escapes destination: {tar_member.name}")
                if tar_member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                tar_source = archive.extractfile(tar_member)
                if tar_source is None:
                    raise ValueError(f"Could not read archive member: {tar_member.name}")
                target.parent.mkdir(parents=True, exist_ok=True)
                with tar_source, target.open("xb") as output:
                    while chunk := tar_source.read(1024 * 1024):
                        extracted_bytes += len(chunk)
                        if extracted_bytes > max_total_bytes:
                            raise ValueError(
                                "Archive exceeds maximum uncompressed size while extracting"
                            )
                        output.write(chunk)
    return len(files)
