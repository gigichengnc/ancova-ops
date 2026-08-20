import ancova_ops
from ancova_ops.showcase import build_showcase_payload, render_showcase_markdown


def test_showcase_preserves_evidence_and_deployment_boundaries() -> None:
    payload = build_showcase_payload(
        seed=2026,
        outcome_rows=120,
        logged_rows=400,
        longitudinal_entities=80,
        longitudinal_days=540,
    )

    assert payload["showcase_version"] == ancova_ops.__version__
    assert payload["evidence_status"]["real_world_performance_claims_allowed"] is False
    assert payload["governance"]["mode"] == "synthetic_only"
    assert payload["governance"]["deployment_status"] == "not_approved_for_real_private_data"
    assert payload["service_request"]["routing"]["department"] == "maintenance"
    assert payload["adaptive_routing"]["deployment_eligible"] is False
    assert (
        payload["longitudinal_benchmark"]["sequence_model_status"]
        == "deferred_not_justified_by_current_benchmark"
    )

    report = render_showcase_markdown(payload)
    assert "ANCOVA Ops Portfolio Showcase" in report
    assert "Private-data pilot | NOT READY / NOT APPROVED" in report
    assert "does **not** demonstrate real service improvement" in report
