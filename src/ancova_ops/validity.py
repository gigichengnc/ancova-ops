from __future__ import annotations

import argparse
import json
from typing import Any

import numpy as np
import pandas as pd

from .analytics import (
    adjusted_department_estimates,
    build_ancova_report,
    department_covariate_interactions,
    fit_ancova,
)
from .synthetic import OUTCOME_DEPARTMENT_EFFECT, generate_outcomes

VALIDITY_BENCHMARK_VERSION = "ancova-validity-v1"
NAIVE_FORMULA = (
    "resolution_hours ~ C(department) + urgency + frustration + complexity "
    "+ previous_related_cases"
)


def generate_measured_confounding_scenario(
    n: int = 2400,
    seed: int = 2026,
    *,
    deterministic_routing: bool = False,
) -> pd.DataFrame:
    """Generate a two-department scenario with known issue-mix confounding."""

    if n < 100:
        raise ValueError("n must be at least 100 for the validity scenario")

    rng = np.random.default_rng(seed)
    issue_category = rng.choice(["complex_repair", "routine_service"], size=n)

    if deterministic_routing:
        department = np.where(
            issue_category == "complex_repair",
            "maintenance",
            "security",
        )
    else:
        department = np.array(
            [
                rng.choice(
                    ["maintenance", "security"],
                    p=[0.88, 0.12] if category == "complex_repair" else [0.12, 0.88],
                )
                for category in issue_category
            ]
        )

    urgency = np.clip(rng.normal(5.0, 1.5, size=n), 0, 10)
    frustration = np.clip(rng.normal(5.0, 1.5, size=n), 0, 10)
    complexity = np.clip(rng.normal(5.0, 1.3, size=n), 0, 10)
    previous_related_cases = rng.poisson(0.6, size=n)

    issue_effect = np.where(issue_category == "complex_repair", 12.0, 0.0)
    department_effect = np.where(department == "security", 2.0, 0.0)
    resolution_hours = (
        8
        + issue_effect
        + department_effect
        + 0.8 * urgency
        + 0.5 * frustration
        + 1.1 * complexity
        + 0.7 * previous_related_cases
        + rng.normal(0, 2.0, size=n)
    )

    return pd.DataFrame(
        {
            "department": department,
            "issue_category": issue_category,
            "urgency": urgency,
            "frustration": frustration,
            "complexity": complexity,
            "previous_related_cases": previous_related_cases,
            "resolution_hours": resolution_hours,
            "data_provenance": "synthetic_validity_benchmark",
        }
    )


