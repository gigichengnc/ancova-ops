# ReasonedOps

[![CI](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/gigichengnc/reasoned-ops?display_name=tag)](https://github.com/gigichengnc/reasoned-ops/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

**Evidence-aware service operations: Operate → Audit → Evaluate.**

ReasonedOps is a runnable research/software prototype that turns unstructured service requests into explainable operational recommendations, preserves human and machine decision history, records outcomes, and checks whether management conclusions are actually supported by the available data.

> **It is not designed to make management decisions. It is designed to make unsupported management conclusions harder to reach.**

The project originated from my participation in the **HKMU Hackathon 2026** and was originally developed under the name **ANCOVA Ops**. It was renamed **ReasonedOps** in v1.1.0 because ANCOVA/regression is only one method inside the Evaluate layer, not the product itself.

Property management is the first use case, not the product boundary.

## Is it actually runnable?

**Yes — as a local research prototype.** The repository contains executable Python code, a FastAPI service, local SQLite persistence, tests, command-line workflows, and a one-command end-to-end showcase. CI runs the project on Python 3.11 and 3.12.

| What you can run now | Status | What happens |
| --- | --- | --- |
| Service-request routing API | ✅ Working prototype | Accepts a request and returns issue signals, recommended department, priority, review flag and reasons. |
| Audit trail | ✅ Working prototype | Stores the original case, machine routing decision, human review/override and observed outcome as separate records. |
| Human override | ✅ Working prototype | A reviewer can confirm or override routing without deleting the original machine decision. |
| Outcome capture | ✅ Working prototype | Records response/resolution time, reassignment, escalation and satisfaction fields. |
| Management outcome report | ✅ Working prototype | Produces raw and adjusted summaries, diagnostics, applicability status and explicit interpretation limits. |
| Validity/applicability checks | ✅ Working prototype | Can return `use`, `caution`, `reject`, or `recommend_alternative`, including refusing unsupported department comparisons. |
| Synthetic benchmarks | ✅ Working prototype | Runs deterministic routing, validity, policy and longitudinal research workflows. |
| Real private-data deployment | ❌ Not approved | Requires separate privacy, security, governance and real-data validation work. |
| Production system | ❌ Not claimed | This repository is a research/portfolio prototype, not an enterprise deployment. |

### 60-second proof

After cloning the repository:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
reasoned-showcase
```

`reasoned-showcase` executes the existing development workflows and writes a reviewer-facing report to:

```text
.reasoned_ops/showcase/showcase.md
```

The report shows, in one run:

```text
Operate   → request understanding + explainable routing
Audit     → decision-history and governance boundary
Evaluate  → comparison support + method applicability + guarded outcome analysis
```

For structured output too:

```bash
reasoned-showcase \
  --output .reasoned_ops/showcase/showcase.md \
  --json-output .reasoned_ops/showcase/showcase.json
```

### Try the API directly

Start the local service:

```bash
uvicorn reasoned_ops.api:app --reload
```

Check that it is alive:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Send a service request:

```bash
curl -X POST http://127.0.0.1:8000/v1/route \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "demo-001",
    "message": "The air conditioner is leaking again and the wet floor could be dangerous.",
    "previous_related_cases": 2,
    "vulnerability_flag": false
  }'
```

The API returns structured JSON containing fields such as:

```text
issue_category
urgency
frustration
complexity
department
priority
requires_human_review
reasons
intelligence_version
router_version
```

The routed case and decision are also persisted locally so later review and outcome records can be attached to the same case.

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

## What makes the Evaluate layer different?

ReasonedOps does not assume that every KPI comparison is meaningful.

For the current continuous resolution-time development example, it can model:

```text
resolution_hours
~ C(department)
+ C(issue_category)
+ urgency
+ frustration
+ complexity
+ previous_related_cases
```

Before adjusted department estimates are reported, the system checks whether department and case type can actually be separated from the observed routing design.

Possible support states are:

```text
supported
weak_overlap
not_identifiable
```

If the design is `not_identifiable`:

```text
adjusted department estimates = withheld
ANOVA department results      = withheld
management ranking            = blocked
```

The separate applicability gate then asks whether the declared question should use the current regression/ANCOVA-style method at all.

```bash
reasoned-applicability \
  --outcome-type continuous \
  --comparison department_outcome \
  --overlap-status supported \
  --json
