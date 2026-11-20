# Dataset Acquisition and Audit Protocol

**Phase:** 3 — Dataset Acquisition and Governance Audit  
**Status:** Protocol defined; OCTDL V4 archive/image and WP13 inner-fold audits recorded; WP14 duplicate review ongoing and governance gates remain open  
**Applies to:** OCT image datasets and all derived manifests

## 1. Purpose and entry criteria

This protocol governs source selection, acquisition, integrity checks, metadata reconciliation, patient grouping, duplicate detection and purpose-specific approval. It is designed to prevent data leakage, undocumented dataset changes and licence assumptions.

The project must not begin model training until:
- the exact source and immutable release/version are identified;
- the applicable licence and terms for the image files are recorded;
- archive hashes and file inventories are recorded;
- image files and labels pass integrity checks;
- patient/eye identifiers are reconciled and grouping feasibility is documented;
- duplicate and near-duplicate checks are completed to the extent feasible;
- exclusions and limitations are recorded; and
- a named-use approval is documented.

## 2. Acquisition principles

1. Prefer the original publisher/author repository or its explicitly linked archival record.
2. Pin a version-specific DOI or release identifier. A concept name or mutable “latest” URL is insufficient.
3. Capture a dated copy or export of the source metadata, licence and terms at acquisition.
4. Do not bypass registration, access controls or usage restrictions.
5. Do not commit raw archives, images, patient identifiers or restricted metadata to Git.
6. Do not upload OCT data to GitHub Actions artifacts, logs or public storage.
7. Keep the original archive immutable. Perform extraction and processing into separate data zones.
8. Never infer that a paper's open-access licence grants the same rights to its dataset images.

## 3. Required acquisition manifest

Create one manifest record per acquired dataset release. Required fields:

| Field | Meaning |
|---|---|
| dataset_id | Stable project identifier, e.g. octdl_v4 |
| dataset_title | Publisher's dataset title |
| publisher_or_depositor | Named source owner/depositor |
| source_url | Exact release landing page |
| persistent_identifier | Version-specific DOI or archive identifier |
| version | Explicit release version |
| publication_or_release_date | Source publication date, if provided |
| acquired_at_utc | UTC timestamp of acquisition |
| acquisition_method | Browser/manual/API/author-provided; no credential values |
| terms_url | Exact terms/licence page |
| licence_name | Exact stated licence, or not stated |
| licence_scope_notes | Ambiguities, research-only language, file-level caveats |
| archive_filename | Original archive filename |
| archive_bytes | Exact archive size in bytes |
| archive_sha256 | SHA-256 of original archive |
| extracted_file_count | Count after safe extraction |
| expected_file_count | Published expected count, if available |
| metadata_files | CSV/JSON/readme files and hashes |
| patient_id_available | Boolean/unknown |
| eye_id_available | Boolean/unknown |
| scanner_site_metadata | Available scanner/site fields or not reported |
| acquisition_status | candidate/source_verified/acquired/audited/approved |
| intended_use | Explicit approved or proposed use |
| limitations | Known caveats and unresolved questions |

Do not store direct identifiers. If a source provides pseudonymous patient IDs, restrict their use to the private local manifest and use non-reversible project grouping keys in shareable outputs where needed.

## 4. Safe archive handling

- Store original downloads in a read-only raw zone outside the repository.
- Calculate SHA-256 before extraction.
- Inspect archive paths before extraction; reject absolute paths, parent traversal and unexpected symbolic links.
- Extract into a fresh interim directory.
- Record archive and extracted-file counts, total bytes and file extensions.
- Hash extracted files where practical; preserve the original archive hash as the primary acquisition identity.
- Never overwrite an existing raw archive. A changed release receives a new dataset/version identifier and manifest.

Suggested local data layout (not committed):

    NEUROVISION_DATA_ROOT/
      raw/<dataset_id>/<archive>
      interim/<dataset_id>/
      manifests/<dataset_id>/
      reports/<dataset_id>/
      processed/<dataset_id>/

## 5. File and image integrity audit

For every image:
- validate file signature and successful decoding;
- record dimensions, channel count, bit depth where available, and format;
- detect empty, corrupt, truncated and unsupported files;
- record exact file hashes;
- identify exact duplicate hashes;
- assess near-duplicates with a documented perceptual method and manually review flagged groups;
- inspect unexpected borders, overlays, text, laterality markers, compression artifacts and inconsistent image geometry;
- never silently convert or resize during the audit.

The audit report must include expected versus observed counts, corrupt-file counts, image dimension/channel distributions, duplicate groups, exclusions and reasons.

## 6. Label and metadata reconciliation

- Reconcile each image path to exactly one metadata record and one target label.
- Check missing, duplicate and orphan metadata rows.
- Compare observed class counts with the publication and explain every discrepancy.
- Preserve original labels and add a separate normalized-label field; never overwrite source labels.
- Record whether labels represent disease, finding, scan-level diagnosis or another unit.
- Do not collapse clinically distinct classes to simplify training without a prespecified rationale.
- Report image-level and patient-level class counts.

## 7. Patient grouping and leakage audit

- Parse patient IDs using the dataset's documented filename/metadata convention, not a guessed regular expression.
- Reconcile patient IDs between filenames and CSV metadata.
- Verify that all scans from a patient remain in one partition.
- Inspect eye and visit relationships when available; both eyes and repeated visits from one patient remain grouped.
- Report patient-ID overlap across any publisher-provided train/validation/test partitions.
- Detect exact duplicate images across partitions and across candidate datasets.
- Use similarity search for near-duplicate screening; treat it as a flagging tool, not proof of patient identity.
- If reliable patient IDs are absent, explicitly state that patient-independent evaluation cannot be guaranteed. Do not claim patient-level separation.
- Store the split manifest with a versioned seed and deterministic algorithm only after the dataset audit is approved.

