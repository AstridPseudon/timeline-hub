# Compiler canary private dead-ingress deletion candidate

Status: CANDIDATE, pending independent reviewer approval. This report does not
claim DELETED or approved test retirement.

## Decision

The compiler-canary snapshot producer is a private, unused debug/example
module, not a public kept extension API and not a live producer. The candidate
deletes only:

- `src/tools/video-editor/lib/compiler-canary.ts`
- `src/tools/video-editor/lib/compiler-canary.test.ts`
- its now-stale entry in `eslint.strict-debt.js`

The source-map implementation and public contracts are intentionally retained:

- `src/tools/video-editor/lib/source-map-runtime.ts`
- `src/tools/video-editor/lib/source-map-runtime.test.ts`
- `src/sdk/video/timeline/sourceMap.ts`
- `src/tools/video-editor/lib/source-code-navigation.ts`
- `src/tools/video-editor/lib/source-code-navigation.test.ts`

This is the smallest cut. It removes the snapshot producer and its own
helpers, without removing shared source-map helpers, project-data native
controls, proposal runtime, feature/version guards, or any fallback
replacement.

## Plan and baseline

The governing PLAN keeps the extensible producer model and the public
source-map/extension contracts, while cutting old duplicate paths and
fallback writers. It does not require an unexported, deferred compiler-canary
example to remain. The current App2 status and the full392 boundary report
identified this module as a source/source-map `project-data.write` producer
with no external production instantiation; the current native project-data
controls remain separate and are not removed here.

The repository documentation describes DSL/compiler-canary behavior as
deferred (D-131), while the SDK public barrel and public API manifest do not
export the compiler-canary module. The `@publicContract` comments in the
module describe intended contract shape, but are not a public export or host
registration.

## Exact static and dynamic consumer proof

### Compiler canary

On the pre-change tree, the only references to the compiler-canary module were
the module's own 59-test file and the factory's internal call from
`createCompilerCanaryExtension` to `createCompilerCanary`.

The following were checked:

- No non-test source import or re-export of `compiler-canary.ts`.
- No `createCompilerCanary` or `createCompilerCanaryExtension` import outside
  the deleted test file.
- No dynamic `import()` or `require()` containing `compiler-canary`.
- No extension registry, loader, pack, manifest, or host assembly entry for
  the compiler-canary module.
- No export from `src/sdk/index.ts`.
- No entry in `config/governance/sdk-public-api-manifest.json`.
- No public extension example or installed extension pack points at the
  module.

The remaining `com.example.compiler-canary` strings are test fixtures for the
independent project-data command controls. They do not import or instantiate
the deleted producer.

The module's former exports were:

`CanaryDslClip`, `CanaryDsl`, `CompilerCanaryResult`,
`CompilerCanaryOptions`, `CompilerCanary`, `createCompilerCanary`, and
`createCompilerCanaryExtension`.

These were deep module exports only. None was present in the public SDK barrel
or public API manifest, so the candidate changes no public SDK export.

### Source-map runtime

`createSourceMapRuntime` has no current non-test production instantiation, but
it must not be cut as part of this candidate. The public `SourceMapRuntime`
interface is exported from `src/sdk/index.ts`; source-code navigation accepts
that public runtime and is covered by its own tests. The implementation and
tests also preserve source-map project-data write/delete, lookup, stale, and
granularity behavior. This is a shared source-map surface, not a private
compiler-canary helper.

## Candidate diff

The candidate removes 2,171 source/test lines plus one stale config entry:

- 601 lines of private compiler-canary producer code and helpers.
- 1,570 lines of tests that instantiate only that private producer.
- One stale strict-debt allowlist entry.

No replacement API, DTO, adapter, fallback, command, schema, or version guard
was added or changed.

## Test retirement ledger

Each retired test below belonged only to the deleted private canary. Because
there is no live or public caller, each is explicitly marked
`BEHAVIORGONE: private canary`. No live/public assertion is being removed.
The active project-data and source-map controls that cover the retained
surfaces are listed after this ledger; they are not misrepresented as
one-for-one replacements for private canary semantics.

