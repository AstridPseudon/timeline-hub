# AP2-M2 parent swap shared adapter packet

## Result

Prepared the conditional flat proposal:

ap2-m2-parent-swap-shared-adapter-packet.patch

Exact base: 455a719b4, branch
tl/ap2-m2-parent-current-row-local-consumers.

The patch is intentionally limited to the missing App shared adapter:

- commitSession.ts: extends the existing preparation-only swap carrier with
  capture, finish, and submit; the preparation methods remain unchanged.
- useTimelineCommandSession.ts: applies the existing legacy-clean fence to
  all three new methods while retaining the preparation fence.
- useTimelineState.types.ts: exposes the full port; useTimelineState.ts
  already mounts the carrier on this base and is not changed.
- Direct session/hook assertions that the new methods are present and refuse
  while a legacy save is dirty.

The adapter captures the detached bundle, target raw clip ID, exact
five-field MediaSelection, local generation, local outbox basis, and display
head before the sole verification await. finish rechecks generation, display
head, and the captured authored bundle before calling the reviewed pure swap
helper. submit checks the exact clip.swap-media command, captured-before
bundle, preview, and generation before enqueueing. No append conversion, late
catalog lookup, raw afterClipId replacement, fallback writer,
Provider/dataProvider edit, useTimelineOps edit, DTO, schema, endpoint, client
API, or new operation is included.

## Settled blocker / exact prerequisite

The current cohort does not yet support the operation this adapter must
submit. Current Agent/Runtime expose occurrence.swap-media; the parent
operation clip.swap-media with intent.ownership = parent is the separate
in-flight peer. Current Runtime schema evidence rejects parent ownership, and
the current Agent source has no parent-scope swap registration.

Therefore this packet does not claim native acceptance. Before applying the
flat App patch, land and qualify the paired Agent/Runtime parent
clip.swap-media member plus the reviewed App pure helper/executor from
tl/ap2-m2-parent-existing-swap-media-member (239 donor tests). Until then,
the row-local preparation carrier and visible refusal remain correct.

## Verification

Passed on the unchanged worker base:

    node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
    -> 4 files / 62 tests passed

    git diff --check
    -> passed; worker worktree clean

The previously recorded current-row neighbor lane is 6 files / 164 tests
passed. A repeat of that longer lane emitted only the Vitest startup banner
within the local command window and is not counted as evidence.

Not run: full suite, browser/e2e, localhost/live sockets, dependency or pin
changes, Runtime/Agent qualification, or reload/retry/undo native acceptance.
The flat proposal was not applied to this worktree or integration.
The proposal text was not syntax-qualified with git apply; it is a
conditional handoff for App source integration after the peer prerequisite,
not a landed product patch.

## Recommended next step

After the paired Agent/Runtime parent operation is integrated, apply this
small App shared patch, then run the donor pure swap tests plus the focused
session/hook lanes and the required actual lost-ack/reload/retry/undo and
zero-legacy journey. Keep the original preparation/refusal assertions.
