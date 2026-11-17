# NeuroVision

**Explainable and Uncertainty-Aware AI for Retinal Disease Detection Using Optical Coherence Tomography (OCT).**

NeuroVision investigates deep learning, explainability, predictive uncertainty, calibration and rigorous validation for retinal OCT image classification.

> **Research prototype notice:** NeuroVision is not a clinically validated medical device and must not be used to diagnose, triage or guide treatment. Research outputs require expert interpretation and independent validation.

## Current status

**Phase:** 3 — Dataset Acquisition and Governance Audit  
**Phase 1:** Closed.  
**Phase 2:** Closed; WP05–WP08 merged and verified.  
**Current work package:** WP10 — local dataset acquisition tooling.

Verified engineering baseline:
- Python 3.12 src-layout package with standard-library settings, path helpers and Python RNG seeding.
- Committed uv.lock and GitHub Actions quality workflow.
- 15 unit tests passed; 98% statement coverage in the verified run.
- Ruff lint/format, mypy and package build passed.
- Non-root Docker image (UID 10001) built and smoke-tested, including production settings and writable data directory.
- PR #5 merged as a975754c747a1c8996d842829a0223fb98b353df after both Python quality and Docker smoke-test jobs passed.
- All three post-merge documentation-update workflows completed successfully.

**Dataset status:** No OCT data has been acquired, audited or approved, and no model has been trained. OCTDL V4 is the leading patient-grouped candidate, subject to exact archive/CSV reconciliation and governance approval. Kermany OCT2017 V3 remains conditional on terms review. See [dataset register](docs/datasets/dataset-register.md), [acquisition/audit protocol](docs/datasets/acquisition-audit-protocol.md) and [dataset tooling guide](docs/datasets/tooling.md).\n\nThe local tooling provides candidate manifest generation, SHA-256 hashing, defensive ZIP/TAR inspection and extraction, and deterministic file inventories. It does not download data, decode OCT images or approve dataset use; see the [tooling guide](docs/datasets/tooling.md).

## Project objectives
- Governed OCT dataset pipeline and patient-level leakage prevention.
- Reproducible deep-learning baselines and controlled model comparisons.
- Investigation of visual explanation methods and their limitations.
- Predictive uncertainty, probability calibration and selective prediction.
- Internal performance, robustness and external generalisation evaluation.
- Modular API and research dashboard with experiment traceability.

## Planned technology
| Area | Technology |
|---|---|
| Language | Python 3.12 |
| Deep learning | PyTorch |
| Image processing | OpenCV, NumPy |
| API / database | FastAPI / PostgreSQL |
| Experiment tracking | MLflow |
| Data versioning | DVC |
| Quality | Pytest, Ruff, mypy |
| Deployment / CI | Docker / GitHub Actions |

See [engineering specification](docs/engineering/phase-2-specification.md), [development setup](docs/engineering/development-setup.md), [Docker guide](docs/engineering/docker.md) and [roadmap](docs/roadmap.md).

## Scientific integrity
- Preserve original datasets and record provenance, licence and acquisition details.
- Never overwrite raw data.
- Use patient-aware grouping whenever reliable patient identifiers are available.
- Keep calibration data separate from final test data.
- Report per-class performance, uncertainty, calibration and confidence intervals.
- Treat heatmaps as investigation tools, not proof of model reasoning.
- Record negative, inconclusive and failed experiments.
- Do not fabricate results or imply clinical validation.
- Do not begin model training before the dataset audit and split policy are approved.

## Licence
Original NeuroVision software and project-authored materials are licensed under Apache License 2.0. Third-party code, datasets, OCT images, annotations, pretrained weights and other assets remain subject to their own licences and terms.
