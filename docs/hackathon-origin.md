# Hackathon Origin

ANCOVA Ops originates from a Spring 2026 HKMU Hackathon proposal for a next-generation concierge / virtual-assistance system.

## Original problem framing

The proposal focused on service requests in property management. A resident or tenant submits a maintenance request, complaint or inquiry; staff then need to understand the actual operational need, manage emotional or urgency signals, hand the case between departments, and report progress back to the user.

The proposal identified two related problems:

- repetitive communication and cross-department handover create operational workload;
- emotional context matters to the service interaction, but it can become mixed with the underlying task that needs to be resolved.

## Original proposed flow

The hackathon deck described a pipeline broadly equivalent to:

```text
new request
  -> NLP / current emotion
  -> department classification
  -> historical context
  -> adaptive routing
  -> department queue
  -> outcome feedback
```

It also proposed learning from recurring complaints, seasonal needs, escalation paths and longitudinal user history.

## Technical clarification made in this repository

The original slides sometimes described emotion filtering as being "achieved by ANCOVA". This repository corrects that architecture.

**ANCOVA is not used to parse or filter an individual message.** NLP, rules or classifiers perform request understanding. Analysis of covariance is used downstream on accumulated outcome data to test whether operational factors are associated with outcomes after adjusting for relevant covariates.

This separation is central to the rebuild:

```text
message understanding -> operational decision -> outcome data -> ANCOVA / evaluation
```

## Human role

A core idea from the hackathon proposal is retained: automation should not simply remove the concierge or service worker. Routine triage and structuring can be automated so staff can spend more time on difficult cases, vulnerable users, community interaction and other work where human judgement matters.

## Historical metrics

The original presentation included several percentages and projected business outcomes. They are treated as presentation-era benchmarks, hypotheses or illustrative figures unless a project-specific experiment and source can be reconstructed. They must not be presented as measured performance of the software in this repository.
