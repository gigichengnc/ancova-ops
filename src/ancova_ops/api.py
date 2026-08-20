from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from .intelligence import BaselineRequestIntelligence
from .models import ServiceCase
from .routing import baseline_route

app = FastAPI(
    title="ANCOVA Ops API",
    version="0.2.0",
    description="Structured service-request intelligence and explainable routing baseline.",
)

_intelligence = BaselineRequestIntelligence()


class RouteRequest(BaseModel):
    case_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=10_000)
    previous_related_cases: int = Field(default=0, ge=0, le=1000)
    vulnerability_flag: bool = False

    @field_validator("case_id", "message")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class RouteResponse(BaseModel):
    case_id: str
    issue_category: str
    urgency: float
    frustration: float
    complexity: float
    department: str
    priority: str
    requires_human_review: bool
    secondary_notify: str | None
    reasons: list[str]
    scoring_note: str = (
        "Phase 1 baseline scores are transparent operational heuristics, not psychological "
        "measurements or validated production risk scores."
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/route", response_model=RouteResponse)
def route_request(payload: RouteRequest) -> RouteResponse:
    features = _intelligence.analyze(
        payload.message,
        previous_related_cases=payload.previous_related_cases,
        vulnerability_flag=payload.vulnerability_flag,
    )

    case = ServiceCase(
        case_id=payload.case_id,
        message=payload.message,
        issue_category=features.issue_category,
        urgency=features.urgency,
        frustration=features.frustration,
        complexity=features.complexity,
        previous_related_cases=payload.previous_related_cases,
        vulnerability_flag=payload.vulnerability_flag,
    )
    decision = baseline_route(case)

    reasons = list(dict.fromkeys((*features.reasons, *decision.reasons)))
    return RouteResponse(
        case_id=case.case_id,
        issue_category=features.issue_category,
        urgency=features.urgency,
        frustration=features.frustration,
        complexity=features.complexity,
        department=decision.department,
        priority=decision.priority,
        requires_human_review=decision.requires_human_review,
        secondary_notify=decision.secondary_notify,
        reasons=reasons,
    )
