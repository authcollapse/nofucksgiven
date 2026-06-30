from __future__ import annotations

import argparse
from collections.abc import Callable, Iterable
from dataclasses import dataclass
import hashlib
import hmac
from time import perf_counter_ns
from typing import Literal

from cryptography.hazmat.decrepit.ciphers import algorithms as decrepit_algorithms
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, AESGCMSIV, ChaCha20Poly1305

BenchmarkOperation = Literal["encrypt", "decrypt", "roundtrip"]
CSV_HEADER = (
    "algorithm,status,operation,payload_size,iterations,elapsed_ns,bytes_processed,"
    "mib_per_second,notes"
)
AAD = b"leaderboard-benchmark"


@dataclass(frozen=True)
class LeaderboardBenchmarkResult:
    algorithm: str
    status: str
    operation: str
    payload_size: int
    iterations: int
    elapsed_ns: int
    bytes_processed: int
    mib_per_second: float
    notes: str


@dataclass(frozen=True)
class BenchmarkCandidate:
    name: str
    factory: Callable[[], BenchmarkCipher] | None
    notes: str

    @property
    def available(self) -> bool:
        return self.factory is not None


class BenchmarkCipher:
    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        raise NotImplementedError

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        raise NotImplementedError


class AeadBenchmarkCipher(BenchmarkCipher):
    def __init__(self, algorithm: AESGCM | AESGCMSIV | ChaCha20Poly1305) -> None:
        self.algorithm = algorithm

    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        nonce = iteration.to_bytes(12, "big")
        return nonce + self.algorithm.encrypt(nonce, plaintext, aad)

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        nonce = sealed[:12]
        ciphertext = sealed[12:]
        return self.algorithm.decrypt(nonce, ciphertext, aad)


class AesCbcHmacCipher(BenchmarkCipher):
    def __init__(self) -> None:
        self.enc_key = bytes(range(32))
        self.mac_key = bytes(range(32, 64))

    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        iv = iteration.to_bytes(16, "big")
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()
        encryptor = Cipher(algorithms.AES(self.enc_key), modes.CBC(iv)).encryptor()
        body = encryptor.update(padded) + encryptor.finalize()
        tag = hmac.digest(self.mac_key, aad + iv + body, hashlib.sha256)
        return iv + body + tag

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        iv = sealed[:16]
        body = sealed[16:-32]
        tag = sealed[-32:]
        expected = hmac.digest(self.mac_key, aad + iv + body, hashlib.sha256)
        if not hmac.compare_digest(tag, expected):
            raise ValueError("authentication failed")
        decryptor = Cipher(algorithms.AES(self.enc_key), modes.CBC(iv)).decryptor()
        padded = decryptor.update(body) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()


class AesCtrHmacCipher(BenchmarkCipher):
    def __init__(self) -> None:
        self.enc_key = bytes(range(32))
        self.mac_key = bytes(range(32, 64))

    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        nonce = iteration.to_bytes(16, "big")
        encryptor = Cipher(algorithms.AES(self.enc_key), modes.CTR(nonce)).encryptor()
        body = encryptor.update(plaintext) + encryptor.finalize()
        tag = hmac.digest(self.mac_key, aad + nonce + body, hashlib.sha256)
        return nonce + body + tag

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        nonce = sealed[:16]
        body = sealed[16:-32]
        tag = sealed[-32:]
        expected = hmac.digest(self.mac_key, aad + nonce + body, hashlib.sha256)
        if not hmac.compare_digest(tag, expected):
            raise ValueError("authentication failed")
        decryptor = Cipher(algorithms.AES(self.enc_key), modes.CTR(nonce)).decryptor()
        return decryptor.update(body) + decryptor.finalize()


class AesCbcCipher(BenchmarkCipher):
    def __init__(self) -> None:
        self.key = bytes(range(32))

    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        iv = iteration.to_bytes(16, "big")
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()
        encryptor = Cipher(algorithms.AES(self.key), modes.CBC(iv)).encryptor()
        return iv + encryptor.update(padded) + encryptor.finalize()

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        iv = sealed[:16]
        body = sealed[16:]
        decryptor = Cipher(algorithms.AES(self.key), modes.CBC(iv)).decryptor()
        padded = decryptor.update(body) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()


class AesEcbCipher(BenchmarkCipher):
    def __init__(self) -> None:
        self.key = bytes(range(32))

    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()
        encryptor = Cipher(algorithms.AES(self.key), modes.ECB()).encryptor()
        return encryptor.update(padded) + encryptor.finalize()

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        decryptor = Cipher(algorithms.AES(self.key), modes.ECB()).decryptor()
        padded = decryptor.update(sealed) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()


class TripleDesCbcCipher(BenchmarkCipher):
    def __init__(self) -> None:
        self.key = bytes(range(24))

    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        iv = iteration.to_bytes(8, "big")
        padder = padding.PKCS7(64).padder()
        padded = padder.update(plaintext) + padder.finalize()
        encryptor = Cipher(decrepit_algorithms.TripleDES(self.key), modes.CBC(iv)).encryptor()
        return iv + encryptor.update(padded) + encryptor.finalize()

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        iv = sealed[:8]
        body = sealed[8:]
        decryptor = Cipher(decrepit_algorithms.TripleDES(self.key), modes.CBC(iv)).decryptor()
        padded = decryptor.update(body) + decryptor.finalize()
        unpadder = padding.PKCS7(64).unpadder()
        return unpadder.update(padded) + unpadder.finalize()


