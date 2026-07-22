import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from vulntrack.domain import FindingStatus, Severity
from vulntrack.schemas import (
    FindingCreate,
    FindingRead,
    FindingStatistics,
    FindingUpdate,
)


class SQLiteFindingRepository:
    """Persist findings in a small, local SQLite database."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)
        self._initialize_schema()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize_schema(self) -> None:
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS findings (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    affected_asset TEXT NOT NULL,
                    description TEXT NOT NULL,
                    source TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL,
                    cvss_score REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    @staticmethod
    def _to_finding(row: sqlite3.Row) -> FindingRead:
        return FindingRead.model_validate(dict(row))

    def create(self, payload: FindingCreate) -> FindingRead:
        """Store and return a new finding."""
        now = datetime.now(UTC)
        finding = FindingRead(
            **payload.model_dump(),
            id=uuid4(),
            status=FindingStatus.NEW,
            created_at=now,
            updated_at=now,
        )
        values = finding.model_dump(mode="json")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO findings (
                    id, title, affected_asset, description, source, severity,
                    status, cvss_score, created_at, updated_at
                ) VALUES (
                    :id, :title, :affected_asset, :description, :source,
                    :severity, :status, :cvss_score, :created_at, :updated_at
                )
                """,
                values,
            )
        return finding

    def get(self, finding_id: UUID) -> FindingRead | None:
        """Return one finding or None when it does not exist."""
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM findings WHERE id = ?",
                (str(finding_id),),
            ).fetchone()
        return self._to_finding(row) if row is not None else None

    def list(
        self,
        severity: Severity | None = None,
        status: FindingStatus | None = None,
    ) -> list[FindingRead]:
        """Return optionally filtered findings from oldest to newest."""
        severity_value = severity.value if severity is not None else None
        status_value = status.value if status is not None else None
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM findings
                WHERE (? IS NULL OR severity = ?)
                  AND (? IS NULL OR status = ?)
                ORDER BY created_at, id
                """,
                (severity_value, severity_value, status_value, status_value),
            ).fetchall()
        return [self._to_finding(row) for row in rows]

    def statistics(self) -> FindingStatistics:
        """Return total findings and a complete severity breakdown."""
        counts = {severity: 0 for severity in Severity}
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT severity, COUNT(*) AS finding_count
                FROM findings
                GROUP BY severity
                """
            ).fetchall()
        for row in rows:
            counts[Severity(row["severity"])] = int(row["finding_count"])
        return FindingStatistics(total=sum(counts.values()), by_severity=counts)

    def update(
        self,
        finding_id: UUID,
        payload: FindingUpdate,
    ) -> FindingRead | None:
        """Apply a validated partial update and return the current record."""
        current = self.get(finding_id)
        if current is None:
            return None

        changes = payload.model_dump(exclude_unset=True)
        updated = current.model_copy(
            update={**changes, "updated_at": datetime.now(UTC)}
        )
        values = updated.model_dump(mode="json")
        with self._connection() as connection:
            connection.execute(
                """
                UPDATE findings SET
                    title = :title,
                    affected_asset = :affected_asset,
                    description = :description,
                    source = :source,
                    severity = :severity,
                    status = :status,
                    cvss_score = :cvss_score,
                    updated_at = :updated_at
                WHERE id = :id
                """,
                values,
            )
        return self.get(finding_id)

    def delete(self, finding_id: UUID) -> bool:
        """Delete one finding and report whether a row was removed."""
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM findings WHERE id = ?",
                (str(finding_id),),
            )
        return cursor.rowcount == 1
