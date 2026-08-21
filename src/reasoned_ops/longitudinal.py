from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

LONGITUDINAL_PROVENANCE = "synthetic_longitudinal"
DEFAULT_START = pd.Timestamp("2025-01-01", tz="UTC")
DEFAULT_CLASSIFICATION_HORIZON_DAYS = 30
DEFAULT_FOLLOWUP_DAYS = 90
DEFAULT_INTERVAL_DAYS = 5

ISSUE_CATEGORIES = (
    "air_conditioning",
    "water_leak",
    "electrical",
    "noise_complaint",
    "security",
    "lease_question",
    "payment_question",
)

FEATURE_COLUMNS = (
    "cases_30d",
    "cases_90d",
    "days_since_last_case",
    "mean_resolution_90d",
    "escalation_rate_90d",
    "mean_urgency_90d",
    "mean_complexity_90d",
    "maintenance_share_90d",
    "security_share_90d",
    "leasing_share_90d",
    "accounts_share_90d",
    "month_sin",
    "month_cos",
)

SIMPLE_FEATURE_COLUMNS = (
    "cases_30d",
    "cases_90d",
    "days_since_last_case",
)


@dataclass(slots=True, frozen=True)
class LongitudinalSplit:
    training: pd.DataFrame
    validation: pd.DataFrame
    validation_start: str
    purge_days: int
    purged_snapshot_count: int


@dataclass(slots=True, frozen=True)
class ClassificationMetrics:
    roc_auc: float
    brier_score: float
    calibration_bias: float
    positive_rate: float


@dataclass(slots=True, frozen=True)
class ModelBenchmark:
    model_name: str
    model_family: str
    feature_count: int
    metrics: ClassificationMetrics
    survival_concordance: float | None = None


@dataclass(slots=True, frozen=True)
class LongitudinalBenchmarkReport:
    provenance: str
    entity_count: int
    event_count: int
    snapshot_count: int
    training_count: int
    validation_count: int
    validation_start: str
    classification_horizon_days: int
    maximum_followup_days: int
    purge_days: int
    purged_snapshot_count: int
    baseline: ModelBenchmark
    survival: ModelBenchmark
    tree: ModelBenchmark
    best_auc_model: str
    best_brier_model: str
    sequence_model_status: str
    complexity_conclusion: str
    leakage_checks: dict[str, bool]
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class DiscreteTimeHazardModel:
    """Discrete-time logistic hazard model for synthetic recurrence timing."""

    def __init__(
        self,
        *,
        interval_days: int = DEFAULT_INTERVAL_DAYS,
        maximum_followup_days: int = DEFAULT_FOLLOWUP_DAYS,
    ) -> None:
        if interval_days <= 0:
            raise ValueError("interval_days must be positive")
        if maximum_followup_days % interval_days:
            raise ValueError("maximum_followup_days must be divisible by interval_days")
        self.interval_days = interval_days
        self.maximum_followup_days = maximum_followup_days
        self.model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, random_state=2026),
        )

    def fit(self, snapshots: pd.DataFrame) -> DiscreteTimeHazardModel:
        expanded = _expand_person_period(
            snapshots,
            interval_days=self.interval_days,
            maximum_followup_days=self.maximum_followup_days,
        )
        features = [*FEATURE_COLUMNS, "interval_index"]
        self.model.fit(expanded[features], expanded["hazard_event"])
        return self

    def predict_event_probability(
        self,
        snapshots: pd.DataFrame,
        *,
        horizon_days: int,
    ) -> np.ndarray:
        if horizon_days <= 0 or horizon_days > self.maximum_followup_days:
            raise ValueError("horizon_days must be within the fitted follow-up window")
        if horizon_days % self.interval_days:
            raise ValueError("horizon_days must be divisible by interval_days")
        intervals = horizon_days // self.interval_days
        repeated = snapshots.loc[:, FEATURE_COLUMNS].loc[
            snapshots.index.repeat(intervals)
        ].reset_index(drop=True)
        repeated["interval_index"] = np.tile(
            np.arange(1, intervals + 1, dtype=float),
            len(snapshots),
        )
        features = [*FEATURE_COLUMNS, "interval_index"]
        hazards = self.model.predict_proba(repeated[features])[:, 1]
        hazard_matrix = hazards.reshape(len(snapshots), intervals)
        return 1.0 - np.prod(1.0 - hazard_matrix, axis=1)


