# MAIN image-cap half-opacity golden: exact App closure mismatch

**BLOCKED on the precise projection discrepancy below. No production change.** The owner’s 11:59 MAIN reference is accepted: opacity **0.5 at frame 105**, not 1. The existing external next-occurrence diagnostics now pass with that expectation, but the **actual captured raw closure does not produce the same cap through current App consumers**. This contradicts the brief’s assumption that the existing path already matches MAIN for that exact closure. It does not dispute the captured MAIN pixels or propose restoring renderConfig.

## Source and MAIN reference

- App base: `cee35da4b1ed653db50dd9d5c26693fab00f04ad`, normal013/public12 root with corrected wrapper. No production files, package pins, compiler/player policy, Viewing source or Agent source changed.
- Read PLAN, `viewing-main-image-cap-actual-reference.md`, `app-root-raw-render-source-clock.md`, source-vector READY/replay/closure/projected-config artifacts, the earlier Agent cap-fade vector, and current Agent visual-compile fixture/contract/tests. Agent integration was `cf7448ed6c1298b172d004914cfe2bb8c99048e7`; its fixture did not yet contain the new exact MAIN cap golden at this check. No alternative native contract was invented.
- MAIN: `a411628f8fd6129f9c58c332019b56769d997384`, original Root/index/generator/components, lock-exact Composition 0.0.6 and exact theme0.1.1 source-tag mechanism. Reference central run: `vw-m3-main-cap-locked-theme-stage-e2e-viewing-main6-locked-theme-image-cap-three-stills-1020115023-5447`, exit 0. This worker did not rerun it.
- Exact reference: raw image hold5/fade_out1, **one** occurrence with stored duration4000ms; numeric30fps, 1920x1080, MAIN duration120. Frame90 RGBA240/240/240/255, PNG SHA256 `7640face10c33eb4c8682b890ddcc6faacaf0e57c0810e9438e4b2df8a88444a`. Frame105 RGBA122/124/130/255, PNG SHA256 `c0b0adc7856e2750137315451a9657661925436746d0da1e9cd6a2527d14431b`. Against background5/8/20, median source-over fraction is0.5. PNG alpha255 is not layer opacity. The static-public RGB240 image is an executable analog, not native App output, live Runtime acceptance or an owner film.

## Changes and exact current consumer evidence

Added two App test paths only:

- `src/tools/video-editor/data/mainImageCap.fixture.json`: byte-for-byte copy of `design/handoff-vw-m3-main-image-cap-source-vector-raw-closure.json`, SHA256 `ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04`. No added next occurrence, changed hold, asset mutation or reconstructed prepared contract.
- `src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts`: actual `RuntimeDataProvider.shotComposition.loadAtHead` against an in-process transport returning those exact pinned parent/shot/internal records; actual adapter preparation; `resolveCanonicalComposition` → default `projectCanonicalComposition`; actual `compilePlayerTransitions` → public12 compiler; actual `preparePlayerTrack` compiled scene and `preparePlayerClipOpacity`. It requires hold4, f90 opacity1, f105 opacity0.5, and no frame120 layer. It retains these ordinary required expectations and is **RED**, with no xfail/skip/disable.

The exact closure’s occurrence is duration4000ms, but `shotCompositionProjection.ts` derives its effective duration using `timelineOccurrenceEffectiveDurationMs`. `shotCompositionTiming.ts:135–143` uses content extent capped only by the next same-lane occurrence. This fixture has no next occurrence, so App replaces4000ms with5000ms, producing hold5/canonicalTiming.occurrenceDurationMs5000. Public12 correctly evaluates that supplied five-second input: f90 opacity1, f105 opacity1, frame120 still present. Compiler invocation succeeds; the closure remains unchanged. Scene media-alpha status is unknown, so the final test asserts layer identity/content frame and the actual opacity helper separately, without equating unknown media coverage with opacity.

The earlier external diagnostic is materially different: prepared fixture occ-1 stores2000ms but has next same-lane occ-2 at4000ms. App derives the effective4000ms cap there. The mounted no-op echo-ACK diagnostic also has a next occurrence at4s. Those passes cannot certify the single-occurrence captured closure. Changing every projection to min(stored duration, content duration) would also change the original required editor positive from hold4 to hold2; that passing assertion was not touched or weakened. No policy change was guessed.

