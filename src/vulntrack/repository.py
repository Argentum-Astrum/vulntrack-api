from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
import sqlite3
from uuid import UUID, uuid4

from vulntrack.domain import FindingStatus
from vulntrack.schemas import FindingCreate, FindingRead


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

    def list(self) -> list[FindingRead]:
        """Return findings from oldest to newest."""
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT * FROM findings ORDER BY created_at, id"
            ).fetchall()
        return [self._to_finding(row) for row in rows]
