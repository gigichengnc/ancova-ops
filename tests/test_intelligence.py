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
