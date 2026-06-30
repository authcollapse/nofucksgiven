from __future__ import annotations

import pytest
from cryptography.exceptions import InvalidTag
from hypothesis import given
from hypothesis import strategies as st

from nofucksgiven.baselines import AEAD_NONCE_SIZE, AeadCipher, SealedMessage


@pytest.mark.parametrize(
    "factory",
    [AeadCipher.new_aes_gcm, AeadCipher.new_chacha20_poly1305],
)
@given(
    plaintext=st.binary(min_size=0, max_size=4096),
    aad=st.binary(min_size=0, max_size=512),
)
def test_round_trip(factory, plaintext: bytes, aad: bytes) -> None:
    cipher = factory()

    sealed = cipher.encrypt(plaintext, aad)

    assert len(sealed.nonce) == AEAD_NONCE_SIZE
    assert cipher.decrypt(sealed, aad) == plaintext


@pytest.mark.parametrize(
    "factory",
    [AeadCipher.new_aes_gcm, AeadCipher.new_chacha20_poly1305],
)
def test_tampered_ciphertext_is_rejected(factory) -> None:
    cipher = factory()
    sealed = cipher.encrypt(b"message", b"context")
    tampered = SealedMessage(sealed.nonce, sealed.ciphertext[:-1] + b"\x00")

    with pytest.raises(InvalidTag):
        cipher.decrypt(tampered, b"context")


@pytest.mark.parametrize(
    "factory",
    [AeadCipher.new_aes_gcm, AeadCipher.new_chacha20_poly1305],
)
def test_wrong_aad_is_rejected(factory) -> None:
    cipher = factory()
    sealed = cipher.encrypt(b"message", b"context")

    with pytest.raises(InvalidTag):
        cipher.decrypt(sealed, b"wrong-context")


def test_wrong_aes_key_size_is_rejected() -> None:
    with pytest.raises(ValueError, match="32-byte key"):
        AeadCipher.new_aes_gcm(b"too-short")


def test_wrong_chacha_key_size_is_rejected() -> None:
    with pytest.raises(ValueError, match="32-byte key"):
        AeadCipher.new_chacha20_poly1305(b"too-short")


def test_wrong_nonce_size_is_rejected() -> None:
    cipher = AeadCipher.new_aes_gcm()
    sealed = SealedMessage(nonce=b"short", ciphertext=b"ciphertext")

    with pytest.raises(ValueError, match="12 bytes"):
        cipher.decrypt(sealed)
