# AP2 M2 ordinary supported-batch fallback cut

## Result

No App-owned row-private legacy writer is separable from the current source.
Supported ordinary patch/proposal batches already use the existing atomic
`genericPatchPort`; proposal acceptance is only
`ProposalPanel → ProposalRuntime.accept → TimelineOps.apply`, so it has no
second snapshot writer to remove. I therefore made no product-code edit and
returned the exact minimum HOME-owned cut as an unapplied patch:

[`ordinary-supported-batch-fallback-cut.patch`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-supported-batch-fallback-cut-targeted-1220/ordinary-supported-batch-fallback-cut.patch)

The patch removes only the shared `useTimelineOps` snapshot branch and its
`useTimelineState` argument plumbing. It changes the no-session behavior to a
visible refusal that preserves the draft. It does not touch the current
`GenericPatchCapture`, proposal runtime, transcript association, project-data,
compiler-canary, generated contracts, or public operations.

## Current live-call evidence

- `useTimelineOps.apply` sends every `supported` or `mixed` patch to
  `genericPatchPort`; `GenericPatchCapture` preflights the complete batch,
  resolves owners only after that check, executes sequentially against one
  authored bundle, and submits one command array.
- `ProposalRuntime.accept` delegates only to `timelineOps.apply`; the native
  proposal positive and mixed refusal are covered at the live adapter boundary.
- `commitSession.ts` owns capture/finish/submit and one outbox enqueue;
  `useTimelineCommandSession.ts` adds the existing clean-save gate;
  `useTimelineState.ts` mounts the port.
- `project-transcript-host.ts`, `data-kinds/dataKindItems.ts`, and
  `compiler-canary.ts` still depend on the central snapshot path. They remain
  live per the settled task boundary. No transcript pin/hash, project-data
  DTO, latest fallback, or new operation was invented.

## Verification

Shared dependency resolution was read-only and confirmed:

```text
realpath node_modules
/home/user/work/app/node_modules
```

Targeted existing App lane, with the required serialized Vitest settings:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/ordinaryMoveMember.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/commands/ordinaryStructuralMember.test.ts \
  src/tools/video-editor/commands/ordinaryTrimMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/ordinaryRealBatch.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/lib/proposal-runtime.test.ts
# 12 files, 253 passed
```

```text
node_modules/.bin/eslint --max-warnings 0 \
  src/tools/video-editor/commands/genericPatchCapture.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/ordinaryMoveMember.ts \
  src/tools/video-editor/commands/ordinaryMoveMember.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/commands/ordinaryStructuralMember.ts \
  src/tools/video-editor/commands/ordinaryStructuralMember.test.ts \
  src/tools/video-editor/commands/ordinaryTrimMember.ts \
  src/tools/video-editor/commands/ordinaryTrimMember.test.ts \
  src/tools/video-editor/commands/ordinaryRealBatch.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/lib/proposal-runtime.ts \
  src/tools/video-editor/lib/proposal-runtime.test.ts
# passed
```

```text
flock /home/user/work/.app-tsc.lock node_modules/.bin/tsc --noEmit --pretty false
# passed

git diff --check
# passed; worktree clean
```

No browser, localhost/socket, full suite, frozen-producer run, install, or
central test request was made. The unapplied cut intentionally has no local
green claim: applying it before the remaining snapshot consumers have native
coverage would be a behavior deletion and would violate the plan.

## Decision / handoff

The exact current blocker is shared ownership and remaining live consumers,
not native ordinary coverage. HOME should apply the attached two-file delta
only after transcript, project-data, seam, and compiler-canary dependencies
are either command-backed or explicitly removed, then update the original
snapshot-path assertions one-to-one to expect the visible refusal. Keep all
original value/presence/opaque/order, atomicity, inverse/undo, retry, and draft
assertions.
