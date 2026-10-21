# App queued-seek correction review

## Verdict

**REQUEST CHANGES** for corrected App candidate `6adab30a50ff17840bd55f534aff69ebc3f46f40`.

The correction removes the first-RAF expiry, but it still treats the public
Remotion `frameupdate` event as completion for the latest coalesced seek. That
event is emitted for every committed frame, including the active A seek before
the queued B seek is flushed. A single boolean can therefore be consumed by A
and leave B unguarded.

## Exact counterexample

Current `RemotionPreview` keeps one active seek and one replaceable pending
seek (`RemotionPreview.tsx:331-375`). `onClickTimeArea(A)` sets the latch and
dispatches A; `onClickTimeArea(B)` queues B. If React commits A and runs its
Player `frameupdate` effect before the preview mailbox RAF dispatches B:

1. `frameupdate(A)` enters `onPreviewTimeUpdate`, sees the latch, clears it,
   and returns.
2. The mailbox RAF dispatches queued B.
3. `frameupdate(B)` enters with the latch false and is accepted by
   `timelineRef.current?.setTime(...)`.

At 30 fps, if authored B is `1`, the accepted frame echo can be `1.001`,
re-authoring the exact drift the correction is intended to prevent.

A narrow React DOM scheduler witness using the installed dependencies produced:

```text
[{"event":"frameupdate-effect","frame":1,"guard":true},
 {"event":"frameupdate-effect","frame":2,"guard":false}]
```

The witness models the actual sequence: set guard, commit active A, schedule
the mailbox RAF that commits B, then observe the two effects. This is not a
fps/tolerance issue.

The public package source confirms the contract: `use-player-methods.js:44-60`
updates the frame state on `seekTo`, while `use-playback.js:300-302` dispatches
`frameupdate` from an effect whenever `frame` changes. App forwards every such
event at `RemotionPreview.tsx:302-304`; it does not identify the latest queued
seek.

## Test gap and preserved behavior

The new regression in `useTimelineSync.test.ts:79-127` passes, but it calls A
and B before rendering any Player effect, then flushes the mailbox and renders
only one synthetic frameupdate. It therefore cannot expose A's earlier effect
consuming the boolean.

The corrected diff is narrowly scoped to `useTimelineSync.ts` and its test;
`RemotionPreview`, fps/window/tolerance behavior, native commands, and public
Player API are unchanged. `onClickTimeArea` still sets the latch, seeks, and
mirrors time without the rejected early return, so final-release input remains
preserved. The callback uses existing refs and has no separate closure/state
issue. Legitimate later playback updates are accepted after the first event,
but that same behavior is the problem when the first event belongs to A rather
than the latest queued B.

Recommended next step: retain the existing carrier and make it distinguish or
cover the active and queued timeline-origin seeks through the mailbox flush,
with a regression that observes A's frameupdate before B is dispatched. Do not
change the Player public contract, fps, tolerance, source window, or native
commands. HOME remains responsible for the mounted split after approval.

## Exact commands and results

Passed:

```text
git diff --check a97f7cc38 6adab30a5
TMPDIR=$(mktemp -d /tmp/timeline-queued-seek-review.XXXXXX) \
  ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/hooks/useTimelineSync.test.ts \
  src/tools/video-editor/components/TimelineEditorShellCore.test.tsx
# 2 files, 127 tests passed
NODE_PATH=/home/user/work/app/node_modules node <inline React scheduler witness>
# output: frame 1 guard:true; frame 2 guard:false
node -e "...read @remotion/player and remotion package.json versions..."
# @remotion/player 4.0.509; remotion 4.0.509
```

The first attempted `--configLoader=runner` invocation was not a product
failure: this repository's config uses CommonJS `__dirname`, which that loader
does not provide. The normal config with `--no-cache` passed.

Not run: full/central suite, browser, physical/native playback, mounted split,
or live-socket tests. No App source, shared dependency, branch, or ref was
modified. The previously reported 149 targeted-test baseline was not
independently rerun as a whole; the two directly relevant files were rerun.
