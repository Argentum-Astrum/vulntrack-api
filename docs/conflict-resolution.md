# Merge conflict evidence

The conflicts in this project came from parallel, useful work. No branch was
changed merely to manufacture conflict markers, and `main` was never broken.

## Conflict 1 — CI orchestration versus security/hooks

### Cause

Branches `ci/23-quality-pipeline` and `security/22-local-controls` started at
main commit `486a32c`. The CI branch added shared tooling and documentation;
the security branch independently added secret checks, hooks, and their local
commands.

After PR #32 merged, updating the security branch with main produced:

```text
CONFLICT (add/add): Merge conflict in Makefile
CONFLICT (content): Merge conflict in README.md
CONFLICT (content): Merge conflict in pyproject.toml
CONFLICT (add/add): Merge conflict in requirements-audit.txt
```

### Resolution

- `Makefile`: retained lint/test/build targets and appended secret and hook
  checks; `verify` depends on all of them.
- `pyproject.toml`: retained bounded quality dependencies and added
  detect-secrets.
- `README.md`: retained CI stages and added hook installation/disclosure.
- `requirements-audit.txt`: retained the explanatory isolated-audit comments
  and exact runtime roots.
- Ruff then normalized imports introduced under the new lint configuration.

Local verification after resolution: 58 tests, 97.39% branch coverage, Ruff,
package build, and hook syntax. GitHub Actions
[#27](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883765831)
verified the complete result including detect-secrets.

### Proof

- local resolution commit: `71175f7`;
- remote resolution commit: [`11144a7`](https://github.com/Argentum-Astrum/vulntrack-api/commit/11144a73413125cf83296347320739f7163b3c67);
- first parent: `09238aa` (security branch);
- second parent: `a8cebc4` (main after CI PR);
- implementing PR: [#33](https://github.com/Argentum-Astrum/vulntrack-api/pull/33).

## Conflict 2 — engineering documentation versus security baseline

### Cause

Branch `docs/24-engineering-docs` started at `486a32c` while the CI and
security branches continued independently. The docs branch rewrote the project
guide and added a release-oriented security policy. Meanwhile PR #33 added
tested hooks, concrete security commands, and a pre-release disclosure policy.

Synchronizing docs tip `6f430a3` with main `7d17523` produced:

```text
CONFLICT (content): Merge conflict in README.md
CONFLICT (add/add): Merge conflict in SECURITY.md
```

### Resolution

- `README.md`: retained the fuller installation, API, documentation, and
  release guide; integrated the executed hooks/security workflow and added the
  unexecuted Bitbucket portability reference.
- `SECURITY.md`: replaced contradictory version tables with one policy valid
  before and after tagging, retained the explicit statement that repository
  settings are separate evidence, and combined all tested baseline controls.

No side was selected wholesale. Conflict markers were removed manually and
`git diff --check` passed. Local verification after resolution: 58 tests,
97.39% branch coverage, Ruff format/lint, package build, Bandit, hook syntax,
and YAML parsing for all three platform configurations. The PR pipeline is the
authoritative verification for the dependency and secret audits.

### Proof

- local two-parent resolution commit: `98bc6a7`;
- first parent: `6f430a3` (docs branch);
- second parent: `7d17523` (main after security/hooks PR);
- remote two-parent resolution commit: [`9142801`](https://github.com/Argentum-Astrum/vulntrack-api/commit/91428014ae234bcf9da0ab1afa2594c13514a945);
- implementing PR: [#34](https://github.com/Argentum-Astrum/vulntrack-api/pull/34).

## Resolution checklist

For each conflict:

1. record branch tips and conflicted paths;
2. explain the intent of each side;
3. edit a combined result rather than selecting a side blindly;
4. remove all conflict markers and run `git diff --check`;
5. run affected and full verification;
6. commit with two parents and preserve the hash in the evidence register.
