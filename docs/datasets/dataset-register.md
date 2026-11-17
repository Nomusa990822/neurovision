# Dataset Register

**Status:** Primary-source desk review completed for the three initial candidates. No dataset has been downloaded, locally audited or approved for model training. Dataset suitability remains conditional on acquisition-time verification.

## Candidate comparison

| Dataset | Published scope | Patient metadata / split evidence | Rights and source | Proposed role | Status |
|---|---|---|---|---|---|
| Kermany OCT2017, Mendeley V3 | Four labels: CNV, DME, DRUSEN, NORMAL. The V3 release is described as having independent-patient train/test partitions. The 2022 leakage analysis reports 108,312 training images and 1,000 test images for V3. | Filenames encode randomized patient IDs. The 2022 analysis found no patient-ID overlap for V3, but did find substantial overlap in V2. We must independently parse and audit V3. | Mendeley DOI: https://doi.org/10.17632/rscbjbr9sj.3. Page states CC BY 4.0 and also describes the image repository as for research use only. Resolve this wording/terms before use beyond non-commercial research or redistribution. | Large four-class baseline candidate. | Source identified; conditional candidate |
| OCTDL | 2,064 images from 821 patients, seven labels: AMD, DME, ERM, NO, RAO, RVO, VID. Class counts: 1,231; 147; 155; 332; 22; 101; 76 respectively. | Published filenames encode patient IDs; CSV includes patient_id and eye. This supports group-aware partitions, subject to validating the acquired CSV against files. | Mendeley DOI: https://doi.org/10.17632/sncdhf53xc (latest version should be confirmed at acquisition). Author-associated Zenodo record: https://doi.org/10.5281/zenodo.10839556. Mendeley record states CC BY 4.0; verify exact version and file-level rights. | Patient-grouped experiments and possible cross-dataset evaluation after label harmonisation. | Strong candidate; source and metadata documented |
| OCTID | More than 500 images; commonly reported as 572 images across NO, MH, AMD, CSR and DR. A 2018 preprint and 2020 journal article describe the database. | Patient-level identifiers and a verified official split were not established in this desk review. Do not assume that an image-level partition is patient-independent. | Paper: https://doi.org/10.1016/j.compeleceng.2019.106532. Borealis citation record: https://doi.org/10.5683/SP2/W43PFI is a citation record containing the paper PDF, not by itself proof that all image files are in that record. The record displays CC0 1.0 for its file; rights for each image collection must be checked separately. | Supplementary cross-dataset robustness study only if original image collections and rights can be verified. | Partially verified; image-source and metadata checks open |

## Important Kermany version warning

Do not refer to the commonly circulated 84,484-image OCT2017 package and the Mendeley V3 release as if they were identical. The literature distinguishes multiple releases. A 2022 analysis reported substantial patient-ID overlap in V2, but no patient-ID overlap in V3. The release version, exact archive and checksum must be pinned in every experiment. The V3 patient separation is a published finding, not a substitute for our own audit.

## External evaluation policy

OCTDL and OCTID are not automatically approved as external test sets simply because they are different named datasets. Before external evaluation:
1. Confirm distinct source cohort and no known shared images/patients with training data.
2. Freeze the model and evaluation protocol before examining external test outcomes.
3. Define a clinically defensible common label ontology. Do not equate AMD with drusen or CNV without explicit justification.
4. Report class mapping, excluded categories, prevalence shift, scanner/site differences and sample counts.
5. Keep all patient groups together and report patient-level uncertainty where feasible.

A broad normal-versus-abnormal task may be investigated as a separate prespecified task, but must not be silently substituted for the four-class task.

## Primary references

- Kermany et al. (2018), *Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning*, Cell 172(5), 1122–1131. DOI: https://doi.org/10.1016/j.cell.2018.02.010. Dataset release V3: https://doi.org/10.17632/rscbjbr9sj.3.
- Tampu, Eklund & Haj-Hosseini (2022), *Inflation of test accuracy due to data leakage in deep learning-based classification of OCT images*, Scientific Data 9, 580. DOI: https://doi.org/10.1038/s41597-022-01618-6.
- Kulyabin et al. (2024), *OCTDL: Optical Coherence Tomography Dataset for Image-Based Deep Learning Methods*, Scientific Data 11, 365. DOI: https://doi.org/10.1038/s41597-024-03182-7. Dataset record: https://doi.org/10.17632/sncdhf53xc.
- Gholami et al. (2020), *OCTID: Optical coherence tomography image database*, Computers & Electrical Engineering 81, 106532. DOI: https://doi.org/10.1016/j.compeleceng.2019.106532. Preprint: https://arxiv.org/abs/1812.07056.

## Acquisition gates

1. Locate the exact original release and version.
2. Save licence and terms evidence for the exact image files, not only the paper or metadata record.
3. Record download date, source URL, archive size and SHA-256.
4. Inventory files and verify decoding, dimensions, channels and label folders.
5. Reconcile counts and labels with the publication.
6. Parse patient and eye identifiers; test group overlap and duplicates.
7. Record scanner/site metadata, class imbalance, missingness and known limitations.
8. Approve the dataset for a named purpose only after the audit report is reviewed.

## Dataset status vocabulary

- Candidate: identified but not verified.
- Source verified: original source and applicable terms checked.
- Acquired: files downloaded and checksummed.
- Audited: integrity, metadata, labels and grouping inspected.
- Approved for specified use: governance review completed for that use.

No candidate in this register has reached Acquired, Audited or Approved status.
