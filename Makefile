PYTHON ?= python
REPORT_DIR ?= reports
PIP_AUDIT_CACHE_DIR ?= $(REPORT_DIR)/.pip-audit-cache

.PHONY: security hooks-test

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
