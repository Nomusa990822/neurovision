# WP14 — Exact, near-duplicate screening and visual review

**Status:** Initial screening and blinded visual reviews completed; computational investigation of ten nonzero-dHash candidates completed; provenance adjudication and duplicate-aware split remain pending  
**Dataset:** OCTDL Mendeley Data Version 4  
**Last updated:** 2026-11-27

## Objective

Identify exact byte-level duplicates and visually similar OCT images before model development. Screening and review-pack generation are read-only: they must not modify, rename, move or delete source images or labels.

## Screening methods

1. **Exact duplicates:** SHA-256 over original image bytes, streamed in 1 MiB chunks.
2. **Near-duplicate candidates:** 64-bit difference hash (dHash). Each image is converted to grayscale, resized to 9×8 using Lanczos resampling, and adjacent horizontal pixel intensities are compared.
3. **Patient relationship:** Candidate groups and pairs include source patient IDs and disease labels in private outputs. Cross-patient candidates are explicitly flagged.
4. **Metadata integrity:** CSV image stems must resolve to exactly one extracted image. Duplicate CSV stems, missing matches and ambiguous matches fail closed. The source labels CSV SHA-256 is recorded.

The initial threshold was 6 (inclusive). It is a screening threshold, not a validated identity threshold.

## OCTDL V4 screening results

The data-specific audit covered 2,064 image records. The labels CSV SHA-256 was:

`b7db437cfe67741623f26e8bb2cef0f4d6828d6d86150f752f412da1c4ee8b3a`

| Finding | Count |
|---|---:|
| Exact duplicate groups | 1 |
| Exact cross-patient groups | 0 |
| Near-duplicate candidate pairs (distance ≤6) | 354 |
| Cross-patient candidate pairs | 309 |
| Distinct images represented in candidate pairs | 474 |
| Patients represented in candidate pairs | 270 |
| Connected components | 188 |
| Cross-patient connected components | 162 |

The single exact group contains two differently named AMD records from the same patient. Both CSV rows have the same disease, subcategory (late), condition (MNV), eye/sex/year source values (all 0), and image dimensions (905×279). Their SHA-256 hashes are identical. They are retained pending source-provenance clarification; no record was removed.

The candidate-pair distance distribution was: 87 at distance 0, 23 at 1, 15 at 2, 21 at 3, 26 at 4, 51 at 5, and 131 at 6. Perceptual hash equality does not establish pixel identity. One connected component contains 62 images from 49 patients and 112 edges; component connectivity is transitive and does not imply all members are duplicates.

The original aggregate report and private candidate CSV remain in the local private audit workspace. They must not be committed or shared publicly.

## Blinded visual review and computational follow-up

### Zero-dHash visual and computational review

All 87 cross-patient dHash-distance-zero candidates received blinded visual review. All were visually flagged as potential duplicates with High confidence. Subsequent computational verification found:

- 87/87 processed with no errors.
- 0 byte-identical pairs.
- 54 decoded RGB pixel-identical pairs.
- 47 cross-patient exact-pixel edges, involving 49 unique patients.
- 22 connected components in that exact-pixel cross-patient graph; 19 components span multiple original folds.
- 39 of the 47 exact-pixel cross-patient edges cross the original folds.

The broader dHash-zero candidate set also contained visually similar pairs that were not pixel-identical. Exact-pixel equality is stronger evidence of image-file content equality after decoding, but does not establish acquisition provenance or correct patient assignment.

### Nonzero-dHash visual review

The nonzero review pack covered 231 cross-patient candidates at dHash distances 1–6. The 36 same-patient nonzero candidates were outside this review pack and remain unresolved.

| Visual disposition | Count |
|---|---:|
| `potential_duplicate` | 10 |
| `similar_distinct` | 221 |
| `inconclusive` | 0 |
| **Total** | **231** |

