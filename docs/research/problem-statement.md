# Research Problem Statement

## Background
Optical Coherence Tomography (OCT) produces cross-sectional images of retinal structures and is an important imaging modality in ophthalmic practice. Deep-learning methods can learn image representations useful for classifying retinal conditions, but predictive performance alone is insufficient to establish reliability.

## Problem
A model may produce a class prediction without a meaningful account of the image evidence influencing it, may be overconfident on ambiguous or unfamiliar inputs, and may output probabilities that are poorly calibrated. Performance can also deteriorate under changes in dataset, scanner, acquisition protocol or patient population. Inadequate data partitioning can introduce patient-level leakage and inflate evaluation results. Incomplete provenance and experiment records further weaken reproducibility.

## Main research question
How can an explainable and uncertainty-aware deep-learning system be developed and rigorously evaluated to improve the interpretability and reliability of retinal disease classification from OCT images?

## Secondary questions
1. How effectively do selected architectures classify OCT images under patient-aware evaluation?
2. How do explanation methods differ in localisation, stability and sensitivity to model behaviour?
3. Can predictive uncertainty identify cases in which the model is more likely to be incorrect?
4. How accurately do predicted probabilities reflect observed correctness?
5. How does performance change on independent datasets or acquisition domains?
6. How do image quality, class imbalance and distribution shift affect reliability?
7. How can these capabilities be integrated into a reproducible research application?

## Research hypotheses
- H1: Appropriate uncertainty methods can support identification of higher-risk predictions and useful selective prediction.
- H2: Post-hoc calibration can improve probability reliability on data representative of the calibration setting.
- H3: Explanation methods differ in stability and faithfulness; visual plausibility alone is insufficient.
- H4: Independent external evaluation may reveal generalisation gaps not apparent in internal testing.
- H5: A combined classification, explanation and uncertainty interface communicates model behaviour more completely than a class label alone.

These hypotheses are to be tested, not treated as established findings.

## Research boundary
The system is a research decision-support prototype. It is not a diagnostic device, does not replace ophthalmic expertise and must not be used to make patient-care decisions. Claims must be limited to the datasets, labels, reference standards and evaluation designs actually studied.