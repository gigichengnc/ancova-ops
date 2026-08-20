# ANCOVA Ops

[![CI](https://github.com/gigichengnc/ancova-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/gigichengnc/ancova-ops/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/gigichengnc/ancova-ops?display_name=tag)](https://github.com/gigichengnc/ancova-ops/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

**Evidence-aware service operations: Operate → Audit → Evaluate.**

ANCOVA Ops is a reproducible research/software prototype for turning unstructured service requests into explainable operational decisions, preserving human and machine decision history, recording outcomes, and testing whether management conclusions are actually supported by the available data.

> **It is not designed to make management decisions. It is designed to make unsupported management conclusions harder to reach.**

The project originated from an HKMU Hackathon 2026 concept. Property management is the first use case, not the product boundary, and ANCOVA is one evaluation method rather than the product itself.

## Operate → Audit → Evaluate

| Layer | What ANCOVA Ops does | Current status |
| --- | --- | --- |
| **Operate** | Structure service requests, extract transparent operational signals and recommend an explainable route | Implemented |
| **Audit** | Preserve the original request, machine/rule decision, human confirmation or override, implementation version and observed outcome | Implemented |
| **Evaluate** | Separate raw summaries from adjusted evidence, test whether a comparison is identifiable, surface assumptions/warnings and withhold unsupported rankings | Implemented as a synthetic research workflow |

The evaluation layer deliberately asks **whether a comparison is supportable before reporting an adjusted result**.

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
Auditable history
      |
      v
Descriptive summaries
      |
      v
Comparison support / identifiability gate
      |
      +--> insufficient overlap --> WITHHOLD adjusted ranking
      |
      +--> sufficient overlap
              |
              v
        appropriate evaluation method
              |
              +--> regression / ANCOVA
              +--> interaction-aware analysis
              +--> offline policy evaluation
              +--> longitudinal / survival-style research
```

## v0.6.0 checkpoint

| Reviewer question | Current answer |
| --- | --- |
| Fastest end-to-end demo | `ancova-showcase` |
| Evaluation validity benchmark | `ancova-validity` |
| Current checkpoint | `v0.6.0` |
| Evidence class | Synthetic data + a small hand-authored routing fixture |
| Real private-data pilot / production | **Not approved** |
| License | Apache-2.0 |
| Citation | Root `CITATION.cff`; no DOI claimed until independently verified |

Current quantitative outputs are development evidence. They are not real-world service-improvement claims, causal department rankings or production-readiness evidence.

## One-command showcase

After installation:

```bash
ancova-showcase
```

This writes a deterministic reviewer-facing report to:

```text
.ancova_ops/showcase/showcase.md
```

For Markdown plus JSON:

```bash
ancova-showcase \
  --output .ancova_ops/showcase/showcase.md \
  --json-output .ancova_ops/showcase/showcase.json
```

The showcase aggregates the existing routing, audit/governance, outcome-analysis, adaptive-policy and longitudinal research workflows. It does not create a new evidence class.

## Evaluation validity benchmark

The v0.6.0 validity benchmark tests the evaluation layer against synthetic scenarios where the truth is known:

```bash
ancova-validity
ancova-validity --json
```

It checks four behaviours:

1. **Known-effect recovery** — with overlapping case mix, adjusted department contrasts should approximately recover the synthetic effects used to generate the data.
2. **Measured confounding** — when routing is deliberately associated with issue type, adding the measured issue-category adjustment should materially reduce bias relative to a naive model that omits it.
3. **No-overlap refusal** — when issue category determines department, the comparison is marked `not_identifiable`; adjusted estimates and department ANOVA results are withheld.
4. **Slope-interaction detection** — when a covariate has a deliberately different department-specific slope, the workflow should flag the common-slope interpretation rather than hide the interaction.

Passing this benchmark means the software behaves as intended on known synthetic scenarios. It does **not** validate real service outcomes or establish causal effects.

## Outcome evaluation

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

Before publishing adjusted department estimates, ANCOVA Ops checks whether department effects can be separated from issue-category case mix. It reports:

- department × issue-category counts;
- structural connectivity / estimability;
- practical overlap at a minimum cell-size threshold;
- design-matrix rank;
- `supported`, `weak_overlap`, or `not_identifiable` status.

If the comparison is not identifiable, adjusted department estimates and department ANOVA results are withheld. If it is estimable, adjusted department means are **standardised over the observed complete-case case-mix distribution** rather than forcing every case into one arbitrary issue-category reference.

Even a supported comparison remains model-based and associational. It is not automatically causal and must not be used as a staff-performance league table.

See [`docs/statistical-methodology.md`](docs/statistical-methodology.md).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
ancova-showcase
ancova-validity
```

The package supports Python 3.11+ and CI tests Python 3.11 and 3.12.

## Service-intelligence API

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

Machine/rule recommendations are preserved even when a later human review changes the effective operational route. Human review is not automatically treated as ground truth.

## Development commands

```bash
# Routing benchmark
ancova-evaluate
ancova-evaluate --json

# Governance
ancova-governance-check
ancova-governance-check --json

# Outcome evaluation
ancova-analyze
ancova-analyze --json
ancova-management-report

# Evaluation validity
ancova-validity
ancova-validity --json

# Offline adaptive-routing research
ancova-policy evaluate
ancova-policy status

# Longitudinal benchmark
ancova-longitudinal
ancova-longitudinal --json
```

## Capability map

| Capability | Status | Evidence class |
| --- | --- | --- |
| Request intelligence + explainable routing | Implemented | Transparent development rules |
| Immutable case / routing history | Implemented | Local development persistence |
| Human confirmation / override | Implemented | Human feedback, not automatic ground truth |
| Outcome capture | Implemented | Local development records |
| Routing benchmark | Implemented | Hand-authored fixture |
| Governance validation | Implemented | Machine-readable development policy |
| Raw-versus-adjusted management report | Implemented | Synthetic outcomes |
| Department/issue-category overlap and identifiability gate | Implemented | Synthetic development evidence |
| Known-effect/confounding/no-overlap validity benchmark | Implemented | Synthetic known-truth scenarios |
| Regression / ANCOVA diagnostics | Implemented | Synthetic outcomes |
| Offline adaptive-policy study | Implemented | Synthetic logged-policy data |
| Longitudinal recurrence benchmark | Implemented | Synthetic histories |
| Sequence/LSTM modelling | Deferred | Requires incremental-value evidence |
| Real private-data pilot | Blocked | Separate governance approval required |
| Production deployment | Blocked | Real-data, security and operational evidence required |

## Method follows the question

ANCOVA/regression is not forced onto every outcome. Examples of cases that need a different method or a refusal include:

- binary outcomes such as resolved/unresolved → logistic-type modelling may be more appropriate;
- censored time-to-resolution → survival/time-to-event methods may be more appropriate;
- repeated observations within building/team/customer → clustered or hierarchical models may be required;
- material department-specific slopes → interaction-aware models should replace a common-slope interpretation;
- no department/case-type overlap → **do not rank departments**;
- routing-policy counterfactual questions → offline policy evaluation rather than ordinary ANCOVA.

A final v1.0 applicability layer will make this method-selection boundary explicit as `use`, `caution`, `reject`, or `recommend alternative` rather than trying to implement every statistical model.

## Evidence and governance boundary

The repository is deliberately synthetic-first. Current quantitative results come from synthetic data or a small hand-authored fixture unless explicitly stated otherwise.

Do **not** report current benchmark outputs as:

- real service improvements;
- causal department or staff effects;
- production routing accuracy;
- validated psychological measurement;
- evidence that a policy should be deployed;
- evidence that private resident/customer histories are safe to process.

A real-data pilot remains blocked until privacy/legal review, notice/consent requirements where applicable, access control, retention/deletion, identity linkage, incident handling and real-data quality protocols are approved.

## Project principles

- **Operate, Audit, Evaluate:** operational support and evidence review are separate responsibilities.
- **Human-in-the-loop:** recommendations support staff rather than silently replacing them.
- **Evidence before claims:** synthetic and hand-authored results are labelled as such.
- **Refuse unsupported comparisons:** a missing identification basis is a result, not an inconvenience to hide.
- **Method follows the question:** ANCOVA is one tool, not a mandatory product feature.
- **Interpretable first:** transparent references precede complex ML.
- **Complexity must earn its place:** richer models must beat simpler baselines on the same benchmark.
- **Data minimisation:** operational usefulness does not automatically justify analytics or long-term retention.
- **Auditability:** original decisions, human reviews, implementation versions and outcomes remain separable.
- **Non-causal reporting:** adjusted associations are not presented as causal rankings.

## License and citation

ANCOVA Ops is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Software citation metadata is stored in [`CITATION.cff`](CITATION.cff). See [`docs/citation.md`](docs/citation.md) for the archival/DOI workflow. A DOI is not claimed until a real archival record is verified.

For detailed project boundaries, see [`docs/project-status.md`](docs/project-status.md), [`docs/release-readiness.md`](docs/release-readiness.md), [`docs/roadmap.md`](docs/roadmap.md) and [`CHANGELOG.md`](CHANGELOG.md).
