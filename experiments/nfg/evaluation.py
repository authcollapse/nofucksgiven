"""Evaluation helpers for the NFG experiment.

These helpers measure local behavior. They do not establish cryptographic
security, but they make weak spots concrete enough to iterate on.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

from experiments.nfg.cipher import NfgCipher


NfgInput = Literal["key", "nonce", "plaintext", "aad"]


@dataclass(frozen=True)
class BitFlipMeasurement:
    changed_input: NfgInput
    bit_index: int
    compared_region: str
    changed_bits: int
    total_bits: int

    @property
    def ratio(self) -> float:
        if self.total_bits == 0:
            return 0.0
        return self.changed_bits / self.total_bits


def hamming_distance(left: bytes, right: bytes) -> int:
    if len(left) != len(right):
        raise ValueError("hamming distance requires equal-length inputs")
    return sum((left_item ^ right_item).bit_count() for left_item, right_item in zip(left, right))


def flip_bit(data: bytes, bit_index: int) -> bytes:
    if bit_index < 0 or bit_index >= len(data) * 8:
        raise ValueError("bit index outside input")
    changed = bytearray(data)
    byte_index, bit_offset = divmod(bit_index, 8)
    changed[byte_index] ^= 1 << (7 - bit_offset)
    return bytes(changed)


def measure_nfg_bit_flips(
    *,
    key: bytes,
    nonce: bytes,
    plaintext: bytes,
    aad: bytes,
    changed_input: NfgInput,
    bit_indices: Iterable[int],
) -> tuple[BitFlipMeasurement, ...]:
    base = NfgCipher(key).encrypt_with_nonce(nonce, plaintext, aad).ciphertext
    measurements: list[BitFlipMeasurement] = []

    for bit_index in bit_indices:
        changed_key = key
        changed_nonce = nonce
        changed_plaintext = plaintext
        changed_aad = aad
        if changed_input == "key":
            changed_key = flip_bit(key, bit_index)
        elif changed_input == "nonce":
            changed_nonce = flip_bit(nonce, bit_index)
        elif changed_input == "plaintext":
            changed_plaintext = flip_bit(plaintext, bit_index)
        elif changed_input == "aad":
            changed_aad = flip_bit(aad, bit_index)
        else:
            raise ValueError(f"unsupported input: {changed_input}")

        changed = (
            NfgCipher(changed_key)
            .encrypt_with_nonce(
                changed_nonce,
                changed_plaintext,
                changed_aad,
            )
            .ciphertext
        )
        measurements.append(
            BitFlipMeasurement(
                changed_input=changed_input,
                bit_index=bit_index,
                compared_region="ciphertext_and_tag",
                changed_bits=hamming_distance(base, changed),
                total_bits=len(base) * 8,
            )
        )

    return tuple(measurements)


def average_ratio(measurements: Iterable[BitFlipMeasurement]) -> float:
    values = tuple(measurement.ratio for measurement in measurements)
    if not values:
        raise ValueError("at least one measurement is required")
    return sum(values) / len(values)
