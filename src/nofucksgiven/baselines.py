"""Vetted baseline AEAD wrappers for experiments.

The wrappers here intentionally use established primitives from cryptography.
They are reference points for tests and benchmarks, not novel algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass
from os import urandom

from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305


AES_GCM_KEY_SIZE = 32
CHACHA20_POLY1305_KEY_SIZE = 32
AEAD_NONCE_SIZE = 12


@dataclass(frozen=True)
class SealedMessage:
    """Nonce and ciphertext returned by an AEAD encryption operation."""

    nonce: bytes
    ciphertext: bytes


class AeadCipher:
    """Small AEAD adapter with generated nonces and strict input sizes."""

    def __init__(self, algorithm: AESGCM | ChaCha20Poly1305, key: bytes) -> None:
        self._algorithm = algorithm
        self.key = key

    @classmethod
    def new_aes_gcm(cls, key: bytes | None = None) -> AeadCipher:
        key = key if key is not None else AESGCM.generate_key(bit_length=256)
        if len(key) != AES_GCM_KEY_SIZE:
            raise ValueError("AES-GCM requires a 32-byte key in this scaffold")
        return cls(AESGCM(key), key)

    @classmethod
    def new_chacha20_poly1305(cls, key: bytes | None = None) -> AeadCipher:
        key = key if key is not None else ChaCha20Poly1305.generate_key()
        if len(key) != CHACHA20_POLY1305_KEY_SIZE:
            raise ValueError("ChaCha20-Poly1305 requires a 32-byte key")
        return cls(ChaCha20Poly1305(key), key)

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> SealedMessage:
        nonce = urandom(AEAD_NONCE_SIZE)
        ciphertext = self._algorithm.encrypt(nonce, plaintext, aad)
        return SealedMessage(nonce=nonce, ciphertext=ciphertext)

    def decrypt(self, sealed: SealedMessage, aad: bytes = b"") -> bytes:
        if len(sealed.nonce) != AEAD_NONCE_SIZE:
            raise ValueError("AEAD nonce must be 12 bytes")
        return self._algorithm.decrypt(sealed.nonce, sealed.ciphertext, aad)
