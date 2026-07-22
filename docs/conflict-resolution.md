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

## Resolution checklist

For each conflict:

1. record branch tips and conflicted paths;
2. explain the intent of each side;
3. edit a combined result rather than selecting a side blindly;
4. remove all conflict markers and run `git diff --check`;
5. run affected and full verification;
6. commit with two parents and preserve the hash in the evidence register.
