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

## Phase 2 — Outcome analytics

Goal: evaluate service outcomes credibly.

- pre-specified analytical questions;
- ANCOVA / regression workflow;
- assumption diagnostics;
- missing-data policy;
- adjusted group comparisons;
- technical and management-friendly reports.

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
