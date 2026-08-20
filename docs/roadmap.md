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
- [ ] continuous integration

## Phase 1 — Service-intelligence MVP

Goal: accept a real request and produce a structured, reviewable routing recommendation.

- request/response API contract;
- issue taxonomy;
- baseline text classifier;
- urgency/context extraction interface;
- persistence layer;
- routing decision audit log;
- manual override / correction capture;
- evaluation dataset for classifier and router.

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
