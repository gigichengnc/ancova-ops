# Portfolio Showcase — ReasonedOps v1.2.0

`reasoned-showcase` is the fastest way to prove that the repository is executable.

Run:

```bash
reasoned-showcase
```

It writes:

```text
.reasoned_ops/showcase/showcase.md
```

The generated file walks through one concrete service request and then shows what the current development workflows do with it.

## What appears in the report

### Request and route

The showcase uses a repeated air-conditioner leak request and displays the extracted operational signals, recommended department, priority and human-review flag.

### Audit boundary

The report explains that the operational model keeps these items separate:

```text
original request
machine/rule recommendation
human confirmation or override
effective route
observed outcome
implementation version
```

### Evaluation boundary

The report then shows whether a department comparison is supportable and which evaluation method family is appropriate. The applicability result can be:

```text
use
caution
reject
recommend_alternative
```

A `reject` result is intentional: it means the current design should not be turned into an adjusted department ranking.

### Development-only research outputs

The showcase also includes the existing routing fixture, synthetic regression/ANCOVA outcome example, offline routing-policy research and synthetic longitudinal benchmark.

Those results are there to demonstrate software behaviour and research workflow integration. They are not production performance estimates.

## Markdown plus JSON

```bash
reasoned-showcase \
  --output .reasoned_ops/showcase/showcase.md \
  --json-output .reasoned_ops/showcase/showcase.json
```

Print the structured payload directly:

```bash
reasoned-showcase --json
```

## Reviewer interpretation

After running the command, a reviewer should be able to answer:

- Can the repository actually execute? **Yes.**
- Can it route a request and explain the route? **Yes, as a local development prototype.**
- Can a human override the route without deleting machine history? **Yes.**
- Can an outcome be stored separately? **Yes.**
- Can the evaluation layer refuse a misleading comparison? **Yes.**
- Does this prove real-world service improvement? **No.**
- Is it approved for real private data or production? **No.**
