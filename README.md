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
Routing and human hand-off
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

The endpoint returns structured issue features, routing, priority, human-review requirements and an explanation trail. Phase 1 scores are transparent heuristics for development; they are not validated psychological or production risk measures.

## Project principles

- **Human-in-the-loop:** the system supports staff rather than pretending every service case should be fully automated.
- **Evidence before claims:** benchmark or simulated results are labelled clearly; project-specific performance claims require project-specific evidence.
- **Interpretable first:** begin with transparent baseline logic before complex ML.
- **Synthetic-data friendly:** early development uses synthetic cases so the software can be tested without exposing resident or customer data.
- **Modular:** property management is the first use case, not the only possible domain.

## Repository layout

```text
src/ancova_ops/
├── api.py          # FastAPI request / routing interface
├── intelligence.py # Transparent raw-text feature baseline
├── models.py       # Core service-case models
├── routing.py      # Explainable baseline routing
├── synthetic.py    # Synthetic outcome data for development
├── analytics.py    # ANCOVA fitting and diagnostics
└── demo.py         # Small runnable demonstration

docs/
├── hackathon-origin.md
├── architecture.md
├── statistical-methodology.md
├── data-model.md
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
- case persistence

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

Phase 0 is complete. Phase 1 is in progress: the first API and transparent request-intelligence baseline are being added before persistence or ML integration.

## Important note on metrics

Figures shown in the original hackathon presentation are not treated here as measured ANCOVA Ops outcomes unless they can be traced to a project-specific experiment. External benchmarks, simulated examples and target metrics will be labelled as such.

## License

A license has not yet been selected.
