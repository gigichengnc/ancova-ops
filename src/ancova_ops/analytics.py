from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor

COVARIATES = ("urgency", "frustration", "complexity", "previous_related_cases")
REQUIRED_COLUMNS = ("department", *COVARIATES, "resolution_hours")
DEFAULT_FORMULA = (
    "resolution_hours ~ C(department) + urgency + frustration + complexity "
    "+ previous_related_cases"
)


@dataclass(slots=True)
class AncovaResult:
    formula: str
    model: object
    anova_table: pd.DataFrame


@dataclass(slots=True)
class AncovaReport:
    formula: str
    provenance: tuple[str, ...]
    n_rows: int
    n_complete_cases: int
    n_dropped_for_missingness: int
    missingness: dict[str, dict[str, float | int]]
    group_sizes: dict[str, int]
    residual_diagnostics: dict[str, float]
    heteroskedasticity: dict[str, float]
    multicollinearity: dict[str, float]
    influence: dict[str, float | int]
    interaction_checks: dict[str, float]
    adjusted_estimates: list[dict[str, float | str]]
    warnings: list[str]
    interpretation_note: str
    model: object
    anova_table: pd.DataFrame

    def to_dict(self) -> dict[str, object]:
        return {
            "formula": self.formula,
            "provenance": list(self.provenance),
            "sample": {
                "n_rows": self.n_rows,
                "n_complete_cases": self.n_complete_cases,
                "n_dropped_for_missingness": self.n_dropped_for_missingness,
                "group_sizes": self.group_sizes,
            },
            "missingness": self.missingness,
            "diagnostics": {
                "residuals": self.residual_diagnostics,
                "heteroskedasticity": self.heteroskedasticity,
                "multicollinearity_vif": self.multicollinearity,
                "influence": self.influence,
                "department_by_covariate_interactions": self.interaction_checks,
            },
            "adjusted_estimates": self.adjusted_estimates,
            "anova": _frame_records(self.anova_table.reset_index(names="term")),
            "warnings": self.warnings,
            "interpretation_note": self.interpretation_note,
        }


def validate_outcome_frame(data: pd.DataFrame, *, minimum_rows: int = 20) -> None:
    missing = sorted(set(REQUIRED_COLUMNS).difference(data.columns))
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
    if len(data) < minimum_rows:
        raise ValueError(f"at least {minimum_rows} rows are required for the analysis")

    for column in COVARIATES + ("resolution_hours",):
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"column {column!r} must be numeric")

    departments = data["department"].dropna().astype(str).unique()
    if len(departments) < 2:
        raise ValueError("at least two departments are required for adjusted comparisons")


def prepare_complete_cases(data: pd.DataFrame) -> pd.DataFrame:
    validate_outcome_frame(data)
    complete = data.dropna(subset=list(REQUIRED_COLUMNS)).copy()
    if len(complete) < 20:
        raise ValueError("fewer than 20 complete cases remain after removing required-field missingness")
    if complete["department"].astype(str).nunique() < 2:
        raise ValueError("fewer than two departments remain after removing required-field missingness")
    return complete


def fit_ancova(data: pd.DataFrame, formula: str = DEFAULT_FORMULA) -> AncovaResult:
    """Fit an OLS ANCOVA-style model and return the model plus ANOVA table."""

    complete = prepare_complete_cases(data)
    model = smf.ols(formula=formula, data=complete).fit()
    table = anova_lm(model, typ=2)
    return AncovaResult(formula=formula, model=model, anova_table=table)


def missingness_summary(data: pd.DataFrame) -> dict[str, dict[str, float | int]]:
    """Summarise missingness for the fields required by the default outcome model."""

    validate_outcome_frame(data)
    total = len(data)
    return {
        column: {
            "missing_count": int(data[column].isna().sum()),
            "missing_fraction": float(data[column].isna().mean()) if total else 0.0,
        }
        for column in REQUIRED_COLUMNS
    }


def residual_diagnostics(result: AncovaResult) -> dict[str, float]:
    """Return machine-readable residual diagnostics for development use."""

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


def heteroskedasticity_diagnostics(result: AncovaResult) -> dict[str, float]:
    """Run a Breusch-Pagan check using the fitted model design matrix."""

    lm_stat, lm_pvalue, f_stat, f_pvalue = het_breuschpagan(
        result.model.resid,
        result.model.model.exog,
    )
    return {
        "breusch_pagan_lm_stat": float(lm_stat),
        "breusch_pagan_lm_pvalue": float(lm_pvalue),
        "breusch_pagan_f_stat": float(f_stat),
        "breusch_pagan_f_pvalue": float(f_pvalue),
    }


