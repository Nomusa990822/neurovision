# ADR-002: Patient-Aware Dataset Partitioning

- **Status:** Accepted
- **Date:** 2026-11-17

## Context
Multiple OCT scans may originate from the same patient, eye or visit. Image-level random splitting can place correlated samples in both training and test sets, inflating performance.

## Decision
Use patient-grouped partitions whenever valid patient identifiers are available and permitted. Audit eye/visit relationships and duplicates. Persist split manifests and automate group-overlap checks.

## Alternatives
- Random image-level splitting.
- Grouping by filename alone without validating its semantics.

## Consequences
The evaluation better reflects generalisation to unseen patients but may reduce usable sample size and require class-balance-aware group allocation. If patient identifiers are absent, document the limitation and do not claim patient-level separation.