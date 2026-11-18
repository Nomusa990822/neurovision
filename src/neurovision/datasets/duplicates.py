"""Exact and perceptual near-duplicate screening for image datasets."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import stat
from collections import defaultdict
from datetime import UTC, datetime
from importlib import import_module
from io import StringIO
from pathlib import Path
from typing import Any

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


def sha256_file(path: Path) -> str:
    """Return a streaming SHA-256 digest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def difference_hash(path: Path) -> int:
    """Compute a 64-bit dHash. Pillow is required at execution time."""
    try:
        image_module = import_module("PIL.Image")
    except ImportError as error:
        raise RuntimeError(
            "Near-duplicate screening requires Pillow; install it with "
            "'python -m pip install Pillow'."
        ) from error
    with image_module.open(path) as source:
        image = source.convert("L").resize((9, 8), image_module.Resampling.LANCZOS)
        pixels = list(image.getdata())
    value = 0
    for row in range(8):
        offset = row * 9
        for column in range(8):
            value = (value << 1) | int(pixels[offset + column] > pixels[offset + column + 1])
    return value


def hamming_distance(left: int, right: int) -> int:
    """Count differing bits between two perceptual hashes."""
    return (left ^ right).bit_count()


def _load_records(labels_csv: Path, images_dir: Path) -> tuple[list[dict[str, Any]], str]:
    if not labels_csv.is_file():
        raise FileNotFoundError(f"Labels CSV does not exist: {labels_csv}")
    if not images_dir.is_dir():
        raise NotADirectoryError(f"Image directory does not exist: {images_dir}")
    image_index: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(images_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            image_index[path.stem.casefold()].append(path)

    records: list[dict[str, Any]] = []
    seen_stems: set[str] = set()
    with labels_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"file_name", "patient_id", "disease"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("Labels CSV must contain file_name, patient_id and disease")
        for row_number, row in enumerate(reader, start=2):
            file_name = (row.get("file_name") or "").strip()
            patient_id = (row.get("patient_id") or "").strip()
            disease = (row.get("disease") or "").strip()
            if not file_name or not patient_id or not disease:
                raise ValueError(f"Missing required metadata at CSV row {row_number}")
            stem = Path(file_name.replace("\\", "/")).stem.casefold()
            if stem in seen_stems:
                raise ValueError(f"Duplicate image stem in labels CSV at row {row_number}")
            seen_stems.add(stem)
            matches = image_index.get(stem, [])
            if len(matches) != 1:
                raise ValueError(
                    f"Expected exactly one image for CSV row {row_number}; found {len(matches)}"
                )
            path = matches[0]
            records.append(
                {
                    "file_name": file_name,
                    "patient_id": patient_id,
                    "disease": disease,
                    "sha256": sha256_file(path),
                    "perceptual_hash": difference_hash(path),
                }
            )
    if not records:
        raise ValueError("No image records were found in the labels CSV")
    return records, sha256_file(labels_csv)


def _write_private_new(path: Path, content: str) -> None:
    """Create an owner-only file and refuse to overwrite prior evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, stat.S_IRUSR | stat.S_IWUSR)
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    path.chmod(0o600)


def run_duplicate_screen(
    labels_csv: Path,
    images_dir: Path,
    report_json: Path,
    pairs_csv: Path,
    max_hamming_distance: int = 6,
) -> dict[str, Any]:
    """Screen exact and perceptual duplicates without modifying source data."""
    if not 0 <= max_hamming_distance <= 64:
        raise ValueError("max_hamming_distance must be between 0 and 64")
    if report_json.resolve() == pairs_csv.resolve():
        raise ValueError("Report and pair output paths must be different")
    if report_json.exists() or pairs_csv.exists():
        raise FileExistsError("Refusing to overwrite an existing duplicate-screening output")

    records, labels_sha256 = _load_records(labels_csv, images_dir)
    exact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        exact[record["sha256"]].append(record)
    exact_groups = [
        {
            "sha256": digest,
            "record_count": len(group),
            "patient_count": len({item["patient_id"] for item in group}),
            "cross_patient": len({item["patient_id"] for item in group}) > 1,
            "records": [
                {key: item[key] for key in ("file_name", "patient_id", "disease")}
                for item in group
            ],
        }
        for digest, group in sorted(exact.items())
        if len(group) > 1
    ]

    pairs: list[dict[str, Any]] = []
    for index, left in enumerate(records):
        for right in records[index + 1 :]:
            if left["sha256"] == right["sha256"]:
                continue
            distance = hamming_distance(left["perceptual_hash"], right["perceptual_hash"])
            if distance <= max_hamming_distance:
                pairs.append(
                    {
                        "left_file_name": left["file_name"],
                        "right_file_name": right["file_name"],
                        "left_patient_id": left["patient_id"],
                        "right_patient_id": right["patient_id"],
                        "left_disease": left["disease"],
                        "right_disease": right["disease"],
                        "hamming_distance": distance,
                        "cross_patient": left["patient_id"] != right["patient_id"],
                    }
                )

    report: dict[str, Any] = {
        "audit_type": "exact_and_perceptual_duplicate_screen",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "image_record_count": len(records),
        "labels_csv_sha256": labels_sha256,
        "unique_image_sha256_count": len({item["sha256"] for item in records}),
        "exact_duplicate_group_count": len(exact_groups),
        "exact_duplicate_record_count": sum(item["record_count"] for item in exact_groups),
        "exact_cross_patient_group_count": sum(int(item["cross_patient"]) for item in exact_groups),
        "perceptual_method": "64-bit difference hash; grayscale 9x8 Lanczos resize",
        "max_hamming_distance_inclusive": max_hamming_distance,
        "near_duplicate_candidate_pair_count": len(pairs),
        "near_duplicate_cross_patient_pair_count": sum(int(item["cross_patient"]) for item in pairs),
        "exact_duplicate_groups": exact_groups,
        "limitations": [
            "Perceptual matches are candidates for manual review, not proof of duplicate identity.",
            "Difference hash can miss transformed duplicates and flag visually similar distinct scans.",
            "The audit does not establish patient identity or clinical equivalence.",
            "No image, label or source file is modified or deleted.",
            "Reports contain private filenames and patient identifiers; keep them outside Git.",
        ],
    }
    fields = [
        "left_file_name", "right_file_name", "left_patient_id", "right_patient_id",
        "left_disease", "right_disease", "hamming_distance", "cross_patient",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(pairs)

    if report_json.exists() or pairs_csv.exists():
        raise FileExistsError("Refusing to overwrite an existing duplicate-screening output")
    _write_private_new(pairs_csv, buffer.getvalue())
    try:
        _write_private_new(report_json, json.dumps(report, indent=2, sort_keys=True) + "\n")
    except Exception:
        pairs_csv.unlink(missing_ok=True)
        raise
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Screen OCT images for exact and near duplicates.")
    parser.add_argument("--labels-csv", type=Path, required=True)
    parser.add_argument("--images-dir", type=Path, required=True)
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--pairs-csv", type=Path, required=True)
    parser.add_argument("--max-hamming-distance", type=int, default=6)
    args = parser.parse_args()
    report = run_duplicate_screen(
        args.labels_csv, args.images_dir, args.report_json, args.pairs_csv,
        args.max_hamming_distance,
    )
    summary = {
        key: report[key]
        for key in (
            "audit_type", "image_record_count", "labels_csv_sha256",
            "exact_duplicate_group_count", "exact_cross_patient_group_count",
            "near_duplicate_candidate_pair_count",
            "near_duplicate_cross_patient_pair_count",
        )
    }
    summary["reports_written"] = True
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
