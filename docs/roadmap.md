# NeuroVision Development Roadmap

**Current phase:** 2 — Engineering Foundation
**Implementation:** WP05–WP08 merged. WP08 PR-level Python and Docker verification passed.
**Next:** Phase 3 — Dataset acquisition and audit. Formal Phase 1/2 closure record awaits the post-merge main workflow.

| Phase | Scope | Status |
|---|---|---|
| 1. Project establishment | Charter, objectives, requirements, architecture, governance and roadmap | Documentation complete; formal closure record pending |
| 2. Engineering foundation | Python package, locked environment, CI, Docker and tests | WP05–WP08 merged; post-merge CI/final sign-off pending |
| 3. Dataset acquisition/audit | Source/version and licence checks, acquisition, hashes, metadata, quality and patient audit | Next |
| 4. EDA and preprocessing | Distribution, image quality, preprocessing and split design | Not started |
| 5. Baseline modelling | Baseline CNN and evaluation | Not started |
| 6. Model investigation | Controlled architecture comparisons and ablations | Not started |
| 7. Explainability | Grad-CAM, Integrated Gradients, occlusion and validation | Not started |
| 8. Uncertainty/calibration | Ensembles/dropout, calibration and selective prediction | Not started |
| 9. Scientific evaluation | Internal, external, robustness and subgroup analysis | Not started |
| 10. Backend | FastAPI, inference, PostgreSQL and model metadata | Not started |
| 11. Dashboard/deployment | Frontend, containers, monitoring and security | Not started |
| 12. Reporting/release | Model cards, technical report and reproducibility audit | Not started |

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
- [x] Phase 2 engineering specification drafted and approved.
- [x] Phase 2 engineering implementation authorised.
- [ ] Formal Phase 1 closure record.

## Phase 2 work packages
- [x] WP05 — engineering specification and ADR-020.
- [x] WP06 — Python package scaffold; merged in PR #4.
- [x] WP07 — Python 3.12 lockfile and quality CI; verified in PR #4.
- [x] WP08 — non-root Docker baseline and CI smoke test; PR #5 merged.

## Phase 2 acceptance evidence
PR #4 verified locked Python 3.12 environment, 15 passing unit tests, 98% statement coverage, Ruff lint/format, mypy and wheel/source distribution build.

WP08 verification passed in [GitHub Actions run #44049962338](https://github.com/Nomusa990822/neurovision/actions/runs/44049962338): Python quality and Docker jobs succeeded. The container build and smoke test verified package import, production settings, UID 10001 and write access to its application data directory. PR #5 merged to main as a975754c747a1c8996d842829a0223fb98b353df.

The post-merge main workflow is the final integration gate. Once it passes, record formal Phase 2 acceptance and Phase 1 closure. Missing, skipped or cancelled checks do not count as passing.

Dataset acquisition and empirical patient/integrity audit belong to Phase 3. Model training must not begin before the dataset audit and split policy are approved.