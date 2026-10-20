# Runtime native clip parity final review

## Decision

**APPROVE** the `runtime-clip-native-parity-fixed.md` design review for
`1f75756cfe2f391397e6e3282a81c6e50c3eb567` (`test(runtime): strengthen native
clip replacement parity`). This approves the test evidence and coverage
mapping only; it does not merge the change or claim ledger D04 complete.

## Coverage mapping

| Original behavior | Native evidence | Review result |
| --- | --- | --- |
| Atomic replacement, exact replay | `test_native_clip_swap_is_atomic_cas_and_exactly_replayable` checks the exact internal target/registry payload, untouched parent clip/config/registry and shot payload, receipt result/kind, one event and ledger deltas, CAS-corrupted exact retry, changed-key `idempotency_mismatch`, and relevant-target stale refusal. | Covered |
| Cross-project source refusal | `test_native_clip_swap_rejects_cross_project_source_without_mutation` uses a real foreign selection and compares the complete SQLite dump. | Covered |
| Malformed source refusal | `test_native_clip_swap_rejects_malformed_source_before_native_commit` sends an unsealed public native swap through `commit_timeline`; the malformed catalog fingerprint is rejected with rows and head unchanged. | Covered at backend commit |
| Tampered CAS refusal | Existing native tampered-CAS and selected-source capture-race tests remain in place, including the already-approved CAS fix. | Covered; CAS ownership remains separate |
| Wrong stream refusal | `test_native_clip_swap_rejects_wrong_stream_without_mutation` sends a real verified audio selection through the native commit path and checks rows/head unchanged. | Covered at backend commit |
| Too-short source and authored-end refusal | The parametrized native commit test exercises duration `1` and `3.5`, with zero-write rows/head assertions. | Covered at backend commit |
| Generic visual media | The original audio refusal remains unchanged. `test_native_generic_visual_media_accepts_verified_image_swap` replaces a generic `clipType='media'` row with two verified `image/png` selections and asserts the hold-only row shape. | Covered in both refusal and supported-positive directions |
| Intervening edit and reopen retry | `test_native_clip_swap_replays_after_intervening_edit_and_reopen` retries the exact request after reopen and checks the post-reopen head plus receipt/event counts. | Covered |
| Public HTTP route | `test_native_clip_swap_public_http_route` checks the accepted response body, receipt/result/event identity, project/key/request identity, and exact HTTP retry. | Covered |

The additional `test_native_clip_swap_rebases_after_disjoint_intervening_edit`
proves stale disjoint acceptance/rebase while preserving the replacement and
the intervening parent edit; this is distinct from relevant-target conflict and
idempotent replay.

## Authority and preservation checks

- The ten original `test_replace_timeline_clip_*` function bodies are
  byte-for-byte unchanged from the pre-fix parent, and the existing strict
  `retired_writer` xfail marker is unchanged.
- Main Agent’s public media authority accepts verified `image/*` and
  `video/*` selections (`astrid/sdk/timeline/_media_inputs.py`), and its media
  command accepts `clipType='media'` for `kind == 'image'` while requiring a
  hold-only image row (`astrid/sdk/timeline/native_occurrence_media_commands.py`).
  The candidate uses actual Runtime `image/png` imports, public selection and
  verified-media reads, so the image positive does not introduce an unsupported
  asset type or bypass capture authority.
- The changed cases reach `service.commit_timeline` (and the HTTP case reaches
  the public `/v1` client route); they are not capture-only refusal tests.

## Evidence

- Direct non-HTTP targeted run, with shared dependencies read-only and pytest
  cache disabled: **12 passed, 11 deselected, 1 xfailed**. The xfail is the
  pre-existing parent `clip.swap-media` public-schema incompatibility.
- Central HTTP-node targeted run for the candidate: **13 passed, 10
  deselected, 1 xfailed** in 23.33s, with the same pre-existing xfail.
- `compile(...)` of `tests/test_timeline_clip_replacement.py`: passed.
- `git diff --check 1f75756^ HEAD -- tests/test_timeline_clip_replacement.py`:
  passed.
- No full suite, broad suite, render suite, or D04 completion claim was made.

## Limits

The parent-owned `clip.swap-media` route remains unqualified because the
current public Runtime schema excludes that ownership and the existing strict
xfail records it. This review does not qualify App popup adoption, a full
cross-repository journey, or the whole D04 ledger. Those remain integration
manager responsibilities.
