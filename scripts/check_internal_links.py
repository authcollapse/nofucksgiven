#!/usr/bin/env python3
"""Check local Markdown links point to existing files."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(?P<title>.+?)\s*#*\s*$")
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
    ".hypothesis",
    "__pycache__",
    "site",
}


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


def slugify_heading(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"`([^`]*)`", r"\1", slug)
    slug = re.sub(r"[^a-z0-9 _-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug.strip("-")


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify_heading(match.group("title"))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def target_exists(source: Path, target: str) -> bool:
    path_part, _, anchor = unquote(target).partition("#")
    if not path_part:
        target_path = source
    else:
        target_path = (source.parent / path_part).resolve()
    if not target_path.exists():
        return False
    if anchor and target_path.suffix == ".md":
        return anchor in markdown_anchors(target_path)
    return True


def main() -> int:
    root = Path.cwd()
    findings: list[str] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        in_fence = False
        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                target = local_target(match.group(1))
                if target and not target_exists(path, target):
                    findings.append(f"{path}:{target}: local link target does not exist")
    if findings:
        print("\n".join(findings))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
