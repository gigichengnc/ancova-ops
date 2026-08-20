# Changelog

All notable project checkpoints are documented here.

## [0.5.4] - 2026-08-20

### Added

- Root `CITATION.cff` using Citation File Format 1.2.0 so GitHub can render software citation metadata.
- `docs/citation.md` describing GitHub citation, Zenodo integration, DOI follow-up and publication boundaries.
- Public project author, keywords and repository/changelog/citation URLs in package metadata.
- Regression coverage that keeps package, CFF version, Apache-2.0 license, author and repository citation metadata aligned.

### Changed

- Bumped project/package checkpoint from `0.5.3` to `0.5.4`.
- Updated README, project status, release readiness and roadmap to distinguish citation readiness from DOI publication or peer review.
- Kept `CITATION.cff` as the single citation metadata source rather than adding a speculative `.zenodo.json` file.

### Citation and Zenodo note

Zenodo supports both `CITATION.cff` and `.zenodo.json`, but gives `.zenodo.json` precedence when both files are present. ANCOVA Ops does not currently require Zenodo-specific grant/community metadata, so duplicate metadata is intentionally avoided. No DOI, ORCID, email address or affiliation is fabricated at this checkpoint.

### Evidence and deployment status

Citation readiness does not change the evidence class. Current quantitative results remain synthetic or hand-authored development evidence. A DOI, once minted, would make a software release persistently citable; it would not constitute peer review, real-world validation, private-data pilot approval or production readiness.

## [0.5.3] - 2026-08-20

### Changed

- Polished the GitHub README first screen with CI/release/license/Python badges, a reviewer-facing status summary and a faster path to the one-command showcase.
- Added `docs/github-storefront.md` with recommended repository About text, focused topic tags and social-preview copy.
- Changed the release workflow so automatic publication follows successful `main` CI rather than being triggered merely by editing the release workflow itself.
- Made the showcase version derive from the package version to remove another source of release-version drift.
- Updated the Release badge link to the repository's latest release rather than a fixed historical tag.

### Evidence and deployment status

This is a presentation and release-synchronisation checkpoint. No routing, statistical, adaptive-policy or longitudinal model logic is promoted as new real-world evidence. Current quantitative evidence remains synthetic or hand-authored; private-data pilot use and production deployment remain not approved.

## [0.5.2] - 2026-08-20

### Added

- Canonical Apache License 2.0 text as the repository root `LICENSE`.
- SPDX `Apache-2.0` package/project license metadata.
- Regression coverage that checks both the declared SPDX identifier and the root license file.

### Changed

- Bumped package/project metadata and showcase version from `0.5.1` to `0.5.2`.
- Replaced the previous no-license repository caveat with an explicit Apache-2.0 licensing statement.
- Clarified that ANCOVA Ops licensing does not relicense third-party dependencies or separately identified third-party material.

### Licensing note

A speculative `THIRD_PARTY_NOTICES.md` file is intentionally not added at this checkpoint. If ANCOVA Ops later incorporates or adapts third-party source material that carries notice obligations, those notices should be recorded separately and preserved as required.

### Evidence and deployment status

This licensing checkpoint does not change the project evidence class or deployment readiness. Current quantitative evidence remains synthetic or hand-authored, private-data pilot use remains not approved, and production deployment remains not approved.

## [0.5.1] - 2026-08-20

### Added

- `ancova-showcase`, a deterministic reviewer-facing command that orchestrates the existing Phase 1–4 workflows without introducing a new model.
- Self-contained Markdown showcase output plus optional structured JSON output.
- One-page evidence/readiness view covering request intelligence, routing benchmark, ANCOVA outcome analysis, adaptive-routing research, longitudinal modelling and governance status.
- `docs/portfolio-showcase.md` with reviewer/demo instructions and interpretation boundaries.
- Deterministic showcase regression coverage and CI smoke testing on Python 3.11 and 3.12.

### Changed

- Bumped package/project metadata from `0.5.0` to `0.5.1`.
- Expanded the public command surface from six to seven CLI entry points.
- Made the portfolio path easier for an external reviewer by providing one command rather than requiring separate execution of every workflow.

### Evidence and deployment status

The showcase only reorganises existing hand-authored and synthetic development evidence. It does not convert any result into real-world evidence, and it does not change the private-data, pilot or production deployment locks.

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

- No project licence had been selected at the v0.5.0 checkpoint, so reuse and redistribution rights were not yet defined.
- Pilot-specific jurisdiction/privacy review, notice/consent design, access controls, retention schedule and deletion procedure remain open.
- Production authentication/RBAC, secrets management, monitoring, incident response and operational deployment controls are outside the current prototype scope.
- Real-data validation is still required before any synthetic benchmark result can support an operational claim.