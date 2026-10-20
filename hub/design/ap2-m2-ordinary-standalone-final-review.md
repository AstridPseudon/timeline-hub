# AP2 M2 ordinary standalone dispatch repair — final review

Date: 2026-10-20

## Verdict

**APPROVE for the patch.** The repair is a narrow dispatch sequencing fix on
`f76d61c5cfa222939a6cc77509e5f7c03019c611` (patch SHA-256
`cd08aa8a8ebc3f0db94834be9bc1e4eedebb4317d6f399676d703196a995e972`). It
classifies the complete patch before native capture, owner resolution, local
preview, or enqueue:

- fully supported batches use the existing native generic port;
- mixed supported/unsupported batches enter that port and refuse atomically
  during its all-member preflight;
- all-unsupported standalone batches bypass the native port and retain the
  existing validate/compile/guarded `commitData` snapshot path.

There is no post-capture fallback, copied support predicate, new legacy
writer, or history/`legacyClean()` bypass. The mounted compiler canary remains
on its existing standalone path until its native migration.

**Actual Door/browser: HOLD.** No Runtime HTTP/Door, browser, localhost,
live-socket, or full-suite qualification was run, as required by the brief.

## Private application and checks

The patch applied cleanly to a fresh archived copy of the assigned `f76d61c5`
root. The assigned worktree remained clean.

Commands and results:

```text
git -C /home/user/work/wt/ap2-m2-ordinary-standalone-final-review apply --check \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-standalone-dispatch-repair.patch
=> exit 0

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
=> 9 files, 275 tests passed

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

git -C /home/user/work/wt/ap2-m2-ordinary-standalone-final-review diff --check
=> exit 0
```

## Behavior verification

The real mounted `useTimelineOps` hook was exercised with the real
`createTimelineCommandSession` generic port in a private one-off probe:

- `compiler-canary.ts` produced its actual source + source-map
  `project-data.write` batch. It made exactly one guarded snapshot commit,
  preserved two project-data entries, and made zero native-port calls.
- A mixed `track.update` + `project-data.write` batch raised
  `Native patch refused` at native capture preflight. It made no snapshot
  commit; finish and submit were not reached.

The native capture tests assert that the supported two-member batch becomes
one ordered command list (`clip.set`, `track.set`) with ordinals `[0, 1]`,
and that unsupported members are rejected before the owner resolver runs.

`commitSession.genericPatch.test.ts` asserts the existing outbox behavior:
one listed owner/intent, one command in the request body, and after the lost
ack/restart retry the request body text and `Idempotency-Key` are byte-for-byte
identical to the original. The mounted session wrapper still applies the
existing `legacyClean()` barrier to native capture, finish, and submit.

## Limits

No product, shared worktree, dependency, pin, generated contract, Git ref,
ledger, or source/test file was changed by this review. No full suite,
browser, socket, Runtime Door, or owner-film run was performed. Runtime-door
acceptance, browser reachability, and actual end-to-end mounted transport
remain unverified and are separately HOLD.
