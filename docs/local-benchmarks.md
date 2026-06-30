# Local Benchmarks

These numbers are local implementation measurements. They do not prove security
and they do not change the evidence leaderboard by themselves.

## Environment

| Field | Value |
| --- | --- |
| Date | 2026-06-30T19:52:20Z |
| OS | Kali 2026.2 |
| CPU | Intel Core i5-9400F CPU @ 2.90GHz |
| Virtualization | VMware |
| Python | 3.13.12 |
| cryptography | 49.0.0 |

## Command

```bash
.venv/bin/python benchmarks/bench_leaderboard.py --iterations 1000 --sizes 1024 --operations roundtrip
.venv/bin/python benchmarks/bench_nfg.py --iterations 1000 --datasets zeros-1k --operations roundtrip
```

## Roundtrip Throughput

Payload size: 1024 bytes. Iterations: 1000. Operation: encrypt plus decrypt.

| Algorithm | Status | MiB/s | Notes |
| --- | --- | ---: | --- |
| AES-GCM-256 | available | 992.84 | library AEAD baseline |
| ChaCha20-Poly1305 | available | 773.38 | library AEAD baseline |
| AES-GCM-SIV | available | 278.38 | library misuse-resistant AEAD baseline |
| RC4 | available | 161.71 | do not use; legacy stream cipher benchmark |
| AES-ECB | available | 111.40 | do not use; pattern-leaking confidentiality-only benchmark |
| AES-CBC without authentication | available | 100.29 | avoid for new work; confidentiality-only benchmark |
| AES-CTR + HMAC-SHA-256 | available | 68.66 | local encrypt-then-MAC composition benchmark |
| AES-CBC + HMAC-SHA-256 | available | 59.78 | local encrypt-then-MAC composition benchmark |
| Triple DES / TDEA | available | 24.59 | withdrawn legacy cipher benchmark |
| NFG-v0 | available | 7.68 | toy experiment; not for real data |
| Ascon-AEAD128 | unavailable | 0.00 | no vetted Ascon implementation is configured in this repo |
| XChaCha20-Poly1305 | unavailable | 0.00 | `cryptography` exposes ChaCha20-Poly1305, not XChaCha20-Poly1305 |
| DES | unavailable | 0.00 | no standalone DES primitive is configured in this repo |

## Takeaways

- AES-GCM-256 is the fastest local 1 KiB roundtrip in this run.
- AES-GCM-SIV is now benchmarked locally, but it is slower than AES-GCM-256 here.
- NFG-v0 is far behind the established baselines on local throughput.
- Legacy algorithms can be fast enough to tempt people. That does not make them safe.
- Missing rows stay explicit instead of getting fake numbers.
