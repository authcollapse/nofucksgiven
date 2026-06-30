# Safety Notes

- Do not use experimental algorithms from this repository to protect real data.
- Prefer audited, standard libraries for real systems.
- Never reuse an AEAD nonce with the same key.
- Keep benchmarks separate from security claims.
- Require known-answer tests, property tests, and tamper tests for every primitive wrapper.
- Require public review and formal cryptanalysis before making any replacement claims.
