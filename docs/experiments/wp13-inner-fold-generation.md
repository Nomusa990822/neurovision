# WP13 — Inner-Fold Generation Implementation

**Status:** Generator and synthetic tests implemented on a feature branch; execution against the private OCTDL files and independent data-specific verification remain pending.  
**Privacy:** Both generated files contain patient identifiers or sensitive split metadata and must remain outside the public repository.

## Purpose

For each of the five outer iterations, generate four patient-grouped inner folds using only the four outer-training folds. The implementation reuses the deterministic greedy multistart allocator in `neurovision.datasets.splits`.

The generator reads the source labels CSV and the private outer assignment, verifies that their patient sets match, and groups all image-level disease labels belonging to each patient. It does not collapse image-level labels, including the multi-label AMD/DME patient.

## Termux execution

Run from the public code repository after pulling the merged implementation:

```bash
cd "$HOME/neurovision"
git pull --ff-only origin main

mkdir -p "$HOME/neurovision-audit/private" "$HOME/neurovision-audit/reports"
chmod 700 "$HOME/neurovision-audit/private"

PYTHONPATH=src python -m neurovision.datasets.nested_splits \
  --labels-csv "$HOME/neurovision-datasets/OCTDL_V4/metadata/OCTDL_labels.csv" \
  --outer-mapping "$HOME/neurovision-audit/private/five-fold-patient-assignments.csv" \
  --output-csv "$HOME/neurovision-audit/private/nested-inner-fold-assignments.csv" \
  --report-json "$HOME/neurovision-audit/reports/nested-inner-fold-integrity.json" \
  --seed 20261118 \
  --candidates 1000
```

The command deliberately refuses to overwrite either output. If a previous run created an output, inspect and preserve it; do not delete or overwrite it blindly. Choose a new versioned output filename for a rerun and record the reason.

## Expected structure

- Five outer iterations.
- Four inner folds per outer iteration.
- 820 unique patients, assuming the source and outer mapping remain unchanged.
- 3,280 mapping rows: each patient appears in the four iterations where it belongs to the outer-training pool and is absent from its own outer evaluation iteration.
- CSV columns: `outer_fold,patient_id,inner_fold`.
- Inner fold values are one-based (1–4); outer fold values are one-based (1–5).

The aggregate JSON report contains patient/image counts, per-class patient/image counts, allocator parameters, the inner-mapping SHA-256 and integrity outcomes. It does not contain patient identifiers or image filenames. Both generated files are written with owner-only permissions (`0600`).

## Verification and interpretation

The generator re-reads the source labels CSV, private outer mapping and newly written inner mapping before accepting the result. It checks that:
- the source patient set matches the outer mapping;
- every outer-training patient appears exactly once in that iteration;
- no patient from the corresponding outer evaluation fold appears in its inner mapping;
- all four inner folds are non-empty;
- there are no duplicate outer/patient rows or invalid fold values;
- the total assignment count is consistent with four training appearances per patient.

Review the per-class support in the aggregate report, especially RAO. A class may have very small support in an inner validation fold. Do not replace undefined metrics with zero or infer stable performance from sparse support.

This tooling verifies partition integrity, not model performance, dataset licence permission, duplicate-image absence or clinical validity. **It does not authorise model training.** Preserve the report and mapping privately and share only the aggregate report contents and SHA-256 with the project review process.
