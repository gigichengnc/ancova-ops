from __future__ import annotations

from dataclasses import dataclass, field


def _validate_score(name: str, value: float) -> None:
    if not 0 <= value <= 10:
        raise ValueError(f"{name} must be between 0 and 10")


@dataclass(slots=True)
class ServiceCase:
    """Structured representation of a service request.

    The numeric context fields are operational modelling inputs, not clinical or
    psychological measurements.
    """

    case_id: str
    message: str
    issue_category: str | None = None
    urgency: float = 5.0
    frustration: float = 5.0
    complexity: float = 5.0
    previous_related_cases: int = 0
    vulnerability_flag: bool = False

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must not be blank")
        if not self.message.strip():
            raise ValueError("message must not be blank")
        _validate_score("urgency", self.urgency)
        _validate_score("frustration", self.frustration)
        _validate_score("complexity", self.complexity)
        if self.previous_related_cases < 0:
            raise ValueError("previous_related_cases must be non-negative")


@dataclass(slots=True, frozen=True)
class RoutingDecision:
    department: str
    priority: str
    requires_human_review: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)
    secondary_notify: str | None = None
