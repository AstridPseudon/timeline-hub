**Verdict: REJECT as submitted.** The substance is approvable, but three things need fixing first. The full review is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-presenter-port.md`. `DONE` is created in the worker directory.

**Blocking**

1. **`artifacts.json` is stale.** The branch changes `component.tsx`, `element.yaml` and `motion.ts`, and adds `scene.ts`, but does not regenerate the manifest. I compared the hashes by reading the branch blobs. `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current` will fail. The fix is `python scripts/artifact_manifest.py`, a digest-only change. Your brief says "no pin changes", so please confirm that regeneration is allowed.
2. **The `element.yaml` comment is not trimmed.** It adds 8 lines with new claims. The approved patch nets about 3 lines. It needs trimming to the approved wording.
3. **Tests not run.** See below.

**Checked and matching the approval**

- The inspection rect is the erase rect padded 1 px horizontally and 2 px vertically. For 151/104/19 it equals the legacy `mouth_box`.
- Default, partial and raw-invalid anchors stay known. Mosaic stays unknown.
- Partial anchors are excluded from legacy qualification.
- Nothing changes outside `astrid/packs/astrid_motion/` and `tests/packs/rendering/`. The comparator, crop, statistics and capture callers are untouched.
- `motion.ts` and `scene.ts` blobs equal the approved patch's post-images.
- There is no schema, provider or compiler change. `pack.yaml` only adds `scene.ts` as a resource.
- The `component.tsx` refactor is accepted. It shares the helpers so there is one erase formula, and the 286 SSR hashes cover it.
- The named tests exist: 17 in the two presenter files, matching Viewing's "17 passed".

**Tests**

I ran none. `request-test` snapshots my worktree, which is on the base, not the branch. Extracting a snapshot to scratchpad was blocked by the permission gate, so I did not work around it. Viewing's logged results (17 + 6 passed, ruff, node checks) are unverified. The review lists the exact commands to run after the fix.

**Housekeeping**

I left `vw.tar` in my scratchpad. Deleting it was denied, so please remove `/tmp/claude-0/-home-user-work-wt-agt-review-presenter-port/b8260db0-c6c3-4d27-96cd-1c5d6d3039d9/scratchpad/vw.tar`. No repo files were changed and no commit-msg was written.
