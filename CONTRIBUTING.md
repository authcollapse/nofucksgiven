# Contributing

This repository is for cryptography research and learning. Contributions should improve clarity, repeatability, or evidence. Do not submit experimental code as production-ready encryption.

## Local Checks

Run these before committing:

```bash
.venv/bin/python -m pytest
.venv/bin/ruff check .
```

Optional benchmark plumbing check:

```bash
.venv/bin/python benchmarks/bench_aead.py --iterations 10 --sizes 64 1024
```

Format Python changes with:

```bash
.venv/bin/ruff format .
```

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