def generate_longitudinal_history(
    *,
    n_entities: int = 240,
    n_days: int = 720,
    seed: int = 2026,
    start: pd.Timestamp = DEFAULT_START,
) -> pd.DataFrame:
    """Generate deterministic synthetic service-case histories.

    The entity IDs and event histories are artificial. The generator intentionally
    includes recurrence feedback and seasonality so longitudinal models have a
    non-trivial development benchmark.
    """

    if n_entities < 80:
        raise ValueError("n_entities must be at least 80")
    if n_days < 540:
        raise ValueError("n_days must be at least 540")
    start = pd.Timestamp(start)
    if start.tzinfo is None:
        start = start.tz_localize("UTC")
    else:
        start = start.tz_convert("UTC")

    rng = np.random.default_rng(seed)
    category_probabilities = np.array([0.17, 0.17, 0.11, 0.14, 0.12, 0.14, 0.15])
    events: list[dict[str, object]] = []
    case_counter = 0

    for entity_index in range(n_entities):
        entity_id = f"synthetic-entity-{entity_index:04d}"
        latent_recurrence = float(rng.normal(0.0, 0.65))
        dominant_category = str(rng.choice(ISSUE_CATEGORIES, p=category_probabilities))
        seasonal_phase = float(rng.uniform(0.0, 2.0 * math.pi))
        initial_day = int(rng.integers(5, 46))
        event_days: list[int] = [initial_day]

        events.append(
            _make_synthetic_event(
                rng,
                entity_id=entity_id,
                case_counter=case_counter,
                event_day=initial_day,
                start=start,
                category=dominant_category,
                latent_recurrence=latent_recurrence,
            )
        )
        case_counter += 1

        for day in range(initial_day + 1, n_days):
            recent_30 = sum(1 for event_day in event_days if day - 30 < event_day < day)
            recent_90 = sum(1 for event_day in event_days if day - 90 < event_day < day)
            season = math.sin((2.0 * math.pi * day / 365.25) + seasonal_phase)
            logit = (
                -5.05
                + 0.78 * latent_recurrence
                + 0.68 * min(recent_30, 2)
                + 0.18 * min(recent_90, 4)
                + 0.42 * season
            )
            probability = 1.0 / (1.0 + math.exp(-logit))
            if rng.random() >= probability:
                continue

            if rng.random() < 0.68:
                category = dominant_category
            else:
                category = str(rng.choice(ISSUE_CATEGORIES, p=category_probabilities))
            events.append(
                _make_synthetic_event(
                    rng,
                    entity_id=entity_id,
                    case_counter=case_counter,
                    event_day=day,
                    start=start,
                    category=category,
                    latent_recurrence=latent_recurrence,
                )
            )
            event_days.append(day)
            case_counter += 1

    frame = pd.DataFrame(events).sort_values(["event_time", "case_id"]).reset_index(drop=True)
    frame["event_time"] = pd.to_datetime(frame["event_time"], utc=True)
    return frame


