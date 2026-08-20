# ANCOVA Ops

**Human-centred service intelligence for turning unstructured requests into measurable, adaptive operations.**

ANCOVA Ops is an experimental service-operations platform originating from an HKMU Hackathon 2026 concept. The project explores how natural-language processing, contextual signals, operational routing and statistical outcome analysis can work together to improve service workflows without removing the human role from service delivery.

The original hackathon concept focused on property-management concierge operations: residents submit requests, the system extracts the operational issue and contextual signals, routes the case to the appropriate team, and learns from historical outcomes. This repository develops that idea into a reproducible software and analytics project.

## Core idea

ANCOVA Ops separates two jobs that are often mixed together in AI demos:

1. **Operational intelligence** — understand a request, structure it and route it.
2. **Outcome evaluation** — measure what actually improves service performance while controlling for relevant covariates.

```text
Resident / user request
        |
        v
Request understanding
(intent, issue, urgency, emotion, context)
        |
        v
Machine/rule routing recommendation
        |
        +--> Human confirmation / override (preserved separately)
        |
        v
Operational outcome
(response time, resolution time, escalation, satisfaction)
        |
        v
Historical dataset
        |
        v
Statistical analysis + model validation
        |
        v
Improved routing policy
```

## Why ANCOVA?

ANCOVA here means **Analysis of Covariance**, used as an analytical layer rather than as a message-processing algorithm.

For example, we may want to compare departmental resolution times while controlling for factors such as urgency, case complexity, issue category or quantified emotional need. This can help distinguish apparent performance differences from differences caused by case mix.

A simplified research model might look like:

```text
resolution_time ~ department + urgency + frustration + complexity
```

Later phases may also test interactions such as:

```text
resolution_time ~ department * frustration + urgency + complexity
```

The repository will document assumptions and validation requirements instead of treating statistical significance as automatic evidence of causal impact.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest
python -m ancova_ops.demo
```

Run the Phase 1 API:

```bash
uvicorn ancova_ops.api:app --reload
```

By default, API case history is stored in `.ancova_ops/ancova_ops.sqlite3`. To use another local database:

```bash
export ANCOVA_OPS_DB_PATH=/path/to/ancova-ops.sqlite3
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

The route endpoint returns structured issue features, routing, priority, human-review requirements, an explanation trail, and version identifiers for the request-intelligence and routing implementations. The routed case and decision are persisted automatically.

Retrieve the stored case:

```bash
curl http://127.0.0.1:8000/v1/cases/demo-api-001
```

A staff reviewer can confirm or override the latest routing recommendation by posting the complete final routing state. The `decision_id` must reference the latest machine/rule recommendation:

```bash
curl -X POST http://127.0.0.1:8000/v1/cases/demo-api-001/routing-reviews \
  -H "Content-Type: application/json" \
  -d '{
    "decision_id": 1,
    "actor_id": "staff-001",
    "reason": "On-site review requires Security ownership.",
    "department": "security",
    "priority": "critical",
    "requires_human_review": true,
    "secondary_notify": null
  }'
```

The original machine/rule recommendation is not overwritten. The case endpoint exposes both the latest recommendation and latest human review, plus an `effective_routing` view for the current operational state.

Record an observed outcome:

```bash
curl -X PUT http://127.0.0.1:8000/v1/cases/demo-api-001/outcome \
  -H "Content-Type: application/json" \
  -d '{
    "response_time_minutes": 10,
    "resolution_time_minutes": 90,
    "reassigned": false,
    "escalated": false,
    "satisfaction": 8.0
  }'
```

Phase 1 scores are transparent heuristics for development; they are not validated psychological or production risk measures. Human confirmations and overrides are also feedback signals rather than automatically trusted training labels.

## Routing evaluation

Run the deterministic Phase 1 routing benchmark:

```bash
ancova-evaluate
```

Machine-readable output:

```bash
ancova-evaluate --json
```

