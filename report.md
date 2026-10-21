# Review report

Decision: **APPROVE** the normal `prepare_pair` caller proof.

Reviewed the producer handoff at:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-normal-prepare-label-proof-1256-REPORT.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-normal-prepare-label-proof-1256-flatpatch.diff`

The single test-file patch is correctly scoped. Its caller chain is:

`verify(labels=True)` → actual `prepare_pair` → `_scene_only_request` plus
`_scene_only_candidate_request` → two managed `rendering.timeline_visualize`
results → existing managed ZIP/source/extent parser → `_scene_frame_carrier`
→ returned `frame_providers` → public `_labelled_tiles`.

The test does not inject providers into the pair. It uses a non-local clip,
blank PNGs, and tripwires both authored-config `labels_for` inference and
private `onscreen.visible_at`; the successful labels therefore come from the
materialized managed Scene rows. The original video/snapshot/authority/refusal
test and stale/forged controls remain active. No product source fix was
discovered or required.

Evidence from the producer worktree/log:

- `python -m py_compile tests/sdk/test_timeline_checkout.py` — passed.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= tests/sdk/test_timeline_checkout.py -k 'prepare_pair_materializes_normal_scene_labels_for_verify'` — **1 passed**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= tests/sdk/test_timeline_checkout.py tests/packs/rendering/test_fast_lane_words.py` — **115 passed**, 4 existing Pillow deprecation warnings.
- `git diff --check` — passed.

Not run: full, browser, native, live-socket, install, or shared-dependency
tests. The existing no-carrier/live-legacy fallback remains intentionally
unqualified by this positive activation proof.

Recommended next step: apply/merge only the supplied flatpatch onto its
approved base `0a6162f12`.
