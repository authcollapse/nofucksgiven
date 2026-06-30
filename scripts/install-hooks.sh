#!/usr/bin/env sh
set -eu

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push .githooks/commit-msg
chmod +x scripts/check_claims.py scripts/check_internal_links.py

echo "Installed git hooks from .githooks"
