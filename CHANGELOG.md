# Changelog

All notable project changes are recorded here. Releases do not imply clinical validation.

## [Unreleased]
### Added
- NeuroVision project charter, research objectives, requirements, architecture and governance records.
- Dataset source desk review and patient-level leakage safeguards.
- Apache License 2.0 for original NeuroVision project materials.
- Phase 2 engineering specification and ADR-020.
- Initial Python src-layout package scaffold, environment-backed settings, path helpers, Python RNG seeding and focused unit tests.
- Committed Python 3.12 uv lockfile and read-only GitHub Actions quality workflow.
### Changed
- README, roadmap and development setup now reflect the verified Python engineering baseline and outstanding Docker work.
### Verified
- GitHub-hosted Python 3.12.16 quality run: locked environment synchronisation, 15 passing unit tests, 98% statement coverage, Ruff lint/format, mypy and wheel/source distribution build.
### Pending
- Non-root Docker baseline, container smoke test and final Phase 2 acceptance.
- Dataset acquisition and empirical integrity/patient audit (Phase 3).

## [0.1.0] - Unreleased
Planned engineering-foundation milestone. Do not tag until its acceptance criteria are verified.
