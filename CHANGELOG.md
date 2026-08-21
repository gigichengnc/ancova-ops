# Changelog

All notable project checkpoints are documented here.

## [1.4.3] - 2026-08-21

### Added

- Added deterministic `unmeasured_confounding_blind_spot` coverage to `reasoned-validity`, where a true latent case-burden variable is removed before the ordinary Evaluate pipeline sees the frame.
- Added regression coverage that treats PASS for the hidden-confounding scenario as successful reproduction and disclosure of a known false-negative mode, not successful hidden-confounder detection.
- Added reviewer-facing regression coverage that keeps Operate described as a rule-based deterministic baseline rather than implying a trained NLP model.

### Changed

- Replaced the remaining current-facing storefront wording that could make ReasonedOps look like a rebuild of somebody else's project with same-project origin/evolution language.
- Reframed broad `request intelligence` presentation language as **rule-based request features + deterministic explainable routing baseline** while preserving the historical AI-concierge idea as project context.
- Bumped the validity benchmark schema to `reasoned-validity-v2` and explicitly separated supported behaviour from a known limitation scenario.
- Bumped package, runtime and citation metadata to `1.4.3` for the final audit-closeout checkpoint.
- Removed the historical v1.4.2 DOI from the v1.4.3 release-candidate `CITATION.cff`; the v1.4.3 DOI will only be recorded after Zenodo actually mints and verifies it.
- Prepared final artifact alignment so the GitHub release, Zenodo archive and PyPI package can all derive from the exact `v1.4.3` tag.

### Evidence boundary

v1.4.3 strengthens the evidence record by publishing a known failure mode. It does not add hidden-confounder detection, causal identification, NLP/ML routing, private-data approval or production readiness.

### Publication boundary

The release candidate intentionally omits a top-level Zenodo DOI because the immutable v1.4.3 version DOI does not exist until Zenodo ingests the release. After DOI verification, current-branch citation documentation can be synced without creating another software version. PyPI publication should use the exact existing `v1.4.3` tag so the installable artifact matches the archived release snapshot.

## [1.4.2] - 2026-08-21

### Changed

- Clarified that ReasonedOps is the author's own project, originating from participation in HKMU Hackathon 2026 and evolving into its current Operate → Audit → Evaluate form.
- Replaced current-facing language that could be read as a rebuild of another project with project-evolution wording.
- Updated `CITATION.cff` so Zenodo-facing metadata uses the corrected project-origin framing.
- Added an explicit README boundary that the Hackathon name is referenced only to describe project origin and does not present ReasonedOps as an official HKMU product or endorsement.
- Added regression coverage preventing the misleading retrospective-rebuild wording from returning to the current README or citation metadata.

### Publication boundary

v1.4.2 is a wording/citation correction only. It does not change software behaviour, evidence status, the currently verified PyPI artifact (`reasoned-ops==1.4.0`), private-data approval or production readiness.

## [1.4.1] - 2026-08-21

### Changed

- Created a documentation/citation-only archive checkpoint after `gigichengnc/reasoned-ops` was enabled for Zenodo GitHub release preservation.
- Bumped package and `CITATION.cff` checkpoint metadata to `1.4.1` so the post-enablement GitHub release has aligned software citation metadata.
- Updated project, citation and release-readiness documentation to distinguish the Zenodo archive release from the currently published and externally verified PyPI artifact `reasoned-ops==1.4.0`.

### Archive boundary

v1.4.1 does not add or change routing, audit, outcome, statistical, adaptive-policy or longitudinal behaviour. It exists so a new GitHub release can be ingested after Zenodo integration was enabled. A Zenodo DOI makes the release persistently citable; it does not constitute peer review, real-world validation, private-data pilot approval or production readiness.

## [1.4.0] - 2026-08-21

### Added

- A dedicated PyPI-facing `PYPI.md` package description with installation and reuse examples.
- CI distribution validation that builds both wheel and source distributions with `python -m build`.
- A clean-environment wheel installation smoke test covering package import, version metadata, routing and an installed CLI entry point.
- `.github/workflows/publish-pypi.yml`, a manually dispatched PyPI Trusted Publishing workflow using GitHub OIDC rather than a long-lived API token.
- `docs/pypi.md` with the exact pending Trusted Publisher identity, first-publication procedure and post-publication verification steps.
- PyPI classifiers for supported Python versions, Apache-2.0 licensing and package maturity.

### Changed

- Bumped package and citation metadata to `1.4.0`.
- Separated the GitHub portfolio README from the PyPI long description so relative repository links do not become the package-index presentation surface.
- Kept the first PyPI upload manual so no publication is attempted before the repository owner configures the matching PyPI Trusted Publisher.

### Distribution boundary

