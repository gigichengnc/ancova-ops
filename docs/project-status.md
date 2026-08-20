# Project Status — v0.6.0

ANCOVA Ops v0.6.0 is an evidence-aware service-operations research/software checkpoint organised around three functions:

> **Operate → Audit → Evaluate**

Its purpose is not to make management decisions automatically. Its purpose is to make unsupported management conclusions harder to reach by preserving decision history, separating raw summaries from adjusted analysis, and withholding comparisons when the observed data cannot support them.

It remains a development/research prototype. It is **not** approved for real private resident/customer data and is **not** a production deployment.

## Capability map

| Layer / area | Status | Primary command / interface | Evidence class |
| --- | --- | --- | --- |
| Operate — request intelligence and routing | Implemented | `uvicorn ancova_ops.api:app --reload` | Transparent development rules |
| Operate — routing benchmark | Implemented | `ancova-evaluate` | Hand-authored fixture |
| Audit — immutable case/routing history | Implemented | case/history API | Local development persistence |
| Audit — human confirmation / override | Implemented | routing-review API | Human feedback, not automatic ground truth |
| Audit — outcome capture | Implemented | outcome API | Local development records |
| Evaluate — raw outcome summaries | Implemented | `ancova-management-report` | Synthetic outcomes |
| Evaluate — department/issue-category overlap | Implemented | `ancova-analyze` | Synthetic outcomes |
| Evaluate — identifiability gate | Implemented | `ancova-analyze` | Synthetic outcomes |
| Evaluate — regression / ANCOVA | Implemented | `ancova-analyze` | Synthetic outcomes |
| Evaluate — known-truth validity benchmark | Implemented | `ancova-validity` | Synthetic validity scenarios |
| Evaluate — management report with blocked/withheld state | Implemented | `ancova-management-report` | Synthetic outcomes |
| Evaluate — offline adaptive-policy study | Implemented | `ancova-policy evaluate` | Synthetic logged-policy data |
| Evaluate — longitudinal recurrence benchmark | Implemented | `ancova-longitudinal` | Synthetic histories |
| Data-governance validation | Implemented | `ancova-governance-check` | Machine-readable development policy |
| Portfolio showcase | Implemented | `ancova-showcase` | Aggregates existing development evidence |
| Repository licensing | Implemented | `LICENSE`, project metadata | Apache-2.0 |
| Citation metadata | Implemented | `CITATION.cff` | CFF 1.2.0; no unverified DOI |
| Sequence/LSTM model | Deferred | none | Not justified by current benchmark |
| Real private-data pilot | Blocked | none | Separate governance approval required |
| Production deployment | Blocked | none | Real-data, security and operational evidence required |

## What v0.6.0 adds

v0.6.0 changes the outcome-analysis layer from "fit an ANCOVA model" to "check whether the comparison is supportable, then fit an appropriate development model only when the design allows it."

The default continuous-outcome example now includes issue category as a measured case-mix factor:

```text
resolution_hours
~ C(department)
+ C(issue_category)
+ urgency
+ frustration
+ complexity
+ previous_related_cases
```

Before adjusted department estimates are published, the workflow evaluates department × issue-category overlap, graph connectivity and design-matrix rank.

The result is classified as:

- `supported` — structurally identifiable with practical overlap at the configured threshold;
- `weak_overlap` — structurally estimable but practically thin;
- `not_identifiable` — department and issue category cannot be separated from the observed design.

When the result is `not_identifiable`, adjusted department estimates, department ANOVA results and management-facing adjusted rankings are withheld.

## v0.6.0 validity benchmark

`ancova-validity` tests four synthetic known-truth scenarios:

1. known department contrasts are recovered within a pre-specified tolerance when overlap exists;
2. measured case-mix adjustment materially reduces deliberately induced confounding bias relative to a naive model;
3. a deterministic no-overlap routing design is rejected rather than ranked;
4. a deliberately department-specific covariate slope is detected by interaction screening.

These scenarios validate software behaviour under known synthetic conditions. They do not validate real operational performance.

## What v0.6.0 demonstrates

