# VulnTrack API

Educational API for registering, triaging and tracking vulnerability findings.

## Requirements

- Python 3.11 or newer
- Git

## Local setup

Create a virtual environment:

`python3 -m venv .venv`

Activate it:

`source .venv/bin/activate`

Install the project and development dependencies:

`python -m pip install -e ".[dev]"`

## Run the application

`python -m uvicorn vulntrack.main:app --host 127.0.0.1 --port 8000`

Health endpoint:

`GET http://127.0.0.1:8000/health`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## Local quality gates

The same Make targets are used locally, by GitHub Actions, and by the GitLab CI
configuration:

```bash
make format-check
make lint
make test
make build
make security
```

`make test` writes JUnit, coverage XML, and HTML coverage reports under
`reports/` and enforces at least 80% coverage. `make security` runs Bandit and
audits the pinned runtime dependency roots. Generated reports and packages are
not committed.

## CI/CD

The staged pipelines run `lint → test → build → security → release`. GitHub
Actions executes on pushes, pull requests, version tags, and manual dispatch.
The equivalent GitLab configuration uses the same Make targets. Build and
machine-readable report artifacts are retained by each platform; release jobs
run only in the documented release context.

## License

MIT
