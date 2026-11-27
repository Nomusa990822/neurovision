from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pytest
from PIL import Image, ImageDraw

SCRIPT_PATH = (
    Path(__file__).resolve().parents[3]
    / "scripts"
    / "audits"
    / "nonzero_candidate_investigation.py"
)
SPEC = importlib.util.spec_from_file_location("nonzero_candidate_investigation", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def _write_fixture(path: Path, offset: int) -> None:
    width, height = 384, 256
    y, x = np.mgrid[0:height, 0:width]
    base = 220 + 16 * np.sin((x + offset) / 17) + 9 * np.cos(y / 11)
    pixels = np.clip(base, 0, 255).astype(np.uint8)
    image = Image.fromarray(pixels).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.ellipse((35 + offset, 55, 345, 205), outline=(75, 75, 75), width=3)
    draw.arc((80, 70, 310, 190), start=190, end=350, fill=(35, 35, 35), width=4)
    draw.line((15, 128 + offset % 9, 369, 128 + offset % 9), fill=(105, 105, 105), width=2)
    image.save(path, format="PNG")


def _write_inputs(root: Path, count: int = 10) -> tuple[Path, Path]:
    image_root = root / "images"
    image_root.mkdir()
    manifest_rows = []
    review_rows = []
    for index in range(count):
        pair_id = f"PAIR-TEST-{index:04d}"
        left_stem = f"left_{index:04d}"
        right_stem = f"right_{index:04d}"
        _write_fixture(image_root / f"{left_stem}.png", index)
        if index == 0:
            (image_root / f"{right_stem}.png").write_bytes(
                (image_root / f"{left_stem}.png").read_bytes()
            )
        else:
            _write_fixture(image_root / f"{right_stem}.png", index + 2)
        manifest_rows.append(
            {
                "pair_id": pair_id,
                "hamming_distance": "2",
                "left_file_name": left_stem,
                "right_file_name": right_stem,
                "left_patient_id": f"patient_left_{index}",
                "right_patient_id": f"patient_right_{index}",
            }
        )
        review_rows.append(
            {
                "pair_id": pair_id,
                "hamming_distance": "2",
                "visual_disposition": "potential_duplicate",
                "confidence": "High",
            }
        )
    manifest = root / "manifest.csv"
    review = root / "review.csv"
    pd.DataFrame(manifest_rows).to_csv(manifest, index=False)
    pd.DataFrame(review_rows).to_csv(review, index=False)
    return manifest, review


def test_affine_warp_uses_inverse_transform_to_align_right_to_left() -> None:
    reference = np.full((AUDIT.CANVAS, AUDIT.CANVAS), 255, dtype=np.uint8)
    reference[150:230, 170:260] = 40
    reference[175:205, 195:235] = 10

    left_to_right = np.array([[1.0, 0.0, 7.0], [0.0, 1.0, -5.0]], dtype=np.float32)
    right = cv2.warpAffine(
        reference,
        left_to_right,
        (AUDIT.CANVAS, AUDIT.CANVAS),
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )

    baseline_ssim = AUDIT.structural_similarity(reference, right, data_range=255)
    aligned = AUDIT.warp_to_left_reference(right, left_to_right)
    aligned_ssim = AUDIT.structural_similarity(reference, aligned, data_range=255)

    assert aligned_ssim > baseline_ssim
    assert np.array_equal(reference, aligned)


def test_full_audit_pipeline_processes_synthetic_pairs(tmp_path, monkeypatch) -> None:
    manifest, review = _write_inputs(tmp_path)
    pair_ids = {f"PAIR-TEST-{index:04d}" for index in range(10)}
    monkeypatch.setattr(AUDIT, "TARGET_PAIRS", pair_ids)
    output = tmp_path / "reports"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "nonzero_candidate_investigation.py",
            "--image-root",
            str(tmp_path / "images"),
            "--manifest",
            str(manifest),
            "--review-register",
            str(review),
            "--output",
            str(output),
        ],
    )

    assert AUDIT.main() == 0

    summary = json.loads((output / "investigation-summary.json").read_text())
    assert summary["selected_candidates"] == 10
    assert summary["successfully_processed"] == 10
    assert summary["processing_errors"] == 0
    assert summary["byte_identical_pairs"] == 1
    assert summary["decoded_rgb_pixel_identical_pairs"] == 1

    register = pd.read_csv(output / "anonymised-computational-register.csv")
    assert len(register) == 10
    assert set(register["pair_id"]) == pair_ids
    assert not {"left_file_name", "right_file_name", "left_patient_id", "right_patient_id"} & set(
        register.columns
    )
    assert not any("patient_" in str(value) for value in register.to_numpy().ravel())


def test_audit_rejects_selected_pair_without_completed_visual_review(tmp_path, monkeypatch) -> None:
    manifest, review = _write_inputs(tmp_path, count=1)
    review_frame = pd.read_csv(review)
    review_frame.loc[0, "confidence"] = ""
    review_frame.to_csv(review, index=False)
    monkeypatch.setattr(AUDIT, "TARGET_PAIRS", {"PAIR-TEST-0000"})
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "nonzero_candidate_investigation.py",
            "--image-root",
            str(tmp_path / "images"),
            "--manifest",
            str(manifest),
            "--review-register",
            str(review),
            "--output",
            str(tmp_path / "reports"),
        ],
    )

    with pytest.raises(SystemExit, match="incomplete confidence values"):
        AUDIT.main()


def test_preflight_rejects_missing_image_before_analysis(tmp_path, monkeypatch) -> None:
    manifest, review = _write_inputs(tmp_path, count=1)
    (tmp_path / "images" / "right_0000.png").unlink()
    monkeypatch.setattr(AUDIT, "TARGET_PAIRS", {"PAIR-TEST-0000"})
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "nonzero_candidate_investigation.py",
            "--image-root",
            str(tmp_path / "images"),
            "--manifest",
            str(manifest),
            "--review-register",
            str(review),
            "--output",
            str(tmp_path / "reports"),
        ],
    )

    with pytest.raises(SystemExit, match="Selected candidate image preflight failed"):
        AUDIT.main()
