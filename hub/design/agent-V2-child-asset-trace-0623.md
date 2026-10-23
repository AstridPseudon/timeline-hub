# V2 child-asset trace 0623 — independent readonly classification

## Verdict

PASS for the readonly review and strictness evidence; FAIL for the unchanged-child positive on current3e. The unchanged dangling child asset blocks an unrelated parent-name edit before final validation. The two write/remove negatives are correctly refused. This is the existing canonical compiler limitation, not grounds to weaken D12/D12a.

## Evidence

Current3e is Agent `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`; the reviewed trace branch records `7fd8f75bb59115ff2dc04f9d90de35b12f79c4b1`. Reused `/tmp/agt-V2-child-asset-trace-0623/child_asset_trace.py` with the current worktree first on `PYTHONPATH`.

The faithful request keeps the existing child selector `asset: "already-missing"` unchanged in source and candidate and changes only the parent name. It is refused with `CommitRejected` at `shots[shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f].internal_timeline.clips[0].asset references missing registry asset 'already-missing'`; `head_unchanged True prepared 0`.

The write-negative changes child `clip-a.asset` from existing `picture` to existing missing selector `already-missing`; it is refused with the same missing-registry error and `head_unchanged True prepared 0`. The remove-negative removes the existing child `registry.assets.picture` while the child still references it; it is refused with `unknown asset 'picture'` and `head_unchanged True prepared 0`. No new identity was invented.

## D12a and repair seam

D12a applies: checks fire only when the commit writes, modifies, or invalidates the declaration/target. The positive leaves both unchanged and must retain the authored bytes. The negatives create/invalidate a target and must remain strict. Preserve owner, closure, retarget, source-authentication, and removal authority.

Smallest existing seam: `astrid/core/timeline/authoring_bundle.py`, `_assert_internal_edit_supported()` (line 652, called at line 982) and `_clip_selected_media()` (line 541; missing registry rejection at lines 550–554). The mounted production path is `astrid/sdk/timeline/commit.py:1116–1124` → `validate_final_candidate()` → `astrid/sdk/timeline/_commit_timing_validation.py:314` → `compile_authoring_candidate()`, so the caller uses the compiler. A repair must rely on authenticated `source_mapping["_runtime_document"]`, exact physical closure/revision pins, content digests, and dependency manifest; preserve raw authored bytes; and reject newly written, modified, removed, retargeted, or physically owner-changed assets. No broad fallback or guessed asset is permitted.

## Quality

The requested targeted suite passed `76 passed in 12.42s`. Scoped Ruff and mypy passed; `make ruff` matched baseline `2149`; private mypy baseline matched `1914`; vendor lock, artifact manifest, and `git diff --check` passed. Existing unchanged 27-target/ratchet evidence is reusable. No source edits, schema/pin/generated/client/Runtime/undo/fork changes, guards weakening, skips/xfails, or broad/full/browser/native14 suites were performed.
