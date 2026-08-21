# Model and method decisions

ReasonedOps treats modelling decisions as reviewable project decisions rather than as a sequence of automatic upgrades.

This document records the main choices that shaped the rebuild.

## Decision 1 — Keep routing transparent before making it sophisticated

### Question
Should the first routing layer immediately use a more complex black-box model?

### Decision
No. The reference routing workflow remains transparent and deterministic.

### Why
The project needed an auditable baseline before it needed model complexity. A reviewer should be able to see:

- which operational features were extracted;
- which route was recommended;
- why the recommendation was made;
- which version made it;
- whether human review was requested.

A complex model can only be judged meaningfully once a stable benchmark and decision record exist.

## Decision 2 — Move ANCOVA downstream

### Question
Should ANCOVA help interpret/filter an individual request?

### Decision
No.

### Why
ANCOVA/regression operates on accumulated observations and outcomes. It is not a text-understanding algorithm.

ReasonedOps therefore uses:

```text
request intelligence → routing → human review → outcome capture → evaluation
```

Only the final evaluation stage may use regression / ANCOVA when the declared question and data structure support it.

## Decision 3 — Add a comparison-support gate before adjusted rankings

### Question
If departments have different average resolution times, should the system always fit an adjusted model and rank them?

### Decision
No.

### Why
If department and case type are nearly or perfectly tied together, the observed data may not contain enough overlap to separate a department contrast from a work-type contrast.

ReasonedOps therefore checks department × case-type overlap and design identifiability first.

Possible outcomes include:

```text
supported
weak_overlap
not_identifiable
```

When the design is `not_identifiable`, adjusted estimates and ranking language are withheld.

## Decision 4 — Let ANCOVA be the wrong method

### Question
Should every evaluation question be forced through the method that inspired the original project name?

### Decision
No.

### Why
Different outcomes and questions imply different model families.

The applicability gate can return:

```text
use
caution
reject
recommend_alternative
```

Examples:

- continuous uncensored outcome + supported overlap → regression / ANCOVA-style workflow may be appropriate;
- binary outcome → recommend logistic-type analysis;
- censored time-to-event outcome → recommend survival analysis;
- repeated/clustered observations → recommend cluster-aware / hierarchical analysis;
- routing-policy counterfactual → recommend offline policy evaluation;
- unsupported department comparison → reject the ranking question.

This decision is also why the project was renamed from **ANCOVA Ops** to **ReasonedOps**.

## Decision 5 — Keep adjusted effects non-causal by default

### Question
Can an adjusted regression coefficient be described as proof that a department or policy caused a better outcome?

### Decision
No.

### Why
Measured adjustment does not remove all confounding and does not create a causal design.

ReasonedOps therefore treats regression / ANCOVA results as adjusted associations unless a separate identification argument exists.

## Decision 6 — Validate statistical behaviour with known synthetic truth

### Question
How can the implementation be tested before representative real service data exist?

### Decision
Use deterministic synthetic scenarios where the true data-generating behaviour is known.

### Current validity scenarios

The benchmark checks that the software can:

- approximately recover known additive effects;
- reduce deliberately induced measured case-mix bias;
- refuse a structurally unsupported no-overlap comparison;
- flag a deliberately introduced slope interaction.

These tests validate software/statistical behaviour. They do **not** validate real operational effectiveness.

## Decision 7 — Keep adaptive routing offline

### Question
If a candidate routing policy looks better on historical synthetic logs, should it replace the live router automatically?

### Decision
No.

### Why
Off-policy evaluation depends on support, propensities, effective sample size, and counterfactual assumptions.

The adaptive workflow therefore remains separate from `/v1/route`. It supports offline evaluation, lifecycle registration, named approval, activation history and rollback records, but `deployment_eligible` remains false by design in the research prototype.

## Decision 8 — Use chronological validation for longitudinal questions

### Question
Can recurrence models be evaluated with ordinary random splits?

### Decision
No.

### Why
Longitudinal data can leak future information into training very easily.

The benchmark therefore uses feature-time checks, follow-up windows, and purged chronological validation.

## Decision 9 — Defer LSTM / sequence modelling

### Question
Should the project add an LSTM because longitudinal histories exist?

### Decision
Not yet.

### Why
A sequence model is justified only if it demonstrates reproducible incremental value over the strongest simpler baseline on the same benchmark.

The current project deliberately records:

```text
sequence_model_status = deferred_not_justified_by_current_benchmark
```

This is a model-development decision, not missing work.

## Decision 10 — Stop the research project at a finite boundary

### Question
Should the repository keep adding methods indefinitely?

### Decision
No.

### Why
The completed research prototype already demonstrates the intended reasoning pattern:

```text
Operate
  ↓
Audit
  ↓
Evaluate
  ↓
use / caution / reject / recommend another method
```

Production security, real-data pilot validation, new model families, and deployment integrations are post-project opportunities that require a concrete use case and new evidence.

## Decision principle

Across the rebuild, one rule is used repeatedly:

> **Complexity, automation and stronger claims must earn their place through evidence.**

That principle is more important to ReasonedOps than any single statistical model.
