# WC3 media-swap deletion gate review

## Verdict

CONCRETE BUG — do not approve.

The WC3 branch is at `449dc471` (`feat(timeline): route media swaps through native sessions`), based on `310e5484`. The worktree is clean. No source files were changed by this review.

### Blocking bug: retry can flush an unrelated pending swap

`astrid/sdk/timeline_media_replacement.py:233-239` treats any pending command whose operation is `clip.swap-media` or `occurrence.swap-media` as the requested retry. It checks the original revision, but does not compare the pending command's `select`, old-media pin, new-media pin/source object, or ownership intent with the current call. Therefore a request for clip B can flush a durable pending swap for clip A; a request with a different source can likewise reuse the pending identity. This violates the settled retry rule that a retry must bind the same user intent, head, reference, and source, and can POST unrelated work under the new call's key.

An inline private-buffer probe reproduced this: an outbox containing `occurrence:other/clip:other` caused a request for `occurrence:occ-a/clip:clip-a` to call `flush()` once. The same probe confirmed that a fresh exact source/body mismatch refuses with no flush and no outbox write.

## Required behavior review

- The old whole-publication path is deleted on this branch; `RemoteTimelines.replace_parent_media` delegates to the existing `TimelineSession` adapter. No new endpoint, DTO, schema, fallback writer, candidate diff, or legacy document route was added by WC3.
- The exact-object scan is project-scoped through `list_generations(project_id)` and `list_variants(generation_id)`, requires exactly one object match, and does not call latest/current/gallery selectors. A duplicate-object private probe refused as ambiguous.
- Selected media is re-read as the exact five-field selection and verified selection before capture. Native capture retains the existing command guards, source-window handling, opaque fields, occurrence isolation, and parent/occurrence operation distinction.
- Fresh exact source/body mismatch refusal and outbox preservation were verified privately. The unrelated-pending retry failure above remains blocking.
- The adapter-specific lost-ack/retry test is not present. Existing `TimelineSession` retry tests do not prove that `replace_parent_media` binds the same target/source after a lost acknowledgement or restart.

## Positive assertion and provider coverage gap

The original whole-publication positive test had six meaningful assertions: success, exactly one publication, idempotency key, selected asset, preserved timing (`at`/`hold`), and expected head. The converted unit test is now only a no-publication negative test, while the converted parent-provider case asserts only success and the final asset. It does not assert the key/receipt, exactly-once acceptance, expected-head binding, or timing preservation one-to-one. The parent-provider test uses a real Runtime commit provider but supplies explicit old/new selections and does not cover the new source-object-only scan.

## Integration overlap

Compared with current Agent integration `130b4937` (and still overlapping current `30fc8dd1`) from base `310e5484`, the exact WC3-overlapping paths are:

- `astrid/sdk/remote.py`: integration removes the WC3 adapter arguments/dispatch and retains the old whole-closure implementation.
- `astrid/sdk/timeline_media_replacement.py`: integration deletes the file.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py`: integration deletes the real parent-provider test.
- `tests/test_timeline_clip_replacement.py`: integration deletes the converted adapter tests.

The non-overlapping integration work includes selected-parameter authority and timeline command/inverse changes, scene/rendering/extraction changes (`astrid/core/rendering/service.py`, `window_inputs.py`, composed-frame/Remotion paths, and timeline elements), plus architecture and timeline documentation. WC3 must be reconciled with those changes; the ordinary canonical `310e5484` work cannot be treated as a standalone merge before the paired public-014 Runtime contract is available.

## Tests and evidence

Passed:

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/test_timeline_clip_replacement.py` — **6 passed**.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_parent_media.py tests/editing_conformance/test_recipe_occurrence_media.py tests/sdk/test_timeline_sync.py` — **142 passed**.
- `git diff --check HEAD^ HEAD` — passed.
- Private adversarial probes — ambiguous object refused; fresh source/body mismatch refused before flush with unchanged outbox; unrelated same-op pending intent incorrectly flushed once.

Unverified/blocked:

- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo` — both parametrizations fail before the adapter because the current Runtime schema rejects `intent.ownership='parent'` (expects `shared`/`occurrence`).
- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m2-native-clip-replacement-positives PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo` — same pre-adapter schema failure. Thus the real parent-provider positive and adapter-specific native ACK/retry case are not independently qualified here.
- No full/public/matrix/live broad suite was requested or run.

## Recommended next steps

1. Make the pending/flight path require exact equality of the saved command's target, ownership, old-media five-tuple, new-media five-tuple/object identity, and original head before calling `flush`; otherwise retain the outbox and return the existing typed error.
2. Restore one-to-one positive assertions for parent and occurrence adapters, including receipt/key, head pair, exactly-once acceptance, timing/source-window preservation, and shared-isolation behavior.
3. Add an adapter-level lost-ACK/restart test and a source-object-only real-provider positive/ambiguous-selection lane after the paired public-014 Runtime contract is available.
