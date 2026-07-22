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

## Local verification and hooks

Run the automated suite:

`python -m pytest -q`

Run source, dependency, and candidate-secret checks:

`make security`

Enable the versioned hooks for this clone:

`./scripts/install-hooks.sh`

The hooks check formatting and lint before commit, enforce Conventional Commits
subjects, and run tests before push. CI remains authoritative because local
hooks can be bypassed. Disable them with:

`./scripts/install-hooks.sh --uninstall`

## Security reporting

Do not place exploit details or credentials in a public issue. Follow
[`SECURITY.md`](SECURITY.md) for supported versions and coordinated disclosure.

## License

MIT
