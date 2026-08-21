from reasoned_ops.analytics import build_ancova_report
from reasoned_ops.management_report import build_management_report, render_markdown
from reasoned_ops.validity import (
    generate_measured_confounding_scenario,
    generate_unmeasured_confounding_scenario,
    main,
    run_validity_benchmark,
)


def test_validity_benchmark_passes_known_synthetic_scenarios() -> None:
    report = run_validity_benchmark(n=1200, seed=23)

    assert report["overall_pass"] is True
    assert report["scenarios"]["known_effect_recovery"]["pass"] is True
    assert report["scenarios"]["measured_confounding"]["pass"] is True
    assert report["scenarios"]["no_overlap"]["pass"] is True
    assert report["scenarios"]["slope_interaction"]["pass"] is True
    assert report["scenarios"]["unmeasured_confounding_blind_spot"]["pass"] is True


def test_case_mix_adjustment_beats_deliberately_naive_model() -> None:
    report = run_validity_benchmark(n=1200, seed=23)
    scenario = report["scenarios"]["measured_confounding"]

    assert scenario["adjusted_absolute_error_hours"] < 0.75
    assert scenario["adjusted_absolute_error_hours"] < scenario["naive_absolute_error_hours"]


def test_unmeasured_confounding_scenario_exposes_false_negative_gate() -> None:
    report = run_validity_benchmark(n=1200, seed=23)
    scenario = report["scenarios"]["unmeasured_confounding_blind_spot"]

    assert scenario["scenario_type"] == "known_limitation"
    assert scenario["hidden_column_removed_before_evaluation"] is True
    assert scenario["identifiability_status"] == "supported"
    assert scenario["gate_disposition"] == "use"
    assert scenario["sign_reversal"] is True
    assert scenario["adjusted_absolute_error_hours"] >= 3.0
    assert "unmeasured confounding" in scenario["interpretation_boundary"].lower()


def test_hidden_confounder_is_explicit_in_generator_but_not_required_by_evaluator() -> None:
    data = generate_unmeasured_confounding_scenario(n=400, seed=35)

    assert "latent_case_burden" in data.columns
    observed = data.drop(columns=["latent_case_burden"])
    report = build_ancova_report(observed)

    assert report.identifiability["status"] == "supported"
    assert report.adjusted_estimates


def test_no_overlap_withholds_department_comparison() -> None:
    data = generate_measured_confounding_scenario(
        n=500,
        seed=51,
        deterministic_routing=True,
    )
    report = build_ancova_report(data)
    payload = report.to_dict()

    assert report.identifiability["status"] == "not_identifiable"
    assert report.adjusted_estimates == []
    assert payload["anova"] == []
    assert any("not separately identifiable" in warning for warning in report.warnings)


def test_management_report_blocks_ranking_when_design_is_not_identifiable() -> None:
    data = generate_measured_confounding_scenario(
        n=500,
        seed=67,
        deterministic_routing=True,
    )
    report = build_management_report(data)
    markdown = render_markdown(report)

    assert report.overall_screening_status == "blocked"
    assert all(row["adjusted_mean_resolution_hours"] is None for row in report.department_comparison)
    assert "withheld" in markdown.lower()
    assert "adjusted department comparison is withheld" in report.executive_summary.lower()
    assert "reporting a department ranking here would be misleading" in report.executive_summary.lower()


def test_validity_cli_returns_success(capsys) -> None:
    exit_code = main(["--n", "1200", "--seed", "23", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"overall_pass": true' in captured.out
    assert '"unmeasured_confounding_blind_spot"' in captured.out
