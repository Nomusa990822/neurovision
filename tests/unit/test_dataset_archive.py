from __future__ import annotations

import tarfile
import zipfile

import pytest

from neurovision.datasets.archive import inspect_archive, safe_extract_archive


def test_zip_inspection_and_safe_extraction(tmp_path) -> None:
    archive_path = tmp_path / "sample.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("images/a.txt", "sample")
    members = inspect_archive(archive_path)
    assert len(members) == 1
    destination = tmp_path / "extracted"
    assert safe_extract_archive(archive_path, destination) == 1
    assert (destination / "images" / "a.txt").read_text() == "sample"


def test_zip_path_traversal_is_rejected(tmp_path) -> None:
    archive_path = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("../escape.txt", "bad")
    with pytest.raises(ValueError, match="Unsafe archive"):
        inspect_archive(archive_path)


def test_tar_special_file_is_rejected(tmp_path) -> None:
    archive_path = tmp_path / "unsafe.tar"
    with tarfile.open(archive_path, "w") as archive:
        info = tarfile.TarInfo("link")
        info.type = tarfile.SYMTYPE
        info.linkname = "target"
        archive.addfile(info)
    with pytest.raises(ValueError, match="Special TAR"):
        inspect_archive(archive_path)


def test_extraction_limits_and_nonempty_destination(tmp_path) -> None:
    archive_path = tmp_path / "sample.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("a.txt", "12345")
    with pytest.raises(ValueError, match="uncompressed size"):
        safe_extract_archive(archive_path, tmp_path / "limited", max_total_bytes=2)
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    (occupied / "existing").touch()
    with pytest.raises(FileExistsError):
        safe_extract_archive(archive_path, occupied)
