# VulnTrack API — Baumanka Findings API

[![CI](https://github.com/Argentum-Astrum/vulntrack-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Argentum-Astrum/vulntrack-api/actions/workflows/ci.yml)

VulnTrack is a compact REST API for registering, triaging, and reporting
information-security findings. It is the practical software product for the
postgraduate assignment **“Git, collaboration platforms, and CI/CD: the full
software-development process.”** The existing repository name is retained;
the assignment product is also referred to as **Baumanka Findings API**.

## Capabilities

- health check at `GET /health`;
- create, retrieve, list, update, and delete findings;
- validated severity, status, CVSS score, source, and required text fields;
- persistent SQLite storage behind a repository boundary;
- filtering by severity and status and aggregate severity statistics in v1.1;
- unit and integration tests with an enforced coverage threshold;
- reproducible format, lint, build, SAST, dependency, and secret checks;
- GitHub Actions and equivalent GitLab CI/CD definitions;
- versioned Git hooks and Semantic Versioning releases.

## Architecture

```text
HTTP client → FastAPI routes → Pydantic schemas → SQLite repository → SQLite
```

The application factory selects the database path, FastAPI owns the HTTP
contract, Pydantic validates data at the boundary, and
`SQLiteFindingRepository` owns parameterized persistence. See
[`docs/architecture.md`](docs/architecture.md) for decisions and limits.

## Requirements

- Python 3.12 (the package supports Python 3.11 or newer);
- Git;
- GNU Make for the shared convenience targets.

## Install

```bash
git clone https://github.com/Argentum-Astrum/vulntrack-api.git
cd vulntrack-api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

No token or credential is required to run the service locally. Do not commit
`.env` files or local SQLite databases.

## Run

```bash
VULNTRACK_DATABASE=./findings.sqlite3 \
  python -m uvicorn vulntrack.main:app --host 127.0.0.1 --port 8000
```

- Health: <http://127.0.0.1:8000/health>
- OpenAPI UI: <http://127.0.0.1:8000/docs>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

## API summary

| Method | Path | Result |
|---|---|---|
| `GET` | `/health` | service status |
| `POST` | `/findings` | create a finding (`201`) |
| `GET` | `/findings` | list and filter findings |
| `GET` | `/findings/{id}` | retrieve one finding |
| `PUT` | `/findings/{id}` | apply validated changes |
| `DELETE` | `/findings/{id}` | delete a finding (`204`) |
| `GET` | `/findings/statistics` | counts by severity (v1.1) |

Example create request:

```bash
curl --fail-with-body -X POST http://127.0.0.1:8000/findings \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Weak TLS configuration",
    "affected_asset": "gateway.example.test",
    "description": "A deprecated protocol is accepted.",
    "source": "configuration-audit",
    "severity": "medium",
    "cvss_score": 5.9
  }'
```

More examples are in [`docs/api.md`](docs/api.md).

## Verify locally

```bash
make format-check  # Ruff formatter check
make lint          # Ruff static lint
make unit          # focused unit suite
make integration   # HTTP + SQLite integration suite
make test          # full suite, JUnit, XML/HTML coverage, threshold
make build         # wheel and source distribution under dist/
make security      # Bandit, dependency audit, candidate-secret scan
make verify        # all mandatory local gates
```

Generated reports live under `reports/` and are ignored by Git.

## Install Git hooks

```bash
./scripts/install-hooks.sh
```

The versioned hooks run format/lint before commit, enforce Conventional
Commits in `commit-msg`, and run tests before push. Disable them with
`./scripts/install-hooks.sh --uninstall`. Hooks are advisory because
`--no-verify` can bypass them; CI repeats the mandatory gates.

## CI/CD

Both platform configurations call the same Make targets:

- [GitHub Actions workflow](.github/workflows/ci.yml);
- [GitLab CI/CD configuration](.gitlab-ci.yml).

The logical sequence is `lint → test → build → security → release`. Pull
requests, branches, `main`, and version tags are covered. CI publishes JUnit,
coverage, security, wheel, and source-distribution artifacts. Release runs only
for a `v*` tag or the documented release-commit context after earlier stages
succeed. See [`docs/ci-cd.md`](docs/ci-cd.md).

## Engineering and research documents

- [Contribution rules](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [Architecture](docs/architecture.md)
- [GitHub Flow](docs/git-workflow.md)
- [Conflict resolution](docs/conflict-resolution.md)
- [Platform comparison](docs/platform-comparison.md)
- [Evidence register](docs/evidence.md)
- [Assignment compliance](docs/assignment-compliance.md)
- [Full report](docs/report.md)

## Releases

- [v1.0.0](https://github.com/Argentum-Astrum/vulntrack-api/releases/tag/v1.0.0) — CRUD baseline;
- [v1.1.0](https://github.com/Argentum-Astrum/vulntrack-api/releases/tag/v1.1.0) — filtering, statistics, and completed research.

## License

[MIT](LICENSE). This permissive license was selected as the assignment's
explicit default assumption.
