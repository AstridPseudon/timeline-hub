# AP2 M2 ordinary qualified writer deletion v2

Date: 2026-10-20

## Result

No App-owned physical writer/helper deletion is safe from this qualification.
The ordinary native family is live and qualified, but the shared
`useTimelineOps` snapshot fallback is still required by the remaining live
ordinary families. I did not edit `useTimelineOps`, `useTimelineCommandSession`,
`commitSession`, or their shared state wiring.

The previously dead query writer (`src/tools/video-editor/hooks/useTimeline.ts`)
is already physically deleted in the current tree (D01-app-unused-query-writer,
integrated before this worker). It was not recreated or touched.

## Current source audit

- `src/tools/video-editor/hooks/useTimelineOps.ts:270-275` sends every
  `supported` or `mixed` patch to `genericPatchPort`; a qualified ordinary
  family therefore cannot return to the snapshot path.
- `src/tools/video-editor/commands/genericPatchCapture.ts:523-545` performs
  whole-patch preflight before owner resolution. A mixed batch fails as one
  `GenericPatchRefusal`, with no partial command list, owner reads, or authored
  write. The draft remains in the existing command-session state.
- `src/tools/video-editor/commands/genericPatchCapture.ts:487-515,559-623`
  still imports and executes `ordinaryMoveMember`, `ordinaryTrimMember`,
  `ordinaryScalarMember`, and `ordinaryStructuralMember`; these are replacement
  command helpers, not dead legacy helpers.
- `src/tools/video-editor/commands/commitSession.ts:888-943` owns the generic
  capture/finish/submit port and its single outbox enqueue. The port is exposed
  by `useTimelineCommandSession.ts:262-270,434-445` and mounted by
  `useTimelineState.ts:827-831,956`.
- `useTimelineOps.ts:277-321` still handles fully unsupported operations by
  validation/compile and `commitData`. That fallback is the remaining shared
  snapshot writer. Removing it now would delete live project-data, transcript,
  seam, proposal, and compiler-canary consumers; it would also turn those
  existing behaviors into refusals without their native replacements.

Therefore there is no own dead writer to delete and no assertion conversion to
make in this worker. No `DELETED` ledger row is manufactured.

## Shared-owner cut proposal (exact, not applied)

After project-data, transcript, seam, proposals, and compiler-canary either
have native captures or are explicitly deleted, the shared owner can apply this
small cut. It removes only the fallback from `useTimelineOps`; the existing
generic port remains the single batch door, and an unavailable session visibly
refuses before any local mutation. The corresponding `useTimelineState` call
must stop passing the removed `commitData` and `trackLabelPort` arguments. The
test edits are one-to-one expectation conversions and require independent
review; they are deliberately not included here.

