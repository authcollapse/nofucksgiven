#!/usr/bin/env python3
"""Emit targeted reminders after edits so Codex keeps repo surfaces aligned."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def changed_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    files: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        files.append(line[3:].strip())
    return files


def main() -> int:
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    files = changed_files(root)
    if not files:
        return 0

    reminders: list[str] = []
    if any(path.startswith("src/") for path in files) and not any(
        path.startswith("tests/") for path in files
    ):
        reminders.append(
            "Source changed without tests. Add or update focused tests before finishing."
        )
    if (
        any(path.startswith("benchmarks/") for path in files)
        and "tests/test_benchmarks.py" not in files
    ):
        reminders.append(
            "Benchmark code changed. Update benchmark smoke tests if behavior changed."
        )
    if any(path.startswith("experiments/") for path in files) and not any(
        path.startswith("docs/") for path in files
    ):
        reminders.append(
            "Experiment files changed. Capture hypothesis, method, results, and caveats."
        )
    if "README.md" in files and "docs/development-map.md" not in files:
        reminders.append(
            "README changed. Check whether docs/development-map.md needs to stay aligned."
        )

    if reminders:
        print("\n".join(reminders), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
