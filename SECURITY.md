# Security policy

## Supported versions

| Version | Supported |
|---|---|
| Latest `1.1.x` | Yes |
| `1.0.x` | Security fixes until the assignment is accepted |
| `<1.0` | No |

## Report a vulnerability

Do not disclose exploit details, credentials, personal data, or private
addresses in a public issue. Prefer GitHub private vulnerability reporting when
it is enabled. Otherwise contact the maintainer through an existing private
channel and include the affected version, impact, minimal reproduction, and
suggested remediation.

The maintainer aims to acknowledge reports within seven calendar days and to
coordinate disclosure. Tool output is not proof of either vulnerability or
absence of vulnerabilities; findings receive human review.

## Baseline controls

The project uses input validation, parameterized SQL, unit and integration
tests, Ruff, Bandit, dependency auditing, secret detection, least-privilege CI
permissions, and release artifacts derived from a gated build.
