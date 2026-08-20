# Roadmap

## Phase 0 — Foundation

Goal: create a runnable, testable project skeleton.

- [x] English project documentation
- [x] corrected separation between NLP/routing and ANCOVA
- [x] baseline service-case models
- [x] transparent routing function
- [x] synthetic outcome generator
- [x] ANCOVA fitting helper
- [x] starter tests
- [x] continuous integration

## Phase 1 — Service-intelligence MVP

Goal: accept a real request and produce a structured, reviewable routing recommendation.

- [x] request/response API contract;
- [x] issue taxonomy;
- [x] transparent baseline text classifier;
- [x] urgency/context extraction interface;
- [x] persistence layer;
- [x] routing decision audit log;
- [x] outcome capture fields;
- [x] human confirmation / override capture;
- [x] effective routing view without overwriting machine history;
- [x] hand-authored routing evaluation fixture;
- [x] deterministic baseline metrics;
- [x] candidate-vs-baseline comparison harness.

## Cross-cutting — Data governance

Goal: define privacy and data-use boundaries before any real pilot data is introduced.

- [x] synthetic-only development boundary;
- [x] machine-readable field sensitivity and purpose registry;
- [x] retention and deletion expectations;
- [x] analytics export restrictions;
- [x] longitudinal-feature purpose and retention register;
- [x] prohibit unsupported psychological profiling;
- [x] prohibit real private records in Git;
- [x] governance validation command and CI check;
- [ ] pilot-specific jurisdiction/privacy review before any private-data import;
- [ ] concrete pilot retention schedule before any private-data import;
- [ ] pilot notice/consent and access-control design before longitudinal personalisation.

## Phase 2 — Outcome analytics

Goal: evaluate service outcomes credibly.

- [x] pre-specified analytical question;
- [x] ANCOVA / regression workflow;
- [x] required-field missingness and complete-case accounting;
- [x] department group-size checks;
- [x] residual and influential-point diagnostics;
- [x] heteroskedasticity diagnostics;
- [x] multicollinearity diagnostics;
- [x] department-by-covariate interaction checks;
- [x] adjusted department estimates with uncertainty;
- [x] explicit model warnings and alternative-model guidance;
- [x] machine-readable and human-readable analysis command;
- [x] synthetic failure-condition tests and CI smoke test;
- [ ] management-facing dashboard or richer report visualisation.

## Phase 3 — Adaptive routing

Goal: test whether historical outcome data can improve routing recommendations.

- policy candidates;
- train/validation split based on time;
- offline counterfactual limitations documented;
- human approval for policy changes;
- model / rule versioning;
- rollback path.

## Phase 4 — Longitudinal models

Goal: investigate recurrence, seasonality and escalation trajectories.

Do not assume an LSTM is necessary. Compare simple baselines, survival/time-to-event approaches, tree models and sequence models using the same evaluation protocol.

Longitudinal model work remains blocked for real private data until the cross-cutting pilot governance items above are completed. Synthetic experiments may continue under the development policy.
