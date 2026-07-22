from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from vulntrack.main import create_app

VALID_PAYLOAD: dict[str, object] = {
    "title": "Insecure direct object reference",
    "affected_asset": "billing-api.example.test",
    "description": "A user can retrieve another account's invoices.",
    "source": "integration-test",
    "severity": "high",
    "cvss_score": 8.2,
}


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    with TestClient(create_app(tmp_path / "api.sqlite3")) as test_client:
        yield test_client


def create_finding(client: TestClient, **overrides: object) -> dict[str, object]:
    response = client.post("/findings", json={**VALID_PAYLOAD, **overrides})
    assert response.status_code == 201
    return response.json()


def test_create_get_and_list_finding(client: TestClient) -> None:
    created = create_finding(client)

    retrieved = client.get(f"/findings/{created['id']}")
    listing = client.get("/findings")

    assert retrieved.status_code == 200
    assert retrieved.json() == created
    assert listing.status_code == 200
    assert listing.json() == [created]
    assert created["status"] == "new"


def test_update_persists_selected_changes(client: TestClient) -> None:
    created = create_finding(client)

    response = client.put(
        f"/findings/{created['id']}",
        json={"status": "confirmed", "severity": "critical", "cvss_score": 9.8},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"
    assert response.json()["severity"] == "critical"
    assert response.json()["title"] == created["title"]
    assert client.get(f"/findings/{created['id']}").json() == response.json()


def test_delete_removes_finding(client: TestClient) -> None:
    created = create_finding(client)

    response = client.delete(f"/findings/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/findings/{created['id']}").status_code == 404


@pytest.mark.parametrize(
    "override",
    [
        {"severity": "blocker"},
        {"title": "  "},
        {"source": "  "},
    ],
)
def test_create_rejects_invalid_payloads(
    client: TestClient,
    override: dict[str, object],
) -> None:
    response = client.post("/findings", json={**VALID_PAYLOAD, **override})

    assert response.status_code == 422


def test_update_rejects_invalid_status(client: TestClient) -> None:
    created = create_finding(client)

    response = client.put(
        f"/findings/{created['id']}",
        json={"status": "archived"},
    )

    assert response.status_code == 422
    assert client.get(f"/findings/{created['id']}").json()["status"] == "new"


def test_missing_and_malformed_identifiers_are_distinct(client: TestClient) -> None:
    assert client.get(f"/findings/{uuid4()}").status_code == 404
    assert client.get("/findings/not-a-uuid").status_code == 422


def test_empty_update_is_rejected(client: TestClient) -> None:
    created = create_finding(client)

    response = client.put(f"/findings/{created['id']}", json={})

    assert response.status_code == 422


def test_list_filters_by_severity_and_status(client: TestClient) -> None:
    create_finding(client, title="Low finding", severity="low", cvss_score=2.1)
    confirmed = create_finding(
        client,
        title="Confirmed high finding",
        severity="high",
    )
    client.put(f"/findings/{confirmed['id']}", json={"status": "confirmed"})

    severity_response = client.get("/findings", params={"severity": "high"})
    status_response = client.get("/findings", params={"status": "confirmed"})
    combined_response = client.get(
        "/findings",
        params={"severity": "low", "status": "confirmed"},
    )

    assert [item["id"] for item in severity_response.json()] == [confirmed["id"]]
    assert status_response.json()[0]["id"] == confirmed["id"]
    assert combined_response.json() == []


@pytest.mark.parametrize(
    ("parameter", "value"),
    [("severity", "blocker"), ("status", "archived")],
)
def test_list_rejects_invalid_filters(
    client: TestClient,
    parameter: str,
    value: str,
) -> None:
    response = client.get("/findings", params={parameter: value})

    assert response.status_code == 422


def test_statistics_report_all_severity_categories(client: TestClient) -> None:
    create_finding(client, title="Low finding", severity="low", cvss_score=2.1)
    create_finding(
        client, title="Critical finding", severity="critical", cvss_score=9.8
    )

    response = client.get("/findings/statistics")

    assert response.status_code == 200
    assert response.json() == {
        "total": 2,
        "by_severity": {"low": 1, "medium": 0, "high": 0, "critical": 1},
    }
