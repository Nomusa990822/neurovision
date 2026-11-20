# Dataset Register

**Status:** Primary-source desk review and OCTDL V4 local acquisition/image audit updated 2026-11-18. OCTDL V4 archive integrity, image decoding, dimensions, CSV reconciliation and patient grouping have been verified locally by the project owner. Exact file-level licence review, duplicate/near-duplicate screening and purpose-specific approval remain open.

## Candidate comparison

| Dataset | Published scope | Patient metadata / split evidence | Rights and source | Proposed role | Status |
|---|---|---|---|---|---|
| Kermany OCT2017, Mendeley V3 | Four labels: CNV, DME, DRUSEN, NORMAL. The V3 record describes training and test sets of independent patients. A leakage study reports 108,312 training images and 1,000 test images for V3. | Filenames encode randomized patient IDs. The 2022 analysis found no subject-ID overlap for V3, but found 92% overlap between training and test subject IDs in V2. NeuroVision must independently parse and audit V3. | Exact record: https://doi.org/10.17632/rscbjbr9sj.3. Mendeley displays CC BY 4.0 and also states the image repository is for research use only. Record both statements; resolve applicable terms for the intended use and do not redistribute images without clear rights. | Large four-class baseline candidate, subject to rights and audit gates. | Source/version reviewed; conditional candidate |
| OCTDL, Mendeley V4 | 2,064 images from 821 patients; seven labels: AMD, DME, ERM, NO, RAO, RVO, VID. Published image counts: 1,231; 147; 155; 332; 22; 101; 76 respectively. | Filenames encode patient IDs. The V4 CSV includes file_name, disease, subcategory, condition, patient_id, eye, sex, year, image_width and image_height. Reconcile CSV and filename identifiers against all acquired files. | Exact record: https://doi.org/10.17632/sncdhf53xc.4 (published 18 March 2024). Mendeley states CC BY 4.0. Archive and CSV are separately listed; capture exact downloaded hashes and terms. | Primary patient-grouped research candidate; possible cross-dataset evaluation only after cohort and label compatibility review. | Archive SHA-256, ZIP CRC, 2,064-image inventory/decoding, dimensions, CSV reconciliation and patient grouping verified locally; licence review, duplicate screening and approval pending |
| OCTID | 572 images commonly reported across normal, macular hole, AMD, CSR and DR. Original work: 2018 preprint and 2020 journal article. | Patient-level identifiers and a verified official patient-independent split have not been established from the source records reviewed. Do not assume image-level partitions are patient-independent. | Paper: https://doi.org/10.1016/j.compeleceng.2019.106532. Borealis DOI https://doi.org/10.5683/SP2/W43PFI is a citation record containing the paper PDF, not the OCT image archive. Later literature points to https://dataverse.scholarsportal.info/dataverse/OCTID; verify owner, files and terms before acquisition. | Supplementary robustness/external evaluation only if source, rights, cohort independence and grouping are verified. | Image-source, licence and metadata checks open |

## Source-review findings and caveats

### Kermany OCT2017

The Mendeley V3 record describes four image classes and filenames containing randomized patient identifiers, and says the provided training and testing partitions contain independent patients. It also says the repository is made available for research use only while displaying a CC BY 4.0 licence. This wording must remain visible in the governance record; do not infer unrestricted commercial use or redistribution.

Tampu et al. (2022) report 92% overlap between train and test subject IDs in Kermany V2, while their analysis found no such overlap in V3. They also show that split strategy materially affects measured performance. This reinforces the need to pin V3 and perform our own empirical audit. Do not mix V2 and V3 or treat the frequently circulated 84,484-image package as interchangeable with the V3 release.

### OCTDL

Pin **Version 4**, DOI **10.17632/sncdhf53xc.4**, not a mutable concept DOI or earlier release. The Mendeley V4 page lists a 380 MB ZIP and a 107 KB CSV. The associated 2024 Scientific Data paper reports 2,064 images from 821 patients and describes patient identifiers in filenames and CSV metadata. The cohort was collected in Yekaterinburg, Russia. Its class imbalance is substantial: RAO has 22 images from 11 patients, while AMD has 1,231 images from 421 patients. Patient-level counts and class counts must both be reported. A random image split would be unacceptable.

