"""Deterministic local datasets for NFG experiments."""

from __future__ import annotations

from dataclasses import dataclass
import json
import random


DATASET_SEED = 0x4E46475F7630


@dataclass(frozen=True)
class DatasetCase:
    """Named plaintext/AAD pair used by tests and benchmarks."""

    name: str
    plaintext: bytes
    aad: bytes
    note: str


def load_dataset_cases() -> tuple[DatasetCase, ...]:
    """Return deterministic inputs that exercise edge cases and common shapes."""
    rng = random.Random(DATASET_SEED)
    cases = [
        DatasetCase("empty", b"", b"case:empty", "zero-length plaintext"),
        DatasetCase("single-byte", b"\x00", b"case:single-byte", "minimum non-empty input"),
        DatasetCase(
            "ascii", b"attack at dawn, but write a test first", b"case:ascii", "short text"
        ),
        DatasetCase(
            "utf8",
            "evidence beats vibes; მონაცემები სჯობს ხმაურს".encode(),
            b"case:utf8",
            "multi-byte UTF-8 text",
        ),
        DatasetCase(
            "json",
            json.dumps(
                {
                    "algorithm": "nfg-v0",
                    "purpose": "experiment",
                    "production_safe": False,
                },
                sort_keys=True,
            ).encode(),
            b"case:json",
            "structured metadata payload",
        ),
        DatasetCase("zeros-1k", bytes(1024), b"case:zeros-1k", "repeated zero bytes"),
        DatasetCase(
            "incrementing-256",
            bytes(range(256)),
            b"case:incrementing-256",
            "every byte value once",
        ),
        DatasetCase(
            "alternating-1k",
            bytes([0xAA, 0x55]) * 512,
            b"case:alternating-1k",
            "highly regular alternating pattern",
        ),
    ]
    for size in (31, 32, 33, 255, 4096):
        cases.append(
            DatasetCase(
                f"deterministic-random-{size}",
                bytes(rng.randrange(0, 256) for _ in range(size)),
                f"case:deterministic-random-{size}".encode(),
                "seeded pseudo-random bytes for reproducible tests",
            )
        )
    return tuple(cases)
