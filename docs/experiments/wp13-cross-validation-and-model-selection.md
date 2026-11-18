# WP13 — Patient-Grouped Cross-Validation and Model-Selection Protocol

**Status:** Protocol approved by project owner on 2026-11-18; implementation and pre-training gates remain outstanding.  
**Work package:** WP13 — Cross-validation and model-selection protocol.  
**Dataset candidate:** OCTDL Mendeley Data Version 4 (DOI: 10.17632/sncdhf53xc.4).  
**Protocol version:** 1.0  
**Date:** 2026-11-18

## 1. Purpose and scope

This protocol defines how NeuroVision will develop and internally evaluate OCT image classifiers using the audited OCTDL V4 candidate. It separates model development from held-out evaluation, preserves patient-level independence, and defines how class imbalance, calibration, uncertainty and clustered observations will be handled.

This document is a research protocol, not evidence of model performance or clinical validity. It does not authorise training until dataset-use approval, licence review and the remaining audit gates are complete.

## 2. Dataset and split evidence available at protocol drafting

The local audit reports the following:

- 2,064 image records and 820 unique patient identifiers.
- Seven image-level disease labels: AMD, DME, ERM, NO, RAO, RVO and VID.
- One patient has records associated with both AMD and DME. Consequently, the sum of disease-specific patient counts is 821 although the number of unique patients is 820.
- A deterministic five-fold patient-grouped allocation was generated using a randomised greedy multistart procedure, 1,000 candidate allocations and base seed 20261117.
- The saved mapping was independently reconciled against the source CSV. All 820 patients were assigned exactly once, all 2,064 image rows were accounted for, and no patient appeared in more than one fold.
- The mapping SHA-256 is 328ba1d5809cb7cf9bd5fc43405e30ef46c3bf503a39d0387212ae1e9c8487ff.

The mapping itself contains patient identifiers and must remain in the private data environment. The public repository may contain this fingerprint and aggregate counts, but must not contain the mapping, patient identifiers, filenames or row-level metadata.

The allocation objective is a heuristic balance score, not a model metric and not proof of a globally optimal partition. Fold balance does not establish external validity or eliminate all forms of dataset bias.

### 2.1 Verified fold composition

| Fold | Patients | Image records |
|---|---:|---:|
| 1 | 163 | 411 |
| 2 | 166 | 412 |
| 3 | 164 | 412 |
| 4 | 163 | 413 |
| 5 | 164 | 416 |
| **Total** | **820** | **2,064** |

All seven labels occur in every fold. RAO is represented by only 11 patients in the full dataset, distributed across folds as 2, 3, 2, 2 and 2 patients. Its class-specific estimates will therefore be imprecise.

## 3. Primary evaluation design: nested patient-grouped cross-validation

Use five outer folds for internal evaluation. In outer iteration k:

1. Set outer fold k aside as the untouched evaluation fold.
2. Combine the other four folds as the outer-training pool.
3. Conduct model and hyperparameter selection only within that outer-training pool using four-fold patient-grouped inner cross-validation.
4. Select one configuration using the prespecified selection rule in Section 6.
5. Refit the selected configuration on the complete outer-training pool.
6. Evaluate once on outer fold k. Do not use outer-fold results to change the configuration for that iteration.
7. Save per-image predictions, probabilities, model/checkpoint metadata and the exact training configuration.

Repeat for all five outer folds. Each patient is in exactly one outer evaluation fold. The five outer evaluation outputs form the out-of-fold (OOF) prediction set.

The existing five-fold mapping is the proposed outer assignment. Inner folds must be generated deterministically from only the outer-training patients, using a documented seed and a patient-grouped, class-aware allocation method. Inner fold assignments must be regenerated separately for each outer iteration and must never include patients from the corresponding outer evaluation fold.

### 3.1 Inner-fold feasibility and rare classes

The outer-training pool will contain approximately 8–9 RAO patients. Four inner folds are proposed to keep the inner validation groups small while retaining a useful training pool. Some inner validation folds may contain only one or two RAO patients. Inner RAO metrics must not be treated as stable estimates or used as the sole selection criterion.

Before training, an implementation-level feasibility check must confirm that every inner split has non-empty training and validation partitions, no patient overlap, and both positive and negative examples for metrics that require them. If a class is absent from an inner validation partition, its fold-specific AUC is undefined and must be recorded as such, not replaced with zero. If the chosen inner allocation cannot retain meaningful class coverage, reduce the number of inner folds or use a prespecified alternative; record the deviation before inspecting outer results.

### 3.2 No repeated test-set tuning

Outer-fold metrics are evaluation results, not tuning feedback. Do not repeatedly alter architectures, preprocessing, thresholds, class weights or training schedules in response to outer-fold outcomes and then report those same outcomes as unbiased evaluation. Any such change creates a new experiment and requires a new untouched evaluation source or a clearly qualified exploratory analysis.

## 4. Prediction unit and patient clustering

The dataset labels are attached to image records. The primary prediction and classification-metric unit is therefore the OCT image record, with the seven-class target preserved at image level.

