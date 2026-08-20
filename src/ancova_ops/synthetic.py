from __future__ import annotations

import numpy as np
import pandas as pd

DEPARTMENTS = np.array(["maintenance", "security", "leasing", "accounts"])
ISSUE_BY_DEPARTMENT = {
    "maintenance": "maintenance_issue",
    "security": "security_issue",
    "leasing": "lease_question",
    "accounts": "payment_question",
}

LOGGED_ROUTING_DEPARTMENTS = np.array(
    ["maintenance", "security", "leasing", "accounts", "community_management"]
)
LOGGED_ROUTING_CATEGORIES = np.array(
    ["water_leak", "security", "lease_question", "payment_question", "noise_complaint"]
)
BASELINE_DEPARTMENT_BY_CATEGORY = {
    "water_leak": "maintenance",
    "security": "security",
    "lease_question": "leasing",
    "payment_question": "accounts",
    "noise_complaint": "security",
}
SYNTHETIC_OPTIMAL_DEPARTMENT_BY_CATEGORY = {
    "water_leak": "maintenance",
    "security": "security",
    "lease_question": "leasing",
    "payment_question": "accounts",
    "noise_complaint": "community_management",
}


def generate_outcomes(n: int = 500, seed: int = 2026) -> pd.DataFrame:
    """Generate synthetic completed service cases for development and tests.

    The generated effects are deliberately artificial. Results from this dataset must
    never be presented as observed service performance.
    """

    if n < 20:
        raise ValueError("n must be at least 20 for a useful demonstration dataset")

    rng = np.random.default_rng(seed)
    department = rng.choice(DEPARTMENTS, size=n, replace=True)
    urgency = np.clip(rng.normal(5.5, 2.0, size=n), 0, 10)
    frustration = np.clip(rng.normal(5.0, 2.2, size=n), 0, 10)
    complexity = np.clip(rng.normal(5.0, 1.8, size=n), 0, 10)
    previous_related_cases = rng.poisson(0.7, size=n)

    department_effect = {
        "maintenance": 3.0,
        "security": -1.0,
        "leasing": 5.0,
        "accounts": 1.5,
    }
    dept_hours = np.array([department_effect[d] for d in department])

    noise = rng.normal(0, 4.0, size=n)
    resolution_hours = (
        8
        + dept_hours
        + 1.1 * urgency
        + 0.7 * frustration
        + 1.8 * complexity
        + 1.2 * previous_related_cases
        + noise
    )
    resolution_hours = np.clip(resolution_hours, 0.5, None)

    escalation_logit = -4 + 0.35 * urgency + 0.25 * frustration + 0.35 * previous_related_cases
    escalation_probability = 1 / (1 + np.exp(-escalation_logit))
    escalated = rng.binomial(1, escalation_probability)

    satisfaction = np.clip(
        9.0 - 0.07 * resolution_hours - 0.25 * escalated + rng.normal(0, 0.7, size=n),
        1,
        10,
    )

    return pd.DataFrame(
        {
            "department": department,
            "issue_category": [ISSUE_BY_DEPARTMENT[d] for d in department],
            "urgency": urgency,
            "frustration": frustration,
            "complexity": complexity,
            "previous_related_cases": previous_related_cases,
            "resolution_hours": resolution_hours,
            "escalated": escalated,
            "satisfaction": satisfaction,
            "data_provenance": "synthetic",
        }
    )


def generate_logged_routing_history(
    n: int = 2000,
    seed: int = 2026,
    start: str = "2026-01-01T00:00:00Z",
) -> pd.DataFrame:
    """Generate synthetic logged routing decisions for offline-policy experiments.

    The logging policy assigns the existing baseline department with probability 0.60
    and each of the four other departments with probability 0.10. These known
    propensities make support-aware inverse-propensity examples possible. The synthetic
    data-generating process intentionally makes community management faster for the
    `noise_complaint` category so an outcome-aware candidate has one learnable departure
    from the current baseline. This is a simulation property, not operational evidence.
    """

    if n < 100:
        raise ValueError("n must be at least 100 for the logged-routing demonstration")

    rng = np.random.default_rng(seed)
    categories = rng.choice(LOGGED_ROUTING_CATEGORIES, size=n, replace=True)
    urgency = np.clip(rng.normal(5.3, 2.0, size=n), 0, 10)
    frustration = np.clip(rng.normal(5.0, 2.1, size=n), 0, 10)
    complexity = np.clip(rng.normal(5.2, 1.8, size=n), 0, 10)
    previous_related_cases = rng.poisson(0.7, size=n)

    logged_departments: list[str] = []
    probability_rows: list[dict[str, float]] = []
    for category in categories:
        baseline = BASELINE_DEPARTMENT_BY_CATEGORY[str(category)]
        probabilities = {
            department: (0.60 if department == baseline else 0.10)
            for department in LOGGED_ROUTING_DEPARTMENTS
        }
        probability_rows.append(probabilities)
        logged_departments.append(
            str(
                rng.choice(
                    LOGGED_ROUTING_DEPARTMENTS,
                    p=[probabilities[str(action)] for action in LOGGED_ROUTING_DEPARTMENTS],
                )
            )
        )

    optimal = np.array(
        [SYNTHETIC_OPTIMAL_DEPARTMENT_BY_CATEGORY[str(category)] for category in categories]
    )
    logged = np.array(logged_departments)
    mismatch_penalty = np.where(logged == optimal, 0.0, 5.0)
    noise_baseline_mask = (categories == "noise_complaint") & (logged == "security")
    mismatch_penalty = np.where(noise_baseline_mask, 2.5, mismatch_penalty)

    category_base = {
        "water_leak": 7.5,
        "security": 6.0,
        "lease_question": 9.0,
        "payment_question": 7.0,
        "noise_complaint": 6.5,
    }
    base_hours = np.array([category_base[str(category)] for category in categories])
    resolution_hours = (
        base_hours
        + 0.8 * urgency
        + 0.45 * frustration
        + 1.1 * complexity
        + 0.9 * previous_related_cases
        + mismatch_penalty
        + rng.normal(0, 2.0, size=n)
    )
    resolution_hours = np.clip(resolution_hours, 0.5, None)

    mismatch = (logged != optimal).astype(float)
    escalation_logit = (
        -4.2
        + 0.32 * urgency
        + 0.20 * frustration
        + 0.30 * previous_related_cases
        + 0.55 * mismatch
    )
    escalation_probability = 1 / (1 + np.exp(-escalation_logit))
    escalated = rng.binomial(1, escalation_probability)
    satisfaction = np.clip(
        9.2 - 0.08 * resolution_hours - 0.35 * escalated + rng.normal(0, 0.6, size=n),
        1,
        10,
    )

    frame = pd.DataFrame(
        {
            "case_id": [f"synthetic-policy-{index:05d}" for index in range(n)],
            "event_time": pd.date_range(start=start, periods=n, freq="h"),
            "issue_category": categories,
            "urgency": urgency,
            "frustration": frustration,
            "complexity": complexity,
            "previous_related_cases": previous_related_cases,
            "logged_department": logged,
            "resolution_hours": resolution_hours,
            "escalated": escalated,
            "satisfaction": satisfaction,
            "data_provenance": "synthetic_logged_policy",
        }
    )

    for department in LOGGED_ROUTING_DEPARTMENTS:
        frame[f"propensity_{department}"] = [
            row[str(department)] for row in probability_rows
        ]
    frame["logged_propensity"] = [
        probability_rows[index][logged_departments[index]] for index in range(n)
    ]
    return frame
