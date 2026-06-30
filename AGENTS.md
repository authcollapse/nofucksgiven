# AGENTS.md

## Repository Purpose

This is a cryptography research workspace, not a production encryption library.
Treat every new construction as experimental and unsafe unless the repository
contains a written security model, test vectors, benchmark context,
cryptanalysis notes, and independent review evidence.

Do not use unsupported replacement or security marketing language for
experimental code. If you need to discuss banned phrases, keep that discussion
clearly labeled as policy text. <!-- claim-ok: this describes wording policy -->

## Working Rules

- Prefer small, reviewable changes.
- Keep code, tests, benchmarks, and docs in sync.
- Do not overclaim. Tests and benchmarks are evidence, not proof of security.
- Benchmark claims may support "faster/slower on this machine," never "more secure."
- Use established library-backed baselines before adding experimental code.
- Put toy or experimental constructions under `experiments/`.
- Record experimental assumptions and caveats in docs or experiment-local notes.
- Reuse existing subagents when delegation is useful:
  - Mimir: crypto research, safety, and credibility review.
  - Runar: repo structure, test, benchmark, and documentation review.

## Verification

Run from the repository root:

```bash
make check
```

For benchmark plumbing:

```bash
make bench-smoke
```

## Required Updates By Change Type

- Public API or baseline wrapper change: update tests and README/docs if behavior changes.
- Benchmark change: update `tests/test_benchmarks.py` and command docs.
- Experiment change: include hypothesis, method, results, and caveats.
- Security/safety wording change: keep `SECURITY.md`, `docs/safety-notes.md`, and README aligned.
- New primitive or wrapper: include known-answer tests, tamper tests, wrong-AAD tests,
  wrong-key tests, nonce-size tests, and round-trip property tests.
- Benchmark claim: include CPU, OS, Python version, dependency versions,
  iterations, payload sizes, and date.

## Commit Guidance

- Commit only source, docs, tests, and intentional config.
- Do not commit `.venv/`, caches, generated egg-info, benchmark output dumps, or secrets.
- Before pushing, verify `git status --short` is clean after checks.