## Old/new expectation pairs

Retained a copy of the held external diagnostic under this worker’s own `notes/sourceClock.test.tsx`; the other worker’s historical artifacts are untouched. Changes cite the actual MAIN reference:

| External case | Old required expectation | New required expectation | Observed |
| --- | --- | --- | --- |
| Production resolver with next cut4s | same as unbounded hold5/opacity1 | same as editor hold4/opacity0.5 | PASS |
| Mounted local no-op projection | hold5/opacity1 | hold4/opacity0.5 | PASS |
| Mounted echo-ACK projection | hold5/opacity1 | hold4/opacity0.5 | PASS |
| Explicit unbounded diagnostic | hold5/opacity1 | unchanged | PASS |
| Metadata endpoint ambiguity | same bounded metadata, raw endpoints7/8 | unchanged | PASS |
| Exact captured single-occurrence closure | newly required hold4/f1050.5/end120 | required MAIN expectation retained | FAIL: hold5/f1051/layer at120 |

The mounted ACK is an unchanged-closure in-process echo only, not server semantic acceptance or publication. Existing legitimate rawhold5 public-unit source is untouched. The original editor-clamp suite is byte-identical to HEAD.

## Exact commands and results

Commands ran from `/home/user/work/wt/app-m3-main-cap-confirmed-half-golden`. For these commands, set:

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main-cap-confirmed-half-golden/notes
```

The retained config imports this worktree’s normal config, aliases Composition/peers to read-only `/tmp/app-coherent-deps12/node_modules`, and sets cacheDir to `$N/vite-cache`. Only this worktree’s node_modules link temporarily pointed to private12; it was restored to `/home/user/work/app/node_modules`. The external notes’ own dependency link resolves the copied diagnostic. No file/link/cache inside any dependency tree was changed. No install was run.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts \
  "$N/sourceClock.test.tsx"
```

**Exit1; 1 passed file / 1 failed file, 3 passed tests / 1 failed test**, 5.66s. Final log: `notes/reference-and-diagnostics.log`. Exact-closure test has three soft assertion failures: hold5 versus4, opacity1 versus0.5 at105, and a layer at120 versus none. Frame90 control, compiler presence, frame identity and raw-closure preservation pass. Initial setup attempts needed external dependency resolution plus the normal mock handshake capabilities/scopes/health instance ID; those setup failures are preserved in earlier logs, not counted as behavioral proof. An intermediate scene assertion incorrectly assumed declared opaque media; it was corrected to avoid inventing asset-alpha metadata. Only the final three-failure run is the claimed counterexample.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/data/canonicalCompositionState.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/lib/canonicalRenderBounds.test.ts
```

**Exit0; 10 files / 192 tests passed**, 23.24s. Log: `notes/neighbors.log`. Includes original editor clamp, overlap/gap, rational clocks, fades, source windows, lifecycle and config/vector pairing neighbors.

`git diff --check`: exit0. Python byte comparison of captured closure vs candidate fixture and of original clamp suite vs HEAD: exit0, exact match; output in `notes/fixture-and-preservation.txt`. No full/browser/render/tsc/install/socket test was run/requested. No git commit/merge/rebase/checkout/push, shared-dependency write, build output or temporary runner file in the worktree.

## Docs notification and disposition

**Docs: close the contingent transient TimelineData.renderConfig proposal.** The 10:37/10:40 proposal and the stop in `app-root-raw-render-source-clock.md` are historical and withdrawn by owner11:59. Do not activate the field or the conditional Viewing consumer. The new issue is the exact single-occurrence App effective-cap discrepancy above; it does not establish a need for that field. This report is the concrete notification for the orchestrator/docs owner to reconcile the historical coordination page, without touching another owner’s source.

Recommended next step: orchestrator decides the bounded App stored/effective-cap reconciliation against this exact closure while preserving the original editor/read positives; then qualify the retained exact-closure test and Agent shared golden together. A clarification request was sent because the brief both prohibits projection changes and permits a precise existing bug fix against this reference. No dependent production edit was made while that decision is pending. Retained required regression is red, so this is **BLOCKED, not DONE**, and no KEEP is requested. MAIN reference is accepted; unified frame/audio parity, real Runtime acceptance and Gate6 remain unverified.
