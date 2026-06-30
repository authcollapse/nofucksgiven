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

This validates benchmark plumbing. When you publish full benchmark results, include CPU, OS, Python version, dependency versions, iterations, payload sizes, and date.

## Docs Site

Build the GitHub Pages site locally:

```bash
make docs-build
```

Preview it while editing:

```bash
make docs-serve
```

The public site is published by GitHub Actions from `main`.

## Before Push

- Make `make check` pass.
- Run `make bench-smoke` when benchmark code or docs changed.
- Write experiment caveats.
- Confirm the threat model is unchanged or update it.
- Keep benchmark language clear: performance numbers are not security claims.
