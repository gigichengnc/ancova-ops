from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from ancova_ops.analysis_report import load_input
from ancova_ops.management_report import ManagementReport
from ancova_ops.management_report import _json_safe
from ancova_ops.management_report import build_management_report as _build_management_report
from ancova_ops.management_report import render_markdown as _render_markdown

DEFAULT_OUTPUT = Path(".reasoned_ops/reports/management-report.md")

__all__ = [
    "ManagementReport",
    "build_management_report",
    "render_markdown",
    "write_management_report",
    "main",
]


def build_management_report(data: pd.DataFrame, *, alpha: float = 0.05) -> ManagementReport:
    """Build the existing guarded outcome report under the canonical ReasonedOps API."""

    return _build_management_report(data, alpha=alpha)


def render_markdown(report: ManagementReport) -> str:
    """Render the management report with the canonical ReasonedOps identity."""

    return _render_markdown(report).replace(
        "# ANCOVA Ops Management Outcome Report",
        "# ReasonedOps Management Outcome Report",
    )


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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate the ReasonedOps management-facing outcome report."
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
    print(f"Wrote ReasonedOps management report to {args.output}")
    if args.json_output is not None:
        print(f"Wrote structured summary to {args.json_output}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
