# ADR-017: Modular Research Package and Application Boundaries

- Status: Proposed for Phase 2 approval
- Date: 2026-11-17
- Decision owners: NeuroVision project

## Context

The repository currently contains project documentation but no executable package. The system must support reproducible research pipelines and a future inference application without coupling scientific logic to HTTP, database or UI concerns.

## Proposed decision

Adopt a modular monolith with an installable Python package under src/neurovision/. Keep research and domain logic in independently testable modules. Treat FastAPI and the dashboard as application adapters that orchestrate package interfaces. Maintain explicit boundaries for data, models, evaluation, explainability, uncertainty, inference and configuration.

## Alternatives considered

- Notebook-first implementation: rejected as the primary architecture because notebooks alone do not provide stable package interfaces or reliable automated testing.
- Microservices from the outset: rejected as unnecessary operational complexity for a research prototype.
- Single monolithic application module: rejected because it couples data science, model logic, API and UI concerns.

## Consequences

- A minimal package, test suite and CI are the first Phase 2 deliverables.
- The first implementation should avoid premature service decomposition.
- Application endpoints should call tested package services.
- Module interfaces and configuration contracts must be documented as implemented.

## Approval note

This ADR remains proposed until the project owner approves the Phase 2 engineering scaffold. The proposed package structure is not implemented by this decision.
