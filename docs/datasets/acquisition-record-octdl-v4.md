# OCTDL Version 4 — Acquisition Record

**Record status:** Acquisition reported by project owner; not independently verified  
**Dataset status:** Candidate; not approved for model development or external evaluation  
**Work package:** WP11 — acquisition and immutable provenance  
**Record date:** 2026-11-17

## 1. Source identity

| Field | Recorded value |
|---|---|
| Dataset | OCTDL — Optical Coherence Tomography Dataset for Image-Based Deep Learning Methods |
| Release | Mendeley Data Version 4 |
| Persistent identifier | DOI: `10.17632/sncdhf53xc.4` |
| Official source | https://data.mendeley.com/datasets/sncdhf53xc/4 |
| Publisher-listed licence | CC BY 4.0; verify scope against the exact archive and metadata files before approval |
| Published release date | 2024-03-18 |
| Expected image records | 2,064, as described by the source record/publication |

## 2. Owner-reported acquisition and storage

The project owner reported downloading the Version 4 archive and CSV and placing them in Google Drive using this intended layout:

```text
Neurovision/
  dataset/
    OCTDL_V4/
      original/
        OCTDL.zip
      metadata/
        OCTDL_labels.csv
      provenance/
      audit-reports/
```

Reported filenames:
- `OCTDL.zip`
- `OCTDL_labels.csv`

This is a record of the owner's report, not an independent verification of the Drive contents. The Google Drive connector is unavailable in this workspace, and the files from the earlier conversation are not currently exposed to the project file tools.

## 3. Verification status

| Check | Status | Evidence / next action |
|---|---|---|
| Exact source and version identified | Documented | Version-specific Mendeley V4 DOI above |
| Owner reports archive downloaded | Reported, unverified | Re-access original archive |
| Owner reports CSV downloaded | Reported, unverified | Re-access original CSV |
| Drive location | Reported | Confirmed folder layout in project conversation; no direct Drive inspection |
| Archive byte size | Not verified | Read filesystem metadata |
| Archive SHA-256 | Not computed | Hash original ZIP before extraction |
| ZIP central directory / CRC | Not verified | Inspect archive and run CRC validation |
| CSV SHA-256 | Not computed | Hash original CSV |
| CSV schema and row counts | Preliminary only | Re-run against the exact acquired CSV |
| Extracted image inventory | Not performed | Inspect and safely extract archive |
| Image decoding and dimensions | Not performed | Run image-level audit |
| CSV-to-image reconciliation | Not performed | Compare normalized filenames and labels |
| Patient/eye grouping | Not approved | Reconcile CSV patient IDs, filenames and eye fields |
| Licence scope for exact files | Needs final review | Preserve source terms evidence and assess file-level scope |
| Dataset approval | Not approved | Complete WP12/WP13 and record purpose-specific decision |

No archive hash, file count, CRC result, image count, or successful image-decoding result is asserted by this record.

## 4. Immutable acquisition checklist

When the exact original files are accessible to the audit environment:

1. Preserve both originals unchanged; do not rename, recompress, edit or extract over them.
2. Record exact filenames, byte sizes and SHA-256 hashes.
3. Save a dated copy or capture of the exact Mendeley V4 source page and applicable licence/terms.
4. Inspect archive member paths and sizes before extraction.
5. Validate ZIP CRC/integrity and safely extract to a new, empty interim directory.
6. Inventory every extracted file and hash each file.
7. Decode every image and record format, dimensions, channels and failures.
8. Reconcile image filenames and labels against the CSV and published counts.
9. Reconcile patient identifiers encoded in filenames against `patient_id`; inspect `eye`, repeated scans and cross-label patient IDs.
10. Produce a private audit report and request WP13 review before approving any use.

## 5. Research and governance constraints

- Raw OCT images and patient-linked metadata must remain outside Git and public CI artifacts.
- The project software's Apache-2.0 licence does not apply to OCTDL images or metadata.
- The publisher-listed CC BY 4.0 statement must be interpreted for the actual files and intended use; do not infer redistribution rights beyond the terms.
- Patient identifiers are grouping metadata, not proof that the data are fully anonymised.
- No patient-aware split is approved until the empirical audit is complete.
- No model training is authorised at this stage.

## 6. Status decision

**WP11 remains in progress.** The owner-reported acquisition is a useful project milestone, but independent file access, checksums, archive integrity, image inventory and metadata reconciliation remain outstanding. The dataset remains a candidate and is not approved for training, external evaluation or redistribution.
