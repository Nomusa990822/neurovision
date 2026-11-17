# Phase 2 Engineering Specification

**Work package:** WP05 — Phase 2 engineering specification  
**Status:** Proposed for review; this document is a design baseline, not implementation evidence.  
**Scope:** Define the minimal reproducible Python foundation and quality gates before dataset processing or model development.

## 1. Engineering objectives

Phase 2 will turn the documentation-first repository into a cleanly installable, testable Python project. The initial scaffold must remain lightweight and avoid premature service, database, UI or model complexity.

The implementation must provide:
- A supported and explicitly selected Python runtime.
- A package installed from the repository using a standard build backend.
- A committed dependency lockfile and deterministic environment synchronisation.
- Centralised, validated configuration with safe secret handling.
- Automated formatting, linting, type checking, tests and package-build checks.
- A minimal Docker development/runtime baseline after the package entry points exist.
- Clear developer commands and evidence-backed acceptance criteria.

No OCT dataset acquisition, image preprocessing, model training, clinical inference or performance claims are part of WP05.

## 2. Runtime and dependency management

### Python

Select **Python 3.12** as the initial project runtime and CI baseline. This is a conservative compatibility target for the scientific Python ecosystem while remaining within the currently documented PyTorch supported range. Reassess the supported range when the actual pinned PyTorch/torchvision pair is selected; do not assume all future packages support every Python release. PyTorch's installation guidance currently identifies Python 3.11 or later for its latest stable release. See the [official PyTorch installation selector](https://pytorch.org/get-started/locally/).

- Declare `requires-python = ">=3.12,<3.13"` initially.
- Add `.python-version` containing `3.12`.
- CI must use an explicit Python 3.12 version, never an implicit runner default.
- Expand the supported Python matrix only after the complete dependency set is tested.

### Package and lock management

Use **uv** with `pyproject.toml` and a committed `uv.lock`.

- `pyproject.toml` is the authoritative package metadata, dependency groups, build configuration and tool configuration.
- `uv.lock` records the resolved dependency graph and exact versions.
- Use `uv sync --locked` in CI so stale lock metadata fails rather than silently changing dependencies.
- Use `uv run` for project commands.
- Dependency changes must update the lockfile in the same change.
- Do not commit virtual environments, package caches or machine-specific paths.

