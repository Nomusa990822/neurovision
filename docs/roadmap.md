# NeuroVision Development Roadmap

**Current phase:** 3 — Dataset Acquisition and Governance Audit  
**Phase 1:** Closed; acceptance record committed.  
**Phase 2:** Closed; WP05–WP08 merged and verified on GitHub-hosted runners.  
**Current work package:** WP14 — Exact and near-duplicate screening.  
**Next gate:** Complete blinded review of 231 cross-patient nonzero-distance candidates, rebuild and verify a duplicate-aware patient-grouped split, and complete dataset-use approval before any training.

| Phase | Scope | Status |
|---|---|---|
| 1. Project establishment | Charter, objectives, requirements, architecture, governance and roadmap | Complete; accepted 2026-11-17 |
| 2. Engineering foundation | Python package, locked environment, CI, Docker and tests | Complete; accepted 2026-11-17 |
| 3. Dataset acquisition/audit | Source/version and licence checks, acquisition, hashes, metadata, quality and patient audit | In progress — archive/image/metadata audit complete; WP14 exact-pixel investigation has identified cross-fold relationships and quarantined the initial outer mapping; 231 nonzero-distance cross-patient candidates await visual review; replacement split and dataset-use approval remain open |
| 4. EDA and preprocessing | Distribution, image quality, preprocessing and split design | Not started |
| 5. Baseline modelling | Baseline CNN and evaluation | Blocked on Phase 3 audit and split approval |
| 6. Model investigation | Controlled architecture comparisons and ablations | Not started |
| 7. Explainability | Grad-CAM, Integrated Gradients, occlusion and validation | Not started |
| 8. Uncertainty/calibration | Ensembles/dropout, calibration and selective prediction | Not started |
| 9. Scientific evaluation | Internal, external, robustness and subgroup analysis | Not started |
| 10. Backend | FastAPI, inference, PostgreSQL and model metadata | Not started |
| 11. Dashboard/deployment | Frontend, containers, monitoring and security | Not started |
| 12. Reporting/release | Model cards, technical report and reproducibility audit | Not started |

## Phase 1 and Phase 2 acceptance

See [Phase 1 and Phase 2 Acceptance Record](engineering/phase-2-acceptance.md). Phase 1 and Phase 2 are closed based on committed project documentation, merged implementation and successful GitHub Actions verification.

Verified evidence:
- PR #4: Python 3.12.16, 15 passing unit tests, 98% statement coverage, Ruff, mypy, locked sync and package build.
- PR #5: Python quality and Docker smoke-test jobs passed in [run #44049962338](https://github.com/Nomusa990822/neurovision/actions/runs/44049962338). The non-root container was verified as UID 10001 with writable application data.
- Post-merge main workflows passed: [run #44050377840](https://github.com/Nomusa990822/neurovision/actions/runs/44050377840), [run #44050384243](https://github.com/Nomusa990822/neurovision/actions/runs/44050384243), [run #44050390407](https://github.com/Nomusa990822/neurovision/actions/runs/44050390407).

## Phase 3 work packages

- [x] WP09 — dataset acquisition and audit protocol; version-specific source review updated.
- [x] WP10 — local manifest, SHA-256, archive safety and file inventory tooling; merged and verified in [run #44053030829](https://github.com/Nomusa990822/neurovision/actions/runs/44053030829) (29 tests, Ruff, mypy, build and Docker smoke test).
- [x] WP11 — acquire and record OCTDL V4 provenance; verify archive SHA-256/LFS integrity, ZIP CRC, image inventory/decoding, dimensions and CSV reconciliation. File-level licence review remains open.
- [x] WP12 — complete local image, label, metadata and patient-group audits; create and independently verify an initial candidate five-fold patient-grouped outer assignment. That assignment is now quarantined following WP14 cross-patient exact-pixel findings; it must not be used for evaluation.
- [x] WP13 — approve the nested patient-grouped evaluation protocol, implement the inner-fold generator and verify the existing private execution: 3,280 assignments across 820 patients and five outer iterations. These inner folds correspond to the original outer mapping and must be regenerated and re-verified if a replacement outer assignment is adopted.
- [~] WP14 — exact SHA-256 and perceptual dHash screening implemented and executed locally. All 354 candidates were computationally examined; 54 dimension-aware exact-pixel matches were found (47 cross-patient). The 87 zero-distance candidates received blinded visual review. A 231-pair cross-patient nonzero-distance visual-review pack is generated; review remains ongoing. The initial outer mapping is quarantined. See [WP14 report](experiments/wp14-duplicate-screening.md).

## Phase 3 candidate strategy

OCTDL Mendeley V4 is the leading candidate for patient-grouped experiments because its published record describes 2,064 images from 821 patients and includes patient/eye fields in its CSV. This is a candidate recommendation, not independent verification or approval. Kermany OCT2017 V3 remains a large four-class candidate but has research-only wording alongside a CC BY 4.0 display that requires terms review. OCTID remains conditional because its actual image source and patient metadata have not been verified.

## Non-negotiable research gate

No model training before the exact acquired release passes provenance, licence, integrity, label, duplicate and patient-grouping audits and the split policy is approved. Raw OCT data must remain outside Git and public CI artifacts. A dataset approved for model development is not automatically approved for external validation or redistribution.
