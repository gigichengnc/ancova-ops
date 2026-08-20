# Project Status — v1.0.0

ANCOVA Ops v1.0.0 is the **completed research/portfolio prototype** for an evidence-aware service-operations architecture:

> **Operate → Audit → Evaluate**

Its purpose is not to make management decisions automatically. Its purpose is to make unsupported management conclusions harder to reach by preserving decision history, separating descriptive from adjusted evidence, checking whether comparisons are identifiable, and refusing or redirecting inappropriate analytical methods.

**Research-project status: COMPLETED / FROZEN AT v1.0.0.**

It is still **not approved for real private resident/customer data** and is **not a production deployment**. Those are separate post-v1 stages.

## Capability map

| Layer / area | v1.0 status | Primary command / interface | Evidence class |
| --- | --- | --- | --- |
| Operate — request intelligence and routing | Complete | `uvicorn ancova_ops.api:app --reload` | Transparent development rules |
| Operate — routing benchmark | Complete | `ancova-evaluate` | Hand-authored fixture |
| Audit — immutable case/routing history | Complete | case/history API | Local development persistence |
| Audit — human confirmation / override | Complete | routing-review API | Human feedback, not automatic ground truth |
| Audit — outcome capture | Complete | outcome API | Local development records |
| Evaluate — raw outcome summaries | Complete | `ancova-management-report` | Synthetic outcomes |
| Evaluate — overlap / identifiability gate | Complete | `ancova-analyze` | Synthetic outcomes |
| Evaluate — known-truth validity benchmark | Complete | `ancova-validity` | Synthetic validity scenarios |
| Evaluate — method applicability gate | Complete | `ancova-applicability` | Deterministic decision rules |
| Evaluate — regression / ANCOVA | Complete | `ancova-analyze` | Synthetic outcomes |
| Evaluate — management report with use/caution/reject/alternative | Complete | `ancova-management-report` | Synthetic outcomes + decision rules |
| Evaluate — offline adaptive-policy study | Complete research workflow | `ancova-policy evaluate` | Synthetic logged-policy data |
| Evaluate — longitudinal recurrence benchmark | Complete research workflow | `ancova-longitudinal` | Synthetic histories |
| Data-governance validation | Complete | `ancova-governance-check` | Machine-readable development policy |
| End-to-end v1 showcase | Complete | `ancova-showcase` | Aggregates existing development evidence |
| Apache-2.0 licensing | Complete | `LICENSE` | Repository licensing |
| Citation metadata | Complete | `CITATION.cff` | CFF 1.2.0; no unverified DOI |
| Sequence/LSTM model | Deferred by design | none | Not justified by current benchmark |
| Real private-data pilot | Post-v1 / blocked | none | Separate governance approval required |
| Production deployment | Post-v1 / blocked | none | Real-data, security and operational evidence required |

## Final evaluation architecture

The evaluation layer uses two different gates.

### 1. Can the comparison be supported?

For department outcome comparisons, v0.6 introduced department × issue-category overlap and design-identifiability checks.

Statuses:

- `supported`;
- `weak_overlap`;
- `not_identifiable`.

When department and case type cannot be separated from the observed routing design:

```text
adjusted estimates       = withheld
ANOVA department results = withheld
management ranking       = blocked
```

### 2. Is this the right method family?

v1.0 adds `ancova-applicability`, which returns exactly one disposition:

- `use`;
- `caution`;
- `reject`;
- `recommend_alternative`.

The gate handles declared continuous, binary and time-to-event outcomes; censoring; repeated/clustered observations; causal intent; routing-policy questions; weak/no overlap; and department-specific slope warnings.

Examples:

```text
continuous + supported overlap
→ use regression_ancova_style

weak overlap
→ caution

no overlap
→ reject no_adjusted_department_comparison

binary
→ recommend_alternative logistic_type_model

censored/time-to-event
→ recommend_alternative survival_time_to_event_model

repeated/clustered
→ recommend_alternative clustered_or_hierarchical_model

routing-policy question
→ recommend_alternative offline_policy_evaluation

causal intent
→ recommend_alternative causal_design_and_identification
```

The gate intentionally recommends rather than implements every alternative model family.

## Validity evidence

`ancova-validity` tests four known synthetic scenarios:

1. known-effect recovery under overlapping case mix;
2. measured-confounding adjustment versus a deliberately naive model;
3. no-overlap refusal;
4. detection of a deliberately violated common-slope assumption.

This demonstrates software behaviour on synthetic known-truth scenarios. It does **not** demonstrate real operational effectiveness or causality.

## What v1.0 demonstrates

- unstructured requests can be converted into explainable routing recommendations;
- later human review can change effective routing without erasing machine history;
- outcomes can be captured separately from predictions and reviews;
- raw averages and adjusted evidence can be kept separate;
- issue type can be treated as measured case mix rather than silently conflated with department performance;
- unsupported department comparisons can be withheld;
- inappropriate method families can be rejected or redirected;
- synthetic known-truth scenarios can test recovery, confounding adjustment and refusal behaviour;
- offline policy and longitudinal research can remain separated from live operational routing;
- evidence provenance and deployment boundaries can remain explicit in code, CI and reports.

## What v1.0 does not demonstrate

- real-world routing accuracy or service improvement;
- causal department/staff performance differences;
- absence of unmeasured confounding;
- production reliability, availability or security;
- approval to process real private resident/customer histories;
- that an alternative method recommendation has been fully implemented;
- that the offline adaptive policy should be deployed;
- that a sequence/LSTM model is necessary;
- peer review merely because the repository is citable or may later receive a DOI.

## Command surface

```bash
ancova-evaluate
ancova-governance-check
ancova-analyze
ancova-management-report
ancova-validity
ancova-applicability
ancova-policy
ancova-longitudinal
ancova-showcase
```

## Evidence hierarchy

1. Hand-authored routing fixture — software regression evidence, not population performance.
2. Synthetic outcome data — analysis/reporting workflow evidence.
3. Synthetic validity scenarios — known-truth evaluation behaviour.
4. Deterministic applicability rules — method-selection/refusal behaviour.
5. Synthetic logged-policy data — offline policy research mechanics.
6. Synthetic longitudinal histories — leakage-aware model-comparison mechanics.
7. Showcase output — aggregation of existing evidence, not a new evidence class.
8. Real pilot evidence — **not present in v1.0.0**.

## Project freeze

The following are now **post-v1 opportunities, not unfinished research-project work**:

- real-organisation pilot work;
- privacy/legal and private-data approval;
- production authentication/RBAC/security/monitoring;
- new statistical model families;
- deeper LLM request intelligence;
- PyPI distribution;
- Zenodo DOI archiving;
- software-paper submission;
- competition-specific extensions.

Further modelling should require a concrete user, competition requirement, research question or pilot opportunity rather than being added simply because additional complexity is possible.

## Pilot and production boundary

A real-data pilot remains blocked until privacy/legal review, notice/consent where applicable, access control, retention/deletion, pseudonymisation/linkage, incident handling, external-provider review and real-data quality protocols are approved.

Production additionally requires real-world validation, authenticated identities, authorization, secure deployment, secrets management, monitoring, recovery, security testing, change control, rollback/fallback procedures and operational acceptance.

## Version

Project metadata, package `__version__`, `CITATION.cff`, showcase version and registered CLI surface target `1.0.0`. CI contains regression checks to prevent version and command-surface drift.
