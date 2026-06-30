#!/usr/bin/env python3
"""Check local Markdown links point to existing files."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EXCLUDED_DIRS = {".git", ".venv", ".pytest_cache", ".ruff_cache", ".hypothesis", "__pycache__"}


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if path.is_file() and not any(part in EXCLUDED_DIRS for part in path.parts)
    )


def local_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    if " " in target and not target.startswith("<"):
        return target.split(" ", 1)[0]
    return target.strip("<>")


def target_exists(source: Path, target: str) -> bool:
    path_part = unquote(target.split("#", 1)[0])
    if not path_part:
        return True
    return (source.parent / path_part).resolve().exists()


def main() -> int:
    root = Path.cwd()
    findings: list[str] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = local_target(match.group(1))
            if target and not target_exists(path, target):
                findings.append(f"{path}:{target}: local link target does not exist")
    if findings:
        print("\n".join(findings))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
