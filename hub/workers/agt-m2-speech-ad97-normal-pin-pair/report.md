Implemented WC5 managed speech seam changes:

- Restored normal014 SDK client/lock bytes (`a0dca169…`, artifact `f021e771…`).
- Kept exact ad97 Runtime archive selection read-only.
- Updated fixture output to `audio` so ad97 derives WAV duration.
- Bound fixture executor to `astrid-pack-host`.
- No Runtime/API/adapter changes.

Tests:

- Draft voiceover: 23 passed.
- Projectless admission: 19 passed.
- Vendor lock/client parity: 29 passed.
- Neighbor publication tests: 1 passed, 2 skipped.
- Central two-node integration rerun remains `running`; qualification is unverified. Initial run failed pre-test due executor credential mismatch, now corrected.

Created commit message and `DONE`. Outer authoring remains a test double; no full D13/WC5 claim.