from __future__ import annotations

import argparse
from collections.abc import Iterable
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Literal

from nofucksgiven.baselines import SUPPORTED_AEAD_ALGORITHMS, AeadCipher

BenchmarkOperation = Literal["encrypt", "decrypt", "roundtrip"]


@dataclass(frozen=True)
class BenchmarkResult:
    algorithm: str
    operation: BenchmarkOperation
    payload_size: int
    iterations: int
    elapsed_ns: int
    bytes_processed: int
    mib_per_second: float


def run_once(
    name: str,
    payload_size: int,
    iterations: int,
    operation: BenchmarkOperation,
) -> BenchmarkResult:
    cipher = AeadCipher.new(name)
    aad = b"benchmark"
    payload = b"x" * payload_size
    sealed = cipher.encrypt(payload, aad)

    start = perf_counter_ns()
    if operation == "encrypt":
        for _ in range(iterations):
            cipher.encrypt(payload, aad)
    elif operation == "decrypt":
        for _ in range(iterations):
            cipher.decrypt(sealed, aad)
    elif operation == "roundtrip":
        for _ in range(iterations):
            roundtrip = cipher.encrypt(payload, aad)
            cipher.decrypt(roundtrip, aad)
    else:
        raise ValueError(f"unsupported benchmark operation: {operation}")
    elapsed_ns = perf_counter_ns() - start

    total_bytes = payload_size * iterations
    seconds = elapsed_ns / 1_000_000_000
    mib_per_second = total_bytes / (1024 * 1024) / seconds
    return BenchmarkResult(
        algorithm=name,
        operation=operation,
        payload_size=payload_size,
        iterations=iterations,
        elapsed_ns=elapsed_ns,
        bytes_processed=total_bytes,
        mib_per_second=mib_per_second,
    )


def run_matrix(
    algorithms: Iterable[str],
    payload_sizes: Iterable[int],
    iterations: int,
    operations: Iterable[BenchmarkOperation],
) -> list[BenchmarkResult]:
    return [
        run_once(algorithm, payload_size, iterations, operation)
        for payload_size in payload_sizes
        for algorithm in algorithms
        for operation in operations
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark AEAD baseline wrappers.")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--sizes", type=int, nargs="+", default=[64, 1024, 16384, 1048576])
    parser.add_argument(
        "--algorithms",
        nargs="+",
        choices=list(SUPPORTED_AEAD_ALGORITHMS),
        default=list(SUPPORTED_AEAD_ALGORITHMS),
    )
    parser.add_argument(
        "--operations",
        nargs="+",
        choices=["encrypt", "decrypt", "roundtrip"],
        default=["encrypt", "decrypt", "roundtrip"],
    )
    args = parser.parse_args()

    print("algorithm,operation,payload_size,iterations,elapsed_ns,bytes_processed,mib_per_second")
    for result in run_matrix(args.algorithms, args.sizes, args.iterations, args.operations):
        print(
            f"{result.algorithm},{result.operation},{result.payload_size},{result.iterations},"
            f"{result.elapsed_ns},{result.bytes_processed},{result.mib_per_second:.2f}"
        )


if __name__ == "__main__":
    main()
