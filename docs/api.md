# Findings API

Start the service with an explicit local database:

```bash
VULNTRACK_DATABASE=./findings.sqlite3 \
  python -m uvicorn vulntrack.main:app --reload
```

The interactive OpenAPI UI is available at `http://127.0.0.1:8000/docs`.

## Register a finding

```bash
curl --fail-with-body -X POST http://127.0.0.1:8000/findings \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Weak TLS configuration",
    "affected_asset": "gateway.example.test",
    "description": "The endpoint accepts a deprecated protocol version.",
    "source": "configuration-audit",
    "severity": "medium",
    "cvss_score": 5.9
  }'
```

The response includes a UUID, the initial `new` status, and UTC timestamps.

## Read findings

```bash
curl --fail-with-body http://127.0.0.1:8000/findings
curl --fail-with-body http://127.0.0.1:8000/findings/FINDING_UUID
```

## Update triage state

`PUT` accepts one or more fields and rejects an empty object.

```bash
curl --fail-with-body -X PUT \
  http://127.0.0.1:8000/findings/FINDING_UUID \
  -H 'Content-Type: application/json' \
  -d '{"status": "confirmed", "severity": "high"}'
```

## Delete a finding

```bash
curl --fail-with-body -X DELETE \
  http://127.0.0.1:8000/findings/FINDING_UUID
```

Successful deletion returns `204 No Content`. A valid but unknown UUID returns
`404`; malformed UUIDs and invalid request fields return `422`.
