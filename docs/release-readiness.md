# Release Readiness — v0.6.0

ANCOVA Ops distinguishes four different meanings of "ready":

1. **research-repository ready** — another developer can clone, install, test and understand the prototype;
2. **citation/archive ready** — machine-readable software metadata is available for GitHub and archival services;
3. **pilot ready** — approved to process real private service data in a controlled study;
4. **production ready** — approved to operate as a real service-routing system.

v0.6.0 targets the first category and the repository-side portion of the second category only.

## Research-repository readiness

- [x] Operate → Audit → Evaluate architecture is explicit;
- [x] explainable request routing and human override are implemented;
- [x] original machine/rule decisions remain auditable after human review;
- [x] outcomes are stored separately from routing decisions;
- [x] raw and adjusted outcome summaries are separated;
- [x] issue category is included as measured case mix in the default continuous-outcome model;
- [x] department × issue-category overlap is reported;
- [x] design identifiability is checked before adjusted rankings are published;
- [x] `not_identifiable` comparisons withhold adjusted estimates and department ANOVA output;
- [x] management reports display a blocked/withheld state rather than manufacturing a ranking;
- [x] adjusted means are standardised over observed complete-case case mix when estimable;
- [x] known-effect recovery is tested on synthetic data;
- [x] measured-confounding adjustment is compared against a deliberately naive model;
- [x] no-overlap refusal is tested;
- [x] slope-interaction detection is tested;
- [x] missingness, heteroskedasticity, multicollinearity and influence diagnostics remain visible;
- [x] `ancova-validity` is registered as a CLI workflow;
- [x] Python 3.11 and 3.12 CI coverage exists;
- [x] lint, unit tests and major workflow smoke tests are part of CI;
- [x] synthetic/private-data governance boundary is executable in CI;
- [x] adaptive-policy research remains separate from the live routing path;
- [x] sequence/LSTM work remains explicitly deferred;
- [x] Apache-2.0 licensing and CFF citation metadata are present.

The release should not be tagged until the v0.6.0 pull request passes the full Python 3.11/3.12 CI matrix on the final head commit.

## Statistical/evaluation boundary

v0.6.0 validates behaviour of the current continuous-outcome evaluation path on known synthetic scenarios. It does not prove that the method is appropriate for every outcome or every service dataset.

The current default path is only a candidate when:

- the outcome is compatible with the regression formulation;
- department and case type are sufficiently separable to support the comparison;
- the declared case mix is measured before the outcome and is substantively defensible;
- diagnostics do not reveal a reason to replace the common-slope model;
- the intended interpretation remains associational unless a stronger design is separately justified.

The remaining v1.0 research-project task is an explicit applicability gate that can return `use`, `caution`, `reject`, or `recommend_alternative` instead of forcing ANCOVA onto incompatible questions.

## Citation and archive readiness

Repository-side citation readiness:

- [x] root `CITATION.cff` uses CFF 1.2.0;
- [x] title, public author name, version, release date, license and repository URL are recorded;
- [x] no fabricated DOI, ORCID, email address or affiliation;
- [x] `.zenodo.json` remains absent while no Zenodo-specific metadata requires a second source;
- [x] DOI follow-up process is documented in `docs/citation.md`.

External account steps remain optional publication/distribution work:

- [ ] connect the repository owner account to Zenodo;
- [ ] enable `gigichengnc/ancova-ops`;
- [ ] archive a release and verify the DOI;
- [ ] add the verified DOI back to `CITATION.cff` in a later reviewed checkpoint;
- [ ] optionally add PyPI trusted publishing after package-build/distribution checks exist.

A DOI or PyPI package does not increase the empirical evidence class.

## Pilot readiness

The following remain intentionally incomplete:

- [ ] jurisdiction-specific privacy/legal review;
- [ ] documented operational purpose and lawful/data-use basis for each private field;
- [ ] notice and consent design where required;
- [ ] concrete retention and deletion schedule;
- [ ] pseudonymisation and identity-linkage design;
- [ ] authenticated staff identities and role-based access control;
- [ ] secure pilot storage and secrets management;
- [ ] deletion/correction request procedure;
- [ ] incident response and breach-handling process;
- [ ] external AI/model-provider data-processing review if private text leaves the controlled environment;
- [ ] real-data annotation and outcome-quality protocol;
- [ ] pilot monitoring and stop criteria.

**Pilot status: NOT READY / NOT APPROVED.**

## Production readiness

Production requires all pilot controls plus:

- [ ] representative real-data routing benchmark;
- [ ] real-data outcome-analysis validation;
- [ ] defensible prospective or counterfactual evaluation of policy impact;
- [ ] deployment architecture and environment separation;
- [ ] authenticated API access and authorization;
- [ ] observability, monitoring and alerting;
- [ ] uptime, recovery and backup objectives;
- [ ] security testing and dependency-management process;
- [ ] policy activation runbook and rollback drill;
- [ ] explicit policy-registry integration contract for `/v1/route`;
- [ ] human escalation and manual fallback procedure;
- [ ] model/rule change-control ownership;
- [ ] production data-retention and audit-retention controls;
- [ ] operational acceptance criteria approved by the service owner.

**Production status: NOT READY / NOT APPROVED.**

## Claims allowed at v0.6.0

Acceptable wording:

> ANCOVA Ops v0.6.0 is an evidence-aware service-operations research prototype that supports explainable routing, auditable human review and outcome evaluation. Its synthetic validity benchmark checks known-effect recovery, measured-confounding adjustment, no-overlap refusal and slope-interaction detection, and it withholds adjusted department rankings when the observed design cannot separate department from case type.

Not acceptable without new evidence:

> ANCOVA Ops improves real service resolution time, routing accuracy or satisfaction.

> ANCOVA proves a department or staff group performs better.

> Passing the synthetic validity benchmark proves real-world accuracy or causality.

> A statistically significant adjusted department term proves that changing a route will improve the outcome.

> A Zenodo DOI, Apache-2.0 license or green CI makes the software pilot- or production-ready.

## Research-project completion rule

For the **v1.0 research/portfolio project**, real private-data pilot controls and production infrastructure are explicitly out of scope.

The project can be considered complete when:

1. v0.6.0 validity behaviour is green in CI;
2. the final applicability gate refuses or redirects inappropriate evaluation questions;
3. the showcase and README present Operate → Audit → Evaluate consistently;
4. the final v1.0 regression suite is green;
5. evidence/governance boundaries remain explicit.

After that point, new modelling or deployment work should require a concrete user, competition requirement, research question or pilot opportunity rather than being added merely because more features are possible.
