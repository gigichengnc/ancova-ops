from fastapi.testclient import TestClient

from ancova_ops.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_route_endpoint_returns_structured_high_context_decision() -> None:
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
    assert payload["issue_category"] == "air_conditioning"
    assert payload["department"] == "maintenance"
    assert payload["priority"] in {"high", "critical"}
    assert payload["requires_human_review"] is True
    assert payload["secondary_notify"] == "community_management"
    assert payload["reasons"]


def test_route_endpoint_rejects_blank_message() -> None:
    response = client.post(
        "/v1/route",
        json={"case_id": "api-2", "message": "   "},
    )

    assert response.status_code == 422


def test_route_endpoint_rejects_negative_history_count() -> None:
    response = client.post(
        "/v1/route",
        json={
            "case_id": "api-3",
            "message": "There is a water leak.",
            "previous_related_cases": -1,
        },
    )

    assert response.status_code == 422
