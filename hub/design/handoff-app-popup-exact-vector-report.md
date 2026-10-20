# Exact native ADD vectors — source-only confirmation

Base: `309cb7a463833126e3af730fb3c6ff536d9e457c` (`tl/app-m2-popup-core-qualify`). Read PLAN, the shared popup consistency document and orchestrator 04:57 INBOX. No product, pin, fixture, root, installed dependency or shared document was changed.

**A is authored at [8,18) seconds and B at [10,20), both on `picture`. The reported 270/330/60 and 330/390/60 describe the existing `clip-a` children BEFORE App occurrence bounding, with an explicitly numeric FPS argument. They do not describe the new ADD child or the default accepted-path A row. Clamp IS exercised by this actual fixture.**

This is production-function evidence through the real RuntimeDataProvider raw graph adapter, not real mouse interaction, mounted UI, Runtime acceptance, public-scene evaluation, pixels or audio.

## Inputs and execution

The entire frozen `src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json` remains unchanged: SHA256 `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46`. No corrected fixture was published; no evidence warrants changing its authored bytes to match an expected answer.

`occurrenceMediaExactVectors.test.ts` is retained here as an investigation probe, with imports relative to its execution location `src/tools/video-editor/commands/`. It uses the earlier bounded fixture transport, serving the actual input/output parent, shot and internal immutable images to `RuntimeDataProvider.shotComposition.loadAtHead`. The product's private `runtimeGraphToContract`, asset normalization and `createShotCompositionAdapter.prepare` build both graphs. There is no hand-built graph or `occurrenceMediaFixtureGraph` use.

The probe captures ADD from the real input authoring bundle and verifies exact command and record equality with the native recipe. Every captured occurrence's internal payload matches reopening actual `add.output`, including unchanged B and opaque/null/registry data. It compares the captured local preview over the original input graph with independently reopening the output graph and using the same local helper. Their projected vectors agree. Separately it runs the normal accepted-hook operations (`projectCanonicalComposition(prepared)` with defaults, then `buildTimelineData`) on that same prepared output graph.

It then directly calls `boundCanonicalConfigClips` and the actual frame/duration helpers. These are renderer preparation functions; the renderer itself was not mounted. The probe checks that these operations preserve the raw documents, raw ADD row and display configs. Complete observations are in `vectors.json`; the probe passes preservation/capture assertions without asserting that the observed projection gap or invalid FPS is correct behavior.

No publication ID, accepted identity or accepted/local `editProjection` was invented. The fixture has no publication receipt. Local retains input revision `parent-1`; the default projector comparison uses the actual output parent revision. “Accepted-path” means the deterministic projection operations used by `useTimelineCommandSession.ts:83-95`, not a Runtime-accepted fixture.

## Occurrences and units

| Occurrence | Raw and adapter span | Child content extent | App effective span |
| --- | --- | --- | --- |
| A | [8,18), duration 10000 ms | 7000 ms | [8,10), duration 2000 ms |
| B | [10,20), duration 10000 ms | 7000 ms | [10,17), duration 7000 ms |

The raw graph/adapter retain both 10-second durations. `timelineOccurrenceHardDurationMs` finds B at 10 on A's lane; `timelineOccurrenceEffectiveDurationMs` caps A's 7-second content extent at that 2-second distance. B has no later blocker and uses its 7-second content extent. These derived bounds do not rewrite the authored occurrence spans.

Child `at` is occurrence-local timeline seconds. `from`, `to`, and `hold` are source seconds; speed divides source duration once. Existing `clip-a` has local `at:1`, source [2,6), `hold:4`, speed 2, hence two timeline seconds. Newly added `reserved-child` has local `at:0.125`, the same source window/hold/speed, `params:null` and opaque fields; its global unbounded span is [8.125,10.125). No copy of this new row exists in B. B still references original `chapter-shot`/`shot-1`/`internal-1`; A uses the actual materialized output shot and internal IDs.

The raw child and its source [2,6) window remain exact before and after projection. Projected trim changes are derived bounds. `canonicalTiming.durationMs:4000` is source duration here, not four timeline seconds; A's `occurrenceDurationMs:2000` is its derived bound, not the raw stored duration.

## Actual config/resolved output in seconds

The following differences occur in both config and resolvedConfig:

| Row | Local helper (captured and reopened) | Default accepted-path projector |
| --- | --- | --- |
| `clip-a` (parent) | at 1, hold 2 | same |
| `clip-b` (parent) | at 5, hold 2 | same |
| `occ-a:clip-a` | at 9, from 2, to 6, speed 2 | at 9, from 2, to 4, speed 2 |
| `occ-a:clip-b` | at 13, hold 2 | omitted |
| `occ-a:reserved-child` | at 8.125, from 2, to 6, speed 2 | at 8.125, from 2, to 5.75, speed 2 |
| `occ-b:clip-a` | at 11, from 2, to 6, speed 2 | same |
| `occ-b:clip-b` | at 15, hold 2 | same |

The local helper opts out at `occurrenceMediaGesture.ts:102-103`; default `projectClip` clamps at `shotCompositionProjection.ts:437-447`. For the actual new row, `2 + (10 - 8.125) * 2 = 5.75`; for A's existing clip-a, `2 + (10 - 9) * 2 = 4`. A clip-b begins beyond 10 and is omitted. This case is overlap with the next same-lane occurrence, **not hypothetical content beyond A's authored endpoint 18**.

## Renderer preparation and the FPS mismatch

