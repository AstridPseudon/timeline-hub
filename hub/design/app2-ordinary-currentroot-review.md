# AP2 M2 ordinary current-root review

Date: 2026-10-20

## Verdicts

- **Source delta (`05b6b488d..f76d61c5c`, two files): APPROVE.** The repaired
  helper is current-root source, has no retired `clipScalarCapture` import or
  cohort/pin dependency, and stays bounded to merge-mode track labels and
  positive clip holds. This approves the helper source as a producer unit; it
  does not claim ordinary-writer retirement.
- **Exact shared patch
  (`handoff-ap2-m2-ordinary-currentroot-port-shared.patch`): REQUEST CHANGES.**
  It applies cleanly as a two-file addition to the empty `05b6` base and
  reverse-checks against this candidate, but it does not wire the helper into
  the actual current-root preview/session/enqueue path. The separate proposed
  session integration patch fails against this current API and must not be
  applied wholesale.

## Source review

The delta is exactly:

```text
src/tools/video-editor/commands/genericPatchCapture.ts       465 lines
src/tools/video-editor/commands/genericPatchCapture.test.ts  112 lines
```

The implementation is concrete rather than pseudo-code. It uses the existing
`MoveRecording`/`AuthoredState` recorder and `trackLabelCapture` machinery. The
preflight at `genericPatchCapture.ts:375-393` rejects the entire patch before
calling the owner resolver when any operation is unsupported. The ordered loop
at `:395-431` preserves public `order` with input-index tie breaking, executes
members sequentially against one copied authored bundle, retains guards/reads/
bindings, emits sequential ordinals, and returns one command list. The clip
path at `:284-339` validates and verifies the captured `clip.set` claims and
keeps opaque fields because it writes only `hold`. Projection at `:447-465` is
immutable and keeps unrelated `dataLanes`/display data.

The supported boundary is honest: `track.update` label plus optional merge
mode, and `clip.update` with one finite positive `hold`. It refuses scalar
clears, `project-data.write`, extension operations, and other operation
families. No writer deletion or all-ordinary coverage claim is present.

## Agent parity

The existing TypeScript-produced payload `/tmp/ap2-ordinary-native-ts-produced.json`
was submitted to the read-only Agent ordinary archive with
`/home/user/work/venv-app2-native/bin/python`. Both commands passed
`validate_command`; authoritative Agent execution reported:

- operations: `clip.set`, `track.set`
- ordinals: `[0, 1]`
- writes: `parent/clip:x::hold`, `parent/track:V1::label`
- values: hold `1.23456789`, label `""`
- original text/app opaque fields preserved
- submitted claims matched the authoritative command records

A valid `track.set` followed by unsupported `project-data.write` raised Agent
`CommandError` and left the input bundle unchanged.

## Shared-patch findings

`git apply --check` for
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-currentroot-port-shared.patch`
returned 0 in an empty exact-base directory; reverse check against this
candidate also returned 0. That patch only adds the helper and its tests.

The current root still has no generic port wiring:

- `useTimelineOps.ts:283-307` retains the single-label special case and sends
  all other valid patches through `commitData(compiled.nextData, ...)`.
- `commitSession.ts` exports only the existing move/label ports; no generic
  port is returned.
- `useTimelineCommandSession.ts` exposes only `port` and `trackLabelPort`.
- `clipScalarCapture.ts` is absent, as required by the repaired source.

The separate four-file integration proposal
`handoff-ap2-m2-ordinary-native-batch-shared.patch` failed
`git apply --check` against this current root at `commitSession.ts`,
`useTimelineCommandSession.ts`, and `useTimelineState.ts`. Therefore there is
no verified actual preview/enqueue execution, one outbox intent, or persisted
original request body/key for this delta yet. Those are the exact changes
needed before approving the shared integration patch; preserve the current
whole-patch preflight and leave snapshot writers in place for unsupported
families.

## Tests and limits

Passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/commands/commitSession.test.ts
=> 6 files, 182 tests passed

node_modules/.bin/eslint \
  src/tools/video-editor/commands/genericPatchCapture.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts --max-warnings 0
=> passed
```

No full, browser, localhost, socket, Runtime HTTP, outbox integration, writer
retirement, dependency, shared-file, or repository mutation was performed.
