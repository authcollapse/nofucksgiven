# Encryption Evidence Leaderboard

This is an evidence-confidence leaderboard, not a proof of security. Use it to compare what we know, what we have tested locally, and what still needs evidence.

## Rubric

| Criterion | Max |
| --- | ---: |
| Standard Status | 30 |
| Security Margin | 25 |
| Auth Integrity | 20 |
| Misuse Resistance | 10 |
| Review Maturity | 15 |

## Leaderboard

| Rank | Algorithm | Family | Status | Evidence Score | Local Experiments | Main Caution |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | AES-GCM-256 | AEAD | recommended_baseline | 94 | known_answer_vectors, round_trip_property_tests, tamper_rejection_tests, benchmark_smoke | Nonce reuse with the same key is catastrophic |
| 2 | AES-GCM-SIV | AEAD | recommended_misuse_resistant | 91 | none yet | Not implemented in the current local baseline wrapper |
| 3 | ChaCha20-Poly1305 | AEAD | recommended_baseline | 88 | known_answer_vectors, round_trip_property_tests, tamper_rejection_tests, benchmark_smoke | Nonce reuse with the same key is unsafe |
| 4 | Ascon-AEAD128 | Lightweight AEAD | recommended_constrained_devices | 85 | none yet | Newer standard than AES and ChaCha20-Poly1305 |
| 5 | XChaCha20-Poly1305 | AEAD | recommended_when_available | 83 | none yet | Not a NIST standard |
| 6 | AES-CBC + HMAC-SHA-256 | Encrypt-then-MAC composition | acceptable_when_composed_correctly | 66 | none yet | Easy to compose incorrectly |
| 7 | AES-CTR + HMAC-SHA-256 | Encrypt-then-MAC composition | acceptable_when_composed_correctly | 66 | none yet | Counter or nonce reuse is unsafe |
| 8 | AES-CBC without authentication | Confidentiality-only mode | avoid_for_new_work | 40 | none yet | No built-in integrity |
| 9 | AES-ECB | Confidentiality-only mode | do_not_use_for_secret_data | 25 | none yet | Leaks repeated plaintext block patterns |
| 10 | Triple DES / TDEA | Legacy block cipher | deprecated_or_withdrawn | 15 | none yet | Withdrawn from NIST recommendation for TDEA |
| 11 | DES | Legacy block cipher | do_not_use | 0 | none yet | 56-bit key is far below modern security requirements |
| 12 | RC4 | Legacy stream cipher | do_not_use | 0 | none yet | Prohibited for TLS by RFC 7465 |

## Source Tags

- AES-GCM-256: NIST FIPS 197, NIST SP 800-38D
- AES-GCM-SIV: RFC 8452
- ChaCha20-Poly1305: RFC 8439
- Ascon-AEAD128: NIST SP 800-232
- XChaCha20-Poly1305: libsodium XChaCha20-Poly1305 documentation
- AES-CBC + HMAC-SHA-256: NIST SP 800-38A
- AES-CTR + HMAC-SHA-256: NIST SP 800-38A
- AES-CBC without authentication: NIST SP 800-38A
- AES-ECB: NIST SP 800-38A
- Triple DES / TDEA: NIST SP 800-67 withdrawal, NIST SP 800-131A
- DES: NIST FIPS 197
- RC4: RFC 7465

## How To Read This

- A high score means stronger public evidence and safer default shape, not guaranteed safety.
- Local experiments currently cover only algorithms implemented in `src/nofucksgiven/baselines.py`.
- Performance benchmarks belong beside environment metadata; they do not increase security.
- Legacy algorithms stay on the board so we can test that our tooling rejects or warns on them.
