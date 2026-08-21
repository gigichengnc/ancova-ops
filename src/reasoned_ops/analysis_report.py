from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

from reasoned_ops.analytics import build_ancova_report
from reasoned_ops.governance import (
    assert_development_provenance,
    load_policy,
    validate_policy,
)
from reasoned_ops.synthetic import generate_outcomes


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the ReasonedOps outcome-evaluation workflow with case-mix/overlap checks, "
            "diagnostics, adjusted department estimates where identifiable, uncertainty and warnings."
        )
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--csv", type=Path, help="CSV dataset to analyse.")
    source.add_argument(
        "--synthetic-n",
        type=int,
        default=500,
        help="Number of synthetic rows when --csv is not supplied (default: 500).",
    )
    parser.add_argument("--seed", type=int, default=2026, help="Synthetic-data random seed.")
    parser.add_argument("--alpha", type=float, default=0.05, help="Inference alpha level.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser


def load_input(args: argparse.Namespace) -> pd.DataFrame:
    if args.csv is None:
        return generate_outcomes(n=args.synthetic_n, seed=args.seed)

    data = pd.read_csv(args.csv)
    if "data_provenance" not in data.columns:
        raise ValueError(
            "CSV input must include data_provenance so development data boundaries can be checked"
        )

    policy = load_policy()
    validate_policy(policy)
    provenance_values = sorted({str(value) for value in data["data_provenance"].dropna().unique()})
    if not provenance_values:
        raise ValueError("CSV input contains no usable data_provenance value")
    for provenance in provenance_values:
        assert_development_provenance(provenance, policy)
    return data


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _print_text(payload: dict[str, object]) -> None:
    sample = payload["sample"]
    diagnostics = payload["diagnostics"]
    adjusted = payload["adjusted_estimates"]
    warnings = payload["warnings"]
    identifiability = payload["identifiability"]

    assert isinstance(sample, dict)
    assert isinstance(diagnostics, dict)
    assert isinstance(adjusted, list)
    assert isinstance(warnings, list)
    assert isinstance(identifiability, dict)

    print("ReasonedOps outcome evaluation")
    print(f"Formula: {payload['formula']}")
    print(f"Provenance: {', '.join(payload['provenance'])}")
    print(
        "Sample: "
        f"{sample['n_complete_cases']} complete / {sample['n_rows']} total "
        f"({sample['n_dropped_for_missingness']} dropped for required-field missingness)"
    )
    print("Group sizes:")
    for department, count in sample["group_sizes"].items():
        print(f"  - {department}: {count}")

    print(f"Department/issue-category identifiability: {identifiability['status']}")
    print(f"  - {identifiability['note']}")

    if adjusted:
        print("Adjusted department estimates (standardised over observed complete-case case mix):")
        for row in adjusted:
            print(
                "  - "
                f"{row['department']}: {row['adjusted_mean_resolution_hours']:.2f} h "
                f"[{row['mean_ci_lower']:.2f}, {row['mean_ci_upper']:.2f}]"
            )
    else:
        print(
            "Adjusted department estimates: withheld because the observed routing design does "
            "not separately identify department from issue-category case mix."
        )

    heteroskedasticity = diagnostics["heteroskedasticity"]
    print(
        "Breusch-Pagan F-test p-value: "
        f"{heteroskedasticity['breusch_pagan_f_pvalue']:.4g}"
    )
    interactions = diagnostics["department_by_covariate_interactions"]
    finite_interactions = {
        covariate: pvalue
        for covariate, pvalue in interactions.items()
        if isinstance(pvalue, (int, float)) and math.isfinite(float(pvalue))
    }
    if finite_interactions:
        print("Department-by-covariate interaction p-values:")
        for covariate, pvalue in finite_interactions.items():
            print(f"  - {covariate}: {float(pvalue):.4g}")
    else:
        print("Department-by-covariate interaction screening: withheld / not applicable")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("Warnings: none triggered by the current screening rules")

    print(f"Interpretation: {payload['interpretation_note']}")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if not 0 < args.alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    data = load_input(args)
    report = build_ancova_report(data, alpha=args.alpha)
    payload = report.to_dict()

    if args.json:
        print(json.dumps(_json_safe(payload), indent=2, sort_keys=True, allow_nan=False))
    else:
        _print_text(payload)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())