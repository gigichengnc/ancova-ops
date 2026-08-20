# Roadmap

ANCOVA Ops is now scoped as a finite research/portfolio project built around:

> **Operate → Audit → Evaluate**

The project is not intended to expand indefinitely. v1.0 is the completion line for the research prototype; real private-data pilots and production infrastructure are separate post-v1 work.

## Phase 0 — Foundation

Goal: create a runnable, testable project skeleton.

- [x] project documentation;
- [x] corrected separation between real-time routing and downstream outcome analysis;
- [x] service-case models;
- [x] transparent routing function;
- [x] synthetic outcome generator;
- [x] regression/ANCOVA helper;
- [x] tests and CI.

## Phase 1 — Operate

Goal: turn a service request into a structured, reviewable operational recommendation.

- [x] request/response API contract;
- [x] issue taxonomy;
- [x] transparent baseline request intelligence;
- [x] urgency/context extraction interface;
- [x] explainable routing recommendation;
- [x] hand-authored routing evaluation fixture;
- [x] deterministic baseline routing metrics.

## Phase 1B — Audit

Goal: preserve decision history and outcomes without overwriting the evidence chain.

- [x] SQLite persistence;
- [x] immutable original service case by `case_id`;
- [x] append-only machine/rule routing decisions;
- [x] human confirmation / override capture;
- [x] effective route without erasing original machine history;
- [x] outcomes stored separately from routing decisions;
- [x] actor/review fields preserved as audit records;
- [x] human review is not automatically treated as ground truth.

## Cross-cutting — Data governance

Goal: define privacy/data-use boundaries before real private data enters the project.

- [x] synthetic-only development boundary;
- [x] machine-readable field sensitivity and purpose registry;
- [x] retention/deletion expectations;
- [x] analytics export restrictions;
- [x] longitudinal-feature purpose register;
- [x] prohibit unsupported psychological profiling;
- [x] prohibit real private records in Git;
- [x] governance validation command and CI check;
- [ ] pilot-specific jurisdiction/privacy review before private-data import;
- [ ] concrete pilot retention schedule before private-data import;
- [ ] pilot notice/consent and access-control design.

The unchecked governance items are **pilot gates**, not blockers to research-project v1.0 completion.

## Phase 2 — Evaluate: outcome analysis

Goal: avoid misleading raw performance comparisons.

- [x] pre-specified analytical question;
- [x] raw-versus-adjusted department reporting;
- [x] ANCOVA/regression workflow;
- [x] missingness and complete-case accounting;
- [x] group-size checks;
- [x] residual diagnostics;
- [x] heteroskedasticity diagnostics;
- [x] multicollinearity diagnostics;
- [x] influence diagnostics;
- [x] department-by-covariate interaction checks;
- [x] adjusted estimates with uncertainty;
- [x] management-facing Markdown and structured reports;
- [x] explicit non-causal interpretation boundary.

## Phase 3 — Evaluate: offline routing-policy research

Goal: test candidate routing policies without wiring them into live routing.

- [x] versioned transparent candidate policy;
- [x] deterministic synthetic logged-routing history with known propensities;
- [x] strict chronological validation split;
- [x] inverse-propensity / self-normalised evaluation;
- [x] effective-sample-size and support diagnostics;
- [x] offline limitations documented;
- [x] explicit human approval before candidate activation;
- [x] local policy version registry and rollback path;
- [x] candidate remains disconnected from live `/v1/route` by design.

## Phase 4 — Evaluate: longitudinal research

Goal: investigate recurrence and seasonality without assuming sequence modelling is necessary.

- [x] deterministic synthetic entity histories;
- [x] recurrence and seasonal structure;
- [x] pre-cutoff feature snapshots;
- [x] recurrence and censored time-to-next-case targets;
- [x] purged chronological validation;
- [x] feature-time/follow-up leakage checks;
- [x] recency/frequency logistic baseline;
- [x] discrete-time hazard benchmark;
- [x] random-forest comparator;
- [x] same-window discrimination/calibration comparison;
- [x] survival concordance;
- [x] model-complexity incremental-value rule;
- [x] LSTM/sequence work deferred until justified by the same benchmark.

