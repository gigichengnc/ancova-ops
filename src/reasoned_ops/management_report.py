from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from ancova_ops.analysis_report import load_input
from ancova_ops.analytics import AncovaReport, build_ancova_report, prepare_complete_cases
from ancova_ops.applicability import assess_from_ancova_report

DEFAULT_OUTPUT = Path(".ancova_ops/reports/management-report.md")


@dataclass(slots=True)
class ManagementReport:
    provenance: tuple[str, ...]
    formula: str
    confidence_level: float
    overall_screening_status: str
    applicability: dict[str, object]
    executive_summary: str
    sample: dict[str, object]
    department_comparison: list[dict[str, object]]
    screening_status: list[dict[str, str]]
    warnings: list[str]
    interpretation_note: str
    technical: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "provenance": list(self.provenance),
            "formula": self.formula,
            "confidence_level": self.confidence_level,
            "overall_screening_status": self.overall_screening_status,
            "applicability": self.applicability,
            "executive_summary": self.executive_summary,
            "sample": self.sample,
            "department_comparison": self.department_comparison,
            "screening_status": self.screening_status,
            "warnings": self.warnings,
            "interpretation_note": self.interpretation_note,
            "technical": self.technical,
        }


def build_management_report(data: pd.DataFrame, *, alpha: float = 0.05) -> ManagementReport:
    """Build a management-facing view over the reproducible outcome-evaluation workflow."""

    analysis = build_ancova_report(data, alpha=alpha)
    applicability_decision = assess_from_ancova_report(analysis, alpha=alpha)
    applicability = applicability_decision.to_dict()

    complete = prepare_complete_cases(data)
    raw = _raw_department_summary(complete)
    adjusted = {str(row["department"]): row for row in analysis.adjusted_estimates}

    comparison: list[dict[str, object]] = []
    for department in sorted(raw):
        raw_row = raw[department]
        row: dict[str, object] = {
            "department": department,
            "complete_case_n": int(raw_row["n"]),
            "raw_mean_resolution_hours": float(raw_row["mean"]),
            "raw_median_resolution_hours": float(raw_row["median"]),
            "adjusted_mean_resolution_hours": None,
            "adjusted_ci_lower": None,
            "adjusted_ci_upper": None,
        }
        if department in adjusted:
            adjusted_row = adjusted[department]
            row.update(
                {
                    "adjusted_mean_resolution_hours": float(
                        adjusted_row["adjusted_mean_resolution_hours"]
                    ),
                    "adjusted_ci_lower": float(adjusted_row["mean_ci_lower"]),
                    "adjusted_ci_upper": float(adjusted_row["mean_ci_upper"]),
                }
            )
        comparison.append(row)

    screening = _screening_status(analysis, alpha=alpha)
    disposition = str(applicability["disposition"])
    if disposition == "reject":
        overall_status = "blocked"
    elif disposition in {"caution", "recommend_alternative"}:
        overall_status = "caution"
    else:
        overall_status = (
            "caution" if any(row["status"] == "caution" for row in screening) else "clear"
        )

    executive_summary = _executive_summary(
        analysis,
        comparison,
        overall_status,
        applicability=applicability,
    )

    technical = {
        "identifiability": analysis.identifiability,
        "residual_diagnostics": analysis.residual_diagnostics,
        "heteroskedasticity": analysis.heteroskedasticity,
        "multicollinearity_vif": analysis.multicollinearity,
        "influence": analysis.influence,
        "department_by_covariate_interactions": analysis.interaction_checks,
    }

    return ManagementReport(
        provenance=analysis.provenance,
        formula=analysis.formula,
        confidence_level=1.0 - alpha,
        overall_screening_status=overall_status,
        applicability=applicability,
        executive_summary=executive_summary,
        sample={
            "n_rows": analysis.n_rows,
            "n_complete_cases": analysis.n_complete_cases,
            "n_dropped_for_missingness": analysis.n_dropped_for_missingness,
            "group_sizes": analysis.group_sizes,
            "missingness": analysis.missingness,
        },
        department_comparison=comparison,
        screening_status=screening,
        warnings=list(analysis.warnings),
        interpretation_note=analysis.interpretation_note,
        technical=technical,
    )


