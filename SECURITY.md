# Security policy

## Supported versions

| Version | Support status |
|---|---|
| Default branch before v1.0.0 | Security fixes only |
| Older snapshots | Not supported |

This table is updated when a tagged release is published. Only the latest
minor release receives fixes in this educational project.

## Reporting a vulnerability

Do not open a public issue containing an exploit, credential, private address,
or personal data.

1. Use GitHub's **Report a vulnerability** option on the Security tab if it is
   available for the repository.
2. If private vulnerability reporting is unavailable, contact the repository
   owner through an already established private channel before disclosure.
3. Include affected version, impact, reproducible steps, and a minimal
   proof-of-concept with all secrets and personal data removed.

The maintainer should acknowledge a report within seven calendar days, agree
on a disclosure timeline, and credit the reporter unless anonymity is
requested. This document does not claim that GitHub private vulnerability
reporting is enabled; repository settings are evidence separately.

## Baseline controls

- Pydantic rejects malformed and unexpected request fields.
- SQLite statements use parameters and static identifiers.
- Ruff and tests run locally and in CI.
- Bandit performs source analysis.
- pip-audit checks the pinned runtime dependency closure.
- detect-secrets blocks candidate credentials in tracked content.
- Build and security reports are retained as CI artifacts.
