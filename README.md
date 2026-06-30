# nofucksgiven

Research workspace for studying modern symmetric encryption and evaluating experimental ideas against established authenticated-encryption baselines.

This repository is not production cryptography. Anything experimental here should be treated as unsafe until it has a clear security model, public analysis, high-quality tests, benchmark evidence, and independent cryptographic review.

## Initial Scope

- Study existing AEAD designs such as AES-GCM, ChaCha20-Poly1305, and Ascon.
- Build repeatable tests and benchmarks around vetted library implementations.
- Keep experiment notes tied to hypotheses, parameters, results, and caveats.
- Avoid presenting new constructions as replacements for established standards.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

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

## Project Layout

- `src/nofucksgiven/`: importable experiment support code.
- `tests/`: correctness, misuse, and tamper-detection tests.
- `benchmarks/`: local benchmark scripts.
- `docs/`: threat model, safety notes, and experiment log template.
