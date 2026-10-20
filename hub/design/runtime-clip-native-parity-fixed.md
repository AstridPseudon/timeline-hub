# Runtime native clip-replacement parity fix

## Result

Strengthened `tests/test_timeline_clip_replacement.py` only. The original ten
legacy assertions are unchanged byte-for-byte. The existing parent-route
schema xfail remains the only xfail; the approved CAS integrity coverage from
3021 is retained and passes.

## Original -> native coverage

| Original behavior | Native evidence |
|---|---|
| `test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable` | `test_native_clip_swap_is_atomic_cas_and_exactly_replayable`: exact target payload, untouched parent rows/config/registry, receipt kind/result, one event, ledger/event count deltas, CAS-corruption exact replay, and changed-key `idempotency_mismatch`. |
| `test_replace_timeline_clip_rejects_cross_project_source` | `test_native_clip_swap_rejects_cross_project_source_without_mutation`: real foreign project selection and full SQLite dump equality. |
| `test_replace_timeline_clip_rejects_malformed_source_without_mutation` | `test_native_clip_swap_rejects_malformed_source_before_native_commit`: actual native commit with an unsealed public command carrying a malformed real selection; full rows and head unchanged. |
| `test_replace_timeline_clip_rejects_tampered_cas_without_mutation` | `test_native_clip_swap_rejects_tampered_cas_without_mutation` plus the 3021 selected-CAS race test; retained, no new xfail. |
| `test_replace_timeline_clip_rejects_wrong_stream_without_mutation` | `test_native_clip_swap_rejects_wrong_stream_without_mutation`: actual commit against an owned target using a real verified audio selection; rows/head unchanged. |
| `test_replace_timeline_clip_rejects_too_short_source_without_mutation` | Duration `1` case in `test_native_clip_swap_rejects_too_short_or_end_short_source`; actual commit and zero-write checks. |
| `test_replace_timeline_clip_requires_source_to_reach_authored_end` | Duration `3.5` case in the same test; actual authored-end commit rejection and zero-write checks. |
| `test_replace_timeline_clip_generic_visual_media_requires_video_stream` | Original refusal remains unchanged. Native audio refusal remains separate; `test_native_generic_visual_media_accepts_verified_image_swap` is the truthful known-type positive using verified `image/png` selections A and B and a hold-only `clipType='media'` row. No video-only restriction is claimed for generic image media. |
| `test_replace_timeline_clip_replays_after_intervening_edit_and_reopen` | `test_native_clip_swap_replays_after_intervening_edit_and_reopen`: exact retry after reopen with post-reopen head and event/receipt counts. |
| `test_replace_timeline_clip_public_http_route` | `test_native_clip_swap_public_http_route`: public `/v1` response receipt/result/event identity, request identity, exact retry, target and untouched-row assertions. |

Additional native coverage is `test_native_clip_swap_rebases_after_disjoint_intervening_edit`, distinct from the target-overlap 409 and exact replay cases; it asserts `status == 'rebased'`, the intervening publication, and the exact replacement.

## Evidence

- Direct non-HTTP targeted command, using read-only shared `venv-runtime` plus
  `venv-agent` with `jsonschema`, and the frozen ordinary Agent source:
  `ASTRID_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source PYTHONPATH=.:packages/python:/home/user/work/venv-agent/lib/python3.11/site-packages:/home/user/work/venv-runtime/lib/python3.11/site-packages /home/user/work/venv-runtime/bin/python -m pytest tests/test_timeline_clip_replacement.py -m integration -q --disable-warnings --tb=short -k 'not public_http_route'`
  -> **12 passed, 1 xfailed**.
- Central integration run with the actual HTTP node:
  `request-test rt-m2-clip-native-parity-fix capture-agentcf7448-integration --files 'tests/test_timeline_clip_replacement.py'`, whose runner executed `.../venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_clip_replacement.py`
  -> **13 passed, 1 existing xfailed, 10 deselected** in 23.33s.
- `python -m py_compile tests/test_timeline_clip_replacement.py` -> passed.
- `git diff --check` -> passed.
- No full, broad, render, or unrelated suite was run.

## Limits / handoff

- The parent-media route remains the pre-existing public-schema xfail for
  `clip.swap-media` ownership; it was not widened or changed.
- The direct local HTTP attempt is sandbox-blocked from binding a socket; the
  central run is the HTTP evidence.
- No direct Agent-worker semantic ACK was available in this worker context;
  the image positive is source-backed by the ordinary Agent `_clip`/`_swap`
  semantics and by the central executable result. The old ambiguous generic
  source-descriptor refusal is not silently claimed as all-ten native parity.
- Scratch/test outputs were kept outside the product repository; shared
  dependencies were read-only. No merge, pin, or branch operation was made.
