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

<div class="nfg-standings">
<article class="nfg-competitor nfg-competitor--top">
  <div class="nfg-competitor__rank">#1</div>
  <div class="nfg-competitor__main">
    <h3>AES-GCM-256</h3>
    <p>AEAD</p>
  </div>
  <div><span class="nfg-status nfg-status--go">baseline</span></div>
  <div class="nfg-competitor__score">94</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>30/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>25/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>20/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>4/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>15/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> vectors, round trips, tamper rejection, benchmark smoke</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Nonce reuse with the same key is catastrophic</div>
</article>

<article class="nfg-competitor nfg-competitor--top">
  <div class="nfg-competitor__rank">#2</div>
  <div class="nfg-competitor__main">
    <h3>AES-GCM-SIV</h3>
    <p>AEAD</p>
  </div>
  <div><span class="nfg-status nfg-status--go">misuse-resistant</span></div>
  <div class="nfg-competitor__score">91</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>24/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>25/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>20/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>10/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>12/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Not implemented in the current local baseline wrapper</div>
</article>

<article class="nfg-competitor nfg-competitor--top">
  <div class="nfg-competitor__rank">#3</div>
  <div class="nfg-competitor__main">
    <h3>ChaCha20-Poly1305</h3>
    <p>AEAD</p>
  </div>
  <div><span class="nfg-status nfg-status--go">baseline</span></div>
  <div class="nfg-competitor__score">88</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>24/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>25/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>20/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>4/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>15/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> vectors, round trips, tamper rejection, benchmark smoke</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Nonce reuse with the same key is unsafe</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#4</div>
  <div class="nfg-competitor__main">
    <h3>Ascon-AEAD128</h3>
    <p>Lightweight AEAD</p>
  </div>
  <div><span class="nfg-status nfg-status--lab">constrained devices</span></div>
  <div class="nfg-competitor__score">85</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>30/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>20/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>20/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>4/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>11/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Newer standard than AES and ChaCha20-Poly1305</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#5</div>
  <div class="nfg-competitor__main">
    <h3>XChaCha20-Poly1305</h3>
    <p>AEAD</p>
  </div>
  <div><span class="nfg-status nfg-status--lab">extended nonce</span></div>
  <div class="nfg-competitor__score">83</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>18/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>25/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>20/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>7/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>13/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Not a NIST standard</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#6</div>
  <div class="nfg-competitor__main">
    <h3>AES-CBC + HMAC-SHA-256</h3>
    <p>Encrypt-then-MAC composition</p>
  </div>
  <div><span class="nfg-status nfg-status--lab">compose carefully</span></div>
  <div class="nfg-competitor__score">66</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>18/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>20/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>15/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>13/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Easy to compose incorrectly</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#7</div>
  <div class="nfg-competitor__main">
    <h3>AES-CTR + HMAC-SHA-256</h3>
    <p>Encrypt-then-MAC composition</p>
  </div>
  <div><span class="nfg-status nfg-status--lab">compose carefully</span></div>
  <div class="nfg-competitor__score">66</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>18/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>20/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>15/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>13/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Counter or nonce reuse is unsafe</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#8</div>
  <div class="nfg-competitor__main">
    <h3>AES-CBC without authentication</h3>
    <p>Confidentiality-only mode</p>
  </div>
  <div><span class="nfg-status nfg-status--avoid">avoid</span></div>
  <div class="nfg-competitor__score">40</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>12/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>20/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>0/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>8/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> No built-in integrity</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#9</div>
  <div class="nfg-competitor__main">
    <h3>AES-ECB</h3>
    <p>Confidentiality-only mode</p>
  </div>
  <div><span class="nfg-status nfg-status--avoid">do not use</span></div>
  <div class="nfg-competitor__score">25</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>5/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>20/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>0/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>0/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Leaks repeated plaintext block patterns</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#10</div>
  <div class="nfg-competitor__main">
    <h3>Triple DES / TDEA</h3>
    <p>Legacy block cipher</p>
  </div>
  <div><span class="nfg-status nfg-status--avoid">withdrawn</span></div>
  <div class="nfg-competitor__score">15</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>0/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>12/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>0/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>3/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Withdrawn from NIST recommendation for TDEA</div>
</article>

<article class="nfg-competitor nfg-competitor--nfg">
  <div class="nfg-competitor__rank">#11</div>
  <div class="nfg-competitor__main">
    <h3>NFG-v0</h3>
    <p>Original experiment</p>
  </div>
  <div><span class="nfg-status nfg-status--lab">lab build</span></div>
  <div class="nfg-competitor__score">12</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>0/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>0/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>7/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>5/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> deterministic datasets, vectors, round trips, tamper rejection, nonce-reuse failure demos, benchmark smoke</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> No public cryptanalysis</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#12</div>
  <div class="nfg-competitor__main">
    <h3>DES</h3>
    <p>Legacy block cipher</p>
  </div>
  <div><span class="nfg-status nfg-status--avoid">do not use</span></div>
  <div class="nfg-competitor__score">0</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>0/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>0/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>0/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>0/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> 56-bit key is far below modern security requirements</div>
</article>

<article class="nfg-competitor">
  <div class="nfg-competitor__rank">#13</div>
  <div class="nfg-competitor__main">
    <h3>RC4</h3>
    <p>Legacy stream cipher</p>
  </div>
  <div><span class="nfg-status nfg-status--avoid">do not use</span></div>
  <div class="nfg-competitor__score">0</div>
  <div class="nfg-score-breakdown" aria-label="Score breakdown">
    <div class="nfg-score-chip">
      <span>Standard</span>
      <strong>0/30</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Margin</span>
      <strong>0/25</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Auth</span>
      <strong>0/20</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Misuse</span>
      <strong>0/10</strong>
    </div>
    <div class="nfg-score-chip">
      <span>Review</span>
      <strong>0/15</strong>
    </div>
  </div>
  <div class="nfg-competitor__detail"><strong>Local reps:</strong> none yet</div>
  <div class="nfg-competitor__detail"><strong>Caution:</strong> Prohibited for TLS by RFC 7465</div>
</article>

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
- NFG-v0: local experiment only
- DES: NIST FIPS 46-3 withdrawal, NIST SP 800-131A
- RC4: RFC 7465

## How To Read This

- A high score means stronger public evidence and safer default shape, not guaranteed safety.
- Local experiments currently cover algorithms implemented in `src/nofucksgiven/baselines.py` and the NFG-v0 scaffold under `experiments/nfg/`.
- Performance benchmarks belong beside environment metadata; they do not increase security.
- Legacy algorithms stay on the board so we can test that our tooling rejects or warns on them.
