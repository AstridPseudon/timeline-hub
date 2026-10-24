## Result

Read-only D30 review complete. No product files changed.

Base verified: `c0fe88994405fd517b58473c14678a0d1b73056d`, tree `8e3ef15ee5f7c08381d8dc9efb38b5c98845466d`.

### Popup A3/P2

- PASS — Retained trace shows fork + add-media targeting newly created `V3`, despite raw child tracks only `plate` and `V2`.
- PASS — Runtime returned the exact pre-execution `422 validation_error` for missing active raw visual child track.
- PASS — Cause is the generic planner’s occupied-track fallback: `findNearestFreeTrack` selects another track or creates `V3`.
- PASS, bounded — Preserving occupied `V2` satisfies the existing structural provider contract. Current validation and frozen SDK lowering impose no clip-overlap rejection; they require an active visual child track and append the clip.
- PASS — C0-created claims are separate from the actual planner defect.
- FAIL, oracle gap — Existing Proof equality at `three-products.p2-popup.spec.ts:464` omits required `created`. Preserve all existing field assertions and separately assert the exact created refs; for the fresh add case source predicts asset then clip refs:
  `occurrence:<owner>/asset:<media.asset>`, `occurrence:<owner>/clip:<row.id>`.

A3 owns the scoped planner repair and its occupied-V2 acceptance proof.

### Parent A2/P2

- PASS — Trace establishes a real local display move from `0` to `5` seconds.
- PASS — Trace records zero commit POSTs and 16 successful `/inspect` responses.
- PASS — Current source chain includes the 19c parent-move validation and capture path.
- PASS — No retained diagnostics distinguish local mutation, owner readiness, capture, outbox, or transport.
- PASS — Correct conclusion is PRECISE UNKNOWN before transport; no source fix is justified from speculative basis/owner-wait theories.
- PASS — Existing direct-injection coverage is not mounted pointer-capture proof.

Sol0511 owns the bounded offline mounted-save reproduction.

### Verification

Read-only checks passed:

- `git diff --check`
- `git status --porcelain=v1 --untracked-files=all` — clean
- source/ref inspection via `git show`
- retained popup trace SHA256 matched `b6bcddfa13da1660743bc72e25f69841c6c9d57d161d417302d150c16c36de1c`

No tests, browser, HTTP, backend, service, full suite, or original rerun performed per task constraints. Commit message and `DONE` marker were written.