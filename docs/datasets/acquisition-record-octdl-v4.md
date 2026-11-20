# OCTDL Version 4 — Acquisition Record

**Record status:** Archive and image audit independently verified in the project owner's local Termux environment; licence scope and named-use approval remain open  
**Dataset status:** Audited for file integrity and metadata consistency; not approved for model development or external evaluation  
**Work package:** WP11 — acquisition and immutable provenance  
**Record date:** 2026-11-20

## 1. Source identity

| Field | Recorded value |
|---|---|
| Dataset | OCTDL — Optical Coherence Tomography Dataset for Image-Based Deep Learning Methods |
| Release | Mendeley Data Version 4 |
| Persistent identifier | DOI: `10.17632/sncdhf53xc.4` |
| Official source | https://data.mendeley.com/datasets/sncdhf53xc/4 |
| Publisher-listed licence | CC BY 4.0; exact file-level scope and intended-use interpretation still require review |
| Published release date | 2024-03-18 |
| Expected image records | 2,064 |

## 2. Acquisition and immutable source evidence

The project owner acquired the Version 4 archive and CSV and stored the originals in the private `neurovision-datasets` GitHub repository, outside the public code repository.

| Artefact | Evidence |
|---|---|
| Original archive | `OCTDL_V4/original/OCTDL.zip` in the private dataset repository |
| Archive size | 398,564,236 bytes |
| Archive SHA-256 | `637a72ff3319645aac30408d4d838189337ac0b8b0f9faabf7c8156d271f46f7` |
| CSV | `OCTDL_V4/metadata/OCTDL_labels.csv` in the private dataset repository |
| CSV SHA-256 | Not recorded in the evidence currently available; must be added if the original CSV is re-hashed |
| LFS verification | Local SHA-256 matched the Git LFS pointer OID; `git lfs fsck` completed without missing or corrupt objects |

The archive hash match and LFS integrity check were performed by the project owner in the local Termux environment. This is recorded as owner-executed verification; it is not a claim that the assistant independently downloaded the private LFS binary.

## 3. Archive and image audit results

| Check | Result | Evidence |
|---|---|---|
| ZIP structure and CRC | Passed | 2,072 archive members including directory entries; CRC validation passed |
| Extracted image inventory | 2,064 images | Safe extraction completed into a separate local audit directory |
| Image decoding | 2,064 passed; 0 failures | Every image fully decoded using Pillow |
| Actual image formats | 1,689 JPEG; 375 PNG | Determined from image content; some PNG files use a `.jpg` filename extension |
| Image modes | 1,797 RGB; 267 RGBA | All 267 RGBA images had fully opaque alpha values |
| Image dimensions | Matched CSV metadata | All 2,064 image dimensions matched the corresponding CSV metadata |
| CSV records | 2,064 rows | Source CSV inspected locally |
| Filename reconciliation | 2,064/2,064 matched | CSV filename stems matched archive image stems after documented normalization |
| Patient identifiers | 820 unique patient IDs | No missing patient IDs |
| Patient-level split integrity | Passed for the candidate outer assignment | 820 patients assigned exactly once across five folds; no patient appears in more than one fold |

The ZIP archive contains 2,072 members, including directories. The 2,064 image files were extracted and decoded successfully. The original archive and source CSV remain preserved; image format detection must use file content rather than filename extension. Any RGB conversion or other preprocessing must be performed only in a separately versioned derived-data stage.

## 4. Metadata and cohort findings

The CSV contains 2,064 image-level records and the source columns `file_name`, `disease`, `subcategory`, `condition`, `patient_id`, `eye`, `sex`, `year`, `image_width` and the publisher's misspelled `image_hight`. Preserve the source column name in raw records; a normalized alias may be added separately.

Primary image-level disease counts:

| Disease label | Images | Patients |
|---|---:|---:|
| AMD | 1,231 | 421 |
| DME | 147 | 107 |
| ERM | 155 | 71 |
| NO | 332 | 110 |
| RAO | 22 | 11 |
| RVO | 101 | 50 |
| VID | 76 | 51 |
| **Total** | **2,064** | **820 unique patients** |

Disease-specific patient counts sum to 821 because one patient has image records in both AMD and DME. This is a multi-label patient grouping fact, not a reason to discard either image-level record. There are 32 patients with both OD and OS records; both eyes must remain in the same data partition.

Additional data-quality observations:
- One VID patient has conflicting F/M sex values; one AMD patient has conflicting year values (1954/1969). These fields must not be silently corrected or used as model inputs.
- 1,616 rows have eye, sex and year all coded as zero. The publisher's precise missing-value convention remains unconfirmed.
- The meaning of the `year` field remains unconfirmed.
- `disease` is the proposed primary seven-class image-level target. `subcategory` and `condition` remain auxiliary source annotations unless a separate protocol justifies their use.
- RAO has only 11 patients; class-specific performance estimates will be highly uncertain.

## 5. Candidate five-fold patient-grouped outer assignment

A deterministic greedy multistart candidate assignment was generated with seed `20261117` and 1,000 candidates. It includes all 820 patients and all 2,064 image records, with each patient assigned to exactly one of five folds. Patient counts are 163, 166, 164, 163 and 164; image counts are 411, 412, 412, 413 and 416.

