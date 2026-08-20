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

## RoutingDecision

| Field | Type | Purpose |
| --- | --- | --- |
| `department` | string | Recommended primary team |
| `priority` | string | `normal`, `high` or `critical` |
| `requires_human_review` | bool | Whether a person should review before/while routing |
| `secondary_notify` | string / null | Additional team to notify |
| `reasons` | list[string] | Audit-friendly explanation |

## Outcome dataset

The analytical table currently uses one row per completed synthetic case with columns such as:

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

## Measurement warning

Urgency, frustration and complexity are modelling variables. Their scales need operational definitions and validation before production use. They should not be described as objective measurements of a person's mental state.
