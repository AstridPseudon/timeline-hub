D88 blocked: workers/rt-D88-digest-chain-sol-0044/BLOCKED and evidence/status.json report a security failure in the held prototype and a subsequent automatic safety-review denial (possible cybersecurity risk). The reviewer stopped; no retry, alternate route, merge or release is authorized. Existing Runtime a3cd remains released. Decision owed: resolve the conflict between unchanged public-hash event authentication and the requested forged-attestation guarantee through the approved process. No further D88 security work dispatched. Evidence: workers/rt-D88-digest-chain-sol-0044/report.md and evidence/status.json.

## Orchestrator decision (01:10Z): D88b
- **D88b, D88 WITHDRAWN; replaced by a replay memo keyed by the RECOMPUTED content digest (01:10Z), deciding escalation runtime-20261025T0104Z-D88-safety-and-integrity:**
  - **Why D88 is withdrawn:** the independent review proved its premise false. Event "authentication" is an unkeyed public SHA-256, so someone who can write the store can change the step patches AND recompute the hashes. The D88 attested read accepted that forgery; today's full replay rejects it. **D88 would weaken a protection we have, so it is NOT merged.** The held prototype stays held. The reviewer was correct.
  - **D88b, the replacement:** keep full replay as the integrity check, and stop REPEATING it for bytes it has already proven.
    - It is an in-process (never persisted) memo of "replay verified OK".
    - The memo is keyed by `(ordinal, entry_digest, chain_digest_through_previous)`, all RECOMPUTED from the stored bytes at read time, never read from a stored attestation.
    - Any change to an entry or to anything before it changes the key, so the lookup misses and full replay runs, rejecting the forgery exactly as today.
    - Evading it would require a SHA-256 collision.
    - The memo is cleared on restart, on any refusal, and on any store write outside accept.
    - The head pair is still CAS-checked, and every fresh-request predicate still runs.
    - Total cost becomes O(N) per process instead of O(N) per request.
  - **Security review scope:** confirm the key is recomputed from stored bytes, includes the chain, and that nothing outside the key influences the replay result. Demonstrate with the EXISTING rejected-forgery fixture: it must still be rejected after the memo is warm. No new exploit tooling is needed; reuse the retained witness.
  - **The safety-review stop is reported to the owner** and not routed around. The new review needs no new attack construction.
  - **Owner:** one HARD Sol (resume rt-D88 branch WIP for the curve harness only), then one independent security review.
