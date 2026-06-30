# Experiment Log

Copy this template when you start a new experiment.

## Hypothesis

What are you testing?

## Construction

What primitive, mode, or design idea are you evaluating?

## Method

What inputs, parameters, machines, and commands did you use?

## Results

Record correctness results, benchmark numbers, and any failures.

## Caveats

List limitations, assumptions, and reasons this does not establish production safety.

## Active Experiments

### NFG-v0

- Location: `experiments/nfg/`
- Purpose: first local scaffold for an original symmetric encryption experiment.
- Current method: deterministic datasets, fixed snapshot vector, tamper rejection tests, wrong-key/wrong-AAD tests, nonce-reuse failure demo, bit-flip sensitivity checks, and benchmark smoke.
- Latest iteration: NFG-v1 swaps HMAC-SHA-256 plumbing for keyed BLAKE2s plumbing, and both variants now use optimized equal-length XOR. In one local 1 KiB roundtrip run, NFG-v0 reached 11.68 MiB/s and NFG-v1 reached 33.07 MiB/s. NFG-v1 does not fix nonce reuse or replay.
- Caveat: NFG-v0 is not for real data. Passing local tests only means the scaffold behaved as expected locally.
