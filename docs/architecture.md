# Architecture

## Design goal

Turn an unstructured service request into a structured, explainable operational decision, record the eventual outcome, and provide a clean dataset for evaluation.

## Layers

### 1. Intake

The FastAPI interface accepts a raw service message plus limited operational context such as known related-case count and an explicit vulnerability flag.

### 2. Request intelligence

Extracts structured signals such as:

- issue category;
- urgency;
- frustration / communication intensity;
- vulnerability or safety context;
- recurrence / prior unresolved cases.

Phase 1 uses a transparent deterministic baseline. Future NLP components should implement the same interface so they can be evaluated against the baseline.

### 3. Routing

Produces:

- recommended department;
- priority level;
- optional escalation / secondary notification;
- human-readable reasons.

The routing result is a recommendation, not an irreversible autonomous action. Both the request-intelligence implementation and routing policy carry explicit version identifiers.

### 4. Persistence and audit trail

A file-backed SQLite store records:

- the immutable original service case;
- structured operational features used at routing time;
- every routing decision as a separate audit row;
- request-intelligence and routing-policy versions;
- exact routing reasons;
- later observed outcomes.

Re-running the same unchanged case can append another routing decision. Reusing a `case_id` with different original case data is rejected to prevent silent historical rewrites.

The default local database is `.ancova_ops/ancova_ops.sqlite3`. It is ignored by Git and can be replaced with the `ANCOVA_OPS_DB_PATH` environment variable.

### 5. Outcome collection

The API can store observed response time, resolution time, reassignment, escalation and satisfaction when available. Outcome data is kept separate from routing recommendations so predictions and observations are not conflated.

### 6. Analytics

Historical cases can later be exported into an analytical dataset. ANCOVA / regression models can compare groups while adjusting for pre-specified covariates.

### 7. Adaptive policy — later phase

Only after the baseline pipeline and evaluation protocol are stable should historical outcomes influence routing policy automatically. Candidate policies should be evaluated offline and retain the same decision audit trail.

## Current Phase 1 flow

```text
POST /v1/route
      |
      v
BaselineRequestIntelligence
      |
      v
ServiceCase
      |
      v
baseline_route()
      |
      v
RoutingDecision
      |
      +----> SQLite routing audit history
      |
      v
human/service operation
      |
      v
PUT /v1/cases/{case_id}/outcome
      |
      v
observed outcome
      |
      v
future analytics export -> ANCOVA / regression
```

## Current API boundary

A routing response is structured JSON rather than prose-only AI output. It includes the decision and the implementation versions needed to reconstruct it:

```json
{
  "case_id": "case-123",
  "decision_id": 17,
  "issue_category": "water_leak",
  "urgency": 8.0,
  "frustration": 7.5,
  "complexity": 6.5,
  "department": "maintenance",
  "priority": "high",
  "requires_human_review": true,
  "secondary_notify": "community_management",
  "reasons": ["matched baseline issue taxonomy: water_leak"],
  "intelligence_version": "baseline-request-intelligence-v1",
  "router_version": "baseline-route-v1"
}
```

Audit and outcome endpoints:

- `GET /v1/cases/{case_id}` — retrieve the persisted case, latest decision and outcome;
- `GET /v1/cases/{case_id}/routing-decisions` — retrieve full routing audit history;
- `PUT /v1/cases/{case_id}/outcome` — add or update observed outcome fields.

## Non-goals for Phase 1

- no LSTM;
- no resident profiling from private production data;
- no fully autonomous dispatch;
- no claim that operational scores are objective psychological measurements;
- no causal claims from a convenience dataset;
- no real private service records committed to Git.
