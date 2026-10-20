# SDK scene-only managed caller review

## Verdict

**HOLD ordinary activation and D09 deletion.** The reviewed caller is
appropriately narrow, but it is not qualified against the actual Viewing
executor contract yet.

Reviewed Agent commit `4f3cd32be34e194d55bad31820e7b6078de319af` with tree
`9a50e3ada5d7da687e49d510370e007e6b50b305`; the worktree was clean and no
product source was changed by this review.

## What is correct

- `_scene_only_request()` reuses `prepare_filmstrip()` for the saved/candidate
  capture and requests the existing managed visualization invocation with
  `mode: "scene_only"`, `view: "filmstrip"`, and `formats: ["md"]`.
- No caller `source_ref`, certification, authority DTO, provider, store,
  endpoint, SourceFactory, copied projector, or new public API was added.
- The adapter is not wired into ordinary `Checkout.check()` activation.
  `_check_core`, save, publish, and transaction paths remain unchanged and
  renderer/Node-free.
- Missing/stale capture and map checks return advisory `UNAVAILABLE` spans.

## Blocking findings

1. The implementation and its positive fixtures use a synthetic
   `scene_result` payload with `scene_answers`, `compiled_id_address_map`, and
   `source_label` (`astrid/sdk/timeline_filmstrip.py:1355-1372, 1398-1427;
   `tests/sdk/test_scene_caller_preservation.py:151-175`). The actual Viewing
   SDK handoff specifies the existing `filmstrip_bundle` artifact and nested
   `scene-answers.json`, with keys `answers`, `scene_clips`, and
   `snapshot_label`, including `status: "unavailable"` with empty answers.
   The adapter neither reads that artifact nor accepts those agreed keys.
   A result from the agreed executor would therefore be classified as
   unavailable (the local probe produced `scene source label unavailable`).
   The two shared handoff notes are themselves inconsistent on these names;
   the orchestrator must settle that exact contract before activation. This
   review does not treat the SDK-only fixture as executor evidence.

2. Source binding is not mandatory. `_scene_only_spans()` only validates a
   managed object/video binding when one is present; it accepts a payload with
   the synthetic capture/map/label fields but no admitted source binding. A
   local probe returned `COVERED` for that case. Exact admitted source/base
   binding is required by the handoff, so missing source must be advisory
   `UNAVAILABLE`, never a certificate from metadata or public rows. The bound
   label is also only checked for non-empty text, not against an executor-bound
   expected label.

3. The caller does not explicitly carry the full canonical frame extent from
   `capture_snapshot.duration_frames`, although the Viewing handoff says the
   Agent caller should request that extent. Confirm the final request shape
   with Viewing when resolving finding 1.

## Evidence

Focused command (private Python bytecode and pytest cache disabled):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_filmstrip.py tests/sdk/test_timeline_filmstrip_invocation.py
```

Result: **87 passed in 3.16s**.

Additional checks passed: `git show --check --oneline HEAD` and
`git diff --check HEAD^ HEAD`. No full suite, browser, live socket, Runtime,
or executor qualification was run.

Reviewed-file SHA-256: `astrid/sdk/timeline_filmstrip.py`
`ffc55b985725b33b6f28d5285fa8309018a1f1a1933229c94f114094d36a2b96`;
`astrid/sdk/timeline/check.py`
`94c277864fbaf29f55050f827cf619217f685471f4eeb7c3299543e41bdc9623`;
`tests/sdk/test_scene_caller_preservation.py`
`5dda3ff8cdd4a749563f7e52b25e79e31bd2bc6db6b5942cb70e76d8e4765f19`.

## Required next step

Viewing and Agent should reconcile the exact managed-artifact field names,
then add a focused positive using the real artifact shape and negatives for
missing/stale source binding and stale label/map. Keep ordinary activation
held until those tests exercise the actual executor; retain save-core,
OFFCANVAS/core-valid, and all existing saveNoNode guards. Do not delete the
private legacy Scene path or claim D09 completion from this SDK-only result.