def multicollinearity_diagnostics(result: AncovaResult) -> dict[str, float]:
    """Return VIF values for fitted design-matrix columns except the intercept."""

    exog = np.asarray(result.model.model.exog, dtype=float)
    names = list(result.model.model.exog_names)
    values: dict[str, float] = {}
    for index, name in enumerate(names):
        if name.lower() == "intercept":
            continue
        try:
            vif = float(variance_inflation_factor(exog, index))
        except (FloatingPointError, ValueError, np.linalg.LinAlgError):
            vif = float("inf")
        values[name] = vif
    return values


def influence_diagnostics(result: AncovaResult) -> dict[str, float | int]:
    """Summarise Cook's distance and leverage using conventional screening thresholds."""

    influence = OLSInfluence(result.model)
    cooks = np.asarray(influence.cooks_distance[0], dtype=float)
    leverage = np.asarray(influence.hat_matrix_diag, dtype=float)
    n = int(result.model.nobs)
    p = int(result.model.df_model) + 1
    cooks_threshold = 4.0 / n
    leverage_threshold = 2.0 * p / n

    return {
        "cooks_distance_threshold": float(cooks_threshold),
        "n_above_cooks_threshold": int(np.sum(cooks > cooks_threshold)),
        "max_cooks_distance": float(np.nanmax(cooks)),
        "leverage_threshold": float(leverage_threshold),
        "n_above_leverage_threshold": int(np.sum(leverage > leverage_threshold)),
        "max_leverage": float(np.nanmax(leverage)),
    }


def department_covariate_interactions(
    data: pd.DataFrame,
    covariates: tuple[str, ...] = COVARIATES,
) -> dict[str, float]:
    """Check department-by-covariate interactions for homogeneity-of-slopes concerns."""

    complete = prepare_complete_cases(data)
    pvalues: dict[str, float] = {}

    for covariate in covariates:
        other_covariates = [name for name in covariates if name != covariate]
        rhs = f"C(department) * {covariate}"
        if other_covariates:
            rhs += " + " + " + ".join(other_covariates)
        formula = f"resolution_hours ~ {rhs}"
        model = smf.ols(formula=formula, data=complete).fit()
        table = anova_lm(model, typ=2)
        term = f"C(department):{covariate}"
        pvalues[covariate] = float(table.loc[term, "PR(>F)"])

    return pvalues


def adjusted_department_estimates(
    data: pd.DataFrame,
    result: AncovaResult,
    *,
    alpha: float = 0.05,
) -> list[dict[str, float | str]]:
    """Estimate department means with covariates held at complete-case sample means."""

    complete = prepare_complete_cases(data)
    covariate_reference = {name: float(complete[name].mean()) for name in COVARIATES}
    departments = sorted(complete["department"].astype(str).unique())
    prediction_frame = pd.DataFrame(
        [{"department": department, **covariate_reference} for department in departments]
    )
    prediction = result.model.get_prediction(prediction_frame).summary_frame(alpha=alpha)

    estimates: list[dict[str, float | str]] = []
    for index, department in enumerate(departments):
        row = prediction.iloc[index]
        estimates.append(
            {
                "department": department,
                "adjusted_mean_resolution_hours": float(row["mean"]),
                "confidence_level": float(1.0 - alpha),
                "mean_ci_lower": float(row["mean_ci_lower"]),
                "mean_ci_upper": float(row["mean_ci_upper"]),
            }
        )
    return estimates


