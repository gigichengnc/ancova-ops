# Evaluation Applicability Gate

## Purpose

ReasonedOps v1.0 completes the research prototype around:

> **Operate → Audit → Evaluate**

The applicability gate is the final guardrail in the Evaluate layer. It asks whether the declared analytical question, outcome type and data structure support the current method family before an adjusted result is interpreted.

The gate does not attempt to implement every statistical method. It makes method selection and refusal explicit so that ANCOVA/regression is not forced onto a question simply because the project is called ReasonedOps.

## High-level dispositions

Every valid declared question returns one of four dispositions.

| Disposition | Meaning |
| --- | --- |
| `use` | The declared method family is plausible for the stated question and structure, subject to its normal diagnostics and interpretation limits. |
| `caution` | The method family may be usable, but support or model assumptions need attention before interpretation. |
| `reject` | The requested adjusted comparison is not identified by the declared data structure and should not be reported. |
| `recommend_alternative` | The question calls for a different analysis family rather than ordinary continuous-outcome ANCOVA/regression. |

A `reject` result is a valid analytical outcome. A more complicated model cannot create identifying information that the observed design does not contain.

## Declared question model

The gate represents:

- outcome type: `continuous`, `binary`, or `time_to_event`;
- comparison type: `department_outcome`, `descriptive`, or `routing_policy`;
- department/case-type overlap: `supported`, `weak_overlap`, `not_identifiable`, or `not_assessed`;
- whether the outcome is censored;
- whether observations are repeated or clustered;
- whether the question has causal intent;
- whether department-specific covariate slopes have been flagged.

The current CLI is:

```bash
reasoned-applicability \
  --outcome-type continuous \
  --comparison department_outcome \
  --overlap-status supported \
  --json
```

## Decision examples

### Continuous department comparison with supported overlap

```text
outcome: continuous
comparison: department_outcome
overlap: supported
censored: no
clustered: no
causal intent: no
interaction flags: none
```

Result:

```text
disposition: use
method family: regression_ancova_style
```

This means the method family is plausible. It does not prove model correctness, causal identification, absence of unmeasured confounding or transportability beyond the observed case mix.

### Weak overlap

Result:

```text
disposition: caution
method family: regression_ancova_style
```

The comparison is structurally estimable but practical support is thin. Conclusions should be restricted to supported case mix or deferred until more overlapping cases exist.

### Department-specific slope detected

Result:

```text
disposition: caution
method family: interaction_aware_regression
```

A common-slope ANCOVA interpretation should not hide material department-specific slopes.

### No department/case-type overlap

Result:

```text
disposition: reject
method family: no_adjusted_department_comparison
```

The correct response is to withhold an adjusted department ranking. Collect overlapping comparable cases, restrict the estimand to a supportable subset, or change the analytical question.

### Binary outcome

Result:

```text
disposition: recommend_alternative
method family: logistic_type_model
```

The gate recommends a binary-outcome model family. Changing the link/distribution does not remove confounding or overlap requirements.

### Censored or time-to-event outcome

Result:

```text
disposition: recommend_alternative
method family: survival_time_to_event_model
```

Unresolved cases still under observation should not simply disappear from a completed-case time analysis.

### Repeated or clustered observations

Result:

```text
disposition: recommend_alternative
method family: clustered_or_hierarchical_model
```

Repeated cases within the same site, team or customer can violate ordinary independence assumptions. Depending on the study, clustered standard errors, GEE, mixed/hierarchical models or another dependence-aware method may be required.

### Routing-policy counterfactual question

Result:

```text
disposition: recommend_alternative
method family: offline_policy_evaluation
```

Observed outcomes under one route are not automatically counterfactual outcomes under another. ReasonedOps already keeps policy evaluation as a separate offline research workflow.

### Causal question

Result:

```text
disposition: recommend_alternative
method family: causal_design_and_identification
```

Ordinary observational adjustment cannot turn a causal question into a causal answer. The intervention, estimand, assignment mechanism and identifying assumptions must be specified separately.

## Priority of identification

For a department comparison, structural non-identifiability is checked before ordinary model-family recommendations. If department and case type cannot be separated from the observed design, the gate returns `reject` even if the outcome itself is continuous.

This reflects an important principle:

> **A different statistical model cannot repair a comparison that the observed design does not identify.**

## Integration with the v0.6 validity layer

The v0.6 outcome report already produces department/case-type overlap and identifiability diagnostics. `assess_from_ancova_report()` reuses that result and any material department-by-covariate interaction flags to generate the final v1 applicability disposition.

The management report displays:

- applicability disposition;
- recommended method family;
- reasons;
- next step;
- interpretation boundary;
- overlap/identifiability status;
- raw and, when supportable, adjusted outcome summaries.

The one-command showcase also surfaces the applicability gate as part of the complete Operate → Audit → Evaluate chain.

## What the gate does not claim

A `use` result does not mean:

- the fitted model is true;
- all confounders have been measured;
- the result is causal;
- a department or staff group should be ranked for performance management;
- the analysis is valid on real private service data;
- the software is ready for production deployment.

The gate is a decision-support guardrail for analytical method selection, not an automatic approval engine.

## v1.0 project boundary

At v1.0, ReasonedOps deliberately stops short of implementing every alternative analysis family. Logistic, survival, hierarchical and causal methods are recommendations unless separately implemented in an existing dedicated research workflow.

The research/portfolio project is considered complete when the gate, validity tests, management output, showcase and CI all work together. Future modelling or deployment should require a concrete external reason rather than being added simply because further complexity is possible.
