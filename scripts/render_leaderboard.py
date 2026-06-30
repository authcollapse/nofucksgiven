#!/usr/bin/env python3
"""Render the evidence leaderboard from structured data."""

from __future__ import annotations

import argparse
from pathlib import Path

from nofucksgiven.leaderboard import load_leaderboard, render_markdown, validate_leaderboard


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("docs/leaderboard.md"))
    args = parser.parse_args()

    payload, algorithms = load_leaderboard()
    findings = validate_leaderboard(payload["criteria"], algorithms)
    if findings:
        print("\n".join(findings))
        return 1

    args.output.write_text(render_markdown(payload["criteria"], algorithms), encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
