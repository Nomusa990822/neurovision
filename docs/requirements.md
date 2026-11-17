# System Requirements and Acceptance Criteria

**Status:** Baseline specification; requirements will be refined through implementation and research evidence.

## Functional requirements

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-001 | Dataset ingestion | Supported source files can be indexed with provenance and integrity metadata. |
| FR-002 | Governance | Dataset source, licence, version and permitted use are recorded. |
| FR-003 | Image validation | Corrupt, unsupported or invalid images are detected and reported. |
| FR-004 | Preprocessing | Transformations are configuration-driven and reproducible. |
| FR-005 | Partitioning | Patient groups do not cross partitions where identifiers are available. |
| FR-006 | Training | Training configuration, environment, seed and checkpoint are recorded. |
| FR-007 | Inference | Versioned model returns validated class scores and model identity. |
| FR-008 | Explainability | Supported methods produce aligned artefacts and method metadata. |
| FR-009 | Uncertainty | Uncertainty output has a documented method and interpretation. |
| FR-010 | Calibration | Calibration metrics and reliability plots are produced on a designated calibration/evaluation protocol. |
| FR-011 | Evaluation | Class-wise metrics, confusion matrix and uncertainty analysis are recorded. |
| FR-012 | Experiment tracking | Runs and artefacts can be inspected and compared. |
| FR-013 | API | Versioned endpoints validate inputs and return documented errors. |
| FR-014 | Dashboard | Users can inspect input, output, explanation, uncertainty and limitations. |
| FR-015 | Traceability | Results identify model version and relevant preprocessing/configuration versions. |

## Non-functional requirements

| ID | Category | Acceptance criteria |
|---|---|---|
| NFR-001 | Reproducibility | Dataset manifest, code revision, config, seed and environment are recorded. |
| NFR-002 | Security | Input validation, least privilege, secret management and dependency checks are implemented. |
| NFR-003 | Maintainability | Components have clear interfaces, tests and documentation. |
| NFR-004 | Reliability | Invalid input and runtime failure are handled safely without misleading outputs. |
| NFR-005 | Performance | Latency and resource use are measured on named hardware. |
| NFR-006 | Portability | Supported deployment can be reproduced using documented containers. |
| NFR-007 | Observability | Structured operational logs and health checks are available without exposing sensitive data. |
| NFR-008 | Accessibility | Interface supports readable contrast, keyboard navigation and responsive layouts. |
| NFR-009 | Privacy | Patient-identifying data are minimised, protected and excluded from public artefacts. |
| NFR-010 | Scientific integrity | Metrics are traceable to an evaluation protocol and immutable result artefacts. |

## Research acceptance criteria
No single accuracy threshold defines success. Reports must include, as applicable:
- Accuracy, macro and per-class precision/recall/F1, sensitivity and specificity.
- Confusion matrix, ROC-AUC and precision-recall analysis with appropriate averaging.
- Confidence intervals with resampling at patient level where feasible.
- Calibration metrics such as Brier score, negative log-likelihood and a clearly specified ECE implementation.
- Reliability diagrams and calibration-set provenance.
- Selective prediction risk-coverage analysis.
- Uncertainty analysis by class and correctness.
- Explanation stability/faithfulness investigations and limitations.
- Internal and independent external evaluation where feasible.

## Release gate
A requirement is accepted only when implementation, tests or research evidence, documentation and known limitations have been reviewed. Software passing tests does not establish clinical validity.