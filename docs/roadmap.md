# NeuroVision Development Roadmap

**Current phase:** Phase 1 — Project Establishment  
**Status:** Foundation documentation committed; primary-source desk review of initial OCT dataset candidates recorded. Phase 1 remains open pending repository review and final governance decisions.

Durations are planning estimates, not commitments. Dependencies and dataset access may change the schedule.

| Phase | Scope | Exit evidence | Status |
|---|---|---|---|
| 1. Project establishment | Charter, objectives, requirements, architecture, governance, roadmap, source verification | Approved documents, verified repository baseline and signed-off Phase 1 review | In progress |
| 2. Engineering foundation | Python package, pinned environment, CI, Docker, tests, logging | Clean setup, passing CI and documented commands | Proposed |
| 3. Dataset acquisition/audit | Exact source/version and licence checks, acquisition, hashes, metadata, quality and patient audit | Dataset register, manifests, audit report and purpose-specific approval | Proposed |
| 4. EDA and preprocessing | Distribution, image quality, preprocessing and split design | Reproducible pipeline and leakage tests | Proposed |
| 5. Baseline modelling | Baseline CNN and evaluation | Reproducible baseline report and checkpoint | Proposed |
| 6. Model investigation | Controlled architecture comparisons and ablations | Comparative experiment report | Proposed |
| 7. Explainability | Grad-CAM, Integrated Gradients, occlusion and validation | Explanation artefacts and limitations report | Proposed |
| 8. Uncertainty/calibration | Ensembles/dropout, calibration and selective prediction | Calibration and risk-coverage report | Proposed |
| 9. Scientific evaluation | Internal, external, robustness and subgroup analysis | Final evaluation report with uncertainty/limitations | Proposed |
| 10. Backend | FastAPI, inference, PostgreSQL and model metadata | Tested API and integration evidence | Proposed |
| 11. Dashboard/deployment | Frontend, containers, monitoring and security | Deployment verification and usability evidence | Proposed |
| 12. Reporting/release | Model cards, technical report and reproducibility audit | Reviewed release package | Proposed |

## Release milestones

- v0.1.0 — engineering foundation.
- v0.2.0 — audited dataset pipeline.
- v0.3.0 — baseline research.
- v0.4.0 — comparative model investigation.
- v0.5.0 — explainability.
- v0.6.0 — uncertainty and calibration.
- v0.7.0 — scientific evaluation.
- v0.8.0 — backend integration.
- v0.9.0 — dashboard and deployment.
- v1.0.0 — documented research prototype.

Release tags are planned milestones, not claims of completion or clinical readiness.

## Milestone governance

Every milestone must have an ID, owner, dependencies, acceptance criteria, evidence links and documentation updates. A task is not complete merely because code was written or a command ran. Failed checks and unresolved issues remain visible.

## Immediate next work

Complete Phase 1 repository consistency review and formal approval of the project foundation. Then establish the engineering scaffold in Phase 2. Dataset acquisition and empirical audit belong to Phase 3; no model training before that audit is complete.
