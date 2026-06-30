from __future__ import annotations

from time import perf_counter_ns

from nofucksgiven.baselines import AeadCipher


def run_once(name: str, cipher: AeadCipher, payload_size: int, iterations: int) -> None:
    aad = b"benchmark"
    payload = b"x" * payload_size

    start = perf_counter_ns()
    for _ in range(iterations):
        sealed = cipher.encrypt(payload, aad)
        cipher.decrypt(sealed, aad)
    elapsed_ns = perf_counter_ns() - start

    total_bytes = payload_size * iterations
    seconds = elapsed_ns / 1_000_000_000
    mib_per_second = total_bytes / (1024 * 1024) / seconds
    print(f"{name}: {payload_size} bytes x {iterations}: {mib_per_second:.2f} MiB/s")


def main() -> None:
    for payload_size in (64, 1024, 16384, 1048576):
        run_once("AES-GCM-256", AeadCipher.new_aes_gcm(), payload_size, 1000)
        run_once("ChaCha20-Poly1305", AeadCipher.new_chacha20_poly1305(), payload_size, 1000)


if __name__ == "__main__":
    main()
