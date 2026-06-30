#!/usr/bin/env python3
"""Print a compact final-state reminder when a Codex turn stops."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    status = subprocess.run(
        ["git", "status", "--short"],
        check=False,
        text=True,
        capture_output=True,
    )
    if status.returncode != 0:
        return 0
    changed = [line for line in status.stdout.splitlines() if line.strip()]
    if changed:
        print(
            f"Repo state reminder: {len(changed)} changed path(s). "
            "Run make check before commit/push when code or benchmark behavior changed.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
