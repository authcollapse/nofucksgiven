# nofucksgiven

No fucks given to unsupported crypto claims.

This project is a beginner-friendly, evidence-first workspace for learning how modern symmetric encryption is evaluated. You can use it to compare established authenticated-encryption baselines, run local tests, benchmark behavior, and document what the evidence actually says.

!!! warning "Research only"
    Do not use experimental code from this repo to protect real data. Local tests and benchmarks help you learn and compare behavior. They do not prove cryptographic security.

## What The Name Means

`nofucksgiven` is the attitude toward sloppy crypto work:

- No patience for magic claims.
- No pretending benchmarks prove security.
- No calling toy code deployable.
- No hiding misuse risks in footnotes.
- No replacing public cryptanalysis with vibes.

We do give a lot of attention to evidence: test vectors, tamper tests, misuse checks, benchmark context, clear threat models, and honest caveats.

## What You Can Do Here

| Goal | Where to start |
| --- | --- |
| See which algorithms have the strongest evidence profile | [Evidence Leaderboard](leaderboard.md) |
| Understand the research flow | [Development Map](development-map.md) |
| Learn the staged path from basics to experiments | [Research Roadmap](roadmap.md) |
| Understand what is in and out of scope | [Threat Model](threat-model.md) |
| Run the project locally | [Commands](commands.md) |

## Current Baselines

The current code wraps library-backed AEAD baselines:

- AES-GCM-256
- ChaCha20-Poly1305

The test suite checks known-answer vectors, round trips, wrong keys, wrong AAD, tampering, nonce-size validation, benchmark structure, and docs/claim hygiene.

## Evidence Leaderboard Preview

This is an evidence-confidence snapshot, not a proof of security.

| Rank | Algorithm | Score | Role | Main caution |
| ---: | --- | ---: | --- | --- |
| 1 | AES-GCM-256 | 94 | Baseline AEAD | Nonce reuse with the same key is catastrophic |
| 2 | AES-GCM-SIV | 91 | Misuse-resistant AEAD | Not implemented locally yet |
| 3 | ChaCha20-Poly1305 | 88 | Baseline AEAD | Nonce reuse with the same key is unsafe |
| 4 | Ascon-AEAD128 | 85 | Lightweight AEAD | Newer standard than AES and ChaCha20-Poly1305 |
| 5 | XChaCha20-Poly1305 | 83 | Extended-nonce AEAD | Not a NIST standard |

Open the full [Evidence Leaderboard](leaderboard.md) for legacy algorithms, source tags, and scoring criteria.

## Local Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make check
```

For benchmark plumbing:

```bash
make bench-smoke
```

## How To Read The Results

Use the repo like a lab notebook:

1. Start with a narrow question.
2. Study the known baseline.
3. Add vectors and tests.
4. Run local benchmarks only after correctness checks pass.
5. Record method, results, and caveats.
6. Treat every original construction as broken until outside review says otherwise.