def run_validity_benchmark(
    *,
    n: int = 2400,
    seed: int = 2026,
    recovery_tolerance_hours: float = 0.6,
) -> dict[str, Any]:
    """Run deterministic scenarios that test when adjustment should work or stop."""

    recovery_data = generate_outcomes(n=n, seed=seed)
    recovery_report = build_ancova_report(recovery_data)
    recovery_estimates = _estimate_map(recovery_report.adjusted_estimates)
    reference = "accounts"
    recovery_errors: dict[str, float] = {}
    recovery_contrasts: dict[str, dict[str, float]] = {}
    for department, truth_effect in OUTCOME_DEPARTMENT_EFFECT.items():
        if department == reference:
            continue
        estimated = recovery_estimates[department] - recovery_estimates[reference]
        truth = truth_effect - OUTCOME_DEPARTMENT_EFFECT[reference]
        error = abs(estimated - truth)
        recovery_errors[department] = float(error)
        recovery_contrasts[department] = {
            "estimated_difference_hours": float(estimated),
            "known_difference_hours": float(truth),
            "absolute_error_hours": float(error),
        }
    max_recovery_error = max(recovery_errors.values())
    recovery_pass = (
        recovery_report.identifiability["status"] in {"supported", "weak_overlap"}
        and max_recovery_error <= recovery_tolerance_hours
    )

    confounded_data = generate_measured_confounding_scenario(n=n, seed=seed + 1)
    adjusted_report = build_ancova_report(confounded_data)
    adjusted_difference = _contrast(
        adjusted_report.adjusted_estimates,
        "security",
        "maintenance",
    )
    naive_result = fit_ancova(confounded_data, formula=NAIVE_FORMULA)
    naive_estimates = adjusted_department_estimates(confounded_data, naive_result)
    naive_difference = _contrast(naive_estimates, "security", "maintenance")
    known_difference = 2.0
    adjusted_error = abs(adjusted_difference - known_difference)
    naive_error = abs(naive_difference - known_difference)
    confounding_pass = adjusted_error < 0.75 and adjusted_error < naive_error * 0.35

    no_overlap_data = generate_measured_confounding_scenario(
        n=max(400, n // 4),
        seed=seed + 2,
        deterministic_routing=True,
    )
    no_overlap_report = build_ancova_report(no_overlap_data)
    no_overlap_pass = (
        no_overlap_report.identifiability["status"] == "not_identifiable"
        and not no_overlap_report.adjusted_estimates
        and not no_overlap_report.to_dict()["anova"]
    )

    interaction_data = generate_outcomes(n=max(800, n // 2), seed=seed + 3)
    rng = np.random.default_rng(seed + 3)
    department_slope = np.where(
        interaction_data["department"].eq("maintenance"),
        4.0,
        0.0,
    )
    interaction_data["resolution_hours"] = (
        10
        + 0.8 * interaction_data["urgency"]
        + department_slope * interaction_data["urgency"]
        + 0.5 * interaction_data["frustration"]
        + 1.1 * interaction_data["complexity"]
        + rng.normal(0, 1.0, size=len(interaction_data))
    )
    interaction_pvalues = department_covariate_interactions(interaction_data)
    interaction_pass = interaction_pvalues["urgency"] < 0.001

    scenarios = {
        "known_effect_recovery": {
            "pass": bool(recovery_pass),
            "n": int(n),
            "identifiability_status": recovery_report.identifiability["status"],
            "reference_department": reference,
            "tolerance_hours": float(recovery_tolerance_hours),
            "max_absolute_error_hours": float(max_recovery_error),
            "contrasts": recovery_contrasts,
        },
        "measured_confounding": {
            "pass": bool(confounding_pass),
            "n": int(n),
            "known_security_minus_maintenance_hours": known_difference,
            "naive_omits_issue_category_hours": float(naive_difference),
            "case_mix_adjusted_hours": float(adjusted_difference),
            "naive_absolute_error_hours": float(naive_error),
            "adjusted_absolute_error_hours": float(adjusted_error),
            "interpretation": (
                "The deliberately confounded routing design tests whether adding measured issue "
                "category reduces case-mix bias relative to a model that omits it."
            ),
        },
        "no_overlap": {
            "pass": bool(no_overlap_pass),
            "n": len(no_overlap_data),
            "identifiability_status": no_overlap_report.identifiability["status"],
            "adjusted_estimate_count": len(no_overlap_report.adjusted_estimates),
            "anova_term_count": len(no_overlap_report.to_dict()["anova"]),
            "interpretation": (
                "When issue category determines department, the benchmark expects the evaluation "
                "layer to withhold adjusted department comparisons rather than manufacture a "
                "ranking."
            ),
        },
        "slope_interaction": {
            "pass": bool(interaction_pass),
            "n": len(interaction_data),
            "urgency_interaction_pvalue": float(interaction_pvalues["urgency"]),
            "interpretation": (
                "A deliberately department-specific urgency slope should be detected before a "
                "single common-slope ANCOVA interpretation is trusted."
            ),
        },
    }
    overall_pass = all(bool(result["pass"]) for result in scenarios.values())
    return {
        "benchmark_version": VALIDITY_BENCHMARK_VERSION,
        "provenance": "synthetic_validity_benchmark",
        "overall_pass": overall_pass,
        "scenarios": scenarios,
        "interpretation": (
            "This benchmark validates statistical behaviour on known synthetic scenarios. It "
            "does not validate real service outcomes, causal effects, or production deployment."
        ),
    }


def _estimate_map(rows: list[dict[str, float | str]]) -> dict[str, float]:
    return {
        str(row["department"]): float(row["adjusted_mean_resolution_hours"])
        for row in rows
    }


def _contrast(
    rows: list[dict[str, float | str]],
    first: str,
    second: str,
) -> float:
    estimates = _estimate_map(rows)
    return estimates[first] - estimates[second]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run synthetic validity scenarios for ANCOVA Ops outcome evaluation: known-effect "
            "recovery, measured confounding, no-overlap refusal and slope-interaction detection."
        )
    )
    parser.add_argument("--n", type=int, default=2400, help="Rows for primary scenarios.")
    parser.add_argument("--seed", type=int, default=2026, help="Deterministic random seed.")
    parser.add_argument(
        "--recovery-tolerance-hours",
        type=float,
        default=0.6,
        help="Maximum absolute known-effect recovery error (default: 0.6 h).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = run_validity_benchmark(
        n=args.n,
        seed=args.seed,
        recovery_tolerance_hours=args.recovery_tolerance_hours,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("ANCOVA Ops evaluation validity benchmark")
        print(f"Overall pass: {report['overall_pass']}")
        for name, scenario in report["scenarios"].items():
            print(f"- {name}: {'PASS' if scenario['pass'] else 'FAIL'}")
        print(report["interpretation"])
    return 0 if report["overall_pass"] else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
