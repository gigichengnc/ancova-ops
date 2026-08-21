# Project Status — ReasonedOps v1.2.0

ReasonedOps is a completed local research/software prototype for following a service case through **request → routing → human review → outcome → evaluation**.

**Research/portfolio project:** COMPLETED  
**Current codebase checkpoint:** v1.2.0  
**Real private-data pilot:** NOT APPROVED  
**Production deployment:** NOT APPROVED

## What is implemented

| Area | Working behaviour |
| --- | --- |
| Request intake | Accepts a text service request through the FastAPI `/v1/route` endpoint. |
| Request intelligence | Extracts transparent development-stage issue, urgency, frustration and complexity signals. |
| Routing | Returns a department, priority, human-review flag and reasons. |
| Human review | Staff can confirm or override a routing decision. |
| Audit history | Original machine/rule decisions remain stored after a human override. |
| Outcome capture | Response time, resolution time, reassignment, escalation and satisfaction can be stored separately. |
| Management report | Produces raw summaries, adjusted estimates when supportable, diagnostics and interpretation warnings. |
| Comparison gate | Can withhold a department comparison when department and case type are not separately identifiable. |
| Method gate | Returns `use`, `caution`, `reject` or `recommend_alternative`. |
| Offline policy research | Evaluates candidate routing policies on synthetic logged-policy data. |
| Longitudinal research | Benchmarks recurrence/time-to-next-case models on synthetic histories. |
| Governance check | Enforces the repository's synthetic/private-data development policy. |

## Canonical codebase

From v1.2.0 onward there is one application namespace:

```text
src/reasoned_ops/
```

The temporary legacy `ancova_ops` package used during the v1.1 rename migration has been removed. Public commands use the `reasoned-` prefix.

```text
reasoned-showcase
reasoned-evaluate
reasoned-validity
reasoned-applicability
reasoned-analyze
reasoned-management-report
reasoned-policy
reasoned-longitudinal
reasoned-governance-check
```

## Evaluation boundary

ReasonedOps does not assume every operational comparison is valid.

For a question such as:

```text
Is Department A slower than Department B?
```

it first asks whether the observed case mix allows those departments to be compared. If department and case type cannot be separated, adjusted department estimates and ranking language are withheld.

When the comparison is supportable, the current continuous-outcome workflow can use regression/ANCOVA-style adjustment with diagnostics and uncertainty reporting. ANCOVA is one method inside Evaluate, not the product itself.

Other question types can be redirected to a more appropriate method family rather than forced through the same model.

## Evidence currently in the repository

Current quantitative development evidence is limited to:

- a small hand-authored routing fixture;
- synthetic outcome data;
- synthetic known-truth validity scenarios;
- deterministic applicability rules;
- synthetic logged-policy data;
- synthetic longitudinal histories.

There is no representative real-company or real-resident/customer pilot dataset in v1.2.0.

## What this project does not prove

The repository does **not** prove that ReasonedOps:

- improves real service resolution time;
- improves real routing accuracy;
- causes better staff or department performance;
- is safe to process private resident/customer data;
- is production-ready;
- delivers a measured commercial return on investment.

Those claims would require a separate real-data pilot, governance approval and a defensible evaluation design.

## Project origin

The project originated from my participation in the **HKMU Hackathon 2026** and was originally developed under the name **ANCOVA Ops**. It was renamed **ReasonedOps** in v1.1.0 because ANCOVA/regression is only one method inside the Evaluate layer, not the product itself.
