# ReasonedOps

**Evidence-aware service operations: Operate → Audit → Evaluate.**

ReasonedOps is a reusable Python package that originated from the author's participation in HKMU Hackathon 2026 and evolved into an evidence-aware service-operations research/software prototype.

It separates three responsibilities:

```text
OPERATE
service request → rule-based operational features → deterministic explainable routing baseline

AUDIT
original request → machine/rule decision → human review → effective route → outcome

EVALUATE
raw outcomes → comparison-support check → method applicability → guarded evidence
```

The current Operate baseline is intentionally transparent and deterministic. It does **not** claim a trained NLP model or production routing accuracy.

The Evaluate layer can withhold a department comparison when the observed case mix cannot support it, and it can redirect questions that should not be forced through ordinary continuous-outcome ANCOVA/regression.

The synthetic validity benchmark also includes an explicit **unmeasured-confounding blind spot**: a latent case-burden variable is deliberately removed before evaluation, allowing observed-data checks to look supportable while the adjusted department contrast becomes badly wrong. That scenario documents a limitation; it does not claim that ReasonedOps can detect an unrecorded confounder.

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

The routing baseline is a reference implementation for development and evaluation. It is not a claim of external routing accuracy.

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

## Evidence boundary

Current quantitative evidence in the public repository is synthetic or hand-authored development evidence. The package does not establish real-world service improvement, causal effects, absence of unmeasured confounding, private-data pilot approval, or production readiness.

## Project links

- Source and full project-evolution case study: https://github.com/gigichengnc/reasoned-ops
- Early-vs-current comparison: https://github.com/gigichengnc/reasoned-ops/blob/main/docs/before-vs-after.md
- Method decisions: https://github.com/gigichengnc/reasoned-ops/blob/main/docs/model-decisions.md
- Release readiness: https://github.com/gigichengnc/reasoned-ops/blob/main/docs/release-readiness.md
- License: Apache-2.0
