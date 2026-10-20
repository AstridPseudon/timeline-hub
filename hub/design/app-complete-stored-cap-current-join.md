# Complete stored-cap producer/consumer current join

Implementation complete; **HOLD integration for App manager and Viewing final consumer review**, the separately owned MAIN574 label reconciliation, and current App2 TypeScript diagnostics. This is a source/unit handoff, not a full-suite or physical-parity qualification.

## Exact source

- Assigned worktree: `/home/user/work/wt/app-m3-complete-stored-cap-producer-consumer-current-join`.
- Base commit: `48576cfa2783331f2c7c8309ff4069162a3afd11`; tree `126983e329d1ab85a59d7a62ebb96676f8aab622`.
- Waited for `managers/app/notes/root-wave2-for-cap-READY`: commit `0d5009e18bee8e29f894dabf5db501a0fcea750f`; tree `b323667662d565526d7c2395733f26e2c6380378`.
- Complete frozen producer: `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` → `3a4350f9d9a578f817568d5fe348c5d750595129`; source tree `24b051ff0f580f0d6b84950ba03a9fb8d11afe47`.
- Exact corrected consumer delta: `3a4350f9d9a578f817568d5fe348c5d750595129` → `8488f9c1c2e3eafd924720e5bcd49a950798ffed`; source tree `711dcdb39bdb2131ffe3ae38c0bdeab6f70a4ad3`.
- Final candidate tree: **`32dc0de053ffb98d718077a111994181ae03ea15`**. Commit SHA is pending the harness; no commit/index/ref mutation was performed.
- 44 changed files relative to the assigned base: READY changes composed first, then the complete 30-file cap unit. Exactly the union of the 22 producer and 11 consumer files differs from READY (three shared paths).
- READY-relative patch: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/ready-candidate.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/ready-candidate.patch), SHA256 `3f75295d6c1d5ef16bbbd63b7dd25f53a16d4f574f61871b9f4af29b9f1f9388`. It applies to an owned READY file archive and reproduces all 30 files byte-for-byte. [Full source/blob manifest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/source-identity.json), [base-relative patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/base-candidate.patch), [patch verification](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/patch-proof.txt).

The earlier `a3144673d10a64bd2d71c4d8567c97b536444fdd` consumer-only candidate was not used as the complete unit. The full frozen delta applied cleanly by hunks after the base→READY patch; no older whole shared file replaced current App2 hooks.

## Actual paths and behavior

- `data/shotCompositionProjection.ts:327,436,530` computes the one `canonicalTiming.storedOccurrenceDurationMs` from the original prepared graph occurrence, before using the effective duration for editor geometry. Existing editor/read next-cut rules remain unchanged.
- `hooks/useTimelineCommandSession.ts:82,98,113,136,156,234` projects verified bootstrap/accepted closures, retains their raw composition in the existing recovery context, and preserves it through local preview and original-outbox recovery. Both READY `elementPort` and `genericPatchPort`, their capture/finish/submit barriers, and generic preview dispatch remain intact. The only cap delta in this shared hook is the three raw-composition arguments to `remember`.
- `hooks/useTimelineSave.draftConfig.ts:15,23` retains the existing raw composition alongside the already retained authored roots; `hooks/useTimelinePersistence.ts:657,973` snapshots one authored config for both the durable draft and save attempt. Missing/ambiguous raw context refuses visibly with editor data retained.
- `lib/serialize.ts:33,52,84,115` resolves raw counterparts through the graph identity map. It strips the newly derived scalar at explicitly projected exits, restores raw same-name `canonical`/`canonicalTiming` collisions, and preserves nulls, opaque fields, own `__proto__`, ordering and untouched parent metadata. No wire/DTO/store/compiler field was introduced.
- Popup `shotTimelineDataProvider.ts:363,395,423,464,626` keeps/rebuilds the raw basis for recovered, current, generation-captured and accepted publication paths. Popup draft projection and publication receive that existing basis explicitly. Existing pending recovery/request bytes retain their owner and retry meaning.
- `canonicalCompositionState.ts` selects the private initial-graph render copy. `useVideoEditorPreviewComposition.ts:56–87` selects the exact config/fact pair and compiles its transition vector. `RemotionPreview` defers config/vector/revision/extent as a unit. `TimelineFramePreview` receives the selected vector, bounded extent, paired config and fact; `useRenderState`/`useClientRender` pass the selected config/vector and recomputed metadata into client rendering.
- The existing `canonicalRenderBounds` helper uses the corrected stored-source clipping branch for both initial-graph and command delivery. Negative/non-finite stored values fall back per clip; the effective scalar and editor/source clip remain untouched.

