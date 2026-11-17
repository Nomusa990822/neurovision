# Dataset Register

**Status:** Candidate register only. No dataset is recorded as locally acquired or approved for experiments until its source, licence, files and metadata are verified.

| Dataset | Candidate role | Known characteristics to verify | Current status |
|---|---|---|---|
| Kermany OCT2017 | Initial baseline candidate | Common four-class OCT dataset; published train/test organisation and patient-related filename information require direct audit | Candidate |
| OCTDL | Independent evaluation candidate | Seven categories and patient identifiers reported in accompanying metadata; class balance and compatibility require audit | Candidate |
| OCTID | Additional candidate | Previously discussed as a smaller multi-class OCT dataset; original source, archive, label definitions and licence unresolved | Pending verification |

## Required register fields
For each acquired dataset record:
- Official name, publisher/authors and publication.
- Original repository URL and DOI/version.
- Download date, acquisition method and responsible person.
- Licence text/version and permitted uses.
- Archive/file sizes and cryptographic checksums.
- Image count, formats, dimensions and colour/channel properties.
- Label taxonomy and reference-standard method.
- Patient/eye/scan identifiers and their permitted use.
- Scanner, site and acquisition metadata where available.
- Original partitions and their documented meaning.
- Known exclusions, missingness, class imbalance and limitations.
- Local storage location identifier (never a personal path in public docs).
- Audit report and approval status.

## Acquisition gates
1. Locate the original publisher source, not an unverified mirror.
2. Read licence and terms before download or redistribution.
3. Preserve original archive and compute SHA-256.
4. Inventory files and verify image decoding.
5. Reconcile counts and labels with source documentation.
6. Audit patient/eye grouping and duplicate relationships.
7. Approve intended research role and record limitations.

## Dataset status vocabulary
- Candidate: identified but not verified.
- Source verified: original source and terms checked.
- Acquired: files downloaded and checksummed.
- Audited: integrity, metadata and labels inspected.
- Approved for specified use: governance review completed for that use.

## Important
Do not assume a dataset's licence, class counts, patient independence or external-validation suitability from secondary summaries. Verify against the original release and accompanying publication. Never redistribute dataset files unless the licence explicitly permits it.