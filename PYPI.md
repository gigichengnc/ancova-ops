# ReasonedOps

**Evidence-aware service operations: Operate → Audit → Evaluate.**

ReasonedOps is a reusable Python package extracted from a retrospective rebuild of an HKMU Hackathon 2026 concierge concept. It provides transparent service-request routing, auditable machine/human decision history, outcome capture, and guarded evaluation workflows that can refuse unsupported management comparisons.

## Install

```bash
pip install reasoned-ops
```

Python 3.11 and 3.12 are supported by the repository CI matrix.

## Minimal Python example

```python
from reasoned_ops import ServiceCase, baseline_route

case = ServiceCase(
    case_id="demo-001",
    message="The air conditioner is leaking again.",
    urgency=8,
    complexity=7,
    previous_related_cases=2,
)

decision = baseline_route(case)

print(decision.department)
print(decision.priority)
print(decision.requires_human_review)
print(decision.reasons)
```

The routing baseline is intentionally transparent and deterministic. It is a reference implementation for development and evaluation, not a claim of production routing accuracy.

## Command-line tools

Installing the package also installs:

```text
reasoned-evaluate
reasoned-validity
reasoned-applicability
reasoned-analyze
reasoned-management-report
reasoned-policy
reasoned-longitudinal
reasoned-showcase
reasoned-governance-check
```

For a one-command development demonstration:

```bash
reasoned-showcase
```

## What the project is for

ReasonedOps separates three responsibilities:

```text
OPERATE
service request → structured signals → explainable routing recommendation

AUDIT
original request → machine decision → human review → effective route → outcome

EVALUATE
raw outcomes → comparison-support check → method applicability → guarded evidence
```

A central design rule is that the evaluation layer is allowed to return **REJECT** when the observed data cannot support a requested comparison. Regression/ANCOVA is one possible method inside Evaluate rather than the product identity.

## Evidence boundary

Current quantitative evidence in the public repository is synthetic or hand-authored development evidence. The package does not establish real-world service improvement, causal effects, private-data pilot approval, or production readiness.

## Project links

- Source and full portfolio case study: https://github.com/gigichengnc/reasoned-ops
- Before/after rebuild: https://github.com/gigichengnc/reasoned-ops/blob/main/docs/before-vs-after.md
- Method decisions: https://github.com/gigichengnc/reasoned-ops/blob/main/docs/model-decisions.md
- Release readiness: https://github.com/gigichengnc/reasoned-ops/blob/main/docs/release-readiness.md
- License: Apache-2.0
