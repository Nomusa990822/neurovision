# Changelog

All notable project changes are recorded here. Releases do not imply clinical validation.

## [Unreleased]

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
- Execute WP14 exact/near-duplicate screening, inspect candidate pairs and record dispositions.
- Complete exact file-level licence review and purpose-specific dataset approval.
- Complete any remaining dataset-level integrity and split approvals; model training remains blocked until all gates are approved.

## [0.1.0] - Unreleased

Planned engineering-foundation milestone. Do not tag until its release criteria are verified.
