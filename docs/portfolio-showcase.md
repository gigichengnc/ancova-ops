# Portfolio Showcase

ANCOVA Ops v0.5.1 adds a reviewer-facing showcase layer for demonstrating the existing Phase 1–4 development workflows in one place.

The showcase does **not** introduce a new model. It orchestrates existing request-intelligence, routing-evaluation, ANCOVA/outcome-analysis, adaptive-routing and longitudinal-benchmark components and keeps their evidence boundaries visible.

## Run the showcase

```bash
ancova-showcase
```

Default Markdown output:

```text
.ancova_ops/showcase/showcase.md
```

Generate Markdown plus structured JSON:

```bash
ancova-showcase \
  --output .ancova_ops/showcase/showcase.md \
  --json-output .ancova_ops/showcase/showcase.json
```

Print the structured payload as well:

```bash
ancova-showcase --json
```

## What the report contains

1. A deterministic service-request example passed through the transparent request-intelligence and baseline-routing pipeline.
2. The hand-authored routing-fixture benchmark with provenance and label status.
3. The synthetic ANCOVA/outcome-analysis formula, adjusted estimates, confidence intervals and warnings.
4. The synthetic logged-policy adaptive-routing comparison, including the explicit `deployment_eligible = false` boundary.
5. The synthetic longitudinal comparison across recency/frequency logistic, discrete-time hazard and random-forest models.
6. Governance and readiness status showing that repository checkpoint readiness does not equal private-data pilot or production readiness.

## Reviewer interpretation

The showcase is designed to answer three questions quickly:

- What does ANCOVA Ops actually do end to end?
- Which parts are implemented and runnable today?
- What evidence is synthetic or hand-authored, and what claims are therefore not justified?

The generated report should be treated as a software/research portfolio artifact. It must not be used to claim that ANCOVA Ops improves real service resolution time, routing accuracy, resident/customer satisfaction or real-world longitudinal prediction.

## Fast CI-sized run

For a smaller deterministic run:

```bash
ancova-showcase \
  --outcome-rows 120 \
  --logged-rows 400 \
  --longitudinal-entities 80 \
  --longitudinal-days 540 \
  --output /tmp/ancova-showcase.md \
  --json-output /tmp/ancova-showcase.json
```

This smaller run preserves the same development/evidence boundaries; it is intended only to reduce execution time during testing.

## Presentation boundary

A strong portfolio description is:

> ANCOVA Ops is a reproducible human-centred service-intelligence research prototype connecting explainable routing, auditable human review, downstream ANCOVA/regression, offline adaptive-policy evaluation and leakage-aware longitudinal benchmarking.

Do not replace that with production-impact claims unless future real-world evidence supports them.
