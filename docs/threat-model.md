# Threat Model

Use this threat model to keep the current work bounded. Right now, we are
working on authenticated encryption with associated data for local experiments
only.

## In Scope

- Confidentiality and integrity checks for messages encrypted with AEAD baselines.
- Tamper detection through authentication tags.
- Correct handling of additional authenticated data.
- Repeatable tests and benchmarks for baseline comparison.

## Out of Scope

- Production deployment.
- Key exchange, password hashing, certificates, secure storage, and protocol design.
- Replacement claims about AES, ChaCha20-Poly1305, or Ascon.

## Assumptions

- Generate keys with a cryptographically secure random source.
- Never reuse a key and nonce pair.
- Install dependencies from trusted package indexes in a controlled environment.
