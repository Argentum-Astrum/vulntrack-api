from pathlib import Path
from uuid import uuid4

import pytest

from vulntrack.domain import FindingStatus, Severity
from vulntrack.repository import SQLiteFindingRepository
from vulntrack.schemas import FindingCreate, FindingUpdate


@pytest.fixture
def repository(tmp_path: Path) -> SQLiteFindingRepository:
    return SQLiteFindingRepository(tmp_path / "findings.sqlite3")


def make_payload(**overrides: object) -> FindingCreate:
    values: dict[str, object] = {
        "title": "Reflected cross-site scripting",
        "affected_asset": "portal.example.test",
        "description": "Untrusted input is returned without output encoding.",
        "source": "manual-review",
        "severity": Severity.MEDIUM,
        "cvss_score": 6.1,
    }
    values.update(overrides)
    return FindingCreate.model_validate(values)


def test_create_assigns_identity_state_and_timestamps(
    repository: SQLiteFindingRepository,
) -> None:
    finding = repository.create(make_payload())

    assert finding.id
    assert finding.status is FindingStatus.NEW
    assert finding.created_at == finding.updated_at
    assert repository.get(finding.id) == finding


def test_get_returns_none_for_unknown_id(
    repository: SQLiteFindingRepository,
) -> None:
    assert repository.get(uuid4()) is None


def test_list_returns_findings_in_creation_order(
    repository: SQLiteFindingRepository,
) -> None:
    first = repository.create(make_payload(title="First finding"))
    second = repository.create(make_payload(title="Second finding"))

    assert [finding.id for finding in repository.list()] == [first.id, second.id]


def test_records_survive_repository_recreation(tmp_path: Path) -> None:
    database = tmp_path / "durable.sqlite3"
    created = SQLiteFindingRepository(database).create(make_payload())

    assert SQLiteFindingRepository(database).get(created.id) == created


def test_update_changes_selected_fields_only(
    repository: SQLiteFindingRepository,
) -> None:
    created = repository.create(make_payload())
    updated = repository.update(
        created.id,
        FindingUpdate(
            severity=Severity.HIGH,
            status=FindingStatus.CONFIRMED,
            source="automated-scanner",
        ),
    )

    assert updated is not None
    assert updated.title == created.title
    assert updated.created_at == created.created_at
    assert updated.severity is Severity.HIGH
    assert updated.status is FindingStatus.CONFIRMED
    assert updated.source == "automated-scanner"
    assert updated.updated_at >= created.updated_at


def test_update_returns_none_for_unknown_id(
    repository: SQLiteFindingRepository,
) -> None:
    result = repository.update(uuid4(), FindingUpdate(status=FindingStatus.RESOLVED))

    assert result is None


def test_delete_removes_existing_finding(
    repository: SQLiteFindingRepository,
) -> None:
    created = repository.create(make_payload())

    assert repository.delete(created.id) is True
    assert repository.get(created.id) is None


def test_delete_reports_missing_finding(
    repository: SQLiteFindingRepository,
) -> None:
    assert repository.delete(uuid4()) is False


def test_repository_stores_sql_metacharacters_as_data(
    repository: SQLiteFindingRepository,
) -> None:
    title = "'; DROP TABLE findings; --"

    created = repository.create(make_payload(title=title))

    assert repository.get(created.id).title == title  # type: ignore[union-attr]
    assert len(repository.list()) == 1
