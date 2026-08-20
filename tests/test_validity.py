from ancova_ops.analytics import build_ancova_report
from ancova_ops.validity import (
    generate_measured_confounding_scenario,
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


def test_case_mix_adjustment_beats_deliberately_naive_model() -> None:
    report = run_validity_benchmark(n=1200, seed=23)
    scenario = report["scenarios"]["measured_confounding"]

    assert scenario["adjusted_absolute_error_hours"] < 0.75
    assert scenario["adjusted_absolute_error_hours"] < scenario["naive_absolute_error_hours"]


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


def test_validity_cli_returns_success(capsys) -> None:
    exit_code = main(["--n", "1200", "--seed", "23", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"overall_pass": true' in captured.out
