# ANCOVA Ops

**Human-centred service intelligence for turning unstructured requests into measurable, adaptive operations.**

ANCOVA Ops is an experimental service-operations platform originating from an HKMU Hackathon 2026 concept. The repository develops that idea into a reproducible software and analytics project covering explainable request routing, human review, outcome analysis, offline policy research and longitudinal model comparison.

**Current checkpoint: `v0.5.0` — Phases 0–4 implemented for synthetic/hand-authored development use.**

> Real private resident/customer data, real longitudinal personalisation and production adaptive deployment are not approved at this stage.

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

## v0.5.0 capability map

| Capability | Status | Entry point | Evidence class |
| --- | --- | --- | --- |
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

For the detailed checkpoint boundary, see [`docs/project-status.md`](docs/project-status.md) and [`docs/release-readiness.md`](docs/release-readiness.md). The release history is in [`CHANGELOG.md`](CHANGELOG.md).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
python -m ancova_ops.demo
```

The package supports Python 3.11+ and CI currently tests Python 3.11 and 3.12.

## Phase 1 — Service-intelligence API

Run the API:

```bash
uvicorn ancova_ops.api:app --reload
```

Example routing request:

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

The API returns structured issue features, routing, priority, human-review requirements, explanation reasons and implementation version identifiers. Machine/rule recommendations are preserved even when a later human review overrides the effective routing.

By default, local case history is stored in `.ancova_ops/ancova_ops.sqlite3`, which is ignored by Git.

Core endpoints:

```text
POST /v1/route
GET  /v1/cases/{case_id}
GET  /v1/cases/{case_id}/routing-decisions
POST /v1/cases/{case_id}/routing-reviews
GET  /v1/cases/{case_id}/routing-reviews
PUT  /v1/cases/{case_id}/outcome
```

## Routing evaluation

```bash
ancova-evaluate
ancova-evaluate --json
```

The current transparent baseline is tested on a small hand-authored fixture. Its deterministic development results are:

- department accuracy: `10 / 11`;
- expected-human-review recall: `2 / 5`;
- explanation coverage: `11 / 11`.

These are fixture results, not production estimates. See [`docs/routing-evaluation.md`](docs/routing-evaluation.md).

## Data-governance boundary

```bash
ancova-governance-check
ancova-governance-check --json
```

ANCOVA Ops currently operates under a **synthetic-only development policy**. The machine-readable policy in `config/data-governance.json` blocks real private records, direct identifiers, raw private-message training, unsupported psychological profiling and unapproved longitudinal personalisation.

See [`docs/data-governance.md`](docs/data-governance.md).

## Phase 2 — Outcome analytics

Technical analysis:

```bash
ancova-analyze
ancova-analyze --json
```

Management-facing report:

```bash
ancova-management-report
```

The analysis workflow includes missingness accounting, department group sizes, residual diagnostics, Breusch–Pagan heteroskedasticity screening, VIF checks, influence diagnostics, department-by-covariate interactions, adjusted department estimates and confidence intervals.

The management report keeps raw observed summaries separate from adjusted model estimates and carries warnings into the management view.

See [`docs/statistical-methodology.md`](docs/statistical-methodology.md) and [`docs/management-report.md`](docs/management-report.md).

## Phase 3 — Adaptive-routing research

```bash
ancova-policy evaluate
```

The offline workflow uses deterministic synthetic logged-routing history with timestamps and known action propensities. It trains a transparent candidate on an earlier window and evaluates baseline and candidate on a later window with support-aware inverse-propensity methods.

Candidate lifecycle commands include:

```bash
ancova-policy evaluate --register
ancova-policy status
ancova-policy approve --version <version> --reviewer <reviewer> --rationale <text>
ancova-policy activate --version <version> --actor <actor>
ancova-policy rollback --version baseline-route-v1 --actor <actor> --rationale <text>
```

Passing the synthetic offline gate does not authorize deployment. Registry activation is intentionally **not wired into `/v1/route`**.

See [`docs/adaptive-routing.md`](docs/adaptive-routing.md).

## Phase 4 — Longitudinal benchmark

```bash
ancova-longitudinal
ancova-longitudinal --json
```

The benchmark creates deterministic synthetic entity-level service histories with recurrence and seasonality, builds features using only pre-cutoff events, and applies a purged chronological split so training follow-up cannot overlap the validation period.

It compares on the same future validation window:

1. recency/frequency logistic baseline;
2. discrete-time logistic hazard model;
3. random-forest recurrence classifier.

The comparison reports ROC-AUC, Brier score, calibration bias and survival concordance where applicable. Sequence modelling remains `deferred_not_justified_by_current_benchmark` until a later same-benchmark experiment demonstrates reproducible incremental value.

See [`docs/longitudinal-benchmark.md`](docs/longitudinal-benchmark.md).

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

Phases 0–4 have runnable development workflows. Current quantitative evidence comes from synthetic data or the small hand-authored routing fixture unless explicitly stated otherwise.

Do **not** report current benchmark outputs as real service improvements, causal effects, production routing accuracy or real resident/customer predictions.

A real-data pilot remains blocked until privacy/legal review, notice/consent requirements where applicable, access control, retention/deletion, identity linkage, incident handling and real-data quality protocols are approved. Production additionally requires authenticated access, RBAC, secrets management, monitoring, recovery targets, security testing and real-world validation.

## Hackathon-origin metrics

Figures in the original hackathon presentation are not treated as measured ANCOVA Ops outcomes unless they can be traced to project-specific experiments. See [`docs/hackathon-origin.md`](docs/hackathon-origin.md).

## License

A licence has not yet been selected. Public visibility does not imply permission to reuse, modify or redistribute the project until a licence is added.
