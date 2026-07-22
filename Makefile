PYTHON ?= python
REPORT_DIR ?= reports
PIP_AUDIT_CACHE_DIR ?= $(REPORT_DIR)/.pip-audit-cache

.PHONY: format format-check lint unit integration test build security verify

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

format-check:
	$(PYTHON) -m ruff format --check .

lint:
	$(PYTHON) -m ruff check .

unit:
	$(PYTHON) -m pytest tests/unit tests/test_health.py -q

integration:
	$(PYTHON) -m pytest tests/integration -q

test:
	mkdir -p $(REPORT_DIR)
	$(PYTHON) -m pytest \
		--junitxml=$(REPORT_DIR)/junit.xml \
		--cov=vulntrack \
		--cov-report=term-missing \
		--cov-report=xml:$(REPORT_DIR)/coverage.xml \
		--cov-report=html:$(REPORT_DIR)/htmlcov \
		--cov-fail-under=80

build:
	$(PYTHON) -m build

security:
	mkdir -p $(REPORT_DIR)
	$(PYTHON) -m bandit -r src -f json -o $(REPORT_DIR)/bandit.json
	$(PYTHON) -m pip_audit \
		--cache-dir $(PIP_AUDIT_CACHE_DIR) \
		--requirement requirements-audit.txt \
		--format json \
		--output $(REPORT_DIR)/pip-audit.json

verify: format-check lint test build security
