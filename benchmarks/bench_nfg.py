from __future__ import annotations

import argparse
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import sys
from time import perf_counter_ns
from typing import Literal

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.nfg import NfgCipher, load_dataset_cases


BenchmarkOperation = Literal["encrypt", "decrypt", "roundtrip"]
CSV_HEADER = (
    "algorithm,dataset,operation,payload_size,iterations,elapsed_ns,bytes_processed,mib_per_second"
)


@dataclass(frozen=True)
class NfgBenchmarkResult:
    algorithm: str
    dataset: str
    operation: BenchmarkOperation
    payload_size: int
    iterations: int
    elapsed_ns: int
    bytes_processed: int
    mib_per_second: float


def run_once(
    dataset_name: str, iterations: int, operation: BenchmarkOperation
) -> NfgBenchmarkResult:
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    cases = {case.name: case for case in load_dataset_cases()}
    if dataset_name not in cases:
        raise ValueError(f"unknown NFG dataset: {dataset_name}")
    case = cases[dataset_name]
    cipher = NfgCipher.new(bytes(32))
    sealed = cipher.encrypt(case.plaintext, case.aad)

    start = perf_counter_ns()
    if operation == "encrypt":
        for _ in range(iterations):
            cipher.encrypt(case.plaintext, case.aad)
    elif operation == "decrypt":
        for _ in range(iterations):
            cipher.decrypt(sealed, case.aad)
    elif operation == "roundtrip":
        for _ in range(iterations):
            current = cipher.encrypt(case.plaintext, case.aad)
            cipher.decrypt(current, case.aad)
    else:
        raise ValueError(f"unsupported benchmark operation: {operation}")
    elapsed_ns = perf_counter_ns() - start
    multiplier = 2 if operation == "roundtrip" else 1
    bytes_processed = len(case.plaintext) * iterations * multiplier
    seconds = elapsed_ns / 1_000_000_000
    mib_per_second = 0.0 if bytes_processed == 0 else bytes_processed / (1024 * 1024) / seconds
    return NfgBenchmarkResult(
        algorithm="nfg-v0",
        dataset=case.name,
        operation=operation,
        payload_size=len(case.plaintext),
        iterations=iterations,
        elapsed_ns=elapsed_ns,
        bytes_processed=bytes_processed,
        mib_per_second=mib_per_second,
    )


def run_matrix(
    datasets: Iterable[str],
    iterations: int,
    operations: Iterable[BenchmarkOperation],
) -> list[NfgBenchmarkResult]:
    return [
        run_once(dataset_name, iterations, operation)
        for dataset_name in datasets
        for operation in operations
    ]


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def main() -> None:
    dataset_names = [case.name for case in load_dataset_cases()]
    parser = argparse.ArgumentParser(description="Benchmark the NFG-v0 experiment.")
    parser.add_argument("--iterations", type=positive_int, default=1000)
    parser.add_argument("--datasets", nargs="+", choices=dataset_names, default=dataset_names)
    parser.add_argument(
        "--operations",
        nargs="+",
        choices=["encrypt", "decrypt", "roundtrip"],
        default=["encrypt", "decrypt", "roundtrip"],
    )
    args = parser.parse_args()

    print(CSV_HEADER)
    for result in run_matrix(args.datasets, args.iterations, args.operations):
        print(
            f"{result.algorithm},{result.dataset},{result.operation},{result.payload_size},"
            f"{result.iterations},{result.elapsed_ns},{result.bytes_processed},"
            f"{result.mib_per_second:.2f}"
        )


if __name__ == "__main__":
    main()
