#!/usr/bin/env python3
"""Reject risky crypto claims unless explicitly justified."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


RISKY_PHRASES = (
    "unbreakable",
    "military-grade",
    "military grade",
    "production-ready",
    "production ready",
    "secure by default",
    "provably secure",
    "better than aes",
    "better than chacha",
    "better than ascon",
    "post-quantum secure",
    "drop-in replacement",
)

DEFAULT_SUFFIXES = {".md", ".py", ".toml", ".json"}
DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
    ".hypothesis",
    "__pycache__",
    "site",
}
EXCLUDED_FILES = {
    Path("scripts/check_claims.py"),
}
CLAIM_OK_RE = re.compile(
    r"claim-ok:\s*(policy-text|policy-example|blocked-wording-example)\b",
    re.IGNORECASE,
)


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        relative = path.relative_to(root)
        if relative in EXCLUDED_FILES:
            continue
        if path.is_file() and path.suffix in DEFAULT_SUFFIXES:
            files.append(path)
    return sorted(files)


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    in_fence = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        lowered = line.lower()
        has_claim_ok = "claim-ok:" in lowered
        for phrase in RISKY_PHRASES:
            if phrase in lowered:
                if has_claim_ok and CLAIM_OK_RE.search(line):
                    continue
                if has_claim_ok:
                    findings.append(
                        f"{path}:{number}: claim-ok must be one of "
                        "policy-text, policy-example, or blocked-wording-example"
                    )
                    break
                findings.append(f"{path}:{number}: risky crypto claim phrase: {phrase!r}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    findings = [finding for path in iter_files(args.root) for finding in scan_file(path)]
    if findings:
        print("\n".join(findings))
        print("\nUse narrower wording, or add 'claim-ok:' with a concrete justification.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
