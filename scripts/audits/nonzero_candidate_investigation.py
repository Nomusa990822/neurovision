#!/usr/bin/env python3
"""Private OCTDL nonzero-dHash candidate investigation.

Outputs contain pair IDs and aggregate image-comparison measurements only.
No filenames, patient identifiers, image pixels, or source metadata are exported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from scipy.ndimage import shift as ndi_shift
from skimage.metrics import structural_similarity
from skimage.registration import phase_cross_correlation


TARGET_PAIRS = {
    "PAIR-NZ-0021",
    "PAIR-NZ-0043",
    "PAIR-NZ-0046",
    "PAIR-NZ-0079",
    "PAIR-NZ-0080",
    "PAIR-NZ-0086",
    "PAIR-NZ-0088",
    "PAIR-NZ-0095",
    "PAIR-NZ-0108",
    "PAIR-NZ-0140",
}
CANVAS = 512
SIFT_RATIO = 0.75
MIN_SIFT_MATCHES = 8
MIN_INLIERS = 6


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_index(root: Path) -> dict[str, list[Path]]:
    root = root.resolve()
    result: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if path.is_file():
            resolved = path.resolve()
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise RuntimeError("Image path escaped extracted root") from exc
            result.setdefault(path.name, []).append(resolved)
    return result


def resolve_image(filename: str, root: Path, index: dict[str, list[Path]]) -> Path:
    relative = Path(filename)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Unsafe manifest image path")
    direct = (root / relative).resolve()
    direct.relative_to(root.resolve())
    if direct.is_file():
        return direct
    matches = index.get(relative.name, [])
    if len(matches) != 1:
        raise FileNotFoundError("Image missing or ambiguous in extracted archive")
    return matches[0]


def read_rgb(path: Path) -> tuple[np.ndarray, dict[str, object]]:
    with Image.open(path) as image:
        image.load()
        metadata = {
            "width": int(image.width),
            "height": int(image.height),
            "mode": str(image.mode),
            "format": str(image.format or "UNKNOWN"),
        }
        rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    return rgb, metadata


def normalise(rgb: np.ndarray) -> np.ndarray:
    h, w = rgb.shape[:2]
    scale = min(CANVAS / w, CANVAS / h)
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    resized = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA)
    canvas = np.full((CANVAS, CANVAS, 3), 255, dtype=np.uint8)
    x = (CANVAS - nw) // 2
    y = (CANVAS - nh) // 2
    canvas[y : y + nh, x : x + nw] = resized
    return cv2.cvtColor(canvas, cv2.COLOR_RGB2GRAY)


def tissue_mask(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return ((a < 245) | (b < 245)).astype(np.uint8) * 255


def masked_mae(a: np.ndarray, b: np.ndarray, mask: np.ndarray) -> float | None:
    if int(np.count_nonzero(mask)) < 100:
        return None
    return float(np.mean(np.abs(a.astype(np.float32) - b.astype(np.float32))[mask > 0]))


def feature_metrics(a: np.ndarray, b: np.ndarray) -> dict[str, object]:
    sift = cv2.SIFT_create(nfeatures=2500)
    key_a, desc_a = sift.detectAndCompute(a, None)
    key_b, desc_b = sift.detectAndCompute(b, None)
    result: dict[str, object] = {
        "sift_keypoints_left": len(key_a),
        "sift_keypoints_right": len(key_b),
        "sift_ratio_matches": 0,
        "sift_inliers": 0,
        "sift_inlier_ratio": None,
        "affine_scale": None,
        "affine_rotation_degrees": None,
        "affine_translation_x": None,
        "affine_translation_y": None,
        "affine_determinant": None,
        "affine_plausible": False,
        "orb_keypoints_left": 0,
        "orb_keypoints_right": 0,
        "orb_ratio_matches": 0,
    }
    if desc_a is None or desc_b is None or len(desc_a) < 2 or len(desc_b) < 2:
        return result

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    pairs = matcher.knnMatch(desc_a, desc_b, k=2)
    good = [
        m
        for pair in pairs
        if len(pair) == 2
        for m, n in [pair]
        if m.distance < SIFT_RATIO * n.distance
    ]
    result["sift_ratio_matches"] = len(good)

    if len(good) >= MIN_SIFT_MATCHES:
        src = np.float32([key_a[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([key_b[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        matrix, inliers = cv2.estimateAffinePartial2D(
            src,
            dst,
            method=cv2.RANSAC,
            ransacReprojThreshold=3.0,
            maxIters=5000,
            confidence=0.99,
            refineIters=20,
        )
        if matrix is not None and inliers is not None:
            count = int(np.count_nonzero(inliers))
            ratio = count / len(good)
            a00, a01 = float(matrix[0, 0]), float(matrix[0, 1])
            scale = float(np.hypot(a00, a01))
            rotation = float(np.degrees(np.arctan2(a01, a00)))
            determinant = float(np.linalg.det(matrix[:, :2]))
            tx, ty = float(matrix[0, 2]), float(matrix[1, 2])
            plausible = (
                count >= MIN_INLIERS
                and ratio >= 0.25
                and 0.80 <= scale <= 1.25
                and abs(rotation) <= 15
                and abs(tx) <= 0.35 * CANVAS
                and abs(ty) <= 0.35 * CANVAS
                and 0.64 <= abs(determinant) <= 1.56
            )
            result.update(
                {
                    "sift_inliers": count,
                    "sift_inlier_ratio": ratio,
                    "affine_scale": scale,
                    "affine_rotation_degrees": rotation,
                    "affine_translation_x": tx,
                    "affine_translation_y": ty,
                    "affine_determinant": determinant,
                    "affine_plausible": bool(plausible),
                }
            )

    orb = cv2.ORB_create(nfeatures=2500)
    orb_a, orb_desc_a = orb.detectAndCompute(a, None)
    orb_b, orb_desc_b = orb.detectAndCompute(b, None)
    result["orb_keypoints_left"] = len(orb_a)
    result["orb_keypoints_right"] = len(orb_b)
    if (
        orb_desc_a is not None
        and orb_desc_b is not None
        and len(orb_desc_a) >= 2
        and len(orb_desc_b) >= 2
    ):
        orb_pairs = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(orb_desc_a, orb_desc_b, k=2)
        orb_good = [
            m
            for pair in orb_pairs
            if len(pair) == 2
            for m, n in [pair]
            if m.distance < 0.75 * n.distance
        ]
        result["orb_ratio_matches"] = len(orb_good)
    return result


def analyse(
    row: dict[str, str], review: dict[str, str], root: Path, index: dict[str, list[Path]]
) -> dict[str, object]:
    left_path = resolve_image(row["left_file_name"], root, index)
    right_path = resolve_image(row["right_file_name"], root, index)
    left_rgb, left_meta = read_rgb(left_path)
    right_rgb, right_meta = read_rgb(right_path)
    same_dimensions = left_rgb.shape == right_rgb.shape
    pixel_equal = bool(same_dimensions and np.array_equal(left_rgb, right_rgb))
    left_sha, right_sha = sha256(left_path), sha256(right_path)

    a, b = normalise(left_rgb), normalise(right_rgb)
    mask = tissue_mask(a, b)
    baseline_mae = masked_mae(a, b, mask)
    baseline_ssim = float(structural_similarity(a, b, data_range=255))

    # Subpixel translation registration via scikit-image; interpolation is
    # performed by SciPy. This is translation-only and does not prove identity.
    phase_shift, phase_error, phase_difference = phase_cross_correlation(
        a, b, upsample_factor=10, normalization="phase"
    )
    phase_aligned = ndi_shift(
        b, shift=phase_shift, order=1, mode="constant", cval=255, prefilter=False
    )
    phase_mask = tissue_mask(a, phase_aligned)
    phase_mae = masked_mae(a, phase_aligned, phase_mask)
    phase_ssim = float(structural_similarity(a, phase_aligned, data_range=255))

    features = feature_metrics(a, b)
    affine_ssim = None
    affine_mae = None
    affine_tissue_overlap = None

    if features["affine_plausible"]:
        sift = cv2.SIFT_create(nfeatures=2500)
        ka, da = sift.detectAndCompute(a, None)
        kb, db = sift.detectAndCompute(b, None)
        matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(da, db, k=2)
        good = [
            m
            for pair in matches
            if len(pair) == 2
            for m, n in [pair]
            if m.distance < SIFT_RATIO * n.distance
        ]
        src = np.float32([ka[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([kb[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        matrix, inliers = cv2.estimateAffinePartial2D(
            src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0,
            maxIters=5000, confidence=0.99, refineIters=20,
        )
        if matrix is not None:
            warped = cv2.warpAffine(
                b,
                matrix,
                (CANVAS, CANVAS),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=255,
            )
            warped_mask = tissue_mask(a, warped)
            affine_mae = masked_mae(a, warped, warped_mask)
            affine_ssim = float(structural_similarity(a, warped, data_range=255))
            affine_tissue_overlap = int(np.count_nonzero(warped_mask))

    if left_meta["width"] > 0 and left_meta["height"] > 0:
        left_aspect = left_meta["width"] / left_meta["height"]
        right_aspect = right_meta["width"] / right_meta["height"]
        aspect_ratio_delta = abs(left_aspect - right_aspect)
    else:
        aspect_ratio_delta = None

    return {
        "pair_id": row["pair_id"],
        "dhash_hamming_distance": int(row["hamming_distance"]),
        "visual_disposition": review["visual_disposition"],
        "review_confidence": review["confidence"],
        "cross_patient": row["left_patient_id"] != row["right_patient_id"],
        "left_width": left_meta["width"],
        "left_height": left_meta["height"],
        "right_width": right_meta["width"],
        "right_height": right_meta["height"],
        "left_format": left_meta["format"],
        "right_format": right_meta["format"],
        "left_mode": left_meta["mode"],
        "right_mode": right_meta["mode"],
        "dimensions_equal": same_dimensions,
        "aspect_ratio_absolute_difference": aspect_ratio_delta,
        "byte_identical": left_sha == right_sha,
        "decoded_rgb_pixel_identical": pixel_equal,
        "baseline_tissue_mae": baseline_mae,
        "baseline_ssim": baseline_ssim,
        "phase_translation_y": float(phase_shift[0]),
        "phase_translation_x": float(phase_shift[1]),
        "phase_registration_error": float(phase_error),
        "phase_registration_difference": float(phase_difference),
        "phase_registered_tissue_mae": phase_mae,
        "phase_registered_ssim": phase_ssim,
        **features,
        "affine_registered_tissue_mae": affine_mae,
        "affine_registered_ssim": affine_ssim,
        "affine_registered_tissue_pixels": affine_tissue_overlap,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--review-register", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.image_root.resolve()
    if not root.is_dir():
        raise SystemExit("Extracted image root is missing")
    manifest = pd.read_csv(args.manifest, dtype=str).fillna("")
    reviews = pd.read_csv(args.review_register, dtype=str).fillna("")
    required_manifest = {
        "pair_id",
        "hamming_distance",
        "left_file_name",
        "right_file_name",
        "left_patient_id",
        "right_patient_id",
    }
    required_review = {"pair_id", "hamming_distance", "visual_disposition", "confidence"}
    if not required_manifest.issubset(manifest.columns):
        raise SystemExit("Manifest schema validation failed")
    if not required_review.issubset(reviews.columns):
        raise SystemExit("Review-register schema validation failed")
    if manifest["pair_id"].duplicated().any() or reviews["pair_id"].duplicated().any():
        raise SystemExit("Duplicate pair IDs found in input registers")

    manifest = manifest.set_index("pair_id")
    reviews = reviews.set_index("pair_id")
    missing = TARGET_PAIRS - set(manifest.index) | (TARGET_PAIRS - set(reviews.index))
    if missing:
        raise SystemExit("One or more target pair IDs are missing")
    index = safe_index(root)
    results = []
    errors = []
    for pair_id in sorted(TARGET_PAIRS):
        row = manifest.loc[pair_id].to_dict()
        review = reviews.loc[pair_id].to_dict()
        if int(row["hamming_distance"]) != int(review["hamming_distance"]):
            raise SystemExit("Manifest/review dHash disagreement")
        if not 1 <= int(row["hamming_distance"]) <= 6:
            raise SystemExit("Target is outside the nonzero dHash range")
        if row["left_patient_id"] == row["right_patient_id"]:
            raise SystemExit("A selected target is not cross-patient")
        try:
            results.append(analyse(row, review, root, index))
            print(f"{pair_id}: completed")
        except Exception as exc:
            errors.append({"pair_id": pair_id, "error_type": type(exc).__name__})
            print(f"{pair_id}: ERROR ({type(exc).__name__})", file=sys.stderr)

    args.output.mkdir(parents=True, exist_ok=True)
    if results:
        pd.DataFrame(results).to_csv(
            args.output / "anonymised-computational-register.csv", index=False
        )
    summary = {
        "audit": "NV-DUP-AUDIT-03",
        "generated_utc": datetime.now(UTC).isoformat(),
        "method": "OpenCV + NumPy + SciPy dependency environment + scikit-image + Pillow + Pandas",
        "selected_candidates": len(TARGET_PAIRS),
        "successfully_processed": len(results),
        "processing_errors": len(errors),
        "byte_identical_pairs": sum(bool(x["byte_identical"]) for x in results),
        "decoded_rgb_pixel_identical_pairs": sum(
            bool(x["decoded_rgb_pixel_identical"]) for x in results
        ),
        "plausible_affine_registrations": sum(bool(x["affine_plausible"]) for x in results),
        "visual_disposition_counts": dict(Counter(str(x["visual_disposition"]) for x in results)),
        "errors": errors,
        "privacy": "No filenames, patient identifiers, source images, or raw metadata exported.",
        "limitations": [
            "SIFT/ORB correspondences and RANSAC affine fits are screening evidence, "
            "not proof of duplication.",
            "Affine plausibility thresholds are conservative engineering filters, "
            "not validated clinical thresholds.",
            "SSIM and MAE depend on normalisation, image content, and registration.",
            "No patient identity merging or fold assignment changes are performed.",
            "Human provenance review remains necessary for suspected cross-patient duplicates.",
        ],
        "interpretation": "Research screening evidence only; no automatic duplicate confirmation.",
    }
    (args.output / "investigation-summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "processed": len(results),
                "errors": len(errors),
                "byte_identical": summary["byte_identical_pairs"],
                "pixel_identical": summary["decoded_rgb_pixel_identical_pairs"],
                "plausible_affine": summary["plausible_affine_registrations"],
            },
            indent=2,
        )
    )
    return 0 if len(results) == len(TARGET_PAIRS) and not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
