"""Deterministic patient-grouped fold allocation utilities.

The allocator uses a seeded greedy multistart heuristic. It is not an optimiser
with a guarantee of global optimality; always audit its returned assignment.
"""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PatientGroup:
    """Image-level labels for every record belonging to one patient."""

    patient_id: str
    image_labels: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.patient_id.strip():
            raise ValueError("patient_id must not be empty")
        if not self.image_labels:
            raise ValueError("each patient group must contain at least one image label")
        if any(not label.strip() for label in self.image_labels):
            raise ValueError("image labels must not be empty")


def _score_counts(
    patient_counts: Sequence[int],
    image_counts: Sequence[int],
    class_patient_counts: Mapping[str, Sequence[int]],
    class_image_counts: Mapping[str, Sequence[int]],
    n_splits: int,
) -> float:
    """Score current fold counters in constant time with respect to group count."""
    def deviation(values: Sequence[int]) -> float:
        total = sum(values)
        if total == 0:
            return 0.0
        target = total / n_splits
        return sum(((value - target) / max(target, 1.0)) ** 2 for value in values)

    score = deviation(patient_counts) + deviation(image_counts)
    for label in class_patient_counts:
        values = class_patient_counts[label]
        score += 2.0 * deviation(values)
        score += deviation(class_image_counts[label])
        if sum(values) >= n_splits:
            score += 4.0 * sum(value == 0 for value in values)
    return score


def allocate_patient_grouped_folds(
    groups: Sequence[PatientGroup],
    *,
    n_splits: int,
    seed: int,
    n_candidates: int = 256,
) -> dict[str, int]:
    """Return patient_id -> zero-based fold using deterministic multistart greedy search.

    All records for a patient are indivisible. The input sequence order is not
    mutated. The same input, seed and parameters produce the same assignment.
    """
    if n_splits < 2:
        raise ValueError("n_splits must be at least 2")
    if n_candidates < 1:
        raise ValueError("n_candidates must be positive")
    if len(groups) < n_splits:
        raise ValueError("number of patient groups must be at least n_splits")

    patient_ids = [group.patient_id for group in groups]
    if len(patient_ids) != len(set(patient_ids)):
        raise ValueError("patient_id values must be unique")

    labels = sorted({label for group in groups for label in group.image_labels})
    label_patient_frequency = Counter(
        label for group in groups for label in set(group.image_labels)
    )
    rng = random.Random(seed)
    best_assignment: dict[str, int] | None = None
    best_score = float("inf")

    for _ in range(n_candidates):
        tie_breakers = {group.patient_id: rng.random() for group in groups}
        ordered = sorted(
            groups,
            key=lambda group: (
                min(label_patient_frequency[label] for label in set(group.image_labels)),
                -len(set(group.image_labels)),
                -len(group.image_labels),
                tie_breakers[group.patient_id],
            ),
        )
        assignment: dict[str, int] = {}
        patient_counts = [0] * n_splits
        image_counts = [0] * n_splits
        class_patient_counts = {label: [0] * n_splits for label in labels}
        class_image_counts = {label: [0] * n_splits for label in labels}

        for group in ordered:
            group_labels = set(group.image_labels)
            empty_folds = [
                fold for fold, count in enumerate(patient_counts) if count == 0
            ]
            candidate_folds = empty_folds or list(range(n_splits))
            candidates: list[tuple[float, int]] = []

            for fold in candidate_folds:
                patient_counts[fold] += 1
                image_counts[fold] += len(group.image_labels)
                for label in group_labels:
                    class_patient_counts[label][fold] += 1
                for label in group.image_labels:
                    class_image_counts[label][fold] += 1

                score = _score_counts(
                    patient_counts,
                    image_counts,
                    class_patient_counts,
                    class_image_counts,
                    n_splits,
                )
                candidates.append((score, fold))

                patient_counts[fold] -= 1
                image_counts[fold] -= len(group.image_labels)
                for label in group_labels:
                    class_patient_counts[label][fold] -= 1
                for label in group.image_labels:
                    class_image_counts[label][fold] -= 1

            _, selected_fold = min(candidates)
            assignment[group.patient_id] = selected_fold
            patient_counts[selected_fold] += 1
            image_counts[selected_fold] += len(group.image_labels)
            for label in group_labels:
                class_patient_counts[label][selected_fold] += 1
            for label in group.image_labels:
                class_image_counts[label][selected_fold] += 1

        score = _score_counts(
            patient_counts,
            image_counts,
            class_patient_counts,
            class_image_counts,
            n_splits,
        )
        if score < best_score:
            best_score = score
            best_assignment = dict(assignment)

    if best_assignment is None:
        raise RuntimeError("fold allocation did not produce an assignment")
    return best_assignment


def validate_patient_grouped_assignment(
    groups: Sequence[PatientGroup],
    assignment: Mapping[str, int],
    *,
    n_splits: int,
) -> list[str]:
    """Return integrity errors for a patient-to-fold assignment."""
    errors: list[str] = []
    expected = {group.patient_id for group in groups}
    actual = set(assignment)
    if expected != actual:
        errors.append("assignment patient identifiers do not match input groups")
    if any(not isinstance(fold, int) or isinstance(fold, bool) for fold in assignment.values()):
        errors.append("fold identifiers must be integers")
    if any(fold < 0 or fold >= n_splits for fold in assignment.values()):
        errors.append("fold identifiers are outside the configured range")
    if any(not any(fold == index for fold in assignment.values()) for index in range(n_splits)):
        errors.append("one or more folds are empty")
    return errors
