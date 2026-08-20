# Architecture

## Design goal

ANCOVA Ops separates operational decision support from downstream evaluation. The system turns an unstructured service request into a structured, explainable routing recommendation, preserves human intervention and observed outcomes, and then uses those records in separate statistical and offline research workflows.

ANCOVA is an **outcome-analysis layer**, not a per-message scoring algorithm.

## v0.5.0 system map

```text
Service request
      |
      v
Request intelligence
(issue, urgency, communication intensity, context)
      |
      v
Explainable routing recommendation
      |
      +------> Human confirmation / override
      |                |
      |                v
      |        Effective operational routing
      |
      v
Observed service outcome
      |
      v
Auditable historical records
      |
      +------> Routing benchmark
      |
      +------> ANCOVA / regression + diagnostics
      |                |
      |                v
      |        Management evidence report
      |
      +------> Offline adaptive-policy research
      |        (time-aware validation, IPS, approval, rollback)
      |
      +------> Synthetic longitudinal benchmark
               (recency/frequency, survival-style, tree models)
```

## Layer 1 — Intake and request intelligence

The FastAPI interface accepts raw service text plus limited operational context. `BaselineRequestIntelligence` converts that input into structured features such as issue category, urgency, communication/frustration intensity, complexity and recurrence context.

The current implementation is deliberately transparent and deterministic. These values are operational development heuristics, not validated psychological measurements.

## Layer 2 — Explainable routing

`baseline_route()` produces a versioned recommendation containing:

- department;
- priority;
- human-review requirement;
- optional secondary notification;
- human-readable reasons.

The recommendation is not an irreversible autonomous dispatch action.

## Layer 3 — Persistence and human review

The local SQLite layer preserves:

- immutable original service cases;
- structured features used at routing time;
- append-only machine/rule routing decisions;
- implementation versions and routing reasons;
- append-only human confirmations or overrides;
- observed outcomes stored separately from predictions.

Human review changes the effective operational state without overwriting the original recommendation. Staff confirmation is feedback, not automatically trusted model-training ground truth.

## Layer 4 — Routing evaluation

`ancova-evaluate` runs a deterministic hand-authored fixture through the routing pipeline. It reports department accuracy, expected-human-review recall and explanation coverage.

The fixture is a software-development benchmark, not representative production data.

## Layer 5 — Data-governance gate

`config/data-governance.json` defines the current development boundary. `ancova-governance-check` validates it in CI.

The repository is synthetic-only for model/analytics development. Real private resident/customer records, direct identifiers, unsupported psychological profiling and unapproved longitudinal personalisation are prohibited.

## Layer 6 — Outcome analytics

`ancova-analyze` fits the pre-specified ANCOVA/regression workflow and exposes:

- required-field missingness and complete-case counts;
- department group sizes;
- residual diagnostics;
- heteroskedasticity screening;
- VIF multicollinearity diagnostics;
- influence screening;
- department-by-covariate interaction checks;
- adjusted department estimates with uncertainty;
- explicit warnings and alternative-model guidance.

Adjusted estimates are model-based associations. They are not causal effects without a separate identification argument and study design.

## Layer 7 — Management reporting

`ancova-management-report` converts the technical analysis into a self-contained Markdown/JSON evidence report. It keeps raw observed summaries separate from adjusted estimates and carries statistical warnings into the management view.

The report is not a staff-performance league table.

## Layer 8 — Offline adaptive-routing research

`ancova-policy evaluate` uses deterministic synthetic logged-routing history with timestamps and known action propensities. Candidate policies are trained on an earlier window and compared on a later window with support-aware inverse-propensity methods.

The lifecycle registry supports candidate registration, named human approval, activation history and rollback. Registry activation does **not** replace the router behind `/v1/route`; deployment integration is intentionally separate.

## Layer 9 — Longitudinal benchmark

`ancova-longitudinal` generates synthetic entity-level service histories with recurrence and seasonality, creates pre-cutoff feature snapshots, and applies a purged chronological split so training follow-up cannot overlap the validation period.

The current benchmark compares:

1. recency/frequency logistic baseline;
2. discrete-time logistic hazard model;
3. random-forest recurrence classifier.

LSTM/sequence modelling remains deferred until a same-benchmark experiment can demonstrate reproducible incremental value over the strongest simpler approach.

## Current API boundary

A routing response is structured JSON with the decision and implementation versions required for reconstruction. Core endpoints are:

- `POST /v1/route` — create and persist a routing recommendation;
- `GET /v1/cases/{case_id}` — retrieve case, current effective routing and outcome;
- `GET /v1/cases/{case_id}/routing-decisions` — retrieve machine/rule decision history;
- `POST /v1/cases/{case_id}/routing-reviews` — append a human confirmation or override;
- `GET /v1/cases/{case_id}/routing-reviews` — retrieve human-review history;
- `PUT /v1/cases/{case_id}/outcome` — store observed outcome fields.

## Separation of responsibilities

```text
Request intelligence answers:  "What does this request appear to need?"
Routing answers:               "Where should it go now?"
Human review answers:          "Do staff accept or override that recommendation?"
Outcome capture answers:       "What actually happened?"
ANCOVA/regression answers:     "How do outcomes compare after case-mix adjustment?"
Adaptive-policy research asks: "Could historical outcomes inform a better policy offline?"
Longitudinal research asks:    "Can recurrence/timing be predicted without avoidable leakage?"
Governance answers:            "Which data/use/deployment steps are currently permitted?"
```

## v0.5.0 deployment boundary

The architecture is runnable as a development prototype but is not approved for private-data pilot or production deployment. Production authentication/RBAC, secrets management, real-data validation, monitoring, incident response and policy-to-route integration remain future work.

See `docs/project-status.md` and `docs/release-readiness.md` for the checkpoint boundary.