Patient grouping applies to partitioning, not to rewriting labels. In particular:

- Do not collapse all records from a patient into one diagnosis.
- Preserve the two disease labels associated with the single multi-label patient on their respective image records.
- Keep all images, both eyes and repeated records belonging to a patient in the same outer and inner partition.
- Report both image counts and unique patient counts for every class and partition.
- Because patients contribute different numbers of images, image-level metrics may give more influence to patients with more records. Include a patient-balanced sensitivity analysis where feasible.
- Calculate confidence intervals by resampling patients as clusters and retaining all image records belonging to each sampled patient. Do not bootstrap image rows independently as though they were independent observations.

A future patient-level decision task would require a separately defined target and aggregation rule; it must not be inferred from this image-level protocol.

## 5. Leakage prevention and preprocessing controls

All of the following operations must be fitted or selected using only the relevant training portion within each inner or outer iteration:

- image-derived normalisation statistics;
- class weights, sampling weights and resampling decisions;
- feature selection or dimensionality reduction;
- learned preprocessing and augmentation policies;
- early stopping and checkpoint selection;
- hyperparameter selection;
- probability calibration and operating-threshold selection.

Apply stochastic augmentation only to training images. Validation and evaluation images receive deterministic inference preprocessing. Do not use outer evaluation images to estimate normalisation statistics, select augmentations, tune class weights, choose checkpoints or set thresholds.

Patient-level grouping is necessary but not sufficient. Before training, complete exact-hash duplicate screening and document the scope and limitations of near-duplicate screening. Check for duplicated images across all partitions and, where possible, across candidate datasets.

## 6. Model selection and training policy

### 6.1 Prespecified search space

Begin with a small, documented candidate set rather than an unrestricted architecture search. The baseline architecture, input size, optimiser, learning-rate schedule, batch size, maximum epochs, stopping rule, augmentation policy and random seeds must be specified in a versioned experiment configuration before the outer evaluation is run.

Any pretrained weights must have documented provenance, licence, source domain and hash. The use of external OCT data in pretraining must be disclosed and checked for overlap with evaluation data where feasible.

### 6.2 Primary selection criterion

Use pooled inner OOF image-level macro-F1 across the seven labels as the primary model-selection criterion. Pool the inner OOF predictions for the outer-training patients before calculating the score, so every outer-training image is evaluated by a model that did not train on its patient.

Use macro one-vs-rest PR-AUC as a secondary criterion where mathematically defined. If candidates are effectively tied under the primary criterion, prefer the simpler model with fewer parameters and lower computational cost. Do not choose a model based on outer-fold results.

Because RAO is rare, report per-class support alongside every selection result. Also report balanced accuracy and class-wise sensitivity/recall. Do not interpret an unstable RAO inner-fold score as reliable evidence of superiority.

### 6.3 Class imbalance

Do not silently discard or merge classes. Candidate imbalance strategies may include training-subset class weighting or carefully controlled sampling, but their values must be calculated from the current training partition only. Compare a plain baseline against a limited number of prespecified strategies. Avoid synthetic image generation or oversampling that could create near-duplicate leakage.

Record the exact class counts and effective weights for each training run. Any strategy that changes the target distribution must be documented, and evaluation metrics must be calculated on the unaltered held-out data.

### 6.4 Repeated runs and compute constraints

Record all random seeds and the number of runs. A single seed is acceptable for an initial engineering baseline but is insufficient to characterise training variability. Repeat the selected configuration with additional seeds when compute permits and report the limitation if it does not. Do not imply that five outer folds alone quantify all sources of stochastic training uncertainty.

## 7. Calibration protocol

Calibration is evaluated separately from discrimination. The initial prespecified post-hoc method is scalar temperature scaling for the seven-class logits.

Within each outer iteration:

1. Generate patient-grouped inner OOF logits for the selected configuration using only the outer-training pool.
2. Fit the temperature parameter using those inner OOF logits and labels only.
3. Refit the selected classifier on the full outer-training pool.
4. Apply the fitted temperature to the outer-fold logits without refitting or adjusting it on outer-fold labels.
5. Compare calibrated and uncalibrated predictions on the outer evaluation fold.

This cross-fitted calibration procedure is an approximation because the inner OOF models are trained on subsets of the outer-training pool while the final outer model is trained on the full pool. Record this limitation. If a separate calibration partition is later feasible, evaluate that design as a separately specified protocol.

Report multiclass Brier score, negative log-likelihood, and expected calibration error (ECE), including the ECE binning rule and bin counts. Include reliability diagrams and class-wise calibration summaries where support permits. Do not fit calibration parameters or choose calibration methods using outer evaluation labels.

## 8. Metrics and statistical reporting

### 8.1 Primary and secondary metrics

Primary internal discrimination metric:
- image-level macro-F1 across the seven classes.

