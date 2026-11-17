# ADR-001: Use a Modular Monorepo

- **Status:** Accepted
- **Date:** 2026-11-17

## Context
NeuroVision combines dataset tooling, ML research, explainability, uncertainty, an API and a dashboard. These components must evolve together while retaining independent boundaries.

## Decision
Use one Git repository with separate research, application, documentation and infrastructure directories. Keep reusable Python functionality in an installable package under `src/neurovision/`.

## Alternatives
- Separate repositories for model, API and frontend.
- One monolithic application directory.

## Consequences
A monorepo simplifies coordinated versioning, issue tracking and CI. It requires explicit module interfaces and disciplined ownership to avoid coupling. Large datasets and checkpoints remain outside normal Git history.