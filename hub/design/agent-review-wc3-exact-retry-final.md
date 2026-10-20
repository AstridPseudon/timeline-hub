# WC3 exact media-swap retry finalguard review

## Verdict

**CONCRETE BUG — do not approve the exact-retry guard as complete; hold whole WC3.**

Reviewed source tree: Agent `747b7ee34f581b3cfa50a0d120e5b942dfba0a5` (`fix(timeline): bind media swap retries to exact intent`), worktree `tl/agt-review-wc3-exact-retry-final`, clean at review time.

The repair closes the original unrelated-pending-operation bug for the normal typed path: it binds one pending command to the explicit owner/occurrence, clip, source object, old/new five-field selections, expected head/publication, and a single pending command. Parent-versus-occurrence retargets, extra pending commands, source/selection/head/publication mismatches, and ambiguous pending state are refused before `flush`, preserving the outbox. The exact persisted request body and key are protected by `TimelineSession._flight_body` (`astrid/sdk/timeline/sync.py:375-395`), including original base identity, body digest, and supplied-key equality.

### Blocking bug: typed old/new selection mismatch still flushes

`astrid/sdk/timeline_media_replacement.py:219-224` only compares caller selections when at least one value is a `Mapping`. If both caller-provided `old_media` and `media` are non-mappings, the condition is skipped and `_pending_matches` returns `True`; line 283 then calls `session.flush`. For example, an exact pending swap plus `old_media="bad", media="bad"` reaches the retry path instead of returning a typed validation failure with zero POST/flush and unchanged outbox. The direct helper probe returned `True` for this case; exact mappings returned `True`, while one-sided typed mismatches returned `False`.

The required rule is that omitted selections may mean “use the persisted pins” for an exact retry, but any supplied old/new selections must be two complete five-field mappings equal to the persisted pins. This is a source-level/control-flow finding; no fake session result is claimed as Runtime acceptance.

## Evidence

Passed:

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/test_timeline_clip_replacement.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_native_frontends.py tests/editing_conformance/test_recipe_parent_media.py tests/editing_conformance/test_recipe_occurrence_media.py` — **165 passed in 20.19s**. This was broader than the requested finalguard probe and will not be repeated.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/test_timeline_clip_replacement.py::test_remote_parent_media_replacement_does_not_publish_a_whole_closure tests/test_timeline_clip_replacement.py::test_selected_occurrence_replacement_uses_the_session_commit_door tests/test_timeline_clip_replacement.py::test_incomplete_or_mismatched_selection_never_falls_back_to_publication tests/test_timeline_clip_replacement.py::test_pending_unrelated_or_ambiguous_swap_refuses_without_flush tests/test_timeline_clip_replacement.py::test_pending_swap_identity_controls_refuse_without_post tests/test_timeline_clip_replacement.py::test_exact_pending_swap_retry_survives_restart_and_keeps_opaque_body` — **10 passed in 1.71s**.
- `git diff --check HEAD^ HEAD` — passed.
- Direct exact-pending helper probe — owner/clip/source/head/publication/extra-pending controls in the focused tests refuse without flush; exact retry preserves the opaque persisted body and uses the persisted receipt key when the caller omits a key. The typed both-non-mapping case is the failure described above.

Not run / not claimed:

- No full, matrix, browser, live-socket, or central integration suite was run.
- The current tests use private/fake session seams for adapter control flow; they do not prove Runtime acceptance. I make no fake-session acceptance claim.
- The old whole-publication publisher remains deleted in this tree, but its replacement is not whole-WC3 qualified by this review. The prior public-014/parent-provider attempt failed before the adapter on the Runtime ownership schema, and the real normal-pin/current-source private Runtime case is assigned to a separate qualification worker. Whole WC3 therefore remains held until that normal private parent-provider case passes with the current client and retains the original six positive assertions (success, exactly-one publication, idempotency key, selected asset, timing `at`/`hold`, and expected head), plus native retry/restart evidence.

## Required next action

Make the pending matcher reject malformed or partially supplied old/new selections: accept only both omitted, or both complete exact five-field mappings equal to the persisted pins. Re-run the focused positive and typed-mismatch-negative probes, then obtain the separate normal private Runtime parent-provider qualification before approving whole WC3. No new retry framework, wire field, alias, or sidecar history is warranted.