| Old test | Disposition |
| --- | --- |
| returns null for invalid JSON | BEHAVIORGONE: private canary |
| returns null for non-object JSON | BEHAVIORGONE: private canary |
| returns null for DSL with wrong version | BEHAVIORGONE: private canary |
| returns null for DSL without clips array | BEHAVIORGONE: private canary |
| returns null for DSL with non-array clips | BEHAVIORGONE: private canary |
| reads snapshot via reader.snapshot() during processDsl | BEHAVIORGONE: private canary |
| uses snapshot baseVersion in data patch | BEHAVIORGONE: private canary |
| reflects project ID from snapshot | BEHAVIORGONE: private canary |
| stores DSL source as project-data.write | BEHAVIORGONE: private canary |
| stores source-map entries as project-data.write | BEHAVIORGONE: private canary |
| source-map entries link to DSL source lines | BEHAVIORGONE: private canary |
| returns source-map entry IDs in result | BEHAVIORGONE: private canary |
| emits a TimelineProposal via proposals.create() | BEHAVIORGONE: private canary |
| proposal carries the correct source | BEHAVIORGONE: private canary |
| proposal includes rationale describing changes | BEHAVIORGONE: private canary |
| proposal uses current snapshot baseVersion | BEHAVIORGONE: private canary |
| proposal is marked as previewable | BEHAVIORGONE: private canary |
| replaceForSource: re-issuing replaces previous pending proposal | BEHAVIORGONE: private canary |
| proposal patch contains clip.add operations with correct structure | BEHAVIORGONE: private canary |
| stamps GeneratedObjectMeta on each clip.add operation | BEHAVIORGONE: private canary |
| includes sourceMapEntryId in GeneratedObjectMeta when source-map exists | BEHAVIORGONE: private canary |
| includes extension namespace in clip app data | BEHAVIORGONE: private canary |
| generated clips have unique IDs | BEHAVIORGONE: private canary |
| generated clips carry version information via DSL version | BEHAVIORGONE: private canary |
| proposes clip.add only for new clips not in snapshot | BEHAVIORGONE: private canary |
| proposes clip.remove only for owned clips no longer in DSL | BEHAVIORGONE: private canary |
| does NOT propose remove for clips owned by other extensions | BEHAVIORGONE: private canary |
| does NOT propose remove for user-authored clips (not managed) | BEHAVIORGONE: private canary |
| proposes clip.update for owned clips that differ from DSL | BEHAVIORGONE: private canary |
| does NOT propose update for owned clips that match DSL exactly | BEHAVIORGONE: private canary |
| does NOT propose update for clips owned by other extensions | BEHAVIORGONE: private canary |
| removes all clips owned by the extension | BEHAVIORGONE: private canary |
| does not remove clips owned by other extensions during cleanup | BEHAVIORGONE: private canary |
| returns empty result when there are no owned objects | BEHAVIORGONE: private canary |
| cleanup proposal includes rationale | BEHAVIORGONE: private canary |
| canary does not import from video-editor internals | BEHAVIORGONE: private canary |
| canary uses only public SDK types for its API | BEHAVIORGONE: private canary |
| canary does not mutate snapshot clips array | BEHAVIORGONE: private canary |
| handles empty DSL (no clips) | BEHAVIORGONE: private canary |
| handles DSL with many clips (stress test) | BEHAVIORGONE: private canary |
| handles concurrent operations: add + remove + update | BEHAVIORGONE: private canary |
| custom sourceUri is propagated to source-map entries | BEHAVIORGONE: private canary |
| uses default sourceUri when not specified | BEHAVIORGONE: private canary |
| canary source file imports only from @astrid/editor-sdk (no internal modules) | BEHAVIORGONE: private canary |
| canary source does not reference TimelineData or DataProvider | BEHAVIORGONE: private canary |
| canary source does not reference store, provider, or command internals | BEHAVIORGONE: private canary |
| canary source does not reference internal config/save/asset utilities | BEHAVIORGONE: private canary |
| canary only calls TimelineOps.apply, not validate/preview/checkpoint/rollback/setAllTracksMuted | BEHAVIORGONE: private canary |
| canary uses proposals.create but not proposals.preview/accept/reject | BEHAVIORGONE: private canary |
| canary operates entirely through CreativeContext.timeline, reader, and proposals | BEHAVIORGONE: private canary |
| canary creates patches using only public SDK operation families | BEHAVIORGONE: private canary |
| recompiling with identical DSL preserves ownership (no-op, no proposal) | BEHAVIORGONE: private canary |
| recompiling with modified DSL updates clip properties while preserving ownership | BEHAVIORGONE: private canary |
| recompiling preserves extension namespace in app data on clip.update | BEHAVIORGONE: private canary |
| recompiling does not affect non-owned clips | BEHAVIORGONE: private canary |
| recompiling updates generatedAt timestamp on modified clips | BEHAVIORGONE: private canary |
| recompiling preserves sourceMapEntryId linkage on updates | BEHAVIORGONE: private canary |
| three-pass recompile: add -> update -> no-op preserves ownership chain | BEHAVIORGONE: private canary |
| recompiling with removed clip proposes clip.remove only for owned clips | BEHAVIORGONE: private canary |

Retained active controls, tested separately, are:

- `src/tools/video-editor/commands/projectDataMember.test.ts` (7 tests):
  source and source-map writes as one ordered native command batch, exact
  values and opaque siblings, replace lowering, namespace birth, malformed
  namespace refusal, guards, and mixed-batch refusal.
- `src/tools/video-editor/lib/source-map-runtime.test.ts` (31 tests):
  public source-map runtime persistence, lookup, stale marking, deletion,
  extension isolation, granularity, and positions.
- `src/tools/video-editor/lib/source-code-navigation.test.ts` (33 tests):
  retained source-to-timeline and timeline-to-source navigation behavior.
- `src/tools/video-editor/commands/genericPatchCapture.test.ts`,
  `timeline-patch.test.ts`, `proposal-runtime.test.ts`, and
  `managed-object-guard.test.ts`: active native patch/proposal/ownership
  controls remain intact.

## Verification

Before the deletion candidate, the affected canary and retained source-map
neighbors passed:

```text
TMPDIR=<private temporary directory> ./node_modules/.bin/vitest run --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  src/tools/video-editor/lib/source-code-navigation.test.ts
=> 3 files, 123 tests passed
```

After the candidate deletion, retained neighbors passed:

```text
TMPDIR=<private temporary directory> ./node_modules/.bin/vitest run --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  src/tools/video-editor/lib/source-code-navigation.test.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts
=> 6 files, 439 tests passed
```

The config cleanup also passed:

```text
./node_modules/.bin/eslint eslint.strict-debt.js --max-warnings 0
node --check eslint.strict-debt.js
git diff --check
=> all passed
```

No full suite, browser, localhost, live socket, or central gate was run.

## Review gate and next step

An independent reviewer must verify the public/private classification, the
zero-caller proof, the retained source-map boundary, and this one-to-one test
ledger before any test retirement is allowed to land. Until that approval,
this worktree is a deletion candidate only and must not be reported as
DELETED.

