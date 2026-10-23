# Handoff: ap2-P2-core-corrected-review-0431

## Verdict

PASS for the independent source review. The only allowed product/test file is
the new `tests/e2e/local/three-products.p2-tour.spec.ts`.

## Review result

The first-return test correctly models the production mounted caller for three
gestures: one parent move and single/bulk transition-None clears. It asserts
the exact guarded `doc.patch` command and ordered step changes, old-value
states, omitted request/step reads versus empty arrays, atomic fallback,
effective reply mode, canonical closure identity/digests/pins, raw absence and
opaque/order preservation, intended-field-only deltas, all siblings, receipt
and history attribution/dependencies, Runtime history with no new legacy
entries, network zero old-route writes, reload, and actual mounted Undo.

One review defect was corrected: the prior helper allowed the actual ABI-1
`undoTimeline` request to omit `label`/`steps`, but also waived the v2
authoritative metadata on the accepted inverse reply/history. It now requires
the synthesized `Timeline edit` label, nonempty authoritative steps and
patches/dependencies, effective merge mode, source, and matching history
records, while retaining the real caller's request shape. `dry_run` is also
required to be the production caller's explicit `false`.

Production trace at current `66b87816e4ce3aa953f2abd53f7ff98cd29b1608`:
`useTimelineSave` → `timelineLocalSaveHandoff` → `createLocalSaveSession` /
`documentPatchIntent`; Undo uses `RuntimeDataProvider.undoTimeline` and the
same commit endpoint.

## Checks

- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p2-tour.spec.ts --list` — PASS, exactly 3 tests.
- `npm exec tsc -- --noEmit` — PASS; root tsconfig excludes e2e tests.
- `npx eslint tests/e2e/local/three-products.p2-tour.spec.ts --max-warnings 0` — PASS.
- `git diff --check` — PASS.

## Limitation

Browser/socket/Runtime/central service/full-suite execution was forbidden, so
the real gesture bodies, `/commits` history, canonical response readback,
reload, and mounted Undo are not runtime-qualified here. D13 future fields
were not demanded; no extra conflict/invalid/preview cases were added.
