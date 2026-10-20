# Raw render source clock: contract stop

**BLOCKED; no product changes.** The P1 reproduces through both production producers and the public12 compiler/evaluator. Keeping the existing editor/read projection while fixing the command render input requires an additional transient host representation, or an approved change to the current dual-use config contract. The brief explicitly says: “If requires new host field/cross-manager contract, write exact proposal and evidence STOP dependent code/escalate instead inventing it.” This report takes that stop. It requests no KEEP or integration action.

Source: App `5117b9da2e17828ec0b3cfbcdf3ff4987dc77ab3`, tree `e7e282fc958942cea263566a66b2e72d21913e0e`. PLAN, independent refreshed-root P1 review, popup consistency investigation, and visual/audio compile contracts were read first. No settled decision is disputed. Repository diff: **0 paths, +0/-0 lines**. All retained artifacts are in this requested design path or this worker's notes/report paths.

## Exact producer/consumer trace

1. `RuntimeDataProvider.loadTimelineCommandBasis` (`src/integrations/runtime/dataProvider.ts:778`) reads the pinned parent/shot/internal images, checks manifest/identity consistency, and returns the canonical document plus the existing graph. Its private `runtimeGraphToContractFromCanonicalDocument` (`:2142`) builds that graph from the same closure. The session opens its raw source with `authoringBundleFromDocument`; the editor bundle is not a render DTO.
2. `useTimelineCommandSession.ts:79-84` prepares that graph and calls **default** `projectCanonicalComposition`. `shotCompositionProjection.ts:439-449` shortens active child `hold`/`to`, and drops children starting beyond the effective cap. The projector already records the effective occurrence boundary in `app.canonicalTiming`. Effective duration comes from the existing content/next-same-lane calculation; it is not simply the stored occurrence duration.
3. The hook passes this clamped config to `buildTimelineData` (`:92-98`), including recovery patches. `TimelineData.config`, editor rows/meta, and `resolvedConfig` consequently all contain the shortened duration. The hook installs the result with its exact `editProjection` fact (`:104-111`). Immediate local preview (`:132-150`) patches that same data; accepted and recovery projections return through the same clamped producer. The retained raw `AuthoringBundle` is private to the command session; it is not carried alongside that displayed snapshot.
4. The graph-based preview/export resolver also calls the default projector (`data/canonicalCompositionState.ts:61`). `useVideoEditorPreviewComposition.ts:15-27` supplies the existing canonical draft or canonical composition to this resolver. However, when command data has a projection fact, `:29-39` deliberately returns **that data's `resolvedConfig`** instead. This protects against rendering an unrelated older/latest graph with the command fact.
5. `useVideoEditorPreviewSurface.tsx:40-46` compiles the selected canonical config with the existing `compilePlayerTransitions`. Revision pairing at `:47-49` depends on `previewConfig === timelineData.resolvedConfig`. Its actual downstream delivery already carries config and compiler vector together. No portal, mailbox, mobile, provider or render/download change is needed to demonstrate the defect.
6. `compositions/playerEvaluation.ts:20-29` adapts the duration it receives and calls the public clip-opacity evaluator; `:58-60` calls the one public `compileCanonicalTransitions`. Public12 `dist/chunk-DMRW7SC3.js:571-590` reads `canonicalTiming.occurrenceStartMs/occurrenceDurationMs`, derives the existing frame end cap, and passes it separately from source duration to `prepareTrack`. `preparePlayerTrack` supplies the same clip clock to `prepareCompositionScene`. This existing compiler cap correctly excludes frame 120 when raw source duration remains five seconds. No evaluator, fade, rounding, or cap-policy modification is justified.

## Why the available seams do not safely complete this repair

