# App native parent trim 029 independent review

## Verdict: HOLD

The source slice is well-contained and the focused suites pass, but there is one
real source-window boundary defect:

- `src/tools/video-editor/commands/clipTrimCapture.ts:169-190` validates the
  unrounded `sourceOut <= limit`, then persists `rounded(sourceOut)` at line
  190. A private repro against `349cf9c77` with registry duration
  `9.9999999` and `out_s=9.99999989` returns `to=10`, `hold=10`. Thus the
  accepted/persisted raw source window exceeds the authoritative registry
  duration even though the input endpoint was in range. The fix should either
  validate the rounded endpoint against the authoritative limit or avoid
  rounding the persisted endpoint. Add this boundary regression before
  approval.

This is the only blocker found. `git diff --check` also reports a non-blocking
extra blank line at EOF in `clipTrimGesture.ts:40`.

## Evidence checked

- Golden parity and exact authored output: `clipTrimCapture.ts:83-200`, with
  `clipTrimCapture.test.ts:34-47`; from/to/hold are source seconds, speed is
  retained, opaque own fields and ordering survive, and the rational
  `30000/1001` fps metadata is untouched (`clipTrimCapture.test.ts:49-64,
  134-147, 150-167`).
- Null/absence and intent cleanup are covered by
  `clipTrimCapture.test.ts:66-85` and
  `commitSession.trim.test.ts:275-294`. Unsupported duration aliases are not
  substituted: `clipTrimCapture.test.ts:169-189` checks the registry's raw
  `duration` and original media/duration guards.
- Reserved identity and ownership fail closed in
  `clipTrimCapture.ts:83-90`, `commitSession.ts:323-338`, and tests at
  `clipTrimCapture.test.ts:124-132` and `commitSession.trim.test.ts:192-210`.
  Grouped, occurrence-owned, mapped, and missing-identity paths produce no
  preview or commit traffic.
- Exact retry/recovery and B-after-unknown-A behavior are asserted in
  `commitSession.trim.test.ts:40-74` and `:228-273`: the original in-flight
  body/key is replayed exactly, B stays behind A, B is rebased to A's accepted
  head only after A recovery, and undo targets B alone. The existing durable
  session machinery remains the single path (`commitSession.ts:428-465,
  488-505`).
- Compound/mixed preview refusal is atomic in `commitSession.ts:368-377`, with
  the prepared trim reusable after refusal in
  `commitSession.trim.test.ts:212-225`. UI capture/finish/submit failures and
  unsupported ownership retain the typed draft without legacy writes in
  `ClipPanelBody.trimSession.test.tsx:200-263` and `:297-365`.
- There is one native trim session port and one compiler path: session wiring is
  `commitSession.ts:323-378`; native preview validation and exact-clone
  materialization are `timeline-patch.ts:1016-1034` and `:1934-1996`.
  Production property-panel ingress passes both the current raw timeline and
  the native port (`PropertiesPanel.tsx:536-545`, `PropertiesPanelBody.tsx:543-556`).
  The old direct `onChange` fields remain only for compatibility callers that
  omit native ingress; the production ingress activates the native controls.
- No source-slice code or test claim was found for collision, snapping, or
  media-duration behavior beyond the authoritative registry-duration guard.
  The defect above is specifically a rounding-at-the-boundary issue in that
  guard, not an unrecorded product claim.
- Compared with upstream `04346844f` (the “44f” retry/recovery line), the
  target adds the trim port and native preview only; it does not introduce a
  second outbox/retry policy. The existing session's exact pending identity and
  recovery flow are reused.

## Tests

All commands ran from a private `git archive` snapshot of
`349cf9c77a04f4f4f887ef4b8f539782e1ca1609`, with the shared `node_modules`
read-only and Vitest cache disabled.

1. Added trim suites, runner mode with a private `__dirname` shim, one worker,
   no file parallelism:

   `NODE_OPTIONS="--import data:text/javascript,globalThis.__dirname='.../config/testing'" npx vitest run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/clipTrimCapture.test.ts src/tools/video-editor/commands/clipTrimGesture.test.ts src/tools/video-editor/commands/commitSession.trim.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.trimSession.test.tsx`

   Result: **4 files, 82 tests passed**.

2. Neighbor suites, no cache, one worker, no file parallelism:

   `npx vitest run --config config/testing/vitest.config.ts --no-cache --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/time-grid-conformance.test.ts src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx`

   Result: **5 files, 506 tests passed**. Existing move, group/occurrence,
   ordinary session, compiler, timing, and property-panel positives remain
   green.

3. Boundary repro (no source mutation): registry duration `9.9999999`,
   endpoint `9.99999989`; result was `to=10`, `hold=10`.

Not run: full suite, build, browser/e2e, live sockets, TypeScript compiler, or
dependency installation, per review scope.

