import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COMMIT_MSG_HOOK = ROOT / ".githooks" / "commit-msg"
SECRET_REPORT_CHECK = ROOT / "scripts" / "check_secret_report.py"


def run_commit_hook(subject: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(COMMIT_MSG_HOOK), "/dev/stdin"],
        input=f"{subject}\n",
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.mark.parametrize(
    "subject",
    [
        "feat(api): add statistics endpoint",
        "fix!: reject an incompatible request",
        "docs(git-workflow): explain branch deletion",
    ],
)
def test_commit_msg_accepts_conventional_subject(subject: str) -> None:
    assert run_commit_hook(subject).returncode == 0


@pytest.mark.parametrize(
    "subject",
    [
        "added a feature",
        "feature(api): wrong type",
        "feat(api) missing colon",
        "feat(API): uppercase scope",
    ],
)
def test_commit_msg_rejects_non_conventional_subject(subject: str) -> None:
    result = run_commit_hook(subject)

    assert result.returncode == 1
    assert "Expected Conventional Commits" in result.stderr


@pytest.mark.parametrize(
    "path",
    [
        ROOT / ".githooks" / "pre-commit",
        ROOT / ".githooks" / "commit-msg",
        ROOT / ".githooks" / "pre-push",
        ROOT / "scripts" / "install-hooks.sh",
    ],
)
def test_hook_scripts_are_executable(path: Path) -> None:
    assert os.access(path, os.X_OK)


def test_secret_report_check_accepts_empty_results(tmp_path: Path) -> None:
    report = tmp_path / "clean.json"
    report.write_text(json.dumps({"results": {}}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SECRET_REPORT_CHECK), str(report)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "no candidate secrets" in result.stdout


def test_secret_report_check_rejects_candidates(tmp_path: Path) -> None:
    report = tmp_path / "finding.json"
    report.write_text(
        json.dumps(
            {
                "results": {
                    "example.py": [
                        {"type": "Secret Keyword", "line_number": 7},
                    ]
                }
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SECRET_REPORT_CHECK), str(report)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "example.py: lines 7" in result.stderr
