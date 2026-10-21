# D09 normal `prepare_pair` caller proof review

Decision: **APPROVE**.

Reviewed the completed producer patch/report and flatpatch:

- Worker log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-normal-prepare-label-proof-1256/log.txt`
- Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-normal-prepare-label-proof-1256/report.md`
- Flatpatch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-normal-prepare-label-proof-1256-flatpatch.diff`

The test-only patch proves the required normal caller chain:

`verify(labels=True)` → actual `prepare_pair` → published and candidate
scene-only requests → managed result ZIP parsing and source/extent checks →
two materialized frame providers → public `_labelled_tiles` labels.

It observes the actual returned providers rather than injecting them. A
non-local clip, blank decoded PNGs, and tripwires on authored-config
`labels_for` and private `onscreen.visible_at` establish that labels came from
the managed Scene rows. Existing video/snapshot/authority/refusal and
stale/forged controls remain active. No minimal source fix was needed.

Evidence in the worker log:

- Focused caller test: **1 passed**.
- `tests/sdk/test_timeline_checkout.py` plus
  `tests/packs/rendering/test_fast_lane_words.py`: **115 passed**, 4 existing
  Pillow deprecation warnings.
- `git diff --check`: passed.

Not run: full, browser, native, live-socket, install, or shared-dependency
tests. The no-carrier/live-legacy fallback remains intentionally unqualified;
this approval is for the successful normal managed caller only.

Apply only the flatpatch to base `0a6162f12`.
