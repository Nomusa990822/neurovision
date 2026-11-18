from __future__ import annotations

import csv

import pytest

from neurovision.datasets.duplicate_review import create_duplicate_review_pack


def _write_image(path, colour: tuple[int, int, int]) -> None:
    image_module = pytest.importorskip("PIL.Image")
    image = image_module.new("RGB", (90, 28), colour)
    image.save(path, format="PNG")


def test_review_pack_is_blinded_and_private(tmp_path) -> None:
    pytest.importorskip("PIL.Image")
    images = tmp_path / "images"
    images.mkdir()
    _write_image(images / "a.png", (10, 20, 30))
    _write_image(images / "b.png", (40, 50, 60))

    pairs = tmp_path / "pairs.csv"
    fields = [
        "left_file_name", "right_file_name", "left_patient_id",
        "right_patient_id", "left_disease", "right_disease",
        "hamming_distance", "cross_patient",
    ]
    with pairs.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "left_file_name": "a.jpg", "right_file_name": "b.jpg",
            "left_patient_id": "PRIVATE-1", "right_patient_id": "PRIVATE-2",
            "left_disease": "AMD", "right_disease": "DME",
            "hamming_distance": 0, "cross_patient": "True",
        })
        writer.writerow({
            "left_file_name": "a.jpg", "right_file_name": "b.jpg",
            "left_patient_id": "PRIVATE-1", "right_patient_id": "PRIVATE-2",
            "left_disease": "AMD", "right_disease": "DME",
            "hamming_distance": 3, "cross_patient": "True",
        })

    output = tmp_path / "review"
    result = create_duplicate_review_pack(pairs, images, output)
    assert result["candidate_pair_count"] == 1
    assert result["contact_sheet_count"] == 1
    assert (output / "contact-sheet-001.png").is_file()
    assert output.stat().st_mode & 0o777 == 0o700
    assert (output / "review-register.csv").stat().st_mode & 0o777 == 0o600
    register = (output / "review-register.csv").read_text()
    assert "PRIVATE-1" not in register
    assert "AMD" not in register
    manifest = (output / "private-pair-manifest.csv").read_text()
    assert "PRIVATE-1" in manifest
    assert "AMD" in manifest
    with pytest.raises(FileExistsError):
        create_duplicate_review_pack(pairs, images, output)


def test_review_pack_rejects_missing_image(tmp_path) -> None:
    images = tmp_path / "images"
    images.mkdir()
    pairs = tmp_path / "pairs.csv"
    pairs.write_text(
        "left_file_name,right_file_name,left_patient_id,right_patient_id,"
        "left_disease,right_disease,hamming_distance,cross_patient\\n"
        "missing.jpg,also-missing.jpg,P1,P2,AMD,DME,0,True\\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="exactly one extracted image"):
        create_duplicate_review_pack(pairs, images, tmp_path / "review")
