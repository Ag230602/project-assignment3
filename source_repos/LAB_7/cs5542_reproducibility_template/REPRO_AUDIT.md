Reproducibility Audit

Environment
Dependencies are pinned in requirements.txt.

Deterministic Execution
random.seed(42)
numpy.random.seed(42)
torch.manual_seed(42)

Logging
Logs are stored in logs/

Artifacts
Outputs saved in artifacts/

Smoke Test
tests/smoke_test.py verifies environment and pipeline initialization.