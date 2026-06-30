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

The claim scanner rejects risky phrases such as `unbreakable`, `production-ready`, `better than AES`, and similar wording unless the line includes `claim-ok:` with a concrete justification. <!-- claim-ok: this line documents blocked wording, not a repo claim -->

## Benchmark Smoke

```bash
make bench-smoke
```

This validates benchmark plumbing. When you publish full benchmark results, include CPU, OS, Python version, dependency versions, iterations, payload sizes, and date.

## Before Push

- Make `make check` pass.
- Run `make bench-smoke` when benchmark code or docs changed.
- Write experiment caveats.
- Confirm the threat model is unchanged or update it.
- Keep benchmark language clear: performance numbers are not security claims.
