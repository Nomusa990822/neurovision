"""Generate and independently audit nested patient-grouped inner folds."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from neurovision.datasets.splits import PatientGroup, allocate_patient_grouped_folds

OUTER_FOLDS = (1, 2, 3, 4, 5)
INNER_FOLDS = 4
ALLOCATOR_VERSION = "greedy-multistart-v1"


def _read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path.name}")
        rows = list(reader)
        return rows, list(reader.fieldnames)


def _required_column(headers: list[str], candidates: tuple[str, ...], description: str) -> str:
    for candidate in candidates:
        if candidate in headers:
            return candidate
    raise ValueError(f"Missing {description} column; expected one of {candidates}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _groups_from_rows(
    rows: list[dict[str, str]], patient_column: str, label_column: str
) -> list[PatientGroup]:
    labels_by_patient: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        patient_id = row[patient_column].strip()
        label = row[label_column].strip()
        if not patient_id or not label:
            raise ValueError("Source CSV contains an empty patient identifier or disease label")
        labels_by_patient[patient_id].append(label)
    return [
        PatientGroup(patient_id, tuple(labels))
        for patient_id, labels in sorted(labels_by_patient.items())
    ]


def _outer_assignment(
    rows: list[dict[str, str]], headers: list[str]
) -> dict[str, int]:
    patient_column = _required_column(headers, ("patient_id",), "patient identifier")
    fold_column = _required_column(headers, ("outer_fold", "fold"), "outer fold")
    assignment: dict[str, int] = {}
    for row in rows:
        patient_id = row[patient_column].strip()
        try:
            fold = int(row[fold_column])
        except (TypeError, ValueError) as error:
            raise ValueError("Outer mapping contains a non-integer fold value") from error
        if not patient_id:
            raise ValueError("Outer mapping contains an empty patient identifier")
        if patient_id in assignment:
            raise ValueError("Outer mapping contains duplicate patient identifiers")
        if fold not in OUTER_FOLDS:
            raise ValueError("Outer mapping fold values must be 1 through 5")
        assignment[patient_id] = fold
    return assignment


def _aggregate(
    groups: list[PatientGroup], patient_to_fold: dict[str, int], n_folds: int
) -> dict[str, Any]:
    patient_counts = Counter(patient_to_fold.values())
    image_counts: Counter[int] = Counter()
    class_patients: dict[str, Counter[int]] = defaultdict(Counter)
    class_images: dict[str, Counter[int]] = defaultdict(Counter)
    group_by_id = {group.patient_id: group for group in groups}
    for patient_id, fold in patient_to_fold.items():
        group = group_by_id[patient_id]
        image_counts[fold] += len(group.image_labels)
        for label in set(group.image_labels):
            class_patients[label][fold] += 1
        for label in group.image_labels:
            class_images[label][fold] += 1
    return {
        "patient_counts": {str(fold): patient_counts[fold] for fold in range(1, n_folds + 1)},
        "image_counts": {str(fold): image_counts[fold] for fold in range(1, n_folds + 1)},
        "class_patient_counts": {
            label: {str(fold): class_patients[label][fold] for fold in range(1, n_folds + 1)}
            for label in sorted(class_patients)
        },
        "class_image_counts": {
            label: {str(fold): class_images[label][fold] for fold in range(1, n_folds + 1)}
            for label in sorted(class_images)
        },
    }


def generate_inner_folds(
    labels_csv: Path,
    outer_mapping_csv: Path,
    output_csv: Path,
    report_json: Path,
    *,
    seed: int = 20261118,
    n_candidates: int = 1000,
) -> dict[str, Any]:
    """Generate five four-fold inner assignments and write private outputs."""
    if output_csv.exists() or report_json.exists():
        raise FileExistsError("Refusing to overwrite an existing mapping or report")
    label_rows, label_headers = _read_csv(labels_csv)
    outer_rows, outer_headers = _read_csv(outer_mapping_csv)
    patient_column = _required_column(label_headers, ("patient_id",), "patient identifier")
    label_column = _required_column(label_headers, ("disease",), "disease label")
    groups = _groups_from_rows(label_rows, patient_column, label_column)
    outer = _outer_assignment(outer_rows, outer_headers)
    group_ids = {group.patient_id for group in groups}
    if group_ids != set(outer):
        raise ValueError("Outer mapping patient identifiers do not match source CSV")
    group_by_id = {group.patient_id: group for group in groups}

    output_rows: list[dict[str, int | str]] = []
    summaries: dict[str, Any] = {}
    for outer_fold in OUTER_FOLDS:
        training_ids = sorted(patient_id for patient_id, fold in outer.items() if fold != outer_fold)
        training_groups = [group_by_id[patient_id] for patient_id in training_ids]
        assignment = allocate_patient_grouped_folds(
            training_groups,
            n_splits=INNER_FOLDS,
            seed=seed + outer_fold * 1009,
            n_candidates=n_candidates,
        )
        if set(assignment) != set(training_ids):
            raise RuntimeError("Allocator returned an incomplete inner assignment")
        for patient_id, inner_fold in assignment.items():
            output_rows.append(
                {
                    "outer_fold": outer_fold,
                    "patient_id": patient_id,
                    "inner_fold": inner_fold + 1,
                }
            )
        summaries[str(outer_fold)] = {
            "outer_test_patient_count": len(groups) - len(training_ids),
            "outer_training_patient_count": len(training_ids),
            "inner_folds": _aggregate(
                training_groups, {key: value + 1 for key, value in assignment.items()}, INNER_FOLDS
            ),
            "rare_class_coverage_note": "See class_patient_counts; absent classes are not imputed.",
        }

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    report_json.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["outer_fold", "patient_id", "inner_fold"])
        writer.writeheader()
        writer.writerows(sorted(output_rows, key=lambda row: (row["outer_fold"], row["patient_id"])))
    os.chmod(output_csv, 0o600)

    # Re-read the written file and source metadata for an independent integrity pass.
    verified_rows, verified_headers = _read_csv(output_csv)
    reread_outer_rows, reread_outer_headers = _read_csv(outer_mapping_csv)
    reread_label_rows, reread_label_headers = _read_csv(labels_csv)
    verified_outer = _outer_assignment(reread_outer_rows, reread_outer_headers)
    verified_patient_column = _required_column(
        reread_label_headers, ("patient_id",), "patient identifier"
    )
    verified_label_column = _required_column(
        reread_label_headers, ("disease",), "disease label"
    )
    verified_labels = _groups_from_rows(
        reread_label_rows, verified_patient_column, verified_label_column
    )
    verified_group_ids = {group.patient_id for group in verified_labels}
    inner_patient_column = _required_column(verified_headers, ("patient_id",), "patient identifier")
    outer_fold_column = _required_column(verified_headers, ("outer_fold",), "outer fold")
    inner_fold_column = _required_column(verified_headers, ("inner_fold",), "inner fold")
    seen: set[tuple[int, str]] = set()
    verified_by_outer: dict[int, dict[str, int]] = defaultdict(dict)
    for row in verified_rows:
        outer_fold = int(row[outer_fold_column])
        inner_fold = int(row[inner_fold_column])
        patient_id = row[inner_patient_column].strip()
        key = (outer_fold, patient_id)
        if key in seen:
            raise RuntimeError("Independent audit found a duplicate outer/patient assignment")
        seen.add(key)
        if outer_fold not in OUTER_FOLDS or inner_fold not in range(1, INNER_FOLDS + 1):
            raise RuntimeError("Independent audit found an out-of-range fold identifier")
        verified_by_outer[outer_fold][patient_id] = inner_fold

    for outer_fold in OUTER_FOLDS:
        expected = {patient_id for patient_id, fold in verified_outer.items() if fold != outer_fold}
        actual = set(verified_by_outer[outer_fold])
        if actual != expected:
            raise RuntimeError("Independent audit found missing, extra or held-out patients")
        if set(verified_by_outer[outer_fold].values()) != set(range(1, INNER_FOLDS + 1)):
            raise RuntimeError("Independent audit found an empty inner fold")

    if len(verified_rows) != len(verified_group_ids) * (len(OUTER_FOLDS) - 1):
        raise RuntimeError("Independent audit found an unexpected assignment row count")

    report: dict[str, Any] = {
        "audit_type": "nested_inner_fold_assignment_integrity",
        "dataset_image_record_count": len(reread_label_rows),
        "unique_patient_count": len(verified_group_ids),
        "outer_fold_count": len(OUTER_FOLDS),
        "inner_fold_count": INNER_FOLDS,
        "assignment_row_count": len(verified_rows),
        "all_outer_training_patients_assigned_once_per_iteration": True,
        "no_outer_test_patient_in_corresponding_inner_mapping": True,
        "all_inner_folds_nonempty": True,
        "independent_re_read_verification_passed": True,
        "allocator": {
            "version": ALLOCATOR_VERSION,
            "method": "seeded greedy multistart heuristic",
            "base_seed": seed,
            "candidates_per_outer_iteration": n_candidates,
            "seed_rule": "base_seed + outer_fold * 1009",
        },
        "inner_assignment_sha256": _sha256(output_csv),
        "outer_iterations": summaries,
        "limitations": [
            "The allocator is a heuristic and does not guarantee a globally optimal balance.",
            "Rare-class support may be small; fold-specific metrics can be undefined or unstable.",
            "This integrity report does not authorise model training.",
        ],
    }
    with report_json.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.chmod(report_json, 0o600)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels-csv", type=Path, required=True)
    parser.add_argument("--outer-mapping", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20261118)
    parser.add_argument("--candidates", type=int, default=1000)
    args = parser.parse_args()
    report = generate_inner_folds(
        args.labels_csv,
        args.outer_mapping,
        args.output_csv,
        args.report_json,
        seed=args.seed,
        n_candidates=args.candidates,
    )
    print(
        json.dumps(
            {
                "audit_type": report["audit_type"],
                "assignment_row_count": report["assignment_row_count"],
                "unique_patient_count": report["unique_patient_count"],
                "inner_assignment_sha256": report["inner_assignment_sha256"],
                "independent_re_read_verification_passed": report[
                    "independent_re_read_verification_passed"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
