# Statistical Methodology

## Role of the evaluation layer

ANCOVA Ops is organised around **Operate → Audit → Evaluate**. The evaluation layer exists to reduce the risk that operational dashboards or raw averages are interpreted as evidence they cannot support.

ANCOVA/regression is one possible evaluation method. It is not the real-time request classifier, it is not an automatic staff-ranking engine, and it is not forced onto every analytical question.

The guiding rule is:

> **Check whether the comparison is supportable first. Choose the method second. Report uncertainty and limitations with the result.**

## Current development question

For the continuous resolution-time example, the current development question is:

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

`department` is the operational path/grouping factor. `issue_category` and the numeric covariates represent measured case mix that is known before or independently of the outcome being analysed.

This remains an observational, associational model unless a separate study design and identification argument supports causal interpretation.

## Why issue category matters

A raw department comparison can be badly misleading when departments handle different work. If maintenance receives complex repairs while another team receives routine requests, a slower raw mean does not establish worse process performance.

The previous development generator made issue category nearly equivalent to department, which was useful for simple code demonstrations but too easy for a serious evaluation example. The v0.6.0 synthetic outcome generator instead creates overlapping issue categories across departments with explicit artificial case-mix and department effects.

The synthetic effects exist only so the software can be tested against known truth. They must never be reported as real operational performance.

## Comparison-support and identifiability gate

Before ANCOVA Ops publishes adjusted department estimates, it checks whether department and issue-category effects can be separated from the observed design.

`routing_overlap_diagnostics()` reports:

- department × issue-category counts;
- number of shared issue categories;
- structural connectivity between departments through shared categories;
- practical connectivity at a configurable minimum cell size;
- design-matrix rank and column count;
- department-specific support summaries;
- one of three statuses: `supported`, `weak_overlap`, or `not_identifiable`.

### Supported

The design matrix is estimable and departments are connected through sufficiently populated shared issue categories at the configured threshold.

This permits model-based comparison. It does **not** prove causal exchangeability, absence of unmeasured confounding, correct model specification, or transportability beyond the observed case mix.

### Weak overlap

The model is structurally estimable, but practical overlap is thin. Adjusted estimates may be shown with a prominent warning, and conclusions should be restricted to the supported case mix or deferred until more comparable cases are collected.

### Not identifiable

When department and issue category are inseparable from the observed routing design, the software withholds:

- adjusted department estimates;
- department ANOVA results;
- management-facing adjusted ranking language.

Raw descriptive summaries may still be shown, but the report states that a department ranking would be misleading.

This refusal behaviour is intentional. Producing a number is not preferable to saying that the data cannot answer the question.

## Adjusted department estimates

When the comparison is estimable, adjusted department means are standardised over the **observed complete-case case-mix distribution**.

Conceptually, ANCOVA Ops asks what the fitted model predicts if the same observed case mix were evaluated under each department label, then averages those predictions over that observed case mix. This avoids choosing an arbitrary categorical issue reference and is easier to interpret than fixing all covariates to one synthetic case.

The resulting estimates remain model-based associations. They must not be described as the causal effect of reassigning a case to another department unless a separate causal design justifies that interpretation.

## v0.6.0 validity benchmark

`ancova-validity` runs deterministic synthetic scenarios in which the data-generating truth is known.

### 1. Known-effect recovery

Overlapping synthetic service outcomes contain explicit artificial department effects. The adjusted contrasts must recover the known contrasts within a pre-specified tolerance.

This tests whether the implemented standardisation and regression machinery can recover known effects in a setting designed to be identifiable.

### 2. Measured confounding

A two-department scenario deliberately routes complex and routine cases to departments with very different probabilities. The true department contrast is known.

The benchmark compares:

- a naive model that omits issue category; and
- the case-mix-adjusted model that includes issue category.

The adjusted model must materially reduce the induced bias relative to the naive model.

### 3. No-overlap refusal

A deterministic routing scenario sends each issue category to only one department. Department and issue-category effects are therefore not separately identifiable.

The required behaviour is:

```text
identifiability = not_identifiable
adjusted department estimates = withheld
ANOVA department results = withheld
management ranking = blocked
```

### 4. Slope-interaction detection

A synthetic scenario deliberately gives one department a different urgency slope. The department × urgency interaction should be detected, warning that a common-slope ANCOVA interpretation is inappropriate.

Passing all four scenarios validates software behaviour on known synthetic cases. It does not validate the method on real service data.

## Other diagnostics

When the main comparison is estimable, the workflow also reports:

- required-field missingness and complete-case counts;
- department group sizes;
- Jarque–Bera residual screening;
- Breusch–Pagan heteroskedasticity screening;
- variance inflation factors;
- Cook's distance and leverage summaries;
- department-by-covariate interaction screens;
- confidence intervals for case-mix-standardised department estimates.

These are screening tools, not mechanical proof that every modelling assumption holds.

## Complete-case policy

The current implementation uses complete cases for the required fields. This is a transparent development baseline rather than a claim that complete-case analysis is universally appropriate.

If required-field missingness exists, the report exposes the number of excluded rows and warns that the missing-data mechanism must be investigated. A real pilot would need a pre-specified missing-data strategy appropriate to its data-generating process.

## Method follows the question

The final method should depend on the outcome, data structure and decision question.

Examples:

- continuous resolution time with acceptable overlap and uncensored completion → regression/ANCOVA-style analysis may be reasonable;
- binary resolved/unresolved outcome → logistic-type modelling may be more appropriate;
- unresolved cases still under observation → survival/time-to-event analysis may be more appropriate;
- repeated observations within site/team/customer → clustered or hierarchical modelling may be required;
- material department-specific covariate slopes → interaction-aware modelling is preferable to a common-slope ANCOVA;
- policy counterfactual questions → offline policy evaluation rather than ordinary ANCOVA;
- insufficient department/case-type overlap → reject the comparison rather than switch to a more complicated model and pretend identification exists.

The v1.0 applicability gate will make these boundaries explicit as `use`, `caution`, `reject`, or `recommend_alternative` decisions. It will not attempt to implement every possible statistical model.

## Data provenance boundary

Current repository analytics operate on approved development provenance only. Quantitative evidence is synthetic or hand-authored unless explicitly stated otherwise.

Real private pilot or production data remains outside the repository's current approval boundary. Synthetic benchmark success must never be presented as observed service improvement.

## Reproducible commands

Run the outcome workflow:

```bash
ancova-analyze
ancova-analyze --json
```

Run the management-facing report:

```bash
ancova-management-report
```

Run the known-truth validity benchmark:

```bash
ancova-validity
ancova-validity --json
```

A development CSV can be supplied to `ancova-analyze` when it includes an approved `data_provenance` value and all required model fields.

## Interpretation boundary

A statistically significant department term is never sufficient on its own to claim operational causality, staff quality, or policy effectiveness.

The evaluation layer is intended to make unsupported conclusions harder to reach, including by refusing to produce adjusted rankings when the design cannot support them.
