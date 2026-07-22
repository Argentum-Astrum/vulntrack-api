# CI/CD

## One command surface

GitHub and GitLab orchestration call the same Make targets. This keeps platform
YAML focused on triggers, stage ordering, reports, artifacts, and permissions
instead of duplicating product-specific shell commands.

| Stage | Command | Gate/output |
|---|---|---|
| lint | `make format-check lint` | Ruff format and static analysis |
| test | `make test` | pytest, JUnit, coverage XML/HTML, at least 80% |
| build | `make build` | wheel and source distribution |
| security | `make security` | Bandit, pip-audit, detect-secrets JSON |
| release | platform release operation | verified package from build stage |

Stages are sequential. Release depends on security, which depends on build,
which depends on test and lint. A failed earlier gate prevents a release.

## Triggers

GitHub Actions runs for:

- every branch push;
- pull-request open/update;
- `main` pushes;
- `v*` tags;
- manual `workflow_dispatch` diagnostics.

The release job is skipped unless the ref is a `v*` tag or `main` carries the
explicit documented `chore(release):` commit context. It has `contents: write`; every
other job keeps `contents: read`.

GitLab workflow rules cover merge-request pipelines, branch pipelines, and tag
pipelines. The release job has a tag-only rule and uses the current GitLab CLI
image. This configuration is equivalent source code, not evidence of execution
without a connected GitLab project and runner.

## Reports and artifacts

| Artifact | Contents | Retention |
|---|---|---:|
| quality reports | JUnit, Cobertura XML, HTML coverage | 14 days |
| Python package | wheel and source distribution | 30 days |
| security reports | Bandit, dependency, candidate-secret JSON | 14 days |
| GitLab release artifact | package copied into release job | 1 year |

Artifacts are diagnostic or release inputs; they are not committed. GitLab's
JUnit and Cobertura report keys allow native test and coverage presentation.
Bandit/pip-audit JSON remains a generic artifact rather than being mislabeled as
GitLab's native Ultimate-tier security-report schema.

## Reproducibility

- CPython is fixed to 3.12 in CI.
- Runtime dependency roots used by pip-audit are exact versions.
- Python tooling uses bounded version ranges.
- Official GitHub actions use current major releases at implementation time.
- Artifact names include `github.run_id`, preventing accidental cross-run reuse.

## Measured GitHub runs

Timestamps below were parsed from GitHub-hosted job logs. Queue is the observed
interval from PR creation to the first job log; total is through the last
mandatory job. It is a small experiment, not a global platform-speed claim.

| Run | Scenario | Queue | Lint | Test | Build | Security | Mandatory span |
|---|---|---:|---:|---:|---:|---:|---:|
| [#24](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883052726) | staged CI; first lint cache cold | ≈8 s | 18 s | 20 s | 24 s | 25 s | ≈103 s |
| [#27](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883765831) | secret/hooks extension; cache restored | ≈6 s | 29 s | 17 s | 19 s | 28 s | ≈109 s |
| [#30](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885192578) | docs/conflict PR; exact cache restored | ≈6 s | 13 s | 20 s | 20 s | 29 s | ≈99 s |
| **Median** | three GitHub PR runs | **≈6 s** | **18 s** | **20 s** | **20 s** | **28 s** | **≈103 s** |

Run #24's first job had no restore message and saved a new dependency key;
later jobs restored it. Runs #27 and #30 contain successful restore evidence,
and every job in #30 restored the exact same dependency key. All three runs
produced quality, package, and security artifacts and correctly skipped release
in a PR. The sample describes only this repository and runner image.

## Executed releases

| Version | Main workflow | Tag target | Release result |
|---|---|---|---|
| `v1.0.0` | [run 29885871737](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885871737) | `0ac42b2` | five jobs success; wheel + sdist published |
| `v1.1.0` | [run 29886550409](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29886550409) | `0b203d1` | five jobs success; wheel + sdist published |

In both cases the PR run skipped release, the Conventional
`chore(release):` merge triggered a new `main` run, and only that run granted
write permission to its final job. GitHub created the tag and Release after the
same run's package and security jobs succeeded.

## Local reproduction

```bash
python -m pip install -e ".[dev]"
make verify
```

To inspect an individual stage, run its target. Do not bypass a failed security
or test target to create a release.
