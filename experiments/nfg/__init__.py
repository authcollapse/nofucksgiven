"""NFG experimental symmetric encryption scaffold.

This package is for research experiments only. It is not a production cipher.
"""

from .cipher import (
    NFG_AAD_LIMIT,
    NFG_KEY_SIZE,
    NFG_NONCE_SIZE,
    NFG_TAG_SIZE,
    NfgCipher,
    NfgSealedMessage,
)
from .datasets import DatasetCase, load_dataset_cases
from .v1 import NfgV1Cipher, NfgV1SealedMessage

__all__ = [
    "NFG_AAD_LIMIT",
    "NFG_KEY_SIZE",
    "NFG_NONCE_SIZE",
    "NFG_TAG_SIZE",
    "DatasetCase",
    "NfgCipher",
    "NfgSealedMessage",
    "NfgV1Cipher",
    "NfgV1SealedMessage",
    "load_dataset_cases",
]
