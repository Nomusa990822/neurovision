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
- OCTDL V4 acquisition evidence ledger distinguishing owner-reported file acquisition from independently verified integrity and provenance.

### Changed
- Dataset register pins OCTDL Mendeley Version 4 and records the Kermany V3 terms ambiguity and OCTID source limitations.
- README and roadmap track Phase 3 acquisition and audit work without claiming unverified archive checks.
- Acquisition/audit protocol records the owner-reported OCTDL V4 download and the outstanding verification gates.

### Verified
- Python 3.12 quality run: 15 passing unit tests, 98% statement coverage, Ruff, mypy and package build.
- WP08 PR #5: Python quality and Docker smoke-test jobs passed; non-root container verified as UID 10001.
- WP09 PR #6: Python quality and Docker smoke-test jobs passed in [run #44051112486](https://github.com/Nomusa990822/neurovision/actions/runs/44051112486); merged as ce625592a5189795bca49e8b36fee6b5f2e0b9a8.
- WP10 PR #7: 29 tests passed; Ruff lint/format, mypy, package build and Docker non-root smoke test passed in [run #44053030829](https://github.com/Nomusa990822/neurovision/actions/runs/44053030829); merged as e26d8955215f6a75ed1990368afa3f517d4df64b.
- The owner-reported download and storage location are documented; the underlying archive bytes, hashes and contents have not been independently verified.

### Pending
- Independently access and checksum the OCTDL V4 archive and CSV; validate archive integrity.
- Empirical image integrity, label, metadata, duplicate and patient-group audit.
- Purpose-specific dataset approval and patient-aware split policy.

## [0.1.0] - Unreleased

Planned engineering-foundation milestone. Do not tag until its release criteria are verified.
