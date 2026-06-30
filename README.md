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

The name is about discipline, not apathy:

- No unsupported security claims.
- No pretending benchmarks prove cryptographic safety.
- No hiding misuse risks.
- No calling toy experiments deployable.
- No replacing public cryptanalysis with vibes.

We do care about test vectors, threat models, public sources, reproducible experiments, and honest caveats.

## License

Apache-2.0. See [LICENSE](LICENSE).

The license covers reuse terms. It does not make experimental cryptography safe for real data.
