import pytest

from reasoned_ops.intelligence import BaselineRequestIntelligence
from reasoned_ops.models import ServiceCase
from reasoned_ops.routing import baseline_route


def test_repeated_high_context_maintenance_case_is_escalated() -> None:
    case = ServiceCase(
        case_id="case-1",
        message="Air conditioner leak again",
        issue_category="air_conditioning",
        urgency=8.5,
        frustration=9.0,
        complexity=7.0,
        previous_related_cases=3,
        vulnerability_flag=True,
    )

    decision = baseline_route(case)

    assert decision.department == "maintenance"
    assert decision.priority in {"high", "critical"}
    assert decision.requires_human_review is True
    assert decision.secondary_notify == "community_management"
    assert any("related cases" in reason for reason in decision.reasons)


def test_low_context_payment_question_stays_normal_priority() -> None:
    case = ServiceCase(
        case_id="case-2",
        message="Can you explain this month's management fee?",
        issue_category="payment_question",
        urgency=2.0,
        frustration=2.0,
        complexity=2.0,
    )

    decision = baseline_route(case)

    assert decision.department == "accounts"
    assert decision.priority == "normal"
    assert decision.requires_human_review is False


@pytest.mark.parametrize(
    "message",
    [
        "The kitchen is on fire.",
        "There is smoke in the corridor.",
        "There is a gas leak near the lift.",
    ],
)
def test_emergency_requests_use_dedicated_human_triage_path(message: str) -> None:
    intelligence = BaselineRequestIntelligence()
    features = intelligence.analyze(message)
    case = ServiceCase(
        case_id="emergency-case",
        message=message,
        issue_category=features.issue_category,
        urgency=features.urgency,
        frustration=features.frustration,
        complexity=features.complexity,
    )

    decision = baseline_route(case)

    assert decision.department == "emergency_response"
    assert decision.priority == "critical"
    assert decision.requires_human_review is True
    assert decision.secondary_notify == "community_management"
    assert any("immediate human triage" in reason for reason in decision.reasons)


@pytest.mark.parametrize(
    "message",
    [
        "I need the current status of my request.",
        "I have feedback on the lobby renovation.",
    ],
)
def test_unrelated_substrings_do_not_trigger_specialist_fallback_routes(message: str) -> None:
    case = ServiceCase(case_id="negative-control", message=message)

    decision = baseline_route(case)

    assert decision.department == "community_management"
