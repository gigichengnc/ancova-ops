from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from ancova_ops.longitudinal import (
    LONGITUDINAL_PROVENANCE,
    DiscreteTimeHazardModel,
    build_longitudinal_snapshots,
    generate_longitudinal_history,
    purged_chronological_split,
    run_longitudinal_benchmark,
)


def test_longitudinal_history_is_deterministic_and_synthetic() -> None:
    first = generate_longitudinal_history(n_entities=80, n_days=540, seed=7)
    second = generate_longitudinal_history(n_entities=80, n_days=540, seed=7)

    pd.testing.assert_frame_equal(first, second)
    assert set(first["data_provenance"]) == {LONGITUDINAL_PROVENANCE}
    assert first["entity_id"].nunique() == 80
    assert first["case_id"].is_unique


def test_snapshot_features_never_use_future_events() -> None:
    history = generate_longitudinal_history(n_entities=80, n_days=540, seed=11)
    snapshots = build_longitudinal_snapshots(history)
    assert (snapshots["feature_max_event_time"] <= snapshots["cutoff_time"]).all()

    selected = snapshots.iloc[len(snapshots) // 2]
    cutoff = pd.Timestamp(selected["cutoff_time"])
    entity_id = str(selected["entity_id"])
    before = snapshots.loc[
        (snapshots["entity_id"] == entity_id)
        & (snapshots["cutoff_time"] == cutoff)
    ].iloc[0]

    injected = history.iloc[0].copy()
    injected["entity_id"] = entity_id
    injected["case_id"] = "future-injected-case"
    injected["event_time"] = cutoff + pd.Timedelta(days=10, hours=12)
    modified = pd.concat([history, pd.DataFrame([injected])], ignore_index=True)
    rebuilt = build_longitudinal_snapshots(modified)
    after = rebuilt.loc[
        (rebuilt["entity_id"] == entity_id)
        & (rebuilt["cutoff_time"] == cutoff)
    ].iloc[0]

    feature_columns = [
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
    ]
    for column in feature_columns:
        assert after[column] == pytest.approx(before[column])


def test_purged_split_keeps_training_followup_before_validation() -> None:
    history = generate_longitudinal_history(n_entities=90, n_days=570, seed=13)
    snapshots = build_longitudinal_snapshots(history)
    split = purged_chronological_split(snapshots)

    assert split.training["label_end_time"].max() < split.validation["cutoff_time"].min()
    assert split.training["cutoff_time"].max() < split.validation["cutoff_time"].min()
    assert split.purged_snapshot_count > 0


def test_wrong_provenance_is_rejected() -> None:
    history = generate_longitudinal_history(n_entities=80, n_days=540, seed=17)
    history.loc[0, "data_provenance"] = "pilot"
    with pytest.raises(ValueError, match="synthetic_longitudinal"):
        build_longitudinal_snapshots(history)


def test_discrete_time_hazard_probabilities_are_bounded() -> None:
    history = generate_longitudinal_history(n_entities=90, n_days=570, seed=19)
    snapshots = build_longitudinal_snapshots(history)
    split = purged_chronological_split(snapshots)
    model = DiscreteTimeHazardModel().fit(split.training)
    probabilities = model.predict_event_probability(split.validation, horizon_days=30)

    assert len(probabilities) == len(split.validation)
    assert np.all(probabilities >= 0.0)
    assert np.all(probabilities <= 1.0)


def test_benchmark_compares_three_model_families_and_defers_sequence_models() -> None:
    report = run_longitudinal_benchmark(n_entities=100, n_days=600, seed=23)

    assert report.provenance == LONGITUDINAL_PROVENANCE
    assert report.baseline.model_family == "simple_baseline"
    assert report.survival.model_family == "survival_time_to_event"
    assert report.tree.model_family == "tree_classifier"
    assert report.sequence_model_status == "deferred_not_justified_by_current_benchmark"
    assert all(report.leakage_checks.values())

    for model in (report.baseline, report.survival, report.tree):
        assert 0.0 <= model.metrics.roc_auc <= 1.0
        assert 0.0 <= model.metrics.brier_score <= 1.0
        assert -1.0 <= model.metrics.calibration_bias <= 1.0

    assert report.survival.survival_concordance is not None
    assert 0.0 <= report.survival.survival_concordance <= 1.0


def test_benchmark_is_deterministic_for_same_seed() -> None:
    first = run_longitudinal_benchmark(n_entities=90, n_days=570, seed=29)
    second = run_longitudinal_benchmark(n_entities=90, n_days=570, seed=29)

    assert first.to_dict() == second.to_dict()
