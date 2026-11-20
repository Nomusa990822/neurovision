# Scientific Evaluation Protocol

**Status:** Proposed; detailed internal evaluation design is specified in [WP13 — Patient-Grouped Cross-Validation and Model-Selection Protocol](wp13-cross-validation-and-model-selection.md).  
**Scope:** Research evaluation of OCT image classifiers; not clinical validation.

## 1. Evaluation principles

- Preserve patient-level independence in every partition.
- Separate model fitting, model selection, calibration and final evaluation.
- Predefine metrics, selection criteria and analysis procedures before examining outer evaluation results.
- Report class-wise performance, support, uncertainty, calibration and failure modes.
- Preserve original labels and dataset provenance.
- Record negative, inconclusive and failed experiments.
- Do not infer clinical utility, safety or diagnostic validity from retrospective dataset performance.

## 2. Partition roles

- **Training:** fit model parameters and training-only preprocessing.
- **Inner validation:** select architecture, hyperparameters, stopping rules and other model-development choices.
- **Calibration:** fit prespecified probability-calibration parameters using development data only.
- **Outer evaluation:** estimate internal generalisation using patient groups excluded from all fitting, selection and calibration for that iteration.
- **External evaluation:** assess a separate, independently governed cohort after model and protocol freeze.

For the OCTDL V4 candidate, WP13 specifies five-fold patient-grouped outer cross-validation with four-fold patient-grouped inner model selection. The initial outer mapping and its corresponding inner-fold mapping were generated and independently verified locally, but the outer mapping is now quarantined after WP14 identified 39 cross-patient exact-pixel relationships crossing its fold boundaries. It must not be used for model evaluation. Any replacement outer mapping must be independently verified, and all corresponding WP13 inner folds must be regenerated and re-verified before training.

## 3. Leakage controls

Group all images, eyes and repeated records from a patient in one partition. Audit patient overlap and exact duplicate images across partitions; use documented similarity screening for likely near-duplicates. For OCTDL V4, see [WP14 duplicate-screening report](wp14-duplicate-screening.md): the initial outer mapping is quarantined, and the 231-pair nonzero-distance cross-patient visual review remains ongoing. Keep all learned preprocessing, class weighting, sampling, augmentation policy selection, early stopping, hyperparameter tuning, calibration and threshold selection inside the relevant training/inner-validation data.

A patient-grouped split does not by itself detect duplicate images from different patient IDs or cross-dataset overlap. Record the scope and limitations of each check.

## 4. Prediction unit and clustered observations

When labels are assigned to image records, preserve image-level targets and calculate primary classification metrics at image level. Do not collapse a patient's images into one diagnosis without a separately justified target and aggregation rule. Report image and patient support. Account for within-patient correlation using patient-cluster bootstrap confidence intervals and patient-balanced sensitivity analyses where feasible.

## 5. Classification metrics

Report confusion matrix and class-wise precision, recall/sensitivity, specificity and F1. Include macro-F1, weighted F1, balanced accuracy and overall accuracy. Report one-vs-rest ROC-AUC and PR-AUC with explicit averaging conventions and undefined cases. Always show image and patient support per class. The proposed WP13 primary selection criterion is pooled inner out-of-fold image-level macro-F1.

## 6. Calibration

Report multiclass Brier score, negative log-likelihood and ECE with the binning strategy and bin counts. Provide reliability diagrams and class-wise calibration summaries where support permits. Fit calibration parameters only on development data; never use outer evaluation labels to fit or select a calibrator. The proposed initial method is cross-fitted scalar temperature scaling, subject to protocol approval.

## 7. Uncertainty and selective prediction

Specify the uncertainty method and whether it is an uncertainty proxy or an estimate of epistemic/aleatoric uncertainty. Evaluate association between uncertainty and errors, class-wise behaviour and risk-coverage. Report coverage and retained-case error. Select abstention thresholds using development data only. A confidence score alone is not uncertainty validation.

## 8. Explainability

Evaluate reproducibility, perturbation sensitivity, model/parameter randomisation and faithfulness. Use localisation metrics only where suitable reference annotations exist. Visual plausibility alone is not evidence of faithful model reasoning.

## 9. Robustness and external validity

Evaluate image quality, source, scanner, site and class-distribution shifts when metadata permits. External results must identify source, population, label definitions and differences from development data. Freeze the model and protocol before external evaluation. Do not pool external data into training after observing results without defining a new experiment.

## 10. Reproducibility and reporting

Record dataset release and archive hash, split-mapping fingerprint, code revision, environment, model/checkpoint hash, preprocessing, random seeds, hardware, metrics, confidence intervals, calibration, uncertainty, exclusions and limitations. Keep patient identifiers, raw images and row-level patient metadata in access-controlled storage; do not commit them to the public repository or public CI artifacts.

## 11. Interpretation boundary

All findings describe performance on specified research datasets and protocols. They do not establish clinical utility, safety or diagnostic validity. NeuroVision remains a research prototype and is not a clinically validated diagnostic device.

## 12. Detailed protocol

See [WP13 — Patient-Grouped Cross-Validation and Model-Selection Protocol](wp13-cross-validation-and-model-selection.md) for the proposed nested five-fold design, rare-class handling, patient-clustered statistical reporting, calibration, model selection and pre-training approval gates.
