# Human Routing Feedback

## Purpose

ReasonedOps keeps the system recommendation and the human operational decision as separate records.
A staff correction must never overwrite the machine/rule recommendation that produced it.

This distinction is necessary for auditability and later evaluation. If a routing model recommends
Maintenance and a staff member changes the case to Security, the database should preserve both:

1. what the system recommended at that time and which versions produced it; and
2. what the reviewer decided, who recorded the review, when it happened, and why.

## Review actions

A routing review is classified automatically as one of two actions:

- `confirmed` — the final department, priority, human-review flag and secondary notification are
  unchanged from the referenced machine/rule recommendation;
- `overridden` — at least one of those operational fields differs.

The API requires the reviewer to submit the complete final routing state rather than only the changed
fields. This removes ambiguity around values such as clearing a secondary notification.

## Audit model

Every review stores:

- `review_id`;
- source `decision_id`;
- timestamp;
- `actor_type` (currently `human_staff`);
- `actor_id`;
- `action` (`confirmed` or `overridden`);
- a short review reason;
- final department;
- final priority;
- final human-review requirement;
- final secondary notification.

Reviews are append-only. The source routing decision remains unchanged in `routing_decisions`.

A review may only target the latest machine/rule recommendation for a case. If a new system routing
decision is created first, a review against an older decision is rejected as stale. This prevents a
human decision from accidentally being applied to a recommendation that is no longer current.

## Effective routing

For operational display, `effective_routing` is resolved as follows:

1. if the latest machine/rule recommendation has a human review, use the latest review's final
   routing state;
2. otherwise use the latest machine/rule recommendation.

This does **not** delete or mutate either history.

## Feedback is not automatically ground truth

A human override is evidence that a reviewer disagreed with a recommendation in a specific context.
It is not automatically a correct training label.

Possible reasons include:

- the system made a classification or routing error;
- the reviewer had information unavailable to the model;
- operational capacity required a temporary reassignment;
- local policy changed before the software was updated;
- the reviewer made a mistake.

Therefore future evaluation should keep at least three concepts separate:

- **system recommendation**;
- **human final operational decision**;
- **observed case outcome**.

Candidate ML training labels should be created only after a defined review/quality process rather
than by copying every override directly into a training set.

## Identity limitation in Phase 1

`actor_id` is currently supplied by the API caller and is not authenticated. It provides an audit
field for development, not verified staff identity. Production deployment would require an
authentication and authorization layer before treating this field as trusted identity evidence.
