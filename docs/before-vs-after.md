# Before vs after: Hackathon concierge concept to ReasonedOps

This document explains the main conceptual and engineering changes between the original HKMU Hackathon 2026 concierge proposal and the current ReasonedOps project.

The goal is not to present the original idea as a failed or separate project. The Hackathon proposal supplied the problem, the first architecture, and several useful human-centred ideas. ReasonedOps is the same project evolved through implementation, audit and tighter evidence boundaries.

## One-page comparison

| Area | Original concept | ReasonedOps today | Why the change matters |
| --- | --- | --- | --- |
| Product centre | AI concierge / intelligent routing | Operate → Audit → Evaluate | Routing is only one part of a trustworthy operational system |
| Request understanding | NLP + emotional/context signals | **Rule-based request features for issue, urgency, communication intensity, complexity and recurrence** | The current baseline is transparent and does not pretend a keyword/rule system is a trained NLP model |
| ANCOVA | Described too close to emotion filtering / message processing | Downstream outcome-analysis method only | ANCOVA cannot parse an individual message |
| Routing | Department classification / adaptive path | Deterministic explainable recommendation with reasons and human-review flag | A route should be reconstructable and challengeable |
| Human role | Human-centred idea present conceptually | Append-only confirm / override records | Human intervention becomes auditable instead of disappearing into the final state |
| Decision history | Not the main design object | Original request, machine decision, human review, effective route and outcome are separate records | Later questions can reconstruct what actually happened |
| Outcome data | Feedback loop idea | Outcome stored separately from routing decision | The system does not rewrite the decision after learning the result |
| Department comparison | Could be read from operational averages | Case-type overlap and identifiability are checked first | Different teams may handle fundamentally different work |
| Statistical output | Risk of treating adjusted results as definitive | Raw summaries, adjusted estimates, diagnostics, warnings and non-causal boundaries are separated | A polished number is not automatically a valid conclusion |
| Unsupported comparison | No explicit refusal behaviour | `not_identifiable` can withhold adjusted ranking | Sometimes the correct answer is “the data cannot support this comparison” |
| Hidden confounding | Not represented as a testable limitation | Synthetic blind-spot scenario deliberately omits a true confounder before evaluation | Passing observed-data checks cannot prove that every important cause was measured |
| Method choice | ANCOVA had a central identity | Applicability gate returns `use`, `caution`, `reject`, or `recommend_alternative` | Method follows the question rather than the project name |
| Binary / censored / clustered outcomes | Not clearly separated | Redirected to logistic-, survival-, or cluster-aware method families | Different data structures require different methods |
| Adaptive routing | Long-term adaptive idea | Offline policy evaluation with support diagnostics and explicit deployment lock | Historical-policy research is not silently turned into live automation |
| Longitudinal modelling | Recurring / seasonal / history ideas | Leakage-aware synthetic recurrence benchmark | Future information must not leak into historical prediction |
| LSTM / sequence model | Complexity could appear like progress | Explicitly deferred unless it shows incremental value over simpler baselines | More complex is not automatically better |
| Performance percentages | Presentation-era targets / illustrative figures | Not treated as ReasonedOps results | Proposal claims are separated from measured software evidence |
| Data governance | Not a complete deployment design | Machine-readable synthetic-only development policy | Public research code is not approval to process private resident/customer data |
| Project identity | ANCOVA Ops | ReasonedOps | ANCOVA is one tool inside Evaluate, not the project itself |

## 1. The most important conceptual correction

The largest correction was separating **real-time operational work** from **downstream evaluation**.

### Early direction

Conceptually, the Hackathon proposal could be read as:

```text
message
  ↓
NLP / emotion
  ↓
ANCOVA-assisted filtering
  ↓
routing
```

That places a statistical outcome-analysis method in the wrong part of the system.

### Current direction

ReasonedOps separates the tasks:

```text
rule-based request features
        ↓
operational recommendation
        ↓
human review
        ↓
observed outcome
        ↓
evaluation question
        ↓
comparability + method check
        ↓
regression / ANCOVA or another method when appropriate
```

ANCOVA is now used only where its assumptions and question make sense. The current request-processing baseline is intentionally simple and inspectable; a future NLP/ML model would need to demonstrate incremental value rather than being assumed superior.

## 2. From a final route to an auditable decision chain

A final department field does not tell a reviewer enough.

ReasonedOps keeps the operational history conceptually separate:

```text
Original request
      ↓
Machine / rule recommendation
      ↓
Human confirmation or override
      ↓
Effective route
      ↓
Observed outcome
```

This makes questions such as these answerable:

- What did the system recommend at the time?
- Which version produced the recommendation?
- Why did it recommend that route?
- Did a staff member change it?
- What outcome was later recorded?

Human review does not erase the original machine history and is not automatically treated as model-training ground truth.

