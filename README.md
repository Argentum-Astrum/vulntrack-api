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

## Run tests

`python -m pytest -q`

## Run lint

`python -m ruff check .`

## License

MIT