Two bounded additions beyond composing the frozen sources: (1) the existing initial-graph render helper now delegates to the corrected stored clipping branch and rejects negative/non-finite scalars, with an assertion added to the existing fallback case; (2) the existing paused/playing cap delivery regression now loads digest-verified Runtime raw graphs and uses `buildTimelineData`, rather than constructing an already-prepared graph. No new fixture or test matrix was added. Revision IDs are asserted and excluded only from the comparison of otherwise identical flattened inputs.

The verified raw fixture keeps hold=5. Both 4000/4500 graph projections reach the editor as hold=5; delivered render copies become 4/4.5 with extents 120/135. At 4000, frame 105 opacity is 0.5, frames 105 and 119 are active, and frame 120 is empty. At 4500, opacity at 105 is 1 and frame 120 remains active. Existing projection/bounds tests retain their editor next-cut, trim/speed and source-unit assertions, including from=2/to=8. No read/editor expectations were replaced with render-cap expectations.

## All producer files (22)

```text
src/tools/travel-between-images/components/ShotTimelinePreview.test.ts
src/tools/travel-between-images/components/ShotTimelinePreview.tsx
src/tools/travel-between-images/components/shotTimelineDataProvider.ts
src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx
src/tools/video-editor/data/DataProvider.ts
src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts
src/tools/video-editor/data/canonicalCompositionState.ts
src/tools/video-editor/data/mainImageCap.fixture.json
src/tools/video-editor/data/shotCompositionProjection.ts
src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
src/tools/video-editor/hooks/useTimelineCommandSession.ts
src/tools/video-editor/hooks/useTimelinePersistence.test.tsx
src/tools/video-editor/hooks/useTimelinePersistence.ts
src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts
src/tools/video-editor/hooks/useTimelineSave.draftConfig.ts
src/tools/video-editor/lib/canonicalRenderBounds.ts
src/tools/video-editor/lib/serialize.test.ts
src/tools/video-editor/lib/serialize.ts
```

## All corrected consumer files (11)

```text
src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx
src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx
src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx
src/tools/video-editor/hooks/useClientRender.ts
src/tools/video-editor/hooks/useRenderState.ts
src/tools/video-editor/hooks/useTimelineState.ts
src/tools/video-editor/lib/canonicalRenderBounds.test.ts
src/tools/video-editor/lib/canonicalRenderBounds.ts
```

## Private public13 graph

`node_modules` in this worktree points to the worker-owned `private13/node_modules`. Public Composition was extracted only into that owned directory after checking its real path. All **77 regular archive members** match the approved `0.0.13` archive before and after tests/typecheck: SHA256 **`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`**. React/ReactDOM are 18.3.1; Remotion/media/player/layout-utils are 4.0.509; TypeScript is 5.9.3. Other dependencies are read-only symlinks. No install or shared package/cache write was performed.

Package, lock, Runtime lock and public13 archive bytes remain identical to READY. [Resolved dependency paths](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dependency-paths.txt), [public13 proof](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/public13-proof.txt), [postflight pins](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/pin-postflight.txt). Runner uses owned cacheDir, `--configLoader=runner --no-cache`, and aliases each official public13 export to its exact archive entry. The first invocation used an insufficient directory alias and failed module resolution (23 failed files/43 passing tests); this was a runner error, not a source result. Its log is retained separately.

## Commands and results

The broad direct Vitest lane contains 26 existing producer, consumer, recovery, serialization, MAIN label, App2 capture/session/ops and PCM files. Exact command:

```text
env -u ASTRID_CHECKOUT node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/canonicalRenderBounds.test.ts src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts src/tools/video-editor/data/canonicalCompositionState.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/travel-between-images/components/ShotTimelinePreview.test.ts src/tools/video-editor/lib/clipDisplayNames.test.ts src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx src/tools/video-editor/compositions/continuousPCM.contract.test.tsx
```
Result: **24 files passed, 2 failed; 575 tests passed, 10 failed**. Eight failures are the existing MAIN574 lifecycle expectations comparing pre-assembly configs to display-labelled resolved inputs. Their original positive assertions remain unchanged. Two were in the strengthened stored-cap test because its strict flattened comparison also included the intentionally different verified graph revision IDs.

The two affected cap files were rerun after asserting the revision identity separately and normalizing that provenance-only field in the flattened comparison:

