from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_POLICY_PATH = Path("config/data-governance.json")


class GovernancePolicyError(ValueError):
    """Raised when the project governance policy is incomplete or violated."""


@dataclass(slots=True, frozen=True)
class FieldPolicy:
    name: str
    sensitivity: str
    operational_purpose: str
    analytics_use: str
    retention_expectation: str
    requires_explicit_review: bool


@dataclass(slots=True, frozen=True)
class LongitudinalFeaturePolicy:
    name: str
    status: str
    operational_purpose: str
    retention_rationale: str
    pilot_requirement: str


@dataclass(slots=True, frozen=True)
class GovernancePolicy:
    policy_version: str
    mode: str
    deployment_status: str
    defaults: dict[str, bool]
    approved_development_provenance: tuple[str, ...]
    fields: tuple[FieldPolicy, ...]
    longitudinal_features: tuple[LongitudinalFeaturePolicy, ...]
    prohibited_by_default: tuple[str, ...]

    @property
    def fields_by_name(self) -> dict[str, FieldPolicy]:
        return {field.name: field for field in self.fields}


REQUIRED_DEFAULT_GUARDRAILS = {
    "real_private_records_allowed": False,
    "direct_identifiers_allowed": False,
    "raw_request_text_for_training_allowed": False,
    "human_review_as_ground_truth_allowed": False,
    "longitudinal_personalisation_allowed": False,
    "analytics_export_requires_pseudonymisation": True,
}

CURRENT_OPERATIONAL_FIELDS = {
    "case_id",
    "message",
    "issue_category",
    "urgency",
    "frustration",
    "complexity",
    "previous_related_cases",
    "vulnerability_flag",
    "department",
    "priority",
    "routing_reasons",
    "actor_id",
    "response_time_minutes",
    "resolution_time_minutes",
    "reassigned",
    "escalated",
    "satisfaction",
}

RESTRICTED_SENSITIVITY_PREFIXES = (
    "restricted_",
    "staff_pseudonymous_identifier",
    "longitudinal_derived_signal",
)

ALLOWED_ANALYTICS_POLICIES = {
    "allowed_if_pseudonymous",
    "allowed_only_for_preapproved_operational_analysis",
}


def load_policy(path: str | Path = DEFAULT_POLICY_PATH) -> GovernancePolicy:
    source = Path(path)
    payload = json.loads(source.read_text(encoding="utf-8"))

    return GovernancePolicy(
        policy_version=payload["policy_version"],
        mode=payload["mode"],
        deployment_status=payload["deployment_status"],
        defaults=dict(payload["defaults"]),
        approved_development_provenance=tuple(payload["approved_development_provenance"]),
        fields=tuple(FieldPolicy(**item) for item in payload["fields"]),
        longitudinal_features=tuple(
            LongitudinalFeaturePolicy(**item) for item in payload["longitudinal_features"]
        ),
        prohibited_by_default=tuple(payload["prohibited_by_default"]),
    )


