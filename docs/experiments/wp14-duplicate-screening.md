# WP14 — OCTDL V4 Exact and Near-Duplicate Screening

**Status:** Data-specific screening in progress; zero-distance candidate review and computational verification complete; nonzero-distance visual review pack generated and awaiting review.  
**Dataset:** OCTDL Mendeley Data Version 4 (DOI: 10.17632/sncdhf53xc.4).  
**Scope:** Local, read-only audit of the 2,064-image acquired dataset.  
**Last evidence update:** 2026-11-20.

## 1. Purpose

WP14 investigates exact and near-duplicate image content that could undermine patient-independent evaluation when image records are associated with different patient identifiers. Perceptual-hash candidates are screening leads, not proof of duplicate identity or patient identity. The audit preserves original images and metadata and keeps patient-linked artefacts private.

## 2. Candidate inventory

The local candidate-generation stage produced 354 image pairs with dHash Hamming distances from 0 through 6.

| Hamming distance | Candidate pairs |
|---:|---:|
| 0 | 87 |
| 1 | 23 |
| 2 | 15 |
| 3 | 21 |
| 4 | 26 |
| 5 | 51 |
| 6 | 131 |
| **Total** | **354** |

All 354 candidate pairs were computationally examined. Both source images were resolved and processed for all pairs; there were zero processing errors.

## 3. Computational verification

The audit calculated original-file SHA-256 hashes and dimension-aware hashes of fully decoded RGB pixel arrays.

| Result | Count |
|---|---:|
| Byte-identical file pairs | 0 |
| Exact decoded RGB pixel matches, with dimensions equal | 54 |
| Cross-patient exact-pixel pairs | 47 |
| Same-patient exact-pixel pairs | 7 |
| Additional exact-pixel matches at dHash distances 1–6 | 0 |
| Processing errors across 354 pairs | 0 |

No byte-identical file pairs were found. The 54 exact decoded-pixel matches have matching dimensions and RGB pixel content despite differing original file hashes. All 54 occurred among the 87 dHash-zero candidates. The remaining 267 nonzero-distance candidates did not produce exact decoded-pixel matches; this does not clear them as visually distinct.

The computational register and summary are retained in the owner's private Termux audit environment. Patient IDs, filenames, image hashes and row-level records are not published.

## 4. Zero-distance blinded visual review

The 87 dHash-zero candidates were placed in a private blinded review pack comprising 44 contact sheets (two pairs per sheet). The reviewer reported all 87 visible pairs, PAIR-0001 through PAIR-0087, as high-confidence potential duplicates.

The 87 visual dispositions are screening judgements only. They are not independent proof of byte identity, patient identity, provenance or clinical equivalence. The contact-sheet count is 44 because the final sheet contains one pair; there is no PAIR-0088.

## 5. Cross-patient exact-pixel relationships and existing split

Among the 54 exact-pixel pairs, 47 connect different patient identifiers. The initial candidate five-fold patient-grouped assignment was checked against these relationships:

- 39 cross-patient exact-pixel relationships cross the existing fold boundary;
- 8 cross-patient exact-pixel relationships are within the same fold;
- 49 unique patients occur in the cross-patient exact-pixel network;
- these relationships form 22 connected components;
- 19 components span more than one existing fold; and
- the largest component contains three patients.

The affected-patient disease audit found 49 patients across the 22 components: AMD 36, DME 2, ERM 2, NO 4, RVO 2 and VID 3. RAO was not represented in this identified network. One patient's records in the source metadata carry both AMD and DME labels; patient grouping must preserve that multi-label relationship.

**Decision:** The original five-fold outer assignment is quarantined and must not be used for model evaluation. No model has been trained or evaluated using this assignment, so no model-performance contamination is claimed. Patient identifiers must not be merged on the basis of image similarity alone.

## 6. Nonzero-distance visual review — ongoing

A separate blinded review pack was generated for all 231 cross-patient candidates with dHash distances 1–6. The 36 same-patient nonzero-distance candidates were excluded from this particular cross-patient pack; they are not thereby cleared.

| Distance | Cross-patient pairs selected |
|---:|---:|
| 1 | 22 |
| 2 | 14 |
| 3 | 18 |
| 4 | 18 |
| 5 | 38 |
| 6 | 121 |
| **Total** | **231** |

Pack-generation verification:
- 231/231 selected pairs resolved to source images;
- zero image-resolution errors;
- 77 contact sheets generated, with three pairs per sheet;
- pair identifiers are anonymous on the contact sheets;
- patient identifiers and original filenames are excluded from the contact sheets;
- original source images were not modified.

**Visual review status: NOT STARTED / IN PROGRESS.** The pack has been generated, but no visual dispositions for these 231 pairs are yet recorded in this report. Do not infer that they are duplicates or distinct until reviewed.

## 7. Private audit artefacts

All paths below are local to the project owner's Termux environment and must not be copied into the public repository:

- Original candidate list: `neurovision-audit/private/octdl-v4-near-duplicate-candidates.csv`
- Zero-distance private manifest and register: `neurovision-audit/private/dhash-zero-review/`
- All-354 computational register: `neurovision-audit/private/dhash-zero-review/computational/all-candidates/all-354-computational-register.csv`
- Nonzero-distance private manifest and review register: `neurovision-audit/private/dhash-nonzero-review/`
- Three-pair contact sheets: `neurovision-audit/private/dhash-nonzero-review/contact-sheets-3-per-page/`
- Original patient-to-fold mapping and component-level patient-linked evidence remain private.

Only aggregate counts, methodology, decisions and non-identifying limitations are suitable for this public report.

## 8. Methodological limitations

1. The candidate list is a shortlist produced by a perceptual-hash search, not an exhaustive comparison of all possible image pairs.
2. dHash distance is a candidate-ranking signal; it is not a calibrated probability of duplication.
3. Exact decoded RGB equality does not prove that two records came from the same patient or acquisition event.
4. Visual review can be subjective and must retain confidence and inconclusive outcomes.
5. A visually similar scan may reflect common anatomy or acquisition characteristics rather than duplicated content.
6. This audit does not establish cross-dataset duplication absence.
7. Connected-component grouping is a conservative split-protection strategy; it does not establish that linked patient identifiers refer to the same individual.

## 9. Next actions and release gates

1. Complete blinded visual review of all 231 nonzero-distance cross-patient candidates.
2. Preserve `potential_duplicate`, `similar_distinct` and `inconclusive` dispositions with confidence and reviewer notes.
3. Independently investigate ambiguous or high-impact relationships; do not merge patient identities automatically.
4. Combine supported cross-patient duplicate links into connected components, documenting the inclusion rule and evidence strength.
5. Rebuild a separate candidate five-fold assignment with each accepted component indivisible; preserve the quarantined mapping unchanged.
6. Independently verify patient uniqueness, image accounting, component integrity, class distribution and fold balance.
7. Reconcile WP13 inner folds against the revised outer assignment; the existing inner-fold mappings must not be assumed valid for a replacement outer split.
8. Complete exact file-level licence review and named-use approval before any model training.

## 10. Current decision

WP14 implementation and initial data execution have produced reproducible aggregate evidence. The 87 zero-distance candidates have undergone blinded visual review and all 354 candidates have undergone computational file/pixel verification. The 231 cross-patient nonzero-distance visual review pack is generated and awaiting human review. The initial five-fold assignment is quarantined due to cross-fold exact-pixel relationships. **Dataset approval and model training remain blocked.**
