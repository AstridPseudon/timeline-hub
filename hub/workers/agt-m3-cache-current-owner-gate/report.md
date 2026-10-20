Implemented the exact reviewed `1d311473` delta on current `HEAD 0b2f662e` across only eight paths; all match the reviewed files byte-for-byte.

Tests:

- Targeted Agent suite with shared read-only peers: `97 passed, 23 deselected`.
- Public13 selected-cut Node neighbor using private overlay: passed; frames `[0, 3, 4, 5]`, all four refusal controls verified.
- Initial native run without peer override had environment setup errors; rerun passed.
- No full suite or repository-wide pytest run.

Verified default-off PNG fallback, fresh-callback-only public rows, source/key/hash guards, stale/forged/incomplete misses, mixed-batch isolation, private crop/statistics fallback, and preserved pixel checks. No physical pixel/PCM parity claim made.

Created:

- `commit-msg`
- Empty `DONE` marker