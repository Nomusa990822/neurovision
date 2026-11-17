# ADR-018: Apache License 2.0 for NeuroVision Software

- Status: Accepted
- Date: 2026-11-17
- Decision owner: Project owner

## Context
A clear software licence is required before broader reuse and contributions.

## Decision
License original NeuroVision software and project-authored materials under Apache License, Version 2.0 (SPDX: Apache-2.0). The canonical licence text is stored in the repository root as LICENSE.

This applies only to material the project has the right to license. Third-party code, fonts, assets, publications, datasets, OCT images, annotations and pretrained weights remain subject to their own licences and terms. The NeuroVision LICENSE grants no rights in dataset contents.

## Rationale
Apache-2.0 is permissive and includes express copyright and patent grants, redistribution conditions, and warranty/liability disclaimers.

## Consequences
- Include the full canonical licence text at repository root.
- Identify third-party materials and their licence notices.
- Add SPDX identifiers to original source files as the implementation scaffold is created.
- Preserve required copyright, attribution and NOTICE information.
- Reassess if project ownership or contribution arrangements materially change.

## Reference
Apache Software Foundation, Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt
