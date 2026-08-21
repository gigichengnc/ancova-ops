from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .routing import CATEGORY_TO_DEPARTMENT, ROUTER_VERSION
from .synthetic import LOGGED_ROUTING_DEPARTMENTS, generate_logged_routing_history

POLICY_VERSION = "outcome-aware-category-mean-v1"
DEFAULT_REGISTRY_PATH = Path(".reasoned_ops/policy-registry.json")
PROPENSITY_PREFIX = "propensity_"
REQUIRED_LOGGED_COLUMNS = (
    "case_id",
    "event_time",
    "issue_category",
    "logged_department",
    "resolution_hours",
    "logged_propensity",
    "data_provenance",
)


@dataclass(slots=True, frozen=True)
class TimeSplit:
    training: pd.DataFrame
    validation: pd.DataFrame
    cutoff_time: str


@dataclass(slots=True, frozen=True)
class PolicyDecision:
    department: str
    policy_version: str
    reasons: tuple[str, ...]


@dataclass(slots=True, frozen=True)
class LearnedCategoryChoice:
    issue_category: str
    department: str
    sample_count: int
    observed_mean_resolution_hours: float


@dataclass(slots=True, frozen=True)
class OutcomeAwarePolicy:
    version: str
    trained_until: str
    min_samples: int
    choices: tuple[LearnedCategoryChoice, ...]

    def predict(self, issue_category: str) -> PolicyDecision:
        lookup = {choice.issue_category: choice for choice in self.choices}
        if issue_category in lookup:
            choice = lookup[issue_category]
            return PolicyDecision(
                department=choice.department,
                policy_version=self.version,
                reasons=(
                    (
                        "training-window observed mean resolution time was lowest among "
                        "supported departments for this issue category"
                    ),
                    f"training support for selected category-action pair: {choice.sample_count}",
                ),
            )
        return PolicyDecision(
            department=baseline_department(issue_category),
            policy_version=self.version,
            reasons=("insufficient supported training evidence; baseline fallback used",),
        )


@dataclass(slots=True, frozen=True)
class OfflinePolicyReport:
    policy_version: str
    validation_count: int
    action_match_count: int
    action_match_rate: float
    unsupported_count: int
    ips_mean_resolution_hours: float | None
    self_normalized_ips_mean_resolution_hours: float | None
    effective_sample_size: float
    observed_matched_mean_resolution_hours: float | None
    support_adequate: bool
    interpretation_note: str


@dataclass(slots=True, frozen=True)
class OfflineComparison:
    training_count: int
    validation_count: int
    cutoff_time: str
    baseline: OfflinePolicyReport
    candidate: OfflinePolicyReport
    candidate_minus_baseline_ips_hours: float | None
    offline_signal: str
    offline_gate_passed: bool
    deployment_eligible: bool
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def baseline_department(issue_category: str) -> str:
    return CATEGORY_TO_DEPARTMENT.get(issue_category, "community_management")


def baseline_policy_decision(issue_category: str) -> PolicyDecision:
    return PolicyDecision(
        department=baseline_department(issue_category),
        policy_version=ROUTER_VERSION,
        reasons=("current transparent category-to-department baseline",),
    )


def validate_logged_history(data: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(set(REQUIRED_LOGGED_COLUMNS).difference(data.columns))
    if missing:
        raise ValueError(f"missing required logged-routing columns: {', '.join(missing)}")
    if len(data) < 100:
        raise ValueError("logged-routing history requires at least 100 rows")

    provenance = {str(value) for value in data["data_provenance"].dropna().unique()}
    if provenance != {"synthetic_logged_policy"}:
        raise ValueError(
            "Phase 3 development currently accepts only synthetic_logged_policy provenance"
        )

    frame = data.copy()
    frame["event_time"] = pd.to_datetime(frame["event_time"], utc=True, errors="raise")
    if frame["event_time"].isna().any():
        raise ValueError("event_time cannot contain missing values")
    if frame["case_id"].astype(str).duplicated().any():
        raise ValueError("case_id must be unique in logged-routing history")
    if (frame["resolution_hours"] <= 0).any():
        raise ValueError("resolution_hours must be positive")

    propensity_columns = [
        f"{PROPENSITY_PREFIX}{department}" for department in LOGGED_ROUTING_DEPARTMENTS
    ]
    missing_propensity = [column for column in propensity_columns if column not in frame.columns]
    if missing_propensity:
        raise ValueError("missing action-propensity columns: " + ", ".join(missing_propensity))

    propensity_matrix = frame[propensity_columns].astype(float)
    if ((propensity_matrix < 0) | (propensity_matrix > 1)).any().any():
        raise ValueError("action propensities must be between 0 and 1")
    if not np.allclose(propensity_matrix.sum(axis=1).to_numpy(), 1.0, atol=1e-9):
        raise ValueError("action propensities must sum to 1 for every row")

    logged_propensity = []
    allowed_departments = {str(item) for item in LOGGED_ROUTING_DEPARTMENTS}
    for row in frame.itertuples(index=False):
        department = str(row.logged_department)
        if department not in allowed_departments:
            raise ValueError(f"unknown logged department: {department}")
        probability = float(getattr(row, f"{PROPENSITY_PREFIX}{department}"))
        if probability <= 0:
            raise ValueError("logged action must have positive logging-policy propensity")
        logged_propensity.append(probability)
    if not np.allclose(frame["logged_propensity"].astype(float), logged_propensity, atol=1e-9):
        raise ValueError("logged_propensity must match the propensity of the logged department")
    return frame


def chronological_split(
    data: pd.DataFrame,
    *,
    validation_fraction: float = 0.30,
) -> TimeSplit:
    if not 0.10 <= validation_fraction <= 0.50:
        raise ValueError("validation_fraction must be between 0.10 and 0.50")
    frame = validate_logged_history(data).sort_values("event_time").reset_index(drop=True)
    split_index = int(len(frame) * (1.0 - validation_fraction))
    cutoff = frame.loc[split_index, "event_time"]
    training = frame.loc[frame["event_time"] < cutoff].copy()
    validation = frame.loc[frame["event_time"] >= cutoff].copy()
    if len(training) < 50 or len(validation) < 20:
        raise ValueError("time split leaves too few rows for training or validation")
    if training["event_time"].max() >= validation["event_time"].min():
        raise ValueError("time split must keep all validation events strictly after training")
    return TimeSplit(
        training=training,
        validation=validation,
        cutoff_time=cutoff.isoformat(),
    )


def train_outcome_aware_policy(
    training: pd.DataFrame,
    *,
    version: str = POLICY_VERSION,
    min_samples: int = 15,
) -> OutcomeAwarePolicy:
    frame = validate_logged_history(training)
    if min_samples < 5:
        raise ValueError("min_samples must be at least 5")

    choices: list[LearnedCategoryChoice] = []
    grouped = (
        frame.groupby(["issue_category", "logged_department"])["resolution_hours"]
        .agg(["count", "mean"])
        .reset_index()
    )
    for issue_category, category_rows in grouped.groupby("issue_category"):
        supported = category_rows.loc[category_rows["count"] >= min_samples].copy()
        if supported.empty:
            continue
        winner = supported.sort_values(["mean", "logged_department"]).iloc[0]
        choices.append(
            LearnedCategoryChoice(
                issue_category=str(issue_category),
                department=str(winner["logged_department"]),
                sample_count=int(winner["count"]),
                observed_mean_resolution_hours=float(winner["mean"]),
            )
        )

    return OutcomeAwarePolicy(
        version=version,
        trained_until=frame["event_time"].max().isoformat(),
        min_samples=min_samples,
        choices=tuple(sorted(choices, key=lambda choice: choice.issue_category)),
    )


def evaluate_policy(
    validation: pd.DataFrame,
    *,
    policy_version: str,
    predictor: Any,
    minimum_effective_sample_size: float = 20.0,
) -> OfflinePolicyReport:
    frame = validate_logged_history(validation)
    weights: list[float] = []
    weighted_outcomes: list[float] = []
    matched_outcomes: list[float] = []
    unsupported_count = 0

    for row in frame.itertuples(index=False):
        decision = predictor(str(row.issue_category))
        if not isinstance(decision, PolicyDecision):
            raise TypeError("policy predictor must return PolicyDecision")
        target = decision.department
        propensity_column = f"{PROPENSITY_PREFIX}{target}"
        if propensity_column not in frame.columns:
            unsupported_count += 1
            weights.append(0.0)
            weighted_outcomes.append(0.0)
            continue
        target_propensity = float(getattr(row, propensity_column))
        if target_propensity <= 0:
            unsupported_count += 1
            weights.append(0.0)
            weighted_outcomes.append(0.0)
            continue

        matched = str(row.logged_department) == target
        weight = (1.0 / target_propensity) if matched else 0.0
        weights.append(weight)
        weighted_outcomes.append(weight * float(row.resolution_hours))
        if matched:
            matched_outcomes.append(float(row.resolution_hours))

    match_count = len(matched_outcomes)
    weight_array = np.asarray(weights, dtype=float)
    weighted_array = np.asarray(weighted_outcomes, dtype=float)
    positive_weights = weight_array[weight_array > 0]
    effective_sample_size = (
        float(positive_weights.sum() ** 2 / np.square(positive_weights).sum())
        if len(positive_weights)
        else 0.0
    )

    if unsupported_count:
        ips_mean = None
        snips_mean = None
    else:
        ips_mean = float(weighted_array.sum() / len(frame))
        snips_mean = (
            float(weighted_array.sum() / weight_array.sum())
            if weight_array.sum() > 0
            else None
        )

    support_adequate = (
        unsupported_count == 0
        and match_count > 0
        and effective_sample_size >= minimum_effective_sample_size
    )
    return OfflinePolicyReport(
        policy_version=policy_version,
        validation_count=len(frame),
        action_match_count=match_count,
        action_match_rate=match_count / len(frame),
        unsupported_count=unsupported_count,
        ips_mean_resolution_hours=ips_mean,
        self_normalized_ips_mean_resolution_hours=snips_mean,
        effective_sample_size=effective_sample_size,
        observed_matched_mean_resolution_hours=(
            float(np.mean(matched_outcomes)) if matched_outcomes else None
        ),
        support_adequate=support_adequate,
        interpretation_note=(
            "IPS is an offline estimate that depends on correct logging propensities, overlap, "
            "the logged-data design and no unhandled violations of the estimator assumptions. "
            "The matched observed mean is descriptive only and is not a counterfactual estimate."
        ),
    )


def build_offline_comparison(
    data: pd.DataFrame,
    *,
    validation_fraction: float = 0.30,
    min_samples: int = 15,
    minimum_effective_sample_size: float = 20.0,
) -> tuple[OfflineComparison, OutcomeAwarePolicy]:
    split = chronological_split(data, validation_fraction=validation_fraction)
    candidate = train_outcome_aware_policy(split.training, min_samples=min_samples)
    baseline_report = evaluate_policy(
        split.validation,
        policy_version=ROUTER_VERSION,
        predictor=baseline_policy_decision,
        minimum_effective_sample_size=minimum_effective_sample_size,
    )
    candidate_report = evaluate_policy(
        split.validation,
        policy_version=candidate.version,
        predictor=candidate.predict,
        minimum_effective_sample_size=minimum_effective_sample_size,
    )

    if (
        baseline_report.ips_mean_resolution_hours is None
        or candidate_report.ips_mean_resolution_hours is None
    ):
        delta = None
        signal = "not_estimable"
    else:
        delta = (
            candidate_report.ips_mean_resolution_hours
            - baseline_report.ips_mean_resolution_hours
        )
        if delta < -1e-9:
            signal = "candidate_lower_estimated_resolution_time"
        elif delta > 1e-9:
            signal = "candidate_higher_estimated_resolution_time"
        else:
            signal = "no_estimated_difference"

    offline_gate_passed = (
        signal == "candidate_lower_estimated_resolution_time"
        and baseline_report.support_adequate
        and candidate_report.support_adequate
    )
    comparison = OfflineComparison(
        training_count=len(split.training),
        validation_count=len(split.validation),
        cutoff_time=split.cutoff_time,
        baseline=baseline_report,
        candidate=candidate_report,
        candidate_minus_baseline_ips_hours=delta,
        offline_signal=signal,
        offline_gate_passed=offline_gate_passed,
        deployment_eligible=False,
        limitations=(
            (
                "The current workflow uses synthetic logged data only; results are not "
                "production performance evidence."
            ),
            "Historical logged actions do not reveal outcomes for actions that were not taken.",
            (
                "IPS relies on known logging propensities and adequate overlap; unsupported "
                "actions must block an offline improvement signal."
            ),
            (
                "Passing the offline gate does not authorise deployment. Human approval and a "
                "separate pilot/governance decision are still required."
            ),
        ),
    )
    return comparison, candidate


class PolicyRegistry:
    """Local append-only lifecycle record for candidate approval, activation and rollback."""

    def __init__(self, path: str | Path = DEFAULT_REGISTRY_PATH) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {
                "schema_version": 1,
                "active_policy": ROUTER_VERSION,
                "policies": {
                    ROUTER_VERSION: {
                        "status": "active",
                        "approved": True,
                        "grandfathered_baseline": True,
                        "offline_gate_passed": True,
                    }
                },
                "events": [],
            }
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError("unsupported policy registry schema version")
        return payload

    def register_candidate(
        self,
        version: str,
        *,
        offline_gate_passed: bool,
        evaluation_summary: dict[str, Any],
    ) -> dict[str, Any]:
        if not version.strip() or version == ROUTER_VERSION:
            raise ValueError("candidate version must be non-blank and distinct from the baseline")
        payload = self.load()
        policies = payload["policies"]
        existing = policies.get(version)
        record = {
            "status": "candidate",
            "approved": False,
            "offline_gate_passed": bool(offline_gate_passed),
            "evaluation_summary": evaluation_summary,
        }
        if existing is not None and existing != record:
            raise ValueError("policy version already exists with different metadata")
        policies[version] = record
        self._append_event(payload, "candidate_registered", version, actor="system")
        self._save(payload)
        return payload

    def approve(self, version: str, *, reviewer: str, rationale: str) -> dict[str, Any]:
        reviewer = reviewer.strip()
        rationale = rationale.strip()
        if not reviewer or not rationale:
            raise ValueError("reviewer and rationale are required for policy approval")
        payload = self.load()
        record = self._candidate_record(payload, version)
        record["approved"] = True
        record["approval"] = {
            "reviewer": reviewer,
            "rationale": rationale,
            "approved_at": _utc_now(),
        }
        if record["status"] == "candidate":
            record["status"] = "approved"
        self._append_event(payload, "policy_approved", version, actor=reviewer)
        self._save(payload)
        return payload

    def activate(self, version: str, *, actor: str) -> dict[str, Any]:
        actor = actor.strip()
        if not actor:
            raise ValueError("actor is required for activation")
        payload = self.load()
        record = self._candidate_record(payload, version)
        if not record.get("approved"):
            raise ValueError("policy requires explicit human approval before activation")
        if not record.get("offline_gate_passed"):
            raise ValueError("policy did not pass the configured offline evaluation gate")

        previous = str(payload["active_policy"])
        if previous in payload["policies"]:
            payload["policies"][previous]["status"] = "inactive"
        record["status"] = "active"
        payload["active_policy"] = version
        self._append_event(
            payload,
            "policy_activated",
            version,
            actor=actor,
            details={"previous_policy": previous},
        )
        self._save(payload)
        return payload

    def rollback(self, version: str, *, actor: str, rationale: str) -> dict[str, Any]:
        actor = actor.strip()
        rationale = rationale.strip()
        if not actor or not rationale:
            raise ValueError("actor and rationale are required for rollback")
        payload = self.load()
        if version not in payload["policies"]:
            raise ValueError("rollback target is not registered")
        target = payload["policies"][version]
        if not target.get("approved"):
            raise ValueError("rollback target must be an approved policy")

        previous = str(payload["active_policy"])
        if previous in payload["policies"]:
            payload["policies"][previous]["status"] = "inactive"
        target["status"] = "active"
        payload["active_policy"] = version
        self._append_event(
            payload,
            "policy_rollback",
            version,
            actor=actor,
            details={"previous_policy": previous, "rationale": rationale},
        )
        self._save(payload)
        return payload

    def _candidate_record(self, payload: dict[str, Any], version: str) -> dict[str, Any]:
        policies = payload["policies"]
        if version not in policies or version == ROUTER_VERSION:
            raise ValueError("candidate policy is not registered")
        return policies[version]

    def _append_event(
        self,
        payload: dict[str, Any],
        event: str,
        version: str,
        *,
        actor: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        payload["events"].append(
            {
                "event": event,
                "policy_version": version,
                "actor": actor,
                "created_at": _utc_now(),
                "details": details or {},
            }
        )

    def _save(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _evaluate_command(args: argparse.Namespace) -> int:
    data = generate_logged_routing_history(n=args.synthetic_n, seed=args.seed)
    comparison, candidate = build_offline_comparison(
        data,
        validation_fraction=args.validation_fraction,
        min_samples=args.min_samples,
        minimum_effective_sample_size=args.minimum_effective_sample_size,
    )
    payload = {
        "data_provenance": "synthetic_logged_policy",
        "candidate_training": {
            "version": candidate.version,
            "trained_until": candidate.trained_until,
            "min_samples": candidate.min_samples,
            "choices": [asdict(choice) for choice in candidate.choices],
        },
        "comparison": comparison.to_dict(),
    }
    if args.register:
        registry = PolicyRegistry(args.registry)
        registry.register_candidate(
            candidate.version,
            offline_gate_passed=comparison.offline_gate_passed,
            evaluation_summary={
                "cutoff_time": comparison.cutoff_time,
                "offline_signal": comparison.offline_signal,
                "candidate_minus_baseline_ips_hours": (
                    comparison.candidate_minus_baseline_ips_hours
                ),
                "data_provenance": "synthetic_logged_policy",
            },
        )
        payload["registry"] = registry.load()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _registry_command(args: argparse.Namespace) -> int:
    registry = PolicyRegistry(args.registry)
    if args.command == "status":
        payload = registry.load()
    elif args.command == "approve":
        payload = registry.approve(
            args.version,
            reviewer=args.reviewer,
            rationale=args.rationale,
        )
    elif args.command == "activate":
        payload = registry.activate(args.version, actor=args.actor)
    elif args.command == "rollback":
        payload = registry.rollback(
            args.version,
            actor=args.actor,
            rationale=args.rationale,
        )
    else:  # pragma: no cover
        raise ValueError(f"unsupported registry command: {args.command}")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline adaptive-routing evaluation and policy lifecycle controls."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Run the synthetic Phase 3 offline study.")
    evaluate.add_argument("--synthetic-n", type=int, default=2000)
    evaluate.add_argument("--seed", type=int, default=2026)
    evaluate.add_argument("--validation-fraction", type=float, default=0.30)
    evaluate.add_argument("--min-samples", type=int, default=15)
    evaluate.add_argument("--minimum-effective-sample-size", type=float, default=20.0)
    evaluate.add_argument("--register", action="store_true")
    evaluate.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)

    status = subparsers.add_parser("status", help="Show the local policy lifecycle registry.")
    status.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)

    approve = subparsers.add_parser("approve", help="Record explicit human approval.")
    approve.add_argument("--version", required=True)
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--rationale", required=True)
    approve.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)

    activate = subparsers.add_parser("activate", help="Activate an approved candidate in registry.")
    activate.add_argument("--version", required=True)
    activate.add_argument("--actor", required=True)
    activate.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)

    rollback = subparsers.add_parser("rollback", help="Rollback to an approved policy version.")
    rollback.add_argument("--version", required=True)
    rollback.add_argument("--actor", required=True)
    rollback.add_argument("--rationale", required=True)
    rollback.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "evaluate":
        return _evaluate_command(args)
    return _registry_command(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
