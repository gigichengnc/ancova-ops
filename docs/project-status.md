# Project Status — ReasonedOps v1.1.0

ReasonedOps is the renamed continuation of the completed v1 research/portfolio prototype formerly called **ReasonedOps**.

> **Operate → Audit → Evaluate**

Its purpose is not to make management decisions automatically. Its purpose is to make unsupported management conclusions harder to reach by preserving decision history, separating descriptive from adjusted evidence, checking whether comparisons are supportable, and refusing or redirecting inappropriate analytical methods.

**Research-project status: COMPLETED.**  
**Current naming/package checkpoint: v1.1.0.**  
**Real private-data pilot: NOT APPROVED.**  
**Production deployment: NOT APPROVED.**

## Canonical identity

| Surface | Canonical v1.1 name |
| --- | --- |
| Project | `ReasonedOps` |
| Repository | `gigichengnc/reasoned-ops` |
| Python distribution | `reasoned-ops` |
| Python package | `reasoned_ops` |
| CLI prefix | `reasoned-` |
| Legacy compatibility namespace | `reasoned_ops` |

Historical release notes before v1.1.0 intentionally retain the former name and old command names.

## Capability map

| Layer / area | Status | Primary command / interface | Evidence class |
| --- | --- | --- | --- |
| Operate — request intelligence and routing | Complete research workflow | `uvicorn reasoned_ops.api:app --reload` | Transparent development rules |
| Operate — routing benchmark | Complete | `reasoned-evaluate` | Hand-authored fixture |
| Audit — immutable case/routing history | Complete | case/history API | Local development persistence |
| Audit — human confirmation / override | Complete | routing-review API | Human feedback, not automatic ground truth |
| Audit — outcome capture | Complete | outcome API | Local development records |
| Evaluate — raw outcome summaries | Complete | `reasoned-management-report` | Synthetic outcomes |
| Evaluate — overlap / identifiability gate | Complete | `reasoned-analyze` | Synthetic outcomes |
| Evaluate — known-truth validity benchmark | Complete | `reasoned-validity` | Synthetic validity scenarios |
| Evaluate — method applicability gate | Complete | `reasoned-applicability` | Deterministic decision rules |
| Evaluate — regression / ANCOVA | Complete | `reasoned-analyze` | Synthetic outcomes |
| Evaluate — offline adaptive-policy study | Complete research workflow | `reasoned-policy evaluate` | Synthetic logged-policy data |
| Evaluate — longitudinal recurrence benchmark | Complete research workflow | `reasoned-longitudinal` | Synthetic histories |
| Governance validation | Complete | `reasoned-governance-check` | Machine-readable development policy |
| End-to-end showcase | Complete | `reasoned-showcase` | Aggregates existing development evidence |
| Apache-2.0 licensing | Complete | `LICENSE` | Repository licensing |
| Citation metadata | Complete | `CITATION.cff` | CFF 1.2.0; no unverified DOI |
| Sequence/LSTM model | Deferred by design | none | Not justified by current benchmark |
| Real private-data pilot | Post-v1 / blocked | none | Separate governance approval required |
| Production deployment | Post-v1 / blocked | none | Real-data, security and operational evidence required |

## Evaluation architecture

ReasonedOps separates two questions:

1. **Can this comparison be supported?** Department × case-type overlap and design-identifiability checks return `supported`, `weak_overlap`, or `not_identifiable`. A `not_identifiable` comparison withholds adjusted estimates and ranking language.
2. **Is this the right method family?** `reasoned-applicability` returns `use`, `caution`, `reject`, or `recommend_alternative` based on the declared outcome, censoring, clustering, causal intent, routing-policy question, overlap and interaction warnings.

ANCOVA/regression is therefore one method inside the Evaluate layer. It is not the product identity and is not forced onto incompatible questions.

## Evidence boundary

Current evidence remains deliberately limited to:

1. hand-authored routing fixtures;
2. synthetic outcome data;
3. synthetic known-truth validity scenarios;
4. deterministic applicability rules;
5. synthetic logged-policy data;
6. synthetic longitudinal histories.

There is **no representative real-pilot evidence** in v1.1.0.

## What the project demonstrates

ReasonedOps demonstrates a reproducible architecture that can:

- structure and route service requests transparently;
- preserve machine and human decision history;
- capture observed outcomes separately;
- distinguish raw summaries from adjusted evidence;
- refuse unsupported comparisons;
- redirect questions to more appropriate method families;
- keep offline policy and longitudinal research separate from live operational routing;
- keep evidence provenance and deployment boundaries explicit.

It does **not** demonstrate real-world service improvement, causal staff/department effects, production security/reliability, or approval to process real private resident/customer histories.

## Project freeze

Further modelling is post-v1 work and should require a concrete user, competition requirement, research question, reuse request, or pilot opportunity. More code by itself is not evidence that the project is more useful.
