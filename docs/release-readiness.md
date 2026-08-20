# Release Readiness — v1.0.0

ANCOVA Ops distinguishes four different meanings of "ready":

1. **research-project ready** — the finite Operate → Audit → Evaluate prototype is complete, reproducible and reviewable;
2. **citation/archive ready** — machine-readable software metadata exists for GitHub/archive tooling;
3. **pilot ready** — approved to process real private service data in a controlled study;
4. **production ready** — approved to operate as a real service-routing system.

v1.0.0 completes category 1 and the repository-side portion of category 2 only.

## Research-project readiness

- [x] Operate → Audit → Evaluate architecture is explicit;
- [x] explainable request routing is implemented;
- [x] human confirmation/override does not erase original machine history;
- [x] outcomes are stored separately from routing decisions;
- [x] raw and adjusted outcome summaries are separated;
- [x] issue category is included as measured case mix in the continuous-outcome example;
- [x] department × issue-category overlap is reported;
- [x] design identifiability is checked before adjusted ranking;
- [x] `not_identifiable` comparisons withhold adjusted estimates and department ANOVA output;
- [x] management reports show blocked/withheld results instead of manufacturing a ranking;
- [x] adjusted means are standardised over observed complete-case case mix when estimable;
- [x] known-effect recovery is tested on synthetic data;
- [x] measured-confounding adjustment is compared with a deliberately naive model;
- [x] no-overlap refusal is tested;
- [x] common-slope violations are tested;
- [x] evaluation applicability returns `use`, `caution`, `reject`, or `recommend_alternative`;
- [x] binary outcomes are redirected to a logistic-type family;
- [x] censored/time-to-event outcomes are redirected to a survival family;
- [x] repeated/clustered observations are redirected to dependence-aware analysis;
- [x] routing-policy questions are redirected to offline policy evaluation;
- [x] causal intent is not cleared by ordinary observational adjustment;
- [x] management reports surface applicability disposition/method family;
- [x] the one-command showcase presents Operate → Audit → Evaluate and applicability;
- [x] `ancova-applicability` is a registered CLI;
- [x] `ancova-validity` is a registered CLI;
- [x] Python 3.11 and 3.12 CI coverage exists;
- [x] lint, unit tests and all major workflow smoke tests are in CI;
- [x] synthetic/private-data governance remains executable in CI;
- [x] adaptive-policy research remains separated from live routing;
- [x] sequence/LSTM work remains deferred unless evidence justifies it;
- [x] Apache-2.0 licensing and CFF citation metadata are present;
- [x] README/status/roadmap explicitly freeze further research-project feature expansion after v1.

The v1.0.0 release must not be merged/tagged until the final PR head passes the full Python 3.11/3.12 CI matrix.

## Statistical/evaluation boundary

A v1 `use` result means only that the declared question/data structure is compatible with the current method family at a high level. It does not prove:

- the fitted model is true;
- all relevant confounders are measured;
- a department coefficient is causal;
- the result is transportable beyond the supported case mix;
- a staff-performance ranking is justified.

A different method family also cannot repair missing identification. For a department comparison with structural no-overlap, the correct disposition remains `reject`.

## Citation and archive readiness

Repository-side citation readiness:

- [x] root `CITATION.cff` uses CFF 1.2.0;
- [x] public author name, title, version, release date, license and repository URL are recorded;
- [x] no fabricated DOI, ORCID, email address or affiliation;
- [x] `.zenodo.json` remains absent while no Zenodo-specific metadata requires a duplicate source;
- [x] DOI follow-up is documented in `docs/citation.md`.

Optional external publication/distribution work:

- [ ] connect the repository owner account to Zenodo;
- [ ] enable `gigichengnc/ancova-ops`;
- [ ] archive a release and verify the DOI;
- [ ] add a verified DOI back to `CITATION.cff`;
- [ ] optionally add PyPI trusted publishing after package-build/distribution checks exist.

These are **post-v1 opportunities, not unfinished v1 research work**.

## Pilot readiness

The following remain intentionally incomplete and are outside the v1 research-project scope:

- [ ] jurisdiction-specific privacy/legal review;
- [ ] private-field purpose/lawful-use basis;
- [ ] notice/consent design where required;
- [ ] concrete retention/deletion schedule;
- [ ] pseudonymisation and identity linkage;
- [ ] authenticated staff identities and RBAC;
- [ ] secure pilot storage and secrets management;
- [ ] deletion/correction procedure;
- [ ] incident/breach response;
- [ ] external model-provider data-processing review;
- [ ] real-data annotation and outcome-quality protocol;
- [ ] pilot monitoring and stop criteria.

**Pilot status: NOT READY / NOT APPROVED.**

## Production readiness

Production additionally requires:

- [ ] representative real-data routing validation;
- [ ] real-data outcome-analysis validation;
- [ ] defensible evaluation of policy impact;
- [ ] deployment/environment separation;
- [ ] authenticated APIs and authorization;
- [ ] monitoring/alerting;
- [ ] backup/recovery objectives;
- [ ] security/dependency-management process;
- [ ] policy activation and rollback drills;
- [ ] manual escalation/fallback procedures;
- [ ] change-control ownership;
- [ ] production retention/audit controls;
- [ ] service-owner acceptance criteria.

**Production status: NOT READY / NOT APPROVED.**

## Claims allowed at v1.0.0

Acceptable wording:

> ANCOVA Ops v1.0.0 is a completed evidence-aware service-operations research prototype organised around Operate, Audit and Evaluate. It implements explainable routing, auditable human review, outcome capture, synthetic validity tests, department/case-type identifiability checks and an evaluation applicability gate that can use, caution, reject or redirect a declared analytical question.

Not acceptable without new evidence:

> ANCOVA Ops improves real service resolution time, routing accuracy or satisfaction.

> ANCOVA proves a department or staff group performs better.

> Passing synthetic validity/applicability checks proves real-world accuracy or causality.

> A significant adjusted department term proves changing a route will improve outcomes.

> A DOI, Apache-2.0 license, green CI or v1.0 tag makes the system private-data or production ready.

## Research-project completion rule

**The research/portfolio project is complete at v1.0.0 once the final PR head passes CI and the v1 release is created.**

After that point, additional modelling or deployment work is post-v1 and should require a concrete user, competition requirement, research question or pilot opportunity.
