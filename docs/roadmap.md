# Roadmap — Research Project Complete at v1.0

ANCOVA Ops is a finite research/portfolio project built around:

> **Operate → Audit → Evaluate**

**v1.0.0 is the completion line for the research prototype.** Real private-data pilots, production infrastructure, new model families and publication/distribution work are separate post-v1 opportunities.

## Phase 0 — Foundation ✅

- [x] runnable/testable project skeleton;
- [x] separation between real-time routing and downstream outcome analysis;
- [x] service-case models and transparent baseline routing;
- [x] synthetic development data;
- [x] regression/ANCOVA helper;
- [x] tests and CI.

## Phase 1 — Operate ✅

- [x] request/response API contract;
- [x] issue taxonomy;
- [x] transparent request intelligence;
- [x] urgency/context extraction;
- [x] explainable routing recommendation;
- [x] hand-authored routing benchmark.

## Phase 1B — Audit ✅

- [x] SQLite persistence;
- [x] immutable original service case by `case_id`;
- [x] append-only machine/rule routing decisions;
- [x] human confirmation / override capture;
- [x] effective route without erasing machine history;
- [x] outcomes stored separately from routing decisions;
- [x] human review not automatically treated as ground truth.

## Cross-cutting — Development data governance ✅

- [x] synthetic-only development boundary;
- [x] machine-readable field sensitivity/purpose registry;
- [x] analytics export restrictions;
- [x] retention/deletion expectations;
- [x] longitudinal-feature purpose register;
- [x] prohibit unsupported psychological profiling;
- [x] prohibit real private records in Git;
- [x] governance validation command and CI check.

Pilot-specific privacy/legal, consent, access-control and retention implementation remains post-v1 because no real private-data pilot is approved.

## Phase 2 — Evaluate: outcome analysis ✅

- [x] pre-specified analytical question;
- [x] raw-versus-adjusted reporting;
- [x] case-mix-adjusted regression/ANCOVA workflow;
- [x] missingness/complete-case accounting;
- [x] group-size, residual, variance, multicollinearity and influence diagnostics;
- [x] department-by-covariate interaction screening;
- [x] adjusted estimates with uncertainty;
- [x] management-facing Markdown/JSON report;
- [x] explicit non-causal interpretation boundary.

## Phase 3 — Evaluate: offline policy research ✅

- [x] transparent candidate policy;
- [x] deterministic synthetic logged-routing history with known propensities;
- [x] strict chronological validation;
- [x] support-aware inverse-propensity evaluation;
- [x] ESS and unsupported-action diagnostics;
- [x] human approval/version/rollback lifecycle;
- [x] candidate remains disconnected from live `/v1/route` by design.

## Phase 4 — Evaluate: longitudinal research ✅

- [x] deterministic synthetic entity histories;
- [x] recurrence/seasonality structure;
- [x] leakage-aware feature snapshots and purged chronological validation;
- [x] recurrence and censored time-to-next-case targets;
- [x] recency/frequency logistic baseline;
- [x] discrete-time hazard benchmark;
- [x] random-forest comparator;
- [x] same-window discrimination/calibration comparison;
- [x] model-complexity incremental-value rule;
- [x] sequence/LSTM work explicitly deferred until justified.

## v0.5.x — Repository / licensing / citation ✅

- [x] package/project version alignment;
- [x] changelog and status/readiness docs;
- [x] external-facing README;
- [x] one-command `ancova-showcase`;
- [x] Apache License 2.0;
- [x] CI-gated GitHub release workflow;
- [x] root `CITATION.cff` and citation guide.

## v0.6.0 — Evaluation validity and refusal behaviour ✅

- [x] `issue_category` as measured case mix;
- [x] overlapping synthetic outcome generator with known effects;
- [x] department × issue-category counts;
- [x] structural overlap/connectivity check;
- [x] practical overlap threshold;
- [x] design-matrix rank / identifiability check;
- [x] `supported`, `weak_overlap`, `not_identifiable` statuses;
- [x] withhold adjusted estimates under non-identifiability;
- [x] withhold department ANOVA output under non-identifiability;
- [x] block management adjusted ranking under no overlap;
- [x] standardise adjusted means over observed case mix;
- [x] known-effect recovery scenario;
- [x] measured-confounding versus naive scenario;
- [x] no-overlap refusal scenario;
- [x] slope-interaction scenario;
- [x] `ancova-validity` CLI, tests and CI smoke;
- [x] Python 3.11/3.12 CI green and v0.6.0 merged.

## v1.0.0 — Evaluation applicability and project freeze ✅

Goal: make **method follows the question** executable rather than forcing ANCOVA onto every analytical problem.

### Applicability gate

- [x] explicit evaluation-question model;
- [x] continuous, binary and time-to-event outcome types;
- [x] department, descriptive and routing-policy question types;
- [x] censoring declaration;
- [x] repeated/clustered-observation declaration;
- [x] causal-intent declaration;
- [x] reuse v0.6 overlap/identifiability status;
- [x] reuse department-specific slope flags;
- [x] exactly four high-level dispositions: `use`, `caution`, `reject`, `recommend_alternative`;
- [x] supported continuous department comparison → `regression_ancova_style`;
- [x] weak overlap → `caution`;
- [x] slope violation → `interaction_aware_regression` caution;
- [x] no overlap → `reject` / no adjusted department comparison;
- [x] binary outcome → logistic-type recommendation;
- [x] censored/time-to-event outcome → survival recommendation;
- [x] repeated/clustered data → clustered/hierarchical recommendation;
- [x] routing-policy question → offline policy evaluation recommendation;
- [x] causal intent → causal design/identification recommendation;
- [x] `ancova-applicability` CLI and deterministic tests;
- [x] management report integration;
- [x] one-command showcase integration;
- [x] applicability methodology guide.

### Final project freeze

- [x] README defines final Operate → Audit → Evaluate identity;
- [x] showcase presents the end-to-end v1 architecture;
- [x] project status/readiness docs define v1 as the research completion line;
- [x] package and citation metadata target `1.0.0`;
- [x] CI includes applicability plus all existing workflow smoke tests;
- [x] further model-building classified as post-v1 work requiring a concrete external reason.

The release/tag is created only after the final pull-request and `main` CI checks succeed; release publication is operational release bookkeeping rather than additional research scope.

## Optional post-v1 publication/distribution

These are **not unfinished v1 work**:

- [ ] connect GitHub to Zenodo and mint/verify a DOI;
- [ ] add a verified DOI back to `CITATION.cff`;
- [ ] optionally publish a package to PyPI;
- [ ] consider a software paper if later research use/reuse justifies it.

## Post-v1 real-data pilot

A pilot requires a new approved stage covering privacy/legal review, notice/consent where applicable, authenticated identities, RBAC, secure storage, retention/deletion, pseudonymisation/linkage, incident response, external-provider review, real-data annotation/outcome-quality protocols and stop criteria.

## Post-v1 production

Production additionally requires representative real-data validation, secure environment separation, authenticated APIs, monitoring/alerting, backup/recovery, security testing, change control, rollback/fallback procedures and operational acceptance.

Neither pilot nor production work changes the fact that the **v1 research/portfolio project is complete**.
