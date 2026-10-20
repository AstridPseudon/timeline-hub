# AP2 M2 ordinary seam persistence role

Date: 2026-10-20

Scope: current App worker tree `22788084f9b9a69322fca1c6aff35d17c5c2c189`; the relevant files are byte-identical between this tree and `tl/integration` for this review. No product, test, shared dependency, pin, or Git-ref changes were made.

## Decision

`visualSeamContract` is not project-catalog state and it is not film/pin membership. It is project-scoped timeline app metadata with two roles:

- Authored render-admission intent: `pictureTracks`, `continuityTracks`, `gaps`/declared pauses, and frame-scoped `intents` (`hard-cut` or `synchronized`). These change how the same authored film is admitted and remain meaningful after reload. They must remain persisted, with unrelated/opaque `config.app` data preserved.
- Derived render diagnostics: `visualSeamContract.report`. This is recomputed from the current projected clips/tracks and is not an authored choice. It should not be copied into canonical saved state.

This is consistent with the settled film-vs-catalog boundary: catalog operations may remain project-scoped outside accepted film state, but film selection/placement/pins remain edit commands. A seam acknowledgement is neither catalog CRUD nor a clip/pin mutation; it is scoped authored configuration for the timeline’s visual-admission policy.

## Exact current write and call chain

1. `src/tools/video-editor/hooks/useRenderState.ts:972-981` is the only live acknowledgement write trigger found. After an admission report is blocked, the user action builds `acknowledged` with `withVisualSeamIntent(renderConfig, boundary.frame, kind)`, rechecks `analyzeVisualSeams(..., {enforceIntent: true})`, and calls the injected callback. The UI wires these actions at `src/tools/video-editor/components/TimelineRenderControls.tsx:354-360`.
2. `src/tools/video-editor/hooks/useTimelineState.ts:659-685` implements that callback. It reads `acknowledgedConfig.app.visualSeamContract`, merges the whole object into `current.config.app`, rebuilds `TimelineData`, calls `commitTimelineData(nextData, {save: true, semantic: true})`, and flushes the snapshot save. This is a direct snapshot writer, not a command-session/outbox/native operation.
3. On canonical shot compositions, `src/tools/video-editor/data/shotCompositionProjection.ts:590-601` first computes `visualSeamReport = analyzeVisualSeams(configBase, {enforceIntent: true})`, then spreads the base contract and adds `version`, `mode`, and `report` to the resolved config. Therefore the current callback can serialize the fresh derived report along with the user’s authored intent.

## Exact readers and behavior proof

The authored portion has consumers beyond display:

- `src/tools/video-editor/data/visualSeamContract.ts:179-184` reads declared picture/continuity tracks.
- `src/tools/video-editor/data/visualSeamContract.ts:224-245` reads frame intents and validates their participant/context/canonical witnesses against the current projected clips. A changed boundary invalidates the stored intent; this is a guarded authored declaration, not a cached warning.
- `src/tools/video-editor/data/visualSeamContract.ts:481-482` reads declared gaps during seam analysis. `src/tools/video-editor/data/shotCompositionEditor.ts:482-515` reads and remaps those pauses after a shot edit, then writes the updated parent-composition config. This directly proves project-scoped authored state that follows film edits without changing clip/pin membership.
- `src/tools/video-editor/data/shotCompositionAdapter.ts:328-333` runs `assertVisualSeamAdmission` against the canonical projection before publication. The stored intent can therefore affect acceptance of a canonical composition.
- `src/tools/video-editor/data/portableVisualSeamIntent.ts:13-17,129-136` derives the portable witness from the current closure and is used by `visualSeamContract.ts:232-238` to reject stale/tampered intent.

The derived portion is not needed as saved input:

- `src/tools/video-editor/hooks/useRenderState.ts:537-538` stores the report in local React state and fingerprints the exact render config; `:920-927` reads the report returned by render admission; `:1371-1378` exposes it to the chrome/UI.
- `src/tools/video-editor/components/TimelineRenderControls.tsx:147-149,354-365` reads that local/admission report for warning/error presentation and acknowledgement controls.
- `src/tools/video-editor/data/shotCompositionProjection.ts:590-601` recomputes the report on each canonical projection. No production reader uses a persisted `contract.report` as authoritative input; the report is diagnostics derived from current content and the authored contract.

The existing tests also pin the distinction: `shotCompositionProjection.test.ts:121-151` expects a fresh report while separately preserving authored intents and opaque `customDisclosure`; `portableVisualSeamIntent.test.ts` covers context-bound intent and pause behavior.

## Concrete removal/migration result

Remove only the automatic persistence of `visualSeamContract.report` from the callback’s saved contract. The save-side normalization must preserve all other contract keys, including authored intent, track policy, gaps, and unknown/opaque keys. The report can continue to be attached to the in-memory canonical projection and surfaced through `useRenderState`; after reload it is recomputed from current content. This keeps renderer-independent saving: the canonical save stores authored data and does not need to run a renderer or persist a renderer-produced diagnostic snapshot.

Do not remove the whole callback yet. If the callback disappears before a native replacement, the acknowledgement buttons can still update a temporary render config but the intent disappears on reload, violating the existing positive behavior. The callback’s remaining authored write is the legacy path that must be migrated, not denied.

## Precise peer seam request

Agent + Runtime: qualify one scoped authored app-config command for the `visualSeamContract` authored fields only. It must:

- carry the exact authored contract value (including explicit clears) and an expected/current-value guard;
- preserve unrelated `config.app` keys and unknown contract members;
- record exact before/after data and support guarded inverse/rebase under the existing `/v1` commit path;
- validate only project/timeline scope, shape, and intent witnesses/guards required by the command contract; never require Composition, a renderer, or a render admission to save;
- leave `report` out of the command payload and out of accepted authored state.

Runtime 0.2.13 / Agent current native operation inventory has no such scoped app-config operation. Do not invent `app.update`, use a whole-document snapshot, or reuse a clip operation as a substitute. Once that peer seam is qualified, the App worker should replace `persistVisualSeamConfig`’s `commitData(..., save: true)` with the existing command-session/outbox submit and keep render admission/report handling unchanged.

Viewing owns the rendering/projection logic; no Viewing source was changed or requested beyond keeping report recomputation/read behavior intact.

## Verification

Targeted existing unit:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/data/visualSeamContract.test.ts
=> Test Files 1 passed; Tests 12 passed
```

An initial cache-safe runner-mode attempt was not usable because the repository config evaluates `__dirname` under the runner loader:

```text
node_modules/.bin/vitest run --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/data/visualSeamContract.test.ts
=> startup failure: ReferenceError: __dirname is not defined in config/testing/vitest.config.ts
```

No full, browser, localhost, socket, dependency, or shared-install test was run.
