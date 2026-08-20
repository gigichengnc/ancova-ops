from fastapi.testclient import TestClient

from ancova_ops.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_route_endpoint_returns_structured_high_context_decision(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "route.sqlite3"))
    response = client.post(
        "/v1/route",
        json={
            "case_id": "api-1",
            "message": (
                "The air conditioner is leaking again. An elderly resident may slip on "
                "the wet floor and this is urgent."
            ),
            "previous_related_cases": 2,
            "vulnerability_flag": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["case_id"] == "api-1"
    assert payload["decision_id"] >= 1
    assert payload["issue_category"] == "air_conditioning"
    assert payload["department"] == "maintenance"
    assert payload["priority"] in {"high", "critical"}
    assert payload["requires_human_review"] is True
    assert payload["secondary_notify"] == "community_management"
    assert payload["intelligence_version"] == "baseline-request-intelligence-v1"
    assert payload["router_version"] == "baseline-route-v1"
    assert payload["reasons"]


def test_route_endpoint_rejects_blank_message(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "blank.sqlite3"))
    response = client.post(
        "/v1/route",
        json={"case_id": "api-2", "message": "   "},
    )

    assert response.status_code == 422


def test_route_endpoint_rejects_negative_history_count(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "history.sqlite3"))
    response = client.post(
        "/v1/route",
        json={
            "case_id": "api-3",
            "message": "There is a water leak.",
            "previous_related_cases": -1,
        },
    )

    assert response.status_code == 422


def test_routed_case_can_be_retrieved_with_audit_history(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "retrieve.sqlite3"))
    request = {
        "case_id": "api-persist-1",
        "message": "The lift is broken and this is urgent.",
        "previous_related_cases": 1,
    }

    routed = client.post("/v1/route", json=request)
    assert routed.status_code == 200

    case_response = client.get("/v1/cases/api-persist-1")
    assert case_response.status_code == 200
    case_payload = case_response.json()
    assert case_payload["message"] == request["message"]
    assert case_payload["latest_decision"]["decision_id"] == routed.json()["decision_id"]
    assert case_payload["latest_decision"]["router_version"] == "baseline-route-v1"
    assert case_payload["latest_review"] is None
    assert case_payload["effective_routing"]["source"] == "machine_recommendation"

    audit_response = client.get("/v1/cases/api-persist-1/routing-decisions")
    assert audit_response.status_code == 200
    audit_payload = audit_response.json()
    assert len(audit_payload) == 1
    assert audit_payload[0]["reasons"] == routed.json()["reasons"]


def test_human_confirmation_keeps_effective_routing_while_recording_feedback(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "confirm-api.sqlite3"))
    routed = client.post(
        "/v1/route",
        json={"case_id": "api-confirm-1", "message": "There is a water leak."},
    )
    assert routed.status_code == 200
    machine = routed.json()

    review = client.post(
        "/v1/cases/api-confirm-1/routing-reviews",
        json={
            "decision_id": machine["decision_id"],
            "actor_id": "staff-001",
            "reason": "Reviewed and confirmed the recommendation.",
            "department": machine["department"],
            "priority": machine["priority"],
            "requires_human_review": machine["requires_human_review"],
            "secondary_notify": machine["secondary_notify"],
        },
    )
    assert review.status_code == 200
    assert review.json()["action"] == "confirmed"

    case_response = client.get("/v1/cases/api-confirm-1")
    payload = case_response.json()
    assert payload["latest_decision"]["department"] == machine["department"]
    assert payload["latest_review"]["action"] == "confirmed"
    assert payload["effective_routing"]["source"] == "human_review"
    assert payload["effective_routing"]["department"] == machine["department"]


def test_human_override_changes_effective_routing_without_overwriting_machine_decision(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "override-api.sqlite3"))
    routed = client.post(
        "/v1/route",
        json={"case_id": "api-override-1", "message": "There is a water leak."},
    )
    assert routed.status_code == 200
    machine = routed.json()
    assert machine["department"] == "maintenance"

    review = client.post(
        "/v1/cases/api-override-1/routing-reviews",
        json={
            "decision_id": machine["decision_id"],
            "actor_id": "staff-002",
            "reason": "On-site review shows an active security threat in the affected area.",
            "department": "security",
            "priority": "critical",
            "requires_human_review": True,
            "secondary_notify": None,
        },
    )
    assert review.status_code == 200
    review_payload = review.json()
    assert review_payload["action"] == "overridden"
    assert review_payload["final_decision"]["department"] == "security"

    case_response = client.get("/v1/cases/api-override-1")
    payload = case_response.json()
    assert payload["latest_decision"]["department"] == "maintenance"
    assert payload["latest_review"]["actor_id"] == "staff-002"
    assert payload["effective_routing"]["source"] == "human_review"
    assert payload["effective_routing"]["department"] == "security"

    reviews = client.get("/v1/cases/api-override-1/routing-reviews")
    assert reviews.status_code == 200
    assert len(reviews.json()) == 1
    assert reviews.json()[0]["action"] == "overridden"


def test_routing_review_rejects_blank_reason(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "blank-review.sqlite3"))
    routed = client.post(
        "/v1/route",
        json={"case_id": "api-review-blank", "message": "There is a water leak."},
    )
    machine = routed.json()

    review = client.post(
        "/v1/cases/api-review-blank/routing-reviews",
        json={
            "decision_id": machine["decision_id"],
            "actor_id": "staff-003",
            "reason": "   ",
            "department": machine["department"],
            "priority": machine["priority"],
            "requires_human_review": machine["requires_human_review"],
            "secondary_notify": machine["secondary_notify"],
        },
    )
    assert review.status_code == 422


def test_case_outcome_can_be_saved_and_retrieved(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "outcome-api.sqlite3"))
    routed = client.post(
        "/v1/route",
        json={"case_id": "api-outcome-1", "message": "There is a water leak."},
    )
    assert routed.status_code == 200

    outcome_response = client.put(
        "/v1/cases/api-outcome-1/outcome",
        json={
            "response_time_minutes": 8,
            "resolution_time_minutes": 75,
            "reassigned": False,
            "escalated": False,
            "satisfaction": 8.5,
        },
    )
    assert outcome_response.status_code == 200

    case_response = client.get("/v1/cases/api-outcome-1")
    assert case_response.status_code == 200
    outcome = case_response.json()["outcome"]
    assert outcome["resolution_time_minutes"] == 75
    assert outcome["satisfaction"] == 8.5


def test_case_id_conflict_returns_409(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "conflict-api.sqlite3"))
    first = client.post(
        "/v1/route",
        json={"case_id": "api-conflict-1", "message": "There is a water leak."},
    )
    assert first.status_code == 200

    second = client.post(
        "/v1/route",
        json={"case_id": "api-conflict-1", "message": "I have a lease renewal question."},
    )
    assert second.status_code == 409


def test_missing_case_returns_404(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ANCOVA_OPS_DB_PATH", str(tmp_path / "missing-api.sqlite3"))
    response = client.get("/v1/cases/does-not-exist")
    assert response.status_code == 404
