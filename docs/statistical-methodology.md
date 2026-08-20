# Statistical Methodology

## Role of ANCOVA

Analysis of covariance is an outcome-analysis method in this project. It is not the real-time request classifier.

An example question is:

> After adjusting for urgency, frustration and case complexity, are mean resolution times different across departments?

A simple model can be expressed as:

```text
resolution_hours ~ C(department) + urgency + frustration + complexity
```

An interaction model may ask whether the relationship between frustration and resolution time differs by department:

```text
resolution_hours ~ C(department) * frustration + urgency + complexity
```

## What the model can and cannot establish

A fitted ANCOVA model can describe adjusted associations under its assumptions. It does not automatically prove that changing departments causes an outcome difference. Causal interpretation requires an appropriate study design, defensible treatment assignment and additional assumptions.

## Pre-model checks

Before treating model output as decision evidence, inspect at least:

- missingness and measurement quality;
- extreme values and influential observations;
- whether the covariate/outcome relationship is plausibly linear;
- whether residual variance is severely non-constant;
- residual distribution when inference depends on it;
- multicollinearity;
- group sizes and overlap in covariate distributions;
- homogeneity of regression slopes when using a classical ANCOVA interpretation.

## Homogeneity of regression slopes

A classical ANCOVA comparison assumes the covariate slope is reasonably similar across groups. Test a department-by-covariate interaction when that assumption is important.

If the interaction is meaningful, do not hide it merely to preserve a simpler ANCOVA. The interaction may itself be operationally useful.

## Data provenance labels

Every analytical dataset should be identifiable as one of:

- `synthetic` — generated for software development;
- `benchmark` — copied or reconstructed from an external study with citation;
- `pilot` — collected in a limited project pilot;
- `production` — collected from a deployed system under an approved data-governance process.

Synthetic results must never be reported as observed service performance.

## Current implementation

`ancova_ops.analytics.fit_ancova` uses statsmodels OLS with formula syntax. The function returns the fitted model and an ANOVA table so the caller can inspect model terms rather than consuming a single opaque score.
