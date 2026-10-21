# AP2-M2 parent viewport fixture readiness 0952

## Result

Repaired only the row-local setup of the original manual-drop case in
`tests/e2e/local/three-products.spec.ts`. No production source, shared helper,
selector contract, browser viewport, timeout, assertion body, pin, or service
was changed.

The setup now prepares all known geometry in one sequence after
`openCommandTimeline`:

1. waits for the rendered `V1` row;
2. waits for both rendered calibration clips (the `at: 0` clip and the
   `THREE_PRODUCTS_REFERENCE_AT = 15` clip);
3. waits for the mounted `.timeline-wrapper`;
4. clicks the existing normal UI button with exact accessible name
   `Zoom out timeline` once;
5. recalculates the same two-anchor scale and asserts that the unchanged
   centered pointer at `22.5` seconds is inside the mounted wrapper;
6. asserts the centered five-second placement is left `20` and is clear of
   the seeded `15..18` V1 clip.

The existing `dropFileOnTimeline` call, real File/DataTransfer dispatch,
wrong-selection 404 checks, native ADD checks, retry/restart/undo checks,
opaque/order/source/epoch/ACK/raw/hold/zeroLegacy assertions, and
`manualDropPointerAt = 22.5` semantics remain unchanged.

## Causal math and control proof

The retained 0939 run failed at `support/app.ts:235`, before File dispatch or
any import, because its calibrated client X for `22.5` seconds was outside
the mounted wrapper.

The seed anchors are the app clip at `0` and the transition clip at
`15`, so the helper's scale is:

`pixelsPerSecond = (referenceBox.x - dropBox.x) / (15 - 0)`

Main's production external-drop coordinator uses the default five-second
duration and subtracts half the width. Therefore the pointer semantics are:

`left = 22.5 - 5 / 2 = 20`

The existing seed transition occupies `15..18`; hence `20 >= 18`, so the
desired centered placement is non-colliding on V1 and must not reroute to S1.
The original native assertion still requires `track: V1`, `at: 20`,
`clipType: media`.

The real Main control is defined in
`src/tools/video-editor/components/TimelineEditorShellToolbar.tsx`:

- exact DOM label/title: `Zoom out timeline`;
- action: `chrome.setScaleWidth(value => clampTimelineScaleWidth(value / TIMELINE_ZOOM_STEP))`;
- `TIMELINE_ZOOM_STEP = 1.4`;
- default `scaleWidth = 160`, `scale = 5`;
- timeline scale therefore changes from `160 / 5 = 32 px/s` to
  `(160 / 1.4) / 5 ~= 22.857 px/s` after one bounded click.

One click is the smallest moderate UI adjustment: it reduces the 22.5-second
pointer's calibrated offset from `720 px` to about `514.3 px`, without
changing the time coordinate, selected timeline, row, or production offsets.
The fixture additionally checks the actual post-click DOM boxes at runtime, so
the wrapper-boundary result is not guessed or hidden.

No second zoom click is used. This avoids unnecessary scale reduction and
keeps the 8 px edge-snap threshold at about `0.35 s`, far below the
two-second separation between desired left `20` and the existing V1 end
`18`; the placement cannot snap to `18` by this fixture change.

## Verification

Passed:

- `npx eslint tests/e2e/local/three-products.spec.ts --ext ts --max-warnings 0`
- `git diff --check`
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts:1410 --list`
  - exactly 1 intended test listed.

Not run, per task boundary: browser, build, daemon/socket, actual mounted
journey, central test service, full suite, install, or service run. Therefore
the repaired case's real import/ADD/retry/restart/undo qualification remains
unverified until the orchestrator schedules a fresh actual.

## Scope and next step

Only `tests/e2e/local/three-products.spec.ts` is modified. The orchestrator
should run one fresh isolated actual using the repaired source; do not reuse
the failed 0939 packet as a pass.