The project owner stored the original `OCTDL.zip` and `OCTDL_labels.csv` in the private `neurovision-datasets` repository. The archive size (398,564,236 bytes), SHA-256, local LFS integrity, ZIP CRC, 2,064-image inventory, image decoding, dimensions and CSV-to-image reconciliation were verified in Termux. The CSV hash is not recorded in the current evidence. The audit found 820 unique patients, including one patient represented in both AMD and DME. WP14 examined all 354 perceptual-hash candidate pairs: 54 were dimension-aware exact decoded-pixel matches (47 cross-patient, 7 same-patient), with no byte-identical pairs and no processing errors. The 87 dHash-zero candidates received blinded visual review. Forty-seven cross-patient exact-pixel relationships form 22 components involving 49 patients; 39 relationships cross folds in the initial outer mapping, which is now quarantined. A separate 231-pair cross-patient nonzero-distance visual-review pack is generated and awaiting review. WP13 inner folds were generated and independently verified for the original mapping, but must be regenerated if a replacement outer mapping is adopted. Licence interpretation and named-use approval remain outstanding. See [OCTDL V4 acquisition record](acquisition-record-octdl-v4.md) and [WP14 duplicate-screening report](../experiments/wp14-duplicate-screening.md).

### OCTID

The Borealis citation record is not the image dataset itself. A later paper points to a Dataverse OCTID collection, but the actual file inventory, data owner, access terms, patient metadata and version have not yet been verified. Do not download a similarly named Kaggle or third-party mirror as a substitute without tracing it to the original source.

## External evaluation policy

OCTDL and OCTID are not automatically approved as external test sets simply because they are different named datasets. Before external evaluation:

1. Confirm distinct source cohort and no known shared images/patients with training data.
2. Freeze the model and evaluation protocol before examining external test outcomes.
3. Define a clinically defensible common label ontology. Do not equate AMD with drusen or CNV without explicit justification.
4. Report class mapping, excluded categories, prevalence shift, scanner/site differences and sample counts.
5. Keep all patient groups together and report patient-level uncertainty where feasible.

A broad normal-versus-abnormal task may be investigated as a separate prespecified task, but must not be silently substituted for the four-class task.

## Primary references

- Kermany et al. (2018), *Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning*, Cell 172(5), 1122–1131. DOI: https://doi.org/10.1016/j.cell.2018.02.010.
- Kermany OCT2017 Mendeley V3: https://doi.org/10.17632/rscbjbr9sj.3.
- Tampu, Eklund & Haj-Hajji (2022), *Inflation of test accuracy due to data leakage in deep learning-based classification of OCT images*, Scientific Data 9, 580. DOI: https://doi.org/10.1038/s41597-022-01618-6.
- Kulyabin et al. (2024), *OCTDL: Optical Coherence Tomography Dataset for Image-Based Deep Learning Methods*, Scientific Data 11, 365. DOI: https://doi.org/10.1038/s41597-024-03182-7.
- OCTDL Mendeley V4: https://doi.org/10.17632/sncdhf53xc.4.
- Gholami et al. (2020), *OCTID: Optical coherence tomography image database*, Computers & Electrical Engineering 81, 106532. DOI: https://doi.org/10.1016/j.compeleceng.2019.106532.
- OCTID Dataverse collection reference (not yet verified for file content/terms): https://dataverse.scholarsportal.info/dataverse/OCTID.

## Acquisition gates

1. Locate the exact original release and version.
2. Save licence and terms evidence for the exact image files, not only the paper or metadata record.
3. Record download date, source URL, archive size and SHA-256.
4. Inventory files and verify decoding, dimensions, formats and label folders.
5. Reconcile counts and labels with the publication.
6. Parse patient and eye identifiers; test group overlap and duplicates.
7. Record scanner/site metadata, class imbalance, missingness and known limitations.
8. Approve the dataset for a named purpose only after the audit report is reviewed.

## Dataset status vocabulary

- Candidate: identified but not verified.
- Source/version reviewed: exact source record and published metadata inspected; licence interpretation or empirical checks may remain open.
- Owner-reported acquired: project owner reports obtaining files; bytes and hashes have not been independently checked.
- Acquired: exact files accessible to the audit environment and archive/metadata hashes recorded.
- Audited: integrity, metadata, labels and grouping inspected.
- Approved for specified use: governance review completed for that use.

OCTDL V4 has passed the recorded file-integrity, image-decoding and metadata-reconciliation audit, but it is not yet approved for model development, external evaluation or redistribution. Other candidate datasets remain conditional.
