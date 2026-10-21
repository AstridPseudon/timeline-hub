# Independent App authored-seek clock review

## Verdict

**REQUEST CHANGES** for App candidate `a97f7cc383007ed19b7cd2afc3a89ff47cb83f40`
(`tree37065fdeda343f82c349f65684da5cd976037d2d`, branch
`tl/app-m2-split-authored-clock-existing-seam-fix-r29`).

The four-file scope and the one-to-one keyboard assertion conversion are
appropriately narrow, but the one-`requestAnimationFrame` boolean guard is not
safe for a rapid-seek sequence once the real Remotion/App seek mailbox ordering
is included.

## Candidate review

The diff is exactly four files, `46 insertions/3 deletions`:

- `useTimelineSync.ts`: set `isSyncingFromTimeline` before the existing
  `previewRef.seek()`, clear it on the next RAF, and keep the existing direct
  `setCurrentTime(time)`.
- `TimelineEditorShellCore.tsx`: route keyboard relative seek through the
  existing `editorOps.onClickTimeArea` seam, retaining the existing non-negative
  clamp and `timelineStore` current-time basis.
- `useTimelineSync.test.ts`: add the `1 -> 1.001` regression and assert a later
  `1.5` preview update is accepted after the RAF.
- `TimelineEditorShellCore.test.tsx`: add the missing `onClickTimeArea` mock and
  convert the existing shell expectation from `__seek(3.5)` to
  `__editorOps.onClickTimeArea(3.5)`.

The shell assertion is one-to-one: it does not remove keyboard seek behavior;
it changes only the carrier asserted. The rejected early return was not revived,
so final release input remains routed through the click seam.

## Real Remotion 4.0.509 ordering

The installed packages were verified as `remotion@4.0.509` and
`@remotion/player@4.0.509` under the shared read-only App install.

The relevant source ordering is:

1. `@remotion/player/dist/cjs/PlayerUI.js:271-284` clamps the public `seekTo`
   frame and calls `player.seek(frame)`.
2. `@remotion/player/dist/cjs/use-player-methods.js:44-60` writes the frame
   state and synchronously dispatches `seeked`; it does not synchronously emit
   `frameupdate`.
3. `@remotion/player/dist/cjs/use-playback.js:300-302` emits `frameupdate` from
   a React `useEffect` after the frame state has committed.
4. App `RemotionPreview.tsx:315-324` has its own RAF mailbox flush. If a second
   seek arrives while the first is active, the latest target is dispatched from
   that mailbox RAF.
5. App `RemotionPreview.tsx:251-253` converts the committed frame to seconds;
   `useTimelineSync.onPreviewTimeUpdate` then decides whether to accept it.

For a single click, the candidate is correct: the explicit seek schedules the
preview mailbox RAF before the candidate's guard-clear RAF; the Player's normal
commit/effect feedback for that seek is expected before the next paint and is
ignored while the guard is held. Playback state, drag state, and final release
input are not changed by the diff.

## Minimal rapid-seek counterexample

Use two timeline-origin seeks A then B before the next frame:

1. A calls `previewRef.seek(A)`, which schedules mailbox RAF `R1`; the candidate
   sets the guard and schedules guard-clear RAF `G1`.
2. B arrives while A is active. `RemotionPreview` stores B as its replaceable
   pending target; the candidate schedules `G2`.
3. `R1` runs before `G1` (it was scheduled by `previewRef.seek` first), clears A,
   and calls `player.seekTo(B)`. That schedules the Player's React frame update;
   the mailbox also schedules its next RAF.
4. `G1`/`G2` clear `isSyncingFromTimeline`.
5. The Player's B frame state commits and its `useEffect` emits `frameupdate`.
   `onPreviewTimeUpdate` now accepts the rational frame echo instead of
   preserving the authored B value. At 30 fps, an authored `1` can therefore
   become `1.001` again in this ordering.

A tiny witness using the installed React DOM scheduler reproduced the essential
ordering: after a queued latest seek is dispatched from a prior RAF, the
`frameupdate` effect observed `guard:false` and accepted frame 2:

```text
[{"event":"frameupdate-effect","frame":0},
 {"event":"frameupdate-effect","frame":2,"guard":false}]
```

This is a timing gap, not a rational-fps or tolerance question. The candidate's
new unit test only models one synchronous `onPreviewTimeUpdate(1.001)` before
the guard RAF and does not cover this queued-seek ordering.

## Minimal correction recommendation

Keep the existing `isSyncingFromTimeline` carrier and the existing
`onClickTimeArea` seam, but make the carrier cover the preview mailbox's active
and queued authored seek(s), rather than clearing solely by the first RAF. The
smallest acceptable correction should either hold the existing carrier through
the mailbox's queued-target flush (with a focused rapid-seek regression), or
carry a seek-generation/completion indication through this existing internal
seam so each timeline-origin Player feedback is consumed before later preview
feedback is accepted. Do not revive the early return, add a second clock, add a
DTO/store/authority, quantize/clamp authored time, or change fps/source-window
behavior.

## Live callers and assertion dispositions

- Timeline ruler click and final pointer release enter
  `useTimelineSync.onClickTimeArea`; the candidate changes their feedback guard.
- Timeline ruler drag remains on the pre-existing `onCursorDrag` guard and
  preserves drag/playback behavior; the candidate does not alter it.
- Keyboard ArrowLeft/ArrowRight enters the same `onClickTimeArea` carrier after
  this candidate; its existing relative delta and non-negative clamp remain.
- Remotion Player `frameupdate` remains the preview-origin callback; it is
  suppressed while the boolean guard is true and accepted afterward.
- Playback slider, CompactPreview slider, TimelineOutlinePanel, browser hook,
  and other direct `previewRef.seek` callers remain direct callers; they are not
  silently claimed as covered by this four-file change.
- The new hook regression covers one authored seek (`1`) versus `1.001` and a
  later legitimate `1.5` update, but not a rapid queued seek.
- The shell expectation conversion is equivalent and preserves the public
  keyboard behavior; no assertion was deleted.
- Existing final-seek/drag/playback tests were inspected unchanged. The peer's
  stated `149 tests, red 1 fail/1 pass -> green 149` was not independently
  rerun, and no DETAILS report was available in the delivered coordination
  paths.

No App source, integration worktree, shared dependency, branch, or ref was
modified. This unit-level review does not qualify the original mounted split
route, physical/native playback, or browser behavior.

## Exact commands and results

Passed:

```text
git -C /home/user/banodoco/reigh-app show --stat --oneline a97f7cc383007ed19b7cd2afc3a89ff47cb83f40
git -C /home/user/banodoco/reigh-app show a97f7cc383007ed19b7cd2afc3a89ff47cb83f40 -- <four candidate files>
git -C /home/user/banodoco/reigh-app diff --check a97f7cc383007ed19b7cd2afc3a89ff47cb83f40^ a97f7cc383007ed19b7cd2afc3a89ff47cb83f40
node -e '<read installed remotion and @remotion/player package.json versions>'  # both 4.0.509
NODE_PATH=/home/user/work/app/node_modules node /tmp/timeline-seek-timing-witness.cjs
```

The witness output is recorded above. The temporary witness was deleted after
the run. No App Vitest suite, central suite, browser, full, physical, native,
install, or shared-dependency write was performed.

Recommended next step: App owner should revise only the existing timeline-origin
feedback carrier to cover the coalesced mailbox seek, add the narrow rapid-seek
regression, and return the exact tree for review. HOME remains responsible for
the original mounted split proof after approval.
