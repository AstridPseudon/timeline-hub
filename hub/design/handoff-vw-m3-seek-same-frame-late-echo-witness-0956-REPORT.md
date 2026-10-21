# Same-frame late-echo witness

## Result

The approved producer at `13bf239d9` is unsafe for the distinct same-frame
ordering requested here. The focused witness in
`src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx`
is intentionally `it.fails`: it proves that a queued A frame-30 effect arrives
after B1's explicit same-frame completion and is forwarded as an unmarked
ordinary callback.

No product source, hook consumer, public API, clock, counter, store, fps,
tolerance, or authored time was changed. The only worktree change is the
focused mailbox fixture/witness.

## Exact trace

At `fps = 30000 / 1001`:

1. A advances the Player's current frame to `30`; its React `frameupdate`
   effect is held in the fixture's existing scheduler boundary.
2. Authored B1=`1` calls `PreviewHandle.seek(1)`, which rounds to frame `30`.
   `getCurrentFrame()` is already `30`, so the producer calls `seekTo(30)` and
   explicitly completes B without a new frame transition.
3. The callback is `[1.001, true]` (`30 / (30000 / 1001)`).
4. A's queued frame-30 effect is released after that completion. The source's
   `onFrameUpdate` sees no active seek marker and emits ordinary `[1.001]`.
5. Later frame `45` is ordinary `[1.5015]`.

Mailbox/event trace: `seek:30 -> frameupdate:30`; the only `seek:30` is B's
same-frame `seekTo`, and the later `frameupdate:30` is the queued A effect.
The expected assertion deliberately excludes the late ordinary `[1.001]`, so
the test remains an explicit red requirement under `it.fails`.

## Source reason

`RemotionPreview.tsx:369-375` explicitly completes a same-frame seek and clears
`activeSeekFrameRef`. `RemotionPreview.tsx:310-320` then labels a frame update
complete only while that marker matches; after the explicit completion the
queued A frame-30 effect therefore takes the ordinary branch.

This ordering is source-backed by the installed Remotion package:
`@remotion/player/dist/cjs/use-player-methods.js:44-60` updates the imperative
frame reference synchronously and avoids a timeline state update when the
target is unchanged, while `use-playback.js:300-302` dispatches `frameupdate`
from a React effect whenever frame state changes.

## Minimal correction proposal — unapplied

The smallest source-side direction is an internal one-shot same-frame stale
effect marker: record the explicitly completed frame, suppress exactly one
later matching `frameupdate` callback, clear the marker there (and on unmount),
then retain the existing ordinary path for later frame 45. This changes no
consumer/API/clock/counter/store/fps/tolerance contract. The marker must be
reviewed against a legitimate later same-frame playback event before landing;
the proposal is intentionally not applied by this worker.

The unapplied proposal is in
`handoff-vw-m3-seek-same-frame-late-echo-witness-0956-UNAPPLIED.patch`.

## Evidence

- Focused Vitest: **19 passed, 1 expected fail** in one mailbox test file.
- Scoped ESLint on the touched test: **passed**.
- `git diff --check`: **passed**.
- `git apply --check` on the unapplied proposal: **passed** (the proposal was
  not applied).
- No full, browser, native/physical, Runtime, socket/helper, install, or graph
  qualification was run.