```text
env -u ASTRID_CHECKOUT node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx src/tools/video-editor/lib/canonicalRenderBounds.test.ts
```
Result: **2 files, 13/13 passed**, including both actual graph→data→Player cases and all existing bound/fallback cases. The remaining eight lifecycle failures are not claimed green. The separately owned label reconciliation `8a79a7bb9416302f36b6a8c104444ff609dff5e0` is under independent review HOLD (missing raw-clips type plus two self-oracles), so it was deliberately not imported or “fixed” by weakening these expectations. See `design/app-main574-derived-label-reconciliation.md` and the independent review report.

A producer-omission negative control transforms only the projector's scalar-emission line in the private Vitest runner; repository source is unchanged:

```text
env -u ASTRID_CHECKOUT node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/producer-negative.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx
```
Result: **expected exit 1, both paused/playing tests failed with “expected 5 to be 4”** at the Player delivery assertion. This directly demonstrates the green regression depends on the actual producer, rather than stamped consumer metadata. [Negative runner config](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/producer-negative.config.mjs).

Scoped lint command:

```text
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 src/tools/travel-between-images/components/ShotTimelinePreview.test.ts src/tools/travel-between-images/components/ShotTimelinePreview.tsx src/tools/travel-between-images/components/shotTimelineDataProvider.ts src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx src/tools/video-editor/data/DataProvider.ts src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts src/tools/video-editor/data/canonicalCompositionState.ts src/tools/video-editor/data/shotCompositionProjection.ts src/tools/video-editor/hooks/useClientRender.ts src/tools/video-editor/hooks/useRenderState.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.ts src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts src/tools/video-editor/hooks/useTimelineSave.draftConfig.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/lib/canonicalRenderBounds.test.ts src/tools/video-editor/lib/canonicalRenderBounds.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/serialize.ts
```
Result: **exit 0** on all 29 cap TypeScript files. The three subsequently edited helper/test files were checked again with the same ESLint executable, `--no-cache --max-warnings 0`; exit 0. `git diff --check`: **exit 0**.

The one actual project typecheck, after complete cap source/private13 graph composition:

```text
flock -x /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json
```
Result: **exit 2, ten diagnostics**. Every named source file is byte-identical to READY; none names a cap-changed file. No scoped TypeScript run or public12 graph was substituted, and no second project typecheck was run. Exact complete diagnostics:

