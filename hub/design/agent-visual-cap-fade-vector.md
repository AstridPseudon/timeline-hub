SETTLED — owner 11:59 decision publishes the original MAIN image-cap golden. The clamped product result is opacity 0.5 at frame 105/30 (RGB 122/124/130 over background 5/8/20, with frame 90 RGB 240/240/240 control). The raw authored hold:5 opacity 1 observation remains diagnostic only. Do not activate the withdrawn native/global renderConfig or flip clamp defaults.

Viewing's actual reference is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-main-image-cap-actual-reference.md`, operation `vw-m3-main-cap-locked-theme-stage-e2e-viewing-main6-locked-theme-image-cap-three-stills-1020115023-5447`. Product source remains unchanged; this is a visual golden, not unified preview/export parity, audio, Runtime acceptance, or Gate 6 proof.

The corpus is `tests/editing_conformance/fixtures/visual_compile_contract.json`, key `cap_fade_closure` (schema 4), with contract section 3 in `docs/design/visual-compile-contract.md`. It includes the verbatim frozen App fixture, its provenance/blob, the explicit 5 s image + 1 s fade-out mutation, and the complete actual raw/default projected clip objects. Existing editor clamp positives remain passing.

Expanded handoff: [agent-visual-cap-fade-vector.json](agent-visual-cap-fade-vector.json). It retains the entire original App fixture, prepared object (including contract and every occurrence/revision), both complete projected configs, both selected clips and exact public observations. No opaque fields were filtered. It is a reproducible synthetic counterexample from the review description; the original review worker's external test bytes are unavailable. The clip ID `overlong-child` follows the existing App overlong-child positive. Do not label this native ADD output.

Source frozen at App `35ebae007d848ff22d8da89461bdb66efc93472f`, `src/tools/video-editor/data/shotComposition.fixture.json`; mutation matches the existing test helper `withOccurrenceRevision`: replace only prepared occ-1's child clips. The authored occurrence duration remains 2000 ms. App's actual projector derives 4000 ms from next same-lane occ-2 at 4000 ms, against 5000 ms content. The Agent editor analog takes this effective cap explicitly; it does not copy App's cap derivation.

| Source/public evaluation at 30 fps | Raw authored diagnostic | Settled product/editor projection |
|---|---:|---:|
| hold (s) | 5 | 4 |
| canonicalTiming.durationMs | 5000 | 5000 |
| occurrenceDurationMs | 4000 | 4000 |
| ownDuration (frames) | 150 (diagnostic) | 120 |
| drawDuration (frames) | 120 | 120 |
| clipOpacity at frame 105 | 1 (diagnostic only) | **0.5 product golden** |
| frame 119 layer count | 1 | 1 |
| frame 120 layers | [] | [] |

The clips differ ONLY in hold. Public pure `prepareScene` receives the no-transition incoming vector `[null]`, so it applies the existing occurrence cap. Public `clipOpacity` and `queryTrackFrame` are exercised from the actual pinned public package; no private fade formula or threshold change is introduced. The raw opacity 1 result is an observation only, never a product golden. The original MAIN pixel reference supports product opacity 0.5 and is recorded with exact PNG hashes in the actual-reference document and fixture.

Exact product seams for owners:

- Frozen App `hooks/useTimelineCommandSession.ts:82` and `data/canonicalCompositionState.ts:61` call the default clamped projector. `data/shotCompositionProjection.ts:440–449` shortens source hold/to. `compositions/playerEvaluation.ts:20–23` retains that shortened duration and `compositions/VisualClip.tsx:301` evaluates its fade. The editor/read representation retains its clamped positive. No global/default `renderConfig` activation or additional caller policy is authorized here.
- Agent `astrid/core/timeline/shot_composition_projection.py:_project_clip` also shortens hold/to. Both `astrid/packs/rendering/actions/render/managed_timeline.py:963` and `astrid/sdk/timeline/commit.py:730` consume that projector. The public native-scene join is `remotion/src/host-scene.ts:25`. This worker does not change any of these product paths.
- MAIN `e51595c6` has the same source-shortening branch. The actual MAIN render reference settles the visible result at 0.5; the frame-105 PNG SHA256 is `c0b0adc7856e2750137315451a9657661925436746d0da1e9cd6a2527d14431b`, and the frame-90 control SHA256 is `7640face10c33eb4c8682b890ddcc6faacaf0e57c0810e9438e4b2df8a88444a`.
- Only the existing Agent projector analog and pinned public evaluator are exercised in this lane. The managed production render join remains an unresolved strict expectation; this handoff does not claim one-compiler completion or force a cap in a production proof.

Actual tests/evidence:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-m3-cap-fade-main-reference /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_compile_contracts.py tests/timeline/test_shot_composition_projection.py tests/core/timeline/test_shot_composition_projection_volume.py
```

PASS: 52 passed, 3 xfailed in 2.62 s. The two pre-existing strict xfails are unchanged audio vectors 10–11; the third is the explicit unresolved production render expectation. The new passing cases cover the clamped Agent projector analog, settled product/editor public evaluation at 0.5, raw authored-clock diagnostic at 1, and half-open frame 119/120 drawing. The cases extract the current pinned Agent public12 archive into a private pytest temp directory and execute its pure runtime exports with Node; this is not admitted/pinned Remotion render evidence. Python is the read-only shared venv's 3.13.16.

The actual frozen App source probe also passes preservation, hold-only-difference, opacity, own/draw-duration and frame-119/120 assertions. It bundles actual App source (no product substitution) with read-only esbuild and public12 evaluation. Reproduce using:

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-visual-cap-fade-vector/notes
python3 "$N/prepare-source.py"
node "$N/run-app-probe.mjs"
node "$N/app-probe.mjs"
```

PASS, exit 0. The first bundler attempt lacked the frozen vendored browser source and editor-sdk alias; exporting the candidate's own vendor files and using its real SDK alias fixed resolution. No stub or product source edit was used. The complete successful output is in the expanded handoff. Private exported source and bundled output are cleaned; reproduction creates them only inside this worker's notes directory.

`git diff --check` and focused Ruff E4/E7/E9/F check both pass. App source fixture structural equality against its frozen Git blob, and the exact hold-only difference, were checked directly and pass.

Existing tests located for the subsequent owner fix (source inspected, not executed by this worker): App `data/shotCompositionProjection.test.ts` overlong-child clamp positive, `compositions/TimelineRenderer.sequence.test.tsx` compiled-cap renderer dispatch (starts with manually supplied input), and Composition `typescript/tests/scene-evaluation.test.ts` incoming-vector cap test. They do not replace a production projector-to-renderer regression. Agent projection neighbours ran above. No Runtime acceptance suite ran.

Next: source owners qualify the managed production raw-source/cap boundary through actual production callers. Keep editor clamp tests unchanged. No full suite, browser/socket test, PCM, Runtime acceptance, unified Gate 6, or release qualification was run/requested here. The requested fixture/test/document/handoff work is complete; the MAIN visual golden is settled, while the production join remains explicitly unresolved.