The v1.4.0 checkpoint validates that ReasonedOps can be built and installed as a normal Python distribution rather than only from an editable Git checkout. A successful wheel build is distribution evidence, not proof of real-world service effectiveness, private-data approval or production readiness.

## [1.3.0] - 2026-08-21

### Added

- `original/README.md`, a public reconstruction of the HKMU Hackathon 2026 concierge concept that preserves project lineage without publishing presentation-only/private source material.
- `docs/before-vs-after.md`, a reviewer-facing comparison of the original concept and the ReasonedOps rebuild.
- `docs/original-concept-audit.md`, documenting which original assumptions were preserved, corrected, narrowed or deferred.
- `docs/model-decisions.md`, recording why ANCOVA moved downstream, unsupported comparisons are refused, adaptive routing stays offline and LSTM remains deferred.
- Regression coverage ensuring the rebuild-story files remain part of the repository checkpoint.

### Changed

- Reframed the repository presentation from a startup-style product overview into a retrospective engineering/research rebuild case study.
- Rewrote the README around: original question → why rebuild → what changed → what runs → evidence/model decisions → limitations → next evidence gate.
- Made the project origin and learning progression visible before deep implementation detail.
- Reworked the architecture documentation into a current version-neutral system map and added comparison-support / applicability before statistical modelling.
- Marked the old v0.5.0 checkpoint summary explicitly as historical rather than current ReasonedOps status.
- Updated project status and release-readiness documentation for the v1.3 portfolio narrative.
- Bumped package and citation metadata to `1.3.0`.

### Evidence and deployment status

This release changes portfolio structure, historical preservation, documentation and reviewer comprehension. It does not add representative real-world evidence or increase deployment readiness. Quantitative development evidence remains synthetic or hand-authored; real private-data pilot use and production deployment remain not approved.

## [1.2.0] - 2026-08-21

### Changed

- Completed the project rename at the implementation level: `src/reasoned_ops` is now the single application package.
- Removed the temporary `src/ancova_ops` compatibility namespace introduced during the v1.1 migration.
- Replaced remaining internal imports and current-facing command/path references with the canonical ReasonedOps namespace.
- Replaced temporary showcase/management/applicability wrappers with self-contained ReasonedOps implementations.
- Rewrote the README around one concrete request → routing → human review → outcome → evaluation workflow rather than architecture-first explanation.
- Reworked the generated showcase so it demonstrates one service case and the later management evidence check directly.
- Updated project-status, release-readiness, hackathon-origin, storefront and showcase documentation for the clean v1.2 identity.
- Added regression coverage preventing the legacy source namespace from reappearing.

### Evidence and deployment status

This release changes naming consistency, code organisation and reviewer usability. It does not add real-world validation. Quantitative development evidence remains synthetic or hand-authored, and real private-data pilot use and production deployment remain not approved.

## [1.1.1] - 2026-08-21

### Changed

- Reworked the README first screen so a first-time reviewer can immediately see that ReasonedOps is a runnable local research prototype rather than only a concept or methodology document.
- Added a concrete working-status table covering the API, audit trail, human override, outcome capture, management reporting, applicability checks and research benchmarks.
- Added a 60-second proof path using `reasoned-showcase`, including the generated report location.
- Added a direct FastAPI health check and example `/v1/route` request so reviewers can verify the operational path without reading the full methodology first.
- Clarified the distinction between a working local prototype, a real private-data pilot and a production deployment.
- Reworded the project-origin statement to reflect the author's participation in HKMU Hackathon 2026.
- Updated the canonical FastAPI title/version from the former ANCOVA Ops branding to ReasonedOps and aligned it with the package version.
- Bumped package and citation metadata to `1.1.1`.

### Evidence and deployment status

This is a usability, documentation and branding-consistency patch. It does not add a new evidence class or establish real-world service improvement. Current quantitative evidence remains synthetic or hand-authored development evidence. Real private-data pilot use and production deployment remain not approved.

## [1.1.0] - 2026-08-21

### Renamed

- Renamed the project from **ANCOVA Ops** to **ReasonedOps** so the name reflects the actual product architecture: **Operate → Audit → Evaluate**.
- Renamed the canonical GitHub repository to `gigichengnc/reasoned-ops`.
- Renamed the Python distribution to `reasoned-ops` and added the canonical `reasoned_ops` package namespace.
- Renamed the public CLI surface from `ancova-*` to `reasoned-*`.
- Updated README, citation metadata, package URLs, CI smoke commands and public examples to the ReasonedOps identity.

### Compatibility

- The legacy `ancova_ops` namespace is retained temporarily for compatibility with historical local examples and development references.
- Historical release notes before v1.1.0 intentionally retain the former project name and old command names.
- ANCOVA/regression remains an evaluation method inside ReasonedOps; the statistical method itself is not renamed.

