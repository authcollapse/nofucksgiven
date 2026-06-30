from __future__ import annotations

import pytest

from benchmarks.bench_aead import run_matrix, run_once
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
