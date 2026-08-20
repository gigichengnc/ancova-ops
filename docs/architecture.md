# Architecture

## Design goal

Turn an unstructured service request into a structured, explainable operational decision, record the eventual outcome, and provide a clean dataset for evaluation.

## Layers

### 1. Intake

Receives a message and basic context. Phase 0 keeps this in Python objects; Phase 1 will expose an API.

### 2. Request intelligence

Extracts structured signals such as:

- issue category;
- urgency;
- frustration / emotional need;
- vulnerability or safety context;
- recurrence / prior unresolved cases.

Phase 0 uses transparent inputs and rules. Future NLP components should implement the same interface so they can be evaluated against the baseline.

### 3. Routing

Produces:

- recommended department;
- priority level;
- optional escalation / secondary notification;
- human-readable reasons.

The routing result is a recommendation, not an irreversible autonomous action.

### 4. Outcome collection

The case record should eventually include response time, resolution time, escalation, reassignment and satisfaction when available.

### 5. Analytics

Historical cases become an analytical dataset. ANCOVA / regression models can compare groups while adjusting for pre-specified covariates.

### 6. Adaptive policy — later phase

Only after the baseline pipeline and evaluation protocol are stable should historical outcomes influence routing policy automatically. Candidate policies should be evaluated offline and retain a decision audit trail.

## Current Phase 0 flow

```text
ServiceCase
   |
   v
baseline_route()
   |
   +--> RoutingDecision(department, priority, reasons)
   |
   v
stored / simulated outcome rows
   |
   v
fit_ancova()
```

## Future API boundary

A future request endpoint should return structured JSON rather than prose-only AI output. A likely contract is:

```json
{
  "case_id": "case-123",
  "issue_category": "water_leak",
  "urgency": 8.0,
  "frustration": 7.5,
  "department": "maintenance",
  "priority": "high",
  "requires_human_review": true,
  "reasons": ["water leak", "repeat case", "high urgency"]
}
```

## Non-goals for Phase 0

- no LSTM;
- no resident profiling from private production data;
- no fully autonomous dispatch;
- no claim that emotion scores are objective psychological measurements;
- no causal claims from a convenience dataset.
