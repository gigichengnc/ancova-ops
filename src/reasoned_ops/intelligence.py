from __future__ import annotations

import re
from dataclasses import dataclass

INTELLIGENCE_VERSION = "baseline-request-intelligence-v2"


@dataclass(slots=True, frozen=True)
class RequestFeatures:
    """Operational features extracted from a raw service request."""

    issue_category: str
    urgency: float
    frustration: float
    complexity: float
    reasons: tuple[str, ...]


CATEGORY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "emergency",
        ("fire", "smoke", "gas leak", "gas smell", "carbon monoxide", "trapped"),
    ),
    (
        "air_conditioning",
        ("air con", "air-con", "air conditioner", "a/c", "ac broken", "ac not working"),
    ),
    ("water_leak", ("water leak", "leaking", "leak", "burst pipe", "flood", "dripping")),
    ("electrical", ("power", "electric", "socket", "outlet", "spark", "blackout")),
    ("noise_complaint", ("noise", "noisy", "loud music", "loud")),
    ("security", ("intruder", "theft", "stolen", "fight", "suspicious", "security")),
    ("lease_question", ("lease", "tenancy", "renewal", "renew my contract")),
    ("payment_question", ("rent", "invoice", "payment", "charge", "fee", "deposit")),
)

CATEGORY_COMPLEXITY = {
    "emergency": 9.0,
    "air_conditioning": 5.0,
    "water_leak": 6.0,
    "electrical": 6.0,
    "noise_complaint": 4.0,
    "security": 6.0,
    "lease_question": 4.0,
    "payment_question": 3.5,
    "general_request": 5.0,
}

EMERGENCY_TERMS = (
    "fire",
    "smoke",
    "gas leak",
    "gas smell",
    "carbon monoxide",
    "flooding",
    "injured",
    "injury",
    "trapped",
)
SAFETY_TERMS = ("danger", "unsafe", "slip", "fall", "sparks", "trapped")
TIME_PRESSURE_TERMS = ("urgent", "immediately", "right now", "as soon as possible", "asap")
RECURRENCE_TERMS = ("again", "still not", "third time", "second time", "keeps happening")
STRONG_COMPLAINT_TERMS = ("unacceptable", "angry", "furious", "ridiculous", "no one helped")
VULNERABILITY_TERMS = ("elderly", "wheelchair", "disabled", "small child", "baby")


def contains_term(text: str, term: str) -> bool:
    """Match a declared word/phrase without accepting substrings inside larger words."""

    escaped = re.escape(term)
    prefix = r"(?<!\w)" if term and term[0].isalnum() else ""
    suffix = r"(?!\w)" if term and term[-1].isalnum() else ""
    return re.search(prefix + escaped + suffix, text) is not None


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(contains_term(text, term) for term in terms)


def _cap(value: float) -> float:
    return round(min(10.0, max(0.0, value)), 1)


def _classify_issue(text: str) -> tuple[str, str]:
    for category, terms in CATEGORY_RULES:
        if contains_any(text, terms):
            return category, f"matched baseline issue taxonomy: {category}"
    return "general_request", "no baseline issue category matched"


class BaselineRequestIntelligence:
    """Transparent text-to-feature baseline for Phase 1.

    The scores are operational heuristics for software development. They are not
    psychological measurements and should not be treated as validated production scores.
    """

    def analyze(
        self,
        message: str,
        *,
        previous_related_cases: int = 0,
        vulnerability_flag: bool = False,
    ) -> RequestFeatures:
        text = " ".join(message.lower().split())
        if not text:
            raise ValueError("message must not be blank")
        if previous_related_cases < 0:
            raise ValueError("previous_related_cases must be non-negative")

        category, category_reason = _classify_issue(text)
        reasons = [category_reason]

        urgency = 3.0
        frustration = 3.0
        complexity = CATEGORY_COMPLEXITY[category]

        if contains_any(text, EMERGENCY_TERMS):
            urgency += 7.0
            reasons.append("emergency/safety term detected; immediate human triage required")
        if contains_any(text, SAFETY_TERMS):
            urgency += 2.0
            complexity += 1.0
            reasons.append("safety context detected")
        if contains_any(text, TIME_PRESSURE_TERMS):
            urgency += 1.5
            reasons.append("time-pressure language detected")

        if contains_any(text, RECURRENCE_TERMS):
            frustration += 2.0
            complexity += 0.5
            reasons.append("recurrence language detected")
        if previous_related_cases > 0:
            frustration += min(2.0, previous_related_cases * 0.7)
            complexity += min(1.5, previous_related_cases * 0.4)
            reasons.append("known related-case history included")

        if contains_any(text, STRONG_COMPLAINT_TERMS):
            frustration += 3.0
            reasons.append("strong complaint language detected")
        if "!" in message:
            frustration += min(1.0, message.count("!") * 0.25)
            reasons.append("message emphasis contributes to communication-intensity score")

        vulnerability_mentioned = contains_any(text, VULNERABILITY_TERMS)
        if vulnerability_flag or vulnerability_mentioned:
            urgency += 1.0
            complexity += 1.0
            reasons.append("vulnerability context requires additional human attention")

        return RequestFeatures(
            issue_category=category,
            urgency=_cap(urgency),
            frustration=_cap(frustration),
            complexity=_cap(complexity),
            reasons=tuple(reasons),
        )
