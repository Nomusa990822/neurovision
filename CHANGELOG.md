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
### Changed
- README and roadmap updated for merged WP08 implementation and next-phase status.
### Verified
- Python 3.12 quality run: 15 passing unit tests, 98% statement coverage, Ruff, mypy and package build.
- WP08 PR #5 run #44049962338: Python quality and Docker smoke-test jobs both passed; container verified as UID 10001 with writable application data directory.
- PR #5 merged to main as a975754c747a1c8996d842829a0223fb98b353df.
### Pending
- Post-merge main integration workflow and formal Phase 1/2 acceptance record.
- Dataset acquisition and empirical integrity/patient audit (Phase 3).

## [0.1.0] - Unreleased
Planned engineering-foundation milestone. Do not tag until its acceptance criteria are verified.