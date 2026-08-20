from __future__ import annotations

import pytest

from ancova_ops.models import RoutingDecision, ServiceCase
from ancova_ops.persistence import CaseConflictError, CaseOutcome, SQLiteCaseStore


def _case() -> ServiceCase:
    return ServiceCase(
        case_id="persist-1",
        message="The air conditioner is leaking again.",
        issue_category="air_conditioning",
        urgency=7.5,
        frustration=6.0,
        complexity=7.0,
        previous_related_cases=2,
        vulnerability_flag=True,
    )


def _decision() -> RoutingDecision:
    return RoutingDecision(
        department="maintenance",
        priority="high",
        requires_human_review=True,
        secondary_notify="community_management",
        reasons=("issue category maps to maintenance",),
    )


def test_case_and_routing_decision_round_trip(tmp_path) -> None:
    store = SQLiteCaseStore(tmp_path / "cases.sqlite3")
    case = _case()
    decision = _decision()
    combined_reasons = (
        "matched baseline issue taxonomy: air_conditioning",
        "issue category maps to maintenance",
    )

    decision_id = store.save_routed_case(
        case,
        decision,
        intelligence_version="intelligence-test-v1",
        router_version="router-test-v1",
        reasons=combined_reasons,
        created_at="2026-08-20T08:00:00+00:00",
    )

    stored = store.get_case(case.case_id)
    assert stored is not None
    assert stored.case == case
    assert stored.created_at == "2026-08-20T08:00:00+00:00"
    assert stored.latest_decision is not None
    assert stored.latest_decision.decision_id == decision_id
    assert stored.latest_decision.intelligence_version == "intelligence-test-v1"
    assert stored.latest_decision.router_version == "router-test-v1"
    assert stored.latest_decision.decision.department == "maintenance"
    assert stored.latest_decision.decision.reasons == combined_reasons


def test_reroute_appends_audit_history_without_replacing_original_case(tmp_path) -> None:
    store = SQLiteCaseStore(tmp_path / "audit.sqlite3")
    case = _case()
    first = _decision()
    second = RoutingDecision(
        department="maintenance",
        priority="critical",
        requires_human_review=True,
        secondary_notify="community_management",
        reasons=("manual policy escalation",),
    )

    store.save_routed_case(
        case,
        first,
        intelligence_version="intelligence-v1",
        router_version="router-v1",
    )
    store.save_routed_case(
        case,
        second,
        intelligence_version="intelligence-v1",
        router_version="router-v2",
    )

    history = store.list_routing_decisions(case.case_id)
    assert len(history) == 2
    assert history[0].router_version == "router-v1"
    assert history[1].router_version == "router-v2"
    assert history[1].decision.priority == "critical"


def test_reusing_case_id_with_different_original_data_is_rejected(tmp_path) -> None:
    store = SQLiteCaseStore(tmp_path / "conflict.sqlite3")
    original = _case()
    store.save_routed_case(
        original,
        _decision(),
        intelligence_version="intelligence-v1",
        router_version="router-v1",
    )

    changed = ServiceCase(
        case_id=original.case_id,
        message="A different request using the same case ID.",
        issue_category="general_request",
        urgency=3.0,
        frustration=3.0,
        complexity=5.0,
    )
    with pytest.raises(CaseConflictError):
        store.save_routed_case(
            changed,
            _decision(),
            intelligence_version="intelligence-v1",
            router_version="router-v1",
        )


def test_outcome_round_trip(tmp_path) -> None:
    store = SQLiteCaseStore(tmp_path / "outcomes.sqlite3")
    case = _case()
    store.save_routed_case(
        case,
        _decision(),
        intelligence_version="intelligence-v1",
        router_version="router-v1",
    )

    outcome = CaseOutcome(
        response_time_minutes=12.0,
        resolution_time_minutes=95.0,
        reassigned=False,
        escalated=True,
        satisfaction=7.5,
    )
    store.save_outcome(case.case_id, outcome)

    stored = store.get_case(case.case_id)
    assert stored is not None
    assert stored.outcome == outcome


def test_outcome_for_unknown_case_is_rejected(tmp_path) -> None:
    store = SQLiteCaseStore(tmp_path / "unknown.sqlite3")
    with pytest.raises(KeyError):
        store.save_outcome("missing", CaseOutcome(resolution_time_minutes=30))
