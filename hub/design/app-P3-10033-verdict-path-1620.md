# NO-GO — concrete cause

D66 P3 failed before the reset journey:

- Retained run: `d66-plain-p3-three-products`, exit 1 / 286s.
- Readiness: 1 passed.
- Gate 5: failed at `gate5-reset-precondition.ts:382`, first mismatch: authoritative history.
- Reached: gesture → App outbox → generated `POST /commit` → Runtime accepted response → authenticated history lookup → canonical document/head checks.
- Unreached: reset POST, lost-ACK flow, restart, retry, and undo.

Cause: Runtime D62 emits authenticated `HistoryEntry.recorder_abi`; this v2 patch has physical bindings, so the value is `2`. The exact Gate-5 oracle omits `recorder_abi` from its expected history object. P1 passes because its broader history matcher tolerates extra fields.

Evidence:

- D66 manifest identities and SHA/original-hash assertions are consistent; test hashes are unchanged before/after.
- P1 retained run passed 2/2 tests on the identical app tree `a3b3b978...`.
- Pinned Runtime `8b32...` adds `recorder_abi` during publish and projects it in authenticated history.
- No raw trace, URLs, authentication data, or request/body export was inspected.

Checks performed:

- `git diff --check` — passed.
- `git status --short --branch` — clean.
- No tests rerun; source was unchanged.

Recommended next step: independent review of the Gate-5 oracle update to include optional authenticated `recorder_abi` handling. No product or test files were modified.