## v0.5.x — Repository, licensing and citation checkpoint

Goal: make the project understandable, reproducible, licensed and citable.

- [x] package/project version alignment;
- [x] changelog;
- [x] project-status and release-readiness docs;
- [x] external-facing README;
- [x] one-command `ancova-showcase`;
- [x] Apache License 2.0;
- [x] CI-gated GitHub release workflow;
- [x] root `CITATION.cff` and citation guide.

## v0.6.0 — Evaluation validity and refusal behaviour

Goal: make the evaluation layer demonstrate **when a department comparison can be supported and when it must be withheld**.

- [x] add `issue_category` as a measured case-mix factor;
- [x] replace one-issue-per-department synthetic outcomes with overlapping case mix;
- [x] add department × issue-category count diagnostics;
- [x] add structural overlap/connectivity check;
- [x] add practical overlap threshold;
- [x] add design-matrix rank / identifiability check;
- [x] classify comparison support as `supported`, `weak_overlap`, or `not_identifiable`;
- [x] withhold adjusted estimates when department and issue type are not separately identifiable;
- [x] withhold department ANOVA output in the no-overlap case;
- [x] block management adjusted ranking when the design is not identifiable;
- [x] standardise adjusted means over observed complete-case case mix;
- [x] add known-effect recovery scenario;
- [x] add measured-confounding scenario comparing adjusted versus naive analysis;
- [x] add no-overlap refusal scenario;
- [x] retain slope-interaction failure scenario;
- [x] add `ancova-validity` CLI and CI smoke test;
- [x] align README/methodology/status docs with Operate → Audit → Evaluate;
- [ ] final Python 3.11/3.12 PR CI pass;
- [ ] merge and publish `v0.6.0` checkpoint.

## v1.0.0 — Final research-project completion gate

Goal: make **method follows the question** executable and freeze the project as a coherent research prototype.

### Evaluation applicability gate

- [ ] represent the intended outcome/evaluation question explicitly;
- [ ] distinguish continuous, binary and time-to-event/censored outcomes;
- [ ] represent repeated/clustered observations when declared;
- [ ] reuse overlap/identifiability results for department comparisons;
- [ ] return one of `use`, `caution`, `reject`, or `recommend_alternative`;
- [ ] recommend logistic-type analysis for binary outcomes rather than forcing ANCOVA;
- [ ] recommend survival/time-to-event analysis for censored resolution time;
- [ ] recommend clustered/hierarchical analysis when repeated grouping is declared;
- [ ] reject non-identifiable department comparisons;
- [ ] caution on weak overlap or common-slope violations;
- [ ] keep recommendations explanatory and non-causal;
- [ ] add deterministic tests and CLI/report output.

### Final project freeze

- [ ] update showcase to present Operate → Audit → Evaluate end to end;
- [ ] finalise README and architecture terminology;
- [ ] final v1.0 regression suite on Python 3.11/3.12;
- [ ] tag/release v1.0.0;
- [ ] mark further modelling as post-v1 work requiring a concrete external reason.

v1.0 does **not** require implementation of every alternative statistical method. It requires the system to avoid using the wrong method silently.

## Optional publication/distribution work

These do not block v1.0 completion:

- [ ] connect GitHub to Zenodo and mint/verify a DOI;
- [ ] add the verified DOI back to `CITATION.cff`;
- [ ] optionally add PyPI trusted publishing;
- [ ] consider a software paper only if research use/reuse evidence later justifies it.

## Post-v1 pilot gates

A real-data pilot requires separate work including privacy/legal review, notice/consent where applicable, authenticated staff identities, RBAC, secure storage, retention/deletion, pseudonymisation/linkage, incident response, external-provider review, real-data annotation/outcome-quality protocols and pilot stop criteria.

## Post-v1 production gates

Production additionally requires real-data validation, environment separation, authenticated APIs, monitoring/alerting, backup/recovery, security testing, change control, rollback drills, manual fallback and operational acceptance criteria.

These items are deliberately outside the research-project completion definition.
