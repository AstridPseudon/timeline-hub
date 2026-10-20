**Ready for Agent owner review: one bounded current extent unit, all requested nonbrowser lanes green.** No merge/remote request was made.

Base/current integration: `df2739f903edac02bd36b4446deeea847524c040`; unchanged at final audit. Branch: `tl/vw-m3-current-extent-landable-unit`. A resulting commit SHA is not available until the harness commits. Exact new delta is seven files, **1,240 insertions / 28 deletions**, at `handoff-vw-m3-current-extent-landable-unit-scope.patch`, SHA-256 `ae4695c47b3a2ee2a92da76cff774a7ec2ae9f1ebb134ac835580e58dd1ca77c`.

Assembled only the granted pieces:

- Frozen `626eed656edf2a6398703e9e5318343069e47019` service/run/Root extent scope and direct extent/Root tests, applied forward with zero fuzz onto current integration.
- Exact completed current pre-tail fix in run/Root, plus its byte-identical 474-line tail test. Original three permanent positive/control functions remain AST-identical to `e2d926319718c396fe579236eb9c8de5fb00f19f`; ordinary tail placement (`RenderClockTail`) remains byte-identical.
- Exact single-file native-layer M2 migration: three existing functions/five nodes now assert the actual final Three.js slice, native/legacy payload equality and retained null-window refusal; two new nodes prove native windows-only admission. All other existing test definitions, including the browser case, are unchanged. The migration file's SHA-256 is `99a726a4326a5492fc112f32c85fcb8eb13de366c76909174dd50f5a609248c5`.
- Exact seven Root tests, SHA-256 `181950efa7e91f646d57496b33897e4e40ec6723c695f6bb6d8ffe940443b6cc`.

The only three product files are `astrid/core/rendering/service.py`, `astrid/packs/rendering/rendering/renderers/remotion/run.py`, and `remotion/src/Root.tsx` (+126/-18). The four direct-test files are `tests/packs/rendering/test_native_layer_extent.py`, `tests/packs/rendering/test_remotion_layer_tail_compat.py`, `tests/packs/rendering/test_live_scene_composition.py`, and `remotion/tests/root-metadata.test.cjs` (+1114/-10).

**Preservation.** All **3,002 tracked files outside that scope** retain their latest integration SHA-256 values. Capture callbacks and `capture_remotion_frames` remain AST-identical; the locked `on_scene_props` invocation is unchanged. The latest package/lock and tracked **0.0.12** archive, current serializer/for_render rounding, duration validator, Three.js implementation and nonowned M2 sources are unchanged. No PCM kernel/caller/activation, precision port, adoption change, source factory, new DTO/projector, authored stamp or foreign ancestry was introduced. Exact source/protected hashes and AST checks are in `handoff-vw-m3-current-extent-landable-unit-source.json`.

**Qualified behavior.** The service measures original render-ready duration before track isolation, ignores caller reserved extent facts, retains absolute native windows and original selected clips, and preserves the legacy slice route. Runner support and locked execution agree on positive-safe-integer extent, native-layer stamp, FPS, source-range, speed and bounds validation. Both Root callbacks retain original 300/600 extents for empty/sparse no-tail layers at integer/rational FPS. The bounded clock-tail fix accepts covered pre-tail [0,30) and [150,165) windows, retains original 330-frame render extent and the unchanged source tail [300,330), and keeps tail placement outside those selected outputs.

The migrated repository tests compare complete actual Three.js capture-seam payloads for native vs unchanged legacy routes, including alpha, MOV/MP4 choice, pinned package/source/revision, from/to/speed/hold and nested opaque data. A separate two-case probe executes the actual `ThreeTimelineComposition.tsx` body (framework imports stubbed) and compares its emitted `LiveSceneClip.source` and `sourceTime` at frames 0–30 across those payloads for z=0/1. Both routes match exactly, including background transparency and the half-open end. CURRENT represents the dynamic source as `app.liveScene` → `LiveSceneClip.source`; there is no separate `dynamicSource` field in this source. These observations come from actual component execution, rather than a guessed raw-source clock. Legacy slicing methods and the Three.js consumer are unchanged from current baseline.

**Tests.** Exact executable commands/environments, fixture setup/cleanup and initial setup failures are recorded in `handoff-vw-m3-current-extent-landable-unit-tests.txt`; logs are adjacent flat files.

| Lane | Result |
|---|---|
| Extent/native-window/capture-callback/tail files | **131 passed**, exit 0 |
| All nonbrowser `test_live_scene_composition.py` | **17 passed, 1 deselected**, exit 0 |
| Service window/segment neighbors | **5 passed, 47 deselected**, exit 0 |
| Clock/storage neighbors | **10 passed, 108 deselected**, exit 0 |
| Exact Root file | **7/7 passed**, exit 0 |
| Rational-FPS/boolean Root supplement | **2/2 passed**, exit 0 |
| Actual Three component source-props comparison | **2 passed**, exit 0 |
| Three Python direct-test files Ruff | **passed**, exit 0 |
| `git diff --check` | **passed**, exit 0 |

Product Ruff retains the exact inherited diagnostics (service 6, runner 7); no new code/message diagnostic. See `handoff-vw-m3-current-extent-landable-unit-ruff.json`.

**Fixture decision and replay prerequisite.** The unchanged tail test explicitly reads its frozen0.0.10 duration archive, absent from the latest tracked tree after the existing pin moved to0.0.12. Its first run therefore failed 11 fixture loads; no behavior expectation changed. To preserve the granted test bytes and current pins, this worker supplied a temporary read-only file leaf to the frozen reviewer archive inside its own real artifacts directory, then removed that leaf after tests. The exact public0.0.10 duration chunk `package/dist/chunk-SE4TPVLW.js` is byte-identical to the currently tracked0.0.12 chunk (SHA-256 `887441a18596fd09bd145381f6745ca986372cd32fb59278733f6b8d161f494b`). Tail-test replay requires that fixture provisioning step; a fresh tracked-only checkout does not contain the old archive. Fixture paths/hashes are in `handoff-vw-m3-current-extent-landable-unit-fixture.json`. Shared dependencies, runtimes and caches were read-only; the only Node module leaf was TypeScript under this worker's real private node_modules directory.

**Limits / next step.** No source conflict or implementation blocker was found. Empty/gap tail scheduling remains a pre-existing limitation: bounded overrides still refuse when existing tail placement would enter the selected output. Tail ownership, tail-crossing native overrides and generalized tail behavior remain unqualified. No full suite, browser, socket, render, encoder/decoder, HTTP, pixel/audio, full TypeScript check, dependency-graph qualification, Runtime certification or consumer adoption was run or claimed. `make check` was not run under this no-render/no-install bounded brief. No git mutation or remote operation was performed.

Recommended next step: Agent owner reviews this exact seven-file source candidate and its bounded tail guard, including the frozen-fixture replay prerequisite. Manager approval is required before requesting integration/remote action. Commit message and DONE are in this worker's assigned directory; no repository docs or temporary/build output were added.
