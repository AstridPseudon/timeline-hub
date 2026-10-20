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

## MAIN17 supersedes the44f-only touch shape — 2026-10-20 12:14 UTC

Owner11:54 requests true refresh of17e46de99b7cef52fe494de1703a9865a8d4be24, now transferred by lead12:12. It adds a touch track sheet with rename/settings/add/delete and removes Text while preserving Gallery/AskAstrid. Its eight-path positive behavior is the newest owner product. The earlier10:13 no-input/Agent-only conclusion remains historical for44f and cannot be applied to hide new17 touch rename. Main refresh worker preserves17 positives; next root/native label port must bind every actual new rename input through the existing command capture/session, preserve desktop original guards, and qualify phone/tablet track-sheet positives. No it.fails or revived superseded44f-only assumptions. Oldc866 staged test removal was correct for44f and is not silently relabelled as17 proof.
