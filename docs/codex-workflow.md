# Codex Workflow

Use these Codex and git hooks to keep our research work consistent.

## Surfaces

| Surface | File | Purpose |
| --- | --- | --- |
| Repo instructions | [AGENTS.md](https://github.com/authcollapse/nofucksgiven/blob/main/AGENTS.md) | Tell Codex how we work in this repo. |
| Project config | [.codex/config.toml](https://github.com/authcollapse/nofucksgiven/blob/main/.codex/config.toml) | Enable project-local Codex hooks after you trust the repo. |
| Codex hooks | [.codex/hooks.json](https://github.com/authcollapse/nofucksgiven/blob/main/.codex/hooks.json) | Run lightweight prompt, edit, and stop checks during Codex sessions. |
| Git hooks | [.githooks/](https://github.com/authcollapse/nofucksgiven/tree/main/.githooks) | Run local checks before you commit and push. |
| Commands | [Makefile](https://github.com/authcollapse/nofucksgiven/blob/main/Makefile) | Give you one command surface for setup, tests, linting, formatting, and benchmark smoke runs. |
| Claim scanner | [scripts/check_claims.py](https://github.com/authcollapse/nofucksgiven/blob/main/scripts/check_claims.py) | Catches risky crypto wording unless you justify it. |

## Install Local Git Hooks

```bash
scripts/install-hooks.sh
```

That sets:

```bash
git config core.hooksPath .githooks
```

## Codex Hook Trust

Codex project hooks load only after you trust the project `.codex/` layer. In the Codex CLI, use:

```text
/hooks
```

Review the hook definitions and trust them when they match the checked-in files.

## Standard Checks

```bash
make check
make bench-smoke
```

## What The Hooks Enforce

- Warn you when prompt wording implies unsafe crypto claims or includes secret-looking text.
- Remind Codex to align source changes with tests.
- Remind Codex to align benchmark changes with benchmark tests.
- Remind Codex to document experiments with hypothesis, method, results, and caveats.
- Block commits and pushes when formatting, linting, claim scanning, docs links, or tests fail.

Codex hooks advise. Git hooks enforce.
