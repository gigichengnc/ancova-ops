# Public package verification — ReasonedOps 1.4.0

ReasonedOps 1.4.0 was published as the public PyPI distribution **`reasoned-ops`** and then installed from PyPI in a Windows environment outside the repository checkout.

This record documents package distribution and executable local behaviour. It is **not** independent scientific validation and does not establish real-world service effectiveness, causal impact, private-data approval, or production readiness.

## Package installation

The released package was installed from PyPI and the installed version was verified with:

```powershell
python -c "import reasoned_ops; print(reasoned_ops.__version__)"
```

Observed version:

```text
1.4.0
```

## Operate verification

The public package was imported directly and the baseline routing surface was exercised:

```powershell
python -c "from reasoned_ops import ServiceCase, baseline_route; case=ServiceCase(case_id='test-001', message='The air conditioner is leaking again.', previous_related_cases=2); decision=baseline_route(case); print('Department:', decision.department); print('Priority:', decision.priority); print('Human review:', decision.requires_human_review); print('Reasons:', decision.reasons)"
```

Observed behaviour:

```text
Department: maintenance
Priority: high
Human review: True
```

The returned reasons included maintenance-related language, high-priority context, recurrence/history and a secondary community-management notification.

The FastAPI application was then started from the installed package:

```powershell
python -m uvicorn reasoned_ops.api:app --reload
```

A test service request was submitted to `POST /v1/route`. The response recorded:

```text
case_id: demo-001
issue_category: air_conditioning
department: maintenance
priority: high
requires_human_review: True
```

The route was persisted with a routing `decision_id`.

## Audit verification

A human review was submitted for the same persisted case. The review changed the effective route from the machine recommendation `maintenance` to `community_management`, with `maintenance` retained as the secondary notification.

A subsequent `GET /v1/cases/demo-001` showed all of the following at the same time:

```text
latest machine decision: maintenance
latest human review: overridden → community_management
effective routing source: human_review
effective department: community_management
```

The original machine recommendation remained present rather than being overwritten.

An outcome was then stored separately:

```text
response_time_minutes: 20
resolution_time_minutes: 300
reassigned: True
escalated: False
satisfaction: 8
```

A later case fetch returned the original request, machine decision, human override, effective route and outcome together.

## Evaluate verification

The installed CLI was used to run the deterministic synthetic validity benchmark:

```powershell
reasoned-validity
```

Observed summary:

```text
Overall pass: True
- known_effect_recovery: PASS
- measured_confounding: PASS
- no_overlap: PASS
- slope_interaction: PASS
```

The detailed JSON run also showed:

- known-effect recovery within the configured tolerance;
- a deliberately confounded naive estimate with the wrong sign, while case-mix adjustment recovered a value close to the known synthetic truth;
- a `not_identifiable` result with zero adjusted estimates in the no-overlap scenario;
- detection of the deliberately introduced department-specific urgency slope.

These are synthetic known-truth tests. They verify statistical/software behaviour under controlled scenarios, not performance on real service data.

## What this verification establishes

The public `reasoned-ops==1.4.0` artifact was shown to be installable and executable outside the repository checkout, with a working path through:

```text
Operate
request → route → explanation
        ↓
Audit
machine decision → human override → persisted history → outcome
        ↓
Evaluate
known-truth recovery → confounding adjustment → no-overlap refusal → interaction detection
```

This supports the repository claim that ReasonedOps is a **publicly distributed, independently installable local research/software prototype**.

Here, "independently installable" means that the public package can be installed and run in another environment. It does **not** mean independently validated scientific effectiveness.
