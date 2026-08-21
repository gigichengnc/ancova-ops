# Adaptive Routing — Phase 3

## Purpose

Phase 3 asks a narrower question than “can we train a model?”:

> Can historical outcome data provide a credible offline signal that a routing policy candidate may improve service outcomes, without pretending that logged history reveals every counterfactual outcome?

The Phase 3 framework is deliberately offline-first. It does not automatically replace the router used by the API.

## Current development boundary

Only `synthetic_logged_policy` data is accepted by this workflow. The repository remains under the synthetic-only development policy. The generated logging data contains no resident identity, raw private message text or production records.

The synthetic generator uses five departments:

- maintenance;
- security;
- leasing;
- accounts;
- community management.

The logging policy chooses the current baseline department with probability `0.60` and each alternative with probability `0.10`. Those probabilities are stored per row as explicit action propensities.

For demonstration only, the synthetic data-generating process makes `community_management` faster on average for `noise_complaint`, while the current baseline maps that category to `security`. This makes one adaptive departure learnable. It is a simulation design choice, not evidence that a real property-management operation should route noise complaints that way.

## Time-aware train / validation split

Rows are sorted by `event_time`. The candidate is trained only on events strictly before the cutoff. Validation events occur at or after the cutoff, and the code verifies:

```text
max(training.event_time) < min(validation.event_time)
```

This prevents the candidate from using future validation outcomes during training.

A time split is not enough to prove future generalisation. Seasonality, operational changes, staffing changes, policy drift and rare-event shifts can still invalidate an offline result.

## Transparent outcome-aware candidate

The first candidate is intentionally simple. Within each issue category it calculates the observed training-window mean resolution time for each department that has at least the configured minimum number of logged cases. It selects the supported department with the lowest training mean.

If there is insufficient support, it falls back to the existing transparent category-to-department mapping.

This candidate is useful because its behaviour can be inspected directly. It is not presented as an optimal policy and it does not justify causal interpretation of the training means.

## Why matched historical outcomes are not enough

Suppose a candidate recommends `maintenance` for a case that historically went to `security`. The history contains the observed security outcome, but it does not contain the resolution time that would have occurred under maintenance for the same case.

Therefore this quantity:

```text
mean outcome among rows where historical action == candidate action
```

is descriptive only. It can be badly biased because matching rows may differ systematically from non-matching rows.

The report exposes this matched mean but labels it as non-counterfactual.

## Inverse-propensity offline estimate

Because the synthetic logging policy records known probabilities for every available department, Phase 3 can demonstrate inverse-propensity scoring (IPS).

For a deterministic target policy, a validation row contributes only when the historical logged action equals the target action. The contribution is weighted by the inverse of the logging probability for that action.

Conceptually:

```text
IPS(policy) = mean[ I(logged_action = policy(x)) * outcome / propensity(policy(x) | x) ]
```

The framework also reports self-normalised IPS as a diagnostic and an effective sample size based on the non-zero weights.

### IPS does not remove all uncertainty

An IPS estimate still depends on important assumptions:

- the logged action propensities are correct;
- every target action has positive probability under the logging policy (overlap / support);
- the logging mechanism is represented adequately by the recorded propensities;
- the observed outcome is measured consistently;
- there is enough effective sample size for the weighted estimate to be useful;
- the environment has not changed in a way that breaks transport from the historical window to the validation window.

The current synthetic experiment is designed so the propensities are known exactly. Real operational routing generally will not satisfy that condition automatically.

## Support gate

Every validation row is checked for positive logging probability for the action selected by the evaluated policy.

If a target action is unsupported, the IPS estimate is marked non-estimable and the candidate cannot pass the configured offline gate.

The candidate also needs the configured minimum effective sample size. Passing this gate only means that the synthetic offline comparison produced a supported lower estimated resolution time than the baseline under the current rules.

It does **not** mean production improvement has been proven.

## Offline comparison language

The report uses signals such as:

- `candidate_lower_estimated_resolution_time`;
- `candidate_higher_estimated_resolution_time`;
- `no_estimated_difference`;
- `not_estimable`.

It deliberately does not convert a synthetic IPS difference into a claim such as “the new router improves resolution time by X%.”

Every report sets `deployment_eligible = false` because the current project has not approved a real pilot or production deployment.

## Human approval and policy lifecycle

`PolicyRegistry` stores a local append-only lifecycle record under `.reasoned_ops/policy-registry.json` by default. That directory is ignored by Git.

A candidate lifecycle is:

```text
candidate
   ↓ offline gate
approved by named human reviewer
   ↓ explicit activation action
active
   ↓ rollback if required
previous approved version restored
```

An offline gate alone cannot activate a candidate. A named reviewer and rationale are required first.

Approval also does not waive the offline gate: a reviewer cannot activate a candidate whose offline estimate was unsupported or failed the configured comparison rule through the normal activation command.

Rollback changes the active registry pointer and appends an event. It does not delete the candidate, its approval or prior activation history.

The existing `baseline-route-v1` is treated as the grandfathered initial active policy so a rollback target always exists.

## Important deployment boundary

The registry is a policy-lifecycle control record. Phase 3 does **not** automatically make `/v1/route` read a newly activated candidate. The operational API continues to use the existing transparent baseline until a future integration explicitly connects a reviewed policy resolver to the request path.

That separation is intentional: evaluation, approval and operational deployment should not collapse into a single command.

## CLI

Run the deterministic synthetic offline study:

```bash
reasoned-policy evaluate
```

Register the evaluated candidate in a local lifecycle registry:

```bash
reasoned-policy evaluate --register
```

Inspect the registry:

```bash
reasoned-policy status
```

Record explicit human approval:

```bash
reasoned-policy approve \
  --version outcome-aware-category-mean-v1 \
  --reviewer reviewer-001 \
  --rationale "Reviewed synthetic offline evidence for controlled staging."
```

Activate the approved candidate in the registry:

```bash
reasoned-policy activate \
  --version outcome-aware-category-mean-v1 \
  --actor ops-lead
```

Rollback:

```bash
reasoned-policy rollback \
  --version baseline-route-v1 \
  --actor ops-lead \
  --rationale "Rollback drill."
```

Again, registry activation is not automatic production deployment.

## What should come next

Before adaptive routing can be tested on real operational records, the still-open pilot governance items must be resolved: jurisdiction/privacy review, concrete retention schedule, notice/consent where required, access control and deletion procedures.

A later Phase 3 extension can compare additional candidates—regularised models, trees or contextual policies—using the same time window, support checks and lifecycle controls. Complexity should only be added if it improves a defined evaluation target without weakening interpretability, auditability or safety.