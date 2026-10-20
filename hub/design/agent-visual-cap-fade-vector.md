HOLD — owner 11:08 decision supersedes the proposed raw-clock render expectation. This is diagnostic source/public-evaluation evidence only. MAIN source predicts projected opacity 0.5; real MAIN pixels must settle the reference. Do not merge 27e3b3b1, promote raw opacity 1 as a product golden, or activate renderConfig meanwhile.

Agent INBOX 10:35 diagnostic vector is ready for Viewing confirmation. Product source is unchanged. No MAIN visible result is claimed.

The corpus is `tests/editing_conformance/fixtures/visual_compile_contract.json`, key `cap_fade_closure` (schema 4), with contract section 3 in `docs/design/visual-compile-contract.md`. It includes the verbatim frozen App fixture, its provenance/blob, the explicit 5 s image + 1 s fade-out mutation, and the complete actual raw/default projected clip objects. Existing editor clamp positives remain passing.

Expanded handoff: [agent-visual-cap-fade-vector.json](agent-visual-cap-fade-vector.json). It retains the entire original App fixture, prepared object (including contract and every occurrence/revision), both complete projected configs, both selected clips and exact public observations. No opaque fields were filtered. It is a reproducible synthetic counterexample from the review description; the original review worker's external test bytes are unavailable. The clip ID `overlong-child` follows the existing App overlong-child positive. Do not label this native ADD output.

Source frozen at App `35ebae007d848ff22d8da89461bdb66efc93472f`, `src/tools/video-editor/data/shotComposition.fixture.json`; mutation matches the existing test helper `withOccurrenceRevision`: replace only prepared occ-1's child clips. The authored occurrence duration remains 2000 ms. App's actual projector derives 4000 ms from next same-lane occ-2 at 4000 ms, against 5000 ms content. The Agent editor analog takes this effective cap explicitly; it does not copy App's cap derivation.

| Source/public evaluation at 30 fps | Raw render input | Default editor projection |
|---|---:|---:|
| hold (s) | 5 | 4 |
| canonicalTiming.durationMs | 5000 | 5000 |
| occurrenceDurationMs | 4000 | 4000 |
| ownDuration (frames) | 150 | 120 |
| drawDuration (frames) | 120 | 120 |
| clipOpacity at frame 105 | 1 | 0.5 |
| frame 119 layer count | 1 | 1 |
| frame 120 layers | [] | [] |

The clips differ ONLY in hold. Public pure `prepareScene` receives the no-transition incoming vector `[null]`, so it applies the existing occurrence cap. Public `clipOpacity` receives the authored content clock; `queryTrackFrame` verifies half-open drawing. No private fade formula, local compiler or threshold change is introduced. This tests clip opacity, not pixel alpha or decoded output. The existing per-call App option was used ONLY to observe raw bytes in the diagnostic; it is not a proposed product policy.

Exact product seams for owners:

- Frozen App `hooks/useTimelineCommandSession.ts:82` and `data/canonicalCompositionState.ts:61` call the default clamped projector. `data/shotCompositionProjection.ts:440–449` shortens source hold/to. `compositions/playerEvaluation.ts:20–23` retains that shortened duration and `compositions/VisualClip.tsx:301` evaluates its fade. The rendering/preview boundary needs raw authored source plus the existing cap while the editor/read representation retains its clamped positive. No global default flip or additional caller policy is authorized here.
- Agent `astrid/core/timeline/shot_composition_projection.py:_project_clip` also shortens hold/to. Both `astrid/packs/rendering/actions/render/managed_timeline.py:963` and `astrid/sdk/timeline/commit.py:730` consume that projector. The public native-scene join is `remotion/src/host-scene.ts:25`. This worker does not change any of these product paths.
- MAIN `e51595c6` has the same source-shortening branch, and main pins Composition 0.0.6. Its retained `docs/reference/timeline-composition-v0.0.6/lib/fade.ts:29–47` uses the supplied duration. Source therefore suggests that feeding a clamped 4 s image to that helper would give 0.5, not 1. That is a reference discrepancy to resolve explicitly, not evidence that MAIN visibly rendered 1. No settled decision was changed.

Actual tests/evidence:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-m3-visual-cap-fade-vector /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_compile_contracts.py tests/timeline/test_shot_composition_projection.py tests/core/timeline/test_shot_composition_projection_volume.py
```

PASS: 51 passed, 2 xfailed in 4.07 s. The two strict xfails are unchanged audio vectors 10–11; no markers added/removed. The new cases are `test_cap_fade_editor_projection_keeps_clamped_timing_and_authored_source` and the two `test_cap_fade_public_source_clock_and_half_open_draw_cap` parameterizations. The latter extract the actual pinned Agent public12 archive into a private pytest temp directory and execute its pure runtime exports with Node v22.22.0; this is not admitted/pinned Remotion render evidence. Python is the read-only shared venv's 3.13.16.

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

Next: Viewing replays MAIN's actual render on this input/explicitly labelled playable-media analog, confirms the reference or reports the discrepancy to the orchestrator, then source owners qualify the raw-source/cap boundary through actual production callers. Keep editor clamp tests unchanged. No full suite, browser/socket test, render, pixels, PCM, Runtime acceptance, MAIN replay or release qualification was run/requested. The requested fixture/test/document/handoff work is complete; physical confirmation and product correction remain with the respective owners.
