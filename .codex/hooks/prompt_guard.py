#!/usr/bin/env python3
"""Warn Codex when prompt wording risks crypto overclaiming or secret exposure."""

from __future__ import annotations

import json
import sys


RISKY_CRYPTO_CLAIMS = (
    "unbreakable",
    "military grade",
    "military-grade",
    "better than aes",
    "better than chacha",
    "production ready",
    "production-ready",
)
SECRET_HINTS = (
    "api_key",
    "apikey",
    "private key",
    "secret_access_key",
    "github_pat",
    "ghp_",
)


def read_payload() -> str:
    raw = sys.stdin.read()
    if not raw:
        return ""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    return json.dumps(payload, sort_keys=True).lower()


def main() -> int:
    text = read_payload().lower()
    warnings: list[str] = []

    if any(term in text for term in RISKY_CRYPTO_CLAIMS):
        warnings.append(
            "Crypto-safety reminder: avoid replacement or production-security claims "
            "without a written model, cryptanalysis, and independent review."
        )
    if any(term in text for term in SECRET_HINTS):
        warnings.append(
            "Secret-safety reminder: do not paste tokens, private keys, or credentials."
        )

    if warnings:
        print("\n".join(warnings), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
