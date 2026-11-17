# Project Risk Register

Likelihood and impact are qualitative and must be revised as evidence changes.

| ID | Risk | Impact | Mitigation | Status |
|---|---|---|---|---|
| R-001 | Patient-level leakage | Critical | Grouped partitions, split manifests and automated overlap tests | Open |
| R-002 | Incorrect or unclear dataset licence | High | Verify publisher terms and record attribution before use | Open |
| R-003 | Class imbalance | High | Per-class metrics, confidence intervals and justified sampling | Open |
| R-004 | Domain shift | High | Independent external testing and domain metadata | Open |
| R-005 | Misleading explanations | High | Faithfulness, stability and randomisation checks; qualify visualisations | Open |
| R-006 | Poor probability calibration | High | Separate calibration data and report calibration metrics | Open |
| R-007 | Dataset-specific shortcuts | High | Image audit, artefact analysis, perturbations and external evaluation | Open |
| R-008 | Limited compute | Medium | Start with lightweight baselines; document hardware and budgets | Open |
| R-009 | Reproducibility failure | High | Pin dependencies, record seeds/configs and track manifests/checkpoints | Open |
| R-010 | Corrupt/duplicate images | Medium | Hashes, decoding checks and duplicate audits | Open |
| R-011 | Privacy exposure | High | Data minimisation, access controls and no patient data in public Git | Open |
| R-012 | Overstated clinical claims | Critical | Research-prototype disclaimer and review of all public reporting | Open |

## Risk review
Review risks at each phase gate and whenever dataset, model, infrastructure or deployment scope changes. Record evidence and residual risk; do not mark a risk closed solely because mitigation is planned.