## 3. From dashboard averages to comparison support

Suppose a dashboard reports:

```text
Maintenance  18 hours
Security      7 hours
```

The raw difference is descriptive. It is not automatically a performance difference.

ReasonedOps asks whether departments have enough comparable case types and whether the observed design can statistically separate department from case mix.

If the design is not identifiable, the adjusted comparison is withheld instead of converted into a league table.

## 4. From “use ANCOVA” to “what question are we actually asking?”

The applicability gate can return:

```text
use
caution
reject
recommend_alternative
```

Examples:

- continuous resolution-time comparison with supported observed overlap → regression / ANCOVA-style workflow may be suitable;
- binary resolved/unresolved outcome → recommend a logistic-type model;
- censored time-to-resolution → recommend survival / time-to-event analysis;
- repeated observations within sites or teams → recommend cluster-aware / hierarchical analysis;
- routing-policy counterfactual → recommend offline policy evaluation;
- causal claim without a causal design → do not convert an adjusted association into a causal conclusion;
- no department/case-type overlap → reject the ranking question.

The important design decision is that **ANCOVA is allowed to be the wrong method**.

## 5. A refusal system can still miss a reason to refuse

The original validity suite tested situations where the software should recover a known effect, reduce measured confounding, refuse no-overlap comparisons, or detect a visible slope interaction.

An external audit identified the missing failure class: **unmeasured confounding**.

ReasonedOps now includes a deterministic scenario where a latent case-burden variable affects both department assignment and outcome. The benchmark knows this variable, then drops it before handing the frame to the normal evaluation pipeline.

The implemented observed-data checks can therefore look supportable while the adjusted answer is still badly wrong:

```text
true hidden case burden
        ↓
affects department + outcome
        ↓
hidden column removed
        ↓
observed overlap looks supported
        ↓
gate returns USE
        ↓
adjusted contrast reverses the known true direction
```

This is recorded as a **known limitation**, not as successful hidden-confounder detection. A `PASS` means the benchmark successfully reproduces and discloses the false-negative mode.

The practical lesson is narrower and more defensible than “the safeguards catch bad comparisons”: they catch some unsupported comparisons visible in the recorded design, while unrecorded confounding remains outside what ordinary diagnostics can certify.

## 6. From “more AI” to controlled model escalation

The project does not treat model complexity as progress by itself.

The routing baseline is rule-based and deterministic. The longitudinal benchmark compares simpler approaches on the same synthetic development problem. LSTM / sequence modelling remains deferred because the current evidence does not justify escalating to it.

The same principle applies to adaptive routing: a candidate can be studied offline, but an offline signal does not authorise live deployment.

## 7. From proposal metrics to evidence classes

ReasonedOps separates evidence into explicit classes:

```text
hand-authored routing fixtures
synthetic outcomes
synthetic known-truth validity scenarios
synthetic known-limitation scenario
synthetic logged-policy data
synthetic longitudinal histories
public package execution evidence
```

There is no representative real-pilot evidence in the repository.

Therefore the project can demonstrate software behaviour, reproducibility, auditability, observed-data guardrails and known synthetic failure modes. It cannot claim that ReasonedOps has improved real service resolution time, satisfaction, routing accuracy, staff performance or causal outcomes.

## 8. What now actually runs

The current project contains working local workflows for:

- FastAPI rule-based request routing;
- SQLite persistence;
- human confirm / override history;
- separate outcome capture;
- routing benchmark;
- guarded regression / ANCOVA outcome analysis;
- management-facing Markdown/JSON report;
- evaluation applicability decisions;
- unmeasured-confounding blind-spot benchmark;
- offline adaptive-policy research;
- leakage-aware longitudinal benchmarking;
- synthetic-only governance checks;
- one-command portfolio showcase;
- Python 3.11 / 3.12 CI.

## 9. What ReasonedOps still does not prove

ReasonedOps is a completed research / portfolio prototype, but it does not prove:

- real-world routing accuracy;
- real service improvement;
- absence of unmeasured confounding;
- causal department or staff effects;
- private-data pilot readiness;
- production security or reliability;
- commercial ROI.

Those require representative data, governance approval, and a study design matched to the real operational question.

## What the project now demonstrates

The strongest portfolio story is not “I built an ANCOVA product” or “I replaced rules with AI.”

It is:

```text
hackathon service concept
        ↓
audit the original assumptions
        ↓
separate operational and analytical tasks
        ↓
build a transparent rule-based routing baseline
        ↓
preserve human + machine decision history
        ↓
record outcomes separately
        ↓
check whether comparisons are supportable
        ↓
benchmark a failure the checks cannot see
        ↓
choose or reject analytical methods
        ↓
defer complexity that is not justified
        ↓
define the next real evidence gate
```

That progression is the main result of ReasonedOps.
