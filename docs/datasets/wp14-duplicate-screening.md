# WP14 — Exact and near-duplicate screening

**Status:** Implementation proposed; data-specific execution and manual review pending  
**Dataset:** OCTDL Mendeley Data Version 4  
**Date:** 2026-11-18

## Objective

Identify exact byte-level duplicates and visually similar OCT images before model development. The screening is read-only and must not modify, rename, move or delete source images or labels.

## Methods

1. **Exact duplicates:** SHA-256 over original image bytes, streamed in 1 MiB chunks.
2. **Near-duplicate candidates:** 64-bit difference hash (dHash). Each image is converted to grayscale, resized to 9×8 using Lanczos resampling, and adjacent horizontal pixel intensities are compared.
3. **Patient relationship:** Candidate groups and pairs include source patient IDs and disease labels in private outputs. Cross-patient candidates are explicitly flagged.
4. **Metadata integrity:** CSV image stems must resolve to exactly one extracted image. Duplicate CSV stems, missing matches and ambiguous matches fail closed. The source labels CSV SHA-256 is recorded.

Default dHash threshold is 6 (inclusive). It is a screening threshold, not a validated identity threshold. Every candidate requires manual review.

## Execution

Run from the public code repository after this implementation is merged:

    cd "$HOME/neurovision"
    git pull --ff-only origin main
    python -c "import PIL; print('Pillow', PIL.__version__)"
    umask 077
    mkdir -p "$HOME/neurovision-audit/reports"
    mkdir -p "$HOME/neurovision-audit/private"
    chmod 700 "$HOME/neurovision-audit/private"

    PYTHONPATH=src python -m neurovision.datasets.duplicates \
      --labels-csv "$HOME/neurovision-datasets/OCTDL_V4/metadata/OCTDL_labels.csv" \
      --images-dir "$HOME/neurovision-audit/extracted/OCTDL_V4" \
      --report-json "$HOME/neurovision-audit/reports/octdl-v4-duplicate-screen.json" \
      --pairs-csv "$HOME/neurovision-audit/private/octdl-v4-near-duplicate-candidates.csv" \
      --max-hamming-distance 6

The module requires Pillow in the active Python environment. The Termux audit environment previously used Pillow for image decoding; verify its availability before execution. Outputs are owner-only and existing paths are never overwritten. Do not rerun with the same output names after success.

## Output handling

- JSON report: aggregate counts, labels CSV SHA-256, exact duplicate groups and limitations.
- CSV: near-duplicate candidate pairs with filenames, patient IDs, disease labels, Hamming distance and cross-patient flag.
- Both outputs are private because they contain dataset filenames and patient identifiers. Keep them under the private audit workspace; do not commit them or paste identifiers into public issues/PRs.
- The command prints only a concise aggregate summary. Inspect detailed reports locally and share only aggregate JSON after checking for identifiers.

## Interpretation and limitations

- An exact SHA-256 match establishes byte-identical files, not whether scans were assigned to the correct patient.
- A dHash match is a candidate only. Similar anatomy, common scan layouts, resizing, cropping, overlays and compression can affect matches.
- dHash can miss transformations and flag distinct scans with similar global structure. It is not a substitute for manual review or source provenance.
- This first pass compares records within OCTDL V4 only.
- No candidate is automatically excluded. Any exclusion requires documented rationale and a new, versioned dataset manifest and split assignment.
- Patient-grouped folds cannot repair incorrect patient metadata or cross-patient duplicate copies.

## Acceptance criteria

- All 2,064 CSV image records resolve uniquely and are decoded by Pillow.
- Every image has a SHA-256 and dHash.
- Exact duplicate groups and near-duplicate pairs are counted and preserved privately.
- Cross-patient candidate counts are reported.
- CSV SHA-256 is recorded.
- Candidate pairs are manually reviewed and dispositions documented before training approval.

**Training remains unauthorised** until the findings are reviewed, dataset terms/use are approved, and all other pre-training gates are cleared.
