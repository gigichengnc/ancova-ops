# Synthetic Longitudinal Benchmark

## Purpose

Phase 4 asks a narrower question than "can we build an LSTM?":

> Does richer longitudinal modelling add measurable value over a simple recency/frequency baseline when every model is evaluated on the same future period?

The current benchmark is development-only and uses deterministic synthetic histories. It is not evidence about real residents, customers or service operations.

## Data boundary

The generator creates artificial entity IDs and service-case histories with:

- event timestamps;
- issue categories;
- urgency and complexity;
- resolution time;
- escalation outcomes;
- recurrence feedback;
- seasonal variation.

Every row is labelled `synthetic_longitudinal`. No raw request text, direct identifier, real resident history or behavioural embedding is used.

Real longitudinal personalisation remains prohibited under the current governance policy until pilot-specific notice/consent, retention, access-control and jurisdictional requirements are approved.

## Prediction snapshots

A prediction snapshot is built for an entity at a cutoff time. Features are derived only from events at or before that cutoff.

Current features include:

- cases in the previous 30 and 90 days;
- days since the most recent case;
- recent mean resolution time;
- recent escalation rate;
- recent mean urgency and complexity;
- recent department-family shares;
- month sine/cosine seasonality terms.

The 30-day binary target asks whether another case occurs within 30 days after the cutoff.

The time-to-event target records days until the next case, censored at 90 days.

## Leakage control

A chronological split by cutoff time alone is not sufficient. A training snapshot near the validation boundary could use future outcome information that occurs during the validation period.

ReasonedOps therefore uses a **purged chronological split**:

1. validation snapshots are selected from the later cutoff dates;
2. training snapshots must come from earlier cutoffs;
3. the complete training follow-up window must end strictly before the first validation cutoff;
4. snapshots between those windows are purged rather than assigned to either set.

The benchmark reports explicit checks that:

- feature history ends at or before the snapshot cutoff;
- training follow-up ends before validation begins;
- validation cutoffs are chronologically later than training cutoffs;
- provenance remains synthetic-only.

## Models

### 1. Recency/frequency logistic baseline

The reference model uses only:

- cases in the previous 30 days;
- cases in the previous 90 days;
- days since the last case.

It intentionally provides a low-complexity baseline that every richer model must beat on the same future window.

### 2. Discrete-time logistic hazard model

The survival/time-to-event approach expands each training snapshot into five-day person-period intervals and fits a logistic hazard model.

Cumulative recurrence probability is obtained from the interval hazards:

```text
P(event by horizon) = 1 - product(1 - interval_hazard)
```

The benchmark reports 30-day recurrence metrics and a Harrell-style concordance index for recurrence-time ranking.

### 3. Random-forest recurrence classifier

The tree model uses the complete engineered longitudinal feature set and predicts the same 30-day recurrence target.

It is included as a flexible non-linear comparator, not as an automatic preferred model.

## Metrics

For the 30-day recurrence target, all three models are evaluated on the same validation cohort with:

- ROC-AUC;
- Brier score;
- calibration bias (`mean predicted probability - observed recurrence rate`).

The survival model also reports a concordance index over the censored time-to-next-case outcome.

No metric in this synthetic benchmark is a production performance claim.

## Complexity rule

A richer model clears the current incremental-value rule only when it improves ROC-AUC by at least `0.02` over the recency/frequency baseline **without worsening the Brier score** on the same future validation window.

This rule is deliberately conservative and development-oriented. Passing it justifies more study of that model family; it does not authorise deployment.

## Why sequence models remain deferred

Phase 4 does not introduce an LSTM, Transformer or other sequence architecture.

A sequence model should only be added in a separate comparison when:

1. the current benchmark and leakage controls remain unchanged or are strengthened;
2. the sequence model receives no information unavailable to the simpler comparators at prediction time;
3. it demonstrates reproducible incremental value over the strongest simple model;
4. the added operational, interpretability and governance cost is justified.

If recency/frequency, survival-style or tree models already explain the useful signal, adding sequence complexity would not be evidence-driven.

## Command

Run the benchmark:

```bash
reasoned-longitudinal
```

Machine-readable output:

```bash
reasoned-longitudinal --json
```

A smaller deterministic smoke run can be used in CI:

```bash
reasoned-longitudinal --entities 100 --days 600 --seed 31 --json
```

## Limitations

- The event process is synthetic and intentionally contains recurrence and seasonal structure.
- Repeated snapshots from the same synthetic entities evaluate future-period generalisation, not unseen-entity generalisation.
- The 30-day target is a project development choice, not a validated service-risk threshold.
- The discrete-time hazard implementation is a benchmark model, not a production survival system.
- Real longitudinal data would require a new privacy, consent, retention and access-control review before use.
