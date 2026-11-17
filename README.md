# NeuroVision

**Explainable and Uncertainty-Aware AI for Retinal Disease Detection Using Optical Coherence Tomography (OCT).**

NeuroVision is a research and engineering project investigating how deep learning, explainability, predictive uncertainty, calibration and rigorous validation can be combined in a reproducible platform for retinal OCT image classification.

> **Research prototype notice:** NeuroVision is not a clinically validated medical device and must not be used to diagnose, triage or guide treatment. Research outputs require expert interpretation and independent validation.

## Project objectives

- Build a traceable, governed OCT dataset pipeline.
- Prevent patient-level leakage in dataset partitioning.
- Establish reproducible deep-learning baselines and controlled model comparisons.
- Investigate visual explanation methods and their limitations.
- Estimate predictive uncertainty and evaluate probability calibration.
- Assess internal performance, robustness and external generalisation.
- Deliver a modular API and research dashboard with experiment traceability.

## Planned technology

| Area | Technology |
|---|---|
| Language | Python 3.12 baseline |
| Dependency management | uv, `pyproject.toml`, `uv.lock` (lockfile pending) |
| Deep learning | PyTorch (modelling phase) |
| Image processing | OpenCV, NumPy |
| API / database | FastAPI / PostgreSQL |
| Experiment tracking | MLflow |
| Data versioning | DVC |
| Quality | Pytest, Ruff, mypy |
| Deployment / CI | Docker / GitHub Actions |

See the [Phase 2 engineering specification](docs/engineering/phase-2-specification.md).

## Repository structure

- `docs/` — research, governance, architecture and engineering documentation.
- `src/neurovision/` — installable Python package.
- `tests/` — unit, integration, data, scientific and reproducibility tests.
- `data/` — manifests and metadata only; raw datasets are not committed.
- `configs/`, `experiments/`, `models/`, `notebooks/`, `scripts/`, `web/`, `docker/` — planned research and application areas.

## Current status

**Phase:** 2 — Engineering Foundation  
**Work package:** WP06 — Initial Python package scaffold  
**Implemented in this work package:** src-layout package metadata, Python 3.12 declaration, immutable environment-backed settings, project/data path helpers, Python RNG seed helper, focused unit tests, ignore rules and setup documentation.

**Still pending:** generated and committed `uv.lock`, full local verification under Python 3.12, Ruff/mypy execution, GitHub Actions CI, Docker image and complete Phase 2 acceptance evidence. This scaffold is not yet a verified reproducible environment. No OCT data has been acquired and no model has been trained.

See the [roadmap](docs/roadmap.md), [requirements](docs/requirements.md), [repository audit](docs/architecture/repository-audit.md), [decision register](docs/decisions.md), [risk register](docs/risk-register.md) and [development setup](docs/engineering/development-setup.md).

## Scientific integrity

- Preserve original datasets and record provenance, licence and acquisition details.
- Never overwrite raw data.
- Use patient-aware grouping whenever reliable patient identifiers are available.
- Keep calibration data separate from final test data.
- Report per-class performance, uncertainty, calibration and confidence intervals.
- Treat heatmaps as investigation tools, not proof of model reasoning.
- Record negative, inconclusive and failed experiments.
- Do not fabricate results or imply clinical validation.

## Licence

Original NeuroVision software and project-authored materials are licensed under [Apache License 2.0](LICENSE) (SPDX: Apache-2.0). Third-party code, datasets, OCT images, annotations, pretrained weights and other assets remain subject to their own licences and terms. See [dataset governance](docs/datasets/governance.md).
