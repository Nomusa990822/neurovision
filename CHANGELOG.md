# Changelog

All notable project changes are recorded here. Releases do not imply clinical validation.

## [Unreleased]

### Dataset audit update — 2026-11-27
- Executed private OCTDL workflow run [#46004611218](https://github.com/Nomusa990822/neurovision-datasets/actions/runs/46004611218): all ten visually flagged nonzero-dHash candidates were processed with zero errors; none were byte-identical or decoded-RGB-pixel-identical. The run's affine-plausibility flags and SIFT/ORB/phase metrics are screening evidence only.
- Post-run code review identified an affine registration direction error: the estimated transform maps left-image coordinates to right-image coordinates, but the warp was applied without inversion when generating left-reference output. Consequently, affine-registered SSIM/MAE values from run #46004611218 are invalid and must not be interpreted. Corrected in PR #18 (merged as `d6df613fdf3d82629b458b60cefec00f4a84864f`); the synthetic translation regression test verifies exact realignment. The private audit must be rerun against this corrected commit before affine metrics are interpreted.
- Completed blinded visual review of all 231 cross-patient nonzero-dHash candidates (dHash 1–6): 10 visually flagged as potential duplicates and 221 classified as similar but distinct; all received High-confidence visual dispositions. These are screening judgments, not duplicate confirmations.
- Completed the full 231-row nonzero visual-review register: 10 `potential_duplicate`, 221 `similar_distinct`, all High confidence. Reviewer identity and timestamps remain blank because they were not present in the source register and have not been reconstructed.
- Added a strict review-register completeness/enum check and an all-20-images preflight that resolves and decodes every selected image before any pairwise computation, preventing partial result sets from being mistaken for complete audits. A synthetic test verifies preflight failure occurs before analysis.
- Investigated failed NV-DUP-AUDIT-03 run [#46001809229](https://github.com/Nomusa990822/neurovision-datasets/actions/runs/46001809229). The hidden per-pair `KeyError` was traced with a synthetic reproduction to loss of `pair_id` when converting an indexed manifest row to a dictionary; the analysis function still required that key. The manifest row now explicitly restores `pair_id` before analysis.
- Reconciled the ten selected visual-review records in the private dataset repository as `potential_duplicate` / `High`, based on the completed manual review; no reviewer identity or review timestamp was invented. Added strict selected-cohort review preflight and private traceback diagnostics. Synthetic integration tests process ten synthetic image pairs, verify byte/pixel equality handling and anonymised exports, and reject incomplete review records.
- Added a dedicated CI job using the same pinned scientific dependency versions as the private audit. The synthetic integration tests and standard Python quality checks passed in [run #46003305018](https://github.com/Nomusa990822/neurovision/actions/runs/46003305018); Docker smoke verification was still running at the time of this changelog update. The private OCTDL workflow has not yet been rerun, so no real-candidate computational findings are available.
- Executed NV-DUP-AUDIT-03 workflow run [#45999286898](https://github.com/Nomusa990822/neurovision-datasets/actions/runs/45999286898). Private repository/LFS checkout, pinned code checkout, dependency setup, required-input checks, archive SHA-256 verification and safe extraction passed.
- The initial computational run did not process any of its 10 selected candidates: the private manifest stores extensionless image stems while the audit resolver expected archive filenames. The run correctly failed with 10 path-resolution errors; no computational duplicate findings are claimed.
- Added a safe, ambiguity-rejecting image path resolver that supports exact filenames and unique extensionless stems, with synthetic unit tests. Public PR #15 was merged as `bee991513ca89bf05b48dd14b57f2aa4652a6bc8` after Python quality and Docker non-root smoke tests passed in [run #46000071890](https://github.com/Nomusa990822/neurovision/actions/runs/46000071890). Private workflow PR #2 was merged as `d1c99411d262dec971ae631eb655dfc09e5805f1` to pin both checkout and provenance to the corrected code commit.
- Executed corrected workflow run [#46000663421](https://github.com/Nomusa990822/neurovision-datasets/actions/runs/46000663421). LFS checkout, pinned code checkout, dependencies, input validation, archive SHA-256 verification and safe extraction passed. The audit stopped before candidate processing because the direct script invocation did not expose the package `src/` directory (`ModuleNotFoundError: No module named 'neurovision'`); 0/10 candidates were processed. Provenance was recorded and uploaded, but no computational findings were produced.
- Corrected the private workflow to set `PYTHONPATH` to the pinned checkout's `neurovision/src` directory and added an explicit package-import smoke check. Private PR #3 was merged as `b28112211965ca7d1f6b8145d766ced52420e2d3`. The modified YAML step was parsed and its environment/import command verified locally; a fresh private audit run is still required to validate execution end to end.
- The original dataset, patient identities and quarantined patient-to-fold mapping remain unchanged. Model training and evaluation remain blocked pending duplicate-aware grouping, provenance review and dataset/split approval.
- Earlier OCTDL V4 duplicate-screening evidence and quarantine rationale are recorded in [WP14 duplicate-screening report](docs/experiments/wp14-duplicate-screening.md). Patient-linked manifests, filenames, hashes and mappings remain private.

### Added
- NeuroVision project charter, research objectives, requirements, architecture and governance records.
- Dataset source desk review and patient-level leakage safeguards.
- Apache License 2.0 for original NeuroVision project materials.
- Phase 2 engineering specification and ADR-020.
- Python package scaffold, settings, path helpers, RNG helper and unit tests.
- Committed Python 3.12 uv lockfile and GitHub Actions quality workflow.
- Non-root Docker runtime, build-context exclusions, Docker guide and ADR-021.
- Formal Phase 1/2 acceptance record and Phase 3 dataset acquisition/audit protocol.
- Local dataset manifest, SHA-256, archive inspection/extraction, inventory CLI and synthetic tests (WP10).
- OCTDL V4 acquisition record updated with verified archive SHA-256/LFS integrity, ZIP CRC, image inventory/decoding, dimensions, CSV reconciliation and patient-group audit evidence.
- WP13 nested inner-fold generator, independent re-read integrity checks, owner-only output handling and synthetic tests.
- WP14 exact SHA-256 duplicate grouping and 64-bit perceptual difference-hash candidate screening, with private report outputs and synthetic tests.
- Safe extensionless image-path resolution for private duplicate-audit manifests, with synthetic tests.

### Changed
- Dataset register pins OCTDL Mendeley Version 4 and records the Kermany V3 terms ambiguity and OCTID source limitations.
- Dataset register, README, roadmap and acquisition/audit protocol distinguish completed local audit evidence from outstanding licence, duplicate-screening and dataset-approval gates.
- Roadmap records data-specific WP13 nested-fold generation and integrity verification as complete; WP14 data execution remains pending.

### Verified
- Python 3.12 quality run: 15 passing unit tests, 98% statement coverage, Ruff, mypy and package build.
- WP08 PR #5: Python quality and Docker smoke-test jobs passed; non-root container verified as UID 10001.
- WP09 PR #6: Python quality and Docker smoke-test jobs passed in [run #44051112486](https://github.com/Nomusa990822/neurovision/actions/runs/44051112486); merged as ce625592a5189795bca49e8b36fee6b5f2e0b9a8.
- WP10 PR #7: 29 tests passed; Ruff lint/format, mypy, package build and Docker non-root smoke test passed in [run #44053030829](https://github.com/Nomusa990822/neurovision/actions/runs/44053030829); merged as e26d8955215f6a75ed1990368afa3f517d4df64b.
- OCTDL V4 archive size (398,564,236 bytes), SHA-256 and local Git LFS integrity were verified by the project owner; ZIP CRC, 2,064-image extraction/decoding, dimensions and CSV-to-image reconciliation passed in the local audit.
- WP13 inner-fold mapping was generated and independently re-read locally: 3,280 assignments, 820 unique patients, five outer iterations, four nonempty inner folds per iteration, and no corresponding outer-test patient in inner mappings. Mapping SHA-256: b01b94536ad2823d213962d0a124b40562567b04822e297a4aa0c3b348cc4f34.

### Pending
- Complete computational investigation of the 10 visually flagged nonzero-dHash candidates and review its findings against image provenance.
- Complete exact file-level licence review and purpose-specific dataset approval.
- Complete remaining dataset-level integrity and split approvals; model training remains blocked until all gates are approved.

## [0.1.0] - Unreleased

Planned engineering-foundation milestone. Do not tag until its release criteria are verified.
