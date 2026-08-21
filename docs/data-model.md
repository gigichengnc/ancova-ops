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

Each machine/rule routing decision is appended as a separate audit record. The persistent record
also stores:

- `decision_id`;
- decision timestamp;
- request-intelligence version;
- routing-policy version;
- the exact explanation list returned for that decision.

A case can therefore be re-routed later without deleting the earlier recommendation.

## RoutingReview

A routing review records a human operational decision separately from the source recommendation.

| Field | Type | Purpose |
| --- | --- | --- |
| `review_id` | int | Stable review event identifier |
| `decision_id` | int | Machine/rule recommendation being reviewed |
| `actor_type` | string | Reviewer type; Phase 1 uses `human_staff` |
| `actor_id` | string | Reviewer identifier supplied by the caller |
| `action` | string | `confirmed` or `overridden` |
| `reason` | string | Short explanation for the human decision |
| final department | string | Final operational owner |
| final priority | string | Final operational priority |
| final human-review flag | bool | Final review/escalation requirement |
| final secondary notification | string / null | Final secondary team notification |

The source `RoutingDecision` is never overwritten. A `confirmed` review means the final operational
fields match the source decision. An `overridden` review means at least one operational field differs.

For a case display, `effective_routing` uses the latest human review of the latest machine/rule
decision when one exists; otherwise it uses the latest machine/rule decision. This is a view of the
current operational state, not a replacement for either audit history.

Human confirmations and overrides are feedback signals, not automatically ground-truth labels.
See `docs/human-routing-feedback.md` for the evaluation and identity limitations.

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

Phase 1 uses a local SQLite database with five main schema objects:

1. `schema_metadata` — explicit schema version;
2. `service_cases` — immutable original request plus structured operational features;
3. `routing_decisions` — append-only machine/rule routing audit history;
4. `routing_reviews` — append-only human confirmations and overrides;
5. `case_outcomes` — latest observed outcome record for a case.

The default development path is `.reasoned_ops/reasoned_ops.sqlite3`. It can be changed with the
`ANCOVA_OPS_DB_PATH` environment variable. Local SQLite files are ignored by Git.

Schema version `2` adds `routing_reviews`. Databases created under schema version `1` are migrated
automatically to version `2` without rewriting existing case or routing records.

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
analysis-ready table. Operational storage and analytical datasets should remain distinct. The export
should preserve system recommendation, human final decision and observed outcome as separate fields.

## Measurement warning

Urgency, frustration and complexity are modelling variables. Their scales need operational
definitions and validation before production use. They should not be described as objective
measurements of a person's mental state.
