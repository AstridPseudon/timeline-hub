# APPROVE — D09 retained SDK scene-join proposal

Independent review of the source worker's unapplied SDK patch:

- `owner-sdk.patch` applies cleanly to this worktree and changes only
  `astrid/sdk/timeline/check.py` plus its proposal regression
  `tests/sdk/test_retained_scene_check.py`.
- The retained helper follows the original full `RenderRequest` before
  `_segment_request`; it does not use a window/layer derivative. It reuses
  the existing `GenericPackHost._materialize_inputs` source handoff,
  `inherited_source`, `prepare_filmstrip`, normal Timeline
  `for_render`/serialization, and the existing
  `_prepared_remotion_root` lifetime through public `scene_answers` Node
  queries.
- Saved and working-copy candidates are checked against the retained
  source; stale, forged, foreign, changed-path, missing-source, and
  segmented inputs remain advisory `UNAVAILABLE` and do not query Node.
  Real scene `UNKNOWN` findings remain advisory and are surfaced by the
  existing formatter.
- `_check_core`, save, publish, transaction, and dry-run remain independent
  of the retained-scene tuple and renderer/Node.
- No second projector, private geometry calculation, clock, pin, API,
  authority factory, store, DTO, or duplicate Root-preparation helper was
  introduced. The only applied source helper is the existing
  `astrid/core/timeline/scene_answers.py::_prepared_host_frames_at`.

## Evidence

Exact command: `COMMAND.sh` in this directory.

Result: **29 passed in 5.76s**.

This was a private overlay only: the SDK worktree stayed unmodified. The
run covered the proposal's two registered-Node positives (saved revision and
working candidate), 11 stale/forged/unavailable negatives, and all 16
`test_scene_save_core.py` saveNoNode cases.

Additional checks:

- `git apply --check owner-sdk.patch`: passed.
- Ruff selected checks for undefined/unused/import errors on the patched SDK
  module and proposal test: passed.
- `git diff --check`: passed; worktree clean.

No full suite, browser, socket/server, install, network, or live Runtime
qualification was run. The source worker's prior 234-test replay is accepted
as existing evidence and was not repeated here.

## Owner-only activation steps

Scoped filenames are the source worker's external
`.../vw-m3-sdk-scene-existing-retention-join/owner-sdk.patch` and the
already-applied helper `astrid/core/timeline/scene_answers.py`. No caller
patch filename is included or approved: this Agent tree has no existing
`_scene_inputs` consumer, so the owner must identify the actual host-retained
integration call site rather than guessing a CLI or service path.

The Agent owner must wire the private `_scene_inputs` tuple at the existing
host-retained original-request caller, before any `_segment_request` call,
and keep `(request, workspace, client)` alive until `Checkout.check()` and
its synchronous scene query return. The ordinary CLI `_cmd_check` remains
unchanged and therefore keeps its existing authored-diagnostics behavior.
The owner should apply `owner-sdk.patch` only after the applied
`scene_answers.py` helper is present, then add that narrowly scoped caller
handoff; do not place it in save/publish/transaction paths.
