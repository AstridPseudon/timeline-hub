# Conditional renderConfig consumer review

**REQUIRES CHANGES; do not activate or merge.** The stage selection/identity seam is reasonable contingent on an atomic producer, but the proposed parent/panel consumption is incomplete. Review complete; no repository edits. The 10:40 Agent + actual MAIN golden prerequisites remain unmet. This report does not choose opacity 0.5 or 1.

Read PLAN, COMMON, CLAUDE.md conventions, Viewing INBOX through 10:55 correction, the consumer REPORT/UNAPPLIED patch/acceptance matrix, raw-clock proposal, donor tests, and MAIN source/capture reports. Decisions were preserved.

## Findings

### P1 — Parent browser render and panel stills lose the compiler vector

The five-file patch selects `data.renderConfig` for parent render and panel stills, but only the stage calls `compilePlayerTransitions` and delivers its result. Frozen prerequisite `5117b9da` establishes the missing downstream steps:

- `hooks/useRenderState.ts:621` passes selected config to `useClientRender`; `hooks/useClientRender.ts:271` sends only `{config, astridElementHost}` to `TimelineRenderer`.
- `components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx:106` passes only config to `TimelineFramePreview`; its `:131` input props likewise omit `compiledTransitions`.
- `compositions/TimelineRenderer.tsx:1607` retains raw clips only for tracks present in `compiledTransitions`; otherwise it calls `boundCanonicalConfigClips`.
- `lib/canonicalRenderBounds.ts:36-44` shortens duration/hold again before clip-opacity evaluation. This helper is byte-identical on 5117 and current 7bb (SHA256 `635790336bf9e67f7142e7f74c1529240be191476a8f0bbf6ad2436c5896dc31`).

Thus selecting the same raw object does not make these consumers render the same clock. For the proposed raw hold5/cap4/fade1 direction, the stage's compiled lane preserves source hold5, whereas parent browser render and the panel's Thumbnail re-shorten to hold4. Source predicts different frame105 fades. This is a source-proven routing defect in the proposed unit, not measured pixels or a ruling on the golden. If the final golden retains MAIN's clamped behavior, the entire raw activation must first be reconciled with that ruling anyway.

**Required handoff correction:** include the existing public compiler/vector delivery at the actual browser-render and panel-Thumbnail boundaries, using the selected config, without changing compiler/opacity policy or introducing a second compiler. Test selected config **and** vector and evaluated frame/end-cap behavior. Preserve no-fact parent committed-graph selection and managed Runtime save/admission/download behavior.

### P2 — Raw source extents can lengthen Player/still metadata

`RemotionPreview.tsx:276-286` derives duration from raw clip `at + getClipDurationInFrames`; `TimelineFramePreview.tsx:115-127` does the same. Neither uses the occurrence cap or delivered compiler extent for metadata. After selection changes to raw data, a source overhang that extends beyond all bounded output increases Player/Thumbnail duration even though the compiler excludes that overhang. A raw image at0/hold5/cap4 alone implies 150 metadata frames at30fps against a 120-frame occurrence. A long overhang capped by a following short occurrence gives the same issue on a multi-occurrence producer output. Rows deliberately retained only in R can extend this further.

Parent `useTimelineState.ts:685` still passes `derived.renderMetadata`, which comes from clamped editor C. The proposed patch therefore also permits different composition extents between parent rendering and preview. This is a source inference; no rendered counterexample or actual producer timing case was executed here.

**Required handoff correction:** prove Player/still duration and seeks against the existing effective output cap, including overhangs and rows absent from C. Supply the appropriate existing bounded composition extent without shortening R's source clock or changing timing policy. Do not simply switch parent metadata to the unbounded maximum. Resolve this within the same shared unit, or explicitly narrow its claimed coverage before implementation.

## What is sound, and what donor tests actually prove

- Select `R = data.renderConfig ?? data.resolvedConfig` only when this same data object has F. The proposed identity check `previewConfig === R` is correct; accepting C OR R would certify the wrong object. One shallow store selector avoids separately reading the slice config and data.
- Missing R retains the existing command C fallback. R without F is ignored. Completeness checks run on selected R; invalid R does not silently certify valid C. Cached graph/draft fallback gets its own identity and a separate unavailable-target notice. Complete command data do not need an independently loaded host graph on the public12 prerequisite.
- Existing `PreviewDelivery` retains config/vector/revision/generation together through timer/RAF delivery. Same-object metadata changes cannot convert delivered local B into accepted A/C. Use the existing generation and scope key; no new counter/store is needed.
- Passing same-render `save.data` to the parent hook is appropriate. Its no-fact committed resolver remains distinct from the preview hook's popup-draft choice. Selected-command errors reach the existing export guard, preventing cached G from silently exporting as the requested command.
- Atomic creation, rebuild, invalidation and durable exclusion are **producer obligations still unverified**. Existing 5117 `useTimelineCommandSession.ts:82/104/140` builds only C/F; `useTimelineCommit.ts:349-351` clears only F. The new producer must rebuild C/R from one verified closure, patch both, install once after the existing generation/disposal fence, and clear both even through spread/rebuild paths. No R/F may enter history, authored snapshots, outbox payloads or wire data.

