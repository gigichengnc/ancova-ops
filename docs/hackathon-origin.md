# Hackathon Origin

ReasonedOps originated from my participation in the **HKMU Hackathon 2026**. The early concept focused on a next-generation concierge / virtual-assistance system for property-management service requests and was originally developed under the name **ANCOVA Ops**.

## Original problem framing

The proposal focused on a practical service problem: a resident or tenant submits a maintenance request, complaint or inquiry, and staff need to understand what happened, decide who should handle it, recognise urgency/context, hand the case between teams and follow the outcome.

The original concept therefore combined two ideas:

- reduce repetitive triage and cross-department handover work;
- preserve the human context of a request instead of treating every message as an identical ticket.

## Original proposed flow

The hackathon deck described a flow broadly equivalent to:

```text
new request
  -> request understanding
  -> department classification
  -> contextual/history signals
  -> routing
  -> department queue
  -> outcome feedback
```

It also proposed later learning from recurring complaints, seasonal needs, escalation paths and longitudinal history.

## What changed after the hackathon

The early slides sometimes described emotion filtering as being “achieved by ANCOVA”. That architecture was corrected during the repository rebuild.

**ANCOVA is not used to parse or filter an individual message.** Request understanding is handled by transparent rules/classifiers or other request-intelligence methods. Regression/ANCOVA is used only downstream, after outcomes have accumulated, when the analytical question and data structure support it.

The rebuilt project therefore became:

```text
request
  -> explainable operational recommendation
  -> human review / override
  -> outcome capture
  -> evidence-aware evaluation
```

That broader scope is why the project was renamed **ReasonedOps** in v1.1.0. ANCOVA/regression remains one method inside the Evaluate layer rather than the product identity.

## Human role

A core idea from the hackathon is retained: automation should not silently replace the concierge or service worker. Routine structuring and triage can support staff, while difficult cases, vulnerable users, exceptions and judgement remain visible to humans.

## Historical metrics

The original presentation included projected percentages and business outcomes. They are treated as presentation-era hypotheses or illustrative figures unless a source and project-specific experiment can be reconstructed. They must not be presented as measured performance of ReasonedOps.
