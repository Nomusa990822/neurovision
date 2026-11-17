# ADR-020: Phase 2 Python Runtime and Engineering Toolchain

- **Status:** Accepted as the Phase 2 implementation baseline
- **Date:** 2026-11-17
- **Decision owners:** NeuroVision project maintainers

## Context

The repository is currently documentation-first. Phase 2 needs a stable, reproducible Python foundation without prematurely installing the full planned machine-learning and service stack. Python and ML package compatibility, deterministic dependency resolution, automated quality checks and maintainable package boundaries are important to later scientific reproducibility.

## Decision

1. Use Python 3.12 as the initial runtime and CI baseline, declared as `>=3.12,<3.13`. Reassess only through a documented compatibility review.
2. Use `pyproject.toml` plus uv and a committed `uv.lock` for package metadata and dependency resolution. CI must use locked synchronisation.
3. Use a src-layout modular monolith under `src/neurovision/`.
4. Use Ruff for linting/formatting, mypy for static typing, pytest/pytest-cov for tests, and a package build check.
5. Keep base dependencies minimal. Add PyTorch/torchvision as a compatible pair in the modelling phase; add OpenCV, FastAPI, PostgreSQL, MLflow and DVC only when their modules are implemented and tested.
6. Use typed configuration, environment overrides, an example environment file and strict secret/data exclusions.
7. Implement pull-request CI with explicit Python setup and read-only permissions by default.
8. Add a minimal non-root Docker baseline after the package scaffold exists.

## Rationale

Python 3.12 is a conservative compatibility baseline for the scientific Python stack. The current official PyTorch installation guidance requires Python 3.11 or later for its latest stable release, while exact wheel compatibility remains platform- and release-dependent. uv provides a lockfile-based workflow and a locked mode that detects stale dependency metadata. Ruff consolidates lint and formatting tasks; mypy and pytest provide separate static and runtime verification.

## Consequences

- Developers use the same declared Python minor version and committed lock.
- Dependency changes become reviewable and reproducible.
- CI failures are visible before merge.
- The base environment remains smaller and cheaper to install.
- GPU-specific PyTorch installation remains hardware-aware rather than embedded in a universal lock assumption.
- New modules are introduced only when their phase begins; the target architecture does not justify empty placeholder packages.
- CI and local success must be reported separately from later scientific validation.

## Alternatives considered

- **Python 3.13/3.14 immediately:** deferred until the selected scientific stack is tested as a whole.
- **pip with unconstrained requirements:** rejected as the primary workflow because it does not provide the same integrated lock/sync process.
- **Poetry:** viable, but uv is selected for its focused project/lock workflow and lightweight command interface.
- **Install every planned dependency at project start:** rejected to reduce installation cost, compatibility risk and unused dependencies.
- **Microservices:** rejected as unnecessary for a single research platform at this stage.

## References

- [PyTorch — Get Started Locally](https://pytorch.org/get-started/locally/)
- [uv — Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [GitHub — Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
