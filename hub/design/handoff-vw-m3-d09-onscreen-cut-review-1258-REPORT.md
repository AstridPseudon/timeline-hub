# D09 onscreen private cut review

## Verdict

**Blocked: no safe cut qualification.** The reviewed private-cut commit
`a5cc85cc7b1f3f8cf4e65d3336243c7f8acc6a15` removes the transition-window
branch from `astrid/core/timeline/onscreen.py`, but does not connect the
remaining `onscreen.coverage()` adapter to `scene_answers`.

The active fallback callers remain:

- `astrid/sdk/timeline/check.py::_CheckMixin._on_screen()` calls
  `onscreen.coverage()` when no bound managed Scene spans are available;
- `astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py::labels_for()`
  calls `onscreen.visible_at()` for ordinary/cache fallback labels.

Therefore the cut removes private transition behavior without proving that
the same success is supplied by public evaluation. A minimal retained-source
probe with a cropped outgoing clip, adjacent incoming clip, and a four-frame
cross-fade gives `GAP` then `DIP` then `COVERED` before the cut; the reviewed
source has no public adapter at that call site and would lose the `DIP` window.

The exact prerequisite is a source-bound public Scene result and adapter for
these fallback callers that preserves the original transition positive, plus
an explicit unavailable result/control when that bound Scene cannot be
evaluated. Until then, retain the private transition branch. No speculative
geometry/timing port is recommended.

## Assertion review

The commit changes only:

- `astrid/core/timeline/onscreen.py`: removes `starts_by_track`, the
  transition-ID/default-duration constants, and the transition `dips` append;
- `tests/packs/rendering/test_scene_answers.py`: reorders imports and changes
  the direct Scene fixture from Composition 0.0.12 to the frozen 0.0.13
  archive (`9412ae25...54738`).

The original positive `tests/core/timeline/test_onscreen.py` and
`test_onscreen_more.py` assertions were not converted one-to-one. The new
public test has positive transition cases and honest package-failure controls,
but those exercise `scene_answers.frames_at()` directly, not
`onscreen.coverage()` or its production fallback callers. No xfail, skip, or
assertion deletion was found. Static roles, timing helpers,
`_timing_evaluators`, and pixel geometry remain untouched.

## Tests and logs

Review tree: `/home/user/work/wt/vw-m3-d09-onscreen-cut-review-1258`.

1. Exact private public13 test hunk, applied temporarily then restored, with
   the pinned Node 20 toolchain:

   ```text
   env -u NODE_OPTIONS -u NODE_PATH \
     ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
     PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
     /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
     -p no:cacheprovider tests/packs/rendering/test_scene_answers.py
   30 passed in 2.22s
   ```

2. Retained Python on-screen/SDK neighbors:

   ```text
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
     /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
     -p no:cacheprovider tests/core/timeline/test_onscreen.py \
     tests/core/timeline/test_onscreen_more.py tests/sdk/test_coverage_empty_cut.py \
     tests/sdk/test_scene_public_summary_rle.py tests/sdk/test_scene_summary_projection.py
   26 passed in 0.80s
   ```

3. The same public test command without the pinned Node override was not
   qualifying: 29 setup errors because only Node v22.22.0 was on PATH; the
   pinned rerun above passed. The current base test file also has a pre-existing
   Ruff import-order failure; the reviewed commit's test hunk passes Ruff.

4. Static checks on the reviewed commit and clean review tree:

   ```text
   git show a5cc85cc7:astrid/core/timeline/onscreen.py | ruff check --no-cache -
   All checks passed!
   git show a5cc85cc7:tests/packs/rendering/test_scene_answers.py | ruff check --no-cache -
   All checks passed!
   git diff --check a5cc85cc7^ a5cc85cc7
   passed
   git status --porcelain=v1
   clean
   ```

No full/browser/localhost/socket/install/shared-dependency write or physical
pixel/audio run was performed.

## Handoff

- Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-onscreen-cut-review-1258/report.md`
- Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-onscreen-cut-review-1258/commit-msg`
- Blocker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-onscreen-cut-review-1258/BLOCKED`
