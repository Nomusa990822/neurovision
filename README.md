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

## Research questions

1. How effectively can deep-learning models classify retinal conditions from OCT images?
2. How useful and stable are different post-hoc explanation methods?
3. Can uncertainty estimates identify unreliable predictions?
4. How well calibrated are predicted probabilities?
5. How does performance change across datasets, scanners and populations?
6. Can the research workflow be delivered as a reproducible software platform?

## Planned technology

| Area | Technology |
|---|---|
| Language | Python 3.12 baseline (Phase 2 decision) |
| Dependency management | uv, `pyproject.toml`, committed `uv.lock` |
| Deep learning | PyTorch (introduced with modelling dependencies) |
| Image processing | OpenCV, NumPy |
| API | FastAPI |
| Database | PostgreSQL |
| Experiment tracking | MLflow |
| Dataset/pipeline versioning | DVC |
| Testing | Pytest |
| Linting/formatting | Ruff |
| Static typing | mypy |
| Deployment | Docker |
| CI | GitHub Actions |

See the [Phase 2 engineering specification](docs/engineering/phase-2-specification.md). These are selected standards and planned technologies; only items explicitly implemented and verified should be described as operational.

## Repository map

- `configs/` — version-controlled experiment and pipeline configuration.
- `data/` — dataset manifests and metadata; raw data is not committed.
- `docs/` — research, governance, architecture and engineering documentation.
- `experiments/` — experiment definitions and records.
- `models/` — model architectures and interfaces.
- `notebooks/` — exploratory analysis, not production pipelines.
- `scripts/` — repeatable command-line workflows.
- `src/neurovision/` — installable Python package (planned Phase 2 scaffold).
- `tests/` — unit, integration, data, scientific and reproducibility tests.
- `web/` — research dashboard.
- `docker/` — container and deployment assets.

## Project status

**Current phase:** Phase 1 — Project Establishment (final approval pending)  
**Current work package:** WP05 — Phase 2 engineering specification (documented; implementation not started)  
**Repository state:** Documentation-first repository. The application scaffold, dependency lock, CI workflow and Docker image are not yet verified. No model training or experimental results are claimed.

See the [roadmap](docs/roadmap.md), [requirements](docs/requirements.md), [repository audit](docs/architecture/repository-audit.md), [decision register](docs/decisions.md), [risk register](docs/risk-register.md) and [engineering specification](docs/engineering/phase-2-specification.md).

## Scientific integrity

- Preserve original datasets and record provenance, licence and acquisition details.
- Never overwrite raw data.
- Use patient-aware grouping whenever reliable patient identifiers are available.
- Keep calibration data separate from final test data.
- Report per-class performance, uncertainty, calibration and confidence intervals.
- Treat heatmaps as diagnostic aids for model investigation, not proof of reasoning.
- Record negative, inconclusive and failed experiments.
- Do not fabricate results or imply clinical validation.

## Documentation

Start with:
1. [Project charter](docs/research/project-charter.md)
2. [Problem statement](docs/research/problem-statement.md)
3. [Research objectives](docs/research/research-objectives.md)
4. [System architecture](docs/architecture/system-architecture.md)
5. [Dataset register](docs/datasets/dataset-register.md)
6. [Data governance](docs/datasets/governance.md)
7. [Evaluation protocol](docs/experiments/evaluation-protocol.md)
8. [Reproducibility strategy](docs/testing/reproducibility-strategy.md)
9. [Phase 2 engineering specification](docs/engineering/phase-2-specification.md)

## Development

Phase 2 will implement the Python package, locked environment, automated quality checks and Docker baseline. Until those artefacts are committed and verified, setup commands and CI status must not be assumed.

## Licence

Original NeuroVision software and project-authored materials are licensed under [Apache License 2.0](LICENSE) (SPDX: Apache-2.0). Third-party code, datasets, OCT images, annotations, pretrained weights and other assets remain subject to their own licences and terms. See [dataset governance](docs/datasets/governance.md).

## Acknowledgements

Dataset authors and institutions will be credited in accordance with their original publications and licences. No dataset is represented as acquired or approved until its provenance and access conditions have been verified.
