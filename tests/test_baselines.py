from __future__ import annotations

import pytest
from cryptography.exceptions import InvalidTag
from hypothesis import given
from hypothesis import strategies as st

from nofucksgiven.baselines import (
    AEAD_NONCE_SIZE,
    AEAD_SPECS,
    AEAD_TAG_SIZE,
    SUPPORTED_AEAD_ALGORITHMS,
    AeadAlgorithm,
    AeadCipher,
    SealedMessage,
)


@pytest.mark.parametrize("algorithm", SUPPORTED_AEAD_ALGORITHMS)
@given(
    plaintext=st.binary(min_size=0, max_size=4096),
    aad=st.binary(min_size=0, max_size=512),
)
def test_round_trip(algorithm: str, plaintext: bytes, aad: bytes) -> None:
    cipher = AeadCipher.new(algorithm)

    sealed = cipher.encrypt(plaintext, aad)

    assert len(sealed.nonce) == AEAD_NONCE_SIZE
    assert cipher.decrypt(sealed, aad) == plaintext


@pytest.mark.parametrize("algorithm", SUPPORTED_AEAD_ALGORITHMS)
def test_tampered_ciphertext_is_rejected(algorithm: str) -> None:
    cipher = AeadCipher.new(algorithm)
    sealed = cipher.encrypt(b"message", b"context")
    tampered = SealedMessage(
        sealed.nonce, sealed.ciphertext[:-1] + bytes([sealed.ciphertext[-1] ^ 1])
    )

    with pytest.raises(InvalidTag):
        cipher.decrypt(tampered, b"context")


@pytest.mark.parametrize("algorithm", SUPPORTED_AEAD_ALGORITHMS)
def test_tampered_nonce_is_rejected(algorithm: str) -> None:
    cipher = AeadCipher.new(algorithm)
    sealed = cipher.encrypt(b"message", b"context")
    tampered_nonce = bytes([sealed.nonce[0] ^ 1]) + sealed.nonce[1:]

    with pytest.raises(InvalidTag):
        cipher.decrypt(SealedMessage(tampered_nonce, sealed.ciphertext), b"context")


@pytest.mark.parametrize("algorithm", SUPPORTED_AEAD_ALGORITHMS)
def test_wrong_aad_is_rejected(algorithm: str) -> None:
    cipher = AeadCipher.new(algorithm)
    sealed = cipher.encrypt(b"message", b"context")

    with pytest.raises(InvalidTag):
        cipher.decrypt(sealed, b"wrong-context")


def test_wrong_aes_key_size_is_rejected() -> None:
    with pytest.raises(ValueError, match="32-byte key"):
        AeadCipher.new_aes_gcm(b"too-short")


def test_wrong_chacha_key_size_is_rejected() -> None:
    with pytest.raises(ValueError, match="32-byte key"):
        AeadCipher.new_chacha20_poly1305(b"too-short")


def test_wrong_aes_gcm_siv_key_size_is_rejected() -> None:
    with pytest.raises(ValueError, match="32-byte key"):
        AeadCipher.new_aes_gcm_siv(b"too-short")


def test_wrong_nonce_size_is_rejected() -> None:
    cipher = AeadCipher.new_aes_gcm()
    sealed = SealedMessage(nonce=b"short", ciphertext=b"ciphertext")

    with pytest.raises(ValueError, match="12 bytes"):
        cipher.decrypt(sealed)


def test_wrong_encrypt_nonce_size_is_rejected() -> None:
    cipher = AeadCipher.new_aes_gcm()

    with pytest.raises(ValueError, match="12 bytes"):
        cipher.encrypt_with_nonce(b"short", b"message")


def test_unknown_algorithm_is_rejected() -> None:
    with pytest.raises(ValueError, match="not-a-real-aead"):
        AeadCipher.new("not-a-real-aead")


def test_algorithm_names_are_unique() -> None:
    assert len(SUPPORTED_AEAD_ALGORITHMS) == len(set(SUPPORTED_AEAD_ALGORITHMS))
    assert set(SUPPORTED_AEAD_ALGORITHMS) == {algorithm.value for algorithm in AeadAlgorithm}
    assert set(AEAD_SPECS) == set(AeadAlgorithm)


