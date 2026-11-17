# Repository Architecture Audit

- Work package: NV-P1-WP03
- Review date: 2026-11-17
- Reviewed branch: main
- Reviewed commit: be30b816bdcc1d8121fce2c482ee6e6d79f5c42c
- Status: review completed; no application code or tests executed.

## Verified repository state

The default branch is main. The recursive Git tree contains a documentation-first repository: root README and changelog plus research, architecture, dataset, experiment, testing, requirements, roadmap, decision and risk documentation.

The tree does not contain application source, Python packaging metadata, a dependency lock, tests, CI workflows, Docker assets, environment templates or ignore rules. The repository metadata reports public visibility. Branch protection is not enabled on main at review time.

## Strengths

- Research purpose and research-prototype boundary are explicit.
- Research questions and system requirements are documented.
- Logical architecture is documented separately from implementation.
- Dataset provenance, licensing and patient-level leakage are acknowledged.
- Evaluation covers discrimination, calibration, uncertainty and explanation limitations.
- Reproducibility and risk registers exist.
- Decision records distinguish proposed choices from implemented software.

## Gaps and Phase 2 actions

| Area | Observed state | Required action |
|---|---|---|
| Python package | Absent | Add pyproject.toml and src/neurovision/ |
| Dependency control | No manifest or lock | Pin supported Python and direct dependencies; create reproducible lock |
| Configuration | Absent | Add validated typed configuration |
| Tests | Absent | Add pytest and unit/API smoke tests |
| CI | Absent | Add GitHub Actions for lint, tests and dependency checks |
| Code quality | No tool configuration | Select formatter, linter and appropriate static checks |
| Containerisation | Absent | Add non-root Docker image after app entrypoint exists |
| Secrets | No environment template or ignore rules | Add .gitignore and .env.example; keep secrets out of Git |
| Data safety | No data policy placeholder | Document local data zones; never commit raw OCT images |
| Experiment tracking | Planned only | Integrate MLflow after package/config foundation |
| DVC | Planned only | Decide remote storage and access controls before enabling |
| Application | Not implemented | Defer FastAPI/UI until package foundation is tested |

## Proposed Phase 2 structure

This is a target structure, not a claim that these files exist.

```text
neurovision/
├── .github/workflows/ci.yml
├── configs/{data,model,training}/
├── data/{README.md,manifests/,processed/}
├── docker/
├── docs/
├── experiments/README.md
├── models/README.md
├── notebooks/README.md
├── scripts/
├── src/neurovision/
│   ├── config/
│   ├── data/
│   ├── evaluation/
│   ├── explainability/
│   ├── inference/
│   ├── models/
│   ├── uncertainty/
│   └── utils/
├── tests/{unit,integration}/
├── web/
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
└── pyproject.toml
```

## Module boundaries

- data: dataset adapters, manifests, validation and split logic; no training orchestration.
- models: architectures and model interfaces; no API concerns.
- evaluation: metrics, confidence intervals, subgroup and robustness analysis.
- explainability: attribution/perturbation methods and explanation-quality tests.
- uncertainty: estimators, calibration and selective prediction.
- inference: model loading, preprocessing contract and prediction orchestration.
- config: validated configuration and environment settings.
- API/UI: application adapters that orchestrate tested package services.

## Phase 2 sequence

1. Decide software licence, Python version policy and dependency strategy.
2. Add .gitignore, .env.example, pyproject.toml and package skeleton.
3. Add configuration loading and structured logging.
4. Add minimal tests and CI quality gates.
5. Add Docker packaging and health checks after package tests pass.
6. Document exact setup, test and run commands.
7. Review CI evidence before declaring Phase 2 complete.

Do not add dataset files, train models or claim experimental results in Phase 2.

## Open governance decisions

- Software licence: no LICENSE file exists.
- Python version and package/lock strategy.
- DVC remote and secure access controls.
- Branch protection and pull-request policy.
- Whether the first service is library-only or includes a minimal FastAPI health endpoint.

## Conclusion

The repository is a sound documentation baseline but is not yet an executable software project. This is an expected Phase 1 state. The recommended direction is a modular monolith with an installable Python research package and separate application adapters.

No code tests, lint checks, CI runs, Docker builds or model experiments were performed during this review.
