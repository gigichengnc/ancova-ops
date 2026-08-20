# Data Model

## ServiceCase

A service case separates message content, structured context and eventual outcome.

| Field | Type | Purpose |
| --- | --- | --- |
| `case_id` | string | Stable case identifier |
| `message` | string | Original service request |
| `issue_category` | string / null | Structured issue label when known |
| `urgency` | float | Operational urgency on a documented 0-10 scale |
| `frustration` | float | Communication / emotional-need signal on a 0-10 scale |
| `complexity` | float | Estimated operational complexity on a 0-10 scale |
| `previous_related_cases` | int | Count of known related cases |
| `vulnerability_flag` | bool | Indicates extra human-review context |

The original case payload is immutable by `case_id`. Reusing an existing case ID with different
original data is rejected rather than silently overwriting the historical record.

## RoutingDecision

| Field | Type | Purpose |
| --- | --- | --- |
| `department` | string | Recommended primary team |
| `priority` | string | `normal`, `high` or `critical` |
| `requires_human_review` | bool | Whether a person should review before/while routing |
| `secondary_notify` | string / null | Additional team to notify |
| `reasons` | list[string] | Audit-friendly explanation |

Each routing decision is appended as a separate audit record. The persistent record also stores:

- `decision_id`;
- decision timestamp;
- request-intelligence version;
- routing-policy version;
- the exact explanation list returned for that decision.

A case can therefore be re-routed later without deleting the earlier recommendation.

## CaseOutcome

Outcome fields are stored separately from the routing recommendation so that predictions and
observations are not mixed together.

| Field | Type | Purpose |
| --- | --- | --- |
| `response_time_minutes` | float / null | Time until first operational response |
| `resolution_time_minutes` | float / null | Time until case resolution |
| `reassigned` | bool / null | Whether the case changed primary handler/team |
| `escalated` | bool / null | Whether the case required escalation |
| `satisfaction` | float / null | Outcome feedback on a 0-10 scale when collected |

These outcome fields are the beginning of the historical dataset used by later statistical
analysis. Missing values remain missing; the application does not invent replacement outcomes.

## SQLite Phase 1 schema

Phase 1 uses a local SQLite database with four schema objects:

1. `schema_metadata` — explicit schema version;
2. `service_cases` — immutable original request plus structured operational features;
3. `routing_decisions` — append-only routing audit history;
4. `case_outcomes` — latest observed outcome record for a case.

The default development path is `.ancova_ops/ancova_ops.sqlite3`. It can be changed with the
`ANCOVA_OPS_DB_PATH` environment variable. Local SQLite files are ignored by Git.

Schema version `1` is created automatically. Future incompatible changes should include an
explicit migration before incrementing the supported schema version.

## Analytical dataset

The separate synthetic-data generator currently produces one row per completed synthetic case
with columns such as:

- `department`;
- `issue_category`;
- `urgency`;
- `frustration`;
- `complexity`;
- `previous_related_cases`;
- `resolution_hours`;
- `escalated`;
- `satisfaction`;
- `data_provenance`.

A later phase will add an explicit export from persistent real/pilot case records into an
analysis-ready table. Operational storage and analytical datasets should remain distinct.

## Measurement warning

Urgency, frustration and complexity are modelling variables. Their scales need operational
definitions and validation before production use. They should not be described as objective
measurements of a person's mental state.
