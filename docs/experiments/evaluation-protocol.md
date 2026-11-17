# Scientific Evaluation Protocol

**Status:** Proposed protocol. Final details depend on verified dataset metadata and research design.

## 1. Evaluation principles
Use patient-aware partitions, predefine metrics, preserve a held-out test set and report uncertainty around estimates. Report all classes and relevant failure modes. Do not select a model solely on aggregate accuracy.

## 2. Partition roles
- Training: fit model parameters.
- Validation: architecture/hyperparameter/model selection.
- Calibration: fit post-hoc calibration parameters and any prespecified operating thresholds.
- Internal test: final evaluation after decisions are frozen.
- External test: independent dataset/site/source not used for model selection.

Where data volume limits separate partitions, justify the design and use nested or cross-validation methods without leaking patient groups. Calibration and test observations must remain disjoint.

## 3. Leakage controls
Group by patient wherever identifiers are available. Audit patient, eye and visit relationships. Check exact duplicates across partitions and use similarity-based review for likely near-duplicates. Persist split manifests and test for group overlap before training.

## 4. Classification metrics
Report confusion matrix and class-wise precision, recall/sensitivity, specificity and F1. Include accuracy and macro averages. Use ROC-AUC and precision-recall metrics with clearly specified one-vs-rest or averaging conventions. Report support/counts for every class. Provide confidence intervals, preferably using patient-level bootstrap resampling.

## 5. Calibration
Report Brier score and negative log-likelihood, plus ECE with binning strategy explicitly documented. Provide reliability diagrams and calibration-set details. Compare uncalibrated and calibrated outputs on held-out evaluation data. Do not fit calibration on the final test set.

## 6. Uncertainty and selective prediction
Specify the uncertainty method and whether it estimates epistemic, aleatoric or a proxy. Evaluate association between uncertainty and errors, class-wise behaviour and risk-coverage curves. Report coverage, retained-case error and the threshold-selection procedure. A confidence score alone is not an uncertainty validation.

## 7. Explainability
Evaluate output alignment and reproducibility. Investigate sensitivity to perturbations, parameter/model randomisation and method choice. Where reference annotations exist, use appropriate localisation metrics. Treat visual plausibility as insufficient evidence of faithfulness.

## 8. Robustness and external validity
Evaluate relevant changes in image quality, source, scanner and class distribution when metadata permits. External results must identify source, population, label definitions and differences from development data. Do not pool external data into training after observing results without defining a new experiment.

## 9. Reporting
Record model/checkpoint hash, code revision, dataset and split manifest hashes, preprocessing config, random seeds, environment, hardware, metrics, confidence intervals, exclusions and limitations. Report negative and inconclusive findings.

## 10. Interpretation boundary
All findings describe performance on specified research datasets and protocols. They do not establish clinical utility, safety or diagnostic validity.