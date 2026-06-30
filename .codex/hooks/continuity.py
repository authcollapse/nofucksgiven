#!/usr/bin/env python3
"""Persist local continuity notes around Codex compaction events."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


NOTES_DIR = Path(".codex/session-notes")
LATEST_NOTE = NOTES_DIR / "latest.md"
EVENT_LOG = NOTES_DIR / "events.jsonl"


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_stdin_payload() -> tuple[str, Any | None]:
    raw = sys.stdin.read()
    if not raw:
        return "", None
    try:
        return raw, json.loads(raw)
    except json.JSONDecodeError:
        return raw, None


def compact_payload(payload: Any | None) -> str:
    if payload is None:
        return "No structured hook payload was provided."
    if isinstance(payload, dict):
        lines = []
        for key in sorted(payload):
            value = payload[key]
            if isinstance(value, str):
                snippet = value[:500].replace("\n", " ")
                lines.append(f"- `{key}`: {snippet}")
            elif isinstance(value, (int, float, bool)) or value is None:
                lines.append(f"- `{key}`: {value}")
            else:
                lines.append(f"- `{key}`: {type(value).__name__}")
        return "\n".join(lines) if lines else "Empty structured hook payload."
    return f"Payload type: {type(payload).__name__}"


def write_event(event: str, raw: str, payload: Any | None) -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": now_iso(),
        "event": event,
        "branch": run_git(["branch", "--show-current"]),
        "head": run_git(["rev-parse", "--short", "HEAD"]),
        "payload": payload,
        "raw": raw if payload is None else None,
    }
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def write_latest_note(event: str, raw: str, payload: Any | None) -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    status = run_git(["status", "--short"])
    recent_commits = run_git(["log", "--oneline", "-5"])
    branch = run_git(["branch", "--show-current"]) or "unknown"
    head = run_git(["rev-parse", "--short", "HEAD"]) or "unknown"
    changed_paths = status if status else "clean"

    LATEST_NOTE.write_text(
        "\n".join(
            [
                "# Codex Continuity Note",
                "",
                f"- Saved: {now_iso()}",
                f"- Event: {event}",
                f"- Branch: {branch}",
                f"- HEAD: {head}",
                "",
                "## Resume Intent",
                "",
                "Continue from the current repository state. Prefer the repo docs, tests,",
                "git history, and this note over memory when reconstructing context.",
                "",
                "## Working Tree",
                "",
                "```text",
                changed_paths,
                "```",
                "",
                "## Recent Commits",
                "",
                "```text",
                recent_commits or "No commits found.",
                "```",
                "",
                "## Hook Payload Summary",
                "",
                compact_payload(payload),
                "",
                "## Raw Payload",
                "",
                "Raw hook payloads are stored in `.codex/session-notes/events.jsonl`.",
                "This directory is gitignored and should stay local.",
                "",
                f"- Raw bytes captured: {len(raw.encode('utf-8'))}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def session_start() -> int:
    if LATEST_NOTE.exists():
        print(f"Continuity note available: {LATEST_NOTE}", file=sys.stderr)
        print(LATEST_NOTE.read_text(encoding="utf-8")[:4000], file=sys.stderr)
    return 0


def save_event(event: str) -> int:
    raw, payload = read_stdin_payload()
    write_event(event, raw, payload)
    write_latest_note(event, raw, payload)
    print(f"Saved continuity note: {LATEST_NOTE}", file=sys.stderr)
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: continuity.py session-start|pre-compact|post-compact", file=sys.stderr)
        return 2

    command = sys.argv[1]
    if command == "session-start":
        return session_start()
    if command in {"pre-compact", "post-compact"}:
        return save_event(command)

    print(f"unknown continuity command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