def build_longitudinal_snapshots(
    history: pd.DataFrame,
    *,
    min_history_days: int = 180,
    step_days: int = 30,
    classification_horizon_days: int = DEFAULT_CLASSIFICATION_HORIZON_DAYS,
    maximum_followup_days: int = DEFAULT_FOLLOWUP_DAYS,
) -> pd.DataFrame:
    """Build entity-time snapshots using only events at or before each cutoff."""

    frame = _validate_history(history)
    if min_history_days < 90:
        raise ValueError("min_history_days must be at least 90")
    if step_days <= 0:
        raise ValueError("step_days must be positive")
    if classification_horizon_days <= 0:
        raise ValueError("classification_horizon_days must be positive")
    if maximum_followup_days < classification_horizon_days:
        raise ValueError("maximum_followup_days must cover the classification horizon")

    observation_start = frame["event_time"].min().floor("D")
    observation_end = frame["event_time"].max().ceil("D")
    first_cutoff = observation_start + pd.Timedelta(days=min_history_days)
    last_cutoff = observation_end - pd.Timedelta(days=maximum_followup_days)
    if first_cutoff >= last_cutoff:
        raise ValueError("history does not provide enough time for longitudinal snapshots")

    cutoffs = pd.date_range(first_cutoff, last_cutoff, freq=f"{step_days}D", tz="UTC")
    entity_ids = sorted(frame["entity_id"].astype(str).unique())
    grouped = {
        entity_id: group.sort_values("event_time")
        for entity_id, group in frame.groupby("entity_id")
    }
    snapshots: list[dict[str, object]] = []

    for cutoff in cutoffs:
        for entity_id in entity_ids:
            entity_events = grouped[entity_id]
            past = entity_events.loc[entity_events["event_time"] <= cutoff]
            if past.empty:
                continue
            window_30 = past.loc[past["event_time"] > cutoff - pd.Timedelta(days=30)]
            window_90 = past.loc[past["event_time"] > cutoff - pd.Timedelta(days=90)]
            future = entity_events.loc[entity_events["event_time"] > cutoff]
            next_event_time = None if future.empty else future.iloc[0]["event_time"]

            if next_event_time is not None:
                duration_days = max(
                    float((next_event_time - cutoff).total_seconds() / 86400.0),
                    1e-6,
                )
                event_observed = duration_days <= maximum_followup_days
            else:
                duration_days = float(maximum_followup_days)
                event_observed = False

            capped_duration = min(duration_days, float(maximum_followup_days))
            recurrence_30d = bool(
                next_event_time is not None
                and next_event_time
                <= cutoff + pd.Timedelta(days=classification_horizon_days)
            )
            last_event_time = past.iloc[-1]["event_time"]
            days_since_last = float((cutoff - last_event_time).total_seconds() / 86400.0)

            shares = _department_shares(window_90)
            snapshots.append(
                {
                    "entity_id": entity_id,
                    "cutoff_time": cutoff,
                    "feature_max_event_time": last_event_time,
                    "label_end_time": cutoff + pd.Timedelta(days=maximum_followup_days),
                    "cases_30d": int(len(window_30)),
                    "cases_90d": int(len(window_90)),
                    "days_since_last_case": days_since_last,
                    "mean_resolution_90d": _mean_or_zero(window_90, "resolution_hours"),
                    "escalation_rate_90d": _mean_or_zero(window_90, "escalated"),
                    "mean_urgency_90d": _mean_or_zero(window_90, "urgency"),
                    "mean_complexity_90d": _mean_or_zero(window_90, "complexity"),
                    **shares,
                    "month_sin": math.sin(2.0 * math.pi * cutoff.month / 12.0),
                    "month_cos": math.cos(2.0 * math.pi * cutoff.month / 12.0),
                    "recurrence_30d": recurrence_30d,
                    "time_to_next_case_days": capped_duration,
                    "event_observed": bool(event_observed),
                    "data_provenance": LONGITUDINAL_PROVENANCE,
                }
            )

    result = pd.DataFrame(snapshots).sort_values(["cutoff_time", "entity_id"]).reset_index(drop=True)
    if result.empty:
        raise ValueError("longitudinal snapshot construction produced no rows")
    return result


