# App mobile label MAIN test supersession

Owner-approved decision: MAIN touch product UI remains unchanged. Touch track
editing is delegated to the Agent, while native track-label command capture is
covered only on desktop. This is a staged test supersession authorized by the
owner, not a product-code change or unilateral weakening.

Source SHA: `35ebae007d848ff22d8da89461bdb66efc93472f`

## Removed staged c866 phone/tablet cases

Each case below was an `it.fails` case in the staged source. It was removed
from the staged source and is **never claimed passing**; each is explicitly
**superseded by the owner's mobile overhaul (44f0b9ca9)**:

- `captures the phone edit before typing and retains it across a remote label change` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `submits an empty phone name on blur as a value` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `keeps phone input and a visible reason after command refusal` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `captures the tablet edit before typing and retains it across a remote label change` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `submits an empty tablet name on blur as a value` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `keeps tablet input and a visible reason after command refusal` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `forwards the phone name edit through the canvas and memoized row` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `forwards the tablet name edit through the canvas and memoized row` — superseded by the owner's mobile overhaul (44f0b9ca9).

## Exact old/new mapping

- TrackListRenderer's three desktop capture cases retain their original inputs
  and assertions. The six phone/tablet capture cases above are removed.
- TimelineCanvas's desktop capture case retains its original inputs and
  assertions. The two phone/tablet capture cases above are removed.
- `TrackListRenderer.test.tsx` now covers the real phone and tablet label click
  path: selection is still delivered and neither label capture nor the
  presentation change callback is invoked.
- `TimelineCanvas.test.tsx` now covers the real phone and tablet label click
  path through the canvas: track selection is still delivered and
  `onTrackLabelEditStart` is not invoked.
- No Track settings-control assertion was added to the new touch coverage.

## Marker and scope accounting

- Current known failure marker count after the change: **3**, all the existing
  audited drag markers in `useClipDrag.test.tsx`; the two forbidden markers in
  these allowlisted files are gone.
- Modified source files: exactly the allowlisted pair,
  `TimelineCanvas.test.tsx` and `TrackListRenderer.test.tsx`.
- No product code, boot, render, root semantics, policy, or unrelated test
  files were changed.
- The actual current pair/browser qualification remains **OPEN** and is not
  claimed by this unit-test-only change.
