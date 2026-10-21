# D09 cache four-positive correction review

## Disposition

**APPROVE the reviewed correction diff, contingent on worker 1240 finalizing
the same tree and emitting its required report/commit marker.** The correction
restores all four original parameterized execution assertions as active tests.

The reviewed uncommitted tree is `/home/user/work/wt/vw-m3-d09-cache-original-tests-fix-1240`,
based on rejected commit `1d69859c8`. Its only new hunk is
`tests/packs/rendering/test_timeline_filmstrip_execution.py`.

## Review findings

- The four `test_composed_capture_uses_remotion_for_requested_frames_without_video_frame_source`
  cases have no `xfail`, `skip`, or expected-failure wrapper.
- The injected provider now uses the existing `CaptureSceneLabels` carrier and
  `scene_for_frame(frame)` callback, with the execution snapshot's exact
  `source_identity`, 64x36/24fps basis, requested frames, projected
  `visible-title -> c1.title` address, and freshly written frame PNGs.
- The carrier's existing public guards remain exercised: exact props/frame
  binding, source identity, canonical basis, projected IDs/addresses, complete
  PNG retention, and stale/forged/no-authority refusal behavior.
- The correction does not change the source adapter. Carrierless PNG-only and
  no-authority rows remain explicitly unavailable (`addresses: None`), while
  the four positives use the real equivalent public carrier; no further source
  cut is therefore held for lack of an equivalent carrier.
- The preserved cache/source/label neighbors remain unchanged in behavior.

## Evidence

Commands were run with the shared Agent venv and no install, browser, native,
full, or live-socket suite was requested by this reviewer.

1. Worker 1240's final corrected exact-original command:

   `ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_timeline_filmstrip_execution.py::test_composed_capture_uses_remotion_for_requested_frames_without_video_frame_source --disable-warnings`

   Result from worker log: **4 passed in 5.85s**.

2. Reviewer baseline on clean current integration (`aa42aec6a`): same four
   original cases: **4 passed in 0.95s**.

3. Reviewer preserved-neighbor command on the corrected uncommitted tree:

   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-d09-cache-original-tests-fix-1240:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider /home/user/work/wt/vw-m3-d09-cache-original-tests-fix-1240/tests/packs/rendering/test_labels_overlay.py /home/user/work/wt/vw-m3-d09-cache-original-tests-fix-1240/tests/packs/rendering/test_timeline_visualize_labels.py /home/user/work/wt/vw-m3-d09-cache-original-tests-fix-1240/tests/packs/rendering/test_scene_cache_payload.py /home/user/work/wt/vw-m3-d09-cache-original-tests-fix-1240/tests/packs/rendering/test_scene_source_carry.py -k 'not native'`

   Result: **96 passed, 19 deselected in 8.38s**.

4. Reviewer correction-focused command (cache payload, labels, visualize
   labels, and the four originals): **60 passed in 8.77s**.

5. `git diff --check` on the correction tree: **passed**. The only remaining
   `skipif` decorators in the touched test file are pre-existing FFmpeg guards
   on unrelated audio tests; none wraps the four originals.

## Procedural blocker

At review time worker 1240 still had an uncommitted one-file diff on branch
`tl/vw-m3-d09-cache-original-tests-fix-1240`; its required `report.md`,
`commit-msg`, and `DONE` files were absent. The approval is therefore for the
exact reviewed diff and test evidence, not a claim that its final handoff or
commit has completed. Do not merge until worker 1240 publishes that marker and
the manager verifies the final tree is unchanged.

Full/browser/native/install suites were not run.
