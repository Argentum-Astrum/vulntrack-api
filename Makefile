PYTHON ?= python
REPORT_DIR ?= reports
PIP_AUDIT_CACHE_DIR ?= $(REPORT_DIR)/.pip-audit-cache

.PHONY: format format-check lint unit integration test build security hooks-test verify

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
	$(PYTHON) -m detect_secrets scan \
		--all-files \
		--exclude-files '(^|/)(\.git|\.venv|build|dist|htmlcov|reports)/' \
		> $(REPORT_DIR)/detect-secrets.json
	$(PYTHON) scripts/check_secret_report.py $(REPORT_DIR)/detect-secrets.json

hooks-test:
	sh -n .githooks/pre-commit
	sh -n .githooks/commit-msg
	sh -n .githooks/pre-push

verify: format-check lint test build security hooks-test
