# nofucksgiven

[![status](https://img.shields.io/badge/status-research-111827)](#status)
[![python](https://img.shields.io/badge/python-3.11%2B-3776AB)](pyproject.toml)
[![tests](https://img.shields.io/badge/tests-pytest-0A7BBB)](tests/)
[![benchmarks](https://img.shields.io/badge/benchmarks-AEAD-6B7280)](benchmarks/)

Research workspace for studying symmetric encryption and testing experimental ideas against established authenticated-encryption baselines.

This repo studies AEAD usage, benchmarks, and experiment discipline. It does not propose a replacement cipher.

This is not production cryptography. New constructions remain non-production unless they receive sustained external cryptanalysis, review, and adoption.

## Status

Current baseline layer:

| Area | What exists |
| --- | --- |
| Baselines | AES-GCM-256, ChaCha20-Poly1305 |
| Tests | Property tests, known-answer vectors, tamper checks, input validation, auth-failure checks |
| Benchmarks | CSV-style rows by algorithm, operation, payload size, and throughput |
| Docs | Threat model, roadmap, safety notes, reading list, experiment log |
| Production use | No. Research only. |

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Commands

Run these from the repository root after Quickstart.

| Task | Command |
| --- | --- |
| Run tests | `.venv/bin/python -m pytest` |
| Lint | `.venv/bin/ruff check .` |
| Format | `.venv/bin/ruff format .` |
| Benchmark smoke run | `.venv/bin/python benchmarks/bench_aead.py --iterations 10 --sizes 64 1024` |
| Default benchmark matrix | `.venv/bin/python benchmarks/bench_aead.py` |

See [CONTRIBUTING.md](CONTRIBUTING.md) for the local check and experiment workflow.

## Repo Map

```mermaid
flowchart TD
    README["README.md<br/>front door and commands"]
    SECURITY["SECURITY.md<br/>research-only warning"]
    PYPROJECT["pyproject.toml<br/>package and tooling"]

    SRC["src/nofucksgiven<br/>importable research code"]
    BASELINES["baselines.py<br/>AEAD registry and wrappers"]

    TESTS["tests<br/>correctness and misuse coverage"]
    TEST_BASE["test_baselines.py<br/>vectors, tamper, round trips"]
    TEST_BENCH["test_benchmarks.py<br/>benchmark smoke coverage"]

    BENCH["benchmarks<br/>performance harness"]
    BENCH_AEAD["bench_aead.py<br/>CSV benchmark matrix"]

    DOCS["docs<br/>research operating manual"]
    ROADMAP["roadmap.md<br/>staged research plan"]
    THREAT["threat-model.md<br/>scope and assumptions"]
    SAFETY["safety-notes.md<br/>rules for safe experiments"]
    READING["reading-list.md<br/>books, standards, resources"]
    LOG["experiment-log.md<br/>experiment template"]

    EXP["experiments<br/>future toy designs"]
    DATA["data<br/>future datasets and vectors"]

    README --> SRC
    README --> TESTS
    README --> BENCH
    README --> DOCS
    PYPROJECT --> SRC
    SECURITY --> DOCS

    SRC --> BASELINES
    TESTS --> TEST_BASE
    TESTS --> TEST_BENCH
    TEST_BASE --> BASELINES
    TEST_BENCH --> BENCH_AEAD
    BENCH --> BENCH_AEAD
    BENCH_AEAD --> BASELINES

    DOCS --> ROADMAP
    DOCS --> THREAT
    DOCS --> SAFETY
    DOCS --> READING
    DOCS --> LOG
    EXP --> LOG
    DATA --> TEST_BASE
```

For the expanded version, see [docs/repo-map.md](docs/repo-map.md).

## Baseline Example

```python
from nofucksgiven.baselines import AeadCipher

cipher = AeadCipher.new_aes_gcm()
message = b"research sample"
aad = b"context"

sealed = cipher.encrypt(message, aad)
opened = cipher.decrypt(sealed, aad)

assert opened == message
```

## Benchmark Output Shape

Example schema only, not measured results:

```text
algorithm,operation,payload_size,iterations,elapsed_ns,bytes_processed,mib_per_second
aes-gcm-256,encrypt,1024,1000,1234567,1024000,791.02
chacha20-poly1305,decrypt,1024,1000,1234567,1024000,791.02
```

Benchmark numbers are machine-local signals, not security claims.

## Research Flow

1. Study a known primitive or failure mode.
2. Add or import test vectors.
3. Write an isolated experiment under `experiments/`.
4. Compare behavior against `src/nofucksgiven/baselines.py`.
5. Record method, results, and caveats in `docs/experiment-log.md`.
6. Treat every original construction as broken until reviewed.

## Documentation

- [Repo map](docs/repo-map.md)
- [Research roadmap](docs/roadmap.md)
- [Threat model](docs/threat-model.md)
- [Safety notes](docs/safety-notes.md)
- [Reading list](docs/reading-list.md)
- [Experiment log template](docs/experiment-log.md)
- [Contributing](CONTRIBUTING.md)

## License

No open-source license has been selected yet. Until a license is added, reuse rights are not granted by default.
