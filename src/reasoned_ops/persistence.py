from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .models import RoutingDecision, ServiceCase

SCHEMA_VERSION = 2


class CaseConflictError(ValueError):
    """Raised when an existing case ID is reused with different original case data."""


class ReviewConflictError(ValueError):
    """Raised when a human review targets a stale routing recommendation."""


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
class StoredRoutingReview:
    review_id: int
    decision_id: int
    created_at: str
    actor_type: str
    actor_id: str
    action: str
    reason: str
    final_decision: RoutingDecision


@dataclass(slots=True, frozen=True)
class StoredCase:
    case: ServiceCase
    created_at: str
    latest_decision: StoredRoutingDecision | None
    latest_review: StoredRoutingReview | None
    outcome: CaseOutcome | None


def default_database_path() -> str:
    """Return the configured local SQLite path.

    The default location is intentionally outside the tracked source tree and is
    ignored by Git. Set ANCOVA_OPS_DB_PATH to use a different database.
    """

    return os.environ.get("ANCOVA_OPS_DB_PATH", ".ancova_ops/ancova_ops.sqlite3")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _decision_state(decision: RoutingDecision) -> tuple[object, ...]:
    return (
        decision.department,
        decision.priority,
        decision.requires_human_review,
        decision.secondary_notify,
    )


class SQLiteCaseStore:
    """SQLite persistence for service cases, machine decisions and human reviews."""

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

    @staticmethod
    def _ensure_base_schema(connection: sqlite3.Connection) -> None:
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
    def _ensure_review_schema(connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS routing_reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                decision_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                actor_type TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                action TEXT NOT NULL CHECK(action IN ('confirmed', 'overridden')),
                reason TEXT NOT NULL,
                final_department TEXT NOT NULL,
                final_priority TEXT NOT NULL,
                final_requires_human_review INTEGER NOT NULL,
                final_secondary_notify TEXT,
                FOREIGN KEY (case_id) REFERENCES service_cases(case_id),
                FOREIGN KEY (decision_id) REFERENCES routing_decisions(decision_id)
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_routing_reviews_case_id
            ON routing_reviews(case_id, review_id)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_routing_reviews_decision_id
            ON routing_reviews(decision_id, review_id)
            """
        )

    def migrate(self) -> None:
        """Create the latest schema and migrate supported older databases."""

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
            version = 1 if row is None else int(row["value"])
            if version > SCHEMA_VERSION:
                raise RuntimeError(
                    f"Unsupported database schema version {version}; expected <= {SCHEMA_VERSION}"
                )

            self._ensure_base_schema(connection)
            if row is None:
                connection.execute(
                    "INSERT INTO schema_metadata (key, value) VALUES ('schema_version', '1')"
                )

            if version < 2:
                self._ensure_review_schema(connection)
                connection.execute(
                    "UPDATE schema_metadata SET value = '2' WHERE key = 'schema_version'"
                )
                version = 2

            if version == 2:
                self._ensure_review_schema(connection)

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

    @staticmethod
    def _stored_decision(row: sqlite3.Row) -> StoredRoutingDecision:
        return StoredRoutingDecision(
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

    @staticmethod
    def _stored_review(row: sqlite3.Row) -> StoredRoutingReview:
        return StoredRoutingReview(
            review_id=row["review_id"],
            decision_id=row["decision_id"],
            created_at=row["created_at"],
            actor_type=row["actor_type"],
            actor_id=row["actor_id"],
            action=row["action"],
            reason=row["reason"],
            final_decision=RoutingDecision(
                department=row["final_department"],
                priority=row["final_priority"],
                requires_human_review=bool(row["final_requires_human_review"]),
                secondary_notify=row["final_secondary_notify"],
                reasons=(),
            ),
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
        """Persist a case and append an immutable machine/rule routing decision."""

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

    def save_routing_review(
        self,
        case_id: str,
        decision_id: int,
        final_decision: RoutingDecision,
        *,
        actor_id: str,
        reason: str,
        actor_type: str = "human_staff",
        created_at: str | None = None,
    ) -> StoredRoutingReview:
        """Append a human review while preserving the source machine recommendation."""

        actor_id = actor_id.strip()
        actor_type = actor_type.strip()
        reason = reason.strip()
        if not actor_id:
            raise ValueError("actor_id must not be blank")
        if not actor_type:
            raise ValueError("actor_type must not be blank")
        if not reason:
            raise ValueError("reason must not be blank")

        timestamp = created_at or _utc_now()
        with self._connect() as connection:
            case_exists = connection.execute(
                "SELECT 1 FROM service_cases WHERE case_id = ?", (case_id,)
            ).fetchone()
            if case_exists is None:
                raise KeyError(case_id)

            source_row = connection.execute(
                "SELECT * FROM routing_decisions WHERE decision_id = ? AND case_id = ?",
                (decision_id, case_id),
            ).fetchone()
            if source_row is None:
                raise KeyError(decision_id)

            latest_row = connection.execute(
                """
                SELECT * FROM routing_decisions
                WHERE case_id = ?
                ORDER BY decision_id DESC
                LIMIT 1
                """,
                (case_id,),
            ).fetchone()
            if latest_row is None or latest_row["decision_id"] != decision_id:
                raise ReviewConflictError(
                    "routing review must reference the latest machine/rule recommendation"
                )

            source = self._stored_decision(source_row).decision
            action = (
                "confirmed"
                if _decision_state(source) == _decision_state(final_decision)
                else "overridden"
            )
            cursor = connection.execute(
                """
                INSERT INTO routing_reviews (
                    case_id, decision_id, created_at, actor_type, actor_id, action, reason,
                    final_department, final_priority, final_requires_human_review,
                    final_secondary_notify
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    case_id,
                    decision_id,
                    timestamp,
                    actor_type,
                    actor_id,
                    action,
                    reason,
                    final_decision.department,
                    final_decision.priority,
                    int(final_decision.requires_human_review),
                    final_decision.secondary_notify,
                ),
            )
            review_id = cursor.lastrowid
            if review_id is None:
                raise RuntimeError("SQLite did not return a routing review ID")

        return StoredRoutingReview(
            review_id=int(review_id),
            decision_id=decision_id,
            created_at=timestamp,
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            reason=reason,
            final_decision=final_decision,
        )

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
            review_row = None
            if decision_row is not None:
                review_row = connection.execute(
                    """
                    SELECT * FROM routing_reviews
                    WHERE decision_id = ?
                    ORDER BY review_id DESC
                    LIMIT 1
                    """,
                    (decision_row["decision_id"],),
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

        latest_decision = None if decision_row is None else self._stored_decision(decision_row)
        latest_review = None if review_row is None else self._stored_review(review_row)

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
            latest_review=latest_review,
            outcome=outcome,
        )

    def list_routing_decisions(self, case_id: str) -> list[StoredRoutingDecision]:
        """Return the full immutable machine/rule routing audit history for a case."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM routing_decisions
                WHERE case_id = ?
                ORDER BY decision_id ASC
                """,
                (case_id,),
            ).fetchall()
        return [self._stored_decision(row) for row in rows]

    def list_routing_reviews(self, case_id: str) -> list[StoredRoutingReview]:
        """Return human confirmations and overrides in append-only order."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM routing_reviews
                WHERE case_id = ?
                ORDER BY review_id ASC
                """,
                (case_id,),
            ).fetchall()
        return [self._stored_review(row) for row in rows]
