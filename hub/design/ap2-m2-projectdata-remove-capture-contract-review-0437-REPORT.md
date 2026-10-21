# App project-data remove capture contract review

Date: 2026-10-21 UTC

## Decision

**HOLD / concrete prerequisite.** There is no new worker SHA/tree to approve:
worker 0436 landed no source changes and its branch remains at App commit
`cd5080bdca2a4baae81b2546de739f4b44326a59` (tree
`f6b21d70ce85529121cdf8f2092368c8b521eda3`). The dormant helper must remain
replace/merge-only until the existing App recording carrier can preserve
object insertion order through inverse and reload.

This is a carrier mismatch, not permission to add a cast or to activate a
writer. The smallest prerequisite is coordinated support for Agent's
`insertion_order` write field in the already-generated `AgentWrite` type,
`MoveRecording.assign/clear`, `AuthoredState.set`, and the existing inverse
application path. That is the shape of Agent correction `b4493c75`; it is
outside worker 0436's member/capture-only scope.

## Main deletion input and live callers

Main already has the deletion input at:

- `src/sdk/video/timeline/patch.ts:29-30`: the public `project-data.delete`
  operation family.
- `src/tools/video-editor/lib/timeline-patch.ts:583-617`: its validation.
- `src/tools/video-editor/lib/timeline-patch.ts:1861-1887`: leaf deletion and
  empty extension-namespace pruning.
- `src/tools/video-editor/lib/timeline-patch.ts:1936-1965`: empty `config.app`
  omission during rebuild.

No new UI deletion operation was invented. The private native source form was
not widened, and the existing Main writer routing is unchanged.

`rg` over `src` and `tests` found zero live production callers of
`captureProjectDataMember`, `executeProjectDataMember`, or their aliases. The
only references are the helper itself and its focused visual/project-data
tests. No producer, `useTimelineOps`, command session, host, pin, public
entrypoint, DTO, store, or writer route changed.

## Agent parity evidence

The complete Agent source reviewed was:

- `5672d2b7deee2bfe2ab375fd6db5fc35a192591d`, tree
  `6dd13b552c4f07fff5586b1fa772bdbdf64accba`.
- Its generated edit-command schema SHA-256 is
  `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
- `ProjectDataWriteArgs` is closed: replace requires `value`; remove requires
  `target`, `key`, and `mode: "remove"`, and explicitly forbids `value`.

The complete ordered-removal correction reviewed was:

- `b4493c75947f8605e61852f340e56b27e24c4adb`, tree
  `24c0900be7d469d1250ca9883b7714c72308ed81`.
- Its schema SHA-256 is
  `0357ef34fbac2416be59dc906fa5a9d9173e322ff1d1e53b758f5c890d543906`.

Agent's remove command reads the target namespace to distinguish an absent
namespace from a present `null`/empty namespace and refuses malformed
non-object namespaces. It writes only the requested leaf for a non-empty
namespace, then prunes an empty namespace and finally an empty `config.app`.
For namespace removal it records the original sibling order as
`insertion_order`; the guarded inverse uses that order to restore the
namespace at its original position after serialization/reload. The Agent
tests retain the sibling-key behavior, empty-container pruning,
absence-versus-null behavior, opaque values, disjoint-key rebase, same-key
ABA/intervening-write refusal, dependent-write refusal, malformed/foreign and
empty-owner guards, and exact inverse/redo order.

Current App `projectDataMember.ts` still accepts only `project-data.write`
with a value and `mode: "replace"` at lines 23-38, 111-144, 238-248, and
316-329. Its `MoveRecording.clear` at
`src/tools/video-editor/commands/clipMovePrimitives.ts:295-309` has no order
carrier; `AuthoredState.set` at `:204-215` restores a present property by
appending it. Thus a target between two namespace siblings is restored in a
different order after pruning and inverse/reload. Adding an untyped field or
cast would conceal this semantic loss.

The current published Runtime bundle at
`/home/user/work/runtime/runtime_protocol/schemas/timeline-commit-bundle.json`
also exposes no `project-data.write` operation constant and no remove-mode
schema. Therefore no pin, activation, or live caller may be changed as part
of this review.

## Checks

Run directly on this clean worktree with shared dependencies treated as
read-only:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/projectDataMember.test.ts
  1 file passed; 9 tests passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts
  2 files passed; 22 tests passed

git diff --check
  passed
```

No full, browser, HTTP/socket, generated-schema, pin, activation, or
unchanged-suite replay was run. The worktree has no source changes.

## Next step

First land and qualify the coordinated existing-carrier `insertion_order`
prerequisite. Then re-review a new dormant helper candidate against the exact
Agent source above, including the existing Main `project-data.delete` input,
all merge/replace and mixed-batch refusal assertions, and the complete
ordered inverse/reload contract. Keep the current published pin and all live
writer routing unchanged until that paired evidence exists.