1. Unstructured service requests can be converted into structured, explainable routing recommendations.
2. Human review can confirm or override routing without erasing the original machine/rule recommendation.
3. Outcomes can be stored separately from routing decisions.
4. Raw outcome differences can be kept separate from model-adjusted estimates.
5. Measured issue type can be included as case mix rather than silently conflated with department performance.
6. The analysis can detect when department and issue type are not separately identifiable.
7. Unsupported adjusted rankings can be withheld rather than manufactured.
8. Known synthetic department contrasts can be used to test coefficient/contrast recovery.
9. A deliberately confounded scenario can show whether measured case-mix adjustment reduces bias relative to a naive model.
10. Interaction, variance, multicollinearity, influence and missingness diagnostics remain visible.
11. Offline policy and longitudinal research remain separated from operational routing.
12. Data-governance boundaries remain executable in CI.

## What v0.6.0 does not demonstrate

- real-world routing accuracy;
- causal improvement in service outcomes;
- causal department or staff performance differences;
- production reliability, availability or security;
- safe use of real private resident/customer histories;
- absence of unmeasured confounding;
- that every continuous outcome should be analysed with ANCOVA;
- that a binary, censored, clustered or repeated-measures outcome can be handled by the current ANCOVA path;
- that the adaptive policy is better than the baseline in a real deployment;
- that a sequence/LSTM model is necessary;
- pilot or production readiness merely because the repository is licensed, citable or statistically careful.

## Current command surface

```bash
# End-to-end reviewer view
ancova-showcase

# Operate / routing benchmark
ancova-evaluate
ancova-evaluate --json

# Governance
ancova-governance-check
ancova-governance-check --json

# Evaluate / outcome analysis
ancova-analyze
ancova-analyze --json
ancova-management-report

# Evaluate / known-truth validity
ancova-validity
ancova-validity --json

# Evaluate / adaptive-policy research
ancova-policy evaluate
ancova-policy status

# Evaluate / longitudinal benchmark
ancova-longitudinal
ancova-longitudinal --json
```

## Evidence hierarchy

The repository deliberately separates evidence classes:

1. **Hand-authored fixture results** — deterministic routing regression tests, not population estimates.
2. **Synthetic outcome results** — statistical/reporting workflow validation, not real service claims.
3. **Synthetic validity scenarios** — known-truth tests of recovery, confounding adjustment, no-overlap refusal and interaction detection.
4. **Synthetic logged-policy results** — offline policy-evaluation mechanics, not production counterfactual evidence.
5. **Synthetic longitudinal results** — model-comparison/leakage testing, not customer forecasting claims.
6. **Portfolio showcase output** — aggregation of existing development evidence, not a higher evidence class.
7. **Citation/archive metadata** — makes software identifiable/citable but does not increase empirical evidence.
8. **Real pilot evidence** — not present in v0.6.0.

## Remaining research-project work before v1.0

The main remaining project task is a compact **evaluation applicability gate** that makes method-selection boundaries explicit. It should be able to return outcomes such as:

- `use` — the current continuous-outcome regression/ANCOVA path is plausible;
- `caution` — the method may be usable but assumptions or support need attention;
- `reject` — the requested comparison is not supportable from the declared data structure;
- `recommend_alternative` — a binary, censored, clustered or other outcome needs a different analysis family.

v1.0 does not need to implement every alternative statistical model. It needs to refuse or redirect inappropriate use rather than forcing ANCOVA because of the project name.

## Pilot and production boundary

A real-data pilot remains blocked until privacy/legal review, notice/consent requirements where applicable, access control, retention/deletion, pseudonymisation/linkage, incident handling, external provider review and real-data quality protocols are approved.

Production additionally requires authenticated identities, RBAC, secrets management, deployment environments, observability, recovery targets, security testing, change control, rollback/fallback procedures and real-world validation.

These are post-research-project deployment gates and do not need to be completed for the v1.0 research prototype to be considered finished.

## Version

Project metadata, package `__version__`, `CITATION.cff` and the registered command surface target `0.6.0`. CI regression checks are expected to fail if these drift.
