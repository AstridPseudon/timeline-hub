# Conditional renderConfig mounted consumer seam

**Design task complete. UNAPPLIED proposal only; no product activation or merge request.** Read PLAN, COMMON, Viewing INBOX through 10:40 (and 10:55 correction), `app-root-raw-render-source-clock.md`, current App source, public12 port report/source, and the Main source-vector/capture reports. No decision was reinterpreted or bypassed.

**Contrary evidence requiring the orchestrator/Agent decision:** `handoff-vw-m3-main-image-cap-source-vector-REPORT.md` reports unmodified Agent MAIN `a411628f8fd6129f9c58c332019b56769d997384` projects hold5 to hold4 and serializes hold4 into its ordinary Composition6 Root. Its source predicts opacity0.5 at105/30, contrary to the suggested raw5/opacity1 direction in INBOX10:35. This is a source result, not decoded pixels; Main capture is still blocked/unverified according to the read report. I did not run or repeat that worker's evidence. Do not treat the conditional 10:40 approval as a confirmed visual golden. The Agent public golden and Viewing physical Main confirmation remain prerequisites.

## Source and patch identity

- Assigned App worktree: `667498cc49b4ec2b1ccd3a515eb87311c5126c93`. Observed current App integration: `7bb885b638838588a0dff81b64b7c34960ac07f3` (only media CORS product/test changes versus this worktree). Integration had three unrelated untracked vendor leaf links; none were touched.
- The refreshed integration/worktree does **not** yet contain `compositions/playerEvaluation.ts`, the public12 compiledTransitions delivery, or the initial/command-projection tests cited in the raw-clock report. A patch against that report cannot silently assume those changes are integrated.
- Exact proposed consumer patch is based on the raw-clock report's **frozen public12 App source** `5117b9da2e17828ec0b3cfbcdf3ff4987dc77ab3`. This source retains MAIN render/admission/download. Frozen source hashes are in `handoff-vw-m3-renderconfig-consumer-seam-source-identity.json`.
- `handoff-vw-m3-renderconfig-consumer-seam-consumer-UNAPPLIED.patch`: five consumer/caller paths, no type/producer/projector, renderer policy, compiler, outbox, Runtime client, or dependency edits. It must be reconciled onto ONE App-owned branch after the public12 prerequisite; it is not directly ready for today's integration. No source files were copied persistently.

## Exact minimal contract and selection

App adds only `renderConfig?: ResolvedTimelineConfig` beside `editProjection?: TimelineEditProjection` in the existing `src/tools/video-editor/lib/timeline-data.ts::TimelineData`. There is no new exported DTO, selection type, store, counter or signature authority. `TimelineEditProjection` and `ResolvedTimelineConfig` keep their existing definitions.

The mounted surface selects one existing store slice object, with `shallow` equality:

```ts
const { resolvedConfig, timelineData } = useTimelineDataSelector((timeline) => ({
  resolvedConfig: timeline.resolvedConfig,
  timelineData: timeline.data,
}), shallow);
```

This is a local selector result, not a second snapshot store. The slice's memoized `resolvedConfig` remains the ordinary fallback. The command selection and fact always come from `timelineData` itself, never a separately memoized `resolvedConfig` slice or another/latest graph:

```ts
const projectedConfig = timelineData?.editProjection
  ? timelineData.renderConfig ?? timelineData.resolvedConfig : null;
const fact = timelineData?.editProjection;
const paired = fact && previewConfig === (timelineData.renderConfig ?? timelineData.resolvedConfig);
```

The identity check is equality to the **selected** object. An OR accepting either config would incorrectly certify the clamped editor config while a different raw config is supplied. A renderConfig without a fact is ignored. A missing field with a fact keeps the existing command-preview clamped fallback; no attempt to restore raw timing from canonicalTiming is allowed.

`useVideoEditorPreviewComposition(resolvedConfig, timelineData?)` keeps its existing signature and unresolved shell/media checks. Check the selected render object, not the editor object. Complete public12 command data retain the existing `source:'canonical'` result even when no host graph has loaded; this ensures the public compiler is used without requiring a stale host graph. Incomplete paired render data retain the existing honest cached canonical fallback plus error; a canonical fallback never gets the command fact because object identity fails. Unavailable target information remains separate from delivered pixel identity. The fallback graph/draft is labelled by its own retained revision/base.

`useVideoEditorPreviewSurface` changes only the selector and equality above. On the public12 prerequisite it still calls `compilePlayerTransitions(previewConfig)` and passes that result with the same previewConfig and previewRevision. `RemotionPreview` remains unchanged: its existing `PreviewDelivery` carries `{config, compiledTransitions, revision, generation}` through the paused timer/playing mailbox; metadata reads `delivery.revision`, vectors read `delivery.compiledTransitions`, and Player receives the delivered config (after the existing output-track projection). The existing generation is reused. This proposal adds no clock, opacity, duration, frame rounding, end-cap or fade policy.

## Parent render and other consumers in the patch

`useRenderState` gains ONE trailing optional argument, `timelineData?: TimelineData | null`, after `canPersistVisualSeamConfig`. Its sole production caller in `useTimelineState` passes **`save.data`**, from the same render as `derived.resolvedConfig`; do not pass `save.dataRef.current` opportunistically after awaits. Inside useRenderState, the existing committed graph resolver remains the no-fact path. The existing preview composition hook is invoked unconditionally, and its result wins when this same data has an editProjection. This avoids a new resolver/projector and ensures a command preview and parent browser-render/export planner consume the same selected object. Unresolved selected data give the existing render guard its error; cached preview fallback is not silently exported as the requested command. Missing field with a fact falls back to the existing command config rather than choosing an unrelated accepted graph.

