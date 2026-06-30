from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RISKY_WORD = "un" + "breakable"


def run_script(script: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script)],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def test_claim_scanner_rejects_unjustified_risky_claim(tmp_path: Path) -> None:
    (tmp_path / "claim.md").write_text(f"This toy cipher is {RISKY_WORD}.\n", encoding="utf-8")

    result = run_script("scripts/check_claims.py", tmp_path)

    assert result.returncode == 1
    assert RISKY_WORD in result.stdout


def test_claim_scanner_requires_concrete_claim_ok_reason(tmp_path: Path) -> None:
    (tmp_path / "claim.md").write_text(
        f"This documents the phrase {RISKY_WORD}. <!-- claim-ok: -->\n",
        encoding="utf-8",
    )

    result = run_script("scripts/check_claims.py", tmp_path)

    assert result.returncode == 1
    assert "claim-ok must be one of" in result.stdout


def test_claim_scanner_allows_justified_policy_examples(tmp_path: Path) -> None:
    (tmp_path / "claim.md").write_text(
        f"This documents the phrase {RISKY_WORD}. <!-- claim-ok: policy-example -->\n",
        encoding="utf-8",
    )

    result = run_script("scripts/check_claims.py", tmp_path)

    assert result.returncode == 0


def test_claim_scanner_ignores_fenced_examples(tmp_path: Path) -> None:
    (tmp_path / "claim.md").write_text(
        f"```text\nThis example says {RISKY_WORD}.\n```\n",
        encoding="utf-8",
    )

    result = run_script("scripts/check_claims.py", tmp_path)

    assert result.returncode == 0


def test_internal_link_checker_rejects_missing_file(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("[missing](docs/nope.md)\n", encoding="utf-8")

    result = run_script("scripts/check_internal_links.py", tmp_path)

    assert result.returncode == 1
    assert "docs/nope.md" in result.stdout


def test_internal_link_checker_rejects_missing_anchor(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "[bad anchor](doc.md#missing-section)\n",
        encoding="utf-8",
    )
    (tmp_path / "doc.md").write_text("# Existing Section\n", encoding="utf-8")

    result = run_script("scripts/check_internal_links.py", tmp_path)

    assert result.returncode == 1
    assert "missing-section" in result.stdout


def test_internal_link_checker_ignores_fenced_examples(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "```md\n[example](missing.md)\n```\n",
        encoding="utf-8",
    )

    result = run_script("scripts/check_internal_links.py", tmp_path)

    assert result.returncode == 0


def test_internal_link_checker_accepts_existing_anchor(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "[good anchor](doc.md#existing-section)\n",
        encoding="utf-8",
    )
    (tmp_path / "doc.md").write_text("# Existing Section\n", encoding="utf-8")

    result = run_script("scripts/check_internal_links.py", tmp_path)

    assert result.returncode == 0
