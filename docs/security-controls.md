# Security controls and limits

The security stage combines three independent checks:

1. **Bandit** scans Python source for risky constructs and writes JSON.
2. **pip-audit** resolves the pinned runtime dependency roots in
   `requirements-audit.txt` and compares the closure with vulnerability data.
3. **detect-secrets** scans tracked content; `check_secret_report.py` converts
   any candidate into a failing gate and reports only file names and line
   numbers.

These checks are defense in depth, not proof that the application is free of
vulnerabilities. Candidate-secret detection can produce false positives, and a
clean dependency audit says only that the selected advisory service reported
no known issue for the resolved versions at scan time.

No report or baseline may contain real credentials. A false positive should be
removed by changing the fixture or using a narrowly documented inline pragma;
blindly accepting a repository-wide baseline is not the default process.

Local hooks provide early feedback, but `--no-verify` can bypass them. Required
controls therefore run again in CI.
