# ADR-016: Dataset Version Pinning and Patient-Group Audit

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owners:** NeuroVision project

## Context

Public OCT datasets may have multiple releases with materially different file counts, partitions and patient overlap. Published research has demonstrated that image-level splitting and reuse of some pre-existing OCT partitions can inflate test performance. A dataset name alone is therefore insufficient to reproduce or interpret an experiment.

## Decision

1. Pin each dataset by canonical source, DOI, version, archive name and SHA-256.
2. Preserve the original archive unchanged.
3. Parse patient and eye identifiers from source metadata where available.
4. Create train/validation/calibration/test partitions at patient level whenever patient identifiers are available and reliable.
5. Run explicit group-overlap assertions and duplicate/near-duplicate audits.
6. Record limitations when grouping metadata is unavailable; never describe such partitions as patient-independent.
7. Keep external test datasets untouched until the model and evaluation protocol are frozen.

## Alternatives considered

- **Use dataset folders as supplied without audit:** rejected because releases can contain leakage and version ambiguity.
- **Random image-level split:** rejected for datasets with multiple scans per patient.
- **Patient-level split only when patient IDs are present:** accepted with an explicit limitation and supplementary similarity checks when IDs are absent.

## Consequences

- Dataset acquisition includes an audit step before modelling.
- Split manifests become versioned experiment inputs.
- Some datasets may be excluded from patient-level evaluation if their metadata is inadequate.
- Published benchmark results may not be directly comparable where split policies differ.

## Evidence informing this decision

- Tampu, Eklund & Haj-Hosseini (2022), *Inflation of test accuracy due to data leakage in deep learning-based classification of OCT images*, Scientific Data 9, 580. https://doi.org/10.1038/s41597-022-01618-6
- Kermany et al. (2018), Cell 172(5), 1122–1131. https://doi.org/10.1016/j.cell.2018.02.010
