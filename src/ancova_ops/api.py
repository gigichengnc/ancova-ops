from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from .intelligence import INTELLIGENCE_VERSION, BaselineRequestIntelligence
from .models import ServiceCase
from .persistence import (
    CaseConflictError,
    CaseOutcome,
    SQLiteCaseStore,
    StoredRoutingDecision,
    default_database_path,
)
from .routing import ROUTER_VERSION, baseline_route

app = FastAPI(
    title="ANCOVA Ops API",
    version="0.3.0",
    description="Structured service-request intelligence, explainable routing and audit persistence.",
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
    decision_id: int
    issue_category: str
    urgency: float
    frustration: float
    complexity: float
    department: str
    priority: str
    requires_human_review: bool
    secondary_notify: str | None
    reasons: list[str]
    intelligence_version: str
    router_version: str
    scoring_note: str = (
        "Phase 1 baseline scores are transparent operational heuristics, not psychological "
        "measurements or validated production risk scores."
    )


class RoutingAuditResponse(BaseModel):
    decision_id: int
    created_at: str
    intelligence_version: str
    router_version: str
    department: str
    priority: str
    requires_human_review: bool
    secondary_notify: str | None
    reasons: list[str]


class OutcomeRequest(BaseModel):
    response_time_minutes: float | None = Field(default=None, ge=0)
    resolution_time_minutes: float | None = Field(default=None, ge=0)
    reassigned: bool | None = None
    escalated: bool | None = None
    satisfaction: float | None = Field(default=None, ge=0, le=10)


class OutcomeResponse(OutcomeRequest):
    case_id: str


class CaseRecordResponse(BaseModel):
    case_id: str
    message: str
    issue_category: str | None
    urgency: float
    frustration: float
    complexity: float
    previous_related_cases: int
    vulnerability_flag: bool
    created_at: str
    latest_decision: RoutingAuditResponse | None
    outcome: OutcomeResponse | None


def _store() -> SQLiteCaseStore:
    return SQLiteCaseStore(default_database_path())


def _audit_response(stored: StoredRoutingDecision) -> RoutingAuditResponse:
    return RoutingAuditResponse(
        decision_id=stored.decision_id,
        created_at=stored.created_at,
        intelligence_version=stored.intelligence_version,
        router_version=stored.router_version,
        department=stored.decision.department,
        priority=stored.decision.priority,
        requires_human_review=stored.decision.requires_human_review,
        secondary_notify=stored.decision.secondary_notify,
        reasons=list(stored.decision.reasons),
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
    try:
        decision_id = _store().save_routed_case(
            case,
            decision,
            intelligence_version=INTELLIGENCE_VERSION,
            router_version=ROUTER_VERSION,
            reasons=reasons,
        )
    except CaseConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return RouteResponse(
        case_id=case.case_id,
        decision_id=decision_id,
        issue_category=features.issue_category,
        urgency=features.urgency,
        frustration=features.frustration,
        complexity=features.complexity,
        department=decision.department,
        priority=decision.priority,
        requires_human_review=decision.requires_human_review,
        secondary_notify=decision.secondary_notify,
        reasons=reasons,
        intelligence_version=INTELLIGENCE_VERSION,
        router_version=ROUTER_VERSION,
    )


@app.get("/v1/cases/{case_id}", response_model=CaseRecordResponse)
def get_case(case_id: str) -> CaseRecordResponse:
    stored = _store().get_case(case_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="case not found")

    outcome = None
    if stored.outcome is not None:
        outcome = OutcomeResponse(
            case_id=stored.case.case_id,
            response_time_minutes=stored.outcome.response_time_minutes,
            resolution_time_minutes=stored.outcome.resolution_time_minutes,
            reassigned=stored.outcome.reassigned,
            escalated=stored.outcome.escalated,
            satisfaction=stored.outcome.satisfaction,
        )

    return CaseRecordResponse(
        case_id=stored.case.case_id,
        message=stored.case.message,
        issue_category=stored.case.issue_category,
        urgency=stored.case.urgency,
        frustration=stored.case.frustration,
        complexity=stored.case.complexity,
        previous_related_cases=stored.case.previous_related_cases,
        vulnerability_flag=stored.case.vulnerability_flag,
        created_at=stored.created_at,
        latest_decision=(
            None if stored.latest_decision is None else _audit_response(stored.latest_decision)
        ),
        outcome=outcome,
    )


@app.get("/v1/cases/{case_id}/routing-decisions", response_model=list[RoutingAuditResponse])
def get_routing_audit(case_id: str) -> list[RoutingAuditResponse]:
    store = _store()
    if store.get_case(case_id) is None:
        raise HTTPException(status_code=404, detail="case not found")
    return [_audit_response(item) for item in store.list_routing_decisions(case_id)]


@app.put("/v1/cases/{case_id}/outcome", response_model=OutcomeResponse)
def put_case_outcome(case_id: str, payload: OutcomeRequest) -> OutcomeResponse:
    outcome = CaseOutcome(
        response_time_minutes=payload.response_time_minutes,
        resolution_time_minutes=payload.resolution_time_minutes,
        reassigned=payload.reassigned,
        escalated=payload.escalated,
        satisfaction=payload.satisfaction,
    )
    try:
        _store().save_outcome(case_id, outcome)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="case not found") from exc

    return OutcomeResponse(case_id=case_id, **payload.model_dump())