class Arc4Cipher(BenchmarkCipher):
    def __init__(self) -> None:
        self.key = bytes(range(16))

    def encrypt(self, plaintext: bytes, aad: bytes, iteration: int) -> bytes:
        encryptor = Cipher(decrepit_algorithms.ARC4(self.key), mode=None).encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

    def decrypt(self, sealed: bytes, aad: bytes) -> bytes:
        decryptor = Cipher(decrepit_algorithms.ARC4(self.key), mode=None).decryptor()
        return decryptor.update(sealed) + decryptor.finalize()


LEADERBOARD_CANDIDATES = (
    BenchmarkCandidate(
        "aes-gcm-256",
        lambda: AeadBenchmarkCipher(AESGCM(bytes(range(32)))),
        "library AEAD baseline",
    ),
    BenchmarkCandidate(
        "aes-gcm-siv",
        lambda: AeadBenchmarkCipher(AESGCMSIV(bytes(range(32)))),
        "library misuse-resistant AEAD baseline",
    ),
    BenchmarkCandidate(
        "chacha20-poly1305",
        lambda: AeadBenchmarkCipher(ChaCha20Poly1305(bytes(range(32)))),
        "library AEAD baseline",
    ),
    BenchmarkCandidate(
        "ascon-aead128",
        None,
        "not benchmarked: no vetted Ascon implementation is configured in this repo",
    ),
    BenchmarkCandidate(
        "xchacha20-poly1305",
        None,
        "not benchmarked: cryptography exposes ChaCha20-Poly1305, not XChaCha20-Poly1305",
    ),
    BenchmarkCandidate(
        "aes-cbc-hmac-sha256",
        AesCbcHmacCipher,
        "local encrypt-then-MAC composition benchmark",
    ),
    BenchmarkCandidate(
        "aes-ctr-hmac-sha256",
        AesCtrHmacCipher,
        "local encrypt-then-MAC composition benchmark",
    ),
    BenchmarkCandidate(
        "aes-cbc-no-auth",
        AesCbcCipher,
        "avoid for new work: confidentiality-only benchmark",
    ),
    BenchmarkCandidate(
        "aes-ecb",
        AesEcbCipher,
        "do not use: pattern-leaking confidentiality-only benchmark",
    ),
    BenchmarkCandidate(
        "triple-des-tdea",
        TripleDesCbcCipher,
        "withdrawn legacy cipher benchmark",
    ),
    BenchmarkCandidate(
        "des",
        None,
        "not benchmarked: no standalone DES primitive is configured in this repo",
    ),
    BenchmarkCandidate(
        "rc4",
        Arc4Cipher,
        "do not use: legacy stream cipher benchmark",
    ),
)


def run_candidate_once(
    candidate: BenchmarkCandidate,
    payload_size: int,
    iterations: int,
    operation: BenchmarkOperation,
) -> LeaderboardBenchmarkResult:
    if payload_size <= 0:
        raise ValueError("payload_size must be positive")
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    if candidate.factory is None:
        return LeaderboardBenchmarkResult(
            algorithm=candidate.name,
            status="unavailable",
            operation=operation,
            payload_size=payload_size,
            iterations=iterations,
            elapsed_ns=0,
            bytes_processed=0,
            mib_per_second=0.0,
            notes=candidate.notes,
        )

    cipher = candidate.factory()
    payload = b"x" * payload_size
    sealed = cipher.encrypt(payload, AAD, 0)

    start = perf_counter_ns()
    if operation == "encrypt":
        for iteration in range(iterations):
            cipher.encrypt(payload, AAD, iteration)
    elif operation == "decrypt":
        for _ in range(iterations):
            cipher.decrypt(sealed, AAD)
    elif operation == "roundtrip":
        for iteration in range(iterations):
            current = cipher.encrypt(payload, AAD, iteration)
            cipher.decrypt(current, AAD)
    else:
        raise ValueError(f"unsupported benchmark operation: {operation}")
    elapsed_ns = perf_counter_ns() - start
    multiplier = 2 if operation == "roundtrip" else 1
    bytes_processed = payload_size * iterations * multiplier
    seconds = elapsed_ns / 1_000_000_000
    return LeaderboardBenchmarkResult(
        algorithm=candidate.name,
        status="available",
        operation=operation,
        payload_size=payload_size,
        iterations=iterations,
        elapsed_ns=elapsed_ns,
        bytes_processed=bytes_processed,
        mib_per_second=bytes_processed / (1024 * 1024) / seconds,
        notes=candidate.notes,
    )


def run_matrix(
    payload_sizes: Iterable[int],
    iterations: int,
    operations: Iterable[BenchmarkOperation],
    candidates: Iterable[BenchmarkCandidate] = LEADERBOARD_CANDIDATES,
) -> list[LeaderboardBenchmarkResult]:
    return [
        run_candidate_once(candidate, payload_size, iterations, operation)
        for payload_size in payload_sizes
        for candidate in candidates
        for operation in operations
    ]


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark leaderboard algorithms locally.")
    parser.add_argument("--iterations", type=positive_int, default=1000)
    parser.add_argument("--sizes", type=positive_int, nargs="+", default=[64, 1024, 16384])
    parser.add_argument(
        "--operations",
        nargs="+",
        choices=["encrypt", "decrypt", "roundtrip"],
        default=["encrypt", "decrypt", "roundtrip"],
    )
    args = parser.parse_args()

    print(CSV_HEADER)
    for result in run_matrix(args.sizes, args.iterations, args.operations):
        print(
            f"{result.algorithm},{result.status},{result.operation},{result.payload_size},"
            f"{result.iterations},{result.elapsed_ns},{result.bytes_processed},"
            f"{result.mib_per_second:.2f},{result.notes}"
        )


if __name__ == "__main__":
    main()
