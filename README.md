# ANCOVA Ops

**Human-centred service intelligence for turning unstructured requests into measurable, adaptive operations.**

ANCOVA Ops is an experimental service-operations platform originating from an HKMU Hackathon 2026 concept. The repository develops that idea into a reproducible software and analytics project covering explainable request routing, human review, outcome analysis, offline policy research and longitudinal model comparison.

**Current checkpoint: `v0.5.2` — Phases 0–4 implemented for synthetic/hand-authored development use, with a one-command portfolio showcase and Apache-2.0 licensing.**

> Real private resident/customer data, real longitudinal personalisation and production adaptive deployment are not approved at this stage.

## One-command showcase

After installation, the fastest way to understand the project is:

```bash
ancova-showcase
```

This generates:

```text
.ancova_ops/showcase/showcase.md
```

For Markdown plus structured JSON:

```bash
ancova-showcase \
  --output .ancova_ops/showcase/showcase.md \
  --json-output .ancova_ops/showcase/showcase.json
```

The showcase runs the existing service-intelligence example, routing benchmark, ANCOVA outcome-analysis workflow, adaptive-routing offline study, longitudinal benchmark and governance/readiness summary in one deterministic report. It does **not** introduce a new model or turn synthetic results into real-world evidence.

See [`docs/portfolio-showcase.md`](docs/portfolio-showcase.md).

## What the project does

ANCOVA Ops deliberately separates operational decision support from downstream statistical evaluation:

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
Observed service outcome
      |
      v
Auditable historical records
      |
      +--> Routing benchmark
      +--> ANCOVA / regression + diagnostics + management report
      +--> Offline adaptive-policy evaluation + approval / rollback
      +--> Synthetic longitudinal recurrence benchmark
```

ANCOVA means **Analysis of Covariance**. It is used downstream to compare service outcomes while adjusting for pre-specified case-mix covariates; it is **not** used to score individual messages.

A simplified analysis might be:

```text
resolution_time ~ department + urgency + frustration + complexity
```

Adjusted estimates are model-based associations, not automatic causal effects or staff-performance rankings.

## v0.5.2 capability map

| Capability | Status | Entry point | Evidence class |
| --- | --- | --- | --- |
| Portfolio showcase | Implemented | `ancova-showcase` | Aggregates existing development evidence |
| Request intelligence + explainable routing | Implemented | FastAPI `/v1/route` | Transparent development rules |
| Immutable case / routing audit history | Implemented | SQLite persistence | Local development records |
| Human confirmation / override | Implemented | routing-review API | Human feedback, not automatic ground truth |
| Routing evaluation | Implemented | `ancova-evaluate` | Hand-authored fixture |
| Data-governance validation | Implemented | `ancova-governance-check` | Machine-readable development policy |
| ANCOVA / regression workflow | Implemented | `ancova-analyze` | Synthetic outcomes |
| Management evidence report | Implemented | `ancova-management-report` | Synthetic outcomes |
| Adaptive-routing offline study | Implemented | `ancova-policy evaluate` | Synthetic logged-policy data |
| Policy approval / rollback registry | Implemented locally | `ancova-policy` | Development lifecycle control |
| Longitudinal recurrence benchmark | Implemented | `ancova-longitudinal` | Synthetic longitudinal histories |
| LSTM / sequence modelling | Deferred | — | Requires incremental-value evidence |
| Real private-data pilot | Blocked | — | Separate governance approval required |
| Production deployment | Blocked | — | Real-data + security/operations evidence required |

For detailed boundaries, see [`docs/project-status.md`](docs/project-status.md), [`docs/release-readiness.md`](docs/release-readiness.md) and [`CHANGELOG.md`](CHANGELOG.md).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
ancova-showcase
```

The package supports Python 3.11+ and CI tests Python 3.11 and 3.12.

## Service-intelligence API

Run the API:

```bash
uvicorn ancova_ops.api:app --reload
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/v1/route \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "demo-api-001",
    "message": "The air conditioner is leaking again and an elderly resident may slip.",
    "previous_related_cases": 2,
    "vulnerability_flag": true
  }'
```

Machine/rule recommendations are preserved even when a later human review changes the effective operational routing. Local development case history is stored in `.ancova_ops/ancova_ops.sqlite3` by default and is ignored by Git.

Core endpoints:

