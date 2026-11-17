# NeuroVision Development Roadmap

**Current phase:** Phase 2 — Engineering Foundation  
**Current work package:** WP06 — Initial Python package scaffold  
**Status:** Initial package structure and focused tests added on a feature branch. The dependency lock, automated CI and Docker baseline remain outstanding. Phase 1 documentation and governance work packages are complete; formal Phase 1 closure will be recorded after this approved Phase 2 implementation baseline is reviewed.

Durations are planning estimates, not commitments. Dependencies and dataset access may change.

| Phase | Scope | Exit evidence | Status |
|---|---|---|---|
| 1. Project establishment | Charter, objectives, requirements, architecture, governance, roadmap, source verification | Approved documents and formal sign-off | Documentation complete; formal closure pending |
| 2. Engineering foundation | Python package, locked environment, CI, Docker, tests, logging | Clean setup, passing CI and documented commands | In progress — initial scaffold |
| 3. Dataset acquisition/audit | Exact source/version and licence checks, acquisition, hashes, metadata, quality and patient audit | Dataset register, manifests, audit report and purpose-specific approval | Not started |
| 4. EDA and preprocessing | Distribution, image quality, preprocessing and split design | Reproducible pipeline and leakage tests | Not started |
| 5. Baseline modelling | Baseline CNN and evaluation | Reproducible baseline report and checkpoint | Not started |
| 6. Model investigation | Controlled architecture comparisons and ablations | Comparative experiment report | Not started |
| 7. Explainability | Grad-CAM, Integrated Gradients, occlusion and validation | Explanation artefacts and limitations report | Not started |
| 8. Uncertainty/calibration | Ensembles/dropout, calibration and selective prediction | Calibration and risk-coverage report | Not started |
| 9. Scientific evaluation | Internal, external, robustness and subgroup analysis | Evaluation report with uncertainty and limitations | Not started |
| 10. Backend | FastAPI, inference, PostgreSQL and model metadata | Tested API and integration evidence | Not started |
| 11. Dashboard/deployment | Frontend, containers, monitoring and security | Deployment verification and usability evidence | Not started |
| 12. Reporting/release | Model cards, technical report and reproducibility audit | Reviewed release package | Not started |

## Phase 1 exit checklist

- [x] Project charter, problem statement and research objectives committed.
- [x] Functional and non-functional requirements documented.
- [x] Logical system architecture documented.
- [x] Dataset candidates and source-review findings recorded.
- [x] Dataset governance and patient-leakage controls documented.
- [x] Evaluation and reproducibility strategy documented.
- [x] Repository contents and missing engineering scaffold audited.
- [x] Apache-2.0 software licence selected and LICENSE committed.
- [x] Local-first data strategy selected; shared DVC remote deferred.
- [x] Phase 2 engineering specification drafted and approved by project owner.
- [x] Phase 2 engineering implementation authorised.
- [ ] Formal Phase 1 closure record.

## Phase 2 work packages

- [x] WP05 — engineering specification and ADR-020.
- [ ] WP06 — initial Python package scaffold, settings, utilities and unit tests.
- [ ] WP07 — generate/commit uv lockfile, verify Python 3.12 environment, configure Ruff/mypy/pytest and GitHub Actions.
- [ ] WP08 — non-root Docker baseline, package build, CI verification and engineering documentation sign-off.

## Phase 2 acceptance gate

Phase 2 is not complete until locked environment synchronisation, package installation/import, configuration tests, Ruff, mypy, pytest, wheel/sdist build, pull-request CI and Docker smoke test have all been executed and their evidence recorded. Missing, skipped or cancelled checks do not count as passing.

Dataset acquisition and empirical patient/integrity audit belong to Phase 3. Model training must not begin before the dataset audit and split policy are approved.