def purged_chronological_split(
    snapshots: pd.DataFrame,
    *,
    validation_fraction: float = 0.30,
    purge_days: int = DEFAULT_FOLLOWUP_DAYS,
) -> LongitudinalSplit:
    """Split snapshots by time and purge training labels that reach validation."""

    frame = _validate_snapshots(snapshots)
    if not 0.15 <= validation_fraction <= 0.45:
        raise ValueError("validation_fraction must be between 0.15 and 0.45")
    if purge_days <= 0:
        raise ValueError("purge_days must be positive")

    unique_cutoffs = np.array(sorted(frame["cutoff_time"].unique()))
    validation_index = int(len(unique_cutoffs) * (1.0 - validation_fraction))
    validation_index = min(max(validation_index, 1), len(unique_cutoffs) - 1)
    validation_start = pd.Timestamp(unique_cutoffs[validation_index]).tz_convert("UTC")

    validation = frame.loc[frame["cutoff_time"] >= validation_start].copy()
    pre_validation = frame.loc[frame["cutoff_time"] < validation_start].copy()
    training = pre_validation.loc[pre_validation["label_end_time"] < validation_start].copy()
    purged_snapshot_count = len(pre_validation) - len(training)

    if len(training) < 100 or len(validation) < 50:
        raise ValueError("purged time split leaves too few training or validation snapshots")
    if training["feature_max_event_time"].max() > training["cutoff_time"].max():
        raise ValueError("training features contain events after their cutoff")
    if validation["feature_max_event_time"].max() > validation["cutoff_time"].max():
        raise ValueError("validation features contain events after their cutoff")
    if training["label_end_time"].max() >= validation["cutoff_time"].min():
        raise ValueError("training follow-up leaks into the validation period")

    return LongitudinalSplit(
        training=training,
        validation=validation,
        validation_start=validation_start.isoformat(),
        purge_days=purge_days,
        purged_snapshot_count=purged_snapshot_count,
    )


def run_longitudinal_benchmark(
    *,
    n_entities: int = 240,
    n_days: int = 720,
    seed: int = 2026,
    classification_horizon_days: int = DEFAULT_CLASSIFICATION_HORIZON_DAYS,
    maximum_followup_days: int = DEFAULT_FOLLOWUP_DAYS,
) -> LongitudinalBenchmarkReport:
    history = generate_longitudinal_history(
        n_entities=n_entities,
        n_days=n_days,
        seed=seed,
    )
    snapshots = build_longitudinal_snapshots(
        history,
        classification_horizon_days=classification_horizon_days,
        maximum_followup_days=maximum_followup_days,
    )
    split = purged_chronological_split(
        snapshots,
        purge_days=maximum_followup_days,
    )
    train = split.training
    validation = split.validation
    y_train = train["recurrence_30d"].astype(int).to_numpy()
    y_validation = validation["recurrence_30d"].astype(int).to_numpy()

    baseline_model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, random_state=seed),
    )
    baseline_model.fit(train.loc[:, SIMPLE_FEATURE_COLUMNS], y_train)
    baseline_probability = baseline_model.predict_proba(
        validation.loc[:, SIMPLE_FEATURE_COLUMNS]
    )[:, 1]

    hazard_model = DiscreteTimeHazardModel(
        maximum_followup_days=maximum_followup_days,
    ).fit(train)
    survival_probability = hazard_model.predict_event_probability(
        validation,
        horizon_days=classification_horizon_days,
    )
    survival_risk_90d = hazard_model.predict_event_probability(
        validation,
        horizon_days=maximum_followup_days,
    )

    tree_model = RandomForestClassifier(
        n_estimators=160,
        max_depth=6,
        min_samples_leaf=12,
        random_state=seed,
        n_jobs=1,
        class_weight="balanced_subsample",
    )
    tree_model.fit(train.loc[:, FEATURE_COLUMNS], y_train)
    tree_probability = tree_model.predict_proba(validation.loc[:, FEATURE_COLUMNS])[:, 1]

    baseline_benchmark = ModelBenchmark(
        model_name="recency-frequency-logistic-v1",
        model_family="simple_baseline",
        feature_count=len(SIMPLE_FEATURE_COLUMNS),
        metrics=_classification_metrics(y_validation, baseline_probability),
    )
    survival_benchmark = ModelBenchmark(
        model_name="discrete-time-logistic-hazard-v1",
        model_family="survival_time_to_event",
        feature_count=len(FEATURE_COLUMNS) + 1,
        metrics=_classification_metrics(y_validation, survival_probability),
        survival_concordance=_harrell_c_index(
            validation["time_to_next_case_days"].to_numpy(dtype=float),
            validation["event_observed"].astype(bool).to_numpy(),
            survival_risk_90d,
        ),
    )
    tree_benchmark = ModelBenchmark(
        model_name="random-forest-recurrence-v1",
        model_family="tree_classifier",
        feature_count=len(FEATURE_COLUMNS),
        metrics=_classification_metrics(y_validation, tree_probability),
    )

    benchmarks = (baseline_benchmark, survival_benchmark, tree_benchmark)
    best_auc = max(benchmarks, key=lambda item: item.metrics.roc_auc)
    best_brier = min(benchmarks, key=lambda item: item.metrics.brier_score)
    complexity_conclusion = _complexity_conclusion(
        baseline_benchmark,
        survival_benchmark,
        tree_benchmark,
    )

    leakage_checks = {
        "features_at_or_before_cutoff": bool(
            (snapshots["feature_max_event_time"] <= snapshots["cutoff_time"]).all()
        ),
        "training_followup_ends_before_validation": bool(
            train["label_end_time"].max() < validation["cutoff_time"].min()
        ),
        "validation_is_chronologically_later": bool(
            train["cutoff_time"].max() < validation["cutoff_time"].min()
        ),
        "synthetic_only_provenance": set(snapshots["data_provenance"].unique())
        == {LONGITUDINAL_PROVENANCE},
    }

    return LongitudinalBenchmarkReport(
        provenance=LONGITUDINAL_PROVENANCE,
        entity_count=int(history["entity_id"].nunique()),
        event_count=len(history),
        snapshot_count=len(snapshots),
        training_count=len(train),
        validation_count=len(validation),
        validation_start=split.validation_start,
        classification_horizon_days=classification_horizon_days,
        maximum_followup_days=maximum_followup_days,
        purge_days=split.purge_days,
        purged_snapshot_count=split.purged_snapshot_count,
        baseline=baseline_benchmark,
        survival=survival_benchmark,
        tree=tree_benchmark,
        best_auc_model=best_auc.model_name,
        best_brier_model=best_brier.model_name,
        sequence_model_status="deferred_not_justified_by_current_benchmark",
        complexity_conclusion=complexity_conclusion,
        leakage_checks=leakage_checks,
        limitations=(
            "All histories are synthetic and do not represent resident or customer behaviour.",
            "Repeated snapshots from the same synthetic entities are used for time-aware forecasting; "
            "the benchmark therefore evaluates future-period generalisation, not unseen-entity generalisation.",
            "Brier score and ROC-AUC assess the 30-day recurrence target; they do not establish operational value.",
            "The discrete-time hazard model is a development time-to-event baseline, not a production survival model.",
            "No sequence model is included. LSTM or other sequence architectures require a separate same-benchmark "
            "comparison and evidence of incremental value over these simpler approaches.",
            "Real longitudinal personalisation remains prohibited until the pilot governance requirements are approved.",
        ),
    )


