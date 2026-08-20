import json
from pathlib import Path

import pytest

from ancova_ops.governance import (
    GovernancePolicyError,
    assert_analytics_columns,
    assert_development_provenance,
    load_policy,
    main,
    validate_policy,
)

POLICY_PATH = Path(__file__).resolve().parents[1] / "config/data-governance.json"


def test_repository_governance_policy_is_valid() -> None:
    policy = load_policy(POLICY_PATH)
    validate_policy(policy)

    assert policy.mode == "synthetic_only"
    assert policy.deployment_status == "not_approved_for_real_private_data"
    assert policy.defaults["real_private_records_allowed"] is False
    assert policy.defaults["raw_request_text_for_training_allowed"] is False
    assert policy.defaults["human_review_as_ground_truth_allowed"] is False
    assert policy.defaults["longitudinal_personalisation_allowed"] is False


def test_sensitive_fields_are_explicitly_registered() -> None:
    policy = load_policy(POLICY_PATH)
    fields = policy.fields_by_name

    assert fields["message"].requires_explicit_review is True
    assert fields["message"].analytics_use == "excluded_by_default"
    assert fields["frustration"].requires_explicit_review is True
    assert fields["previous_related_cases"].requires_explicit_review is True
    assert fields["vulnerability_flag"].requires_explicit_review is True
    assert fields["vulnerability_flag"].analytics_use == "excluded_by_default"
    assert fields["actor_id"].requires_explicit_review is True


def test_every_longitudinal_feature_has_purpose_retention_and_pilot_boundary() -> None:
    policy = load_policy(POLICY_PATH)

    assert policy.longitudinal_features
    for feature in policy.longitudinal_features:
        assert feature.operational_purpose.strip()
        assert feature.retention_rationale.strip()
        assert feature.pilot_requirement.strip()

    statuses = {feature.name: feature.status for feature in policy.longitudinal_features}
    assert statuses["previous_related_cases"] == "approved_for_synthetic_development"
    assert statuses["resident_message_history"] == "not_approved"
    assert statuses["emotion_trajectory"] == "not_approved"
    assert statuses["resident_profile_embedding"] == "not_approved"


def test_only_approved_development_provenance_is_accepted() -> None:
    policy = load_policy(POLICY_PATH)

    assert_development_provenance("synthetic", policy)
    assert_development_provenance("hand_authored_fixture", policy)

    with pytest.raises(GovernancePolicyError, match="not approved"):
        assert_development_provenance("private_pilot_export", policy)


def test_general_analytics_gate_excludes_raw_and_sensitive_context_fields() -> None:
    policy = load_policy(POLICY_PATH)

    assert_analytics_columns(
        [
            "case_id",
            "issue_category",
            "urgency",
            "complexity",
            "department",
            "resolution_time_minutes",
            "escalated",
        ],
        policy,
    )

    with pytest.raises(GovernancePolicyError, match="excluded from analytics"):
        assert_analytics_columns(["message", "department"], policy)

    with pytest.raises(GovernancePolicyError, match="excluded from analytics"):
        assert_analytics_columns(["vulnerability_flag"], policy)

    with pytest.raises(GovernancePolicyError, match="unregistered columns"):
        assert_analytics_columns(["resident_personality_score"], policy)


def test_policy_validation_fails_if_private_data_is_enabled(tmp_path) -> None:
    payload = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    payload["defaults"]["real_private_records_allowed"] = True
    path = tmp_path / "unsafe-policy.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(GovernancePolicyError, match="real_private_records_allowed"):
        validate_policy(load_policy(path))


def test_governance_cli_emits_machine_readable_status(capsys) -> None:
    exit_code = main(["--policy", str(POLICY_PATH), "--json"])
    assert exit_code == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "valid"
    assert payload["mode"] == "synthetic_only"
    assert payload["deployment_status"] == "not_approved_for_real_private_data"
    assert payload["registered_fields"] >= 17
