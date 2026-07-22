from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from vulntrack.domain import FindingStatus, Severity
from vulntrack.schemas import FindingCreate, FindingRead, FindingUpdate


VALID_CREATE_PAYLOAD: dict[str, object] = {
    "title": "SQL injection in search endpoint",
    "affected_asset": "search-api.internal",
    "description": "Unsanitized input reaches a database query.",
    "source": "penetration-test",
    "severity": Severity.HIGH,
    "cvss_score": 8.1,
}


def make_finding_read(**overrides: object) -> FindingRead:
    """Build a valid response model and apply selected field overrides."""
    now = datetime.now(UTC)
    payload: dict[str, object] = {
        **VALID_CREATE_PAYLOAD,
        "id": uuid4(),
        "status": FindingStatus.NEW,
        "created_at": now,
        "updated_at": now,
    }
    payload.update(overrides)
    return FindingRead.model_validate(payload)


def test_finding_create_accepts_valid_payload() -> None:
    finding = FindingCreate.model_validate(VALID_CREATE_PAYLOAD)

    assert finding.title == "SQL injection in search endpoint"
    assert finding.source == "penetration-test"
    assert finding.severity is Severity.HIGH
    assert finding.cvss_score == 8.1


@pytest.mark.parametrize("severity", list(Severity))
def test_finding_create_accepts_supported_severity(severity: Severity) -> None:
    payload = {**VALID_CREATE_PAYLOAD, "severity": severity}

    assert FindingCreate.model_validate(payload).severity is severity


@pytest.mark.parametrize("status", list(FindingStatus))
def test_finding_read_accepts_supported_status(status: FindingStatus) -> None:
    assert make_finding_read(status=status).status is status


def test_finding_create_rejects_unknown_severity() -> None:
    payload = {**VALID_CREATE_PAYLOAD, "severity": "blocker"}

    with pytest.raises(ValidationError):
        FindingCreate.model_validate(payload)


def test_finding_read_rejects_unknown_status() -> None:
    with pytest.raises(ValidationError):
        make_finding_read(status="closed")


@pytest.mark.parametrize(
    "cvss_score",
    [-0.1, 10.1, float("inf"), float("nan")],
)
def test_finding_create_rejects_invalid_cvss_score(cvss_score: float) -> None:
    payload = {**VALID_CREATE_PAYLOAD, "cvss_score": cvss_score}

    with pytest.raises(ValidationError):
        FindingCreate.model_validate(payload)


def test_finding_create_strips_surrounding_whitespace() -> None:
    payload = {
        **VALID_CREATE_PAYLOAD,
        "title": "  SQL injection  ",
        "affected_asset": "  search-api.internal  ",
        "description": "  Unsanitized input  ",
    }

    finding = FindingCreate.model_validate(payload)

    assert finding.title == "SQL injection"
    assert finding.affected_asset == "search-api.internal"
    assert finding.description == "Unsanitized input"


def test_finding_create_rejects_short_title() -> None:
    payload = {**VALID_CREATE_PAYLOAD, "title": "ab"}

    with pytest.raises(ValidationError):
        FindingCreate.model_validate(payload)


def test_finding_create_rejects_blank_description() -> None:
    payload = {**VALID_CREATE_PAYLOAD, "description": "   "}

    with pytest.raises(ValidationError):
        FindingCreate.model_validate(payload)


def test_finding_create_rejects_blank_affected_asset() -> None:
    payload = {**VALID_CREATE_PAYLOAD, "affected_asset": "   "}

    with pytest.raises(ValidationError):
        FindingCreate.model_validate(payload)


def test_finding_create_rejects_blank_source() -> None:
    payload = {**VALID_CREATE_PAYLOAD, "source": "   "}

    with pytest.raises(ValidationError):
        FindingCreate.model_validate(payload)


def test_finding_update_accepts_selected_fields() -> None:
    update = FindingUpdate(status=FindingStatus.CONFIRMED, cvss_score=9.0)

    assert update.model_dump(exclude_unset=True) == {
        "status": FindingStatus.CONFIRMED,
        "cvss_score": 9.0,
    }


@pytest.mark.parametrize("payload", [{}, {"title": None}])
def test_finding_update_rejects_missing_values(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        FindingUpdate.model_validate(payload)


def test_finding_update_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        FindingUpdate.model_validate({"owner": "attacker-controlled"})


def test_finding_create_rejects_unexpected_fields() -> None:
    payload = {**VALID_CREATE_PAYLOAD, "unexpected": True}

    with pytest.raises(ValidationError):
        FindingCreate.model_validate(payload)


def test_finding_read_preserves_identity_and_timestamps() -> None:
    finding_id = uuid4()
    now = datetime.now(UTC)

    finding = make_finding_read(
        id=finding_id,
        created_at=now,
        updated_at=now,
    )

    assert finding.id == finding_id
    assert finding.created_at == now
    assert finding.updated_at == now
