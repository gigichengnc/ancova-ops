from __future__ import annotations

from .models import RoutingDecision, ServiceCase

ISSUE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "maintenance": (
        "leak",
        "water",
        "air con",
        "air-con",
        "air conditioner",
        "electric",
        "lift",
        "repair",
        "broken",
    ),
    "security": ("noise", "fight", "intruder", "security", "theft", "smoke"),
    "leasing": ("lease", "tenancy", "contract", "renewal"),
    "accounts": ("rent", "invoice", "payment", "charge", "fee", "deposit"),
}

CATEGORY_TO_DEPARTMENT = {
    "water_leak": "maintenance",
    "air_conditioning": "maintenance",
    "electrical": "maintenance",
    "noise_complaint": "security",
    "security": "security",
    "lease_question": "leasing",
    "payment_question": "accounts",
}


def _infer_department(case: ServiceCase) -> tuple[str, str]:
    if case.issue_category in CATEGORY_TO_DEPARTMENT:
        department = CATEGORY_TO_DEPARTMENT[case.issue_category]
        return department, f"issue category maps to {department}"

    normalized = case.message.lower()
    for department, keywords in ISSUE_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return department, f"message contains {department}-related terms"

    return "community_management", "no specialist category matched the baseline rules"


def baseline_route(case: ServiceCase) -> RoutingDecision:
    """Return a transparent baseline routing recommendation.

    This is intentionally simple. It provides a benchmark that future NLP/ML routing
    should outperform under a defined evaluation protocol.
    """

    department, category_reason = _infer_department(case)
    reasons = [category_reason]

    critical = case.urgency >= 9 or (
        case.vulnerability_flag and case.urgency >= 8 and case.complexity >= 7
    )
    high = (
        case.urgency >= 7
        or case.frustration >= 8
        or case.previous_related_cases >= 2
        or case.vulnerability_flag
    )

    if critical:
        priority = "critical"
        reasons.append("critical urgency/context threshold reached")
    elif high:
        priority = "high"
        reasons.append("high-priority context threshold reached")
    else:
        priority = "normal"

    requires_human_review = (
        priority == "critical"
        or case.vulnerability_flag
        or case.previous_related_cases >= 2
        or case.frustration >= 8
    )

    if case.previous_related_cases >= 2:
        reasons.append("multiple related cases indicate recurrence or unresolved history")
    if case.vulnerability_flag:
        reasons.append("vulnerability context requires human attention")
    if case.frustration >= 8:
        reasons.append("high communication/emotional-need signal")

    secondary_notify = None
    if department == "maintenance" and requires_human_review:
        secondary_notify = "community_management"
        reasons.append("community management notified for a high-context maintenance case")

    return RoutingDecision(
        department=department,
        priority=priority,
        requires_human_review=requires_human_review,
        secondary_notify=secondary_notify,
        reasons=tuple(reasons),
    )
