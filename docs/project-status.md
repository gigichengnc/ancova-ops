# Project Status — v0.5.4

ANCOVA Ops v0.5.4 is a reproducible development and research checkpoint covering service-request structuring, explainable routing, outcome analysis, offline adaptive-policy research and synthetic longitudinal modelling, with a reviewer-facing one-command showcase, polished GitHub storefront, Apache-2.0 licensing and machine-readable citation metadata.

It is **not** a production deployment and is **not** approved for real private resident/customer data.

## Capability map

| Area | Status | Primary command / interface | Evidence class |
| --- | --- | --- | --- |
| Portfolio showcase | Implemented | `ancova-showcase` | Aggregates existing development evidence |
| Request intelligence and routing | Implemented | `uvicorn ancova_ops.api:app --reload` | Transparent development rules |
| Routing audit and human override | Implemented | API case/review endpoints | Local development persistence |
| Routing benchmark | Implemented | `ancova-evaluate` | Hand-authored fixture |
| Data-governance validation | Implemented | `ancova-governance-check` | Machine-readable development policy |
| ANCOVA / regression analysis | Implemented | `ancova-analyze` | Synthetic outcome data |
| Management outcome report | Implemented | `ancova-management-report` | Synthetic outcome data |
| Adaptive-routing offline study | Implemented | `ancova-policy evaluate` | Synthetic logged-policy data |
| Policy approval / rollback registry | Implemented locally | `ancova-policy approve`, `activate`, `rollback` | Development lifecycle control |
| Longitudinal recurrence benchmark | Implemented | `ancova-longitudinal` | Synthetic longitudinal histories |
| Repository licensing | Implemented | `LICENSE`, package metadata | Apache-2.0 for repository-licensed ANCOVA Ops material |
| Citation metadata | Implemented | `CITATION.cff` | CFF 1.2.0; no DOI minted yet |
| LSTM / sequence model | Deferred | none | Not justified by current benchmark |
| Real private-data pilot | Blocked | none | Requires separate governance approval |
| Production adaptive routing | Blocked | none | Requires real-data validation and deployment controls |

## What v0.5.4 demonstrates

1. An unstructured service request can be converted into a structured, explainable routing recommendation with versioned implementation metadata.
2. Human review can confirm or override routing without erasing the original machine/rule recommendation.
3. Outcomes can be stored separately from predictions and analysed with case-mix adjustment rather than raw rankings alone.
4. Statistical diagnostics and uncertainty are surfaced before adjusted comparisons are interpreted.
5. Candidate routing policies can be evaluated offline with time-aware validation and support-aware inverse-propensity methods without silently treating logged outcomes as counterfactual truth.
6. Longitudinal recurrence modelling can be benchmarked with leakage controls and simpler references before sequence-model complexity is considered.
7. Data-governance boundaries are executable in CI rather than existing only as prose.
8. An external reviewer can run one command and inspect the Phase 1–4 evidence chain without manually assembling outputs from separate commands.
9. Reuse terms for ANCOVA Ops repository material are explicit through Apache-2.0.
10. Repository presentation and formal release metadata are synchronised without changing the underlying evidence class.
11. GitHub and archival services can consume one `CITATION.cff` source for title, author, version, license, repository and software-description metadata.

## What v0.5.4 does not demonstrate

- real-world routing accuracy;
- causal improvement in service outcomes;
- production reliability or security;
- validated psychological/emotional measurement;
- safe use of real resident/customer histories;
- evidence that adaptive routing outperforms the baseline in a real deployment;
- evidence that an LSTM or other sequence model is needed;
- any new real-world evidence merely because the portfolio showcase aggregates existing outputs;
- any relicensing of third-party dependencies under Apache-2.0;
- pilot or production readiness merely because the repository is open-source licensed or polished for external review;
- a Zenodo DOI until a Zenodo software record is actually created;
- peer review merely because a DOI or archival record may later exist.

## Command surface

```bash
# One-command portfolio view
ancova-showcase

# Test and development
pytest
python -m ancova_ops.demo

# API
uvicorn ancova_ops.api:app --reload

# Phase 1 routing evaluation
ancova-evaluate
ancova-evaluate --json

# Governance
ancova-governance-check
ancova-governance-check --json

# Phase 2 analytics
ancova-analyze
ancova-analyze --json
ancova-management-report

# Phase 3 adaptive-routing research
ancova-policy evaluate
ancova-policy evaluate --register
ancova-policy status

# Phase 4 longitudinal benchmark
ancova-longitudinal
ancova-longitudinal --json
```

## Evidence hierarchy

The repository deliberately separates evidence classes:

1. **Hand-authored fixture results** — useful for deterministic software regression testing, not population performance estimates.
2. **Synthetic outcome results** — useful for validating statistical and reporting workflows, not real service claims.
3. **Synthetic logged-policy results** — useful for validating offline policy-evaluation mechanics, not production counterfactual evidence.
4. **Synthetic longitudinal results** — useful for model-comparison and leakage testing, not resident/customer forecasting claims.
5. **Portfolio showcase output** — an aggregation of classes 1–4, not a higher evidence class.
6. **Citation/archive metadata** — makes software easier to identify and cite, but does not increase the empirical evidence class.
7. **Real pilot evidence** — not present in v0.5.4 and cannot be implied from the earlier classes.

## Citation and archiving

The root `CITATION.cff` file uses Citation File Format 1.2.0 and records the public software title, author name, version, release date, Apache-2.0 license, repository URL, abstract and keywords. The project intentionally does not invent a DOI, ORCID, email address or affiliation.

A `.zenodo.json` file is not maintained at this checkpoint because Zenodo would give it precedence over `CITATION.cff`; there is currently no concrete Zenodo-specific grants/community requirement that justifies duplicate metadata. See `docs/citation.md` for the integration and DOI follow-up workflow.

## Licensing

ANCOVA Ops repository material distributed under the project license is licensed under the Apache License 2.0. The SPDX identifier in project metadata is `Apache-2.0`; the canonical license text is stored in the root `LICENSE` file.

Third-party dependencies and any separately identified third-party material remain subject to their own licences and notices. A separate notices file should be introduced when incorporated/adapted material creates an actual notice-preservation obligation rather than as a speculative placeholder.

## Current blockers before a real pilot

A real-data pilot must not start until the project has an approved jurisdiction/privacy review, notice/consent design where applicable, access-control model, retention and deletion schedule, pseudonymisation/linkage design, operational authentication, incident process and a documented method for validating labels and outcomes.

Any external AI/model provider used with private request content would also require an approved data-processing configuration, provider/region/retention review and prompt minimisation plan.

## Current blockers before production deployment

Production deployment additionally requires real-data validation, authenticated actor identities, RBAC, secrets management, deployment environments, monitoring/alerting, audit retention, rollback/runbook testing, availability/recovery targets and an explicit decision on how approved adaptive policies would integrate with the operational `/v1/route` path.

## Version

Project metadata, the Python package, the portfolio showcase report version and `CITATION.cff` all report `0.5.4`. CI contains regression tests that fail if those versions, the registered CLI surface, Apache-2.0 metadata or core citation metadata drift apart.
