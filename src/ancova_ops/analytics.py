from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

DEFAULT_FORMULA = (
    "resolution_hours ~ C(department) + urgency + frustration + complexity "
    "+ previous_related_cases"
)


@dataclass(slots=True)
class AncovaResult:
    formula: str
    model: object
    anova_table: pd.DataFrame


def validate_outcome_frame(data: pd.DataFrame) -> None:
    required = {
        "department",
        "urgency",
        "frustration",
        "complexity",
        "previous_related_cases",
        "resolution_hours",
    }
    missing = sorted(required.difference(data.columns))
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
    if len(data) < 20:
        raise ValueError("at least 20 rows are required for the demonstration analysis")


def fit_ancova(data: pd.DataFrame, formula: str = DEFAULT_FORMULA) -> AncovaResult:
    """Fit an OLS ANCOVA-style model and return the model plus ANOVA table."""

    validate_outcome_frame(data)
    model = smf.ols(formula=formula, data=data).fit()
    table = anova_lm(model, typ=2)
    return AncovaResult(formula=formula, model=model, anova_table=table)


def residual_diagnostics(result: AncovaResult) -> dict[str, float]:
    """Return small, machine-readable residual diagnostics for development use."""

    residuals = result.model.resid
    fitted = result.model.fittedvalues
    jb_stat, jb_pvalue, skew, kurtosis = sm.stats.jarque_bera(residuals)
    correlation = float(pd.Series(abs(residuals)).corr(pd.Series(fitted)))
    return {
        "jarque_bera_stat": float(jb_stat),
        "jarque_bera_pvalue": float(jb_pvalue),
        "residual_skew": float(skew),
        "residual_kurtosis": float(kurtosis),
        "abs_residual_fitted_correlation": correlation,
    }
