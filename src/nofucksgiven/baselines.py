"""Vetted baseline AEAD wrappers for experiments.

The wrappers here intentionally use established primitives from cryptography.
They are reference points for tests and benchmarks, not novel algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305


AES_GCM_KEY_SIZE = 32
CHACHA20_POLY1305_KEY_SIZE = 32
AEAD_NONCE_SIZE = 12
AEAD_TAG_SIZE = 16


class AeadAlgorithm(StrEnum):
    """Supported AEAD baselines."""

    AES_GCM_256 = "aes-gcm-256"
    CHACHA20_POLY1305 = "chacha20-poly1305"


@dataclass(frozen=True)
class AeadSpec:
    """Metadata used by tests and benchmark reporting."""

    name: AeadAlgorithm
    key_size: int
    nonce_size: int
    tag_size: int


AEAD_SPECS = {
    AeadAlgorithm.AES_GCM_256: AeadSpec(
        name=AeadAlgorithm.AES_GCM_256,
        key_size=AES_GCM_KEY_SIZE,
        nonce_size=AEAD_NONCE_SIZE,
        tag_size=AEAD_TAG_SIZE,
    ),
    AeadAlgorithm.CHACHA20_POLY1305: AeadSpec(
        name=AeadAlgorithm.CHACHA20_POLY1305,
        key_size=CHACHA20_POLY1305_KEY_SIZE,
        nonce_size=AEAD_NONCE_SIZE,
        tag_size=AEAD_TAG_SIZE,
    ),
}
SUPPORTED_AEAD_ALGORITHMS = tuple(algorithm.value for algorithm in AeadAlgorithm)


@dataclass(frozen=True)
class SealedMessage:
    """Nonce and ciphertext returned by an AEAD encryption operation."""

    nonce: bytes
    ciphertext: bytes


class AeadCipher:
    """Small AEAD adapter with generated nonces and strict input sizes."""

    def __init__(
        self,
        name: AeadAlgorithm,
        algorithm: AESGCM | ChaCha20Poly1305,
        key: bytes,
    ) -> None:
        self.name = name
        self._algorithm = algorithm
        self.key = key

    @classmethod
    def new(cls, name: AeadAlgorithm | str, key: bytes | None = None) -> AeadCipher:
        algorithm = AeadAlgorithm(name)
        if algorithm is AeadAlgorithm.AES_GCM_256:
            return cls.new_aes_gcm(key)
        if algorithm is AeadAlgorithm.CHACHA20_POLY1305:
            return cls.new_chacha20_poly1305(key)
        raise ValueError(f"unsupported AEAD algorithm: {name}")

    @classmethod
    def new_aes_gcm(cls, key: bytes | None = None) -> AeadCipher:
        key = key if key is not None else AESGCM.generate_key(bit_length=256)
        if len(key) != AES_GCM_KEY_SIZE:
            raise ValueError("AES-GCM requires a 32-byte key in this scaffold")
        return cls(AeadAlgorithm.AES_GCM_256, AESGCM(key), key)

    @classmethod
    def new_chacha20_poly1305(cls, key: bytes | None = None) -> AeadCipher:
        key = key if key is not None else ChaCha20Poly1305.generate_key()
        if len(key) != CHACHA20_POLY1305_KEY_SIZE:
            raise ValueError("ChaCha20-Poly1305 requires a 32-byte key")
        return cls(AeadAlgorithm.CHACHA20_POLY1305, ChaCha20Poly1305(key), key)

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> SealedMessage:
        nonce = os.urandom(AEAD_NONCE_SIZE)
        return self.encrypt_with_nonce(nonce, plaintext, aad)

    def encrypt_with_nonce(self, nonce: bytes, plaintext: bytes, aad: bytes = b"") -> SealedMessage:
        """Encrypt with an explicit nonce for test vectors and controlled experiments."""
        if len(nonce) != AEAD_NONCE_SIZE:
            raise ValueError("AEAD nonce must be 12 bytes")
        ciphertext = self._algorithm.encrypt(nonce, plaintext, aad)
        return SealedMessage(nonce=nonce, ciphertext=ciphertext)

    def decrypt(self, sealed: SealedMessage, aad: bytes = b"") -> bytes:
        if len(sealed.nonce) != AEAD_NONCE_SIZE:
            raise ValueError("AEAD nonce must be 12 bytes")
        return self._algorithm.decrypt(sealed.nonce, sealed.ciphertext, aad)
