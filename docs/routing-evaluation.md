# Routing Evaluation

## Purpose

ANCOVA Ops needs a stable benchmark before more complex NLP, LLM or machine-learning routing is introduced. A candidate system should not be described as an improvement simply because a few demonstrations look better.

Phase 1 therefore evaluates every routing system on the same labelled fixture set and reports the same metrics.

## Evaluation fixture

The first fixture is:

`data/evaluation/hand_authored_v1.json`

It is explicitly marked as:

- provenance: `hand_authored_fixture`;
- label status: `design_expectation_not_ground_truth`.

The scenarios cover maintenance, security, leasing, accounts and community-management routing, plus deliberately difficult wording and human-review cases.

The baseline is not expected to score perfectly. Known misses are useful because they create measurable room for later systems to improve.

## Metrics

### Department accuracy

The proportion of fixture cases where the predicted primary department equals the hand-authored expected department.

```text
department accuracy = correct department predictions / all fixture cases
```

This is a routing-classification metric. It does not measure whether the department later resolved the case well.

### High-risk human-review recall

The proportion of cases labelled as requiring human review that the routing system also flags for human review.

```text
human-review recall = flagged expected-review cases / all expected-review cases
```

The fixture labels represent operational review/escalation expectations. They are not psychological risk labels and are not validated clinical or safety assessments.

### Routing-explanation coverage

The proportion of cases for which the routing system returns at least one non-blank reason.

```text
explanation coverage = predictions with an explanation / all fixture cases
```

Coverage measures whether an explanation exists, not whether that explanation is correct or sufficient.

## Current transparent baseline

The Phase 1 fixture intentionally exposes weaknesses in the transparent baseline. The deterministic expected report is locked by tests:

- department accuracy: `10 / 11`;
- high-risk human-review recall: `2 / 5`;
- explanation coverage: `11 / 11`.

The current department miss is an intentionally ambiguous leasing request. The current review misses include electrical-safety and security/emergency cases that the first threshold rules do not escalate strongly enough.

These values describe performance on this small fixture only. They are not production performance estimates.

## Run locally

After installing the development package:

```bash
ancova-evaluate
```

Machine-readable output:

```bash
ancova-evaluate --json
```

A different fixture can be supplied explicitly:

```bash
ancova-evaluate --fixture path/to/fixture.json
```

## Compare a candidate system

A candidate predictor can be supplied with `module:function` syntax:

```bash
ancova-evaluate \
  --candidate my_package.my_router:predict \
  --candidate-name experimental-router-v1
```

The callable must accept an `EvaluationCase` and return an `EvaluationPrediction`.

Example interface:

```python
from ancova_ops.evaluation import EvaluationCase, EvaluationPrediction


def predict(case: EvaluationCase) -> EvaluationPrediction:
    ...
    return EvaluationPrediction(
        department="maintenance",
        requires_human_review=True,
        reasons=("safety context detected",),
    )
```

The comparison code refuses to compare reports from different dataset names, versions or sample counts.

A candidate is marked `improved` only when:

1. it is evaluated on the same fixture as the baseline;
2. none of the comparable headline metrics regress; and
3. at least one comparable headline metric improves.

A candidate that improves one metric while worsening another is reported as `mixed`, not as an improvement.

## CI

CI runs the unit tests and also executes the evaluation CLI as a smoke test. The baseline metric test makes unexpected behaviour changes visible in pull requests.

If the intended baseline behaviour changes, update the fixture or expected metrics deliberately and explain why in the pull request. Do not silently move the benchmark to make a new system look better.

## Limitations

The first fixture is intentionally small and cannot support production claims. In particular:

- cases are hand-authored rather than sampled from real operations;
- expected labels are design judgements rather than independent adjudications;
- English wording is overrepresented;
- class frequencies do not represent real property-management workloads;
- the fixture does not estimate calibration, latency, cost or longitudinal outcomes;
- confirmation/override records from staff are not automatically accepted as ground truth;
- real pilot evaluation will require a documented annotation process, sampling strategy and privacy/data-governance controls.

The hand-authored fixture is a software-development benchmark, not a substitute for a prospective pilot evaluation.