- Flipping the projector default would erase the passing clamped-editor behavior at `shotCompositionProjection.test.ts:481`. Changing only the hook's clamp option also changes its editor rows, selected-clip controls, and read config. `useDerivedTimeline.ts:20-29` uses `resolvedConfig` for editor-selected clips, so placing raw timing there alone would still change the editor contract.
- Changing only `canonicalCompositionState.ts:61` fixes the graph lane but leaves the command override above clamped. It cannot close P1.
- Selecting `shots.canonicalComposition` instead of command `resolvedConfig` abandons the existing closure/fact pairing. The hook adopts a graph only for projections without remaining previews (`useTimelineCommandSession.ts:112`). Local command data therefore need not have a matching host graph. The existing lifecycle tests intentionally retain a different older graph while command data wins.
- `canonicalDraft` is an existing occurrence-editor session contract (`runtime/ports.ts:13-23`), keyed by project/parent/**occurrence/editorSessionId**, and managed by `useAstridShotsHost`. Treating a parent command outbox as that draft, inventing an occurrence/session identity, or allowing it to overwrite popup drafts would be a contract change, not reuse of an unchanged approved seam.
- Recovering raw fields from `canonicalTiming.durationMs` is insufficient. The projector computes that field from authored hold/duration precedence, but preserves a trim pair in the projected clip when present. The focused passing probe uses `hold:5, from:2, to:7` versus `hold:5, from:2, to:8`: both have identical bounded source fields **and identical canonicalTiming**, yet their unbounded endpoints are 7 and 8. Rows discarded by the clamp are another irreversible loss from this representation. Adding raw timing fields inside `app` would itself add a host contract and would still need to handle dropped rows.

## Exact proposal for App + Viewing approval (not implemented)

Add **one optional transient `TimelineData.renderConfig?: ResolvedTimelineConfig`**, paired atomically with the existing `editProjection`. It is not authored, serialized, sent over the wire, or added to `AuthoringBundle`. This is a proposed field, not an approved name or landed API.

For occurrence-backed command projections, the App producer keeps its current bounded `config`, `resolvedConfig`, rows and meta. From the **same prepared immutable closure** it obtains the raw render config through the existing `projectCanonicalComposition(..., {clampToOccurrenceDuration:false})`; this still supplies the existing effective occurrence cap. Resolve its assets against the same pinned registry. Apply the existing local/recovery patches to both representations before atomically installing the fact. Rebuild it from every returned accepted closure and recovery basis; drop it when the fact is invalidated by an ordinary edit. Do not reconstruct source timing in a player adapter. No new projector or timing compiler is proposed.

The App preview-input producer would choose that paired render config for occurrence-backed command data. The graph/draft render-input resolver would use the same raw-producing path, leaving the projector's default/read callsites untouched. Ordinary parent-only configs retain their existing path. Viewing must approve updating the surface's **existing config/fact identity pairing** to recognize the new paired config, while retaining the existing deferred config/vector delivery and stale-graph defenses. `VisualClip`, `playerEvaluation`, public compiler/end-cap policy, and render/download policy remain unchanged. This required consumer-contract change is why the current worker did not land the producer half alone.

After approval: promote the retained ordinary positives into the neighboring main suites, implement this bounded producer/consumer unit, and prove local + ACK + recovery vectors on actual timing-changing commands, not only the no-op source-clock isolation case below. Re-run the original overlap/gap/rational-clock/fade/opaque/source-window neighbors without replacing expectations or adding failure markers. This report does not claim a repair is complete.

## Executed proof

Retained ordinary tests: `workers/app-m3-root-raw-render-source-clock/notes/sourceClock.test.tsx`. No tracked test was changed, skipped, weakened, or given an expected-failure marker.

- **Exact external prepared-shot case**, including the original `occ-1:overlong`, five-second image, one-second fade out and four-second next-occurrence cap, now goes through the production `resolveCanonicalComposition` and public compiler/scene/opacity evaluator. Editor vector: hold **4**, opacity **0.5** at frame **105**, visible at 105, excluded at **120**. Unbounded vector: hold **5**, opacity **1**, visible at 105, excluded at 120. Production resolver returns the editor vector; the original required raw-render expectation fails.
- **Mounted production command hook and preview-input consumer** use a separately constructed synthetic canonical document with this same five-second/fade/cap case. The real `RuntimeDataProvider` raw-image adapter, manifest pin checks, adapter preparation and authoring opener run against the bounded in-process transport. A captured **no-op parent clip move** isolates the exact same raw closure during local preview and after an in-process echo ACK. Bootstrap, local and accepted outputs all have hold **4**, opacity **0.5**, visibility true at 105 and false at 120. Both required opacity-1 positives fail. Local and accepted vectors agree with each other; agreeing on the wrong clock is not repair evidence. Raw document equality remains intact.
- The ACK is an explicitly labeled test stub returning the unchanged closure; it proves App producer/consumer behavior, **not Runtime semantic acceptance, idempotency or a new publication**. No authority is inferred from this synthetic setup. The native popup ADD fixture is absent from this task's base; no claim is made to requalify its ADD/ACK vector here.
- The metadata ambiguity positive passes. The existing neighboring main suites also pass, including the original clamped-editor assertion, overlap/gap, rational numeric frame rate, fades, source windows, opaque roots, lifecycle and config/vector pairing coverage.

## Exact commands and results

Commands ran in `/home/user/work/wt/app-m3-root-raw-render-source-clock`. For brevity only in these commands, `N` means the worker's absolute `.../scratchpad/orch/workers/app-m3-root-raw-render-source-clock/notes` path. This is not an environment variable change outside the commands.

The runner config imports the existing repository config, aliases Composition and its peers to **read-only `/tmp/app-coherent-deps12/node_modules`**, and puts cacheDir in `N/vite-cache`. The own-worktree `node_modules` link was temporarily pointed at that same existing private12 tree so native external dependencies use one React instance; it was restored to `/home/user/work/app/node_modules` after testing. Nothing inside either dependency tree was modified. Reproduction requires that own-worktree link adjustment, or an equivalent private source export using the same dependency tree.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  "$N/sourceClock.test.tsx"
```

**Exit 1; 1 passed / 2 failed**, 4.02 s. Final failures are the ordinary production source-clock expectations, with three assertion failures across the two test cases. Log: `notes/counterexamples.log`. During test setup, an initial synthetic parent omitted `config.clips` and an initial mixed React dependency run hit an invalid-hook-call error. Both setup issues were corrected; neither is counted as behavioral proof. Only the final log above is claimed.

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

**Exit 0; 10 files / 192 tests passed**, 30.02 s. Log: `notes/neighbors.log`.

`git diff --stat`, `git status --short`, and final `git diff --check`: **exit 0, empty output**. No repository source/assertion change, build output, or temporary runner file remains in the worktree. The temporary own-worktree dependency link was restored. The requested report, positive red reproduction and logs remain in the assigned orchestrator paths.

## Unknowns and disposition

Actual pixels/audio, browser/Player media decoding, real Runtime acceptance, the current Agent/Runtime pair, native popup acceptance/reload/undo/retry, and timing-changing local/accepted closure parity are **UNRUN**. No full suite, build, browser, socket, project tsc or install was run or requested. No Git commit/merge/rebase/checkout/push was run. Renderer policy and all protected product areas are untouched.

**Next step:** orchestrator/App/Viewing approve the transient paired render-input contract (or supply an approved existing representation that satisfies the same closure and unchanged-editor requirements), then resume the bounded implementation and promote the red positives. Worker `BLOCKED` records this contract stop; no DONE or KEEP is asserted.