def render_markdown(report: ManagementReport) -> str:
    """Render a self-contained management report suitable for review and versioning."""

    provenance = ", ".join(report.provenance)
    sample = report.sample
    confidence_percent = report.confidence_level * 100
    identifiability = report.technical["identifiability"]
    assert isinstance(identifiability, dict)

    disposition = str(report.applicability["disposition"])
    method_family = str(report.applicability["method_family"])
    next_step = str(report.applicability["next_step"])
    reasons = report.applicability["reasons"]
    assert isinstance(reasons, (list, tuple))

    report_boundary = (
        "> This report separates raw observed summaries from model-adjusted estimates. "
        "Adjusted values are associations, not causal effects, and are withheld when the "
        "routing design cannot separate department from issue-category case mix."
    )
    comparison_note = (
        "Raw means describe the complete-case observations. Where identifiable, adjusted means "
        "are standardised over the observed complete-case case-mix distribution rather than "
        "holding a categorical issue type at an arbitrary reference."
    )

    lines = [
        "# ANCOVA Ops Management Outcome Report",
        "",
        f"**Data provenance:** {provenance}",
        f"**Screening status:** {report.overall_screening_status.upper()}",
        f"**Evaluation applicability:** {disposition.upper()}",
        f"**Recommended method family:** `{method_family}`",
        f"**Department/issue-category identifiability:** {identifiability['status']}",
        "",
        report_boundary,
        "",
        "## Executive summary",
        "",
        report.executive_summary,
        "",
        "## Evaluation applicability gate",
        "",
        (
            "The applicability gate asks whether the declared question/data structure supports the "
            "current method before management interprets an adjusted comparison."
        ),
        "",
        f"**Disposition:** `{disposition}`",
        f"**Method family:** `{method_family}`",
        "",
        "Reasons:",
    ]
    for reason in reasons:
        lines.append(f"- {reason}")
    lines.extend(
        [
            "",
            f"**Next step:** {next_step}",
            "",
            f"**Boundary:** {report.applicability['interpretation_boundary']}",
            "",
            "## Data and sample",
            "",
            f"- Total rows: {sample['n_rows']}",
            f"- Complete cases used by the model: {sample['n_complete_cases']}",
            f"- Rows excluded for required-field missingness: {sample['n_dropped_for_missingness']}",
            f"- Model formula: `{report.formula}`",
            "",
            "## Department comparison",
            "",
            comparison_note,
            "",
            (
                "| Department | N | Raw mean (h) | Raw median (h) | Adjusted mean (h) | "
                f"{confidence_percent:.0f}% CI (h) |"
            ),
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for row in report.department_comparison:
        if row["adjusted_mean_resolution_hours"] is None:
            adjusted_text = "withheld"
            ci_text = "withheld"
        else:
            adjusted_text = f"{float(row['adjusted_mean_resolution_hours']):.2f}"
            ci_text = (
                f"{float(row['adjusted_ci_lower']):.2f}–"
                f"{float(row['adjusted_ci_upper']):.2f}"
            )
        lines.append(
            f"| {row['department']} | {row['complete_case_n']} | "
            f"{float(row['raw_mean_resolution_hours']):.2f} | "
            f"{float(row['raw_median_resolution_hours']):.2f} | "
            f"{adjusted_text} | {ci_text} |"
        )

    lines.extend(
        [
            "",
            "## Statistical screening dashboard",
            "",
            (
                "A `clear` result means the current screening rule did not flag that issue; it "
                "does not prove the assumption is true. A `blocked` result means the adjusted "
                "comparison should not be reported from the current design."
            ),
            "",
            "| Area | Status | Management interpretation |",
            "| --- | --- | --- |",
        ]
    )
    for row in report.screening_status:
        lines.append(f"| {row['area']} | {row['status']} | {row['interpretation']} |")

    lines.extend(["", "## Warnings and decision implications", ""])
    if report.warnings:
        for warning in report.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append(
            "- No warning was triggered by the current screening rules. This is not evidence "
            "that every modelling assumption is satisfied."
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            report.interpretation_note,
            "",
            (
                "For management use, identifiable adjusted department estimates are case-mix-aware "
                "signals for investigation and operational learning. They should not be used as a "
                "causal league table or as an automatic basis for staff performance decisions. If "
                "overlap is insufficient, the correct output is to withhold the comparison rather "
                "than rank teams."
            ),
            "",
            "## Technical appendix",
            "",
            "### Department/issue-category overlap",
            "",
            f"- Status: {identifiability['status']}",
            f"- Design-matrix full rank: {identifiability['design_matrix_full_rank']}",
            (
                "- Practical overlap graph connected: "
                f"{identifiability['practical_overlap_graph_connected']}"
            ),
            f"- Minimum supported cell size: {identifiability['minimum_cell_n']}",
            "",
            "### Department-by-covariate interaction p-values",
            "",
            "| Covariate | p-value |",
            "| --- | ---: |",
        ]
    )

    interactions = report.technical["department_by_covariate_interactions"]
    assert isinstance(interactions, dict)
    for covariate, pvalue in interactions.items():
        numeric = float(pvalue)
        display = "withheld" if not math.isfinite(numeric) else f"{numeric:.4g}"
        lines.append(f"| {covariate} | {display} |")

    lines.extend(["", "### Variance and influence screening", ""])
    heteroskedasticity = report.technical["heteroskedasticity"]
    influence = report.technical["influence"]
    assert isinstance(heteroskedasticity, dict)
    assert isinstance(influence, dict)
    lines.extend(
        [
            (
                "- Breusch-Pagan F-test p-value: "
                f"{float(heteroskedasticity['breusch_pagan_f_pvalue']):.4g}"
            ),
            (
                "- Observations above Cook's-distance screening threshold: "
                f"{int(influence['n_above_cooks_threshold'])}"
            ),
            (
                "- Observations above leverage screening threshold: "
                f"{int(influence['n_above_leverage_threshold'])}"
            ),
            "",
            "### Multicollinearity VIF",
            "",
            "| Model term | VIF |",
            "| --- | ---: |",
        ]
    )

    vif = report.technical["multicollinearity_vif"]
    assert isinstance(vif, dict)
    if vif:
        for term, value in vif.items():
            display = "∞" if not math.isfinite(float(value)) else f"{float(value):.2f}"
            lines.append(f"| {term} | {display} |")
    else:
        lines.append("| not reported | comparison not identifiable |")

    lines.append("")
    return "\n".join(lines)


def write_management_report(
    data: pd.DataFrame,
    output: str | Path = DEFAULT_OUTPUT,
    *,
    json_output: str | Path | None = None,
    alpha: float = 0.05,
) -> ManagementReport:
    report = build_management_report(data, alpha=alpha)
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(report), encoding="utf-8")

    if json_output is not None:
        json_target = Path(json_output)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(
            json.dumps(_json_safe(report.to_dict()), indent=2, sort_keys=True, allow_nan=False),
            encoding="utf-8",
        )
    return report


