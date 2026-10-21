# Viewing queued-seek completion producer — handoff

Status: **implemented and targeted-qualified; consumer/activation remain held**.

Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-queued-seek-existing-callback-producer-0935/REPORT.md`

## Current-only source packet

- Worktree: `/home/user/work/wt/vw-m3-queued-seek-existing-callback-producer-0935`
- Base source: `4db86a76acd505dd1c7dc798695e2b7a9c932170`, tree `461fa0cddd67f4eb574563b38407733bd50afa7c`
- Current producer blob: `df6bf5740412f92b6f00e2f81841fb3236c799c2`
- Current direct-test blob: `ca5238598ccde30b5a786fc9124e40949ac69a5a`
- Current-only `git diff --binary` SHA-256: `426efc6110a4b9fca75c703f1b6fc989bfd2e914822d389ffb890b0ddc92ad9f`
- Exact patch source is the uncommitted diff in the worktree above; no unrelated
  files are included. Harness commit/tree is intentionally unavailable until
  the worker exits and the harness commits it.

The producer source was byte-compared before editing against HOME
`33b4a86cfdc2ac2ee63b069c225ae465d1f35656` and pending
`ab938b4beacc02419de7293dfa09190956b9d0ba`; all three pre-edit SHA-256 values
were `3bd5cddce54f10e0b75c28aab7ddcea9b4f1c860508ad24bec4b7c0679a5a902`.

## Contract and evidence

`onTimeUpdate(time, seekComplete?)` is the existing callback with one optional
bit. The producer retains the active target beyond the mailbox RAF, treats A's
feedback as ordinary while B is queued, and marks B's matching frame feedback
complete. It explicitly completes same-frame/clamped no-op seeks without a new
frame effect. Config replacement cancels stale active state and dispatches only
the matching generation from the existing pending mailbox; unmount clears the
mailbox and completion state. No consumer, public Player API, DTO, store,
counter, clock, fps, source window, tolerance, or authored time changed.

The new scheduler witness uses the existing preview mailbox and a React
state/effect Player fixture. At `30000/1001` it proves the actual order
`seek:15 → frameupdate:15 → seek:30 → frameupdate:30`, with only the final
callback carrying `true`; later frame 45 is ordinary feedback. Direct neighbors
cover same-frame completion, coalesced latest target, config-deferred delivery,
and unmount cancellation. Existing assertions were retained unchanged.

## Exact checks

- Targeted Vitest: **47 passed / 3 files** (`RemotionPreview.test.tsx`,
  `RemotionPreview.mailbox.test.tsx`, `RemotionPreview.audioFailure.test.tsx`)
- Scoped ESLint: **passed**
- `git diff --check`: **passed**
- No full, browser, actual split, physical/native, Runtime, socket/helper,
  install, or public graph qualification was run.

Live callers changed: **none**. Existing callers remain one-argument callback
consumers. App owns the paired `useTimelineSync`/`useTimelinePlayback` consumer
and must review this producer before activation and the original mounted split
proof.
