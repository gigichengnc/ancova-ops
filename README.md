# ReasonedOps

[![CI](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/gigichengnc/reasoned-ops?display_name=tag)](https://github.com/gigichengnc/reasoned-ops/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

**Evidence-aware service operations: Operate → Audit → Evaluate.**

ReasonedOps is a completed research/software prototype for turning unstructured service requests into explainable operational recommendations, preserving human and machine decision history, recording outcomes, and testing whether management conclusions are actually supported by the available data.

> **It is not designed to make management decisions. It is designed to make unsupported management conclusions harder to reach.**

The project originated from an HKMU Hackathon 2026 concept and was originally developed under the name **ANCOVA Ops**. It was renamed **ReasonedOps** in v1.1.0 because ANCOVA/regression is only one method inside the Evaluate layer, not the product itself.

Property management is the first use case, not the product boundary.

## Current status

| Reviewer question | Current answer |
| --- | --- |
| Current rename checkpoint | **v1.1.0 — ReasonedOps** |
| Research/portfolio prototype | **Completed** |
| Core architecture | **Operate → Audit → Evaluate** |
| Fastest end-to-end demo | `reasoned-showcase` |
| Evaluation validity benchmark | `reasoned-validity` |
| Method applicability gate | `reasoned-applicability` |
| Canonical Python package | `reasoned_ops` |
| Legacy compatibility namespace | `ancova_ops` |
| Evidence class | Synthetic data + a small hand-authored routing fixture |
| Real private-data pilot | **Not approved** |
| Production deployment | **Not approved** |
| License | Apache-2.0 |
| Citation | Root `CITATION.cff`; no DOI claimed until independently verified |

Current quantitative outputs are development evidence. They are not real-world service-improvement claims, causal department rankings, or production-readiness evidence.

## Operate → Audit → Evaluate

| Layer | What ReasonedOps does |
| --- | --- |
| **Operate** | Structure service requests, extract transparent operational signals, and recommend an explainable route. |
| **Audit** | Preserve the original request, machine/rule decision, human confirmation or override, implementation version, and observed outcome. |
| **Evaluate** | Ask whether a comparison is supportable, choose or recommend an analysis family, separate raw from adjusted evidence, surface uncertainty, and withhold unsupported conclusions. |

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

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
reasoned-showcase
```

The showcase writes a reviewer-facing report to:

```text
.reasoned_ops/showcase/showcase.md
```

For Markdown plus JSON:

```bash
reasoned-showcase \
  --output .reasoned_ops/showcase/showcase.md \
  --json-output .reasoned_ops/showcase/showcase.json
```

## Operate — service intelligence

Run the API:

```bash
uvicorn reasoned_ops.api:app --reload
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

ReasonedOps keeps the original request, machine/rule recommendation, later human review, effective route, implementation version, and observed outcome as separable records.

A human override changes the effective operational route without erasing the original machine history. Human review is not automatically treated as ground truth.

This lets a later reviewer distinguish:

```text
what the system recommended
what a human changed
what route was ultimately used
what outcome was observed
which implementation version was active
```

## Evaluate — support before statistics

### 1. Can the comparison be supported?

For the current continuous resolution-time development example:

```text
resolution_hours
~ C(department)
+ C(issue_category)
+ urgency
+ frustration
+ complexity
+ previous_related_cases
```

Before adjusted department estimates are reported, ReasonedOps checks whether department and issue-category effects can actually be separated from the observed design.

The overlap/identifiability layer reports:

```text
supported
weak_overlap
not_identifiable
```

When the design is `not_identifiable`:

```text
adjusted department estimates = withheld
ANOVA department results      = withheld
management ranking            = blocked
```

A missing identification basis is treated as a result, not as an inconvenience to hide.

### 2. Known-truth validity benchmark

```bash
reasoned-validity
reasoned-validity --json
```

The benchmark tests deterministic synthetic behaviours including known-effect recovery, measured-confounding adjustment, no-overlap refusal, and detection of a deliberately violated common-slope assumption.

Passing the benchmark validates software/statistical behaviour on known synthetic scenarios. It does **not** validate real service outcomes or causal effects.

### 3. Is this the right evaluation method?

```bash
reasoned-applicability \
  --outcome-type continuous \
  --comparison department_outcome \
  --overlap-status supported \
  --json
```

The applicability gate returns one high-level disposition:

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

ANCOVA/regression therefore remains **one tool in the evaluation layer**. ReasonedOps does not force ANCOVA onto every question merely because of the project's history.

### 4. Management outcome report

```bash
reasoned-management-report
```

The report combines raw summaries, applicability status, identifiability, case-mix-standardised estimates where supportable, uncertainty, diagnostics, and explicit interpretation boundaries. It can show **withheld** instead of a ranking when the data cannot support one.

## Other research workflows

```bash
# Routing benchmark
reasoned-evaluate
reasoned-evaluate --json

# Governance
reasoned-governance-check
reasoned-governance-check --json

# Outcome analysis
reasoned-analyze
reasoned-analyze --json
reasoned-management-report

# Validity and applicability
reasoned-validity
reasoned-applicability --json

# Offline routing-policy research
reasoned-policy evaluate
reasoned-policy status

# Longitudinal benchmark
reasoned-longitudinal
reasoned-longitudinal --json
```

Offline policy and longitudinal workflows remain research components using synthetic data. They do not authorize deployment.

## Evidence and governance boundary

The repository is deliberately synthetic-first. Current quantitative results come from synthetic data or a small hand-authored fixture unless explicitly stated otherwise.

Do **not** report current outputs as:

- real service improvements;
- causal department or staff effects;
- production routing accuracy;
- validated psychological measurement;
- evidence that a routing policy should be deployed;
- evidence that private resident/customer histories are safe to process.

A real-data pilot remains blocked until privacy/legal review, notice/consent requirements where applicable, access control, retention/deletion, identity linkage, incident handling, and real-data quality protocols are approved.

## Rename and compatibility

**ReasonedOps** is the canonical project name from v1.1.0 onward.

Canonical names:

```text
Repository:          gigichengnc/reasoned-ops
Distribution:        reasoned-ops
Python package:      reasoned_ops
CLI prefix:          reasoned-
```

The `ancova_ops` namespace is retained temporarily as a compatibility surface for existing local examples and historical development references. New code and documentation should use `reasoned_ops` and `reasoned-*` commands.

Historical release notes before v1.1.0 may still use the former name **ANCOVA Ops**. That history is intentional.

## Project principles

- **Operate, Audit, Evaluate:** operational support and evidence review are separate responsibilities.
- **Human-in-the-loop:** recommendations support staff rather than silently replacing them.
- **Evidence before claims:** synthetic and hand-authored results are labelled as such.
- **Refuse unsupported comparisons:** a missing identification basis is a result, not something to hide.
- **Method follows the question:** ANCOVA is one tool, not a mandatory product feature.
- **Interpretable first:** transparent baselines precede complex ML.
- **Complexity must earn its place:** richer models must beat simpler baselines on the same benchmark.
- **Data minimisation:** operational usefulness does not automatically justify analytics or long-term retention.
- **Auditability:** original decisions, human reviews, versions, and outcomes remain separable.
- **Non-causal reporting:** adjusted associations are not presented as causal rankings.

## License and citation

ReasonedOps is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Software citation metadata is stored in [`CITATION.cff`](CITATION.cff). A DOI is not claimed until a real archival record is verified.

For detailed boundaries and methodology, see [`docs/project-status.md`](docs/project-status.md), [`docs/release-readiness.md`](docs/release-readiness.md), [`docs/statistical-methodology.md`](docs/statistical-methodology.md), [`docs/evaluation-applicability.md`](docs/evaluation-applicability.md), and [`CHANGELOG.md`](CHANGELOG.md).
