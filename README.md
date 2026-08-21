# ReasonedOps

[![CI](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/gigichengnc/reasoned-ops?display_name=tag)](https://github.com/gigichengnc/reasoned-ops/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

**A runnable service-operations prototype that follows a case from request → routing → human review → outcome → evidence check.**

ReasonedOps does three practical things:

1. **Operate:** read a service request and recommend where it should go, with reasons.
2. **Audit:** keep the original request, machine recommendation, human override and final outcome as separate records.
3. **Evaluate:** later check whether a management claim such as “Team A is slower” or “the new routing policy improved performance” is actually supported by comparable data.

> **It is not designed to make management decisions. It is designed to make unsupported management conclusions harder to reach.**

## What does that look like in practice?

Imagine a resident submits this request:

```text
The air conditioner is leaking again. This is the third time and the wet floor could be dangerous.
```

### 1. ReasonedOps routes the case

Send the request to the local API:

```bash
curl -X POST http://127.0.0.1:8000/v1/route \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "demo-001",
    "message": "The air conditioner is leaking again. This is the third time and the wet floor could be dangerous.",
    "previous_related_cases": 2,
    "vulnerability_flag": false
  }'
```

The response contains operational fields such as:

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

So the software does not only return a department name. It also records **why** the route was recommended and which logic/version produced it.

### 2. A human can confirm or override it

The machine recommendation is not final authority.

A staff member can confirm it or submit a different final route through the routing-review endpoint. The original machine recommendation is still kept.

The stored history therefore looks conceptually like this:

```text
Original request
      ↓
Machine recommendation
      ↓
Human confirmation / override
      ↓
Effective route
```

This matters when someone later asks:

```text
Why was this case sent there?
Did the staff member change the recommendation?
Which system version made the original recommendation?
```

### 3. The outcome is recorded separately

When the case is completed, an outcome can be attached:

```bash
curl -X PUT http://127.0.0.1:8000/v1/cases/demo-001/outcome \
  -H "Content-Type: application/json" \
  -d '{
    "response_time_minutes": 20,
    "resolution_time_minutes": 180,
    "reassigned": false,
    "escalated": false,
    "satisfaction": 8
  }'
```

ReasonedOps keeps that outcome separate from the routing decision instead of rewriting history after the result is known.

### 4. Later, management asks a question

For example:

```text
“Maintenance takes 18 hours on average while Security takes 7.
Is Maintenance performing worse?”
```

A normal dashboard might immediately rank Maintenance below Security.

ReasonedOps first checks whether the comparison is meaningful.

If Maintenance mostly receives complex repair cases while Security receives simpler complaints, the two groups may not have enough comparable cases. In that situation ReasonedOps can return:

```text
REJECT
Do not produce an adjusted department ranking from this design.
```

If there is enough overlap between comparable cases, the evaluation workflow can continue with case-mix adjustment, diagnostics and uncertainty reporting.

That is the core idea of the project: **do the operational work, preserve the evidence trail, then check whether the data really supports the conclusion.**

---

## Run it locally

### Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

### Start the API

```bash
uvicorn reasoned_ops.api:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### Generate the one-command showcase

```bash
reasoned-showcase
```

It writes:

```text
.reasoned_ops/showcase/showcase.md
```

The showcase runs the existing development workflows and summarises the current routing, audit, evaluation, policy-research, longitudinal and governance evidence in one file.

---

## What works now?

| Capability | What it actually does | Status |
| --- | --- | --- |
| Request routing API | Turns a text request into operational signals and an explainable route recommendation | Working local prototype |
| Human routing review | Confirms or overrides a recommendation without deleting the original decision | Working local prototype |
| Audit history | Stores request, routing decisions, reviews, versions and outcome records separately | Working local prototype |
| Outcome capture | Stores response time, resolution time, reassignment, escalation and satisfaction | Working local prototype |
| Management report | Separates raw summaries from adjusted estimates and shows interpretation warnings | Working local prototype |
| Comparison-support check | Detects weak/no department × case-type overlap and can withhold a ranking | Working local prototype |
| Method applicability | Returns `use`, `caution`, `reject` or `recommend_alternative` | Working local prototype |
| Routing benchmark | Runs a small hand-authored development fixture | Working development benchmark |
| Policy evaluation | Runs offline evaluation on synthetic logged-policy data | Research workflow |
| Longitudinal benchmark | Tests recurrence/time-to-next-case models on synthetic histories | Research workflow |
| Real private-data operation | Process real resident/customer records | **Not approved** |
| Production deployment | Enterprise authentication, security, monitoring and live operations | **Not claimed** |

## Main API endpoints

```text
POST /v1/route
GET  /v1/cases/{case_id}
GET  /v1/cases/{case_id}/routing-decisions
POST /v1/cases/{case_id}/routing-reviews
GET  /v1/cases/{case_id}/routing-reviews
PUT  /v1/cases/{case_id}/outcome
```

## Main commands

```bash
reasoned-showcase
reasoned-evaluate
reasoned-validity
reasoned-applicability --json
reasoned-analyze
reasoned-management-report
reasoned-policy evaluate
reasoned-longitudinal
reasoned-governance-check
```

## Where does ANCOVA fit?

ANCOVA is **one evaluation method**, not the product.

For the current continuous resolution-time example, the evaluation model can adjust for measured case mix such as issue category, urgency, frustration, complexity and previous related cases. Before doing that comparison, ReasonedOps checks whether departments and case types can actually be separated from the observed data.

If the question should use another method family, the applicability gate redirects it instead of forcing ANCOVA onto the problem. Examples include binary outcomes, censored time-to-event outcomes, repeated/clustered observations, routing-policy counterfactuals and causal questions.

See [`docs/statistical-methodology.md`](docs/statistical-methodology.md) and [`docs/evaluation-applicability.md`](docs/evaluation-applicability.md) for the technical details.

## Repository structure

```text
src/reasoned_ops/     application and research code
tests/                regression and workflow tests
data/evaluation/      small hand-authored development fixture
config/               machine-readable development governance policy
docs/                 architecture, methodology and research notes
```

There is no separate legacy application package in the v1.2 codebase; `reasoned_ops` is the single canonical Python namespace.

## Project origin

The project originated from my participation in the **HKMU Hackathon 2026** and was originally developed under the name **ANCOVA Ops**. It was renamed **ReasonedOps** in v1.1.0 because ANCOVA/regression is only one method inside the Evaluate layer, not the product itself.

Property management remains the first worked use case, not the product boundary.

## Evidence boundary

The repository currently uses synthetic data and a small hand-authored routing fixture for quantitative development evidence.

Current outputs should **not** be presented as proof of:

- real service improvement;
- causal department or staff performance;
- production routing accuracy;
- validated psychological measurement;
- real-world return on investment;
- approval to process private resident/customer histories.

A real pilot would require separate privacy/legal review, access control, retention/deletion design, secure storage, real-data quality checks and a defensible evaluation plan.

## License and citation

ReasonedOps is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

Software citation metadata is in [`CITATION.cff`](CITATION.cff). No DOI is claimed until an archival record is independently verified.

For deeper technical material, see [`docs/architecture.md`](docs/architecture.md), [`docs/data-model.md`](docs/data-model.md), [`docs/project-status.md`](docs/project-status.md), [`docs/release-readiness.md`](docs/release-readiness.md), and [`CHANGELOG.md`](CHANGELOG.md).
