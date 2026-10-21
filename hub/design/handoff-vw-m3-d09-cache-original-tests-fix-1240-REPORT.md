# vw-m3-d09-cache-original-tests-fix-1240

## Result

Restored all four original composed-capture execution positives as active tests by removing the unauthorized strict xfail. The direct execution test provider now uses the existing `CaptureSceneLabels` public callback carrier with the exact requested source identity, clip/address mapping, basis, frame, and retained PNG binding.

The normal `RemotionFrameProvider` was inspected and already carries `scene_for_frame` plus `source_identity` from its existing callback/cache path, so no production adapter, API, DTO, or store change was made. Existing no-authority PNG/cache negatives remain visibly unavailable.

## Evidence

- Original four: **4 passed**.
- Focused cache/source neighbors: **60 passed** total.
- `git diff --check`: **passed**.
- No new skip/xfail/expected-failure wrapper; no unrelated fastlane, builtin, or labels-helper edits.

The separately requested 96-test focused lane was not run; no full, browser, install, or shared-write suite was run. This is reported as unverified rather than inferred green.

## Scope

Exactly one repository path changed:

`tests/packs/rendering/test_timeline_filmstrip_execution.py`

The worker report and flat patch are adjacent to this handoff under the orchestrator scratchpad.
