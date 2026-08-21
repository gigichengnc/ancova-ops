import json

import pandas as pd
import pytest

from reasoned_ops.adaptive import (
    POLICY_VERSION,
    PolicyRegistry,
    build_offline_comparison,
    chronological_split,
    train_outcome_aware_policy,
)
from reasoned_ops.routing import ROUTER_VERSION
from reasoned_ops.synthetic import generate_logged_routing_history


def test_chronological_split_has_no_future_leakage() -> None:
    data = generate_logged_routing_history(n=600, seed=11)
    split = chronological_split(data, validation_fraction=0.25)

    assert len(split.training) == 450
    assert len(split.validation) == 150
    assert split.training["event_time"].max() < split.validation["event_time"].min()
    assert set(split.training["case_id"]).isdisjoint(set(split.validation["case_id"]))


def test_outcome_aware_policy_learns_supported_noise_routing_choice() -> None:
    data = generate_logged_routing_history(n=4000, seed=17)
    split = chronological_split(data)
    policy = train_outcome_aware_policy(split.training, min_samples=25)

    decision = policy.predict("noise_complaint")

    assert decision.department == "community_management"
    assert policy.trained_until < split.cutoff_time


def test_offline_comparison_is_support_aware_and_non_deployment_claim() -> None:
    data = generate_logged_routing_history(n=4000, seed=23)
    comparison, candidate = build_offline_comparison(
        data,
        min_samples=25,
        minimum_effective_sample_size=20,
    )

    assert candidate.version == POLICY_VERSION
    assert comparison.baseline.support_adequate is True
    assert comparison.candidate.support_adequate is True
    assert comparison.baseline.unsupported_count == 0
    assert comparison.candidate.unsupported_count == 0
    assert comparison.candidate_minus_baseline_ips_hours is not None
    assert comparison.candidate_minus_baseline_ips_hours < 0
    assert comparison.offline_signal == "candidate_lower_estimated_resolution_time"
    assert comparison.offline_gate_passed is True
    assert comparison.deployment_eligible is False
    assert "synthetic" in comparison.limitations[0].lower()


def test_logged_history_rejects_non_synthetic_provenance() -> None:
    data = generate_logged_routing_history(n=200, seed=3)
    data["data_provenance"] = "pilot"

    with pytest.raises(ValueError, match="synthetic_logged_policy"):
        chronological_split(data)


def test_policy_registry_requires_approval_before_activation_and_preserves_rollback(
    tmp_path,
) -> None:
    registry_path = tmp_path / "registry.json"
    registry = PolicyRegistry(registry_path)
    registry.register_candidate(
        POLICY_VERSION,
        offline_gate_passed=True,
        evaluation_summary={"offline_signal": "candidate_lower_estimated_resolution_time"},
    )

    with pytest.raises(ValueError, match="explicit human approval"):
        registry.activate(POLICY_VERSION, actor="ops-lead")

    approved = registry.approve(
        POLICY_VERSION,
        reviewer="reviewer-001",
        rationale="Synthetic offline checks reviewed; approve for controlled staging only.",
    )
    assert approved["policies"][POLICY_VERSION]["approved"] is True

    active = registry.activate(POLICY_VERSION, actor="ops-lead")
    assert active["active_policy"] == POLICY_VERSION
    assert active["policies"][ROUTER_VERSION]["status"] == "inactive"

    rolled_back = registry.rollback(
        ROUTER_VERSION,
        actor="ops-lead",
        rationale="Rollback drill.",
    )
    assert rolled_back["active_policy"] == ROUTER_VERSION
    assert rolled_back["policies"][POLICY_VERSION]["status"] == "inactive"
    events = rolled_back["events"]
    assert [event["event"] for event in events] == [
        "candidate_registered",
        "policy_approved",
        "policy_activated",
        "policy_rollback",
    ]

    persisted = json.loads(registry_path.read_text(encoding="utf-8"))
    assert persisted["events"] == events


def test_activation_rejects_candidate_that_failed_offline_gate(tmp_path) -> None:
    registry = PolicyRegistry(tmp_path / "registry.json")
    registry.register_candidate(
        "candidate-without-offline-support-v1",
        offline_gate_passed=False,
        evaluation_summary={"offline_signal": "not_estimable"},
    )
    registry.approve(
        "candidate-without-offline-support-v1",
        reviewer="reviewer-001",
        rationale="Approval records review but does not waive the offline gate.",
    )

    with pytest.raises(ValueError, match="offline evaluation gate"):
        registry.activate("candidate-without-offline-support-v1", actor="ops-lead")


def test_synthetic_propensity_rows_sum_to_one() -> None:
    data = generate_logged_routing_history(n=250, seed=5)
    columns = [column for column in data.columns if column.startswith("propensity_")]
    probabilities = data[columns].sum(axis=1)

    assert isinstance(probabilities, pd.Series)
    assert probabilities.min() == pytest.approx(1.0)
    assert probabilities.max() == pytest.approx(1.0)
