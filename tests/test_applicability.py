from ancova_ops.analytics import build_ancova_report
from ancova_ops.applicability import (
    EvaluationQuestion,
    assess_evaluation_question,
    assess_from_ancova_report,
    main,
)
from ancova_ops.synthetic import generate_outcomes
from ancova_ops.validity import generate_measured_confounding_scenario


def test_supported_continuous_department_comparison_uses_ancova_style() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status="supported",
        )
    )

    assert decision.disposition == "use"
    assert decision.method_family == "regression_ancova_style"


def test_weak_overlap_returns_caution() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status="weak_overlap",
        )
    )

    assert decision.disposition == "caution"


def test_interaction_flag_returns_caution_and_interaction_aware_method() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status="supported",
            interaction_flags=("urgency",),
        )
    )

    assert decision.disposition == "caution"
    assert decision.method_family == "interaction_aware_regression"


def test_no_overlap_rejects_department_comparison() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status="not_identifiable",
        )
    )

    assert decision.disposition == "reject"
    assert decision.method_family == "no_adjusted_department_comparison"


def test_binary_outcome_recommends_logistic_type_analysis() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="binary",
            comparison="department_outcome",
            overlap_status="supported",
        )
    )

    assert decision.disposition == "recommend_alternative"
    assert decision.method_family == "logistic_type_model"


def test_censored_time_recommends_survival_analysis() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status="supported",
            censored=True,
        )
    )

    assert decision.disposition == "recommend_alternative"
    assert decision.method_family == "survival_time_to_event_model"


def test_clustered_observations_recommend_hierarchical_analysis() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status="supported",
            repeated_or_clustered=True,
        )
    )

    assert decision.disposition == "recommend_alternative"
    assert decision.method_family == "clustered_or_hierarchical_model"


def test_routing_policy_question_uses_offline_policy_evaluation() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="routing_policy",
        )
    )

    assert decision.disposition == "recommend_alternative"
    assert decision.method_family == "offline_policy_evaluation"


def test_causal_intent_is_not_cleared_by_observational_adjustment() -> None:
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status="supported",
            causal_intent=True,
        )
    )

    assert decision.disposition == "recommend_alternative"
    assert decision.method_family == "causal_design_and_identification"


def test_gate_can_be_derived_from_supported_ancova_report() -> None:
    report = build_ancova_report(generate_outcomes(n=500, seed=81))
    decision = assess_from_ancova_report(report)

    assert decision.disposition in {"use", "caution"}
    assert decision.method_family in {"regression_ancova_style", "interaction_aware_regression"}


def test_gate_rejects_from_no_overlap_ancova_report() -> None:
    data = generate_measured_confounding_scenario(
        n=500,
        seed=83,
        deterministic_routing=True,
    )
    report = build_ancova_report(data)
    decision = assess_from_ancova_report(report)

    assert decision.disposition == "reject"


def test_applicability_cli_emits_json(capsys) -> None:
    exit_code = main(
        [
            "--outcome-type",
            "continuous",
            "--comparison",
            "department_outcome",
            "--overlap-status",
            "supported",
            "--json",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"disposition": "use"' in captured.out