def build_ancova_report(
    data: pd.DataFrame,
    *,
    formula: str = DEFAULT_FORMULA,
    alpha: float = 0.05,
) -> AncovaReport:
    """Build the Phase 2 outcome-analysis report with diagnostics and explicit warnings."""

    validate_outcome_frame(data)
    missingness = missingness_summary(data)
    complete = prepare_complete_cases(data)
    result = fit_ancova(complete, formula=formula)
    residuals = residual_diagnostics(result)
    heteroskedasticity = heteroskedasticity_diagnostics(result)
    vif = multicollinearity_diagnostics(result)
    influence = influence_diagnostics(result)
    interactions = department_covariate_interactions(complete)
    adjusted = adjusted_department_estimates(complete, result, alpha=alpha)
    group_sizes = {
        str(name): int(count)
        for name, count in complete["department"].astype(str).value_counts().sort_index().items()
    }
    provenance = _extract_provenance(data)
    warnings = _analysis_warnings(
        missingness=missingness,
        group_sizes=group_sizes,
        residuals=residuals,
        heteroskedasticity=heteroskedasticity,
        vif=vif,
        influence=influence,
        interactions=interactions,
        alpha=alpha,
    )

    return AncovaReport(
        formula=formula,
        provenance=provenance,
        n_rows=len(data),
        n_complete_cases=len(complete),
        n_dropped_for_missingness=len(data) - len(complete),
        missingness=missingness,
        group_sizes=group_sizes,
        residual_diagnostics=residuals,
        heteroskedasticity=heteroskedasticity,
        multicollinearity=vif,
        influence=influence,
        interaction_checks=interactions,
        adjusted_estimates=adjusted,
        warnings=warnings,
        interpretation_note=(
            "Adjusted estimates describe model-based associations with covariates held at their "
            "complete-case sample means. They are not causal effects unless the study design and "
            "identification assumptions separately justify a causal interpretation."
        ),
        model=result.model,
        anova_table=result.anova_table,
    )


def _analysis_warnings(
    *,
    missingness: dict[str, dict[str, float | int]],
    group_sizes: dict[str, int],
    residuals: dict[str, float],
    heteroskedasticity: dict[str, float],
    vif: dict[str, float],
    influence: dict[str, float | int],
    interactions: dict[str, float],
    alpha: float,
) -> list[str]:
    warnings: list[str] = []

    missing_fields = [
        field for field, summary in missingness.items() if int(summary["missing_count"]) > 0
    ]
    if missing_fields:
        warnings.append(
            "Required-field missingness caused complete-case exclusion; inspect missing-data "
            "mechanisms before treating complete-case estimates as representative: "
            + ", ".join(missing_fields)
            + "."
        )

    small_groups = [name for name, count in group_sizes.items() if count < 10]
    if small_groups:
        warnings.append(
            "At least one department has fewer than 10 complete cases; uncertainty and diagnostics "
            "may be unstable: "
            + ", ".join(small_groups)
            + "."
        )

    if heteroskedasticity["breusch_pagan_f_pvalue"] < alpha:
        warnings.append(
            "Breusch-Pagan screening suggests non-constant residual variance. Consider robust "
            "standard errors, a variance model, transformation, or a more suitable outcome model."
        )

    finite_vifs = [value for value in vif.values() if isfinite(value)]
    max_vif = max(finite_vifs, default=0.0)
    if any(not isfinite(value) for value in vif.values()) or max_vif > 5.0:
        warnings.append(
            "High multicollinearity is present in the fitted design matrix; coefficient-level "
            "interpretation may be unstable. Review redundant predictors or re-specify the model."
        )

    if residuals["jarque_bera_pvalue"] < alpha:
        warnings.append(
            "Residual normality screening is poor. For a positive/skewed time outcome, inspect a "
            "transformation, robust inference, or a distribution better matched to resolution time."
        )

    significant_interactions = [
        covariate for covariate, pvalue in interactions.items() if pvalue < alpha
    ]
    if significant_interactions:
        warnings.append(
            "Department-by-covariate interaction screening questions homogeneity of slopes for: "
            + ", ".join(significant_interactions)
            + ". Prefer an interaction-aware model rather than hiding the differing slopes."
        )

    if int(influence["n_above_cooks_threshold"]) > 0:
        warnings.append(
            "Potentially influential observations exceed the Cook's-distance screening threshold. "
            "Inspect them and run sensitivity analyses rather than deleting them automatically."
        )

    return warnings


def _extract_provenance(data: pd.DataFrame) -> tuple[str, ...]:
    if "data_provenance" not in data.columns:
        return ("unlabelled",)
    values = sorted({str(value) for value in data["data_provenance"].dropna().unique()})
    return tuple(values) if values else ("unlabelled",)


def _frame_records(frame: pd.DataFrame) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for record in frame.to_dict(orient="records"):
        clean: dict[str, object] = {}
        for key, value in record.items():
            if isinstance(value, (np.integer,)):
                clean[key] = int(value)
            elif isinstance(value, (np.floating, float)):
                clean[key] = None if pd.isna(value) else float(value)
            else:
                clean[key] = value
        records.append(clean)
    return records
