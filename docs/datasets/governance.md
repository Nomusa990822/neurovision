# Dataset Governance and Data Management

## Principles
Original data are immutable. All transformations must be reproducible and traceable to a source version, manifest and configuration. Access and use must comply with the dataset licence, institutional requirements and applicable privacy law.

## Data zones
- **Raw:** original acquired archives/files; read-only; never committed to Git.
- **Interim:** audited intermediate data and temporary transformations.
- **Processed:** reproducibly generated model inputs.
- **Manifests:** file references, labels, pseudonymous grouping keys and split assignments.
- **Metadata:** provenance, licence, data dictionary and quality reports.

## Provenance
Record publisher, source URL, DOI/version, licence, acquisition date, archive hash, file count and audit status. Each derived artefact must identify its source manifest and preprocessing configuration.

## Patient and eye grouping
Use patient identifiers for group-aware partitioning where available and permitted. Keep scans from the same patient in one partition; assess eye-level and visit relationships where metadata supports it. Do not expose direct identifiers. If identifiers are absent or unreliable, document the limitation and perform defensible duplicate/similarity audits; do not claim patient-level separation.

## Partition governance
Keep training, model-selection validation, calibration and final testing roles distinct. Do not use final test data for tuning, threshold selection or calibration. External datasets must remain independent of training and model-selection data. Store split manifests and test for patient-group overlap.

## Integrity and quality
Compute SHA-256 hashes; validate decoding, dimensions and formats; identify exact duplicates; inspect near-duplicates where feasible; check label consistency and missing metadata. Retain an audit log of exclusions with reasons.

## Privacy and security
Minimise data collection and retention. Restrict access to sensitive data. Do not commit patient data, identifiers, credentials or private storage locations. Avoid logging images or identifiers. Apply encryption and access controls appropriate to the storage environment.

## Redistribution
Dataset licences are independent of the NeuroVision software licence. Do not publish raw OCT images or derived data unless redistribution rights are explicitly established. Public manifests must not reveal sensitive identifiers or enable re-identification.

## Governance approval
A dataset is approved only for a specified purpose after source, licence, provenance, integrity and privacy checks are documented. Approval for model training does not automatically grant redistribution rights.