def _make_synthetic_event(
    rng: np.random.Generator,
    *,
    entity_id: str,
    case_counter: int,
    event_day: int,
    start: pd.Timestamp,
    category: str,
    latent_recurrence: float,
) -> dict[str, object]:
    urgency = float(np.clip(rng.normal(5.1 + 0.35 * latent_recurrence, 1.8), 0.0, 10.0))
    complexity = float(np.clip(rng.normal(4.8 + 0.25 * latent_recurrence, 1.6), 0.0, 10.0))
    category_effect = {
        "air_conditioning": 2.0,
        "water_leak": 3.0,
        "electrical": 2.6,
        "noise_complaint": -0.5,
        "security": -0.8,
        "lease_question": 4.3,
        "payment_question": 1.2,
    }[category]
    resolution_hours = max(
        0.5,
        float(
            7.0
            + category_effect
            + 1.0 * urgency
            + 1.45 * complexity
            + 1.3 * latent_recurrence
            + rng.normal(0.0, 3.5)
        ),
    )
    escalation_logit = -4.2 + 0.34 * urgency + 0.25 * complexity + 0.3 * latent_recurrence
    escalation_probability = 1.0 / (1.0 + math.exp(-escalation_logit))
    return {
        "entity_id": entity_id,
        "case_id": f"long-case-{case_counter:07d}",
        "event_time": start + pd.Timedelta(days=event_day, hours=12),
        "issue_category": category,
        "urgency": urgency,
        "complexity": complexity,
        "resolution_hours": resolution_hours,
        "escalated": int(rng.random() < escalation_probability),
        "data_provenance": LONGITUDINAL_PROVENANCE,
    }


