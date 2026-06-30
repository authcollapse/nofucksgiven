# Contributing

Use this repo for cryptography research and learning. Your changes should improve clarity, repeatability, or evidence. Do not present experimental code as deployable encryption.

## Local Checks

Run these before committing:

```bash
make check
```

Optional benchmark plumbing check:

```bash
make bench-smoke
```

Format Python changes with:

```bash
.venv/bin/ruff format .
```

Install local git hooks with:

```bash
scripts/install-hooks.sh
```

See [docs/commands.md](docs/commands.md) for the command tiers and pre-push checklist.

## Experiment Rules

- Put toy or experimental constructions under `experiments/`.
- Include a short `README.md` for each experiment with the hypothesis, method, and caveats.
- Add fixed test vectors when behavior should be reproducible.
- Compare against the baseline AEAD wrappers before making performance claims.
- Keep security claims conservative. Benchmarks and tests do not prove a cipher is secure.

## Commit Shape

Prefer small commits with one purpose:

- Docs-only improvements.
- Test or benchmark improvements.
- One experimental prototype at a time.
- One baseline wrapper or algorithm registry change at a time.
