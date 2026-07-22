#!/usr/bin/env python3
"""Fail when a detect-secrets JSON report contains candidate credentials."""

import json
from pathlib import Path
import sys


def main(report_path: str) -> int:
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    findings = {
        path: candidates
        for path, candidates in report.get("results", {}).items()
        if candidates
    }
    if not findings:
        print("detect-secrets: no candidate secrets found")
        return 0

    print("detect-secrets: candidate secrets require review", file=sys.stderr)
    for path, candidates in findings.items():
        lines = ", ".join(str(item.get("line_number", "?")) for item in candidates)
        print(f"- {path}: lines {lines}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_secret_report.py REPORT.json")
    raise SystemExit(main(sys.argv[1]))
