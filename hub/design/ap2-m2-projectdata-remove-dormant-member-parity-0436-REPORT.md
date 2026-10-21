# App project-data remove parity report

Date: 2026-10-21 UTC

## Decision

**BLOCKED by the current App recording carrier.** I did not widen
`projectDataMember.ts` unsafely. The requested `mode: "remove"` command has no
value, prunes an empty namespace and `config.app`, and must restore the removed
namespace at its original object position after serialized inverse/reload.
The current App public record type and recorder cannot express that last
requirement.

## Main deletion input path

Main already exposes the deletion input as the public `TimelinePatch` family
`project-data.delete` at `src/sdk/video/timeline/patch.ts:29-30`. Its existing
payload validation is at `src/tools/video-editor/lib/timeline-patch.ts:584-617`.
The compiler applies it at `:1861-1887`: it deletes the requested leaf,
prunes an empty extension namespace, and the final config rebuild omits an
empty `config.app` at `:1936-1965`. No UI deletion request was invented or
changed.

## Exact source reviewed

The requested Agent source is:

- Agent commit `5672d2b7deee2bfe2ab375fd6db5fc35a192591d`
- full source tree `6dd13b552c4f07fff5586b1fa772bdbdf64accba`
- `astrid/core/timeline/schema/edit-command.schema.json` SHA-256
  `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`

That source defines the closed `project-data.write` remove shape as
`{target, key, mode: "remove"}` with no `value`. The later Agent ordered-
inverse correction is commit `b4493c75947f8605e61852f340e56b27e24c4adb`, tree
`24c0900be7d469d1250ca9883b7714c72308ed81`, schema SHA-256
`0357ef34fbac2416be59dc906fa5a9d9173e322ff1d1e53b758f5c890d543906`.
It adds `insertion_order` to the recorded write and threads that through the
state setter and inverse; this is the complete behavior required by the task.

## Concrete App prerequisite

The current App carrier is insufficient:

- `src/integrations/runtime/timeline-commit-types.ts:15` defines
  `AgentWrite` as only `ref`, `path`, `before`, and `after`; it has no
  `insertion_order` field.
- `src/tools/video-editor/commands/clipMovePrimitives.ts:204-215` restores a
  present property by appending it with `Object.defineProperty`; it has no
  ordered setter.
- `src/tools/video-editor/commands/clipMovePrimitives.ts:295-309` records
  writes and exposes `clear` without an insertion-order carrier.

For example, removing the only key from
`config.app[target]` when `target` is between `before` and `after` prunes the
namespace. Replaying the inverse through the current setter restores
`target` after `after`, losing the raw order. A cast or an extra untyped field
would make the capture appear complete while leaving inverse/reload semantics
wrong.

The smallest safe prerequisite is a coordinated carrier update (generated
`AgentWrite` type plus `MoveRecording.assign/clear`, `AuthoredState.set`, and
the inverse application path) equivalent to Agent `b4493c7`; then this private
member can capture the Agent remove record using that carrier. That prerequisite
is outside the assigned “member/capture and focused test only” scope, so no
partial remove implementation was landed.

## Live callers and evidence

There are **zero live production callers** of this private member. The only
references are the member’s own exports and its focused visual/project-data
tests (`rg` over `src`/`tests`). No producer, `useTimelineOps`, session, host,
pin, public entrypoint, DTO, store, or writer routing was changed.

Existing focused baseline, run with the shared dependency treated as read-only:

```text
realpath node_modules
=> /home/user/work/app/node_modules

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/projectDataMember.test.ts
=> 1 file passed; 9 tests passed
```

No full, browser, HTTP/socket, matrix, install, generated-schema, or live
producer/pin test was run. The worktree has no source changes; `git diff
--check` passes.

