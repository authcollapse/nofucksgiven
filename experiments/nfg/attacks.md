# NFG-v0 Failure Notes

NFG-v0 is a toy construction. These notes track what breaks or remains outside
the experiment.

## Nonce Reuse

NFG-v0 uses a stream-style XOR body. Reusing the same key and nonce reuses the
same keystream. The tests demonstrate two consequences:

- XORing two ciphertext bodies produced under the same key and nonce reveals the
  XOR of the plaintexts.
- If one plaintext is known, the matching bytes of another plaintext can be
  recovered.

Different AAD changes the tag, but it does not save confidentiality when the
same key and nonce are reused.

## Zero Plaintext

Encrypting zero bytes under a fixed key and nonce exposes the keystream for that
key and nonce. This is expected for stream-style constructions and is dangerous
when paired with nonce reuse.

## Replay

The same sealed message decrypts repeatedly. NFG-v0 does not provide replay
protection. Protocol state or sequence numbers in AAD would be required to study
that behavior.

## Current Non-Claims

- No side-channel review.
- No proof.
- No public cryptanalysis.
- No misuse-resistance claim.
- No production deployment story.
- No claim that local statistical checks imply security.
