# Original concept reconstruction — HKMU Hackathon 2026

This directory preserves the **starting point** of the project before it became ReasonedOps.

The project originated from my participation in **HKMU Hackathon 2026**. The original proposal explored a next-generation concierge / virtual-assistance system for service operations, initially framed around property-management requests.

This file is a public reconstruction of the concept. It is **not** a verbatim copy of the original presentation and does not publish private, copyrighted, or presentation-only source material.

## Original question

The early project asked a practical question:

> Can an AI-assisted concierge understand a resident or tenant request, recognise operational urgency and communication context, and route the case to the right service team more effectively?

The proposed workflow was broadly:

```text
resident / tenant request
        ↓
NLP + current emotional / contextual signals
        ↓
department classification
        ↓
historical context
        ↓
adaptive routing
        ↓
department queue
        ↓
outcome feedback
```

The proposal also discussed recurring complaints, seasonal needs, escalation paths and longer-term user history.

## What was useful in the original idea

Several ideas survived the rebuild:

- unstructured service requests should be converted into structured operational cases;
- routing should be explainable rather than a black-box department label;
- urgency and communication context can matter to triage;
- people should remain able to review or override automation;
- outcomes should feed back into later evaluation;
- repeated and longitudinal service patterns may become useful once enough appropriate data exist.

## What was incomplete or technically wrong

The original concept mixed together several different tasks.

### 1. ANCOVA was placed too close to message understanding

The presentation sometimes described ANCOVA as helping to filter or separate emotional factors in an individual message.

That is not a valid role for ANCOVA.

ANCOVA/regression can be useful **after many completed cases exist**, for example when asking whether observed outcome differences remain after adjusting for measured case mix. It is not a text parser, emotion detector, or per-message routing algorithm.

### 2. Routing and evaluation were not clearly separated

The early concept focused heavily on getting a request to the right department. It did not yet make the decision trail itself a first-class object:

```text
what the user said
what the system recommended
why it recommended that route
whether a staff member changed it
what the final route became
what outcome followed
```

Without that history, later evaluation becomes much harder to audit.

### 3. Management comparisons could still be misleading

A dashboard can show that one department takes longer than another without showing whether those departments handled comparable work.

For example:

```text
Maintenance  18 hours
Security      7 hours
```

That does not prove Maintenance performs worse if Maintenance mainly receives complex repair cases while Security mainly receives simpler complaints.

The rebuild therefore added overlap / identifiability checks before adjusted department comparisons are reported.

### 4. Presentation targets were not software evidence

The original presentation included projected percentages and business-impact figures. Those figures are treated as presentation-era hypotheses, targets or illustrative benchmarks unless their source and project-specific measurement can be independently reconstructed.

They are **not ReasonedOps performance results**.

### 5. More advanced modelling was not automatically better

The original direction left room for increasingly complex adaptive or sequence models. The rebuild instead requires a model to beat simpler baselines on the same benchmark before complexity is promoted.

That is why LSTM / sequence modelling remains deferred in the current project.

## How the project changed

The rebuild eventually became:

```text
OPERATE
request → structured case → explainable routing

AUDIT
machine decision → human review → effective route → outcome

EVALUATE
raw evidence → comparability check → method-selection gate → guarded analysis
```

The project was initially developed under the name **ANCOVA Ops**. It was renamed **ReasonedOps** because ANCOVA/regression became only one method inside the Evaluate layer rather than the identity of the whole system.

## Historical boundary

This folder exists to make the learning history visible rather than silently rewriting the past.

For the direct comparison between the original concept and the rebuilt project, see [`../docs/before-vs-after.md`](../docs/before-vs-after.md).

For a more detailed audit of the original assumptions, see [`../docs/original-concept-audit.md`](../docs/original-concept-audit.md).