def _department_shares(window: pd.DataFrame) -> dict[str, float]:
    if window.empty:
        return {
            "maintenance_share_90d": 0.0,
            "security_share_90d": 0.0,
            "leasing_share_90d": 0.0,
            "accounts_share_90d": 0.0,
        }

    categories = window["issue_category"].astype(str)
    maintenance = categories.isin(["air_conditioning", "water_leak", "electrical"]).mean()
    security = categories.isin(["noise_complaint", "security"]).mean()
    leasing = categories.eq("lease_question").mean()
    accounts = categories.eq("payment_question").mean()
    return {
        "maintenance_share_90d": float(maintenance),
        "security_share_90d": float(security),
        "leasing_share_90d": float(leasing),
        "accounts_share_90d": float(accounts),
    }


def _mean_or_zero(frame: pd.DataFrame, column: str) -> float:
    if frame.empty:
        return 0.0
    return float(frame[column].mean())


def _validate_history(history: pd.DataFrame) -> pd.DataFrame:
    required = {
        "entity_id",
        "case_id",
        "event_time",
        "issue_category",
        "urgency",
        "complexity",
        "resolution_hours",
        "escalated",
        "data_provenance",
    }
    missing = sorted(required.difference(history.columns))
    if missing:
        raise ValueError("longitudinal history missing columns: " + ", ".join(missing))
    if history.empty:
        raise ValueError("longitudinal history cannot be empty")
    frame = history.copy()
    provenance = {str(value) for value in frame["data_provenance"].dropna().unique()}
    if provenance != {LONGITUDINAL_PROVENANCE}:
        raise ValueError("Phase 4 benchmark accepts only synthetic_longitudinal provenance")
    frame["event_time"] = pd.to_datetime(frame["event_time"], utc=True, errors="raise")
    if frame["case_id"].astype(str).duplicated().any():
        raise ValueError("case_id must be unique")
    if (frame["resolution_hours"].astype(float) <= 0).any():
        raise ValueError("resolution_hours must be positive")
    return frame


def _validate_snapshots(snapshots: pd.DataFrame) -> pd.DataFrame:
    required = {
        "entity_id",
        "cutoff_time",
        "feature_max_event_time",
        "label_end_time",
        "recurrence_30d",
        "time_to_next_case_days",
        "event_observed",
        "data_provenance",
        *FEATURE_COLUMNS,
    }
    missing = sorted(required.difference(snapshots.columns))
    if missing:
        raise ValueError("longitudinal snapshots missing columns: " + ", ".join(missing))
    frame = snapshots.copy()
    frame["cutoff_time"] = pd.to_datetime(frame["cutoff_time"], utc=True, errors="raise")
    frame["feature_max_event_time"] = pd.to_datetime(
        frame["feature_max_event_time"],
        utc=True,
        errors="raise",
    )
    frame["label_end_time"] = pd.to_datetime(frame["label_end_time"], utc=True, errors="raise")
    if set(frame["data_provenance"].astype(str).unique()) != {LONGITUDINAL_PROVENANCE}:
        raise ValueError("longitudinal snapshots must be synthetic_longitudinal")
    if (frame["feature_max_event_time"] > frame["cutoff_time"]).any():
        raise ValueError("snapshot feature history extends beyond the cutoff")
    return frame