```

It returns one of:

| Disposition | Meaning |
| --- | --- |
| `use` | The declared method family is plausible, subject to diagnostics and interpretation limits. |
| `caution` | The method may be usable, but support or assumptions need attention. |
| `reject` | The requested adjusted comparison is not supported by the declared design. |
| `recommend_alternative` | The question should use a different analysis family. |

Examples include redirecting binary outcomes toward logistic-type analysis, censored time-to-event questions toward survival analysis, repeated observations toward clustered/hierarchical methods, and routing-policy counterfactuals toward offline policy evaluation.

ANCOVA/regression is therefore **one method inside Evaluate**, not the product itself.

## Main runnable interfaces

```bash
# End-to-end reviewer demo
reasoned-showcase

# Routing development benchmark
reasoned-evaluate

# Known-truth synthetic validity benchmark
reasoned-validity

# Evaluation-method gate
reasoned-applicability --json

# Outcome analysis and management report
reasoned-analyze
reasoned-management-report

# Governance checks
reasoned-governance-check --json

# Offline routing-policy research
reasoned-policy evaluate

# Longitudinal benchmark
reasoned-longitudinal --json
```

FastAPI endpoints:

```text
GET  /health
POST /v1/route
GET  /v1/cases/{case_id}
GET  /v1/cases/{case_id}/routing-decisions
POST /v1/cases/{case_id}/routing-reviews
GET  /v1/cases/{case_id}/routing-reviews
PUT  /v1/cases/{case_id}/outcome
```

## Evidence and deployment boundary

The repository is deliberately synthetic-first. Current quantitative results come from synthetic data or a small hand-authored fixture unless explicitly stated otherwise.

Do **not** report current outputs as:

- real service improvements;
- causal department or staff effects;
- production routing accuracy;
- validated psychological measurement;
- evidence that a routing policy should be deployed;
- evidence that private resident/customer histories are safe to process.

A real-data pilot remains blocked until privacy/legal review, access control, retention/deletion, identity linkage, incident handling and real-data quality protocols are approved.

This distinction is intentional:

```text
Working local research prototype   ✅
Real private-data pilot            ❌ not approved
Production deployment              ❌ not approved
```

## Rename and compatibility

**ReasonedOps** is the canonical project name from v1.1.0 onward.

```text
Repository:          gigichengnc/reasoned-ops
Distribution:        reasoned-ops
Python package:      reasoned_ops
CLI prefix:          reasoned-
```

The `ancova_ops` namespace is retained temporarily as a compatibility surface for historical development references. New code and documentation should use `reasoned_ops` and `reasoned-*` commands.

Historical release notes before v1.1.0 intentionally retain the former name **ANCOVA Ops**.

## Project principles

- **Operate, Audit, Evaluate:** operational support and evidence review are separate responsibilities.
- **Human-in-the-loop:** recommendations support staff rather than silently replacing them.
- **Evidence before claims:** synthetic and hand-authored results are labelled as such.
- **Refuse unsupported comparisons:** a missing identification basis is a result, not something to hide.
- **Method follows the question:** ANCOVA is one tool, not a mandatory product feature.
- **Interpretable first:** transparent baselines precede complex ML.
- **Auditability:** original decisions, human reviews, versions, and outcomes remain separable.
- **Non-causal reporting:** adjusted associations are not presented as causal rankings.

## License, citation and deeper documentation

ReasonedOps is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Software citation metadata is stored in [`CITATION.cff`](CITATION.cff). A DOI is not claimed until a real archival record is verified.

For deeper detail, see:

- [`docs/project-status.md`](docs/project-status.md)
- [`docs/release-readiness.md`](docs/release-readiness.md)
- [`docs/statistical-methodology.md`](docs/statistical-methodology.md)
- [`docs/evaluation-applicability.md`](docs/evaluation-applicability.md)
- [`docs/portfolio-showcase.md`](docs/portfolio-showcase.md)
- [`CHANGELOG.md`](CHANGELOG.md)