Secondary metrics:
- per-class precision, recall/sensitivity, specificity and F1;
- macro and weighted F1;
- balanced accuracy and overall accuracy;
- one-vs-rest ROC-AUC and PR-AUC, with averaging convention and undefined cases stated;
- confusion matrix with raw counts;
- multiclass Brier score and negative log-likelihood;
- ECE and reliability diagrams;
- uncertainty/error association and risk-coverage curves once an uncertainty method is prespecified.

Always report image support and unique-patient support for every class. Include both pooled OOF metrics and fold-level results. Do not report only a single aggregate accuracy.

### 8.2 Confidence intervals

Use patient-cluster bootstrap resampling for OOF metrics: sample patients with replacement and include all image records belonging to each sampled patient. State the number of bootstrap replicates, random seed and interval method. For rare classes, intervals may be very wide or undefined; show this transparently. Avoid interpreting overlapping or unstable intervals as proof of equivalence.

The five outer folds are dependent through overlapping training sets. Do not treat the five fold scores as five independent studies or use a naive standard error across folds as the only uncertainty estimate.

### 8.3 Multi-class and rare-class reporting

Use a fixed seven-class label order and publish the class mapping in each experiment record. RAO results must always be accompanied by patient and image support. If a metric is undefined because a class is absent from a particular evaluation subset, report it as undefined with the reason. Do not impute a value.

## 9. Predictive uncertainty and selective prediction

The uncertainty method is not yet selected. Candidate methods may include deep ensembles or Monte Carlo dropout, subject to compute feasibility and a separate prespecified experiment. Distinguish uncertainty proxies from validated epistemic or aleatoric uncertainty.

Evaluate whether uncertainty is associated with errors, including class-wise analyses where support permits. Report risk-coverage curves, retained-case error and coverage. Any abstention threshold must be selected using training/inner-validation data only and then frozen before outer evaluation. Do not choose a threshold to optimise outer-fold performance.

## 10. Explainability evaluation

Explainability methods are not evidence of causal reasoning. For any selected method, record target class, layer or feature attribution settings, preprocessing and random seed. Evaluate stability, perturbation sensitivity, model/parameter randomisation and faithfulness checks. Use localisation metrics only if suitable expert annotations exist. Visually plausible heatmaps alone do not establish validity.

## 11. External validation

The five-fold OCTDL experiment is internal cross-validation on one dataset source. It is not external validation. External validation requires a separate cohort/source, verified rights, patient-level independence, compatible label definitions and a frozen model and protocol before external outcomes are examined. Do not use external evaluation data for tuning or calibration.

## 12. Reproducibility and artefact requirements

For every inner and outer run, record:

- dataset release identifier and source archive SHA-256;
- private split-mapping fingerprint and split-generation method;
- outer and inner fold identifiers, without publishing patient IDs;
- code commit, environment lockfile and dependency versions;
- model architecture, pretrained-weight provenance and checkpoint hash;
- preprocessing and augmentation configuration;
- optimiser, learning-rate schedule, batch size, epochs and stopping rule;
- class weights or sampling configuration;
- random seeds and hardware;
- per-image OOF predictions and probability outputs in access-controlled storage;
- metrics, supports, confidence intervals, calibration and uncertainty outputs;
- exclusions, failures, deviations and limitations.

Do not commit raw OCT images, patient identifiers, row-level patient metadata or the private assignment CSV to the public repository. Do not upload sensitive dataset contents to public CI logs or workflow artefacts.

## 13. Approval gates before training

Training remains blocked until all applicable gates are documented:

1. Dataset source, exact version, licence scope and intended research use are reviewed and approved.
2. The outstanding duplicate/near-duplicate audit and any remaining dataset-quality checks are completed or explicitly risk-accepted.
3. The private patient-to-fold mapping is preserved, hash-verified and access-controlled.
4. The inner-fold generation and split-integrity tests are implemented and pass.
5. Baseline model, input contract, preprocessing and training configuration are frozen in a versioned experiment specification.
6. Metric definitions, model-selection rule, calibration procedure and statistical reporting plan are frozen.
7. Compute budget and checkpoint/artifact storage plan are feasible.

Approval of this protocol does not constitute dataset licence approval or clinical validation.

## 14. Known limitations

- OCTDL is a single-source cohort and cannot establish broad scanner, site or population generalisability.
- RAO has only 11 patients, making class-specific performance estimates highly uncertain.
- One patient has image records with two disease labels; image-level labels must be preserved.
- The five-fold allocation uses a heuristic balancing procedure and is not a globally proven optimum.
- Cross-fitted calibration has a training-size mismatch between calibration logits and the final outer model.
- Image-level metrics can overweight patients with multiple images; patient-cluster confidence intervals and patient-balanced sensitivity analyses are required.
- External validation, clinical utility and prospective evaluation are outside the scope of this internal protocol.

## 15. Current status

**Approved protocol; implementation pending.** The project owner approved the nested patient-grouped evaluation design on 2026-11-18. No model training or performance evaluation is claimed. Dataset governance and audit gates, inner-fold implementation and integrity tests, and the baseline experiment configuration remain outstanding.
