from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from experiments.nfg import (
    NFG_KEY_SIZE,
    NFG_NONCE_SIZE,
    NFG_TAG_SIZE,
    NfgV1Cipher,
    NfgV1SealedMessage,
    load_dataset_cases,
)


FIXED_KEY = bytes(range(NFG_KEY_SIZE))
FIXED_NONCE = bytes(range(100, 100 + NFG_NONCE_SIZE))


@pytest.mark.parametrize("case", load_dataset_cases(), ids=lambda case: case.name)
def test_nfg_v1_dataset_round_trips(case) -> None:
    cipher = NfgV1Cipher(FIXED_KEY)

    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, case.plaintext, case.aad)

    assert len(sealed.nonce) == NFG_NONCE_SIZE
    assert len(sealed.ciphertext) == len(case.plaintext) + NFG_TAG_SIZE
    assert cipher.decrypt(sealed, case.aad) == case.plaintext


@given(plaintext=st.binary(max_size=2048), aad=st.binary(max_size=256))
def test_nfg_v1_property_round_trip(plaintext: bytes, aad: bytes) -> None:
    cipher = NfgV1Cipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, plaintext, aad)

    assert cipher.decrypt(sealed, aad) == plaintext


def test_nfg_v1_wrong_key_is_rejected() -> None:
    first = NfgV1Cipher(FIXED_KEY)
    second = NfgV1Cipher(b"\xff" * NFG_KEY_SIZE)
    sealed = first.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")

    with pytest.raises(ValueError, match="authentication failed"):
        second.decrypt(sealed, b"context")


def test_nfg_v1_wrong_aad_is_rejected() -> None:
    cipher = NfgV1Cipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")

    with pytest.raises(ValueError, match="authentication failed"):
        cipher.decrypt(sealed, b"wrong-context")


@pytest.mark.parametrize("offset", [0, -1])
def test_nfg_v1_tampering_is_rejected(offset: int) -> None:
    cipher = NfgV1Cipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")
    tampered = bytearray(sealed.ciphertext)
    tampered[offset] ^= 1

    with pytest.raises(ValueError, match="authentication failed"):
        cipher.decrypt(NfgV1SealedMessage(sealed.nonce, bytes(tampered)), b"context")


def test_nfg_v1_nonce_reuse_still_exposes_plaintext_xor_failure_mode() -> None:
    cipher = NfgV1Cipher(FIXED_KEY)
    left_plaintext = b"A" * 32
    right_plaintext = b"B" * 32
    left = cipher.encrypt_with_nonce(FIXED_NONCE, left_plaintext, b"context")
    right = cipher.encrypt_with_nonce(FIXED_NONCE, right_plaintext, b"context")

    left_body = left.ciphertext[:-NFG_TAG_SIZE]
    right_body = right.ciphertext[:-NFG_TAG_SIZE]
    xor_ciphertexts = bytes(a ^ b for a, b in zip(left_body, right_body, strict=True))
    xor_plaintexts = bytes(a ^ b for a, b in zip(left_plaintext, right_plaintext, strict=True))

    assert xor_ciphertexts == xor_plaintexts


def test_nfg_v1_replay_same_message_still_decrypts() -> None:
    cipher = NfgV1Cipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")

    assert cipher.decrypt(sealed, b"context") == b"message"
    assert cipher.decrypt(sealed, b"context") == b"message"


def test_nfg_v1_output_differs_from_nfg_v0_vector() -> None:
    cipher = NfgV1Cipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, b"nfg test vector", b"vector:v0")

    assert sealed.ciphertext.hex() != (
        "116caaf1e8b8b9b67fa5120e8821855df7a4638090b79bf1bb3164a6b1c5fd"
    )
