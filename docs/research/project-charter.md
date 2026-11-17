# NeuroVision — Project Charter

**Status:** Approved project direction; implementation not yet verified  
**Project:** NeuroVision  
**Research title:** Explainable and Uncertainty-Aware AI for Retinal Disease Detection Using Optical Coherence Tomography

## 1. Purpose
Develop a reproducible research platform to investigate retinal OCT image classification alongside explainability, predictive uncertainty, calibration and generalisation. The project integrates scientific experimentation with maintainable software engineering.

## 2. Vision and mission
The vision is a scientifically rigorous, transparent and professionally engineered platform for studying the reliability and interpretability of deep-learning systems applied to retinal OCT images.

The mission is to acquire and govern suitable datasets; develop controlled model baselines; investigate explanations and uncertainty; evaluate calibration, robustness and external generalisation; and expose research outputs through a traceable software application.

## 3. Scope
**In scope**
- OCT dataset acquisition, provenance, licensing and governance.
- Image integrity, quality assessment, exploratory analysis and preprocessing.
- Patient-aware data partitioning and leakage audits.
- Deep-learning baselines and controlled architecture comparisons.
- Explainability methods and explanation-quality investigations.
- Predictive uncertainty, calibration and selective prediction.
- Internal and independent external evaluation.
- Experiment tracking, model documentation, API, dashboard and deployment.
- Reproducibility, testing, security and technical reporting.

**Out of scope**
- Autonomous diagnosis, treatment recommendations or clinical triage.
- Claims of regulatory approval or clinical validation.
- Use of data without appropriate access rights and governance.
- Treating model confidence or heatmaps as clinical evidence.

## 4. Stakeholders and responsibilities
The project owner/researcher is responsible for research decisions, data access, implementation review and approval of deliverables. The engineering workflow provides architecture, implementation guidance, testing plans and documentation support. Any future clinical interpretation requires appropriately qualified domain experts and is outside the authority of this prototype.

## 5. Technical baseline
Python, PyTorch, OpenCV/NumPy, FastAPI, PostgreSQL, MLflow, DVC, Pytest, Docker and GitHub Actions are the preferred stack. Final versions and configurations will be pinned and verified during Phase 2.

## 6. Principles
1. Preserve original datasets.
2. Record provenance and licensing.
3. Prevent patient-level leakage wherever identifiers permit.
4. Separate training, validation, calibration and final testing roles.
5. Track code, data manifests, configurations and checkpoints.
6. Evaluate discrimination, calibration, uncertainty and generalisation.
7. Investigate explanation faithfulness and stability.
8. Report limitations and negative findings.
9. Never invent metrics, results or completed milestones.
10. Maintain the research-prototype boundary.

## 7. Success criteria
The project succeeds as a research-engineering portfolio when its data pipeline is auditable, experiments are reproducible, evaluation is scientifically defensible, uncertainty and explanation limitations are reported, software components are tested and documented, and the deployed prototype communicates its limitations clearly.

## 8. Governance
The roadmap, requirements, decision register, risk register, dataset register, experiment register and changelog are authoritative project records. A milestone is not complete until its acceptance criteria and evidence are reviewed and documentation is synchronised.

## 9. Constraints and assumptions
Dataset access, licensing, patient metadata, compute capacity and availability of independent external datasets remain subject to verification. Timelines are estimates and will be revised based on evidence.

## 10. Status
The charter establishes project direction. It does not assert that the repository scaffold, datasets, models, experiments or application have been implemented.