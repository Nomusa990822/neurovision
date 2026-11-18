"""Tests for nested patient-grouped inner-fold generation."""

from __future__ import annotations

import csv
import json
import stat
from pathlib import Path

import pytest

from neurovision.datasets.nested_splits import generate_inner_folds


def _write_inputs(directory: Path) -> tuple[Path, Path]:
    labels_path = directory / "labels.csv"
    outer_path = directory / "outer.csv"
    labels = ["AMD", "DME", "ERM", "NO", "RAO", "RVO", "VID"]
    with labels_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["patient_id", "disease"])
        writer.writeheader()
        for index in range(35):
            writer.writerow(
                {"patient_id": f"patient-{index:03d}", "disease": labels[index % len(labels)]}
            )
            if index % 5 == 0:
                writer.writerow(
                    {"patient_id": f"patient-{index:03d}", "disease": labels[(index + 1) % 7]}
                )
    with outer_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["patient_id", "fold"])
        writer.writeheader()
        for index in range(35):
            writer.writerow({"patient_id": f"patient-{index:03d}", "fold": index % 5 + 1})
    return labels_path, outer_path


def test_nested_inner_assignments_are_complete_and_private(tmp_path: Path) -> None:
    labels_path, outer_path = _write_inputs(tmp_path)
    output_path = tmp_path / "private" / "inner-folds.csv"
    report_path = tmp_path / "private" / "inner-report.json"

    report = generate_inner_folds(
        labels_path,
        outer_path,
        output_path,
        report_path,
        seed=20261118,
        n_candidates=8,
    )

    assert report["assignment_row_count"] == 140
    assert report["unique_patient_count"] == 35
    assert report["independent_re_read_verification_passed"] is True
    assert report["all_outer_training_patients_assigned_once_per_iteration"] is True
    assert report["no_outer_test_patient_in_corresponding_inner_mapping"] is True
    assert report["all_inner_folds_nonempty"] is True
    assert len(report["inner_assignment_sha256"]) == 64
    assert stat.S_IMODE(output_path.stat().st_mode) == 0o600
    assert stat.S_IMODE(report_path.stat().st_mode) == 0o600

    mapping = list(csv.DictReader(output_path.open(encoding="utf-8", newline="")))
    assert len(mapping) == 140
    for outer_fold in range(1, 6):
        iteration = [row for row in mapping if int(row["outer_fold"]) == outer_fold]
        assert len(iteration) == 28
        assert {int(row["inner_fold"]) for row in iteration} == {1, 2, 3, 4}
        assert all((int(row["outer_fold"]), row["patient_id"]) for row in iteration)

    public_report = report_path.read_text(encoding="utf-8")
    assert "patient-000" not in public_report


def test_generator_refuses_to_overwrite_outputs(tmp_path: Path) -> None:
    labels_path, outer_path = _write_inputs(tmp_path)
    output_path = tmp_path / "inner.csv"
    report_path = tmp_path / "report.json"
    output_path.write_text("do not overwrite", encoding="utf-8")

    with pytest.raises(FileExistsError):
        generate_inner_folds(labels_path, outer_path, output_path, report_path)


def test_generator_rejects_outer_mapping_with_missing_patient(tmp_path: Path) -> None:
    labels_path, outer_path = _write_inputs(tmp_path)
    rows = list(csv.DictReader(outer_path.open(encoding="utf-8", newline="")))
    with outer_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["patient_id", "fold"])
        writer.writeheader()
        writer.writerows(rows[:-1])

    with pytest.raises(ValueError, match="do not match"):
        generate_inner_folds(
            labels_path, outer_path, tmp_path / "inner.csv", tmp_path / "report.json"
        )