The ten visually flagged candidates were investigated computationally in private workflow [#46005797560](https://github.com/Nomusa990822/neurovision-datasets/actions/runs/46005797560). The workflow checked out public research code at immutable commit `d6df613fdf3d82629b458b60cefec00f4a84864f`, verified the OCTDL archive SHA-256, recorded input hashes and processed all ten candidates without errors.

| Computational result | Count |
|---|---:|
| Candidates processed | 10 |
| Processing errors | 0 |
| Byte-identical pairs | 0 |
| Decoded RGB pixel-identical pairs | 0 |
| Affine estimates passing the engineering plausibility filter | 10 |

The corrected affine registration direction was merged in PR #18 before this run. The prior run's affine-registered measurements are invalid and must not be used. The corrected run's metrics are screening evidence only; no automatic duplicate confirmation was made.

An anonymised triage register is maintained in the private dataset repository at `research_audits/nonzero_review/nonzero_candidate_adjudication-triage.csv`. It prioritises two candidates with near-identical image geometry, four with strong transformed correspondence, one intermediate candidate, and three with weaker/ambiguous correspondence. All ten remain pending human provenance adjudication. These priority groupings are not validated thresholds or identity conclusions.

## Duplicate-component reconciliation and split status

The zero-dHash exact-pixel graph is a verified screening output, but the edge-level patient-link table and component membership export are not currently committed to the private dataset repository alongside the nonzero review records. Therefore the two evidence sets have **not yet been deterministically joined**. Aggregate counts are not sufficient to infer overlap or transitive component membership.

The original patient-to-fold mapping remains quarantined. It must not be used for training or evaluation. No patient IDs have been merged, no labels or source records have been changed, and no new split is approved.

The next gate is to make the zero-dHash edge-level and component-membership exports available inside the private audit environment, join them with the ten nonzero candidates, adjudicate provenance, then construct and validate a duplicate-aware patient-level split candidate.

## Blinded visual-review pack implementation

The `neurovision.datasets.duplicate_review` module creates a private review pack from the candidate CSV and extracted image directory.

- Select one exact Hamming-distance band at a time (start with distance 0).
- Contact sheets show anonymous pair IDs, the two images, and Hamming distance only.
- The separate review register contains pair ID, distance, blank disposition and notes fields.
- A private pair manifest maps pair IDs to filenames, patient IDs, disease labels and cross-patient status. It must remain owner-only and must not be shared.
- Output directory permissions are 0700; files are 0600.
- Existing output directories are never overwritten.
- No images, labels, patient assignments or source files are modified.

Example for the first 87 distance-zero pairs:

    cd "$HOME/neurovision"
    git pull --ff-only origin main
    umask 077
    mkdir -p "$HOME/neurovision-audit/reports"
    chmod 700 "$HOME/neurovision-audit/reports"

    PYTHONPATH=src python -m neurovision.datasets.duplicate_review \
      --pairs-csv "$HOME/neurovision-audit/private/octdl-v4-near-duplicate-candidates.csv" \
      --images-dir "$HOME/neurovision-audit/extracted/OCTDL_V4" \
      --output-dir "$HOME/neurovision-audit/private/dhash-zero-review" \
      --hamming-distance 0 \
      --pairs-per-sheet 2

The review pack contains anonymous contact-sheet PNGs, `review-register.csv`, `private-pair-manifest.csv`, and an aggregate summary. Never paste or upload the private manifest or original candidate CSV.

## Review dispositions

For each pair, record one of:

- `potential_duplicate`: visual evidence suggests the same scan or a transformed copy; provenance confirmation still required.
- `similar_distinct`: visibly different scans.
- `inconclusive`: image quality or visual evidence is insufficient.

Record concise rationale in the notes field. A visual judgement is not proof of patient identity. Cross-patient potential duplicates require a separate provenance investigation. Do not merge patients or alter labels based solely on image similarity.

## Limitations and acceptance criteria

- An exact SHA-256 match establishes byte-identical files, not whether scans were assigned to the correct patient.
- dHash can miss transformed duplicates and flag visually similar scans.
- Connected components are transitive candidate networks, not duplicate clusters.
- The audit does not establish patient identity or clinical equivalence.
- The first pass compares records within OCTDL V4 only.
- No candidate is automatically excluded. Any exclusion requires documented rationale and a new, versioned dataset manifest and split assignment.
- Patient-grouped folds cannot repair incorrect patient metadata or cross-patient duplicate copies.

**Training remains unauthorised** until candidate review, dataset terms/use approval and all other pre-training gates are complete.