def _raw_department_summary(complete: pd.DataFrame) -> dict[str, dict[str, float | int]]:
    grouped = complete.assign(department=complete["department"].astype(str)).groupby("department")
    return {
        str(department): {
            "n": int(group["resolution_hours"].count()),
            "mean": float(group["resolution_hours"].mean()),
            "median": float(group["resolution_hours"].median()),
        }
        for department, group in grouped
    }


def _screening_status(analysis: AncovaReport, *, alpha: float) -> list[dict[str, str]]:
    finite_vif = [
        float(value) for value in analysis.multicollinearity.values() if math.isfinite(float(value))
    ]
    max_vif = max(finite_vif, default=0.0)
    has_infinite_vif = any(
        not math.isfinite(float(value)) for value in analysis.multicollinearity.values()
    )
    interaction_flags = [
        covariate
        for covariate, pvalue in analysis.interaction_checks.items()
        if math.isfinite(float(pvalue)) and float(pvalue) < alpha
    ]

    overlap_status = str(analysis.identifiability["status"])
    overlap_row = {
        "area": "Department/issue-category overlap",
        "status": (
            "blocked"
            if overlap_status == "not_identifiable"
            else ("caution" if overlap_status == "weak_overlap" else "clear")
        ),
        "interpretation": str(analysis.identifiability["note"]),
    }

    return [
        overlap_row,
        {
            "area": "Required-field missingness",
            "status": "caution" if analysis.n_dropped_for_missingness else "clear",
            "interpretation": (
                "Some rows were excluded; assess the missing-data mechanism."
                if analysis.n_dropped_for_missingness
                else "No required-field exclusions in this dataset."
            ),
        },
        {
            "area": "Residual variance",
            "status": (
                "caution"
                if analysis.heteroskedasticity["breusch_pagan_f_pvalue"] < alpha
                else "clear"
            ),
            "interpretation": (
                "Non-constant variance was flagged; standard OLS uncertainty may be unreliable."
                if analysis.heteroskedasticity["breusch_pagan_f_pvalue"] < alpha
                else "Breusch-Pagan screening did not flag non-constant variance."
            ),
        },
        {
            "area": "Residual distribution",
            "status": (
                "caution"
                if analysis.residual_diagnostics["jarque_bera_pvalue"] < alpha
                else "clear"
            ),
            "interpretation": (
                "Residual normality screening was poor; inspect a better-matched outcome model."
                if analysis.residual_diagnostics["jarque_bera_pvalue"] < alpha
                else "Jarque-Bera screening did not flag strong non-normality."
            ),
        },
        {
            "area": "Multicollinearity",
            "status": (
                "caution"
                if analysis.multicollinearity and (has_infinite_vif or max_vif > 5)
                else "clear"
            ),
            "interpretation": (
                "At least one fitted term has high VIF; coefficient interpretation may be unstable."
                if analysis.multicollinearity and (has_infinite_vif or max_vif > 5)
                else (
                    "VIF is not used to rescue a non-identifiable comparison."
                    if not analysis.multicollinearity
                    else "No fitted term exceeded the current VIF screening threshold."
                )
            ),
        },
        {
            "area": "Homogeneity of slopes",
            "status": "caution" if interaction_flags else "clear",
            "interpretation": (
                "Department-specific slopes were flagged for: " + ", ".join(interaction_flags) + "."
                if interaction_flags
                else (
                    "Interaction screening was withheld because the main comparison is not identifiable."
                    if overlap_status == "not_identifiable"
                    else "No department-by-covariate interaction crossed the screening threshold."
                )
            ),
        },
        {
            "area": "Influential observations",
            "status": (
                "caution" if int(analysis.influence["n_above_cooks_threshold"]) > 0 else "clear"
            ),
            "interpretation": (
                "Potentially influential observations need sensitivity review."
                if int(analysis.influence["n_above_cooks_threshold"]) > 0
                else "No observation crossed the Cook's-distance screening threshold."
            ),
        },
    ]


