Both reviews are written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-viewing-landings-0745.md`, and the DONE marker is created. The worktree is clean. I read the diffs and did not run any tests.

## 1. `tl/vw-m3-presenter-clean-land` at `8a78c25ac`: APPROVE

- **Scope:** the 11 paths are limited to `astrid/packs/astrid_motion`, `tests/packs/rendering`, and `artifacts.json`. No report or receipt files are included.
- **Manifest:** I hashed the five presenter blobs with `git show | sha256sum`, and all five match `artifacts.json`. I did not recompute the manifest `version` digest.
- **Comment:** `element.yaml` gains exactly 3 comment lines. Their wording does not match any approved hunk I found in `design/`, so the orchestrator should confirm it.
- **Geometry:** the inspection rect is the erase rect padded 1 px horizontally and 2 px vertically, which matches legacy `mouth_box`.
- **Anchors:** default, partial, and raw-invalid anchors stay known, and mosaic is unknown.
- **Drawing:** the component's drawing is unchanged, and `presenter-core.ts` is untouched.
- **API:** `PixelRect` and the new helpers are pack-internal exports. There is no new public type.
- **Tests:** the new Python tests have no skip or xfail markers. Viewing reports `17 passed` for the presenter tests, `8 passed` for the manifest test, and `40 passed` for the neighbours. I did not run these, because `request-test` snapshots my worktree, which sits at `tl/integration`.

## 2. `tl/vw-m3-current-capture-scene-hook` at `18ec2b573`: APPROVE, with one check not met as written

- **Save path:** the only addition is a callback invoked after the props file is written. It evaluates no scene.
- **Authority:** only `run.py` and its test file change. No source authority, provider, or pin changes.
- **Inert by default:** the parameter defaults to `None`, and omitting it keeps the existing call shape. No caller installs it.
- **Failure:** the literal check "failure never changes capture results" is **not met**. An observer exception aborts capture before submission. `viewing.md` documents this as the existing cleanup path. Nothing installs the observer, so production is unaffected today. I recommend recording fail-closed as the decided semantics, since the alternative is to log and continue. That is the orchestrator's call.
- **Tests:** Viewing reports `41 passed` and clean lint, but I did not run them.
