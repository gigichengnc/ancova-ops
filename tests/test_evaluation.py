import json
from pathlib import Path

import pytest

from ancova_ops.evaluation import (
    EvaluationCase,
    EvaluationPrediction,
    baseline_predict,
    compare_reports,
    evaluate_predictor,
    load_dataset,
    main,
)

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "data/evaluation/hand_authored_v1.json"


def _perfect_candidate(case: EvaluationCase) -> EvaluationPrediction:
    return EvaluationPrediction(
        department=case.expected_department,
        requires_human_review=case.expected_human_review,
        reasons=("fixture expectation explained",),
    )


def test_hand_authored_dataset_has_explicit_provenance_and_limitations() -> None:
    dataset = load_dataset(FIXTURE_PATH)
    assert dataset.provenance == "hand_authored_fixture"
    assert dataset.label_status == "design_expectation_not_ground_truth"
    assert len(dataset.cases) == 11
    assert dataset.limitations


def test_baseline_metrics_are_deterministic() -> None:
    dataset = load_dataset(FIXTURE_PATH)
    report = evaluate_predictor(
        dataset,
        baseline_predict,
        system_name="transparent-baseline-v1",
    )

    assert report.metrics.sample_count == 11
    assert report.metrics.department_correct == 10
    assert report.metrics.department_accuracy == pytest.approx(10 / 11)
    assert report.metrics.high_risk_count == 5
    assert report.metrics.high_risk_reviewed == 2
    assert report.metrics.human_review_recall == pytest.approx(2 / 5)
    assert report.metrics.explained_count == 11
    assert report.metrics.explanation_coverage == 1.0
    assert report.department_errors == ("leasing-ambiguous-001",)
    assert report.human_review_misses == (
        "maint-electrical-safety-001",
        "security-intruder-001",
        "security-smoke-001",
    )
    assert report.unexplained_cases == ()


def test_candidate_is_only_called_improved_after_same_dataset_comparison() -> None:
    dataset = load_dataset(FIXTURE_PATH)
    baseline = evaluate_predictor(
        dataset,
        baseline_predict,
        system_name="baseline",
    )
    candidate = evaluate_predictor(
        dataset,
        _perfect_candidate,
        system_name="perfect-test-candidate",
    )

    comparison = compare_reports(baseline, candidate)
    assert comparison.verdict == "improved"
    assert comparison.no_regressions is True
    assert comparison.strict_improvement is True
    assert comparison.eligible_for_improvement_claim is True
    assert comparison.department_accuracy_delta == pytest.approx(1 / 11)
    assert comparison.human_review_recall_delta == pytest.approx(3 / 5)
    assert comparison.explanation_coverage_delta == 0.0


def test_same_predictor_is_reported_as_tied() -> None:
    dataset = load_dataset(FIXTURE_PATH)
    baseline = evaluate_predictor(dataset, baseline_predict, system_name="baseline")
    candidate = evaluate_predictor(dataset, baseline_predict, system_name="candidate")

    comparison = compare_reports(baseline, candidate)
    assert comparison.verdict == "tied"
    assert comparison.eligible_for_improvement_claim is False


def test_cli_emits_machine_readable_baseline_report(capsys) -> None:
    exit_code = main(["--fixture", str(FIXTURE_PATH), "--json"])
    assert exit_code == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["dataset"]["provenance"] == "hand_authored_fixture"
    assert payload["baseline"]["metrics"]["department_correct"] == 10
    assert payload["baseline"]["metrics"]["high_risk_reviewed"] == 2


def test_cli_can_compare_candidate_with_baseline(capsys) -> None:
    exit_code = main(
        [
            "--fixture",
            str(FIXTURE_PATH),
            "--candidate",
            "ancova_ops.evaluation:baseline_predict",
            "--candidate-name",
            "same-baseline",
            "--json",
        ]
    )
    assert exit_code == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["candidate"]["system_name"] == "same-baseline"
    assert payload["comparison"]["verdict"] == "tied"
    assert payload["comparison"]["eligible_for_improvement_claim"] is False
