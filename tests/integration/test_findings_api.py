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