Donor `8246c6c3` keeps the original 12 mounted controls and adds six cases: accepted R, local/recovery delivery, deferred A→B, local B with ACK/head metadata and observed C, missing R, invalidation/rebuild. Five new cases correctly fail on unchanged current source; missing R passes. Their stub captures **only config**. They do not observe vectors, renderer output, browser metadata, parent render or panel stills. “Recovery” is an injected accepted snapshot, not restart/outbox reconstruction; “late ACK” supplies a still-local pair to the store, not actual acknowledgement handling. Invalidation supplies `dataFor(C)` with both fields already absent, so it cannot expose a producer retaining stale R. Equal-signature controls are useful, but cannot replace producer tests.

Before treating the shared branch as qualified, extend the neighboring tests for: stray R/no F; invalid preferred R with valid C and cached/no-cache paths; R/vector/revision deferral/coalescing and vector-only updates; producer ordinary-edit invalidation; real timing-changing local/accepted/recovery projections; disposal/stale async completion; both endpoint-distinct trim examples and dropped children; parent and panel evaluated output. Keep these staged intentional RED tests out of integration. Do not replace original passing expectations with refusals or skips. CompactPreviewCore remains separately unqualified; do not claim all preview hosts from this patch.

## MAIN producer semantics and prerequisite status

Independently read frozen Agent MAIN `a411628f8fd6129f9c58c332019b56769d997384`, `astrid/core/timeline/shot_composition_projection.py:312-326`: it caps the child end and writes the visible source duration back to hold/to. The source-vector report traces ordinary managed materialization/serialization retaining hold4 and predicts opacity0.5 at105. Actual MAIN capture report remains BLOCKED/unrun. These contradict treating INBOX10:35's suggested raw5/opacity1 as established MAIN behavior. No decision was overridden and no golden was chosen here.

Patch prerequisite: `5117b9da2e17828ec0b3cfbcdf3ff4987dc77ab3`. Donor: `8246c6c323c9f2007af7bc85eacdcc80e4fb6bc6`, based on `667498cc4`. Reviewed/current worktree and integration: `7bb885b638838588a0dff81b64b7c34960ac07f3`. Current 7bb is the older 0.0.8 product/dependency lane and lacks public12 playerEvaluation/vector delivery and refreshed producer work. The patch is not an integration-ready change on 7bb. Exact hashes and frozen line matches are in the flat `-source-review.json` artifact. UNAPPLIED patch SHA256: `9a1ca3a5b1c40141447f90c80672cf0686cf7d84eea6872984feab3cb47edf73`.

## Executed tests

All commands ran from `/home/user/work/wt/vw-m3-renderconfig-contingent-review`. Private config/cache and the donor test copy live only in the assigned worker overlay. The copy changes import paths only; no assertion/body changes. Production imports use unchanged current 7bb. These runs are current-lane unit/delivery evidence, **not public12, proposed-patch, dependency-environment or pixel qualification**. Existing shared packages were read, never repaired or modified.

```sh
node /home/user/work/app/node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-renderconfig-contingent-review/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/lib/canonicalRenderBounds.test.ts
```

**Exit0: 2 files, 16 passed (12 original mounted + 4 bounds), 2.98s.** Flat log: `handoff-vw-m3-renderconfig-contingent-review-original-controls.log`.

```sh
node /home/user/work/app/node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-renderconfig-contingent-review/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-renderconfig-contingent-review/donor.lifecycle.test.tsx
```

**Exit1: 1 file, 13 passed / 5 expected raw-selection failures, 2.44s.** Ordinary assertions remain RED; no expected-failure marker was added. Flat log: `handoff-vw-m3-renderconfig-contingent-review-donor-current.log`.

Initial private-runner setup attempts failed on runner-mode `__dirname` handling, missing admissions/pinned-Astrid aliases, alias ordering, and external Player mock resolution for the relocated test. The latter produced an invalid 14-fail/4-pass attempt with real Player code mounted in jsdom; it is not product evidence. Corrected only the private runner/dependency leaf links, preserving test assertions. Final logs above supersede those setup attempts. No browser or media render job ran.

`git diff --check`: exit0. `git status --porcelain=v1 --untracked-files=all` and `git diff --stat`: empty. Product/type/dependency/test changes in worktree: **0 paths, +0/-0**. No full suite, central request, whole-project typecheck, install/network, listener, browser, actual frame/audio capture, Runtime acceptance or git mutation was run. Frozen public12 behavior and the unapplied producer/consumer pair were not executed. The unavailable former `/tmp/app-coherent-deps12` graph was not recreated or substituted as public12 qualification.

## One handoff, after the golden

After Agent supplies the explicit 5/4/fade golden and Viewing confirms actual MAIN, ask App through the orchestrator for exactly **`tl/app-m3-renderconfig-atomic-pair`**, based on its owner-approved refreshed public12 source, containing type/producer/invalidation/recovery plus the corrected consumers and tests together. This is a concrete requested branch name, not an existing agreement or branch created here. App returns its exact SHA and changed paths; Viewing qualifies mounted lifecycle/vector, parent and panel behavior on that same SHA before any merge. Do not merge producer and consumer halves independently. No permission question or new approval process was invented.

Review is DONE; activation remains held on the existing golden/shared-unit gates and these findings. No BLOCKED marker is needed for this completed read-only review. Harness commit-msg and DONE are in the assigned worker directory. All retained review evidence uses this flat absolute design prefix; temporary overlay cache/setup copies are removed.
