#!/usr/bin/env sh
set -eu

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push .githooks/commit-msg
chmod +x .codex/hooks/*.py
chmod +x scripts/check_claims.py scripts/check_internal_links.py

echo "Installed git hooks from .githooks"
echo "Codex project hooks are configured in .codex/hooks.json"
echo "In Codex CLI, use /hooks to review and trust project-local hooks."
