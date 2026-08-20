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
