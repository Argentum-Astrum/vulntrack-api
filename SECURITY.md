# Security policy

## Supported versions

| Version | Support status |
|---|---|
| Default branch before `v1.0.0` | Best-effort security fixes |
| Latest tagged minor release | Supported |
| Older minor releases | Not supported after a newer minor is published |

This table describes an educational project, not a commercial support
commitment. It is updated when the release policy changes.

## Reporting a vulnerability

Do not open a public issue containing an exploit, credential, private address,
personal data, or an unredacted production log.

1. Use GitHub's **Report a vulnerability** option on the Security tab if it is
   available for the repository.
2. If private vulnerability reporting is unavailable, contact the repository
   owner through an already established private channel before disclosure.
3. Include the affected version, impact, reproducible steps, and a minimal
   proof-of-concept with all secrets and personal data removed.

The maintainer aims to acknowledge a report within seven calendar days, agree
on a disclosure timeline, and credit the reporter unless anonymity is
requested. This document does not claim that GitHub private vulnerability
reporting is enabled; repository settings are separate evidence.

## Baseline controls

- Pydantic rejects malformed and unexpected request fields.
- SQLite statements use parameters and static identifiers.
- Ruff, unit tests, and integration tests run locally and in CI.
- Bandit performs source analysis.
- pip-audit checks the pinned runtime dependency closure.
- detect-secrets blocks candidate credentials in tracked content.
- GitHub Actions uses read-only repository permissions except for the release
  job, and release artifacts come from the gated build.

Tool output is not proof of either a vulnerability or the absence of
vulnerabilities. Findings require human review.
