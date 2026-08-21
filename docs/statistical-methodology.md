# Statistical Methodology

## Role of the evaluation layer

ReasonedOps is organised around **Operate → Audit → Evaluate**. The evaluation layer exists to reduce the risk that operational dashboards or raw averages are interpreted as evidence they cannot support.

ANCOVA/regression is one possible evaluation method. It is not the real-time request classifier, it is not an automatic staff-ranking engine, and it is not forced onto every analytical question.

The v1 rule is:

> **Check whether the comparison is supportable first. Check whether the method family matches the question second. Report uncertainty and limitations with the result.**

## Continuous resolution-time example

For the implemented continuous-outcome example, the development question is:

> Among sufficiently comparable completed cases, after adjusting for measured pre-routing case mix, how do model-based mean resolution times differ across departments?

The default model is:

```text
resolution_hours
~ C(department)
+ C(issue_category)
+ urgency
+ frustration
+ complexity
+ previous_related_cases
```

`department` is the operational path/grouping factor. `issue_category` and the numeric covariates represent measured case mix known before or independently of the outcome being analysed.

This is an observational, associational model unless a separate study design and identification argument supports causal interpretation.

## Comparison support and identifiability

A raw department comparison can be badly misleading when departments handle different work. If maintenance receives complex repairs while another team receives routine requests, a slower raw mean does not establish worse process performance.

Before adjusted department estimates are published, `routing_overlap_diagnostics()` evaluates:

- department × issue-category counts;
- shared issue categories;
- structural connectivity between departments through shared categories;
- practical connectivity at a configurable minimum cell size;
- design-matrix rank and column count;
- department-specific support summaries.

It returns one of:

### `supported`

The department/case-type design is structurally estimable and has practical overlap at the configured threshold. Model-based comparison may proceed, subject to all remaining assumptions and interpretation limits.

### `weak_overlap`

The model is structurally estimable, but practical overlap is thin. Adjusted estimates can be shown only with caution and conclusions should be restricted to supported case mix or deferred until more comparable cases exist.

### `not_identifiable`

Department and issue category cannot be separated from the observed routing design. The software withholds:

```text
adjusted department estimates
ANOVA department results
management adjusted ranking
```

Raw descriptive summaries can remain visible, but a different model cannot manufacture a department contrast that the observed design does not identify.

## Adjusted department estimates

When the comparison is estimable, adjusted department means are standardised over the **observed complete-case case-mix distribution**.

Conceptually, ReasonedOps predicts the same observed case mix under each department label using the fitted model and averages those predictions over the observed case mix. This avoids choosing one arbitrary categorical issue reference.

The resulting estimates remain model-based associations. They must not be described as the causal effect of reassigning a case to another department unless a separate causal design justifies that interpretation.

## Known-truth validity benchmark

`reasoned-validity` runs deterministic synthetic scenarios where the data-generating truth is known.

### Known-effect recovery

Overlapping synthetic service outcomes contain explicit artificial department effects. Adjusted contrasts must recover the known contrasts within a pre-specified tolerance.

### Measured confounding

A two-department scenario deliberately routes complex and routine cases to departments with very different probabilities. The benchmark compares a naive model omitting issue category with the case-mix-adjusted model. Adjustment must materially reduce the deliberately induced bias.

### No-overlap refusal

A deterministic routing scenario sends each issue category to only one department. The required result is:

```text
identifiability = not_identifiable
adjusted department estimates = withheld
ANOVA department results = withheld
management ranking = blocked
```

### Slope-interaction detection

A synthetic scenario gives one department a different urgency slope. The department × urgency interaction should be detected before a common-slope ANCOVA interpretation is trusted.

Passing these scenarios validates software behaviour on known synthetic cases. It does not validate real service outcomes.

## v1 evaluation applicability gate

`reasoned-applicability` makes **method follows the question** executable.

It represents:

- outcome type: `continuous`, `binary`, `time_to_event`;
- question type: `department_outcome`, `descriptive`, `routing_policy`;
- overlap status: `supported`, `weak_overlap`, `not_identifiable`, `not_assessed`;
- censoring;
- repeated/clustered observations;
- causal intent;
- department-specific covariate slope flags.

It returns exactly one high-level disposition:

- `use`;
- `caution`;
- `reject`;
- `recommend_alternative`.

Examples:

```text
continuous + supported overlap + no declared complication
→ use regression_ancova_style

weak overlap
→ caution

material department-specific slope
→ caution interaction_aware_regression

no overlap
→ reject no_adjusted_department_comparison

binary outcome
→ recommend_alternative logistic_type_model

censored/time-to-event outcome
→ recommend_alternative survival_time_to_event_model

repeated/clustered observations
→ recommend_alternative clustered_or_hierarchical_model

routing-policy counterfactual
→ recommend_alternative offline_policy_evaluation

causal-intent question
→ recommend_alternative causal_design_and_identification
```

See [`evaluation-applicability.md`](evaluation-applicability.md).

## Why recommendations are not all implementations

v1.0 deliberately does not implement every logistic, survival, hierarchical or causal method merely to increase feature count.

The final research-project requirement is that ReasonedOps does not silently use the wrong method. Alternative model implementation is post-v1 work that should be justified by a concrete research question or real use case.

A `recommend_alternative` result is therefore a valid output, not an incomplete code path.

## Other diagnostics

When the continuous-outcome comparison is estimable, the workflow also reports:

- required-field missingness and complete-case counts;
- department group sizes;
- Jarque–Bera residual screening;
- Breusch–Pagan heteroskedasticity screening;
- variance inflation factors;
- Cook's distance and leverage summaries;
- department-by-covariate interaction screens;
- confidence intervals for case-mix-standardised estimates.

These are screening tools, not proof that every modelling assumption holds.

## Complete-case policy

The current implementation uses complete cases for required fields. This is a transparent development baseline rather than a universal recommendation.

If required-field missingness exists, the report exposes excluded rows and warns that the missing-data mechanism must be investigated. A real pilot would require a pre-specified missing-data strategy appropriate to its data-generating process.

## Causal boundary

Ordinary observational case-mix adjustment does not answer a causal question automatically.

A causal question needs a defined intervention, target estimand, assignment mechanism and identification assumptions before method selection. A statistically significant adjusted department term is never sufficient on its own to claim that changing a route will improve the outcome.

## Data provenance boundary

Current repository analytics operate on approved development provenance only. Quantitative evidence is synthetic or hand-authored unless explicitly stated otherwise.

Real private pilot or production data remains outside the repository's current approval boundary. Synthetic validity/applicability success must never be presented as observed service improvement.

## Reproducible commands

```bash
# Continuous-outcome workflow
reasoned-analyze
reasoned-analyze --json

# Management report with applicability gate
reasoned-management-report

# Known-truth validity scenarios
reasoned-validity
reasoned-validity --json

# Standalone method applicability
reasoned-applicability \
  --outcome-type continuous \
  --comparison department_outcome \
  --overlap-status supported \
  --json
```

A development CSV can be supplied to `reasoned-analyze` when it includes an approved `data_provenance` value and all required model fields.

## Interpretation boundary

The evaluation layer is intended to make unsupported conclusions harder to reach. Its correct output can be an adjusted comparison, a warning, a recommendation to use another method family, or a refusal to make the comparison at all.