def _expand_person_period(
    snapshots: pd.DataFrame,
    *,
    interval_days: int,
    maximum_followup_days: int,
) -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []
    for row in snapshots.itertuples(index=False):
        duration = min(float(row.time_to_next_case_days), float(maximum_followup_days))
        interval_count = max(1, int(math.ceil(duration / interval_days)))
        event_interval = (
            int(math.ceil(duration / interval_days))
            if bool(row.event_observed) and duration <= maximum_followup_days
            else None
        )
        base = {feature: float(getattr(row, feature)) for feature in FEATURE_COLUMNS}
        for interval_index in range(1, interval_count + 1):
            rows.append(
                {
                    **base,
                    "interval_index": float(interval_index),
                    "hazard_event": int(event_interval == interval_index),
                }
            )
    expanded = pd.DataFrame(rows)
    if expanded["hazard_event"].nunique() < 2:
        raise ValueError("person-period expansion requires both event and non-event rows")
    return expanded


def _classification_metrics(
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> ClassificationMetrics:
    if len(np.unique(y_true)) < 2:
        raise ValueError("classification metrics require both outcome classes")
    probabilities = np.clip(np.asarray(probabilities, dtype=float), 1e-8, 1.0 - 1e-8)
    observed_rate = float(np.mean(y_true))
    return ClassificationMetrics(
        roc_auc=float(roc_auc_score(y_true, probabilities)),
        brier_score=float(brier_score_loss(y_true, probabilities)),
        calibration_bias=float(np.mean(probabilities) - observed_rate),
        positive_rate=observed_rate,
    )


def _harrell_c_index(
    durations: np.ndarray,
    event_observed: np.ndarray,
    risk_scores: np.ndarray,
) -> float:
    concordant = 0.0
    comparable = 0
    for left in range(len(durations) - 1):
        for right in range(left + 1, len(durations)):
            left_duration = durations[left]
            right_duration = durations[right]
            if event_observed[left] and left_duration < right_duration:
                earlier, later = left, right
            elif event_observed[right] and right_duration < left_duration:
                earlier, later = right, left
            else:
                continue
            comparable += 1
            if risk_scores[earlier] > risk_scores[later]:
                concordant += 1.0
            elif risk_scores[earlier] == risk_scores[later]:
                concordant += 0.5
    if not comparable:
        raise ValueError("survival concordance has no comparable event pairs")
    return concordant / comparable


def _complexity_conclusion(
    baseline: ModelBenchmark,
    survival: ModelBenchmark,
    tree: ModelBenchmark,
) -> str:
    baseline_auc = baseline.metrics.roc_auc
    baseline_brier = baseline.metrics.brier_score
    challengers = (survival, tree)
    materially_better = [
        challenger.model_name
        for challenger in challengers
        if challenger.metrics.roc_auc >= baseline_auc + 0.02
        and challenger.metrics.brier_score <= baseline_brier
    ]
    if not materially_better:
        return (
            "No more-complex model clears the current incremental-value rule over the "
            "recency/frequency baseline; retain the simple reference model for now."
        )
    return (
        "At least one more-complex model improves ROC-AUC by at least 0.02 without a worse "
        "Brier score on the same future window. This justifies further study of that model "
        "family, not automatic deployment or a sequence model."
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the ReasonedOps synthetic longitudinal recurrence benchmark."
    )
    parser.add_argument("--entities", type=int, default=240)
    parser.add_argument("--days", type=int, default=720)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--output", type=Path, help="Optional JSON output file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = run_longitudinal_benchmark(
        n_entities=args.entities,
        n_days=args.days,
        seed=args.seed,
    )
    payload = report.to_dict()

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print("ReasonedOps synthetic longitudinal benchmark")
    print(f"Provenance: {report.provenance}")
    print(
        f"Snapshots: {report.snapshot_count} "
        f"(train={report.training_count}, validation={report.validation_count}, "
        f"purged={report.purged_snapshot_count})"
    )
    for benchmark in (report.baseline, report.survival, report.tree):
        line = (
            f"{benchmark.model_name}: AUC={benchmark.metrics.roc_auc:.3f}, "
            f"Brier={benchmark.metrics.brier_score:.3f}, "
            f"calibration_bias={benchmark.metrics.calibration_bias:+.3f}"
        )
        if benchmark.survival_concordance is not None:
            line += f", C-index={benchmark.survival_concordance:.3f}"
        print(line)
    print(f"Sequence model status: {report.sequence_model_status}")
    print(report.complexity_conclusion)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
