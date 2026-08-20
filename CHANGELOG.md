# Changelog

All notable project checkpoints are documented here.

## [0.5.0] - 2026-08-20

### Added

- FastAPI service-request routing API with structured request intelligence and explainable baseline routing.
- SQLite persistence for immutable service cases, append-only routing decisions, human routing reviews and observed outcomes.
- Deterministic routing evaluation fixture with baseline department accuracy, human-review recall and explanation-coverage metrics.
- Machine-readable development-stage data-governance policy with CI validation and explicit restrictions on private data, raw-message training and unsupported profiling.
- ANCOVA/regression workflow with missingness, group-size, residual, heteroskedasticity, multicollinearity, influence and interaction diagnostics.
- Adjusted departmental estimates with confidence intervals plus technical and management-facing reporting commands.
- Synthetic logged-policy adaptive-routing research framework with chronological validation, inverse-propensity scoring, support diagnostics, human approval, versioning and rollback.
- Synthetic longitudinal recurrence benchmark with leakage-safe time splits, recency/frequency baseline, discrete-time hazard model and random-forest comparator.
- CLI entry points for routing evaluation, governance validation, outcome analysis, management reporting, adaptive-policy evaluation and longitudinal benchmarking.
- Python 3.11 and 3.12 CI coverage for tests, lint and every major command-line smoke test.

### Changed

- Corrected the original hackathon architecture so ANCOVA is used for downstream outcome analysis rather than per-message scoring.
- Reframed emotional/contextual scores as transparent operational heuristics rather than psychological measurements.
- Made synthetic or hand-authored provenance explicit throughout evaluation workflows.
- Deferred LSTM/sequence modelling until a same-benchmark experiment can demonstrate incremental value over simpler approaches.
- Aligned package `__version__` with the project metadata at `0.5.0` and added a regression test to prevent future version drift.

### Evidence status

The v0.5.0 checkpoint is a reproducible development and research prototype. Current quantitative results come from synthetic data or a small hand-authored fixture unless explicitly stated otherwise. They are not production performance estimates, causal effects or evidence of real resident/customer outcomes.

### Governance and deployment status

- Real private resident/customer data: **not approved**.
- Longitudinal personalisation using real histories: **not approved**.
- Adaptive-policy integration into the live `/v1/route` path: **not enabled**.
- Production deployment: **not approved**.
- External AI/model-provider use with private request content: requires a separate data-processing and governance review.

### Known release-readiness limitations

- No project licence has been selected, so reuse and redistribution rights are not yet defined.
- Pilot-specific jurisdiction/privacy review, notice/consent design, access controls, retention schedule and deletion procedure remain open.
- Production authentication/RBAC, secrets management, monitoring, incident response and operational deployment controls are outside the current prototype scope.
- Real-data validation is still required before any synthetic benchmark result can support an operational claim.
