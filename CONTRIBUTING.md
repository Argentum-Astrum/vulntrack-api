# Contributing

## Workflow

This repository uses GitHub Flow. `main` is the only stable branch. Every
change starts from an issue, is implemented in a short-lived branch, passes CI,
and reaches `main` through a pull request.

1. Confirm or create an issue with context, scope, and acceptance criteria.
2. Update local `main` and create a branch named
   `<type>/<issue>-<short-description>`.
3. Install the project and hooks with `./scripts/install-hooks.sh`.
4. Make small, logically complete Conventional Commits.
5. Run `make verify` and push the branch.
6. Open a PR with `Closes #<issue>`, evidence, risks, and a checklist.
7. Address review with new commits; do not erase review history by force push.
8. Merge only after required checks and discussions are complete, then delete
   the short-lived branch.

Examples:

- `feat/26-filtering-statistics`
- `fix/18-request-validation`
- `ci/23-quality-pipeline`
- `docs/24-engineering-docs`

## Commit subjects

Use Conventional Commits 1.0.0:

```text
<type>[optional scope][!]: <imperative description>
```

Allowed types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `chore`, and `revert`. Keep the subject at most 72 characters.
Do not create empty commits or split a single trivial change merely to increase
the commit count.

## Pull request content

Every PR must include:

- issue closing link;
- goal and implementation summary;
- important changed paths;
- exact local verification result;
- CI result;
- risks and limitations;
- readiness checklist;
- reviewer when an independent collaborator is available.

Self-review comments must be labeled as self-review and are not independent
approval. Never create a fictitious reviewer.

## Review and merge

Use inline threads for line-specific feedback. Answer with the fixing commit
and resolve a thread only after the new CI run succeeds. Merge commits are used
for this research repository because they preserve PR and real conflict
topology. Direct and force pushes to `main` are process violations even where a
repository-plan or connector limitation prevents technical enforcement.

## Releases

Releases follow Semantic Versioning 2.0.0. Prepare the changelog and package
version in a PR; after merge, the release context creates the `vMAJOR.MINOR.PATCH`
tag and attaches the already verified build artifacts.
