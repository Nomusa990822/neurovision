# Phase 1 and Phase 2 Acceptance Record

**Status:** Accepted  
**Recorded:** 2026-11-17  
**Scope:** Project establishment and engineering foundation

## Phase 1 — Project establishment

**Outcome:** Complete.

The project charter, problem statement, research objectives, requirements, system architecture, dataset governance, evaluation protocol, reproducibility strategy, risk register, roadmap and architecture decisions are committed. The repository architecture review identified and documented the modular Python package direction. Apache License 2.0 was selected for original project-authored material only. A local-first data strategy was approved; no shared DVC remote is configured.

## Phase 2 — Engineering foundation

**Outcome:** Complete for the defined foundation scope.

| Work package | Deliverable | Evidence |
|---|---|---|
| WP05 | Engineering specification and ADR-020 | Merged documentation |
| WP06 | Python 3.12 src-layout package, settings, path utilities and tests | PR #4 merged |
| WP07 | Committed uv lockfile and automated Python quality workflow | GitHub-hosted runner verification |
| WP08 | Non-root Docker runtime, build-context exclusions and container smoke tests | PR #5 merged |

### Verified quality evidence

- Python 3.12.16 environment.
- 15 unit tests passed.
- 98% statement coverage in the verified test run.
- Ruff lint and formatting passed.
- mypy passed.
- Locked dependency sync and package build passed.
- Docker image built and smoke-tested.
- Container runtime verified as UID/GID 10001, with production settings and writable application data directory.
- PR #5 merged to main as `a975754c747a1c8996d842829a0223fb98b353df`.
- PR-level workflow: [run #44049962338](https://github.com/Nomusa990822/neurovision/actions/runs/44049962338).
- Post-merge main workflows on the documentation updates all completed successfully: [run #44050384243](https://github.com/Nomusa990822/neurovision/actions/runs/44050384243), [run #44050390407](https://github.com/Nomusa990822/neurovision/actions/runs/44050390407). The README update workflow also completed successfully (run #44050377840).

### Scope limitations

This acceptance does not claim that NeuroVision has a trained model, acquired OCT data, completed a dataset audit, or delivered a production API/dashboard. The Docker image is an engineering runtime baseline, not an inference service. PyTorch, OpenCV, NumPy, FastAPI, PostgreSQL, MLflow and DVC integration remain future work packages.

## Phase 1/2 exit decision

The documented project-establishment and engineering-foundation acceptance criteria are met. Phase 1 and Phase 2 are closed. Phase 3 — Dataset Acquisition and Governance Audit — is authorised to begin.

## Phase 3 entry constraints

1. No model training until dataset source, version, terms, integrity and patient grouping are audited and the split policy is approved.
2. Raw OCT data must remain outside Git and must not be placed in public CI artifacts.
3. Dataset licences and terms remain separate from the NeuroVision Apache-2.0 software licence.
4. Any dataset approval is purpose-specific; approval for research use does not imply redistribution rights or external-validation suitability.
5. Empirical findings must be generated from the exact acquired archive and recorded with cryptographic hashes.