def validate_policy(policy: GovernancePolicy) -> None:
    """Validate non-negotiable development-stage governance boundaries."""

    errors: list[str] = []

    if policy.mode != "synthetic_only":
        errors.append("development governance mode must remain synthetic_only")
    if policy.deployment_status != "not_approved_for_real_private_data":
        errors.append("deployment must remain not approved for real private data")

    for key, expected in REQUIRED_DEFAULT_GUARDRAILS.items():
        actual = policy.defaults.get(key)
        if actual is not expected:
            errors.append(f"default guardrail {key!r} must be {expected!r}")

    fields_by_name = policy.fields_by_name
    missing_fields = sorted(CURRENT_OPERATIONAL_FIELDS - fields_by_name.keys())
    if missing_fields:
        errors.append(f"unregistered operational fields: {', '.join(missing_fields)}")

    duplicate_fields = _duplicates(field.name for field in policy.fields)
    if duplicate_fields:
        errors.append(f"duplicate field policies: {', '.join(sorted(duplicate_fields))}")

    for field in policy.fields:
        if not field.operational_purpose.strip():
            errors.append(f"field {field.name!r} has no operational purpose")
        if not field.retention_expectation.strip():
            errors.append(f"field {field.name!r} has no retention expectation")
        if field.sensitivity.startswith(RESTRICTED_SENSITIVITY_PREFIXES) and not (
            field.requires_explicit_review
        ):
            errors.append(f"restricted field {field.name!r} must require explicit review")

    if fields_by_name.get("message") and fields_by_name["message"].analytics_use != (
        "excluded_by_default"
    ):
        errors.append("raw request message must be excluded from analytics by default")

    if fields_by_name.get("vulnerability_flag") and fields_by_name[
        "vulnerability_flag"
    ].analytics_use != "excluded_by_default":
        errors.append("vulnerability_flag must be excluded from analytics by default")

    duplicate_longitudinal = _duplicates(feature.name for feature in policy.longitudinal_features)
    if duplicate_longitudinal:
        errors.append(
            "duplicate longitudinal feature policies: "
            + ", ".join(sorted(duplicate_longitudinal))
        )

    for feature in policy.longitudinal_features:
        if not feature.operational_purpose.strip():
            errors.append(f"longitudinal feature {feature.name!r} has no operational purpose")
        if not feature.retention_rationale.strip():
            errors.append(f"longitudinal feature {feature.name!r} has no retention rationale")
        if not feature.pilot_requirement.strip():
            errors.append(f"longitudinal feature {feature.name!r} has no pilot requirement")

    if "hand_authored_fixture" not in policy.approved_development_provenance:
        errors.append("hand-authored evaluation fixtures must remain approved for development")
    if "synthetic" not in policy.approved_development_provenance:
        errors.append("synthetic data must remain approved for development")

    if errors:
        raise GovernancePolicyError("; ".join(errors))


def assert_development_provenance(provenance: str, policy: GovernancePolicy) -> None:
    """Reject data sources that are outside the current synthetic-only development policy."""

    if provenance not in policy.approved_development_provenance:
        raise GovernancePolicyError(
            f"provenance {provenance!r} is not approved under {policy.policy_version}"
        )


def assert_analytics_columns(columns: Iterable[str], policy: GovernancePolicy) -> None:
    """Gate fields before they are included in a general analytics/model dataset.

    This intentionally blocks fields marked `excluded_by_default`. Restricted fields that are
    only allowed for pre-approved operational analysis are permitted by this low-level checker,
    but the caller is responsible for documenting that approval before use.
    """

    fields_by_name = policy.fields_by_name
    blocked: list[str] = []
    unknown: list[str] = []

    for column in columns:
        field = fields_by_name.get(column)
        if field is None:
            unknown.append(column)
        elif field.analytics_use not in ALLOWED_ANALYTICS_POLICIES:
            blocked.append(column)

    problems: list[str] = []
    if unknown:
        problems.append("unregistered columns: " + ", ".join(sorted(set(unknown))))
    if blocked:
        problems.append("columns excluded from analytics by default: " + ", ".join(sorted(set(blocked))))
    if problems:
        raise GovernancePolicyError("; ".join(problems))


def _duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate ANCOVA Ops development-stage data-governance guardrails."
    )
    parser.add_argument(
        "--policy",
        default=str(DEFAULT_POLICY_PATH),
        help="Path to the machine-readable governance policy.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    policy = load_policy(args.policy)
    validate_policy(policy)

    summary = {
        "policy_version": policy.policy_version,
        "mode": policy.mode,
        "deployment_status": policy.deployment_status,
        "registered_fields": len(policy.fields),
        "registered_longitudinal_features": len(policy.longitudinal_features),
        "approved_development_provenance": list(policy.approved_development_provenance),
        "status": "valid",
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Governance policy: {summary['policy_version']}")
        print(f"Mode: {summary['mode']}")
        print(f"Deployment status: {summary['deployment_status']}")
        print(f"Registered fields: {summary['registered_fields']}")
        print(f"Longitudinal features: {summary['registered_longitudinal_features']}")
        print("Status: valid")

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
