"""NFG-v0 toy symmetric encryption experiment.

NFG-v0 is a research scaffold, not a serious cipher. It combines:

- HMAC-SHA-256 based key separation.
- HMAC-SHA-256 based counter-mode keystream blocks.
- Encrypt-then-MAC authentication with a truncated HMAC tag.

This shape is useful for local tests because it has concrete keys, nonces,
associated data, tags, and failure modes. It is not a substitute for public
cryptanalysis, standardized AEADs, or production libraries.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import os
from typing import Final


NFG_KEY_SIZE: Final = 32
NFG_NONCE_SIZE: Final = 24
NFG_TAG_SIZE: Final = 16
NFG_AAD_LIMIT: Final = 2**32 - 1
_BLOCK_SIZE: Final = 32
_VERSION: Final = b"NFG-v0"
_ENC_LABEL: Final = b"NFG-v0/enc"
_MAC_LABEL: Final = b"NFG-v0/mac"
_STREAM_LABEL: Final = b"NFG-v0/stream"


@dataclass(frozen=True)
class NfgSealedMessage:
    """Nonce and ciphertext-plus-tag returned by NFG-v0."""

    nonce: bytes
    ciphertext: bytes


class NfgCipher:
    """Experimental NFG-v0 encrypt-then-MAC construction."""

    def __init__(self, key: bytes) -> None:
        if len(key) != NFG_KEY_SIZE:
            raise ValueError("NFG-v0 requires a 32-byte key")
        self.key = key
        self._enc_key = _derive_key(key, _ENC_LABEL)
        self._mac_key = _derive_key(key, _MAC_LABEL)

    @classmethod
    def new(cls, key: bytes | None = None) -> NfgCipher:
        return cls(key if key is not None else os.urandom(NFG_KEY_SIZE))

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> NfgSealedMessage:
        return self.encrypt_with_nonce(os.urandom(NFG_NONCE_SIZE), plaintext, aad)

    def encrypt_with_nonce(
        self, nonce: bytes, plaintext: bytes, aad: bytes = b""
    ) -> NfgSealedMessage:
        if len(nonce) != NFG_NONCE_SIZE:
            raise ValueError("NFG-v0 nonce must be 24 bytes")
        _validate_aad(aad)
        stream = _keystream(self._enc_key, nonce, len(plaintext))
        body = _xor_bytes(plaintext, stream)
        tag = _tag(self._mac_key, nonce, aad, body)
        return NfgSealedMessage(nonce=nonce, ciphertext=body + tag)

    def decrypt(self, sealed: NfgSealedMessage, aad: bytes = b"") -> bytes:
        if len(sealed.nonce) != NFG_NONCE_SIZE:
            raise ValueError("NFG-v0 nonce must be 24 bytes")
        _validate_aad(aad)
        if len(sealed.ciphertext) < NFG_TAG_SIZE:
            raise ValueError("NFG-v0 ciphertext must include a 16-byte tag")
        body = sealed.ciphertext[:-NFG_TAG_SIZE]
        tag = sealed.ciphertext[-NFG_TAG_SIZE:]
        expected = _tag(self._mac_key, sealed.nonce, aad, body)
        if not hmac.compare_digest(tag, expected):
            raise ValueError("NFG-v0 authentication failed")
        stream = _keystream(self._enc_key, sealed.nonce, len(body))
        return _xor_bytes(body, stream)


def _validate_aad(aad: bytes) -> None:
    if len(aad) > NFG_AAD_LIMIT:
        raise ValueError("NFG-v0 AAD is too large for this scaffold")


def _derive_key(key: bytes, label: bytes) -> bytes:
    return hmac.digest(key, label, hashlib.sha256)


def _keystream(enc_key: bytes, nonce: bytes, size: int) -> bytes:
    output = bytearray()
    counter = 0
    while len(output) < size:
        block_input = _STREAM_LABEL + nonce + counter.to_bytes(8, "big")
        output.extend(hmac.digest(enc_key, block_input, hashlib.sha256))
        counter += 1
    return bytes(output[:size])


def _tag(mac_key: bytes, nonce: bytes, aad: bytes, body: bytes) -> bytes:
    aad_len = len(aad).to_bytes(8, "big")
    body_len = len(body).to_bytes(8, "big")
    material = b"|".join([_VERSION, nonce, aad_len, aad, body_len, body])
    return hmac.digest(mac_key, material, hashlib.sha256)[:NFG_TAG_SIZE]


def _xor_bytes(left: bytes, right: bytes) -> bytes:
    return bytes(left_item ^ right_item for left_item, right_item in zip(left, right, strict=True))
