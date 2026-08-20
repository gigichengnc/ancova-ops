import json

import pytest

from ancova_ops.governance import GovernancePolicyError
from ancova_ops.management_report import build_management_report, main, render_markdown
from ancova_ops.synthetic import generate_outcomes


def test_management_report_separates_raw_and_adjusted_results() -> None:
    data = generate_outcomes(n=180, seed=91)
    report = build_management_report(data)

    assert report.provenance == ("synthetic",)
    assert len(report.department_comparison) == 4
    assert report.overall_screening_status in {"clear", "caution"}
    assert all("raw_mean_resolution_hours" in row for row in report.department_comparison)
    assert all("adjusted_mean_resolution_hours" in row for row in report.department_comparison)
    assert "not causal" in report.executive_summary.lower()


def test_markdown_keeps_management_and_causal_boundaries_visible() -> None:
    report = build_management_report(generate_outcomes(n=160, seed=22))
    markdown = render_markdown(report)

    assert "# ANCOVA Ops Management Outcome Report" in markdown
    assert "## Executive summary" in markdown
    assert "## Department comparison" in markdown
    assert "Raw mean (h)" in markdown
    assert "Adjusted mean (h)" in markdown
    assert "## Statistical screening dashboard" in markdown
    assert "not causal effects" in markdown
    assert "automatic basis for staff performance decisions" in markdown


def test_management_cli_writes_markdown_and_json(tmp_path, capsys) -> None:
    markdown_path = tmp_path / "management.md"
    json_path = tmp_path / "management.json"

    exit_code = main(
        [
            "--synthetic-n",
            "140",
            "--seed",
            "44",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert markdown_path.exists()
    assert json_path.exists()
    assert "Wrote management report" in captured.out

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["provenance"] == ["synthetic"]
    assert payload["sample"]["n_rows"] == 140
    assert len(payload["department_comparison"]) == 4


def test_management_report_surfaces_missingness_as_caution() -> None:
    data = generate_outcomes(n=120, seed=14)
    data.loc[:4, "complexity"] = None
    report = build_management_report(data)

    assert report.overall_screening_status == "caution"
    missingness = next(
        row for row in report.screening_status if row["area"] == "Required-field missingness"
    )
    assert missingness["status"] == "caution"
    assert any("missingness" in warning.lower() for warning in report.warnings)


def test_management_cli_rejects_unapproved_csv_provenance(tmp_path) -> None:
    data = generate_outcomes(n=80, seed=31)
    data["data_provenance"] = "production_private"
    csv_path = tmp_path / "unapproved.csv"
    data.to_csv(csv_path, index=False)

    with pytest.raises(GovernancePolicyError):
        main(["--csv", str(csv_path), "--output", str(tmp_path / "report.md")])
