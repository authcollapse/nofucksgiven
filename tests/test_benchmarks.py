from __future__ import annotations

import pytest

from benchmarks.bench_aead import run_matrix, run_once
from benchmarks.bench_nfg import run_matrix as run_nfg_matrix
from benchmarks.bench_nfg import run_once as run_nfg_once
from nofucksgiven.baselines import SUPPORTED_AEAD_ALGORITHMS


def test_run_once_returns_structured_result() -> None:
    result = run_once("aes-gcm-256", payload_size=16, iterations=1, operation="roundtrip")

    assert result.algorithm == "aes-gcm-256"
    assert result.operation == "roundtrip"
    assert result.payload_size == 16
    assert result.iterations == 1
    assert result.elapsed_ns > 0
    assert result.bytes_processed == 32
    assert result.mib_per_second > 0


def test_run_matrix_covers_requested_algorithms_and_sizes() -> None:
    results = run_matrix(
        SUPPORTED_AEAD_ALGORITHMS,
        payload_sizes=[8, 32],
        iterations=1,
        operations=["encrypt", "decrypt"],
    )

    assert {(result.algorithm, result.payload_size, result.operation) for result in results} == {
        (algorithm, size, operation)
        for algorithm in SUPPORTED_AEAD_ALGORITHMS
        for size in (8, 32)
        for operation in ("encrypt", "decrypt")
    }


def test_roundtrip_counts_encrypt_and_decrypt_bytes() -> None:
    result = run_once("aes-gcm-256", payload_size=16, iterations=3, operation="roundtrip")

    assert result.bytes_processed == 96


@pytest.mark.parametrize(
    ("payload_size", "iterations"),
    [(0, 1), (-1, 1), (1, 0), (1, -1)],
)
def test_run_once_rejects_non_positive_inputs(payload_size: int, iterations: int) -> None:
    with pytest.raises(ValueError):
        run_once(
            "aes-gcm-256", payload_size=payload_size, iterations=iterations, operation="encrypt"
        )


def test_nfg_benchmark_uses_named_datasets() -> None:
    result = run_nfg_once("ascii", iterations=1, operation="roundtrip")

    assert result.algorithm == "nfg-v0"
    assert result.dataset == "ascii"
    assert result.payload_size > 0
    assert result.bytes_processed == result.payload_size * 2
    assert result.mib_per_second > 0


def test_nfg_benchmark_allows_empty_dataset() -> None:
    result = run_nfg_once("empty", iterations=1, operation="encrypt")

    assert result.payload_size == 0
    assert result.bytes_processed == 0
    assert result.mib_per_second == 0


def test_nfg_benchmark_matrix_covers_requested_datasets() -> None:
    results = run_nfg_matrix(["empty", "ascii"], iterations=1, operations=["encrypt", "decrypt"])

    assert {(result.dataset, result.operation) for result in results} == {
        ("empty", "encrypt"),
        ("empty", "decrypt"),
        ("ascii", "encrypt"),
        ("ascii", "decrypt"),
    }


def test_nfg_benchmark_rejects_unknown_dataset() -> None:
    with pytest.raises(ValueError, match="unknown NFG dataset"):
        run_nfg_once("missing", iterations=1, operation="encrypt")
