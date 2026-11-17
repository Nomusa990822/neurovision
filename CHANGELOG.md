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
- GitHub Actions Docker build and container smoke-test job.
- Formal Phase 1/2 acceptance record.
- Phase 3 dataset acquisition and audit protocol.
- Local dataset manifest, SHA-256, archive inspection/extraction, inventory CLI and synthetic tests (WP10; pending merge).

### Changed
- Dataset register now pins OCTDL Mendeley Version 4 and records the Kermany V3 terms ambiguity and OCTID source limitations.
- README and roadmap updated to show Phase 1/2 closure and Phase 3 in progress.

### Verified
- Python 3.12 quality run: 15 passing unit tests, 98% statement coverage, Ruff, mypy and package build.
- WP08 PR #5 run #44049962338: Python quality and Docker smoke-test jobs both passed; container verified as UID 10001 with writable application data directory.
- PR #5 merged to main as a975754c747a1c8996d842829a0223fb98b353df.
- Post-merge main workflows #44050377840, #44050384243 and #44050390407 all completed successfully.

### Pending
- WP10 CI and review.
- Select and acquire a version-pinned OCT dataset under verified terms.
- Empirical image integrity, label, metadata, duplicate and patient-group audit (Phase 3).
- Purpose-specific dataset approval and patient-aware split policy.

## [0.1.0] - Unreleased
Planned engineering-foundation milestone. Do not tag until its acceptance criteria are verified.
