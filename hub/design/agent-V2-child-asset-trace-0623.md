# agt-V2-child-asset-trace-0623 — ORCH report

**Readonly review: PASS. Child missing-asset retention: FAIL.** Current Agent
HEAD `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80` reproduces the prior faithful
request: an unchanged child `asset: "already-missing"` plus unrelated parent
name edit is refused as `invalid_document` before D12/D12a final validation;
head is unchanged and no preparation occurs. The current valid-child control is
accepted.

Two production-provider negatives also refuse correctly and remain strict:

1. Write existing child `asset: "picture"` to existing missing selector
   `"already-missing"` → `invalid_document`, unchanged head, `prepared 0`.
2. Remove existing `registry.assets.picture` while `clip-a.asset` remains
   `picture` → `invalid_document`, unchanged head, `prepared 0`.

This is a pre-existing canonical authoring/projection limitation, not new V2
invalidity. D12/D12a still applies because the inherited declaration and target
are unchanged; do not remove the approved retention guards. Later owner seam:
`astrid/core/timeline/authoring_bundle.py` `_assert_internal_edit_supported`
and `_clip_selected_media`; preserve Runtime-authenticated
`source_mapping["_runtime_document"]`, exact physical pins/digests and manifest,
authored bytes, and strict write/remove/retarget/owner-change guards. The
map-locality `_commit_timing_validation.py` owner was not touched.

Evidence command: `/tmp/agt-V2-child-asset-trace-0623/child_asset_trace.py`
with `PYTHONPATH=.:/home/user/work/runtime` and
`/home/user/work/venv-agent/bin/python`; imports resolve to this worktree,
`/home/user/work/runtime/runtime_protocol`, and the shared site-package schema.

Tests/gates: targeted pytest **27 passed**; focused Ruff and private mypy pass;
normal Ruff **2149/2149**; mypy ratchet **1914/1914**; vendor lock, artifact
manifest, and `git diff --check` pass. No full/browser/HTTP/native14/heavy/farm
suite. Detailed command lines and the existing exploratory broad-scope
diagnostics are in the worker `report.md`.