This deliberately retains the small existing graph useMemo alongside the reused hook: no-fact parent render continues to use MAIN's committed graph, while the preview hook retains its existing draft behavior. Removing the graph memo by always using the preview hook would also change ordinary parent export to select popup drafts. No such behavior change is proposed.

`VideoEditorAssetPanelSurface` already has `data`; it passes that same snapshot into the existing hook for panel stills. Its editor rows, registry/control inputs and transcript binding are unchanged. `PreviewPanel` and `useDerivedTimeline` are untouched; controls/rows keep their existing clamped vectors. `CompactPreviewCore` is a separate direct graph consumer, outside this mounted-surface patch; do not claim this proposal proves every App preview. App/Viewing should include its command-data selection review in the eventual shared unit if that surface is an active command-session host.

Managed Runtime rendering still uses MAIN's existing save barrier, admission and exact server snapshot. This transient field must never be added to its wire payload, history, AuthoringBundle, recovery persistence or a render-input certificate. Parent consumer selection supplies its existing local rendering/planning inputs; it does not certify that an acknowledged server render equals an unacknowledged browser draft. MAIN's scheduling, admission/version checks, streaming and download code are unchanged.

## One exact App shared-branch handoff request

**To the App owner via the orchestrator:** reserve **`tl/app-m3-renderconfig-atomic-pair`** as the ONE producer/type/projection + consumer handoff branch. This is a requested branch name, not an existing/agreed branch or a branch created here. Base it on the owner-approved refreshed public12 source (the draft is pinned to 5117b9 above), after Main capture and the Agent golden settle the 5/4/fade vector. Return its exact SHA and changed-path list to Viewing for mounted lifecycle qualification before any integration merge. Do not merge separate producer and consumer halves.

On that branch, App owns:

1. The one optional TimelineData field at the location above, including disposal with editProjection on ordinary edits/fact invalidation. Audit `useTimelineCommit`'s existing spread/fact invalidation, generic patch builders, rebuild paths and history/recovery serialization; the new field must not survive as stale raw data or enter durable snapshots.
2. One same-closure production: default clamped editor `config/resolvedConfig/rows/meta`; prebuilt resolved renderConfig through existing `projectCanonicalComposition(prepared, baseConfig, {clampToOccurrenceDuration:false})`. Keep the same effective occurrence cap/registry and pinned asset resolution. Rebuild both from bootstrap, accepted closure and recovery; apply existing local/recovered patches to both before one commitData call. A failure, stale generation or disposal must not publish half a pair. Do not reconstruct source fields from canonicalTiming or infer raw source from the clamped object. Preserve hold5/from2/to7 versus to8 and children lost by clamping.
3. The existing graph/draft render-input resolver's raw projection option where approved, leaving read/editor/default callsites clamped. A graph-only change does not fix the command override. No projector default flip, new projector, draft-session masquerade, or extra raw timing app fields.
4. The same-render `save.data` argument to parent render, and coordination of the panel-still caller hunk. These are included in the unapplied consumer patch solely for a concrete reviewable unit; no App-owned file was edited.

Viewing contributes the attached consumer patch and the acceptance matrix below, keeping public12 compiler/delivery machinery intact. Agreement means both owners name that single branch/SHA and all prerequisites are satisfied; silence or this written proposal is not agreement. No user permission question is needed.

## Validation and limits

Executed artifact check, from the assigned worktree (absolute commands):

```sh
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-renderconfig-consumer-seam-validation-input.py | node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-renderconfig-consumer-seam-tests.cjs
```

**Exit0; 6 artifact checks passed, 0 failed.** The command streams `git show` source in memory, verifies exact source hashes/hunk context and parses all five proposed TypeScript/TSX files using read-only installed TypeScript. It does not execute the candidate, typecheck missing producer types, compile a film or prove lifecycle behavior. Log: `handoff-vw-m3-renderconfig-consumer-seam-tests.log`. Final `git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-renderconfig-consumer-seam-consumer-UNAPPLIED.patch` also exited0 against the five original frozen public12 files exported into a private temporary worker directory; that directory was removed immediately. No patch was applied.

Initial artifact runner attempt (`node --test ...-tests.cjs`) could not start its child process. Direct execution diagnosed `spawnSync git EPERM` (1 artifact allowlist check passed, 5 setup errors). The final runner uses Python for read-only Git source streaming and Node in-process tests; no permission escalation or dependency write. These setup failures are not product regressions. An earlier draft against the assigned current tree passed `git apply --check`; that draft was superseded and is not the final public12-pinned patch evidence.

No main behavioral suite was run: there is no activated product/type/producer change to qualify, and the requested golden/shared-branch preconditions are unmet. The accompanying acceptance matrix specifies main-suite tests to add/run after those gates, without replacing existing expectations. Full suites, browsers, sockets, actual renders, installs, network, builds, whole-project typecheck and Runtime acceptance were not run/requested. No deps, caches, integration files or refs were modified. No product tests were weakened, skipped, deleted or marked failing.

Final `git diff --check` and `git status --short`: exit0, empty. Worktree diff: 0 paths, +0/-0. All report/proposal/check artifacts use this flat absolute design prefix; harness commit-msg/DONE use the assigned worker directory. Design work is complete; product work remains contingent, not implicitly authorized for activation. Next: orchestrator reconciles contrary Main evidence with Agent, App supplies the exact single branch, then the producer and mounted consumer tests run on that paired tree.
