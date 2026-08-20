# ANCOVA Ops

[![CI](https://github.com/gigichengnc/ancova-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/gigichengnc/ancova-ops/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/gigichengnc/ancova-ops?display_name=tag)](https://github.com/gigichengnc/ancova-ops/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

**Evidence-aware service operations: Operate → Audit → Evaluate.**

ANCOVA Ops is a completed v1.0 research/software prototype for turning unstructured service requests into explainable operational recommendations, preserving human and machine decision history, recording outcomes, and testing whether management conclusions are actually supported by the available data.

> **It is not designed to make management decisions. It is designed to make unsupported management conclusions harder to reach.**

The project originated from an HKMU Hackathon 2026 concept. Property management is the first use case, not the product boundary. ANCOVA is one evaluation method inside the system rather than the product itself.

## v1.0 status

| Reviewer question | Current answer |
| --- | --- |
| Research/portfolio project | **COMPLETED / FROZEN at v1.0.0** |
| Core architecture | **Operate → Audit → Evaluate** |
| Fastest end-to-end demo | `ancova-showcase` |
| Evaluation validity benchmark | `ancova-validity` |
| Method applicability gate | `ancova-applicability` |
| Evidence class | Synthetic data + a small hand-authored routing fixture |
| Real private-data pilot | **Not approved** |
| Production deployment | **Not approved** |
| License | Apache-2.0 |
| Citation | Root `CITATION.cff`; no DOI claimed until independently verified |

Current quantitative outputs are development evidence. They are not real-world service-improvement claims, causal department rankings or production-readiness evidence.

## Operate → Audit → Evaluate

| Layer | What ANCOVA Ops does | v1.0 status |
| --- | --- | --- |
| **Operate** | Structure service requests, extract transparent operational signals and recommend an explainable route | Complete for research prototype |
| **Audit** | Preserve original request, machine/rule decision, human confirmation or override, implementation version and observed outcome | Complete for research prototype |
| **Evaluate** | Check whether a question/comparison is supportable, choose or recommend an analysis family, separate raw from adjusted evidence, surface uncertainty and withhold unsupported rankings | Complete for research prototype |

```text
Service request
      |
      v
Request intelligence
      |
      v
Explainable routing recommendation
      |
      +--> Human confirmation / override
      |
      v
Observed outcome
      |
      v
Auditable decision history
      |
      v
Descriptive summaries
      |
      v
Comparison support / identifiability
      |
      v
Evaluation applicability gate
      |
      +--> USE
      +--> CAUTION
      +--> REJECT
      +--> RECOMMEND_ALTERNATIVE
```

## One-command showcase

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
ancova-showcase
```

This writes:

```text
.ancova_ops/showcase/showcase.md
```

The v1 showcase presents the full **Operate → Audit → Evaluate** chain, including the evaluation applicability decision, while preserving the synthetic/hand-authored evidence and deployment boundaries.

For Markdown plus JSON:

```bash
ancova-showcase \
  --output .ancova_ops/showcase/showcase.md \
  --json-output .ancova_ops/showcase/showcase.json
```

## Operate — service intelligence

Run the API:

```bash
uvicorn ancova_ops.api:app --reload
```

Core endpoints:

```text
POST /v1/route
GET  /v1/cases/{case_id}
GET  /v1/cases/{case_id}/routing-decisions
POST /v1/cases/{case_id}/routing-reviews
GET  /v1/cases/{case_id}/routing-reviews
PUT  /v1/cases/{case_id}/outcome
```

The routing layer provides transparent development-stage request intelligence and an explainable baseline recommendation. It does not silently replace human staff.

## Audit — preserve the evidence chain

ANCOVA Ops keeps the original request, machine/rule recommendation, later human review and observed outcome as separable records.

A human override changes the effective operational route without erasing the original machine history. Human review is not automatically treated as ground truth.

This allows later evaluation to distinguish:

```text
what the system recommended
what a human changed
what route was ultimately used
what outcome was observed
which implementation version was active
```

## Evaluate — support before statistics

### 1. Comparison support and identifiability

For the current continuous resolution-time example, the default development model is:

```text
resolution_hours
~ C(department)
+ C(issue_category)
+ urgency
+ frustration
+ complexity
+ previous_related_cases
```

Before adjusted department estimates are reported, ANCOVA Ops checks whether department and issue-category effects can actually be separated from the observed design.

The overlap/identifiability layer reports `supported`, `weak_overlap`, or `not_identifiable`.

When the design is `not_identifiable`:

```text
adjusted department estimates = withheld
ANOVA department results      = withheld
management ranking            = blocked
```

A missing identification basis is treated as a result, not as an inconvenience to hide.

### 2. Known-truth validity benchmark

```bash
ancova-validity
ancova-validity --json
```

The benchmark tests four deterministic synthetic behaviours:

- known-effect recovery under overlapping case mix;
- measured-confounding adjustment versus a deliberately naive model;
- no-overlap refusal;
- detection of a deliberately violated common-slope assumption.

Passing the benchmark validates software/statistical behaviour on known synthetic scenarios. It does **not** validate real service outcomes or causal effects.

### 3. Evaluation applicability gate

```bash
ancova-applicability \
  --outcome-type continuous \
  --comparison department_outcome \
  --overlap-status supported \
  --json
```

The final v1 gate returns exactly one high-level disposition:

| Disposition | Meaning |
| --- | --- |
| `use` | The declared method family is plausible, subject to diagnostics and interpretation limits. |
| `caution` | The method may be usable, but support or assumptions need attention. |
| `reject` | The requested adjusted comparison is not supported by the declared design. |
| `recommend_alternative` | The question should use a different analysis family. |

Examples:

```text
continuous + supported overlap
→ use regression_ancova_style

weak overlap
→ caution

material department-specific slope
→ caution + interaction_aware_regression

no department/case-type overlap
→ reject + no_adjusted_department_comparison

binary outcome
→ recommend_alternative + logistic_type_model

censored/time-to-event outcome
→ recommend_alternative + survival_time_to_event_model

repeated/clustered observations
→ recommend_alternative + clustered_or_hierarchical_model

routing-policy counterfactual
→ recommend_alternative + offline_policy_evaluation

causal-intent question
→ recommend_alternative + causal_design_and_identification
```

See [`docs/evaluation-applicability.md`](docs/evaluation-applicability.md).

### 4. Management outcome report

```bash
ancova-management-report
```

The report combines:

- raw summaries;
- applicability disposition and recommended method family;
- department/case-type identifiability;
- case-mix-standardised adjusted estimates where supportable;
- uncertainty and model diagnostics;
- explicit warnings and non-causal interpretation boundaries.

The report can show **withheld** instead of an adjusted ranking when the design cannot support one.

## Other evaluation research

Offline adaptive-routing research:

```bash
ancova-policy evaluate
ancova-policy status
```

This uses synthetic logged-policy data and support-aware offline evaluation. It is not wired into live `/v1/route`, and passing an offline gate does not authorise deployment.

Longitudinal benchmark:

```bash
ancova-longitudinal
ancova-longitudinal --json
```

The benchmark compares simpler recurrence/time-to-event approaches on synthetic histories with leakage-aware validation. Sequence/LSTM work remains deferred unless a same-benchmark experiment demonstrates reproducible incremental value.

## Complete command surface

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

## v1.0 capability map

| Capability | Status | Evidence class |
| --- | --- | --- |
| Explainable request routing | Implemented | Transparent development rules |
| Immutable case / routing history | Implemented | Local development persistence |
| Human confirmation / override | Implemented | Human feedback, not automatic ground truth |
| Outcome capture | Implemented | Local development records |
| Routing benchmark | Implemented | Hand-authored fixture |
| Governance validation | Implemented | Machine-readable development policy |
| Raw-versus-adjusted management reporting | Implemented | Synthetic outcomes |
| Department/case-type overlap and identifiability | Implemented | Synthetic development evidence |
| Known-truth evaluation validity benchmark | Implemented | Synthetic validity scenarios |
| Evaluation applicability gate | Implemented | Deterministic decision rules |
| Regression / ANCOVA diagnostics | Implemented | Synthetic outcomes |
| Offline adaptive-policy research | Implemented | Synthetic logged-policy data |
| Longitudinal recurrence benchmark | Implemented | Synthetic histories |
| One-command v1 showcase | Implemented | Aggregates existing development evidence |
| Sequence/LSTM modelling | Deferred | Requires incremental-value evidence |
| Real private-data pilot | Blocked | Separate governance approval required |
| Production deployment | Blocked | Real-data, security and operational evidence required |

## Method follows the question

ANCOVA/regression is one method, not a mandatory product feature.

A different statistical model does not fix missing overlap or identification. Likewise, changing the link function does not remove confounding, and a significant adjusted coefficient does not turn observational data into a causal experiment.

v1.0 deliberately stops at **method recommendation/refusal** for analysis families that are not part of the existing research workflows. It does not implement every logistic, survival, hierarchical or causal model merely to increase feature count.

## Evidence and governance boundary

The repository remains synthetic-first. Current quantitative evidence comes from synthetic data or a small hand-authored fixture unless explicitly stated otherwise.

Do **not** report current outputs as:

- real service improvements;
- causal department or staff effects;
- production routing accuracy;
- validated psychological measurement;
- evidence that an adaptive policy should be deployed;
- evidence that real private histories are approved to process.

A real-data pilot remains blocked until privacy/legal review, notice/consent requirements where applicable, access control, retention/deletion, identity linkage, incident handling and real-data quality protocols are approved.

Production requires additional real-world validation, authentication/authorization, secure deployment, monitoring, recovery, security testing, change control and operational acceptance.

## Project completion and freeze

**ANCOVA Ops v1.0.0 is the completion line for this research/portfolio project.**

The following are **post-v1 opportunities, not unfinished v1 work**:

- a real organisation/pilot;
- private-data governance approval;
- production infrastructure;
- new statistical model families;
- deeper AI/LLM request intelligence;
- PyPI distribution;
- Zenodo DOI archiving;
- software-paper submission;
- competition-specific extensions.

Further model-building should require a concrete user, competition requirement, research question or pilot opportunity rather than being added simply because more complexity is possible.

## Project principles

- **Operate, Audit, Evaluate:** operational support and evidence review are separate responsibilities.
- **Human-in-the-loop:** recommendations support staff rather than silently replacing them.
- **Evidence before claims:** synthetic and hand-authored results are labelled as such.
- **Refuse unsupported comparisons:** `reject` and `withheld` are valid analytical outputs.
- **Method follows the question:** ANCOVA is one method, not the product definition.
- **Interpretable first:** transparent references precede complex ML.
- **Complexity must earn its place:** richer models must beat simpler baselines on the same benchmark.
- **Data minimisation:** operational usefulness does not automatically justify analytics or long-term retention.
- **Auditability:** original decisions, human reviews, implementation versions and outcomes remain separable.
- **Non-causal reporting:** adjusted associations are not presented as causal rankings.

## License and citation

ANCOVA Ops is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Software citation metadata is stored in [`CITATION.cff`](CITATION.cff). See [`docs/citation.md`](docs/citation.md) for the optional archival/DOI workflow. A DOI is not claimed until a real archival record is verified.

For detailed boundaries, see [`docs/project-status.md`](docs/project-status.md), [`docs/release-readiness.md`](docs/release-readiness.md), [`docs/statistical-methodology.md`](docs/statistical-methodology.md), [`docs/evaluation-applicability.md`](docs/evaluation-applicability.md), [`docs/roadmap.md`](docs/roadmap.md) and [`CHANGELOG.md`](CHANGELOG.md).
