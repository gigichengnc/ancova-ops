# Project Status — ReasonedOps v1.3.0

ReasonedOps is a completed local research/software prototype and retrospective rebuild of an **HKMU Hackathon 2026** concierge concept.

The current project story is:

```text
original concept
      ↓
audit assumptions
      ↓
rebuild as Operate → Audit → Evaluate
      ↓
validate software behaviour with public development evidence
      ↓
define the next real evidence gate
```

**Research/portfolio project:** COMPLETED  
**Current portfolio/code checkpoint:** v1.3.0  
**Real private-data pilot:** NOT APPROVED  
**Production deployment:** NOT APPROVED

## What is implemented

| Area | Working behaviour |
| --- | --- |
| Request intake | Accepts a text service request through the FastAPI `/v1/route` endpoint. |
| Request intelligence | Extracts transparent development-stage issue, urgency, communication-intensity and complexity signals. |
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
| Rebuild record | Preserves the reconstructed original concept, before/after comparison, concept audit and model decisions. |

## Portfolio narrative

From v1.3.0, the repository is intentionally presented as a **rebuild case study**, not as a startup-style product landing page.

Start with:

1. [`../original/README.md`](../original/README.md) — reconstructed original Hackathon concept;
2. [`before-vs-after.md`](before-vs-after.md) — original concept vs current rebuild;
3. [`original-concept-audit.md`](original-concept-audit.md) — assumptions preserved/corrected/deferred;
4. [`model-decisions.md`](model-decisions.md) — why methods/models were selected, rejected or deferred;
5. [`../README.md`](../README.md) — runnable overview and portfolio story.

## Canonical codebase

There is one application namespace:

```text
src/reasoned_ops/
```

Public commands use the `reasoned-` prefix:

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

There is no representative real-company or real-resident/customer pilot dataset in v1.3.0.

## What this project does not prove

The repository does **not** prove that ReasonedOps:

- improves real service resolution time;
- improves real routing accuracy;
- causes better staff or department performance;
- is safe to process private resident/customer data;
- is production-ready;
- delivers a measured commercial return on investment.

Those claims require a separate real-data pilot, governance approval and a defensible evaluation design.

## Next evidence gate

The research/portfolio project is complete. If ReasonedOps is ever resumed for a real use case, the next substantive step is not another synthetic model. It is a controlled real-data evidence process with privacy/governance approval, representative cases, predefined evaluation questions and explicit stop criteria.

## Project origin

The project originated from my participation in **HKMU Hackathon 2026** and was originally developed under the name **ANCOVA Ops**. It was renamed **ReasonedOps** because ANCOVA/regression is only one method inside the Evaluate layer, not the product itself.
