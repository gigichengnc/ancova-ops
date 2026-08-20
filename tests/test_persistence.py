from __future__ import annotations

import sqlite3

import pytest

from ancova_ops.models import RoutingDecision, ServiceCase
from ancova_ops.persistence import (
    SCHEMA_VERSION,
    CaseConflictError,
    CaseOutcome,
    ReviewConflictError,
    SQLiteCaseStore,
)


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
    assert stored.latest_review is None


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


def test_human_confirmation_is_recorded_without_changing_machine_decision(tmp_path) -> None:
    store = SQLiteCaseStore(tmp_path / "confirm.sqlite3")
    case = _case()
    machine = _decision()
    decision_id = store.save_routed_case(
        case,
        machine,
        intelligence_version="intelligence-v1",
        router_version="router-v1",
    )

    review = store.save_routing_review(
        case.case_id,
        decision_id,
        machine,
        actor_id="staff-001",
        reason="Reviewed the request and confirmed the recommendation.",
        created_at="2026-08-20T09:00:00+00:00",
    )

    assert review.action == "confirmed"
    stored = store.get_case(case.case_id)
    assert stored is not None
    assert stored.latest_decision is not None
    assert stored.latest_decision.decision == machine
    assert stored.latest_review is not None
    assert stored.latest_review.action == "confirmed"
    assert stored.latest_review.actor_id == "staff-001"


def test_human_override_preserves_original_recommendation_and_stores_final_decision(
    tmp_path,
) -> None:
    store = SQLiteCaseStore(tmp_path / "override.sqlite3")
    case = _case()
    machine = _decision()
    decision_id = store.save_routed_case(
        case,
        machine,
        intelligence_version="intelligence-v1",
        router_version="router-v1",
    )
    final = RoutingDecision(
        department="security",
        priority="critical",
        requires_human_review=True,
        secondary_notify=None,
        reasons=(),
    )

    review = store.save_routing_review(
        case.case_id,
        decision_id,
        final,
        actor_id="staff-002",
        reason="The reported threat requires Security ownership rather than Maintenance.",
    )

    assert review.action == "overridden"
    stored = store.get_case(case.case_id)
    assert stored is not None
    assert stored.latest_decision is not None
    assert stored.latest_decision.decision.department == "maintenance"
    assert stored.latest_review is not None
    assert stored.latest_review.final_decision.department == "security"
    assert stored.latest_review.reason.startswith("The reported threat")

    history = store.list_routing_reviews(case.case_id)
    assert len(history) == 1
    assert history[0].decision_id == decision_id
    assert history[0].action == "overridden"


def test_review_of_stale_machine_decision_is_rejected(tmp_path) -> None:
    store = SQLiteCaseStore(tmp_path / "stale-review.sqlite3")
    case = _case()
    first_id = store.save_routed_case(
        case,
        _decision(),
        intelligence_version="intelligence-v1",
        router_version="router-v1",
    )
    store.save_routed_case(
        case,
        RoutingDecision(
            department="maintenance",
            priority="critical",
            requires_human_review=True,
            secondary_notify="community_management",
            reasons=("updated policy",),
        ),
        intelligence_version="intelligence-v1",
        router_version="router-v2",
    )

    with pytest.raises(ReviewConflictError):
        store.save_routing_review(
            case.case_id,
            first_id,
            _decision(),
            actor_id="staff-003",
            reason="This review is based on an outdated recommendation.",
        )


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


def test_schema_version_one_database_migrates_to_review_schema(tmp_path) -> None:
    database = tmp_path / "migration.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE schema_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        connection.execute(
            "INSERT INTO schema_metadata (key, value) VALUES ('schema_version', '1')"
        )

    SQLiteCaseStore(database)

    with sqlite3.connect(database) as connection:
        version = connection.execute(
            "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
        ).fetchone()
        table = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'routing_reviews'"
        ).fetchone()

    assert version == (str(SCHEMA_VERSION),)
    assert table == ("routing_reviews",)
