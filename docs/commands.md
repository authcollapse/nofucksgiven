# Commands

Run commands from the repository root after `make setup`.

## Fast

```bash
make check
```

This runs formatting checks, linting, claim scanning, Markdown link checks, and tests.

## Crypto Hygiene

```bash
.venv/bin/python scripts/check_claims.py
```

The claim scanner rejects risky phrases such as `unbreakable`, `production-ready`, `better than AES`, and similar wording unless the line is clearly marked as policy text. <!-- claim-ok: policy-text -->

## Benchmark Smoke

```bash
make bench-smoke
```

This validates benchmark plumbing for the library-backed AEAD baselines and the NFG-v0 experiment datasets. When you publish full benchmark results, include CPU, OS, Python version, dependency versions, iterations, payload sizes, dataset names, and date.

## NFG Focus

```bash
.venv/bin/python -m pytest tests/test_nfg_experiment.py tests/test_nfg_evaluation.py
.venv/bin/python benchmarks/bench_nfg.py --iterations 10 --datasets empty ascii deterministic-random-255
```

Use these when changing the NFG experiment. Passing them means local behavior
matched the current scaffold; it does not make NFG deployable.

## Docs Site

The public site is published by GitHub Actions from `main`. The generated `site/`
directory is a disposable build artifact and stays out of git.

## Before Push

- Make `make check` pass.
- Run `make bench-smoke` when benchmark code or docs changed.
- Write experiment caveats.
- Confirm the threat model is unchanged or update it.
- Keep benchmark language clear: performance numbers are not security claims.
