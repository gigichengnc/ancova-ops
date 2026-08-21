# Release Readiness — ReasonedOps v1.1.0

ReasonedOps distinguishes four different meanings of "ready":

1. **research-project ready** — the finite Operate → Audit → Evaluate prototype is complete, reproducible, and reviewable;
2. **citation/archive ready** — machine-readable software metadata exists for GitHub/archive tooling;
3. **pilot ready** — approved to process real private service data in a controlled study;
4. **production ready** — approved to operate as a real service-routing system.

The research project was completed at v1.0.0. v1.1.0 is a naming/package migration from **ANCOVA Ops** to **ReasonedOps** and does not increase the empirical evidence class.

## Research-project readiness

- [x] Operate → Audit → Evaluate architecture is explicit;
- [x] explainable request routing is implemented;
- [x] human confirmation/override does not erase original machine history;
- [x] outcomes are stored separately from routing decisions;
- [x] raw and adjusted outcome summaries are separated;
- [x] department/case-type overlap and design identifiability are checked before adjusted ranking;
- [x] unsupported comparisons can be withheld;
- [x] known-effect recovery, measured-confounding adjustment, no-overlap refusal, and slope-interaction behaviour are tested on synthetic scenarios;
- [x] method applicability returns `use`, `caution`, `reject`, or `recommend_alternative`;
- [x] incompatible outcomes/questions are redirected instead of being forced through ANCOVA;
- [x] management reports surface applicability and interpretation boundaries;
- [x] the one-command showcase presents Operate → Audit → Evaluate;
- [x] Python 3.11 and 3.12 CI coverage exists;
- [x] synthetic/private-data governance boundary remains executable;
- [x] adaptive-policy research remains separate from live routing;
- [x] sequence/LSTM work remains deferred until justified;
- [x] Apache-2.0 licensing and CFF citation metadata are present.

## v1.1 naming/package readiness

- [x] canonical project name: `ReasonedOps`;
- [x] repository: `gigichengnc/reasoned-ops`;
- [x] distribution: `reasoned-ops`;
- [x] canonical package: `reasoned_ops`;
- [x] public CLI prefix: `reasoned-`;
- [x] README and `CITATION.cff` use ReasonedOps;
- [x] package URLs point to the renamed repository;
- [x] CI smoke commands use the new CLI surface;
- [x] legacy `ancova_ops` namespace is explicitly treated as temporary compatibility, not the canonical API;
- [x] historical changelog entries preserve the former name intentionally.

## Citation/archive readiness

Repository-side citation readiness is complete. External publication steps remain optional:

- [ ] connect the repository owner account to Zenodo;
- [ ] archive a release and verify the DOI;
- [ ] add the verified DOI back to `CITATION.cff`;
- [ ] optionally add PyPI trusted publishing after package-build/distribution checks exist.

A DOI or PyPI package would improve distribution/citation, not empirical validation.

## Pilot readiness

A real private-data pilot still requires, at minimum:

- jurisdiction-specific privacy/legal review;
- documented purpose and data-use basis;
- notice/consent design where required;
- retention and deletion schedule;
- pseudonymisation/identity-linkage design;
- authenticated staff identities and RBAC;
- secure storage and secrets management;
- correction/deletion procedures;
- incident/breach response;
- external model/provider data-processing review where relevant;
- real-data annotation and outcome-quality protocol;
- pilot monitoring and stop criteria.

**Pilot status: NOT READY / NOT APPROVED.**

## Production readiness

Production additionally requires representative real-data validation, deployment architecture, authenticated APIs, observability, backups/recovery, security testing, change control, rollback/fallback procedures, and operational acceptance criteria.

**Production status: NOT READY / NOT APPROVED.**

## Claims allowed at v1.1.0

Acceptable:

> ReasonedOps is a completed evidence-aware service-operations research prototype built around Operate → Audit → Evaluate. It supports explainable routing, auditable human review, guarded outcome evaluation, and explicit refusal or redirection when a comparison/method is not supportable.

Not acceptable without new evidence:

> ReasonedOps improves real service resolution time, routing accuracy, satisfaction, or staff performance.

> ANCOVA proves a department performs better.

> Green CI, Apache-2.0 licensing, or a future DOI makes the software pilot- or production-ready.
