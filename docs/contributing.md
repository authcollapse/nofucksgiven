# Contributing

Use this project to improve evidence, clarity, tests, benchmarks, and documentation.

Before committing:

```bash
make check
```

When benchmark code or benchmark docs change:

```bash
make bench-smoke
```

Install local git hooks:

```bash
scripts/install-hooks.sh
```

## Experiment Rules

- Put toy or experimental constructions under `experiments/`.
- Include a short `README.md` for each experiment with hypothesis, method, results, and caveats.
- Add fixed test vectors when behavior should be reproducible.
- Compare behavior against baseline AEAD wrappers before making performance statements.
- Keep security claims conservative. Tests and benchmarks do not prove a cipher is safe.
