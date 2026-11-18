"""Tests for patient-grouped fold allocation."""

from neurovision.datasets.splits import (
    PatientGroup,
    allocate_patient_grouped_folds,
    validate_patient_grouped_assignment,
)


def _groups() -> list[PatientGroup]:
    groups: list[PatientGroup] = []
    labels = ["AMD", "DME", "ERM", "NO", "RAO", "RVO", "VID"]
    for index in range(56):
        label = labels[index % len(labels)]
        records = (label, label) if index % 3 == 0 else (label,)
        groups.append(PatientGroup(f"patient-{index:03d}", records))
    return groups


def test_all_patients_are_assigned_once_and_folds_are_nonempty() -> None:
    groups = _groups()
    assignment = allocate_patient_grouped_folds(
        groups, n_splits=4, seed=20261118, n_candidates=32
    )

    assert set(assignment) == {group.patient_id for group in groups}
    assert validate_patient_grouped_assignment(groups, assignment, n_splits=4) == []
    assert {assignment[group.patient_id] for group in groups} == {0, 1, 2, 3}


def test_all_records_for_a_patient_share_one_fold() -> None:
    groups = _groups()
    assignment = allocate_patient_grouped_folds(
        groups, n_splits=4, seed=17, n_candidates=16
    )

    for group in groups:
        assert assignment[group.patient_id] in range(4)


def test_allocation_is_deterministic() -> None:
    groups = _groups()
    first = allocate_patient_grouped_folds(
        groups, n_splits=4, seed=123, n_candidates=20
    )
    second = allocate_patient_grouped_folds(
        groups, n_splits=4, seed=123, n_candidates=20
    )

    assert first == second


def test_multi_label_patient_remains_one_group() -> None:
    groups = _groups()
    groups.append(PatientGroup("patient-multilabel", ("AMD", "DME")))
    assignment = allocate_patient_grouped_folds(
        groups, n_splits=4, seed=42, n_candidates=20
    )

    assert "patient-multilabel" in assignment
    assert validate_patient_grouped_assignment(
        groups, assignment, n_splits=4
    ) == []


def test_invalid_duplicate_patient_ids_are_rejected() -> None:
    groups = [
        PatientGroup("duplicate", ("AMD",)),
        PatientGroup("duplicate", ("DME",)),
    ]

    try:
        allocate_patient_grouped_folds(
            groups, n_splits=2, seed=1, n_candidates=2
        )
    except ValueError as error:
        assert "unique" in str(error)
    else:
        raise AssertionError("duplicate patient identifiers should be rejected")


def test_invalid_split_count_is_rejected() -> None:
    groups = _groups()
    try:
        allocate_patient_grouped_folds(
            groups, n_splits=1, seed=1, n_candidates=2
        )
    except ValueError as error:
        assert "at least 2" in str(error)
    else:
        raise AssertionError("n_splits=1 should be rejected")
