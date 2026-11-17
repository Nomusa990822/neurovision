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
- Non-root Docker runtime baseline, build-context exclusions, Docker operating guide and ADR-021.
- GitHub Actions Docker build and container smoke-test job.
### Changed
- README, roadmap and development setup now reflect the verified Python engineering baseline and WP08 Docker implementation.
### Verified
- GitHub-hosted Python 3.12.16 quality run: locked environment synchronisation, 15 passing unit tests, 98% statement coverage, Ruff lint/format, mypy and wheel/source distribution build.
- WP08 PR #5 GitHub Actions run #44049716757: Python quality job and Docker non-root smoke-test job both passed. The container imported the package, loaded production settings, ran as UID 10001 and wrote to its application data directory.
### Pending
- PR #5 review/merge and formal Phase 2 acceptance, including formal Phase 1 closure.
- Dataset acquisition and empirical integrity/patient audit (Phase 3).

## [0.1.0] - Unreleased
Planned engineering-foundation milestone. Do not tag until its acceptance criteria are verified.
