# App MAIN574 derived-label failure reconciliation

Date: 2026-10-20 UTC  
Worker: `app-m3-main574-derived-label-failure-reconciliation`

## Frozen reference and scope

The supplied classification remains unchanged and is the authority for the
original failure count:

- frozen classification: `app-full8bd8-current-classification.md`
- frozen root: `8bd8f741f7c8b28b8682aa960a658417f70c8522`
- frozen App expected SHA: `ea38656fe62950440b36cafee780698cff2c3f9c`
- worker base HEAD: `d12d0909746c552dee6dac7b5d8459e8e1f27679`
- worker base tree: `c91e3c07f293658aa0f26dd180ac464c45b71559`
- final uncommitted diff SHA-256 (`git diff --binary`): `c7f3387d5bb8ae3231059d18aabf1b6d19843f1067d99efc3943cd9590ff2e32`

The frozen root/classification was not relabelled or modified. The worker
changed only the App timeline data, output projection, save-utils regression
oracles, and PreviewSurface lifecycle oracle paths.

## Causality decision

MAIN574 readable names are valid display projection behavior. `assembleTimelineData`
keeps authored `config` untouched and derives names into `resolvedConfig` and
row metadata. Therefore the eleven object/signature mismatches were stale
restored oracles, not a reason to remove labels.

One failure was a real product defect: row reconstruction copied derived
`meta.label` values back into authored config. This changed a stable authoring
signature during a move/undo when the authored label was absent. The fix uses
the existing raw `extras.clips` carrier in `rowsToConfig`; existing clips keep
their own label state (including absence and opaque values), while newly
materialized clips may use supplied metadata. No DTO, store, compiler, or new
contract field was added.

The existing output projection also now returns its exact input config when no
source track exists. This prevents an irrelevant clone from breaking the
PreviewSurface's exact delivered-config identity; source-track filtering is
unchanged.

## Manager ledger: old expectation -> reconciled expectation

All twelve old cases remain. No case was skipped, deleted, marked expected to
fail, or weakened. Timing, head, draft, race, and metadata-only certification
assertions remain in place.

### `timeline-save-utils.test.ts` (4)

1. `data.resolvedConfig.toBe(resolvedConfig)` -> strict equality with the
   exact post-assembly projection containing `video.mp4` and `audio.mp3`.
   The authored `data.config.toBe(config)` assertion remains unchanged.
2. `data.signature === getConfigSignature(data.resolvedConfig)` -> the exact
   unprojected resolved input signature, plus an explicit inequality against
   the display-labelled projection. This records that derived labels are not
   identity bytes.
3. The legacy pinned-group repair uses an exact manually specified resolved
   input oracle with repaired geometry and no derived labels, while retaining
   all group-order and geometry assertions.
4. The inverse-transaction stable-signature assertion is unchanged. It now
   passes because raw authored labels are retained through row reconstruction;
   the old absent-label input no longer acquires `asset-1.mp4`.

### `useVideoEditorPreviewSurface.lifecycle.test.tsx` (8)

1. Candidate/closure delivery now names `localEdit.resolvedConfig`, the exact
   already-assembled input, retains the exact deferred `deliveredEdit` during
   acknowledgement, and expects `acceptedClosure.resolvedConfig` after the
   acknowledged delivery. The asset-entry and registry identity assertions
   remain.
2. Retained B now uses the exact `afterA.resolvedConfig` and `afterC.resolvedConfig`
   inputs while preserving the original base-R labels and observed-C sequence.
3. Same-content acceptance now compares the exact `initial.resolvedConfig` and
   `next.resolvedConfig` references across the 149ms/1ms timing boundary.
4. Metadata-only certification uses accepted A/C facts over the exact initial
   assembled config reference. This preserves the old unsaved label until the
   actual target projection changes, then retains the C-unavailable notice and
   clear-only-target behavior.
5. Complete paired config keeps the exact delivered reference while an
   independent canonical read fails and recovers.
6. Paused coalescing expects the exact newest `localB.resolvedConfig` and still
   rejects delivery of A.
7. Playing coalescing retains the exact initial reference before the frame and
   exact `localB.resolvedConfig` after the frame; superseded A remains absent.
8. Scope remount expects the exact `acceptedPending.resolvedConfig` and keeps
   the committed-A label and zero-timer assertion.

## Changes made

- `src/tools/video-editor/lib/timeline-data.ts`: preserve raw authored clip
  labels at the row-to-config funnel using the existing raw config carrier.
- `src/tools/video-editor/data/timelineOutputProjection.ts`: preserve exact
  config identity when no source-track projection is needed.
- `src/tools/video-editor/lib/timeline-save-utils.test.ts`: reconcile display
  projection versus identity-signature expectations without changing inputs or
  dropping assertions.
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx`:
  reconcile expected references to exact post-assembly inputs while preserving
  all twelve lifecycle behaviors.

Visible MAIN574 names remain covered by the existing `clipDisplayNames` and
`timeline-data` tests. Raw authored labels remain carried by `config`; derived
labels remain visible through `resolvedConfig`/row metadata.

## Evidence

Exact failing-file repro before edits:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/timeline-save-utils.test.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
```

Result: 2 files, 39 tests, 12 failures (the classified baseline).

Exact failing-file rerun after edits, with the private TMPDIR and existing
`snapshot-vitest-runner.cjs` preload: **2 files passed, 39 tests passed**.

App-owned label/timeline/signature/projection neighbors:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/clipDisplayNames.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/data/timelineOutputProjection.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx
```

Result: **6 files passed, 85 tests passed**.

The broader neighbor probe also included `config-utils.test.ts` and
`useVideoEditorPreviewComposition.initialRead.test.tsx`; it had 115 passing
tests and 31 failures before reaching product assertions because the shared
renderer dependency exports no `getSanitizedMediaTrimProps` function. No shared
dependency, install, or cache was changed. This is recorded as an environment
blocker, not product evidence.

Scoped lint:

```text
node_modules/.bin/eslint --no-cache \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/data/timelineOutputProjection.ts \
  src/tools/video-editor/lib/timeline-data.ts \
  src/tools/video-editor/lib/timeline-save-utils.test.ts
```

Result: exit 0. `git diff --check`: exit 0.

Not run: full suite, browser/e2e, localhost/live sockets, build, TypeScript
check, install, or shared dependency/cache writes.