The private patient-to-fold mapping is stored locally with restricted permissions and is not committed to the public code repository. Its SHA-256 fingerprint is:

`328ba1d5809cb7cf9bd5fc43405e30ef46c3bf503a39d0387212ae1e9c8487ff`

An independent verification re-read the source CSV and private mapping and confirmed:
- all 820 source patients were assigned exactly once;
- all 2,064 image records were accounted for;
- no patient crossed folds;
- all five folds were non-empty; and
- the mapping fingerprint matched.

This is a candidate outer assignment, not a completed training split or evidence of model performance. The mapping itself must remain private. WP13 inner-fold assignments were generated and independently re-read locally: 3,280 assignments across 820 patients and five outer iterations. The inner-fold mapping fingerprint is recorded in the project audit evidence. These assignments correspond to the original outer mapping and must be regenerated if a replacement outer mapping is adopted.

## 6. Duplicate and near-duplicate audit (WP14)

The project owner executed the data-specific WP14 audit locally in Termux. The original 354-pair perceptual-hash candidate shortlist was fully examined, with zero processing errors.

| Check | Result |
|---|---:|
| Original candidate pairs | 354 |
| Byte-identical original file pairs | 0 |
| Dimension-aware exact decoded-RGB pixel pairs | 54 |
| Cross-patient exact-pixel pairs | 47 |
| Same-patient exact-pixel pairs | 7 |
| Exact-pixel matches at dHash distances 1–6 | 0 |
| Computational processing errors | 0 |

The 54 exact-pixel pairs have equal dimensions and equal decoded RGB pixel content, despite differing original file hashes. All 54 were among the 87 candidates with dHash distance zero.

The 87 zero-distance candidates received blinded visual review across 44 contact sheets. The reviewer recorded all 87 as high-confidence potential duplicates. This is a visual screening disposition, not proof of shared patient identity or provenance.

The 47 cross-patient exact-pixel relationships form 22 connected components involving 49 patients. Nineteen components span more than one fold in the original candidate outer assignment. The component-linked patient disease audit found AMD 36, DME 2, ERM 2, NO 4, RVO 2 and VID 3; RAO was not represented in this identified network.

**Split decision:** The original outer mapping is quarantined and must not be used for model evaluation. Thirty-nine cross-patient exact-pixel relationships cross its fold boundaries. No model has been trained or evaluated using this mapping; therefore no model-performance contamination is claimed. Patient identifiers are not merged based on image similarity alone.

A second blinded review pack was generated for 231 cross-patient candidates with dHash distances 1–6. The pack contains 77 contact sheets with three pairs per sheet, all 231 source-image pairs resolved and zero image-resolution errors. Visual review is **ongoing**; no dispositions are yet claimed. The 36 same-patient nonzero-distance candidates were excluded from this cross-patient pack and are not thereby cleared.

Detailed patient-linked manifests, filenames, image hashes, component registers and fold mappings remain in the private local audit environment. Public documentation contains aggregate evidence only. See [WP14 duplicate-screening report](../experiments/wp14-duplicate-screening.md).

## 7. Remaining verification and governance gates

| Check | Status | Next action |
|---|---|---|
| Original archive size and SHA-256 | Verified | Preserve immutable source evidence |
| ZIP CRC and safe extraction | Passed | Preserve audit report |
| Full image decoding and dimensions | Passed | Preserve audit report |
| CSV-to-image reconciliation | Passed | Preserve aggregate report |
| Initial patient grouping and outer assignment | Initially verified, now quarantined | Replace after WP14 component review; do not use for evaluation |
| dHash-zero computational and visual screening | Complete for 87 candidates | Retain findings; do not infer identity |
| Nonzero-distance cross-patient visual screening | Ongoing | Review all 231 pairs in the blinded pack |
| Duplicate-aware replacement split | Not generated | Build only after review and component adjudication |
| CSV SHA-256 | Not recorded in current evidence | Re-hash original CSV and add to private manifest |
| Exact file-level licence scope | Open | Review publisher terms and intended use |
| Purpose-specific dataset approval | Not approved | Record a named-use decision after remaining gates |
| Model training | Not authorised | Do not train until all required gates are approved |

## 8. Research and governance constraints

- Raw OCT images and patient-linked metadata remain outside the public code repository and public CI artifacts.
- The private dataset repository is access-controlled; the patient-to-fold mapping and detailed patient-linked reports remain local and private unless a separate access-controlled preservation decision is approved.
- The project software's Apache-2.0 licence does not apply to OCTDL images or metadata.
- The publisher-listed CC BY 4.0 statement must be interpreted for the actual files and intended use; do not infer redistribution rights beyond the terms.
- Patient identifiers are grouping metadata, not proof that the data are fully anonymised.
- No model training is authorised at this stage.
- This is a research dataset audit, not a clinical validation.

## 9. Status decision

**WP11 acquisition and core file-integrity audit evidence are recorded.** The archive hash, ZIP integrity, image inventory, decoding, dimensions, CSV reconciliation and candidate outer patient-grouped assignment have been verified locally by the project owner. Exact file-level licence review, completion of nonzero-distance visual review, duplicate-aware replacement split and corresponding inner-fold regeneration, CSV hash recording and purpose-specific dataset approval remain outstanding. The dataset is not yet approved for model development, external evaluation or redistribution.
