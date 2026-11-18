# Engineering and Research Decision Register

This is the summary register. Significant decisions should have individual ADR files under `docs/architecture/adr/`.

| ID | Decision | Status | Rationale / qualification |
|---|---|---|---|
| ADR-001 | Modular monorepo | Accepted | Shared version history with explicit component boundaries. |
| ADR-002 | Python primary language | Accepted | Research and ML ecosystem. |
| ADR-003 | PyTorch | Accepted | Deep-learning framework preference. |
| ADR-004 | FastAPI | Accepted | Typed, testable API layer. |
| ADR-005 | PostgreSQL | Accepted | Structured application metadata and records. |
| ADR-006 | MLflow | Accepted | Experiment tracking and artefacts. |
| ADR-007 | DVC | Accepted; local-first | Track non-sensitive manifests and DVC metadata initially; no shared remote until storage governance is approved. |
| ADR-008 | Docker | Accepted | Reproducible service packaging. |
| ADR-009 | Patient-aware splitting | Accepted | Prevent leakage when patient grouping is available. |
| ADR-010 | Kermany OCT2017 V3 candidate | Conditional candidate | Large four-class baseline candidate. Exact V3 archive, terms and patient IDs must be independently audited; V2 must not be substituted. |
| ADR-011 | OCTDL candidate | Conditional candidate | Patient IDs and eye metadata make group-aware evaluation feasible; class imbalance and source terms require audit. |
| ADR-012 | OCTID candidate | Pending verification | Image collection source, per-collection rights and patient metadata remain unresolved. |
| ADR-013 | Separate explainability/uncertainty/calibration modules | Accepted | Independent testing and method transparency. |
| ADR-014 | Research prototype boundary | Accepted | No diagnostic or clinical-validity claims. |
| ADR-015 | Apache License 2.0 scope | Accepted | Applies to original NeuroVision software and project-authored materials only; third-party materials retain their own terms. |
| ADR-016 | Dataset version pinning and patient-group audit | Accepted | Dataset versions are not interchangeable; leakage must be checked empirically. |
| ADR-017 | Modular research package boundary | Proposed for Phase 2 approval | Modular monolith with scientific domain logic separated from API/database/UI adapters. |
| ADR-018 | Apache License 2.0 | Accepted | Full canonical licence at repository root; see ADR-018. |
| ADR-019 | Local-first DVC and dataset storage | Accepted | No shared remote until cost, security, privacy and licence implications are assessed. |
| ADR-020 | Phase 2 Python runtime and toolchain | Accepted | Python 3.12, uv lockfile, src-layout package, Ruff, mypy, pytest, CI and minimal Docker baseline; see ADR-020. |
| ADR-022 | Nested patient-grouped cross-validation for OCTDL V4 | Proposed | Five-fold outer evaluation with four-fold inner model selection; exact method, rare-class limitations and approval gates are specified in WP13. The private outer mapping is independently verified but not yet approved for training. |

## Decision process

Each ADR records context, decision, alternatives, consequences, date and status. Reversals require a new record or explicit superseding decision; history must not be silently rewritten.

## Open decisions

- Final dataset selection and exact versions after acquisition audit and purpose-specific rights review.
- Formal approval of the WP13 nested cross-validation and model-selection protocol.
- Completion or documented risk acceptance of duplicate/near-duplicate screening.
- Whether OCTDL can support external evaluation under a prespecified harmonised task.
- Whether OCTID image files and their separate collections can be sourced and licensed for use.
- Supported OCT file formats and image input contract.
- Baseline architecture and input resolution.
- Compute environment and experiment budget.
- DVC remote/storage backend and access controls.
- Frontend framework.
- Data retention and inference audit policy.
