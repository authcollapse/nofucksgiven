# Research Roadmap

You should not trust encryption algorithms because they look complex
or feel novel. They earn trust through years of public cryptanalysis, formal
models, side-channel review, high-quality implementations, and real deployment.

Use this repo to learn, reproduce, measure, and document. Start any original
design as a toy construction, and treat it as broken until serious evidence says
otherwise.

## Stage 1: Foundations

- Study symmetric encryption, authenticated encryption, hashing, MACs, key
  derivation, elliptic-curve cryptography, and post-quantum basics.
- Work through known attacks before attempting new designs.
- Reproduce failures such as stream-cipher nonce reuse, padding oracles, and
  GCM nonce reuse in isolated toy code.

## Stage 2: Baselines

Use library-backed implementations as comparison points:

- AES-GCM.
- ChaCha20-Poly1305.
- AES-GCM-SIV for nonce-misuse-resistance study.
- Ascon for lightweight authenticated encryption study.

## Stage 3: Evaluation

Evaluate every serious experiment against:

- Security model: IND-CPA, IND-CCA, AEAD security, and misuse assumptions.
- Cryptanalysis: differential, linear, algebraic, rotational, related-key,
  meet-in-the-middle, and slide attacks.
- Side-channel behavior: timing, cache behavior, power/fault resistance, and
  constant-time implementation feasibility.
- Performance: throughput, latency, memory, SIMD, embedded targets, and hardware.
- Simplicity: small specification, clean test vectors, and minimal attack surface.
- Composability: safe use inside larger protocols.

## Stage 4: Toy Designs

Start with intentionally small primitives. Write a specification, generate test
vectors, benchmark it, and then try to break it. A broken toy design is useful
when it teaches you something concrete.

## Stage 5: External Review

Do not claim production security from local tests. Before you make a credible
security claim, you need a clear specification, public cryptanalysis, proofs
where applicable, test vectors, constant-time implementation review, and
independent review.