uv documents lock/sync behaviour and the `--locked` guard in its [official project documentation](https://docs.astral.sh/uv/concepts/projects/sync/).

### Dependency policy

Keep the base installation minimal. Add packages only when an implemented module needs them.

Initial runtime candidates:
- `pydantic` and `pydantic-settings` for typed configuration and validation.
- `PyYAML` only if a concrete human-authored YAML configuration use case is adopted.

Initial development tools:
- `pytest` and `pytest-cov`.
- `ruff` for linting and formatting.
- `mypy` for static type checking.
- `build` for package-build verification if not supplied by the selected uv build workflow.

Do not add PyTorch, torchvision, OpenCV, FastAPI, PostgreSQL drivers, MLflow or DVC to the base environment simply because they are planned technologies. Introduce them in the phase where their interfaces and versions can be tested. PyTorch/torchvision must be selected as a compatible pair using the official installation selector for the target OS and CPU/CUDA/ROCm platform. Avoid committing a hardware-specific accelerator wheel index as the universal default.

## 3. Package architecture

Use a **src-layout modular monolith**. The initial implementation should create only modules that have real, testable responsibilities.

Target package boundaries:

| Package area | Responsibility | Introduction |
|---|---|---|
| `config/` | Typed settings, validation and configuration loading | Phase 2 |
| `utils/` | Small cross-cutting deterministic helpers; no domain logic | Phase 2, only as needed |
| `data/` | Dataset manifests, metadata contracts, integrity and split logic | Phase 3 |
| `preprocessing/` | OCT decoding, quality checks and transformations | Phase 4 |
| `models/` | Model definitions and weight interfaces | Phase 5 |
| `training/` | Training loops, optimisation and checkpointing | Phase 5 |
| `evaluation/` | Metrics, confidence intervals and evaluation protocols | Phase 5 onward |
| `explainability/` | Explanation methods and explanation evaluation | Phase 7 |
| `uncertainty/` | Predictive uncertainty and selective prediction | Phase 8 |
| `calibration/` | Probability calibration and calibration evaluation | Phase 8 |
| `tracking/` | MLflow adapters and experiment metadata | Phase 5 onward |
| `inference/` | Versioned preprocessing/model inference contract | Phase 10 |
| `api/` | FastAPI transport and request/response schemas | Phase 10 |

The target layout is not a requirement to create empty directories now. Keep domain logic independent of API, database and UI adapters. Do not introduce microservices.

## 4. Configuration and secrets

- Use a typed settings object with validation; environment variables override safe defaults.
- Keep non-secret, reviewed defaults in version-controlled configuration.
- Provide `.env.example` containing names and placeholders only.
- Ignore `.env`, credentials, tokens, private keys, local database files, raw datasets and generated artefacts.
- Fail clearly when a required setting is missing or invalid.
- Never log secrets, patient identifiers, image contents or sensitive metadata.
- Resolve paths from an explicit project/data root rather than the caller's current working directory.
- Do not store dataset paths, patient metadata or credentials in public experiment logs.

## 5. Quality and testing standard

### Tool responsibilities

- **Ruff:** enforce selected lint rules and formatting; CI runs both `ruff check` and `ruff format --check`.
- **mypy:** statically check typed package code. Start with strict checking for new core modules and explicitly document any temporary boundary exceptions.
- **pytest:** run deterministic unit and integration tests.
- **pytest-cov:** report coverage; initially use a measured baseline rather than an arbitrary high percentage target before meaningful code exists.
- **Build check:** build a wheel/sdist and verify package metadata.

### Initial test scope

Phase 2 tests should cover:
1. Package import and version metadata.
2. Configuration defaults, environment overrides and invalid-value failures.
3. Path resolution independent of the shell's current directory.
4. Deterministic seed helper behaviour, if such a helper is implemented.
5. Basic manifest/schema validation only if the manifest contract is implemented in Phase 2.

Dataset checksum, image decoding, patient grouping and leakage tests belong to Phase 3/4 and must use audited fixtures. Model tests belong to later modelling phases. Do not create placeholder tests that merely assert `True`.

### CI workflow

Create a GitHub Actions workflow triggered on pull requests and pushes to the protected default branch. It must:
1. Check out the repository.
2. Set up the explicit Python version.
3. Install a pinned uv release using the supported installation action or documented installation method.
4. Run `uv sync --locked --all-groups`.
5. Run Ruff lint and format checks.
6. Run mypy.
7. Run pytest (and publish coverage output/artifact where configured).
8. Build the package.
9. Use read-only repository permissions unless a job demonstrably requires more.

Pin third-party GitHub Actions to reviewed major versions initially; adopt full commit-SHA pinning as a supply-chain hardening follow-up. Do not expose secrets to untrusted pull-request workflows. GitHub's official Python workflow guide documents explicit interpreter setup and dependency installation: [Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

## 6. Docker development baseline

Docker is in Phase 2 scope, but implementation follows the package scaffold so the image has a real install target.

- Use a supported slim Python 3.12 base image, pinned to a deliberate version (and digest where practical).
- Use a non-root runtime user.
- Do not copy raw datasets, local secrets, virtual environments or experiment artefacts into the image.
- Add a `.dockerignore`.
- Keep build-time dependencies separate from runtime dependencies where practical.
- Do not install CUDA into the general-purpose application image. GPU training environments are a separately documented concern.
- Verify image build and a minimal package smoke test; API health checks are deferred until the API exists.

## 7. Documentation and reproducibility

The scaffold must document:
- Supported Python and uv versions.
- Environment creation and synchronisation commands.
- Lint, format, type-check, test and build commands.
- Configuration variables and secret-handling rules.
- How to add/update dependencies and regenerate the lockfile.
- CPU/GPU dependency selection policy.
- Known platform limitations.

Every experiment introduced later must record code revision, configuration, dataset version/manifest hash, split definition, random seeds, environment/dependency lock, hardware/software context and checkpoint/artifact identifiers.

## 8. Phase 2 work packages

| ID | Work package | Deliverable |
|---|---|---|
| P2-01 | Python package metadata and src scaffold | Installable package and version metadata |
| P2-02 | Runtime and dependency lock | `.python-version`, `pyproject.toml`, `uv.lock` |
| P2-03 | Configuration foundation | Validated settings and safe example environment |
| P2-04 | Quality tooling | Ruff, mypy, pytest configuration and meaningful initial tests |
| P2-05 | Continuous integration | Pull-request quality workflow |
| P2-06 | Container baseline | Minimal non-root Docker image and ignore rules |
| P2-07 | Developer documentation | Exact setup, test and maintenance instructions |

## 9. Acceptance criteria

Phase 2 may be marked complete only when all applicable evidence exists:

- [ ] A clean Python 3.12 environment can be created from the committed lockfile.
- [ ] `uv sync --locked --all-groups` succeeds without modifying the lock.
- [ ] The package installs and imports outside the repository working directory.
- [ ] Configuration tests cover defaults, overrides and invalid inputs.
- [ ] `ruff check .` passes.
- [ ] `ruff format --check .` passes.
- [ ] `mypy` passes for the configured package scope.
- [ ] `pytest` passes; test count and coverage are recorded.
- [ ] Wheel/sdist build succeeds.
- [ ] Pull-request CI runs all required checks and reports green.
- [ ] Docker image builds and runs the package smoke test.
- [ ] Secret, dataset and generated-artifact exclusions are verified.
- [ ] README, changelog, architecture and roadmap reflect implemented—not merely planned—behaviour.

A successful local command is not a substitute for CI evidence. A skipped, cancelled or absent check is not a passing check.

## 10. Out of scope and gates

- Dataset acquisition and licence approval: Phase 3.
- OCT image preprocessing: Phase 4.
- Model architecture/training and metrics: Phase 5 onward.
- Explainability, uncertainty and calibration implementations: Phases 7–8.
- FastAPI, PostgreSQL and dashboard: Phases 10–11.
- Shared DVC remote: deferred pending cost, access-control, backup, privacy and dataset-licence review.

**Research safeguard:** NeuroVision remains a research prototype. No output from this engineering phase is a medical diagnosis or evidence of clinical validity.
