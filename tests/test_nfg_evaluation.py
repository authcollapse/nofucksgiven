from __future__ import annotations

import pytest

from experiments.nfg import NFG_KEY_SIZE, NFG_NONCE_SIZE, NFG_TAG_SIZE, NfgCipher
from experiments.nfg.evaluation import (
    average_ratio,
    flip_bit,
    hamming_distance,
    measure_nfg_bit_flips,
)


FIXED_KEY = bytes(range(NFG_KEY_SIZE))
FIXED_NONCE = bytes(range(100, 100 + NFG_NONCE_SIZE))
FIXED_PLAINTEXT = bytes(range(128))
FIXED_AAD = b"nfg-evaluation"


def test_hamming_distance_counts_changed_bits() -> None:
    assert hamming_distance(b"\x00", b"\xff") == 8
    assert hamming_distance(b"\x00\x0f", b"\x00\xf0") == 8


def test_hamming_distance_rejects_different_lengths() -> None:
    with pytest.raises(ValueError, match="equal-length"):
        hamming_distance(b"a", b"ab")


def test_flip_bit_uses_stable_most_significant_bit_order() -> None:
    assert flip_bit(b"\x00", 0) == b"\x80"
    assert flip_bit(b"\x00", 7) == b"\x01"


def test_flip_bit_rejects_out_of_range_index() -> None:
    with pytest.raises(ValueError, match="outside input"):
        flip_bit(b"\x00", 8)


@pytest.mark.parametrize("changed_input", ["key", "nonce"])
def test_nfg_key_and_nonce_flips_change_broad_output(changed_input: str) -> None:
    measurements = measure_nfg_bit_flips(
        key=FIXED_KEY,
        nonce=FIXED_NONCE,
        plaintext=FIXED_PLAINTEXT,
        aad=FIXED_AAD,
        changed_input=changed_input,
        bit_indices=(0, 17, 63, 127),
    )

    ratio = average_ratio(measurements)

    assert 0.35 <= ratio <= 0.65


def test_nfg_plaintext_flip_has_stream_cipher_body_shape() -> None:
    cipher = NfgCipher(FIXED_KEY)
    base = cipher.encrypt_with_nonce(FIXED_NONCE, FIXED_PLAINTEXT, FIXED_AAD).ciphertext
    changed = cipher.encrypt_with_nonce(
        FIXED_NONCE,
        flip_bit(FIXED_PLAINTEXT, 0),
        FIXED_AAD,
    ).ciphertext

    base_body = base[:-NFG_TAG_SIZE]
    changed_body = changed[:-NFG_TAG_SIZE]
    base_tag = base[-NFG_TAG_SIZE:]
    changed_tag = changed[-NFG_TAG_SIZE:]

    assert hamming_distance(base_body, changed_body) == 1
    assert hamming_distance(base_tag, changed_tag) > NFG_TAG_SIZE * 8 * 0.35


def test_nfg_aad_flip_changes_tag_not_ciphertext_body() -> None:
    cipher = NfgCipher(FIXED_KEY)
    base = cipher.encrypt_with_nonce(FIXED_NONCE, FIXED_PLAINTEXT, FIXED_AAD).ciphertext
    changed = cipher.encrypt_with_nonce(
        FIXED_NONCE,
        FIXED_PLAINTEXT,
        flip_bit(FIXED_AAD, 0),
    ).ciphertext

    assert base[:-NFG_TAG_SIZE] == changed[:-NFG_TAG_SIZE]
    assert hamming_distance(base[-NFG_TAG_SIZE:], changed[-NFG_TAG_SIZE:]) > NFG_TAG_SIZE * 8 * 0.35


def test_nfg_bit_flip_measurement_reports_deterministic_ratio() -> None:
    [measurement] = measure_nfg_bit_flips(
        key=FIXED_KEY,
        nonce=FIXED_NONCE,
        plaintext=FIXED_PLAINTEXT,
        aad=FIXED_AAD,
        changed_input="plaintext",
        bit_indices=(0,),
    )

    assert measurement.changed_input == "plaintext"
    assert measurement.bit_index == 0
    assert measurement.compared_region == "ciphertext_and_tag"
    assert measurement.changed_bits > 1
    assert measurement.total_bits == (len(FIXED_PLAINTEXT) + NFG_TAG_SIZE) * 8
