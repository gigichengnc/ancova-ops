# Statistical Methodology

## Role of ANCOVA

Analysis of covariance is an outcome-analysis method in this project. It is not the real-time request classifier.

The current pre-specified development question is:

> After adjusting for urgency, frustration, case complexity and previous related cases, are model-based mean resolution times different across departments?

The default model is:

```text
resolution_hours ~ C(department) + urgency + frustration + complexity + previous_related_cases
```

This is an OLS regression / ANCOVA-style model. Department is treated as the grouping factor and the remaining terms as covariates.

## What the model can and cannot establish

The Phase 2 workflow estimates adjusted associations under the fitted model and its assumptions. It does **not** automatically establish that moving a case to another department would cause its resolution time to change.

Causal interpretation would require a study design and identification strategy that justify treatment assignment, exchangeability and other causal assumptions. Operational observational data should therefore be described as adjusted association unless stronger evidence exists.

## Data provenance boundary

Every analytical dataset must carry a provenance label. The current development policy approves synthetic and hand-authored development data only. Real private pilot or production data is not approved by the repository's current governance policy.

Synthetic results must never be reported as observed service performance.

## Complete-case policy

The current implementation uses complete cases for the fields required by the default model. This is a transparent development baseline, not a claim that complete-case analysis is universally appropriate.

The report therefore exposes:

- missing count and missing fraction for every required field;
- total row count;
- complete-case count;
- number of rows excluded for required-field missingness;
- complete-case department group sizes.

If required-field missingness is present, the report warns that the missing-data mechanism must be investigated before the resulting estimates are treated as representative. A future pilot should pre-specify whether complete-case analysis, multiple imputation, inverse-probability methods or another approach is justified.

## Diagnostics

`ancova-analyze` reports the following screening diagnostics.

### Residual distribution

Jarque-Bera statistics, residual skew and residual kurtosis are reported. A poor normality screen is not, by itself, a reason to discard OLS, but it is a prompt to inspect whether inference or the outcome distribution is poorly matched to the model.

### Residual variance

A Breusch-Pagan test screens for heteroskedasticity. If residual variance is strongly non-constant, consider robust standard errors, an explicit variance model, transformation, or an outcome model whose distribution better matches resolution time.

### Multicollinearity

Variance inflation factors are reported for non-intercept design-matrix columns. High VIF values indicate that coefficient-level interpretation may be unstable because predictors contain redundant information.

### Influential observations

Cook's distance and leverage are summarised with conventional screening thresholds. Flagged observations are not automatically errors and must not be deleted mechanically. They should be inspected and included in sensitivity analyses.

### Homogeneity of slopes

For each default covariate, the workflow fits a department-by-covariate interaction screen. For example:

```text
resolution_hours ~ C(department) * frustration + urgency + complexity + previous_related_cases
```

A meaningful interaction questions the classical ANCOVA assumption that the covariate slope is sufficiently similar across departments. If an interaction matters, prefer an interaction-aware model rather than removing the interaction simply to preserve a simpler ANCOVA.

## Adjusted department estimates

The report produces a model-based adjusted mean resolution time for each observed department, with a confidence interval. In the current implementation, the covariates are held at their complete-case sample means.

These are adjusted estimates, not raw departmental averages and not causal treatment effects. The report states this limitation explicitly.

## When the default ANCOVA-style model is not appropriate

The workflow emits warnings rather than silently switching models. Depending on the failure mode, a later analysis may need:

- heteroskedasticity-robust inference or a variance model when residual variance is non-constant;
- an interaction-aware regression when department-specific slopes are important;
- transformation, Gamma/log-link modelling, survival/time-to-event analysis or another positive-outcome model when resolution time is strongly skewed or censored;
- robust regression or sensitivity analysis when a small number of observations dominate the fit;
- predictor reduction or re-specification when multicollinearity is severe;
- a pre-specified missing-data strategy when complete-case exclusion is not defensible;
- hierarchical/multilevel models when outcomes are clustered by building, team, resident or time period;
- designs and methods specifically intended for causal inference if the question is causal rather than descriptive/associational.

The existence of a statistically significant department term is never sufficient on its own to claim operational causality.

## Reproducible command

Run the complete synthetic development report with:

```bash
ancova-analyze
```

Machine-readable output:

```bash
ancova-analyze --json
```

A development CSV can be supplied with:

```bash
ancova-analyze --csv path/to/data.csv --json
```

CSV input must contain `data_provenance`. The command validates the provenance against the repository's current development governance policy before analysis, so pilot or production provenance remains blocked until governance is separately updated and approved.

## Programmatic API

`ancova_ops.analytics.build_ancova_report()` returns:

- formula and data provenance;
- row counts and group sizes;
- required-field missingness;
- residual diagnostics;
- Breusch-Pagan heteroskedasticity diagnostics;
- VIF multicollinearity diagnostics;
- Cook's-distance and leverage summaries;
- department-by-covariate interaction p-values;
- adjusted department estimates with uncertainty;
- an ANOVA table;
- explicit warnings and a non-causal interpretation note.

The lower-level `fit_ancova()` helper remains available when direct access to the fitted statsmodels object is needed.