```text
POST /v1/route
GET  /v1/cases/{case_id}
GET  /v1/cases/{case_id}/routing-decisions
POST /v1/cases/{case_id}/routing-reviews
GET  /v1/cases/{case_id}/routing-reviews
PUT  /v1/cases/{case_id}/outcome
```

## Development workflows

Routing evaluation:

```bash
ancova-evaluate
ancova-evaluate --json
```

The transparent baseline currently scores `10 / 11` department accuracy, `2 / 5` expected-human-review recall and `11 / 11` explanation coverage on a small hand-authored development fixture. These are fixture results, not production estimates.

Governance validation:

```bash
ancova-governance-check
ancova-governance-check --json
```

Outcome analysis and management reporting:

```bash
ancova-analyze
ancova-analyze --json
ancova-management-report
```

The ANCOVA/regression workflow exposes missingness, group sizes, residual diagnostics, heteroskedasticity, multicollinearity, influence, interaction checks, adjusted estimates, confidence intervals and warnings. The management report keeps raw observed summaries separate from adjusted estimates.

Adaptive-routing research:

```bash
ancova-policy evaluate
ancova-policy evaluate --register
ancova-policy status
```

The candidate is evaluated only on synthetic logged-policy data with chronological validation and support-aware inverse-propensity methods. Passing an offline gate does not authorise deployment, and registry activation is intentionally not wired into `/v1/route`.

Longitudinal benchmark:

```bash
ancova-longitudinal
ancova-longitudinal --json
```

The benchmark compares a recency/frequency logistic baseline, a discrete-time hazard model and a random forest on the same later validation window with a purged chronological split. Sequence modelling remains `deferred_not_justified_by_current_benchmark` until a same-benchmark experiment demonstrates reproducible incremental value.

## Project principles

- **Human-in-the-loop:** recommendations support staff rather than silently replacing them.
- **Evidence before claims:** synthetic and hand-authored results are labelled as such.
- **Interpretable first:** simple transparent references precede complex ML.
- **Complexity must earn its place:** richer models must beat simpler baselines on the same future benchmark.
- **Data minimisation:** operational usefulness does not automatically justify analytics or long-term retention.
- **Auditability:** original decisions, human reviews, implementation versions and outcomes remain separable.
- **Non-causal reporting:** adjusted associations are not presented as causal department/staff rankings.
- **Offline before deployment:** adaptive-policy candidates remain research objects until separate approval and integration work exists.
- **Leakage-aware validation:** future events cannot enter historical model features or overlapping training labels.
- **Modular:** property management is the first use case, not the product definition.

## Repository layout

```text
LICENSE
README.md
CHANGELOG.md

src/ancova_ops/
├── api.py
├── intelligence.py
├── models.py
├── persistence.py
├── routing.py
├── evaluation.py
├── governance.py
├── analytics.py
├── analysis_report.py
├── management_report.py
├── adaptive.py
├── longitudinal.py
├── showcase.py
├── synthetic.py
└── demo.py

config/
└── data-governance.json

data/evaluation/
└── hand_authored_v1.json

docs/
├── architecture.md
├── project-status.md
├── release-readiness.md
├── portfolio-showcase.md
├── roadmap.md
├── hackathon-origin.md
├── data-model.md
├── data-governance.md
├── routing-evaluation.md
├── human-routing-feedback.md
├── statistical-methodology.md
├── management-report.md
├── adaptive-routing.md
└── longitudinal-benchmark.md
```

## Evidence and deployment status

Phases 0–4 and the v0.5.2 showcase have runnable development workflows. Current quantitative evidence comes from synthetic data or the small hand-authored routing fixture unless explicitly stated otherwise.

Do **not** report current benchmark outputs as real service improvements, causal effects, production routing accuracy or real resident/customer predictions.

A real-data pilot remains blocked until privacy/legal review, notice/consent requirements where applicable, access control, retention/deletion, identity linkage, incident handling and real-data quality protocols are approved. Production additionally requires authenticated access, RBAC, secrets management, monitoring, recovery targets, security testing and real-world validation.

## Hackathon-origin metrics

Figures in the original hackathon presentation are not treated as measured ANCOVA Ops outcomes unless they can be traced to project-specific experiments. See [`docs/hackathon-origin.md`](docs/hackathon-origin.md).

## License

ANCOVA Ops is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

The Apache-2.0 license applies to ANCOVA Ops material distributed under this repository license. Third-party dependencies and any separately identified third-party material remain subject to their own licences and notices.
