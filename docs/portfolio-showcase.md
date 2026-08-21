# Portfolio Showcase — v1.0

The v1.0 `reasoned-showcase` command is the reviewer-facing entry point for the completed ReasonedOps research prototype:

> **Operate → Audit → Evaluate**

The showcase does not introduce a new model or a new evidence class. It orchestrates the existing request-intelligence, routing/audit, outcome-evaluation, applicability, adaptive-policy and longitudinal research components while keeping their evidence and deployment boundaries visible.

## Run the showcase

```bash
reasoned-showcase
```

Default Markdown output:

```text
.reasoned_ops/showcase/showcase.md
```

Generate Markdown plus JSON:

```bash
reasoned-showcase \
  --output .reasoned_ops/showcase/showcase.md \
  --json-output .reasoned_ops/showcase/showcase.json
```

Print the structured payload:

```bash
reasoned-showcase --json
```

## What the v1 report contains

### Operate

- deterministic service-request example;
- transparent request-intelligence features;
- explainable baseline routing recommendation;
- hand-authored routing benchmark with provenance and label status.

### Audit

- the architecture boundary separating original request, machine/rule decision, later human review, effective route and outcome;
- explicit synthetic-only governance status;
- reminder that human review does not erase the original machine history and is not automatic ground truth.

### Evaluate

- department/case-type identifiability status;
- final `use` / `caution` / `reject` / `recommend_alternative` applicability disposition;
- recommended method family and reasons;
- synthetic case-mix-adjusted regression/ANCOVA output when supportable;
- warnings and non-causal interpretation boundary;
- offline adaptive-routing research with `deployment_eligible = false`;
- synthetic longitudinal comparison and sequence-model deferral.

### Completion and deployment boundary

The report explicitly states:

```text
Research/portfolio prototype: COMPLETED at v1.0
Private-data pilot: NOT READY / NOT APPROVED
Production deployment: NOT READY / NOT APPROVED
```

## Reviewer interpretation

The showcase is designed to answer:

- What does ReasonedOps do end to end?
- How do Operate, Audit and Evaluate fit together?
- Can the evaluation layer refuse a comparison when the data cannot support it?
- Does the method-selection gate redirect incompatible questions instead of forcing ANCOVA?
- Which evidence is synthetic/hand-authored and which claims therefore remain unjustified?

The generated report is a software/research portfolio artifact. It must not be used to claim real improvements in resolution time, routing accuracy, satisfaction, staff performance or real-world longitudinal prediction.

## Fast CI-sized run

```bash
reasoned-showcase \
  --outcome-rows 120 \
  --logged-rows 400 \
  --longitudinal-entities 80 \
  --longitudinal-days 540 \
  --output /tmp/reasoned-showcase.md \
  --json-output /tmp/reasoned-showcase.json
```

This smaller run preserves the same evidence and governance boundaries.

## Portfolio description

A concise v1 description is:

> ReasonedOps is a completed evidence-aware service-operations research prototype organised around Operate, Audit and Evaluate. It combines explainable routing, auditable human review, outcome capture, comparison-support checks and an evaluation applicability gate that can use, caution, reject or redirect an analytical question before management interprets the result.

A shorter principle is:

> It is not designed to make management decisions. It is designed to make unsupported management conclusions harder to reach.

## Post-v1 boundary

New model families, private-data pilot work, production deployment, DOI/PyPI publication or competition-specific extensions are post-v1 opportunities rather than unfinished showcase work.

## License

ReasonedOps repository material distributed under the project license is licensed under Apache-2.0. See the root [`LICENSE`](../LICENSE). Third-party dependencies and separately identified third-party material retain their own licences and notices.