```text
src/tools/video-editor/commands/elementCapture.ts(236,26): error TS2345: Argument of type 'string | null' is not assignable to parameter of type 'string'.
  Type 'null' is not assignable to type 'string'.
src/tools/video-editor/commands/elementGesture.ts(89,40): error TS2345: Argument of type 'ElementCaptureArgs | undefined' is not assignable to parameter of type 'ElementCaptureArgs'.
  Type 'undefined' is not assignable to type 'ElementCaptureArgs'.
src/tools/video-editor/commands/elementGesture.ts(93,26): error TS18048: 'edit.elementRef' is possibly 'undefined'.
src/tools/video-editor/commands/elementGesture.ts(112,42): error TS2345: Argument of type 'ElementCaptureArgs | undefined' is not assignable to parameter of type 'ElementCaptureArgs'.
  Type 'undefined' is not assignable to type 'ElementCaptureArgs'.
src/tools/video-editor/commands/genericPatchCapture.ts(315,22): error TS2345: Argument of type 'JSON' is not assignable to parameter of type 'number'.
  Type 'null' is not assignable to type 'number'.
src/tools/video-editor/commands/occurrenceDuplicateCapture.ts(83,3): error TS2322: Type '(ref: string, path: string[]) => AgentStateVariant1 | AgentStateVariant2 | { state: "present"; value: { members: { state: string; value: {} | null; } | { ...; }; payload?: undefined; internal_timeline?: undefined; }; } | { ...; }' is not assignable to type '(ref: string, path: string[]) => AgentState'.
  Type 'AgentStateVariant1 | AgentStateVariant2 | { state: "present"; value: { members: { state: string; value: {} | null; } | { state: string; value?: undefined; }; payload?: undefined; internal_timeline?: undefined; }; } | { ...; }' is not assignable to type 'AgentState'.
    Type '{ state: "present"; value: { members: { state: string; value: {} | null; } | { state: string; value?: undefined; }; payload?: undefined; internal_timeline?: undefined; }; }' is not assignable to type 'AgentState'.
      Type '{ state: "present"; value: { members: { state: string; value: {} | null; } | { state: string; value?: undefined; }; payload?: undefined; internal_timeline?: undefined; }; }' is not assignable to type 'AgentStateVariant2'.
        Types of property 'value' are incompatible.
          Type '{ members: { state: string; value: {} | null; } | { state: string; value?: undefined; }; payload?: undefined; internal_timeline?: undefined; }' is not assignable to type 'JSON'.
            Type '{ members: { state: string; value: {} | null; } | { state: string; value?: undefined; }; payload?: undefined; internal_timeline?: undefined; }' is not assignable to type '{ [key: string]: JSON; }'.
              Property 'members' is incompatible with index signature.
                Type '{ state: string; value: {} | null; } | { state: string; value?: undefined; }' is not assignable to type 'JSON'.
                  Type '{ state: string; value?: undefined; }' is not assignable to type 'JSON'.
                    Type '{ state: string; value?: undefined; }' is not assignable to type '{ [key: string]: JSON; }'.
                      Property 'value' is incompatible with index signature.
                        Type 'undefined' is not assignable to type 'JSON'.
src/tools/video-editor/commands/occurrenceDuplicateCapture.ts(195,7): error TS2345: Argument of type 'JSON' is not assignable to parameter of type 'string'.
  Type 'null' is not assignable to type 'string'.
src/tools/video-editor/commands/occurrenceDuplicateCapture.ts(199,52): error TS2345: Argument of type 'JSON' is not assignable to parameter of type 'string'.
  Type 'null' is not assignable to type 'string'.
src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx(49,92): error TS2345: Argument of type '{ readonly params: { readonly values: Record<string, JSON>; readonly clear: readonly []; }; }' is not assignable to parameter of type 'ElementEdit'.
  Type '{ readonly params: { readonly values: Record<string, JSON>; readonly clear: readonly []; }; }' is not assignable to type '{ elementRef?: undefined; params: ElementParamsArgs; }'.
    The types of 'params.clear' are incompatible between these types.
      The type 'readonly []' is 'readonly' and cannot be assigned to the mutable type 'string[]'.
src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx(50,39): error TS2345: Argument of type '{ readonly params: { readonly values: Record<string, JSON>; readonly clear: readonly []; }; }' is not assignable to parameter of type 'ElementEdit'.
  Type '{ readonly params: { readonly values: Record<string, JSON>; readonly clear: readonly []; }; }' is not assignable to type '{ elementRef?: undefined; params: ElementParamsArgs; }'.
    The types of 'params.clear' are incompatible between these types.
      The type 'readonly []' is 'readonly' and cannot be assigned to the mutable type 'string[]'.
```
No NodeNext package-declaration diagnostic appeared in this actual project run. The known separate declaration issue is not counted as an App source failure or used to excuse these ten concrete App2 diagnostics.

Logs: [broad lane](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/targeted.log), [cap retest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/cap-retest.log), [producer negative](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/producer-negative.log), [typecheck](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/tsc.log).

## Limits and next steps

- App manager and Viewing must review this exact tree and complete producer+consumer patch before merge. In particular, review the retained raw context, immutable editor geometry, and config/fact/vector/extent pairing across Player/still/clientRender.
- The implementation is complete; current-root qualification is held by the eight known MAIN574 label lifecycle failures and ten unchanged App2 TypeScript diagnostics. Incorporate their separately reviewed repairs before claiming a clean integrated source gate. Do not import the held label candidate as-is.
- An initial source-only concern about `elementRef` being absent from a mutable-field list was withdrawn after tracing the actual merge-mode metadata path. No App2 preview regression is asserted from that incomplete inspection, and no independent App2 port redesign was made here.
- Targeted commit-session tests include exact bodyText/idempotency-key retry after restart. This run used the in-process unit fixture; it does not claim a live Runtime restart or browser journey.
- Not run: full suite, browser/e2e, localhost/live sockets, install, build, physical frame/audio capture or parity, owner-film viewing, macOS. The raw fixture test/evaluator checks source behavior; no pixel or audio parity claim is made.
- MAIN574 tabs/touch and cold-readiness source, readable labels, PCM13/progress source and native ports are preserved via the exact READY join. PCM lifetime/contract controls passed in the broad lane. No integration worktree, branch/ref, other worker tree, shared dependency or shared cache was mutated.

`commit-msg`, `DONE` and `KEEP` are provided in the worker directory. The harness supplies the eventual commit SHA; the candidate tree and exact patches above identify the reviewed source without inventing a commit.
