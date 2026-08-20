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

Goal: accept a service request and produce a structured, reviewable routing recommendation.

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
- [x] management-facing Markdown report and structured summary;
- [x] raw-versus-adjusted department comparison;
- [x] management screening dashboard with visible warnings.

## Phase 3 — Adaptive routing

Goal: test whether historical outcome data can improve routing recommendations.

- [x] versioned baseline and transparent outcome-aware policy candidate;
- [x] deterministic synthetic logged-routing history with known action propensities;
- [x] train/validation split based strictly on time;
- [x] support-aware inverse-propensity offline evaluation;
- [x] effective-sample-size and unsupported-action checks;
- [x] offline counterfactual limitations documented;
- [x] explicit human approval required before candidate activation;
- [x] model / rule version registry;
- [x] append-only activation history and rollback path;
- [x] adaptive-routing CLI and CI smoke coverage.

The Phase 3 framework remains offline and synthetic-only. Registry activation does not automatically replace the router used by `/v1/route`. Real pilot evaluation and operational deployment remain blocked by the open cross-cutting governance items.

## Phase 4 — Longitudinal models

Goal: investigate recurrence, seasonality and escalation trajectories without assuming that a sequence model is necessary.

- [x] deterministic synthetic entity-level event histories;
- [x] recurrence feedback and seasonal structure in development data;
- [x] pre-cutoff recency/frequency/context feature snapshots;
- [x] 30-day recurrence target;
- [x] censored time-to-next-case target;
- [x] purged chronological train/validation split;
- [x] explicit feature-time and follow-up leakage checks;
- [x] recency/frequency logistic baseline;
- [x] discrete-time survival/hazard benchmark;
- [x] tree-based recurrence benchmark;
- [x] same-window ROC-AUC, Brier and calibration comparison;
- [x] survival concordance reporting;
- [x] model-complexity incremental-value rule;
- [x] sequence/LSTM work deferred unless a later same-benchmark comparison justifies it;
- [x] longitudinal benchmark CLI, documentation, tests and CI smoke coverage.

The Phase 4 benchmark remains synthetic-only. Real longitudinal personalisation and private service-history modelling remain blocked until the cross-cutting pilot governance items are completed.

## v0.5.x — Project checkpoint and presentation

Goal: make Phases 0–4 understandable, reproducible, clearly licensed and citable as one coherent research/software checkpoint before adding more modelling complexity.

- [x] package and project version alignment with regression coverage;
- [x] changelog;
- [x] current Phase 0–4 architecture map;
- [x] concise project-status document;
- [x] release-readiness checklist separating repository, pilot and production readiness;
- [x] README converted into an external-facing project entry point;
- [x] one-command reviewer showcase (`v0.5.1`);
- [x] Apache License 2.0 selected and declared in root `LICENSE` plus package metadata (`v0.5.2`);
- [x] GitHub storefront polish and CI-gated release flow (`v0.5.3`);
- [x] root `CITATION.cff`, citation guide and citation/version regression checks (`v0.5.4`).

## Publication / distribution gates

These are separate from model-building and do not change the evidence class:

- [ ] connect the repository owner GitHub account to Zenodo;
- [ ] enable `gigichengnc/ancova-ops` in the Zenodo GitHub integration;
- [ ] archive a GitHub software release and verify the minted DOI;
- [ ] add the verified DOI back to `CITATION.cff` in a reviewed checkpoint;
- [ ] optionally add PyPI trusted publishing after package-build and distribution checks are introduced;
- [ ] consider a software paper only after the research-use case, field context and user/reuse evidence justify it.

A DOI is a persistent identifier for a software record, not evidence that the software or its empirical claims have been peer reviewed.

## Next gates — before a real-data pilot

These are governance/evidence gates rather than another model-building phase:

- [ ] jurisdiction-specific privacy/legal review;
- [ ] notice/consent design where applicable;
- [ ] authenticated staff identities and role-based access control;
- [ ] concrete retention/deletion schedule;
- [ ] pseudonymisation and identity-linkage design;
- [ ] secure pilot storage, secrets management and incident process;
- [ ] real-data annotation and outcome-quality protocol;
- [ ] representative real-data routing benchmark and pilot stop criteria.

Only after those gates should the project consider real-data adaptive-policy learning, production integration or a new sequence-model experiment.
