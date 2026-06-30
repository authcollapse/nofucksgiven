# Encryption Evidence Leaderboard

<section class="nfg-hero" markdown>
<div class="nfg-hero__kicker">Season one standings</div>
<div class="nfg-hero__title">Authenticated encryption cage match.</div>

<p class="nfg-hero__subtitle">
The score is evidence confidence: standards, review maturity, misuse shape, auth integrity, and what this repo has actually tested. It is not a magical security number.
</p>
</section>

<div class="nfg-podium" markdown>
<div class="nfg-card nfg-card--champ" markdown>
<div class="nfg-rank">#1 | belt holder</div>
<div class="nfg-score nfg-score--gold">94</div>
### AES-GCM-256
<p class="nfg-tagline">The default heavyweight. Standardized, widely deployed, locally tested here. Still gets folded by nonce reuse.</p>
</div>

<div class="nfg-card" markdown>
<div class="nfg-rank">#2 | mistake-resistant challenger</div>
<div class="nfg-score nfg-score--silver">91</div>
### AES-GCM-SIV
<p class="nfg-tagline">Built for a better nonce-mistake posture. Winning on public evidence while it waits for local reps.</p>
</div>

<div class="nfg-card" markdown>
<div class="nfg-rank">#3 | software-speed favorite</div>
<div class="nfg-score nfg-score--bronze">88</div>
### ChaCha20-Poly1305
<p class="nfg-tagline">The software-speed favorite. Clean modern AEAD shape, no freestyle nonce nonsense.</p>
</div>

</div>

<p class="nfg-callout">
High score means "stronger public evidence and safer default shape." It is not a proof of security, and it is not "go encrypt production data with random code from a GitHub repo."
</p>


## Rubric

| Criterion | Max |
| --- | ---: |
| Standard Status | 30 |
| Security Margin | 25 |
| Auth Integrity | 20 |
| Misuse Resistance | 10 |
| Review Maturity | 15 |

## Leaderboard

<div class="nfg-board" markdown>

| Rank | Algorithm | Family | Status | Evidence Score | Local Experiments | Main Caution |
| ---: | --- | --- | --- | ---: | --- | --- |
| <span class="nfg-medal">1</span> | AES-GCM-256 | AEAD | <span class="nfg-status nfg-status--go">baseline</span> | 94 | vectors, round trips, tamper rejection, benchmark smoke | Nonce reuse with the same key is catastrophic |
| <span class="nfg-medal">2</span> | AES-GCM-SIV | AEAD | <span class="nfg-status nfg-status--go">misuse-resistant</span> | 91 | none yet | Not implemented in the current local baseline wrapper |
| <span class="nfg-medal">3</span> | ChaCha20-Poly1305 | AEAD | <span class="nfg-status nfg-status--go">baseline</span> | 88 | vectors, round trips, tamper rejection, benchmark smoke | Nonce reuse with the same key is unsafe |
| 4 | Ascon-AEAD128 | Lightweight AEAD | <span class="nfg-status nfg-status--lab">constrained devices</span> | 85 | none yet | Newer standard than AES and ChaCha20-Poly1305 |
| 5 | XChaCha20-Poly1305 | AEAD | <span class="nfg-status nfg-status--lab">extended nonce</span> | 83 | none yet | Not a NIST standard |
| 6 | AES-CBC + HMAC-SHA-256 | Encrypt-then-MAC composition | <span class="nfg-status nfg-status--lab">compose carefully</span> | 66 | none yet | Easy to compose incorrectly |
| 7 | AES-CTR + HMAC-SHA-256 | Encrypt-then-MAC composition | <span class="nfg-status nfg-status--lab">compose carefully</span> | 66 | none yet | Counter or nonce reuse is unsafe |
| 8 | AES-CBC without authentication | Confidentiality-only mode | <span class="nfg-status nfg-status--avoid">avoid</span> | 40 | none yet | No built-in integrity |
| 9 | AES-ECB | Confidentiality-only mode | <span class="nfg-status nfg-status--avoid">do not use</span> | 25 | none yet | Leaks repeated plaintext block patterns |
| 10 | Triple DES / TDEA | Legacy block cipher | <span class="nfg-status nfg-status--avoid">withdrawn</span> | 15 | none yet | Withdrawn from NIST recommendation for TDEA |
| 11 | DES | Legacy block cipher | <span class="nfg-status nfg-status--avoid">do not use</span> | 0 | none yet | 56-bit key is far below modern security requirements |
| 12 | RC4 | Legacy stream cipher | <span class="nfg-status nfg-status--avoid">do not use</span> | 0 | none yet | Prohibited for TLS by RFC 7465 |

</div>

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
