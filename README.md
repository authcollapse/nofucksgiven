# nofucksgiven

[![status](https://img.shields.io/badge/status-research-111827)](#status)
[![python](https://img.shields.io/badge/python-3.11%2B-3776AB)](pyproject.toml)
[![tests](https://img.shields.io/badge/tests-pytest-0A7BBB)](tests/)
[![site](https://img.shields.io/badge/site-GitHub%20Pages-111827)](https://authcollapse.github.io/nofucksgiven/)

No fucks given to unsupported crypto claims.

`nofucksgiven` is an evidence-first workspace for learning how modern symmetric encryption is tested, benchmarked, documented, and challenged. The repo compares established authenticated-encryption baselines, tracks public evidence, and keeps experimental work clearly separated from real-world crypto.

This is research only. Do not use experimental code here to protect real data.

## Start Here

The readable docs site is the main entry point:

https://authcollapse.github.io/nofucksgiven/

It includes the evidence leaderboard, development map, roadmap, threat model, safety notes, commands, and contribution workflow.

## Current Baselines

- AES-GCM-256
- ChaCha20-Poly1305

The local test suite covers known-answer vectors, property tests, tamper rejection, wrong keys, wrong AAD, nonce validation, benchmark structure, docs links, and claim hygiene.

## Current Experiment

- NFG-v0 lives under `experiments/nfg/`.
- It is a toy symmetric encryption scaffold for datasets, vectors, misuse tests, and benchmark plumbing.
- It sits at #11 on the evidence leaderboard with score 12: cool lab toy, zero public-review swagger.
- It is not for real data.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make check
```

Useful commands:

```bash
make bench-smoke
make docs-build
make docs-serve
```

## Name

It is called `nofucksgiven` because the repo has no patience for crypto theater.

Benchmarks go in tables. Experiments go in the lab. Unsupported security claims go directly into the trash.

## License

Apache-2.0. See [LICENSE](LICENSE).

The license covers reuse terms. It does not make experimental cryptography safe for real data.
