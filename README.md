# NeuroVision

**Explainable and Uncertainty-Aware AI for Retinal Disease Detection Using Optical Coherence Tomography (OCT).**

NeuroVision investigates deep learning, explainability, predictive uncertainty, calibration and rigorous validation for retinal OCT image classification.

> **Research prototype notice:** NeuroVision is not a clinically validated medical device and must not be used to diagnose, triage or guide treatment. Research outputs require expert interpretation and independent validation.

## Current status

**Phase:** 2 — Engineering Foundation
**WP05–WP08:** implementation merged.
**Next:** Phase 3 — Dataset acquisition and audit.

Verified engineering baseline:
- Python 3.12 src-layout package with standard-library settings, path helpers and Python RNG seeding.
- Committed uv.lock and GitHub Actions quality workflow.
- 15 unit tests passed; 98% statement coverage in the verified run.
- Ruff lint/format, mypy and package build passed.
- Non-root Docker image (UID 10001) built and smoke-tested, including production settings and writable data directory.
- PR #5 merged as a975754c747a1c8996d842829a0223fb98b353df after both Python quality and Docker smoke-test jobs passed.

**Final integration check:** the post-merge main-branch workflow is still the final gate before formal Phase 1/2 sign-off.

**Dataset status:** No OCT data has been acquired and no model has been trained. Dataset acquisition, licence verification, integrity checks and empirical patient-level audit remain Phase 3 work.

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

See docs/engineering/phase-2-specification.md, docs/engineering/development-setup.md, docs/engineering/docker.md and docs/roadmap.md.

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
Original NeuroVision software and project-authored materials are licensed under Apache License 2.0. Third-party code, datasets, OCT images, annotations, pretrained weights and other assets remain subject to their own licences and terms.