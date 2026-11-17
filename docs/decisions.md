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
| ADR-007 | DVC | Accepted in principle | Dataset/pipeline versioning; storage backend to be selected. |
| ADR-008 | Docker | Accepted | Reproducible service packaging. |
| ADR-009 | Patient-aware splitting | Accepted | Prevent leakage when patient grouping is available. |
| ADR-010 | Kermany OCT2017 V3 candidate | Conditional candidate | Large four-class baseline candidate. Exact V3 archive, terms and patient IDs must be independently audited; V2 must not be substituted. |
| ADR-011 | OCTDL candidate | Conditional candidate | Patient IDs and eye metadata make group-aware evaluation feasible; class imbalance and source terms require audit. |
| ADR-012 | OCTID candidate | Pending verification | Image collection source, per-collection rights and patient metadata remain unresolved. |
| ADR-013 | Separate explainability/uncertainty/calibration modules | Accepted | Independent testing and method transparency. |
| ADR-014 | Research prototype boundary | Accepted | No diagnostic or clinical-validity claims. |
| ADR-015 | Project software licence | Open | Select after considering dependencies and intended contribution model. |
| ADR-016 | Dataset version pinning and patient-group audit | Accepted | Dataset versions are not interchangeable; leakage must be checked empirically. |

## Decision process

Each ADR records context, decision, alternatives, consequences, date and status. Reversals require a new record or explicit superseding decision; history must not be silently rewritten.

## Open decisions

- Final dataset selection and exact versions after acquisition audit.
- Whether OCTDL can support external evaluation under a prespecified harmonised task.
- Whether OCTID image files and their separate collections can be sourced and licensed for use.
- Supported OCT file formats and image input contract.
- Baseline architecture and input resolution.
- Compute environment and experiment budget.
- DVC remote/storage backend.
- Frontend framework.
- Project software licence.
- Data retention and inference audit policy.