## 8. Dataset-specific checks

### Kermany OCT2017

- Pin Mendeley V3 (DOI 10.17632/rscbjbr9sj.3) explicitly; do not mix V2 and V3.
- V3's source page describes randomized patient IDs in filenames and independent-patient train/test partitions.
- The source page also says the images are for research use only while displaying CC BY 4.0. Record this ambiguity and restrict use to the verified permitted purpose; do not redistribute images unless the applicable rights are clarified.
- Independently parse IDs and test overlap. Published split descriptions do not replace our audit.

### OCTDL

- Pin Mendeley Version 4 (DOI 10.17632/sncdhf53xc.4).
- Reconcile the 2,064 image records against the archive and the CSV columns file_name, disease, patient_id, eye, and other available fields.
- Reconcile filename-encoded patient IDs against CSV patient IDs.
- Report image and patient counts by class, and assess rare classes before defining any task.
- The published cohort is from Yekaterinburg, Russia; do not claim broad geographic or device generalisability from this cohort alone.
- Track owner-reported acquisition separately from independently verified archive access, hashes and integrity results. See the OCTDL V4 acquisition record.

### OCTID

- The Borealis DOI 10.5683/SP2/W43PFI is a citation record containing a paper PDF, not evidence that the image archive is present there.
- A separate Dataverse OCTID collection is referenced in later literature. Verify its owner, files, terms and metadata before acquisition.
- Do not assume patient identifiers or an independent test split are available.

## 9. Dataset approval record

Approval is purpose-specific and must state:
- exact dataset release and archive SHA-256;
- approved purpose (training, development, calibration, internal test, external test, or descriptive analysis);
- licence/terms determination and restrictions;
- audit report location and date;
- patient grouping confidence and unresolved leakage risks;
- class mapping and exclusions;
- approver and decision date.

A dataset approved for model development is not automatically approved for external validation or redistribution.

## 10. Duplicate-screening interpretation and split quarantine

Perceptual-hash distances are candidate-generation signals, not proof of duplicate identity. Computational verification must distinguish original-file byte identity from decoded-pixel identity and must compare dimensions as well as decoded pixel hashes. A visually reviewed pair must retain its disposition, confidence and reviewer notes; inconclusive cases remain unresolved.

For OCTDL V4, all 354 shortlisted pairs were computationally examined. Fifty-four pairs had equal dimensions and identical decoded RGB pixel arrays (47 cross-patient and 7 same-patient); no original files were byte-identical. All 54 exact-pixel matches occurred at dHash distance zero. The 87 zero-distance candidates received blinded visual review. A further 231 cross-patient candidates at distances 1–6 have a three-pair-per-sheet review pack; visual review remains ongoing.

The 47 cross-patient exact-pixel relationships form 22 connected components involving 49 patients. Because 39 of those relationships cross folds in the initial candidate outer assignment, that mapping is quarantined and must not be used for model evaluation. Do not merge patient identifiers based only on image similarity. Any replacement split must assign accepted duplicate-linked components as indivisible groups, retain the original patient identities, be independently verified, and trigger regeneration/re-verification of the WP13 inner folds.

## 11. Current project state

As of 2026-11-18:
- The original OCTDL V4 ZIP and CSV are stored in the private neurovision-datasets repository, outside the public code repository.
- The archive size (398,564,236 bytes), SHA-256, local Git LFS integrity, ZIP CRC, 2,064-image extraction/inventory, full image decoding, image dimensions and CSV-to-image reconciliation have been verified locally by the project owner.
- The CSV contains 2,064 image rows and 820 unique patient IDs. One patient has records in both AMD and DME; both records remain in the same patient group.
- A deterministic five-fold patient-grouped outer assignment was independently re-read and verified locally. The patient mapping remains private.
- The WP13 nested inner-fold mapping contains 3,280 assignments across 820 patients and five outer iterations. Independent re-read verification passed; the mapping remains private.
- WP14 data-specific computational screening is complete for the 354-pair candidate shortlist; the 87 zero-distance candidates received blinded visual review. The 231-pair cross-patient nonzero-distance visual review is ongoing. The initial outer mapping is quarantined due to cross-fold exact-pixel relationships.
- Exact file-level licence scope, purpose-specific dataset approval and CSV SHA-256 recording remain open.
- No model training is authorised.

See the OCTDL V4 acquisition record and WP14 duplicate-screening protocol for the evidence ledger and outstanding checks.

## 12. Primary references

- Kermany et al. (2018), Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning, Cell. https://doi.org/10.1016/j.cell.2018.02.010
- Kermany OCT2017 Mendeley Version 3. https://doi.org/10.17632/rscbjbr9sj.3
- Tampu et al. (2022), Inflation of test accuracy due to data leakage in deep learning-based classification of OCT images, Scientific Data. https://doi.org/10.1038/s41597-022-01618-6
- Kulyabin et al. (2024), OCTDL: Optical Coherence Tomography Dataset for Image-Based Deep Learning Methods, Scientific Data. https://doi.org/10.1038/s41597-024-03182-7
- OCTDL Mendeley Data Version 4. https://doi.org/10.17632/sncdhf53xc.4
- Gholami et al., OCTID: Optical Coherence Tomography Image Database. https://doi.org/10.1016/j.compeleceng.2019.106532
- OCTID collection reference (availability must be verified). https://dataverse.scholarsportal.info/dataverse/OCTID
