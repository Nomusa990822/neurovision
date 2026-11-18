# ADR-022: Nested Patient-Grouped Cross-Validation for OCTDL V4

- **Status:** Proposed; approval required before model training
- **Date:** 2026-11-18
- **Decision owners:** NeuroVision research project

## Context

The OCTDL V4 audit identified 2,064 image records and 820 unique patient identifiers. All image records from a patient must remain in one partition. One patient has image records associated with both AMD and DME, so disease-specific patient counts sum to 821 while the unique patient count is 820. RAO is represented by only 11 patients.

A deterministic five-fold patient-grouped allocation was generated using a randomised greedy multistart procedure with 1,000 candidate allocations and base seed 20261117. Its patient-to-fold mapping was independently reconciled against the source CSV. The mapping fingerprint is:

`328ba1d5809cb7cf9bd5fc43405e30ef46c3bf503a39d0387212ae1e9c8487ff`

The mapping contains patient identifiers and must remain in access-controlled private storage.

## Decision proposed

Adopt five-fold patient-grouped outer cross-validation for internal evaluation, with four-fold patient-grouped inner cross-validation inside each outer-training pool for model selection.

For each outer iteration, hold one fold untouched, perform all model selection using only the other four folds, refit the selected configuration on that outer-training pool, and evaluate once on the held-out fold. Combine the five outer predictions into an out-of-fold evaluation set.

Use image-level labels and metrics because labels belong to image records. Do not collapse the multi-label patient's records into one patient diagnosis. Account for within-patient correlation using patient-cluster bootstrap confidence intervals and report patient-balanced sensitivity analyses where feasible.

The proposed primary model-selection criterion is pooled inner out-of-fold image-level macro-F1 across seven classes. Report class-wise metrics and supports, with particular caution for RAO. The initial calibration proposal is scalar temperature scaling fitted on inner out-of-fold logits only. Outer evaluation labels must not be used for model selection, calibration or threshold setting.

The full procedure and reporting requirements are specified in [WP13 — Patient-Grouped Cross-Validation and Model-Selection Protocol](../../experiments/wp13-cross-validation-and-model-selection.md).

## Alternatives considered

1. **Random image-level train/test split:** rejected because images from the same patient could appear in both partitions, inflating apparent generalisation.
2. **Single fixed patient-level holdout:** possible, but with only 11 RAO patients the test estimate would be highly sensitive to the allocation and would use a small number of patients for final internal evaluation.
3. **Five-fold patient-grouped CV without nested selection:** not sufficient if hyperparameters are tuned using the same folds whose scores are reported as final evaluation.
4. **Nested patient-grouped CV:** proposed because it separates inner model selection from outer evaluation while using the limited cohort more efficiently.

## Consequences and limitations

- The five outer folds are not independent studies because their training sets overlap.
- RAO class-specific estimates will be highly uncertain; inner-fold RAO metrics are exploratory.
- Four-fold inner validation must pass a feasibility and integrity check before training.
- The greedy allocation is a reproducible heuristic, not a globally proven optimum.
- Image-level metrics can overweight patients with more scans; clustered confidence intervals and patient-balanced sensitivity analyses are required.
- Cross-fitted calibration has a training-size mismatch between inner OOF models and the final outer model; this limitation must be reported.
- This internal CV design does not constitute external validation or clinical validation.

## Approval conditions

This ADR remains proposed until dataset licence and intended-use review, outstanding duplicate/near-duplicate checks, inner-fold integrity tests, baseline configuration, metrics and statistical reporting are approved. No model training is authorised by this ADR alone.
