# App ordinary project-data consumer boundary

## Result

Prepared the source-only activation boundary. The worktree has one focused
schema-capability test added to the existing pinned Runtime operation guard:

`src/integrations/runtime/pinnedRuntimeEditCommandContract.test.ts`

No App production/shared seam, Runtime lock, generated client, public pin,
activation path, or current HOME edit was changed.

The test constructs the already-reviewed closed `project-data.write` v1
command shape and asks `assertPinnedRuntimeEditCommandOps` whether the pinned
schema advertises that operation. It expects refusal when the capability is
absent (the current public013/Main0146ba state) and acceptance when the exact
consumer-pinned successor advertises it. It does not infer capability from a
version string, package version, or schema digest.

## Exact current seam

The single classification seam is:

```text
useTimelineOps.ts:270
  classifyGenericPatch(patch)
        -> genericPatchCapture.ts:129 supported(operation)
        -> genericPatchCapture.ts:154 classifyGenericPatch(patch)
```

Current behavior is intentionally correct for the unpinned state:

- `project-data.write` is not in `supported()` on this branch.
- An all-unsupported standalone project-data patch remains on the existing
  guarded snapshot/draft path.
- A mixed batch reaches the generic port as `mixed`; its preflight refuses the
  complete batch before owner resolution, capture, enqueue, or fallback.
- The inert `captureProjectDataMember` remains uncalled by the live generic
  port, so no project-data write is activated by this worktree.

The existing helper is the only eventual builder. It already validates the
closed target/key/value shape, supports declared `merge` and `replace` patch
modes by lowering them to guarded command `mode: "replace"`, and preserves
the original namespace/leaf claims. `project-data.delete`, remove/unset modes,
and any new unpinned semantics remain excluded.

## Exact small shared patch proposal (not applied)

HOME owns the current shared session/useTimelineOps files, so this is a
proposal for the later exact-successor adoption, not a patch applied here.
It should be carried on top of the already-qualified private392 membership
delta, not reimplemented from a whole-document writer.

1. In `genericPatchCapture.ts`, import the existing
   `captureProjectDataMember`, `executeProjectDataMember`,
   `projectDataOperationReason`, and `projectDataValue` helpers.
2. Add one explicit capability argument to the existing generic classifier
   and capture path, defaulting to false:

   ```ts
   export type GenericPatchCapabilities = Readonly<{
     projectDataWrite: boolean;
   }>;

   const NO_PROJECT_DATA_CAPABILITY: GenericPatchCapabilities = Object.freeze({
     projectDataWrite: false,
   });

   function supported(
     operation: TimelinePatchOperation,
     capabilities: GenericPatchCapabilities,
   ): boolean {
     // retain the current generic guards above this point
     if (operation.op === 'project-data.write') {
       return capabilities.projectDataWrite
         && projectDataOperationReason(operation) === undefined;
     }
     // retain every current ordinary branch unchanged
   }

   export function classifyGenericPatch(
     patch: TimelinePatch,
     capabilities = NO_PROJECT_DATA_CAPABILITY,
   ): GenericPatchSupport {
     const supportedCount = patch.operations.filter((operation) =>
       supported(operation, capabilities)).length;
     // retain the existing supported/mixed/unsupported calculation unchanged
   }

   export function captureGenericPatch(
     bundle: AuthoredBundle,
     patch: TimelinePatch,
     resolve: (operation: TimelinePatchOperation) => string,
     capabilities = NO_PROJECT_DATA_CAPABILITY,
   ) {
     // use the same capability-aware preflight and dispatch the already
     // reviewed captureProjectDataMember for project-data.write members
   }
   ```

   The capture branch must assign project-data members to the existing parent
   owner, execute them sequentially against the copied `after` bundle, and
   project with `projectDataValue`. It must not diff the whole config, submit
   members separately, or recapture a new safety basis.
3. Extend the existing `GenericPatchCapturePort` with that capability and pass
   the same value to both `classifyGenericPatch` and `captureGenericPatch`.
   The command-session default remains false. Only the exact successor-pinned
   consumer composition may set `projectDataWrite: true`, after its generated
   consumer/schema bytes and matched Agent/Runtime tuple are adopted.
4. Keep the existing `useTimelineOps` branch ordering. With the capability
   false, standalone project-data remains legacy/unsupported. With it true,
   a valid project-data batch is native; any unsupported member makes the
   complete batch `mixed` and therefore refuses atomically before any write.

This is the only generic classification change proposed. No `mode: remove`,
`project-data.delete`, public013 pin change, generated-client edit, Runtime
endpoint/DTO, or activation/current shared edit belongs in this cut.

## Focused test evidence

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/pinnedRuntimeEditCommandContract.test.ts
PASS — 1 file, 7 tests

node_modules/.bin/eslint \
  src/integrations/runtime/pinnedRuntimeEditCommandContract.test.ts \
  --ext ts --max-warnings 0
PASS

git diff --check
PASS
```

The current run takes the refusal branch because the pinned public013 schema
does not advertise `project-data.write`. The test is deliberately driven by
the existing schema operation walker; no version/digest/string capability
guess is used. The exact successor success branch remains unrun here because
that successor is not consumer-pinned in this worktree, and no pin or shared
activation was authorized.

Previously qualified evidence intentionally reused, not repeated here:

- private392 App HTTP6846 and native/Door10824;
- the inert `captureProjectDataMember` merge/replace/guard tests;
- the e010 source39/replace Agent guard reports; and
- the existing generic mixed-batch atomic refusal/draft-preservation tests.

No browser, full suite, localhost, live socket, dependency copy, Runtime
mutation, public pin, or activation run was performed.

## Live callers

The current source search found:

| Surface | Current callers / status |
| --- | --- |
| `useTimelineOps` generic classification | Live: `src/tools/video-editor/hooks/useTimelineState.ts:827-831` supplies the session port; `src/tools/video-editor/hooks/useTimelineOps.ts:270-274` classifies/captures/submits; `src/tools/video-editor/hooks/useTimelineCommandSession.ts:262-270` applies the clean-save fence. |
| `captureGenericPatch` | Live: `src/tools/video-editor/commands/commitSession.ts:954-986`; helper call at `ordinaryScalarMember.ts:397` is an internal ordinary producer. |
| `captureProjectDataMember` | No non-test live caller found. It is intentionally inert on this branch. |
| compiler-canary project-data producer | `src/tools/video-editor/lib/compiler-canary.ts:421-441` builds a source + source-map batch and calls `timeline.apply`; no external production instantiation of `createCompilerCanary` was found outside its own extension factory/tests. |
| source-map project-data producer | `src/tools/video-editor/lib/source-map-runtime.ts:151-174` exposes write/delete helpers; no live production instantiation was found. Its delete path remains excluded. |
| examples/dev extensions | Multiple `project-data.write` strings are examples or dev fixtures, not evidence of a mounted production consumer; they remain outside this cut. |

## Decisions / blockers / next step

No decision was made beyond the settled plan. The current public013/Main0146ba
capability remains disabled. The next step is HOME's review and later
integration of the capability-gated shared hunk only after the exact approved
successor is consumer-pinned and its matched qualification is authorized.

There is no implementation blocker for this source-only preparation; the
success branch is intentionally blocked by the settled pin/adoption boundary,
not by a test failure.
