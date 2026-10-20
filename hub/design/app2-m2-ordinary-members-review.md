# AP2 M2 ordinary members review

## Verdict

**REQUEST CHANGES for adoption onto current App integration.** The reviewed
compose commit is behaviorally approved on its stated base; current integration
has diverged and removed the ordinary-member units, so it needs a fresh
forward-port and qualification before adoption. The Runtime/actual Door remains
separate and was not reviewed here.

## Branch delta and overlap

- Review HEAD: `6966c7df6cd06c9c623867ca47946cfa5afa6247`
  (`feat(app): compose ordinary move and scalar members`).
- Stated base: `tl/ap2-m2-ordinary-members-compose`, equal to review HEAD;
  branch delta from its parent `4a48638b2` is exactly six paths:
  `genericPatchCapture.ts`, its test, and the ordinary move/scalar source and
  tests. The commit is `+833/-21` lines.
- Current App integration: `0d5009e18bee8e29f894dabf5db501a0fcea750f`.
  It diverges from this candidate at `48576cfa2783331f2c7c8309ff4069162a3afd11`.
  Against current integration, the generic helper and test differ and all four
  ordinary-member files are deleted; `commitSession.ts` and the command-session
  hooks also differ. Direct adoption is therefore not qualified.
- Approved source reuse: `ordinaryMoveMember.ts` and
  `ordinaryScalarMember.ts` are byte-identical to their reviewed source
  branches `tl/ap2-m2-ordinary-move-member` and
  `tl/ap2-m2-ordinary-scalar-member`.

## Behavior reviewed

The compose integration uses the existing generic helper and existing
`MoveRecording`/Agent command implementations. It pre-classifies the complete
patch before owner resolution, routes malformed qualified move/scalar shapes to
native refusal, refuses mixed supported/unsupported batches atomically, keeps
unsupported-only standalone patches on the existing snapshot path, preserves
public ordering, sequential records/ordinals, combined projection, and one
outbox command list with exact retry identity/body.

## Evidence

Passed on review HEAD:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/ordinaryMoveMember.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts
# 11 files, 289 passed

node_modules/.bin/tsc --noEmit --pretty false
# passed

node_modules/.bin/eslint \
  src/tools/video-editor/commands/genericPatchCapture.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/ordinaryMoveMember.ts \
  src/tools/video-editor/commands/ordinaryMoveMember.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/video-editor/hooks/useTimelineOps.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.ts --max-warnings 0
# passed

git diff --check HEAD^ HEAD
# passed
```

Using the locked graph's read-only dependency install in a private source run,
the actual current App TypeScript emitted `clip.set`, `track.set`, and
`clip.move` for a mirrored parent bundle with a hold value plus transition
clear, track label, and absolute move. The current Agent at
`/home/user/work/agent` validated and executed the exact commands and records:
three records with ordinals `[0, 1, 2]`; App and Agent bundles and full records
matched; guarded inverse, inverse redo, and `replay()` all passed. The locked
graph lease wrapper itself targets the older `48576cfa` source tree, so it was
not falsely claimed as a current-tree wrapper result.

The existing generic session test also passed in the 289-test lane and verified
one persisted command list, lost-ack recovery, exact request body, and exact
retry key. No full, browser, socket, live Door, dependency, pin, or shared
install mutation was run.

## Required next step

Forward-port the six-path ordinary integration onto current App integration
`0d5009e18`, resolve the generic-helper/session overlap without restoring stale
source wholesale, then rerun the 289 focused lane, real project `tsc`/lint,
and the current-source locked-graph TS→Agent parity probe. Re-review that
current-root result before adoption.