The first benchmark uses `data/evaluation/hand_authored_v1.json`, which is explicitly labelled as a hand-authored software-development fixture rather than real operational ground truth.

Current transparent-baseline results on that fixture are:

- department accuracy: `10 / 11`;
- high-risk human-review recall: `2 / 5`;
- routing-explanation coverage: `11 / 11`.

These figures are deliberately not perfect. The fixture includes ambiguous leasing wording and safety/security cases that expose weaknesses in the current threshold rules.

A candidate implementation can be compared on the same fixture:

```bash
ancova-evaluate \
  --candidate my_package.my_router:predict \
  --candidate-name experimental-router-v1
```

A candidate is only marked `improved` when it uses the same fixture, does not regress on the comparable headline metrics, and improves at least one of them. See `docs/routing-evaluation.md` for metric definitions and limitations.

## Project principles

- **Human-in-the-loop:** the system supports staff rather than pretending every service case should be fully automated.
- **Evidence before claims:** benchmark or simulated results are labelled clearly; project-specific performance claims require project-specific evidence.
- **Interpretable first:** begin with transparent baseline logic before complex ML.
- **Synthetic-data friendly:** early development uses synthetic or hand-authored cases so the software can be tested without exposing resident or customer data.
- **Auditability:** original cases, routing explanations, implementation versions and human reviews are preserved instead of silently overwritten.
- **Same-dataset comparison:** routing improvements must be demonstrated against the baseline on the same labelled benchmark.
- **Modular:** property management is the first use case, not the only possible domain.

## Repository layout

```text
src/ancova_ops/
├── api.py          # FastAPI routing, review and case-history interface
├── intelligence.py # Transparent raw-text feature baseline
├── models.py       # Core service-case models
├── persistence.py  # SQLite case, machine-decision, review and outcome storage
├── routing.py      # Explainable baseline routing
├── evaluation.py   # Deterministic routing benchmark and candidate comparison
├── synthetic.py    # Synthetic outcome data for development
├── analytics.py    # ANCOVA fitting and diagnostics
└── demo.py         # Small runnable demonstration

data/evaluation/
└── hand_authored_v1.json

docs/
├── hackathon-origin.md
├── architecture.md
├── statistical-methodology.md
├── data-model.md
├── human-routing-feedback.md
├── routing-evaluation.md
└── roadmap.md
```

## Roadmap

### Phase 0 — Foundation

- project structure and development conventions
- service-case data schema
- synthetic dataset generator
- baseline routing engine
- ANCOVA analysis skeleton
- documentation of the hackathon origin and corrected technical architecture

### Phase 1 — Working service-intelligence MVP

- request API
- structured issue extraction
- urgency and contextual scoring
- department classification
- human-readable routing explanation
- case persistence and routing audit log
- outcome capture
- human confirmation / override capture
- deterministic routing evaluation harness

### Phase 2 — Outcome analytics

- reproducible ANCOVA workflow
- model assumption checks
- department and case-mix analysis
- evaluation dashboard / report outputs

### Phase 3 — Adaptive routing

- learn routing policy candidates from historical outcomes
- offline evaluation before deployment
- audit trail for routing decisions

### Phase 4 — Longitudinal prediction

- recurring-case and escalation modelling
- seasonality / user-history experiments
- compare sequence models against simpler baselines before adopting them

## Status

Phase 0 is complete. The Phase 1 MVP foundation now includes the request API, transparent request-intelligence baseline, SQLite case persistence, append-only routing audit history, outcome capture, separate human confirmation/override records, and a deterministic same-dataset routing evaluation harness. Before any real pilot data is introduced, the project still needs explicit privacy and data-governance boundaries; deeper outcome analytics follow in Phase 2.

## Important note on metrics

Figures shown in the original hackathon presentation are not treated here as measured ANCOVA Ops outcomes unless they can be traced to a project-specific experiment. The routing benchmark figures above describe a small hand-authored fixture only and are not production estimates. External benchmarks, simulated examples and target metrics will be labelled as such.

## License

A license has not yet been selected.
