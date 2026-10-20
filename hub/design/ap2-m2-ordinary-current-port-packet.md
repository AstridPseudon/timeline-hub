# AP2 M2 ordinary CURRENT-root port packet

Date: 2026-10-20

## Base and artifacts

- Exact App base: `590c19795111fd1891bbd50a5f8d48bef3505a26` (`hub/timeline/app/tl/integration`).
- Approved helper prerequisite: `f76d61c5cfa222939a6cc77509e5f7c03019c611`.
- Approved standalone-dispatch source: `cd08aa8a8ebc3f0db94834be9bc1e4eedebb4317d6f399676d703196a995e972` (SHA-256 of the approved patch).
- Four-file shared-port proposal: `handoff-ap2-m2-ordinary-currentroot-port.patch`
  (SHA-256 `3668a64e17a96237a24ff6bb5984de42e04470e1c736e740b60bdafd36fb68cd`).
  It changes only:
  `commands/commitSession.ts`,
  `hooks/useTimelineCommandSession.ts`,
  `hooks/useTimelineOps.ts`, and
  `hooks/useTimelineState.ts`.
- Helper prerequisite plus row-local predicate/classifier test: `handoff-ap2-m2-ordinary-currentroot-helper.patch`
  (SHA-256 `0250886a3b33802e413b2bb2c9e3c0e0e541c98263d686c590ff9b376ac25336`).
  This is the approved `f76d` two-file helper source/test with the approved `classifyGenericPatch` delta and its test. The assigned worktree contains only these two helper files; shared session/hook/state/ops files were not changed there.

## Port contract

```ts
interface GenericPatchCapturePort {
  capture(input: {
    patch: TimelinePatch;
    current: TimelineData;
  }): GenericPatchBasis;

  finish(basis: GenericPatchBasis): {
    commands: EditCommand[];
    preview: TimelinePatch;
  };

  submit(input: {
    commands: EditCommand[];
    preview: TimelinePatch;
  }): void;
}
```

The session implementation captures the displayed scope/head and authored bundle, preserves the original dependent basis (`lastIntent ? { after: lastIntent } : { head: copy(known.head) }`), prepares once, and submits once through the existing outbox. It requires the same generation/bundle and exact combined preview at finish/submit. No direct Runtime POST/store/DTO/API path was added.

## Dispatch behavior

`classifyGenericPatch` classifies the complete patch before native capture or owner resolution:

- fully supported native label/hold batches use the generic port;
- mixed supported/unsupported batches enter the generic port and are refused atomically by its all-member preflight, before owner resolution, capture, preview, enqueue, or snapshot fallback;
- all-unsupported batches remain on the existing validate/compile/guarded `commitData` producer path.

There is no post-capture fallback, copied support predicate, duplicate writer, or `legacyClean()` bypass. The existing cold-read readiness gate and MAIN574 changes remain intact. The mounted compiler canary therefore stays on its existing standalone path until its native operation is paired.

## Private validation

The private candidate was an archived copy of exact base `590c19795`, with the helper prerequisite and the four-file proposal applied. The approved dispatch repair was applied unchanged; it applies cleanly to this current root.

Combined targeted command:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts
```

Result: **9 files, 278 tests passed**. The current `590c19795` root has three more tests than the earlier 275-test review count.

```text
node_modules/.bin/eslint \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/video-editor/commands/genericPatchCapture.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.ts \
  src/tools/video-editor/hooks/useTimelineOps.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineState.ts --max-warnings 0
=> exit 0

node_modules/.bin/tsc --noEmit --pretty false
=> exit 0

git diff --check
=> exit 0 on the assigned worktree
```

Apply checks:

```text
git apply --check handoff-ap2-m2-ordinary-currentroot-port.patch
=> PASS against the assigned 590c19795 root

fresh archive of 590c19795:
  helper patch apply --check + apply
  shared patch apply --check
=> PASS
```

The private session test preserved one listed owner/intent and exact retry body/key behavior. The native helper tests preserved ordered commands/ordinals, opaque fields, and mixed atomic refusal. No full suite, browser, localhost, live socket, Runtime Door, dependency/pin, generated contract, ledger, or Git-ref operation was run.

## Handoff decision

This packet is ready for the single App owner worker to apply in order: helper patch, then the four-file shared-port patch. The private integration tests are validation evidence only; shared session/hook/state/ops files remain untouched in this worker's worktree as required.