### Evidence and deployment status

This is a naming/package migration checkpoint. It does not add a new evidence class or change the project completion boundary. Current quantitative evidence is synthetic or hand-authored development evidence. Real private-data pilot use and production deployment remain not approved.

## [1.0.0] - 2026-08-20

### Added

- `ancova-applicability`, the final evaluation-method gate for the completed Operate → Audit → Evaluate research prototype.
- Explicit `EvaluationQuestion` and `ApplicabilityDecision` models.
- Four high-level applicability dispositions: `use`, `caution`, `reject`, and `recommend_alternative`.
- Method-family recommendations for binary outcomes, censored/time-to-event outcomes, repeated/clustered observations, routing-policy counterfactuals and causal-intent questions.
- Direct reuse of v0.6 department/case-type identifiability and department-specific slope warnings in the final gate.
- Management-report integration that surfaces applicability disposition, recommended method family, reasons, next step and interpretation boundary.
- v1 showcase integration that presents Operate → Audit → Evaluate end to end.
- `docs/evaluation-applicability.md` with the final method-selection/refusal framework.
- Deterministic applicability tests and CI smoke coverage.

### Changed

- Bumped package/project/citation metadata to `1.0.0`.
- Reframed the project as a completed evidence-aware service-operations research prototype rather than an indefinitely expanding ANCOVA product.
- Made the final project identity explicit: Operate → Audit → Evaluate.
- Made unsupported management conclusions, not automatic management decision-making, the central product/research boundary.
- Updated the management report so method applicability is a first-class output alongside overlap/identifiability and statistical diagnostics.
- Updated the one-command showcase to mark the research project complete/frozen at v1 while retaining private-data pilot and production locks.
- Finalised README, statistical methodology, project status, release readiness and roadmap around the v1 completion line.

### Project completion boundary

v1.0.0 is the completion line for the research/portfolio project. The project deliberately does not implement every possible logistic, survival, hierarchical or causal model. Instead, the applicability gate refuses or redirects questions that should not be forced through ordinary continuous-outcome ANCOVA/regression.

Further model-building, real-data work or deployment is post-v1 and should require a concrete user, competition requirement, research question or pilot opportunity.

### Evidence and deployment status

The v1 release preserves the existing evidence hierarchy. Current quantitative evidence is synthetic or hand-authored development evidence. Applicability rules and synthetic validity benchmarks do not establish real-world service improvement, causal effects, private-data pilot approval or production readiness.

## [0.6.0] - 2026-08-20

### Added

- `ancova-validity`, a deterministic synthetic validity benchmark covering known-effect recovery, measured case-mix confounding, no-overlap refusal and slope-interaction detection.
- Department/issue-category overlap diagnostics that check graph connectivity, practical support and design-matrix rank before adjusted department comparisons are reported.
- Explicit model applicability output in technical and management-facing outcome reports.

### Changed

- Repositioned ANCOVA/regression as one method inside a broader evidence-aware evaluation layer rather than the product core.
- Added `issue_category` as a pre-routing case-mix factor in the default outcome model.
- Replaced the previous one-issue-per-department synthetic outcome setup with overlapping issue categories and known artificial department/issue effects.
- Standardised adjusted department estimates over the observed complete-case case-mix distribution instead of holding only continuous covariates at their means.
- Withhold adjusted department estimates and department ANOVA output when department and issue category are not separately identifiable.
- Updated management reporting so unsupported comparisons are shown as `withheld` rather than converted into a league table.
- Bumped package, citation metadata and CLI surface to `0.6.0`.

### Validation boundary

The new benchmark demonstrates that the software behaves sensibly on synthetic scenarios where the truth is known: it should recover known additive effects within tolerance, reduce deliberately induced measured case-mix bias, refuse comparisons under structural no-overlap, and flag a deliberately violated common-slope assumption. This validates software/statistical behaviour, not real service outcomes.

### Evidence and deployment status

ANCOVA Ops remains a synthetic/hand-authored research prototype. The evaluation layer does not prove causal department effects, real routing improvement, private-data pilot readiness or production readiness. Real operational use still requires representative data, a defensible study design, governance approval and method selection matched to the actual outcome/question.

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

Zenodo supports both `CITATION.cff` and `.zenodo.json` for GitHub software metadata, but gives `.zenodo.json` precedence when both files are present. ANCOVA Ops does not currently require Zenodo-specific grant/community metadata, so duplicate metadata is intentionally avoided. No DOI, ORCID, email address or affiliation is fabricated at this checkpoint.

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
- Deferred LSTM/sequence modelling until a same-benchmark experiment can demonstrate incremental value over simpler baselines.
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
