Implemented the missing CURRENT test prerequisite on Agent HEAD
`8a78c25ac331ff769291c0207119b3f4ee49b822` (presenter prerequisite `802669926`).
Only four files under `tests/packs/rendering` changed. Product scene/capture,
astrid_motion, SDK/provider/compiler/core, package pins and original PNGs are
unchanged. No production consumer activation, source admission, private math
retirement, or Gate 6 completion is claimed.

Changes:
- Export existing `prepareRoot` and port donor `seriesInspection` into current
  `presenter_crop_geometry.mjs`. It resolves one exact compiled clip, checks
  owner/clip/track/index, uses public DrawPlan/component zero, queries the SAME
  prepared scene once and returns the retained ROI. Track checks are additional
  guards; the nonnegative mounted-zero candidate follows the existing Agent
  proposal's public-clock rule, without a new clock inverse or search.
- Add one direct Node/pytest regression. A spy delegates to the real registered
  capability and observes exactly one read. Missing/ambiguous ID, foreign
  owner, stale params, clipped-away zero, unknown mosaic ROI, empty scene and
  unavailable scene cannot supply a replacement region. Delayed positive-speed
  input uses public component zero at frame150. Existing known default,
  partial, fractional and raw-invalid crop expectations remain passing.
- Let the existing test fixture explicitly select the immutable public12
  archive by environment. Only the exact known public10/public12 SHA256s are
  accepted. Extraction, all77-file checks, generated pack discovery, resolved
  React18.3.1/Remotion4.0.509 peers, and cleanup remain intact. Default is still
  this checkout's public10 artifact; this is not package adoption.

Exact source facts: the fixture discovers `pack:astrid_motion`, verifies its
root is THIS checkout's `astrid/packs/astrid_motion/rendering/elements/effects/
am-presenter`, generates ordinary host owner maps, and bundles that actual
source. No authored owner string or params-only identity is treated as source
admission. The helper's comment makes this fixture boundary explicit. The
reviewed presenter files are unchanged, including scene.ts SHA256
`bb1374c5e7d4a15dae83fe5ba0618eb3b9a887a3c72d7e3d446be350a1a71c7a`.
Public12 archive SHA256 is
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

Retained pixel qualification:
- Used the original six-member archive, SHA256
  `e7f32e40aa1aa25d81f30d05fd5ccb83a8a19cd8ce4a5a560e9fd93dc73d7c39`.
  Existing proposal tests verify every original file hash before/after. Four
  PNGs remain frames0,3,4,5; frame0 and4 are independently retained equal bytes.
- Ran the unapplied selected-cut proposal in disposable staging, against this
  current helper, on both public10 and public12. Public12 uses the capture's
  EXACT explicit public10 theme. Its new default differs, as settled in PLAN;
  the original proposal query's `retained.props == propsFor()` incorrectly
  equates that explicit capture theme with the newly installed default.
- Flat `proposal-query-public12.patch` is UNAPPLIED to the repository (the
  proposal itself is still unapplied). It preserves timeline/assets checks and
  pins the ENTIRE original inspection JSON by its independently retained hash,
  thereby preserving the original explicit theme instead of substituting the
  public12 default. Both variants produced identical rows and pixel results.
- Actual cut: index1, clip presenter, track overlay, [0,2), empty shot and
  occurrence IDs. Actual original reads [0,3,4,5], pairs0→3/3→4/4→5,
  336 changed pixels / 799 each, exact finding:
  `LIPSYNC pixels: mouth region changed between 3 of 3 sampled frame pairs`.
  Existing proposal controls preserve missing-key1/2, missing-image1/3,
  half-open selection, fewer-than-three behavior and strict15/799≤2%<16/799.

Exact commands (cwd is this worktree):

```sh
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD
export ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
export ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules
export ASTRID_COMPOSITION_TEST_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.12.tgz
/home/user/work/venv-agent/bin/python -m pytest -q -c pyproject.toml -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_presenter_series_inspection.py tests/packs/rendering/test_presenter_crop_equivalence.py
# 10 passed in 4.00s (one new direct case + nine unchanged crop neighbors)

python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth-series-current-port-check.py 12
# 15 passed, 4 existing integration-marker warnings in 3.69s
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth-series-current-port-check.py 10
# 15 passed, 4 existing integration-marker warnings in 3.69s
# check.py sets the exact env independently, stages unchanged proposal tests
# and original archive, selects the query variant, and removes all staging.

/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/packs/rendering/test_presenter_series_inspection.py tests/packs/rendering/test_presenter_scene_capability.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth-series-current-port-check.py
# All checks passed!
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/packs/rendering/presenter_crop_geometry.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/packs/rendering/presenter_series_inspection.mjs
git diff --check
git apply --reverse --check --whitespace=error-all /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth-series-current-port-port.patch
# All exit0.
```

No implementation blocker remains for this test prerequisite. Next: review
and land its four-file patch, then review the retained selected-cut proposal
with the separate public12 query adjustment. Production admission/context
qualification remains held for its owner: this flat retained fixture has no
Runtime candidate/historical authority or certified occurrence mapping. No
Agent-owned source change was necessary or manufactured in this task.

No browser, SSR render, capture, socket, install, network, full suite, central
request, new xfail, git commit/ref mutation or push ran. Source and temporary
fixtures compiled only in memory; staging was cleaned. Raw logs, check.py,
port.patch and the separate proposal query/patch are flat files alongside this
report with the same absolute handoff prefix. Commit message and DONE supplied.