```diff
diff --git a/src/tools/video-editor/hooks/useTimelineOps.ts b/src/tools/video-editor/hooks/useTimelineOps.ts
--- a/src/tools/video-editor/hooks/useTimelineOps.ts
+++ b/src/tools/video-editor/hooks/useTimelineOps.ts
@@
 import {
   validateTimelinePatch,
-  compileTimelinePatch,
   previewTimelinePatch,
 } from '@/tools/video-editor/lib/timeline-patch';
@@
 import {
-  classifyGenericPatch,
   type GenericPatchCapturePort,
 } from '../commands/genericPatchCapture.ts';
-import type { CommitDataOptions } from '@/tools/video-editor/hooks/useTimelineCommit';
@@
-import {
-  captureTrackLabelEdit,
-  submitTrackLabelEdit,
-  type TrackLabelCapturePort,
-} from '../commands/trackLabelGesture.ts';
@@
 export interface UseTimelineOpsArgs {
-  /** Stable commitData from useTimelineCommit / useTimelineSave. */
-  commitData: (nextData: TimelineData, options?: CommitDataOptions) => void;
-
   /** Mutable ref holding the current canonical TimelineData. */
@@
-  /** Original authored track-label capture and the shared command outbox. */
-  trackLabelPort?: TrackLabelCapturePort;
-
   /** One atomic native batch port; unsupported operation families refuse as one patch. */
   genericPatchPort?: GenericPatchCapturePort;
@@
 export function useTimelineOps({
-  commitData,
   dataRef,
@@
-  trackLabelPort,
   genericPatchPort,
@@
-      // Retain the guarded snapshot/draft route for standalone operations
-      // until their command migration lands. Mixed patches must reach the
-      // native port so its whole-batch refusal remains atomic.
-      if (genericPatchPort && classifyGenericPatch(patch) !== 'unsupported') {
+      if (genericPatchPort) {
         const captured = genericPatchPort.capture({ patch, current });
         const finished = genericPatchPort.finish(captured);
         genericPatchPort.submit(finished);
         return previewTimelinePatch(finished.preview, current).diff;
       }
 
-      // 1. Validate the full batch
-      const validation = validateTimelinePatch(patch);
-      if (!validation.valid) {
-        const messages = validation.diagnostics
-          .filter((d) => d.severity === 'error')
-          .map((d) => d.message)
-          .join('; ');
-        throw new Error(
-          `TimelineOps.apply: patch validation failed. ${messages}`,
-        );
-      }
-
-      // 2. Compile against current canonical data
-      const compiled = compileTimelinePatch(patch, current);
-      if (!compiled.valid || !compiled.nextData) {
-        const messages = compiled.diagnostics
-          .filter((d) => d.severity === 'error')
-          .map((d) => d.message)
-          .join('; ');
-        throw new Error(
-          `TimelineOps.apply: patch compilation failed. ${messages}`,
-        );
-      }
-
-      const labelUpdates = patch.operations.filter((operation) =>
-        operation.op === 'track.update' && operation.payload && 'label' in operation.payload);
-      if (labelUpdates.length > 0) {
-        const operation = labelUpdates[0];
-        const payload = operation.payload!;
-        if (patch.operations.length !== 1 || (payload.mode !== undefined && payload.mode !== 'merge')
-          || Object.keys(payload).some((key) => key !== 'label' && key !== 'mode')
-          || typeof payload.label !== 'string') {
-          throw new Error('TimelineOps.apply: only a single merge-mode label-only track.update is supported.');
-        }
-        const captured = captureTrackLabelEdit(trackLabelPort, current, operation.target);
-        submitTrackLabelEdit(captured, { values: { label: payload.label }, clear: [] });
-        return compiled.diff;
-      }
-
-      // 3. Unmigrated operations still use the existing snapshot path.
-      //    History recording is enabled by default (skipHistory defaults to false).
-      commitData(compiled.nextData, {
-        save: true,
-        semantic: true,
-      });
-
-      // 4. Return the semantic diff
-      return compiled.diff;
+      throw new Error('TimelineOps.apply: native command session is unavailable; draft preserved.');
     },
-    [assertTimelineEditable, commitData, dataRef, genericPatchPort, getCanonicalVersion, trackLabelPort],
+    [assertTimelineEditable, dataRef, genericPatchPort, getCanonicalVersion],
   );
```

This patch is intentionally held. It is not valid while the five live native
families above still use the snapshot producer. In particular, the current
mixed-batch refusal is already correct and must remain before owner resolution;
the future cut must not replace it with sequential native submissions or a
qualified-family snapshot fallback.

## Evidence

Authoritative qualification already recorded in
`ap2-m2-ordinary-qualified-graph-runner-repair-REPORT.md`:

- ordinary26437: PASS, one ordinary test, hosted build and Chromium smoke,
  approved pre-A closure oracle, complete SDK 8130 records, disjoint S1/V1,
  lost-ACK/restart/exact-retry/rebase, both undos, opaque/order/manifest and
  zero-legacy assertions. No repeat was requested.

Local targeted checks on this unchanged source tree:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/ordinaryMoveMember.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/commands/ordinaryStructuralMember.test.ts \
  src/tools/video-editor/commands/ordinaryTrimMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts
# 8 files, 108 tests passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/ordinaryRealBatch.test.ts \
  src/tools/video-editor/dev/localExtensions.catalog.test.ts \
  src/test/threeProductsAuthoring.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
# 4 files, 53 tests passed

git diff --check
# passed; worktree source unchanged
```

Not run: browser/socket/localhost/request-test/full suite, as prohibited by the
brief. No dependency, pin, schema, generated-client, or test assertion changes
were made.

## Blocker and next step

The exact blocker is the live unsupported family set named above, not the
ordinary native family. The App manager should land the native replacements or
explicit deletion decisions for those consumers, then independently review and
apply the shared cut above. Only after that cut and its one-to-one test review
should D01-app-ordinary-batch be considered for physical deletion evidence.
