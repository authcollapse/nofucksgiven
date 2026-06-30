# nofucksgiven

<section class="nfg-hero" markdown>
<div class="nfg-hero__kicker">Crypto lab, scoreboard included</div>
<div class="nfg-hero__title">No trophies for hand-wavy encryption.</div>

<p class="nfg-hero__subtitle">
`nofucksgiven` is a beginner-friendly lab for testing symmetric encryption like it is entering a tournament: vectors first, tamper tests second, benchmarks with receipts, and zero patience for fake victory laps.
</p>

<div class="nfg-actions">
  <a class="nfg-button nfg-button--primary" href="leaderboard/">Open the leaderboard</a>
  <a class="nfg-button" href="development-map/">See the development map</a>
  <a class="nfg-button" href="commands/">Run it locally</a>
</div>
</section>

!!! warning "Research only"
    Do not use experimental code from this repo to protect real data. Local tests and benchmarks help you learn and compare behavior. They do not prove cryptographic security.

## What The Name Means

The repo name is not a shrug. It is a filter.

No fucks given to crypto theater. Plenty of fucks given to test vectors, threat models, public sources, reproducible runs, and caveats that do not hide in size-11 footnotes.

## Current Matchup

<div class="nfg-podium" markdown>
<div class="nfg-card nfg-card--champ" markdown>
<div class="nfg-rank">Current champ</div>
<div class="nfg-score nfg-score--gold">94</div>
### AES-GCM-256
<p class="nfg-tagline">Fast, standardized, battle-tested. Still loses instantly if you reuse a nonce with the same key.</p>
</div>

<div class="nfg-card" markdown>
<div class="nfg-rank">Misuse-resistant contender</div>
<div class="nfg-score nfg-score--silver">91</div>
### AES-GCM-SIV
<p class="nfg-tagline">Great shape for nonce-mistake resistance. Waiting for local wrapper work in this repo.</p>
</div>

<div class="nfg-card" markdown>
<div class="nfg-rank">Portable brawler</div>
<div class="nfg-score nfg-score--bronze">88</div>
### ChaCha20-Poly1305
<p class="nfg-tagline">Excellent software performance profile. Still not a permission slip to freestyle nonce handling.</p>
</div>
</div>

<div class="nfg-lab-card" markdown>
<div>
<div class="nfg-rank">Experimental undercard | #11 | score 12</div>
### NFG-v0
<p class="nfg-tagline">Our in-house symmetric-encryption lab build. It has datasets, vectors, tamper tests, nonce-reuse failure demos, and absolutely no permission to touch real data.</p>
</div>
<a class="nfg-button" href="leaderboard/#leaderboard">See where it lands</a>
</div>

## What You Can Do Here

| Goal | Where to start |
| --- | --- |
| See the current standings | [Evidence Leaderboard](leaderboard.md) |
| Understand the research flow | [Development Map](development-map.md) |
| Learn the staged path from basics to experiments | [Research Roadmap](roadmap.md) |
| Understand what is in and out of scope | [Threat Model](threat-model.md) |
| Run the project locally | [Commands](commands.md) |

## Current Baselines

The current code wraps library-backed AEAD baselines:

- AES-GCM-256
- ChaCha20-Poly1305

The test suite checks known-answer vectors, round trips, wrong keys, wrong AAD, tampering, nonce-size validation, benchmark structure, and docs/claim hygiene.

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
