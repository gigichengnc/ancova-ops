from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .models import RoutingDecision, ServiceCase

SCHEMA_VERSION = 1


class CaseConflictError(ValueError):
    """Raised when an existing case ID is reused with different original case data."""


@dataclass(slots=True, frozen=True)
class CaseOutcome:
    response_time_minutes: float | None = None
    resolution_time_minutes: float | None = None
    reassigned: bool | None = None
    escalated: bool | None = None
    satisfaction: float | None = None

    def __post_init__(self) -> None:
        for name in ("response_time_minutes", "resolution_time_minutes"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be non-negative")
        if self.satisfaction is not None and not 0 <= self.satisfaction <= 10:
            raise ValueError("satisfaction must be between 0 and 10")


@dataclass(slots=True, frozen=True)
class StoredRoutingDecision:
    decision_id: int
    created_at: str
    intelligence_version: str
    router_version: str
    decision: RoutingDecision


@dataclass(slots=True, frozen=True)
class StoredCase:
    case: ServiceCase
    created_at: str
    latest_decision: StoredRoutingDecision | None
    outcome: CaseOutcome | None


def default_database_path() -> str:
    """Return the configured local SQLite path.

    The default location is intentionally outside the tracked source tree and is
    ignored by Git. Set ANCOVA_OPS_DB_PATH to use a different database.
    """

    return os.environ.get("ANCOVA_OPS_DB_PATH", ".ancova_ops/ancova_ops.sqlite3")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


class SQLiteCaseStore:
    """Small SQLite persistence layer for Phase 1 service cases and audit history."""

    def __init__(self, database: str | Path) -> None:
        self.database = str(database)
        if self.database == ":memory:":
            raise ValueError("Use a file-backed SQLite database so audit data persists")
        Path(self.database).expanduser().parent.mkdir(parents=True, exist_ok=True)
        self.migrate()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def migrate(self) -> None:
        """Create or validate the current database schema.

        Phase 1 uses an explicit integer schema version. Future incompatible schema
        changes should add a migration step before incrementing SCHEMA_VERSION.
        """

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            row = connection.execute(
                "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
            ).fetchone()
            if row is None:
                connection.execute(
                    "INSERT INTO schema_metadata (key, value) VALUES ('schema_version', ?)",
                    (str(SCHEMA_VERSION),),
                )
            elif int(row["value"]) != SCHEMA_VERSION:
                raise RuntimeError(
                    "Unsupported database schema version "
                    f"{row['value']}; expected {SCHEMA_VERSION}"
                )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS service_cases (
                    case_id TEXT PRIMARY KEY,
                    message TEXT NOT NULL,
                    issue_category TEXT,
                    urgency REAL NOT NULL,
                    frustration REAL NOT NULL,
                    complexity REAL NOT NULL,
                    previous_related_cases INTEGER NOT NULL,
                    vulnerability_flag INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS routing_decisions (
                    decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    intelligence_version TEXT NOT NULL,
                    router_version TEXT NOT NULL,
                    department TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    requires_human_review INTEGER NOT NULL,
                    secondary_notify TEXT,
                    reasons_json TEXT NOT NULL,
                    FOREIGN KEY (case_id) REFERENCES service_cases(case_id)
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_routing_decisions_case_id
                ON routing_decisions(case_id, decision_id)
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS case_outcomes (
                    case_id TEXT PRIMARY KEY,
                    response_time_minutes REAL,
                    resolution_time_minutes REAL,
                    reassigned INTEGER,
                    escalated INTEGER,
                    satisfaction REAL,
                    observed_at TEXT NOT NULL,
                    FOREIGN KEY (case_id) REFERENCES service_cases(case_id)
                )
                """
            )

    @staticmethod
    def _case_values(case: ServiceCase) -> tuple[object, ...]:
        return (
            case.case_id,
            case.message,
            case.issue_category,
            case.urgency,
            case.frustration,
            case.complexity,
            case.previous_related_cases,
            int(case.vulnerability_flag),
        )

    @staticmethod
    def _row_matches_case(row: sqlite3.Row, case: ServiceCase) -> bool:
        return (
            row["case_id"] == case.case_id
            and row["message"] == case.message
            and row["issue_category"] == case.issue_category
            and row["urgency"] == case.urgency
            and row["frustration"] == case.frustration
            and row["complexity"] == case.complexity
            and row["previous_related_cases"] == case.previous_related_cases
            and bool(row["vulnerability_flag"]) is case.vulnerability_flag
        )

    def save_routed_case(
        self,
        case: ServiceCase,
        decision: RoutingDecision,
        *,
        intelligence_version: str,
        router_version: str,
        reasons: tuple[str, ...] | list[str] | None = None,
        created_at: str | None = None,
    ) -> int:
        """Persist a case and append an immutable routing-decision audit record."""

        timestamp = created_at or _utc_now()
        stored_reasons = tuple(reasons) if reasons is not None else decision.reasons

        with self._connect() as connection:
            existing = connection.execute(
                "SELECT * FROM service_cases WHERE case_id = ?", (case.case_id,)
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO service_cases (
                        case_id, message, issue_category, urgency, frustration, complexity,
                        previous_related_cases, vulnerability_flag, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (*self._case_values(case), timestamp),
                )
            elif not self._row_matches_case(existing, case):
                raise CaseConflictError(
                    f"case_id {case.case_id!r} already exists with different original data"
                )

            cursor = connection.execute(
                """
                INSERT INTO routing_decisions (
                    case_id, created_at, intelligence_version, router_version,
                    department, priority, requires_human_review, secondary_notify, reasons_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    case.case_id,
                    timestamp,
                    intelligence_version,
                    router_version,
                    decision.department,
                    decision.priority,
                    int(decision.requires_human_review),
                    decision.secondary_notify,
                    json.dumps(stored_reasons, ensure_ascii=False),
                ),
            )
            decision_id = cursor.lastrowid
            if decision_id is None:
                raise RuntimeError("SQLite did not return a routing decision ID")
            return int(decision_id)

    def save_outcome(
        self,
        case_id: str,
        outcome: CaseOutcome,
        *,
        observed_at: str | None = None,
    ) -> None:
        timestamp = observed_at or _utc_now()
        with self._connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM service_cases WHERE case_id = ?", (case_id,)
            ).fetchone()
            if exists is None:
                raise KeyError(case_id)
            connection.execute(
                """
                INSERT INTO case_outcomes (
                    case_id, response_time_minutes, resolution_time_minutes,
                    reassigned, escalated, satisfaction, observed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(case_id) DO UPDATE SET
                    response_time_minutes = excluded.response_time_minutes,
                    resolution_time_minutes = excluded.resolution_time_minutes,
                    reassigned = excluded.reassigned,
                    escalated = excluded.escalated,
                    satisfaction = excluded.satisfaction,
                    observed_at = excluded.observed_at
                """,
                (
                    case_id,
                    outcome.response_time_minutes,
                    outcome.resolution_time_minutes,
                    None if outcome.reassigned is None else int(outcome.reassigned),
                    None if outcome.escalated is None else int(outcome.escalated),
                    outcome.satisfaction,
                    timestamp,
                ),
            )

    def get_case(self, case_id: str) -> StoredCase | None:
        with self._connect() as connection:
            case_row = connection.execute(
                "SELECT * FROM service_cases WHERE case_id = ?", (case_id,)
            ).fetchone()
            if case_row is None:
                return None

            decision_row = connection.execute(
                """
                SELECT * FROM routing_decisions
                WHERE case_id = ?
                ORDER BY decision_id DESC
                LIMIT 1
                """,
                (case_id,),
            ).fetchone()
            outcome_row = connection.execute(
                "SELECT * FROM case_outcomes WHERE case_id = ?", (case_id,)
            ).fetchone()

        case = ServiceCase(
            case_id=case_row["case_id"],
            message=case_row["message"],
            issue_category=case_row["issue_category"],
            urgency=case_row["urgency"],
            frustration=case_row["frustration"],
            complexity=case_row["complexity"],
            previous_related_cases=case_row["previous_related_cases"],
            vulnerability_flag=bool(case_row["vulnerability_flag"]),
        )

        latest_decision = None
        if decision_row is not None:
            reasons = tuple(json.loads(decision_row["reasons_json"]))
            latest_decision = StoredRoutingDecision(
                decision_id=decision_row["decision_id"],
                created_at=decision_row["created_at"],
                intelligence_version=decision_row["intelligence_version"],
                router_version=decision_row["router_version"],
                decision=RoutingDecision(
                    department=decision_row["department"],
                    priority=decision_row["priority"],
                    requires_human_review=bool(decision_row["requires_human_review"]),
                    secondary_notify=decision_row["secondary_notify"],
                    reasons=reasons,
                ),
            )

        outcome = None
        if outcome_row is not None:
            outcome = CaseOutcome(
                response_time_minutes=outcome_row["response_time_minutes"],
                resolution_time_minutes=outcome_row["resolution_time_minutes"],
                reassigned=(
                    None if outcome_row["reassigned"] is None else bool(outcome_row["reassigned"])
                ),
                escalated=(
                    None if outcome_row["escalated"] is None else bool(outcome_row["escalated"])
                ),
                satisfaction=outcome_row["satisfaction"],
            )

        return StoredCase(
            case=case,
            created_at=case_row["created_at"],
            latest_decision=latest_decision,
            outcome=outcome,
        )

    def list_routing_decisions(self, case_id: str) -> list[StoredRoutingDecision]:
        """Return the full immutable routing audit history for a case."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM routing_decisions
                WHERE case_id = ?
                ORDER BY decision_id ASC
                """,
                (case_id,),
            ).fetchall()

        return [
            StoredRoutingDecision(
                decision_id=row["decision_id"],
                created_at=row["created_at"],
                intelligence_version=row["intelligence_version"],
                router_version=row["router_version"],
                decision=RoutingDecision(
                    department=row["department"],
                    priority=row["priority"],
                    requires_human_review=bool(row["requires_human_review"]),
                    secondary_notify=row["secondary_notify"],
                    reasons=tuple(json.loads(row["reasons_json"])),
                ),
            )
            for row in rows
        ]
