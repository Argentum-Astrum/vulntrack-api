#!/bin/sh
set -eu

repository_root="$(git rev-parse --show-toplevel)"
cd "${repository_root}"

if [ "${1:-}" = "--uninstall" ]; then
  git config --unset-all core.hooksPath 2>/dev/null || true
  printf '%s\n' "Git hooks disabled for ${repository_root}"
  exit 0
fi

chmod +x .githooks/pre-commit .githooks/commit-msg .githooks/pre-push
git config core.hooksPath .githooks

configured_path="$(git config --get core.hooksPath)"
if [ "${configured_path}" != ".githooks" ]; then
  printf '%s\n' "Unable to configure core.hooksPath" >&2
  exit 1
fi

printf '%s\n' "Git hooks enabled from ${repository_root}/.githooks"
