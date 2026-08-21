import pytest

from reasoned_ops.intelligence import BaselineRequestIntelligence


def test_air_conditioning_request_is_classified_before_generic_leak() -> None:
    intelligence = BaselineRequestIntelligence()

    result = intelligence.analyze("The air conditioner is leaking again.")

    assert result.issue_category == "air_conditioning"
    assert result.frustration > 3.0


def test_vulnerability_and_history_raise_context_scores() -> None:
    intelligence = BaselineRequestIntelligence()

    baseline = intelligence.analyze("There is a water leak in the kitchen.")
    contextual = intelligence.analyze(
        "There is a water leak in the kitchen and an elderly resident may slip.",
        previous_related_cases=2,
        vulnerability_flag=True,
    )

    assert contextual.urgency > baseline.urgency
    assert contextual.complexity > baseline.complexity
    assert contextual.frustration > baseline.frustration


def test_unknown_request_falls_back_to_general_request() -> None:
    intelligence = BaselineRequestIntelligence()

    result = intelligence.analyze("I need help with something in the building.")

    assert result.issue_category == "general_request"


@pytest.mark.parametrize(
    "message",
    [
        "The kitchen is on fire.",
        "There is smoke in the corridor.",
        "I can smell a gas leak near the lift.",
    ],
)
def test_emergency_language_requires_emergency_category_and_critical_urgency(message: str) -> None:
    intelligence = BaselineRequestIntelligence()

    result = intelligence.analyze(message)

    assert result.issue_category == "emergency"
    assert result.urgency == 10.0
    assert any("immediate human triage" in reason for reason in result.reasons)


@pytest.mark.parametrize(
    "message",
    [
        "I need the current status of my request.",
        "I have feedback on the lobby renovation.",
    ],
)
def test_substrings_inside_unrelated_words_do_not_trigger_categories(message: str) -> None:
    intelligence = BaselineRequestIntelligence()

    result = intelligence.analyze(message)

    assert result.issue_category == "general_request"
