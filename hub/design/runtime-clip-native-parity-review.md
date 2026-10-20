# Runtime native clip-replacement parity review

## Decision

**REQUEST CHANGES** for source commit `cd6e9c7d2862ae7ece5f64dc931eebff9dd93160` (`test(runtime): cover native clip media replacement positives`). The candidate is useful bounded evidence, but it is not yet one-to-one proof of all ten original behaviors. The CAS-negative xfail is excluded from this decision because it is owned by `rt-m2-selected-media-cas-integrity`.

The candidate’s recorded evidence is `9 passed, 1 strict xfailed` for the native non-HTTP lane and `1 passed` for the HTTP node. I could not reproduce that lane in this checkout: `PYTHONPATH=packages/python pytest -q tests/test_timeline_clip_replacement.py -m integration --disable-warnings` produced `8 errors, 1 failed, 1 passed, 10 deselected, 1 xfailed`; all native setup errors and the HTTP failure were `ModuleNotFoundError: jsonschema` while importing the frozen ordinary Agent source. `python -m py_compile tests/test_timeline_clip_replacement.py` and `git diff --check cd6e9c7d^ cd6e9c7d -- tests/test_timeline_clip_replacement.py` passed. No full/broad/render suite was run.

## Original-to-replacement mapping

| Original test | Candidate replacement | Review result |
| --- | --- | --- |
| `test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable` | `test_native_clip_swap_is_atomic_cas_and_exactly_replayable` | Partial: retry, changed-key 409, and relevant stale refusal are covered; exact old body/receipt/event invariants are not. |
| `test_replace_timeline_clip_rejects_cross_project_source` | `test_native_clip_swap_rejects_cross_project_source_without_mutation` | Mostly covered: real foreign selection and whole SQLite dump equality; error identity/message is weaker than the old `NotFoundError` + `timeline project` assertion. |
| `test_replace_timeline_clip_rejects_malformed_source_without_mutation` | `test_native_clip_swap_rejects_malformed_source_before_native_commit` | Not equivalent: only media-import admission is tested; no native target, swap command, commit, or native mutation/event/idempotency assertion. |
| `test_replace_timeline_clip_rejects_tampered_cas_without_mutation` | `test_native_clip_swap_rejects_tampered_cas_without_mutation` | Intentionally bounded strict xfail; owned by the CAS-integrity worker and not duplicated here. |
| `test_replace_timeline_clip_rejects_wrong_stream_without_mutation` | `test_native_clip_swap_rejects_wrong_stream_without_mutation` | Partial: capture-time refusal and DB equality, but no native commit-path refusal. |
| `test_replace_timeline_clip_rejects_too_short_source_without_mutation` | `test_native_clip_swap_rejects_too_short_or_end_short_source[1]` | Not equivalent: capture-time assertion only; no commit rejection or native event/idempotency proof. |
| `test_replace_timeline_clip_requires_source_to_reach_authored_end` | `test_native_clip_swap_rejects_too_short_or_end_short_source[3.5]` | Not equivalent for the same reason; the authored end is checked only while capturing. |
| `test_replace_timeline_clip_generic_visual_media_requires_video_stream` | `test_native_generic_visual_media_requires_video_stream` | Insufficient: only audio rejection is exercised; image is not tested. |
| `test_replace_timeline_clip_replays_after_intervening_edit_and_reopen` | `test_native_clip_swap_replays_after_intervening_edit_and_reopen` | Partial: exact idempotency replay survives reopen; no disjoint stale rebase acceptance, and no post-reopen head/event-count assertions. |
| `test_replace_timeline_clip_public_http_route` | `test_native_clip_swap_public_http_route` | Partial: native `/v1` commit succeeds and asset changes; response receipt/body invariants from the old HTTP test are not asserted. |

Extra candidate test `test_native_parent_clip_swap_route_replaces_parent_media` is useful route coverage but has no one-to-one original behavior to substitute.

## Required changes

1. Keep the original atomic assertions when porting the native route: assert the exact accepted body fields that correspond to the old clip/untouched-row/registry checks, receipt command kind and event IDs, one accepted receipt/event, exact retry equality, and changed idempotency payload refusal. The current test only checks the replacement asset, status, and HTTP status/asset.
2. Make malformed, wrong-stream, and both duration/end cases exercise an actual native swap commit against an existing owned target, with the strong no-mutation assertion. Import-time decoding rejection may remain a fixture prerequisite, but it is not a replacement proof.
3. Add the missing generic-visual image counterexample. In the ordinary Agent source, `_clip` accepts `row['clipType'] == 'media'` for `kind == 'image'` (`native_occurrence_media_commands.py:104-106`), and `_swap` only requires old/new kinds to match (`:190-195`). A small executable case is: create an occurrence-owned `clipType='media'` image clip with a hold-only row, then swap verified `image/png` selection A to verified `image/png` selection B. The current implementation accepts this, so the audio-only test does not establish “generic visual requires VIDEO stream.”
4. Split stale behavior into relevant conflict versus disjoint rebase acceptance. The candidate’s stale edit changes the target clip (and writes the existing `hold=3` value); the reopen test retries the same idempotency key and therefore proves replay, not rebase. Add one disjoint intervening edit and assert the stale swap is accepted/rebased while the target replacement remains exact; retain the relevant-target 409.
5. Assert the HTTP response body’s receipt and exact accepted result, at least the old test’s `receipt.command_kind` equivalent plus event/request identity, and exercise exact HTTP retry if that is the intended transport proof.

These are proof/test changes only; no Runtime feature change, authority bypass, xfail widening, source edit, merge, or pin is requested by this review.
