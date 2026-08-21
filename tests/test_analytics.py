import numpy as np
import pytest

from reasoned_ops.analytics import (
    COVARIATES,
    adjusted_department_estimates,
    build_ancova_report,
    department_covariate_interactions,
    fit_ancova,
    heteroskedasticity_diagnostics,
    multicollinearity_diagnostics,
)
from reasoned_ops.synthetic import generate_outcomes


def test_synthetic_data_is_explicitly_labelled() -> None:
    data = generate_outcomes(n=100, seed=7)
    assert set(data["data_provenance"]) == {"synthetic"}


def test_ancova_fit_contains_department_term() -> None:
    data = generate_outcomes(n=200, seed=7)
    result = fit_ancova(data)

    assert "C(department)" in result.formula
    assert "C(department)" in result.anova_table.index


def test_phase2_report_exposes_counts_diagnostics_and_adjusted_estimates() -> None:
    data = generate_outcomes(n=240, seed=17)
    report = build_ancova_report(data)

    assert report.provenance == ("synthetic",)
    assert report.n_rows == 240
    assert report.n_complete_cases == 240
    assert report.n_dropped_for_missingness == 0
    assert sum(report.group_sizes.values()) == 240
    assert set(report.interaction_checks) == set(COVARIATES)
    assert "breusch_pagan_f_pvalue" in report.heteroskedasticity
    assert "n_above_cooks_threshold" in report.influence

    departments = set(data["department"])
    estimates = adjusted_department_estimates(data, fit_ancova(data))
    assert {row["department"] for row in estimates} == departments
    for row in estimates:
        assert row["mean_ci_lower"] < row["adjusted_mean_resolution_hours"]
        assert row["adjusted_mean_resolution_hours"] < row["mean_ci_upper"]


def test_report_makes_complete_case_exclusion_visible() -> None:
    data = generate_outcomes(n=120, seed=21)
    data.loc[:4, "complexity"] = np.nan

    report = build_ancova_report(data)

    assert report.missingness["complexity"]["missing_count"] == 5
    assert report.n_complete_cases == 115
    assert report.n_dropped_for_missingness == 5
    assert any("missingness" in warning.lower() for warning in report.warnings)


def test_heteroskedasticity_screen_detects_known_variance_pattern() -> None:
    data = generate_outcomes(n=600, seed=23)
    rng = np.random.default_rng(23)
    noise_scale = 0.25 + 1.8 * data["urgency"].to_numpy()
    data["resolution_hours"] = (
        8
        + 1.0 * data["urgency"]
        + 0.6 * data["frustration"]
        + 1.4 * data["complexity"]
        + rng.normal(0, noise_scale)
    )

    diagnostics = heteroskedasticity_diagnostics(fit_ancova(data))

    assert diagnostics["breusch_pagan_f_pvalue"] < 0.01


def test_vif_detects_known_collinearity() -> None:
    data = generate_outcomes(n=240, seed=29)
    data["complexity"] = data["urgency"]

    diagnostics = multicollinearity_diagnostics(fit_ancova(data))

    assert any(not np.isfinite(value) or value > 10 for value in diagnostics.values())


def test_interaction_screen_detects_known_department_specific_slope() -> None:
    data = generate_outcomes(n=600, seed=31)
    rng = np.random.default_rng(31)
    department_slope = np.where(data["department"].eq("maintenance"), 5.0, 0.0)
    data["resolution_hours"] = (
        10
        + 0.8 * data["urgency"]
        + department_slope * data["urgency"]
        + 0.5 * data["frustration"]
        + 1.1 * data["complexity"]
        + rng.normal(0, 1.0, size=len(data))
    )

    pvalues = department_covariate_interactions(data)

    assert pvalues["urgency"] < 0.001


def test_generator_rejects_tiny_dataset() -> None:
    with pytest.raises(ValueError):
        generate_outcomes(n=10)
