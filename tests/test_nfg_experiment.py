from __future__ import annotations

import json
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from experiments.nfg import (
    NFG_KEY_SIZE,
    NFG_NONCE_SIZE,
    NFG_TAG_SIZE,
    NfgCipher,
    NfgSealedMessage,
    load_dataset_cases,
)


FIXED_KEY = bytes(range(NFG_KEY_SIZE))
FIXED_NONCE = bytes(range(100, 100 + NFG_NONCE_SIZE))
VECTOR_PATH = Path("experiments/nfg/vectors.json")


@pytest.mark.parametrize("case", load_dataset_cases(), ids=lambda case: case.name)
def test_nfg_dataset_round_trips(case) -> None:
    cipher = NfgCipher(FIXED_KEY)

    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, case.plaintext, case.aad)

    assert len(sealed.nonce) == NFG_NONCE_SIZE
    assert len(sealed.ciphertext) == len(case.plaintext) + NFG_TAG_SIZE
    assert cipher.decrypt(sealed, case.aad) == case.plaintext


@given(plaintext=st.binary(max_size=2048), aad=st.binary(max_size=256))
def test_nfg_property_round_trip(plaintext: bytes, aad: bytes) -> None:
    cipher = NfgCipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, plaintext, aad)

    assert cipher.decrypt(sealed, aad) == plaintext


def test_nfg_snapshot_vector() -> None:
    [vector] = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
    cipher = NfgCipher(bytes.fromhex(vector["key_hex"]))
    sealed = cipher.encrypt_with_nonce(
        bytes.fromhex(vector["nonce_hex"]),
        bytes.fromhex(vector["plaintext_hex"]),
        bytes.fromhex(vector["aad_hex"]),
    )

    assert sealed.ciphertext.hex() == vector["ciphertext_hex"]
    assert cipher.decrypt(sealed, bytes.fromhex(vector["aad_hex"])) == bytes.fromhex(
        vector["plaintext_hex"]
    )


def test_nfg_same_plaintext_with_different_nonce_changes_ciphertext() -> None:
    cipher = NfgCipher(FIXED_KEY)
    first = cipher.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")
    second_nonce = bytes([FIXED_NONCE[0] ^ 1]) + FIXED_NONCE[1:]
    second = cipher.encrypt_with_nonce(second_nonce, b"message", b"context")

    assert first.ciphertext != second.ciphertext


def test_nfg_wrong_key_is_rejected() -> None:
    first = NfgCipher(FIXED_KEY)
    second = NfgCipher(b"\xff" * NFG_KEY_SIZE)
    sealed = first.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")

    with pytest.raises(ValueError, match="authentication failed"):
        second.decrypt(sealed, b"context")


def test_nfg_wrong_aad_is_rejected() -> None:
    cipher = NfgCipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")

    with pytest.raises(ValueError, match="authentication failed"):
        cipher.decrypt(sealed, b"wrong-context")


@pytest.mark.parametrize("offset", [0, -1])
def test_nfg_tampering_is_rejected(offset: int) -> None:
    cipher = NfgCipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")
    tampered = bytearray(sealed.ciphertext)
    tampered[offset] ^= 1

    with pytest.raises(ValueError, match="authentication failed"):
        cipher.decrypt(NfgSealedMessage(sealed.nonce, bytes(tampered)), b"context")


def test_nfg_tampered_nonce_is_rejected() -> None:
    cipher = NfgCipher(FIXED_KEY)
    sealed = cipher.encrypt_with_nonce(FIXED_NONCE, b"message", b"context")
    tampered_nonce = bytes([sealed.nonce[0] ^ 1]) + sealed.nonce[1:]

    with pytest.raises(ValueError, match="authentication failed"):
        cipher.decrypt(NfgSealedMessage(tampered_nonce, sealed.ciphertext), b"context")


def test_nfg_rejects_wrong_key_size() -> None:
    with pytest.raises(ValueError, match="32-byte key"):
        NfgCipher(b"too-short")


def test_nfg_rejects_wrong_nonce_size() -> None:
    cipher = NfgCipher(FIXED_KEY)

    with pytest.raises(ValueError, match="24 bytes"):
        cipher.encrypt_with_nonce(b"short", b"message")


def test_nfg_rejects_missing_tag() -> None:
    cipher = NfgCipher(FIXED_KEY)

    with pytest.raises(ValueError, match="16-byte tag"):
        cipher.decrypt(NfgSealedMessage(FIXED_NONCE, b"short"))


def test_nfg_nonce_reuse_exposes_plaintext_xor_failure_mode() -> None:
    cipher = NfgCipher(FIXED_KEY)
    left_plaintext = b"A" * 32
    right_plaintext = b"B" * 32
    left = cipher.encrypt_with_nonce(FIXED_NONCE, left_plaintext, b"context")
    right = cipher.encrypt_with_nonce(FIXED_NONCE, right_plaintext, b"context")

    left_body = left.ciphertext[:-NFG_TAG_SIZE]
    right_body = right.ciphertext[:-NFG_TAG_SIZE]
    xor_ciphertexts = bytes(a ^ b for a, b in zip(left_body, right_body, strict=True))
    xor_plaintexts = bytes(a ^ b for a, b in zip(left_plaintext, right_plaintext, strict=True))

    assert xor_ciphertexts == xor_plaintexts


def test_nfg_nonce_reuse_known_plaintext_recovers_other_plaintext() -> None:
    cipher = NfgCipher(FIXED_KEY)
    known_plaintext = b"known-prefix:" + b"A" * 20
    secret_plaintext = b"secret-prefix:" + b"B" * 19
    known = cipher.encrypt_with_nonce(FIXED_NONCE, known_plaintext, b"context")
    secret = cipher.encrypt_with_nonce(FIXED_NONCE, secret_plaintext, b"context")

    known_body = known.ciphertext[:-NFG_TAG_SIZE]
    secret_body = secret.ciphertext[:-NFG_TAG_SIZE]
    recovered = bytes(
        known_plaintext_item ^ known_ciphertext_item ^ secret_ciphertext_item
        for known_plaintext_item, known_ciphertext_item, secret_ciphertext_item in zip(
            known_plaintext, known_body, secret_body, strict=True
        )
    )

    assert recovered == secret_plaintext
