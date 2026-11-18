from __future__ import annotations

import csv
import hashlib

import pytest

from neurovision.datasets.duplicates import (
    hamming_distance,
    run_duplicate_screen,
    sha256_file,
)


def _write_image(path, colour: tuple[int, int, int]) -> None:
    image_module = pytest.importorskip("PIL.Image")
    image = image_module.new("RGB", (32, 24), colour)
    image.save(path, format="PNG")


def _write_labels(path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file_name", "patient_id", "disease"])
        writer.writeheader()
        writer.writerows(rows)


def test_sha256_file_matches_standard_digest(tmp_path) -> None:
    path = tmp_path / "sample.bin"
    path.write_bytes(b"neurovision")
    assert sha256_file(path) == hashlib.sha256(b"neurovision").hexdigest()


def test_hamming_distance_counts_different_bits() -> None:
    assert hamming_distance(0b1010, 0b0011) == 2


def test_duplicate_screen_reports_exact_cross_patient_duplicates(tmp_path) -> None:
    pytest.importorskip("PIL.Image")
    images = tmp_path / "images"
    images.mkdir()
    _write_image(images / "a.png", (10, 20, 30))
    (images / "b.png").write_bytes((images / "a.png").read_bytes())
    labels = tmp_path / "labels.csv"
    _write_labels(
        labels,
        [
            {"file_name": "a.jpg", "patient_id": "P1", "disease": "AMD"},
            {"file_name": "b.jpg", "patient_id": "P2", "disease": "DME"},
        ],
    )
    report_path = tmp_path / "report.json"
    pairs_path = tmp_path / "pairs.csv"
    report = run_duplicate_screen(labels, images, report_path, pairs_path)
    assert report["image_record_count"] == 2
    assert report["exact_duplicate_group_count"] == 1
    assert report["exact_cross_patient_group_count"] == 1
    assert report["near_duplicate_candidate_pair_count"] == 0
    assert report_path.stat().st_mode & 0o777 == 0o600
    assert pairs_path.stat().st_mode & 0o777 == 0o600
    with pytest.raises(FileExistsError):
        run_duplicate_screen(labels, images, report_path, pairs_path)


def test_duplicate_screen_rejects_ambiguous_image_stem(tmp_path) -> None:
    pytest.importorskip("PIL.Image")
    images = tmp_path / "images"
    images.mkdir()
    _write_image(images / "a.png", (10, 20, 30))
    _write_image(images / "a.jpg", (30, 20, 10))
    labels = tmp_path / "labels.csv"
    _write_labels(labels, [{"file_name": "a.tif", "patient_id": "P1", "disease": "AMD"}])
    with pytest.raises(ValueError, match="exactly one image"):
        run_duplicate_screen(labels, images, tmp_path / "report.json", tmp_path / "pairs.csv")
