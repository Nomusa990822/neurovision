"""Dataset acquisition manifest creation and structural validation."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "dataset_id",
    "dataset_title",
    "publisher_or_depositor",
    "source_url",
    "persistent_identifier",
    "version",
    "acquired_at_utc",
    "acquisition_method",
    "terms_url",
    "licence_name",
    "licence_scope_notes",
    "archive_filename",
    "archive_bytes",
    "archive_sha256",
    "extracted_file_count",
    "metadata_files",
    "patient_id_available",
    "eye_id_available",
    "scanner_site_metadata",
    "acquisition_status",
    "intended_use",
    "limitations",
)
VALID_STATUSES = {"candidate", "source_verified", "acquired", "audited", "approved"}


def create_manifest_template(dataset_id: str, dataset_title: str) -> dict[str, Any]:
    """Return an explicit, unapproved manifest template for one dataset release."""
    if not dataset_id.strip() or not dataset_title.strip():
        raise ValueError("dataset_id and dataset_title must not be empty")
    return {
        "dataset_id": dataset_id,
        "dataset_title": dataset_title,
        "publisher_or_depositor": "",
        "source_url": "",
        "persistent_identifier": "",
        "version": "",
        "publication_or_release_date": None,
        "acquired_at_utc": None,
        "acquisition_method": "",
        "terms_url": "",
        "licence_name": "not stated",
        "licence_scope_notes": "",
        "archive_filename": None,
        "archive_bytes": None,
        "archive_sha256": None,
        "extracted_file_count": None,
        "expected_file_count": None,
        "metadata_files": [],
        "patient_id_available": None,
        "eye_id_available": None,
        "scanner_site_metadata": "not reported",
        "acquisition_status": "candidate",
        "intended_use": "",
        "limitations": [],
    }


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Return validation errors; this checks structure, not legal permission."""
    errors = [f"missing required field: {key}" for key in REQUIRED_FIELDS if key not in manifest]
    if manifest.get("acquisition_status") not in VALID_STATUSES:
        errors.append("acquisition_status must be one of: " + ", ".join(sorted(VALID_STATUSES)))
    for key in ("archive_bytes", "extracted_file_count"):
        value = manifest.get(key)
        if value is not None and (not isinstance(value, int) or value < 0):
            errors.append(f"{key} must be a non-negative integer or null")
    digest = manifest.get("archive_sha256")
    if digest is not None and (not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest)):
        errors.append("archive_sha256 must be a lowercase 64-character SHA-256 hex digest or null")
    for key in ("metadata_files", "limitations"):
        if not isinstance(manifest.get(key), list):
            errors.append(f"{key} must be a list")
    if manifest.get("acquisition_status") in {"acquired", "audited", "approved"}:
        for key in ("acquired_at_utc", "archive_filename", "archive_bytes", "archive_sha256"):
            if manifest.get(key) in (None, ""):
                errors.append(f"{key} is required once acquisition_status is acquired or later")
    if manifest.get("acquisition_status") in {"audited", "approved"} and manifest.get("extracted_file_count") is None:
        errors.append("extracted_file_count is required for audited or approved status")
    if manifest.get("acquisition_status") == "approved" and not str(manifest.get("intended_use", "")).strip():
        errors.append("intended_use is required for approved status")
    return errors


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Validate and write a UTF-8 JSON manifest without overwriting an existing file."""
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("Invalid manifest: " + "; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\\n") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\\n")