`boundCanonicalConfigClips` independently takes the seven local rows to the same six bounded row geometries as the default accepted-path projection. Calling it on the accepted-path rows keeps those six geometries. Thus the earlier config/resolved mismatch alone does not prove a picture/audio mismatch.

This boundary is called by `TimelineRenderer.tsx:1605-1611` for tracks without a compiled canonical transition vector. The exact new row retains literal `clipType:video`; `compilePlayerTransitions` only admits media/image/hold and requires every row on a track to qualify (`playerEvaluation.ts:32-35,46-60`), so this picture lane is excluded. That source trace supports applying the ordinary boundary in this fixture; no compiled vector was fabricated. Host dispatch and playable media were not qualified.

**The unchanged native output FPS is the object `{numerator:30000,denominator:1001}`, including after both `buildTimelineData` paths.** The normal preview reads it directly (`RemotionPreview.tsx:277-285`); `secondsToFrames` expects a number and multiplies by it. Direct calls with the actual output value produce `NaN` start/end/duration for every row. Therefore finite frame vectors cannot truthfully be claimed as the native App's actual playable output.

For comparison ONLY, the probe separately supplies numeric `30000 / 1001` to the real frame helpers, without editing fixture or config. Start is rounded separately; end is rounded start plus rounded duration, as in the App helper. Triples below are **start / exclusive end / duration in render frames**, not source windows or an accepted compiled artifact:

| Row | Local before boundary, numeric diagnostic | Default accepted path, numeric diagnostic | Either path after boundary, numeric diagnostic |
| --- | --- | --- | --- |
| parent clip-a | 30 / 90 / 60 | 30 / 90 / 60 | 30 / 90 / 60 |
| parent clip-b | 150 / 210 / 60 | 150 / 210 / 60 | 150 / 210 / 60 |
| A existing clip-a | **270 / 330 / 60** | **270 / 300 / 30** | **270 / 300 / 30** |
| A existing clip-b | 390 / 450 / 60 | omitted | omitted |
| A new reserved-child | **244 / 304 / 60** | **244 / 300 / 56** | **244 / 300 / 56** |
| B existing clip-a | **330 / 390 / 60** | **330 / 390 / 60** | **330 / 390 / 60** |
| B existing clip-b | 450 / 510 / 60 | 450 / 510 / 60 | 450 / 510 / 60 |

Agent's two reported triples align with existing clip-a local/unbounded diagnostic values. A's triple does not align with App's default projection or boundary; B's does. If “child” meant the ADD row, that is a row-identity mismatch as well. The probe establishes no reason to replace the native fixture with A-at-0/B-at-8 or another hypothetical overhang.

## Verification

Executed from the assigned worktree with Node v22.22.0, Vitest 4.1.5. Probe files were temporarily copied into `src/tools/video-editor/commands/` for normal test resolution, then removed from the suite and retained under notes.

```bash
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/occurrenceMediaExactVectors.test.ts
```

**1 passed**, exit 0 (`exact-probe.log`, exploratory run). Final version, including post-boundary preservation checks, ran with the focused neighbors:

```bash
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/lib/canonicalRenderBounds.test.ts src/tools/video-editor/commands/occurrenceMediaCapture.test.ts src/tools/video-editor/commands/commitSession.occurrenceMedia.test.ts src/tools/video-editor/commands/occurrenceMediaExactVectors.test.ts
```

**228 passed, 5 files**, exit 0 (`targeted.log`). This includes the exact probe. No permanent test was added.

```bash
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/occurrenceMediaProjectionConsistency.test.ts
```

**1 failed, two soft parity assertion failures**, exit 1 (`preserved-red.log`): config and resolvedConfig still differ as reported. The previous red reproduction is retained byte-for-byte under notes, SHA256 `15ddcbc19fc1b0ad286094654312c90164b9366902e6c0341ba92851f2d21afb`. It was not weakened, inverted, skipped or converted into a passing behavior requirement. Its pre-parity assertions pass.

```bash
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/occurrenceMediaExactVectors.test.ts --max-warnings=0
git diff --check
sha256sum src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json
```

ESLint **exit 0** (`probe-lint.log`); diff check **exit 0**; fixture hash unchanged as above. Existing tracked files have no diff.

Shared dependency limitation: `node_modules` is the provided symlink to `/home/user/work/app/node_modules`; its Composition package reports **0.0.10**, while this base's package/lock pin **0.0.8**. Nothing was installed or repinned. The new diagnostic imports no public Composition evaluator/player planner; the reported calculations directly call the worktree's App adapter, projector, builder, boundary and frame helpers. These results are not qualification of the locked public package or a complete renderer run.

## Decisions, limits and manager handoff

Kept this as a source-only investigation and left the original red test outside the main suite. An observational probe belongs in notes; asserting the gap/NaN as desired product behavior would encode missing behavior. No clamp option, raw window, policy, graph pin or fixture byte was changed. No full suite, build, tsc, browser, localhost/live Runtime, acceptance/reload/undo/retry, audio/export or pixel test was run.

The assigned investigation is complete; nothing blocks its report. The claim “real App UI produces 270/330/60 for A and 330/390/60 for B” remains unverified and is inconsistent with the default A projection plus the native FPS shape. The suggested shared-document correction is in `suggested-shared-doc-correction.md`; the manager owns applying it. Pass the exact unchanged closure and these stage-labelled vectors to Agent/Viewing for the ONE compiler/reference qualification. Keep popup writer retirement and film-policy decisions with the orchestrator. KEEP is set until manager review.
