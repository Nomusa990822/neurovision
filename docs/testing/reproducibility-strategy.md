# Testing and Reproducibility Strategy

## Testing layers
1. Unit: image utilities, preprocessing, metrics, calibration and uncertainty calculations.
2. Integration: dataset-to-model and model-to-inference workflows.
3. Data: decoding, dimensions, labels, hashes, duplicates and metadata.
4. Leakage: patient/eye group overlap and duplicate contamination across partitions.
5. Model: tensor shapes, finite outputs, class ordering and checkpoint compatibility.
6. Scientific: metric calculations, confidence intervals, calibration and selective prediction.
7. Explainability: image alignment, deterministic behaviour where expected and method failure handling.
8. API: schema validation, errors, authentication and model identity.
9. Security: upload limits, file validation, dependency and container scanning.
10. Deployment: container health, configuration and service integration.
11. Reproducibility: seed/config/environment capture and repeat-run comparisons.

## Experiment record
Every run should record:
- Unique run ID and timestamp.
- Git commit and working-tree state.
- Dataset version, manifest hash and split definition.
- Model architecture and complete configuration.
- Preprocessing configuration/version.
- Optimiser, scheduler, learning rate, batch size and epochs.
- Random seeds and determinism settings.
- Python, library, CUDA/cuDNN and OS versions.
- Hardware and resource use.
- Metrics, evaluation population and confidence intervals.
- Checkpoint and artefact hashes.
- Deviations, failures and notes.

## Tooling
Planned tools: Pytest for automated tests, MLflow for run tracking, DVC for data/pipeline versioning, Git for source history, Docker for service packaging and GitHub Actions for CI.

## Reproducibility levels
Distinguish:
- Configuration reproducibility: same declared inputs and settings.
- Execution reproducibility: repeatable execution in a controlled environment.
- Statistical reproducibility: comparable conclusions across seeds or environments.
- External reproducibility: independent reproduction using documented resources.

Do not promise bit-for-bit identical GPU results across arbitrary hardware/software stacks.

## CI gates
The engineering foundation should introduce formatting/linting, type or static checks where appropriate, unit/integration tests, dependency/security checks and documentation validation. Expensive training and full-dataset tests should not run on every pull request; use small synthetic fixtures and scheduled/manual research workflows.

## Evidence and acceptance
A test is accepted only when its assertion is meaningful, its result is captured and failures are addressed or explicitly tracked. Passing software tests does not establish scientific validity.