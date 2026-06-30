# NFG Experiment

`NFG` is a nod to `nofucksgiven`. The attitude applies to sloppy crypto claims,
not to evidence.

## Status

NFG-v0 is a toy symmetric encryption experiment. Do not use it to protect real
data.

It is not a replacement for AES-GCM, ChaCha20-Poly1305, Ascon, or any standard
AEAD. Passing tests only shows expected behavior for tested cases. Benchmarks are
local implementation measurements, not security evidence.

The first version gives us a concrete thing to test:

- 32-byte key.
- 24-byte nonce.
- HMAC-SHA-256 key separation.
- HMAC-SHA-256 counter-mode keystream.
- Encrypt-then-MAC tag truncated to 16 bytes.

That is a research harness, not a public-security argument.

NFG-v1 is a speed-focused toy variant. It swaps the HMAC-SHA-256 subkey, stream,
and tag plumbing for keyed BLAKE2s plumbing while keeping the same broad
stream-style shape. It is also not for real data.

## Question

What can we learn from building a small stream-style construction, testing its
authentication behavior, and then deliberately demonstrating its misuse
failures?

## What We Test

- Deterministic local datasets in `datasets.py`.
- Dataset manifest in `corpus.json`.
- Fixed snapshot vector in `vectors.json`.
- Failure notes in `attacks.md`.
- Round trips across empty, text, structured, repeated, and seeded-random inputs.
- Wrong key, wrong AAD, nonce tampering, ciphertext tampering, and tag tampering.
- A nonce-reuse failure demo showing why stream-style reuse is dangerous.
- Bit-flip sensitivity checks for key, nonce, plaintext, and AAD changes.
- Snapshot vectors so accidental behavior changes are visible.
- NFG-v0 versus NFG-v1 benchmark comparison.

## Current Observations

- Key and nonce bit flips broadly change the sealed output in deterministic local checks.
- AAD bit flips change the tag, not the ciphertext body, which is expected for authenticated associated data.
- Plaintext bit flips change exactly one ciphertext-body bit before the tag is considered. That stream-style shape is simple and testable, but it is not a diffusion breakthrough.
- NFG-v1 should target a clearly stated improvement before changing code: misuse resistance, a better nonce story, a stronger construction argument, or a measured failure reduction.
- NFG-v1 currently targets performance only. It does not fix nonce reuse, replay, or the lack of public cryptanalysis.

## Caveats

- No public cryptanalysis.
- No proof.
- No side-channel review.
- No misuse-resistance claim.
- No production deployment story.
- No replay protection by itself.
- No forward secrecy after key compromise.

If it survives local tests, that only means it survived local tests.
