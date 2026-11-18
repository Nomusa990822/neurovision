"""Create blinded contact sheets for manual near-duplicate review."""

from __future__ import annotations

import argparse
import csv
import json
import os
import stat
from collections import defaultdict
from importlib import import_module
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
REGISTER_FIELDS = ("pair_id", "hamming_distance", "disposition", "notes")
MANIFEST_FIELDS = (
    "pair_id",
    "left_file_name",
    "right_file_name",
    "left_patient_id",
    "right_patient_id",
    "left_disease",
    "right_disease",
    "hamming_distance",
    "cross_patient",
)


def _image_index(images_dir: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(images_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            index[path.stem.casefold()].append(path)
    return index


def _write_private(path: Path, content: str | bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags, stat.S_IRUSR | stat.S_IWUSR)
    mode = "wb" if isinstance(content, bytes) else "w"
    kwargs: dict[str, Any] = {} if mode == "wb" else {"encoding": "utf-8", "newline": "\n"}
    with os.fdopen(descriptor, mode, **kwargs) as handle:
        handle.write(content)
    path.chmod(0o600)


def _resolve_image(file_name: str, index: dict[str, list[Path]]) -> Path:
    stem = Path(file_name.replace("\\", "/")).stem.casefold()
    matches = index.get(stem, [])
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one extracted image for candidate stem {stem!r}; "
            f"found {len(matches)}"
        )
    return matches[0]


def _make_contact_sheet(
    pairs: list[dict[str, str]],
    image_index: dict[str, list[Path]],
    page_number: int,
    pairs_per_sheet: int,
) -> bytes:
    image_module = import_module("PIL.Image")
    draw_module = import_module("PIL.ImageDraw")
    font_module = import_module("PIL.ImageFont")

    page_width = 1500
    page_height = 120 + pairs_per_sheet * 285
    page = image_module.new("RGB", (page_width, page_height), "white")
    draw = draw_module.Draw(page)
    font = font_module.load_default()
    draw.text(
        (35, 25),
        f"NEUROVISION | BLINDED DUPLICATE REVIEW | PAGE {page_number:03d}",
        fill="black",
        font=font,
    )

    for slot, pair in enumerate(pairs):
        row_top = 75 + slot * 285
        pair_id = pair["pair_id"]
        draw.text(
            (35, row_top),
            f"{pair_id}    dHash Hamming distance: {pair['hamming_distance']}",
            fill="black",
            font=font,
        )
        for side, key, label in (
            (0, "left_file_name", "Image A"),
            (1, "right_file_name", "Image B"),
        ):
            x = 35 + side * 730
            draw.text((x, row_top + 25), label, fill="black", font=font)
            path = _resolve_image(pair[key], image_index)
            with image_module.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((700, 220), image_module.Resampling.LANCZOS)
                page.paste(image, (x, row_top + 48))
    output = BytesIO()
    page.save(output, format="PNG", optimize=True)
    return output.getvalue()


def create_duplicate_review_pack(
    pairs_csv: Path,
    images_dir: Path,
    output_dir: Path,
    hamming_distance: int = 0,
    pairs_per_sheet: int = 2,
) -> dict[str, Any]:
    """Create blinded sheets plus private pair manifest and review register."""
    if not 0 <= hamming_distance <= 64:
        raise ValueError("hamming_distance must be between 0 and 64")
    if not 1 <= pairs_per_sheet <= 4:
        raise ValueError("pairs_per_sheet must be between 1 and 4")
    if not pairs_csv.is_file():
        raise FileNotFoundError(f"Candidate CSV does not exist: {pairs_csv}")
    if not images_dir.is_dir():
        raise NotADirectoryError(f"Image directory does not exist: {images_dir}")
    if output_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing review directory: {output_dir}")

    # pair_id is generated here; it is not a source candidate-CSV column.
    required = set(MANIFEST_FIELDS) - {"pair_id"}
    with pairs_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("Candidate CSV is missing required columns")
        selected = [
            {field: (row.get(field) or "").strip() for field in MANIFEST_FIELDS}
            for row in reader
            if int(row["hamming_distance"]) == hamming_distance
        ]

    selected.sort(
        key=lambda row: (
            row["left_file_name"],
            row["right_file_name"],
            row["left_patient_id"],
            row["right_patient_id"],
        )
    )
    for index, pair in enumerate(selected, start=1):
        pair["pair_id"] = f"PAIR-{index:04d}"

    image_index = _image_index(images_dir)
    for pair in selected:
        _resolve_image(pair["left_file_name"], image_index)
        _resolve_image(pair["right_file_name"], image_index)

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(mode=0o700)
    output_dir.chmod(0o700)

    try:
        manifest_buffer = StringIO()
        manifest_writer = csv.DictWriter(
            manifest_buffer, fieldnames=MANIFEST_FIELDS, lineterminator="\n"
        )
        manifest_writer.writeheader()
        manifest_writer.writerows(selected)
        _write_private(output_dir / "private-pair-manifest.csv", manifest_buffer.getvalue())

        register_buffer = StringIO()
        register_writer = csv.DictWriter(
            register_buffer, fieldnames=REGISTER_FIELDS, lineterminator="\n"
        )
        register_writer.writeheader()
        register_writer.writerows(
            {
                "pair_id": pair["pair_id"],
                "hamming_distance": pair["hamming_distance"],
                "disposition": "",
                "notes": "",
            }
            for pair in selected
        )
        _write_private(output_dir / "review-register.csv", register_buffer.getvalue())

        page_count = 0
        for offset in range(0, len(selected), pairs_per_sheet):
            page_count += 1
            batch = selected[offset : offset + pairs_per_sheet]
            page_bytes = _make_contact_sheet(batch, image_index, page_count, pairs_per_sheet)
            _write_private(output_dir / f"contact-sheet-{page_count:03d}.png", page_bytes)

        summary = {
            "audit_type": "blinded_near_duplicate_visual_review_pack",
            "candidate_hamming_distance": hamming_distance,
            "candidate_pair_count": len(selected),
            "pairs_per_sheet": pairs_per_sheet,
            "contact_sheet_count": page_count,
            "review_register": "review-register.csv",
            "private_pair_manifest": "private-pair-manifest.csv",
            "contact_sheet_prefix": "contact-sheet-",
        }
        _write_private(
            output_dir / "review-pack-summary.json",
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
        )
    except Exception:
        for child in output_dir.iterdir():
            child.unlink(missing_ok=True)
        output_dir.rmdir()
        raise

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create blinded contact sheets for near-duplicate review."
    )
    parser.add_argument("--pairs-csv", type=Path, required=True)
    parser.add_argument("--images-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--hamming-distance", type=int, default=0)
    parser.add_argument("--pairs-per-sheet", type=int, default=2)
    args = parser.parse_args()
    print(
        json.dumps(
            create_duplicate_review_pack(
                args.pairs_csv,
                args.images_dir,
                args.output_dir,
                args.hamming_distance,
                args.pairs_per_sheet,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
