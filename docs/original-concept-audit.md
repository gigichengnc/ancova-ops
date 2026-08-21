# Original concept audit

This document records the main assumptions from the HKMU Hackathon 2026 concierge concept that were preserved, corrected, narrowed, or deferred during the ReasonedOps rebuild.

It is an audit of the project idea, not a criticism of the original student proposal. The purpose is to make the reasoning behind the rebuild visible.

## Audit summary

| Original idea | Audit finding | Rebuild decision |
| --- | --- | --- |
| Use NLP to understand requests | Useful, but operational signals must be separated from unsupported psychological inference | Keep transparent request intelligence for issue, urgency, communication intensity, complexity and recurrence |
| Use emotional context in routing | Context can matter, but a heuristic score is not a validated mental-state measurement | Treat it as communication / escalation context, not psychology |
| Use ANCOVA to help separate emotion from the request | Incorrect task placement | Move ANCOVA downstream to accumulated outcome analysis |
| Route requests to departments automatically | Useful as decision support, risky as irreversible automation | Return explainable recommendation + human-review flag |
| Learn from history | Potentially useful, but history introduces privacy, leakage and causal confounding risks | Keep synthetic-only longitudinal research until governance and evidence justify real histories |
| Improve routing adaptively | Potentially useful, but historical logs do not automatically prove a new policy is better | Keep candidate policy evaluation offline with propensity / overlap diagnostics |
| Compare department performance | Useful question only when comparable cases exist | Check case-type overlap / identifiability before adjusted comparison |
| Use more advanced sequence models later | Possible, but complexity must beat simpler baselines | Defer LSTM until incremental value is demonstrated |
| Present projected performance percentages | Appropriate as proposal targets only if labelled clearly | Do not treat presentation-era percentages as measured ReasonedOps results |

## 1. Request intelligence

The original proposal correctly recognised that service requests arrive as messy natural language rather than clean operational fields.

That problem remains central.

The rebuild therefore keeps a request-intelligence layer that extracts development features such as:

- issue category;
- urgency;
- communication / frustration intensity;
- complexity;
- recurrence context;
- limited vulnerability context when explicitly supplied.

However, these development scores are not presented as validated psychological measurements.

### Boundary

ReasonedOps may support operational triage from declared text/context. It does not infer personality, diagnose mental state, or treat frustration heuristics as clinical evidence.

## 2. ANCOVA placement

The original presentation sometimes placed ANCOVA too close to the task of separating emotional/contextual signals from the underlying request.

That is a category error.

ANCOVA/regression is a method for analysing outcomes across observations while adjusting for measured covariates. It does not understand the semantics of one message.

The rebuild therefore separates:

```text
request understanding
        ↓
routing decision
        ↓
completed outcomes
        ↓
statistical evaluation
```

This correction became one of the main intellectual changes in the project.

## 3. Human role and accountability

The original proposal was human-centred in spirit: automation should reduce repetitive triage so staff can spend more time on difficult or vulnerable cases.

The rebuild turns that principle into data structure.

Machine/rule routing and human review are stored separately. A human override changes the effective route without deleting the original recommendation.

This means disagreement remains visible rather than being overwritten.

## 4. Outcome evaluation and misleading dashboards

Operational systems generate attractive summary metrics quickly.

That creates a second problem: managers may compare teams or policies that handled different kinds of work.

ReasonedOps therefore treats a raw mean as a description, not a performance verdict.

Before adjusted department estimates are reported, the evaluation layer checks whether department and case type are sufficiently separable in the observed design.

When there is structural no-overlap, the correct output is a refusal to rank rather than a statistically decorated number.

## 5. Causal language

A regression coefficient does not automatically answer:

> What would have happened if the same case had been sent somewhere else?

ReasonedOps therefore uses non-causal interpretation by default.

A causal claim requires a defensible identification strategy, study design, and assumptions beyond ordinary adjusted regression.

## 6. Adaptive routing

Historical outcomes can motivate a candidate routing policy, but the logs were produced by an existing policy. That creates support and counterfactual problems.

The rebuild therefore keeps adaptive routing as an offline research workflow with:

- chronological train/validation separation;
- known propensities in synthetic logged-policy data;
- inverse-propensity estimators;
- overlap / unsupported-action diagnostics;
- effective sample-size checks;
- human approval/version/rollback records;
- an explicit deployment lock.

Passing an offline gate does not replace the live baseline router.

## 7. Longitudinal personalisation

Recurring cases and seasonality are plausible sources of operational value, but real longitudinal histories can create privacy and leakage risks.

The current benchmark therefore uses deterministic synthetic histories and time-aware validation.

Real longitudinal personalisation remains outside the approved development boundary.

## 8. Presentation-era performance claims

The original hackathon material included projected efficiency, service, and business-impact percentages.

Those figures are not treated as measured results of the current software unless a source and project-specific experiment can be reconstructed.

ReasonedOps therefore distinguishes:

```text
proposal target / illustrative figure
        ≠
software-development benchmark
        ≠
real-pilot result
        ≠
production performance
```

## 9. Project-name audit

The name **ANCOVA Ops** made sense as an early intellectual hook because ANCOVA motivated part of the project.

After the rebuild, that name became misleading because the system can explicitly decide that ANCOVA is the wrong method.

The project was therefore renamed **ReasonedOps**.

The current identity is:

> **Operate → Audit → Evaluate**

The goal is not to make management decisions automatically. The goal is to make unsupported management conclusions harder to reach.

## Result of the audit

The rebuild did not simply add more code to the original proposal.

It changed the project question from:

> How can an AI concierge route requests more intelligently?

into a broader question:

> How can a service-operations system make explainable recommendations, preserve accountability, and prevent its own operational data from being over-interpreted later?

That change is the main reason ReasonedOps exists in its current form.