def _executive_summary(
    analysis: AncovaReport,
    comparison: list[dict[str, object]],
    overall_status: str,
    *,
    applicability: dict[str, object],
) -> str:
    provenance = ", ".join(analysis.provenance)
    adjusted_rows = [
        row for row in comparison if row["adjusted_mean_resolution_hours"] is not None
    ]

    if not adjusted_rows:
        return (
            f"Using {analysis.n_complete_cases} complete cases from {provenance} data, raw "
            "department summaries are available but the adjusted department comparison is "
            "withheld because department and issue-category case mix are not separately "
            "identifiable in the observed routing design. Reporting a department ranking here "
            "would be misleading. The evaluation applicability gate returns "
            f"{applicability['disposition']} and the available statistics are descriptive and not causal."
        )

    ranked = sorted(
        adjusted_rows,
        key=lambda row: float(row["adjusted_mean_resolution_hours"]),
    )
    fastest = ranked[0]
    slowest = ranked[-1]
    warning_text = (
        f"The statistical screening status is {overall_status}; {len(analysis.warnings)} warning(s) "
        "should be reviewed before operational interpretation."
        if analysis.warnings
        else "No current screening rule triggered a warning, although assumptions are not proven."
    )
    return (
        f"Using {analysis.n_complete_cases} complete cases from {provenance} data, the lowest "
        f"case-mix-standardised mean resolution-time estimate is {fastest['department']} "
        f"({float(fastest['adjusted_mean_resolution_hours']):.2f} h) and the highest is "
        f"{slowest['department']} ({float(slowest['adjusted_mean_resolution_hours']):.2f} h). "
        f"The evaluation applicability gate returns {applicability['disposition']} with method "
        f"family {applicability['method_family']}. {warning_text} These adjusted estimates are "
        "intended for case-mix-aware investigation, not causal ranking or automatic staff-performance "
        "decisions."
    )


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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate the ANCOVA Ops management-facing outcome report."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--csv", type=Path, help="Approved development CSV dataset to analyse.")
    source.add_argument(
        "--synthetic-n",
        type=int,
        default=500,
        help="Number of synthetic rows when --csv is not supplied (default: 500).",
    )
    parser.add_argument("--seed", type=int, default=2026, help="Synthetic-data random seed.")
    parser.add_argument("--alpha", type=float, default=0.05, help="Inference alpha level.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Markdown output path (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument("--json-output", type=Path, help="Optional structured JSON output path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if not 0 < args.alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    data = load_input(args)
    write_management_report(
        data,
        args.output,
        json_output=args.json_output,
        alpha=args.alpha,
    )
    print(f"Wrote management report to {args.output}")
    if args.json_output is not None:
        print(f"Wrote structured summary to {args.json_output}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
