# ADR-019: Local-First DVC and Dataset Storage

- Status: Accepted
- Date: 2026-11-17
- Decision owner: Project owner

## Context
Dataset acquisition is incomplete. A remote storage provider, budget, access-control model and retention requirements have not yet been selected.

## Decision
1. Keep raw OCT archives outside Git and preserve them as immutable local source data.
2. Track code, documentation, non-sensitive manifests and DVC metadata in Git.
3. Do not configure or assume a shared DVC remote yet.
4. Keep DVC cache and data directories outside tracked source paths where practical; never commit credentials, private storage paths or raw medical images.
5. Before enabling a remote, document provider, cost, encryption, access controls, backup, retention, data residency and dataset licence compatibility.
6. Revisit remote configuration when acquisition begins and storage needs are measurable.

## Consequences
- Local experiments can be prepared without an immediate cloud-storage commitment.
- Local-only DVC is not a shared backup or collaboration solution.
- Manifests must avoid direct patient identifiers and private local paths.
- The team must explicitly approve a remote before sharing data artefacts.

## Alternatives
- Configure public cloud storage immediately: deferred until privacy, cost, security and licence implications are assessed.
- Store raw images in Git: rejected due to size, provenance and redistribution risks.
