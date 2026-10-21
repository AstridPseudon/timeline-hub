# App2 clip scalar public-patch type fix

## Result

Fixed App diagnostic `clipScalarGesture.ts:26:37` with the smallest source
change. `ClipScalarArgs.clear` remains the four-key command-side carrier,
including `elementRef`. `clipScalarPreview` now projects only
`hold | asset | transition` into the existing public `TimelinePatch.clear`.
The paired command still carries `['transition', 'elementRef']`; the
transition-only reset remains `['transition']`.

Changed files:

- `src/tools/video-editor/commands/clipScalarGesture.ts`
- `src/tools/video-editor/commands/clipScalarGesture.test.ts` (keeps the
  original command assertion and updates the preview assertion to the public
  shape)

No SDK, Runtime, DTO, pin, normalization, caller, or public API changes.

## Verification

Working directory for all commands: `/home/user/work/wt/ap2-m2-clip-scalar-public-patch-type-fix-1220`.

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts`
  - PASS: 3 files, 99 tests.
- `./node_modules/.bin/eslint src/tools/video-editor/commands/clipScalarGesture.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts --report-unused-disable-directives --max-warnings 0`
  - PASS.
- `git diff --check`
  - PASS.
- `flock -w 300 /home/user/work/.app-tsc.lock bash -lc './node_modules/.bin/tsc -p tsconfig.app.json --noEmit > /tmp/ap2-m2-clip-scalar-public-patch-type-fix-1220-tsc.log 2>&1; status=$?; cat /tmp/ap2-m2-clip-scalar-public-patch-type-fix-1220-tsc.log; exit $status'`
  - NONZERO: 28 existing diagnostics, all outside the changed App2 source.
    None mention `clipScalarGesture.ts`, `clipScalarCapture.ts`, or
    `commitSession.clipScalar.test.ts`. The remaining diagnostics are
    package/Composition-boundary errors: optional `theme` versus the resolved
    package `TimelineConfig`, missing declaration exports such as
    `CompiledCanonicalTransitions`, `computeMediaTrim`,
    `getSanitizedPlaybackRate`, `clipOpacity`, and
    `encodedEnvelopeSource`, plus related implicit-any diagnostics in
    Composition callers. They are not claimed green or fixed here.

Dependency resolution was read-only and used the existing protected graph:
`realpath node_modules/@banodoco/timeline-composition` resolves to
`/home/user/work/app/node_modules/@banodoco/timeline-composition`, version
`0.0.8`; declarations came from that path's `dist/*.d.ts`. No install, cache
write, shared-node_modules mutation, or new dependency graph was performed.

## Live-call review handoff

No live caller changed. The existing preview seam is consumed by
`submitClipScalarEdit` and `submitClipTransitionClears` in
`clipScalarGesture.ts`, and by the scalar batch preview in
`commands/commitSession.ts:990-991`. Existing UI callers remain
`BulkClipPanelBody.tsx:212` for atomic transition clears and
`ClipTransitionSection.tsx:116` for transition-only clears.

Independent diff review confirms the public preview no longer attempts to
carry `elementRef`, while the durable command validation and paired semantic
capture remain unchanged. No browser, full suite, frozen packet, or custody
proof was run or claimed.
