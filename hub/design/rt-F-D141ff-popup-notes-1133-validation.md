# D141ff popup note validation

Status: **PASS_PRIVATE_D141FF_CANDIDATES**.

- Canonical README and gate-results preimages matched the required hashes and remained regular `0644` non-symlinks.
- Both candidates conserve the complete preimage byte prefix and add only the bounded D141ff popup suffix once.
- The previous known gaps, 32-ID table, ledger/witness/limits, and C0 prose remain in the conserved prefix.
- All eight hash-exact D141cc originals matched their published SHA-256 bindings.
- Controlled `delivery-build.render_readme` was exercised as a function only with four controlled repository records; placeholders resolved, fences balanced, and the fallback was checked.
- Popup result 27026 is retained as genuine service FAIL (readiness PASS, popup FAIL, missing shared-occurrence label within 5 s, cause UNKNOWN). Original 1368 is retained as a pointer; cancelled 13234/20413 have no functional verdict. No custodyPASS is claimed.
- The first-tool sampler coverage gap is recorded in `sampler-lifecycle.json`; the restarted sampler records its own PID and terminal lifecycle.

No canonical write, installation, build, service, diagnostic, product test, or full suite was run.
