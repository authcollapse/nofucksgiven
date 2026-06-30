"""NFG-v1 toy symmetric encryption experiment.

NFG-v1 exists to test whether a keyed-BLAKE2s construction is a faster local
research scaffold than NFG-v0. It is not a production cipher and it has not had
public cryptanalysis.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import os
from typing import Final

from experiments.nfg.cipher import NFG_AAD_LIMIT, NFG_KEY_SIZE, NFG_NONCE_SIZE, NFG_TAG_SIZE


_VERSION: Final = b"NFG-v1"
_BLOCK_SIZE: Final = 32
_ENC_PERSON: Final = b"NFGv1enc"
_MAC_PERSON: Final = b"NFGv1mac"
_STREAM_PERSON: Final = b"NFGv1str"
_TAG_PERSON: Final = b"NFGv1tag"


@dataclass(frozen=True)
class NfgV1SealedMessage:
    """Nonce and ciphertext-plus-tag returned by NFG-v1."""

    nonce: bytes
    ciphertext: bytes


class NfgV1Cipher:
    """Experimental NFG-v1 keyed-BLAKE2s encrypt-then-MAC construction."""

    def __init__(self, key: bytes) -> None:
        if len(key) != NFG_KEY_SIZE:
            raise ValueError("NFG-v1 requires a 32-byte key")
        self.key = key
        self._enc_key = _derive_key(key, _ENC_PERSON)
        self._mac_key = _derive_key(key, _MAC_PERSON)

    @classmethod
    def new(cls, key: bytes | None = None) -> NfgV1Cipher:
        return cls(key if key is not None else os.urandom(NFG_KEY_SIZE))

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> NfgV1SealedMessage:
        return self.encrypt_with_nonce(os.urandom(NFG_NONCE_SIZE), plaintext, aad)

    def encrypt_with_nonce(
        self, nonce: bytes, plaintext: bytes, aad: bytes = b""
    ) -> NfgV1SealedMessage:
        if len(nonce) != NFG_NONCE_SIZE:
            raise ValueError("NFG-v1 nonce must be 24 bytes")
        _validate_aad(aad)
        stream = _keystream(self._enc_key, nonce, len(plaintext))
        body = _xor_bytes(plaintext, stream)
        tag = _tag(self._mac_key, nonce, aad, body)
        return NfgV1SealedMessage(nonce=nonce, ciphertext=body + tag)

    def decrypt(self, sealed: NfgV1SealedMessage, aad: bytes = b"") -> bytes:
        if len(sealed.nonce) != NFG_NONCE_SIZE:
            raise ValueError("NFG-v1 nonce must be 24 bytes")
        _validate_aad(aad)
        if len(sealed.ciphertext) < NFG_TAG_SIZE:
            raise ValueError("NFG-v1 ciphertext must include a 16-byte tag")
        body = sealed.ciphertext[:-NFG_TAG_SIZE]
        tag = sealed.ciphertext[-NFG_TAG_SIZE:]
        expected = _tag(self._mac_key, sealed.nonce, aad, body)
        if not hmac.compare_digest(tag, expected):
            raise ValueError("NFG-v1 authentication failed")
        stream = _keystream(self._enc_key, sealed.nonce, len(body))
        return _xor_bytes(body, stream)


def _validate_aad(aad: bytes) -> None:
    if len(aad) > NFG_AAD_LIMIT:
        raise ValueError("NFG-v1 AAD is too large for this scaffold")


def _derive_key(key: bytes, person: bytes) -> bytes:
    return hashlib.blake2s(key=key, person=person, digest_size=_BLOCK_SIZE).digest()


def _keystream(enc_key: bytes, nonce: bytes, size: int) -> bytes:
    output = bytearray()
    counter = 0
    while len(output) < size:
        block = hashlib.blake2s(key=enc_key, person=_STREAM_PERSON, digest_size=_BLOCK_SIZE)
        block.update(nonce)
        block.update(counter.to_bytes(8, "big"))
        output.extend(block.digest())
        counter += 1
    return bytes(output[:size])


def _tag(mac_key: bytes, nonce: bytes, aad: bytes, body: bytes) -> bytes:
    digest = hashlib.blake2s(key=mac_key, person=_TAG_PERSON, digest_size=NFG_TAG_SIZE)
    digest.update(_VERSION)
    digest.update(nonce)
    digest.update(len(aad).to_bytes(8, "big"))
    digest.update(aad)
    digest.update(len(body).to_bytes(8, "big"))
    digest.update(body)
    return digest.digest()


def _xor_bytes(left: bytes, right: bytes) -> bytes:
    if len(left) != len(right):
        raise ValueError("NFG-v1 XOR inputs must have equal length")
    if not left:
        return b""
    return (int.from_bytes(left, "big") ^ int.from_bytes(right, "big")).to_bytes(len(left), "big")