@pytest.mark.parametrize("algorithm", AeadAlgorithm)
def test_algorithm_specs_match_runtime_behavior(algorithm: AeadAlgorithm) -> None:
    spec = AEAD_SPECS[algorithm]
    cipher = AeadCipher.new(algorithm, key=bytes(spec.key_size))
    sealed = cipher.encrypt_with_nonce(nonce=bytes(spec.nonce_size), plaintext=b"sample")

    assert cipher.name == algorithm
    assert len(cipher.key) == spec.key_size
    assert len(sealed.nonce) == spec.nonce_size
    assert len(sealed.ciphertext) == len(b"sample") + spec.tag_size
    assert spec.tag_size == AEAD_TAG_SIZE


@pytest.mark.parametrize("algorithm", SUPPORTED_AEAD_ALGORITHMS)
def test_wrong_key_is_rejected(algorithm: str) -> None:
    first = AeadCipher.new(algorithm, key=bytes(32))
    second = AeadCipher.new(algorithm, key=b"\x01" * 32)
    sealed = first.encrypt_with_nonce(nonce=bytes(12), plaintext=b"message", aad=b"context")

    with pytest.raises(InvalidTag):
        second.decrypt(sealed, b"context")


@pytest.mark.parametrize("algorithm", SUPPORTED_AEAD_ALGORITHMS)
def test_truncated_ciphertext_is_rejected(algorithm: str) -> None:
    cipher = AeadCipher.new(algorithm)
    sealed = cipher.encrypt(b"message", b"context")
    truncated = SealedMessage(sealed.nonce, sealed.ciphertext[:-1])

    with pytest.raises(InvalidTag):
        cipher.decrypt(truncated, b"context")


def test_cross_algorithm_decrypt_is_rejected() -> None:
    aes = AeadCipher.new_aes_gcm(key=bytes(32))
    chacha = AeadCipher.new_chacha20_poly1305(key=bytes(32))
    siv = AeadCipher.new_aes_gcm_siv(key=bytes(32))
    sealed = aes.encrypt_with_nonce(nonce=bytes(12), plaintext=b"message", aad=b"context")

    with pytest.raises(InvalidTag):
        chacha.decrypt(sealed, b"context")

    with pytest.raises(InvalidTag):
        siv.decrypt(sealed, b"context")


def test_aes_gcm_256_known_answer_vector() -> None:
    # NIST SP 800-38D, AES-GCM test case with zero-length plaintext and AAD.
    cipher = AeadCipher.new_aes_gcm(key=bytes(32))

    sealed = cipher.encrypt_with_nonce(nonce=bytes(12), plaintext=b"", aad=b"")

    assert sealed.ciphertext.hex() == "530f8afbc74536b9a963b4f1c4cb738b"
    assert cipher.decrypt(sealed) == b""


def test_chacha20_poly1305_known_answer_vector() -> None:
    # RFC 8439, section 2.8.2 AEAD_CHACHA20_POLY1305 example.
    cipher = AeadCipher.new_chacha20_poly1305(
        key=bytes.fromhex("808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f")
    )
    nonce = bytes.fromhex("070000004041424344454647")
    aad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
    plaintext = bytes.fromhex(
        "4c616469657320616e642047656e746c656d656e206f662074686520636c61737320"
        "6f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c7920"
        "6f6e652074697020666f7220746865206675747572652c2073756e73637265656e20"
        "776f756c642062652069742e"
    )

    sealed = cipher.encrypt_with_nonce(nonce=nonce, plaintext=plaintext, aad=aad)

    assert sealed.ciphertext.hex() == (
        "d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d"
        "63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b"
        "3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d"
        "7bc3ff4def08e4b7a9de576d26586cec64b61161ae10b594f09e26a7e902ecbd"
        "0600691"
    )
    assert cipher.decrypt(sealed, aad) == plaintext
