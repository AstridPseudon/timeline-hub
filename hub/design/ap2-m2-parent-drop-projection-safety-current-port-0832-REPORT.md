# AP2 M2 parent-drop projection safety current port

## Verdict

**APPROVE** the exact donor0819 two-file delta for port onto current HOME App
integration. This is an independent data-safety approval for the wrong-target
projection correction, not qualification of the later real parent original case.
Product remains unqualified and there is no writer cut.

The donor's retained packet establishes `DOMhit=V1`, raw `track=S1`, and the
native occurrence-owned `S1` fence refusing before any commit POST. It does not
serialize the internal transient row snapshot, so the browser trace alone does
not prove the projection mismatch. The source-level regression does prove that
the observed wrong owner is produced when mutable rows are reordered against
rendered track geometry, while the existing strict occurrence refusal remains
unchanged.

## Source identities and exact delta

- HOME base: `hub/tl/integration` / `e2267a418a89d659c1a70524b17dde631f12fd16`, tree `99af03128b9df4d20e5ca8779cb7540a8bc8be8a`.
- Donor base: `af1605a28f31a53b5a3472251493d44941b618fe`, tree `b0cb1f973c0e1b465241ebef38bd267fd39f0434`.
- Donor final harness ref: `tl/ap2-m2-parent-drop-owner-origin-0819`, commit `a4a93dab33eb6c01a52501c99a12f0e267c916fc`, tree `580819cc95662553da7bda5283b453009e7c0651`.
- Exact uncommitted patch hash: `8e54d4d5277de6a2c556582c33277a9216431180a43e6301af6375fdc0c4f9ef` (matches donor commit's binary patch).
- Final patched blobs: `drop-position.ts` `c634ede997c8ca9c197fcf17d84fcf2630c69889`; `drop-position.test.ts` `4ed1d4cde67f32f1b573baafea400ae58bc4dd22`.
- Changed paths are exactly `src/tools/video-editor/lib/drop-position.ts` and `src/tools/video-editor/lib/drop-position.test.ts`.
- Final harness commit SHA/tree: pending the post-exit harness commit; no committed final SHA/tree was available while writing this report. The committed base and exact final blobs above are recorded for reconciliation.

## Safety review

`TimelineCanvas.tsx:557-565` builds and publishes row geometry from the
existing `tracks` order. `buildTimelineRowLayout` records each media row's
`mediaRowIndex` in that same order (`timeline-row-layout.ts:70-74`). The planner
previously indexed the raw pointer against `current.rows`, then resolved the
row ID (`clip-drag-planner.ts:230-247`), allowing a lagging/reordered mutable
snapshot to select `S1` for a hit whose rendered owner was `V1`.

The port maps `current.tracks` to existing rows by ID, retaining each row's
actions and row-local behavior. A missing row gets only `{ id, actions: [] }`.
This preserves normal target identity and intent, makes transient reordered
rows follow the rendered owner, keeps mixed/data-lane `mediaRowIndex` geometry
and data-lane refusal behavior unchanged, preserves same-ID actions by ID, and
does not invent or normalize an accepted state. Empty-track construction still
uses the planner's existing new-track path; the focused planner empty-row test
remains green.

The occurrence-owned safety fence is unchanged at
`src/tools/video-editor/commands/parentClipAddCapture.ts:379-385`, including
the original `S1` refusal. No fixture, guard, shared session, Provider,
harness, door, preview, retry, or writer path was changed.

## RED to GREEN evidence

Base-only new regression, before the source correction:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/drop-position.test.ts -t 'keeps the hit owner when mutable rows lag the rendered track order'
```

Result: **RED**, `1 failed, 5 skipped`, exit `1`; expected `v`, received `a`.

Final donor/current port and focused controls:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/drop-position.test.ts src/tools/video-editor/lib/clip-drag-planner.test.ts
```

Result: **GREEN**, `2 files, 39 tests passed`.

Final checks:

```text
node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/lib/drop-position.ts src/tools/video-editor/lib/drop-position.test.ts
```

Passed. `git diff --check` passed. No browser, actual journey, build,
install, socket, full suite, test-service request, matrix, snapshot, or
exhaustive run was performed.

## Changed live callers and infrastructure

The changed helper is consumed live by
`src/tools/video-editor/hooks/useDragCoordinator.ts:155-170`; its resulting
`DropPosition` is used by clip drag commit and external-drop finalization.
External drops finalize through `useExternalDrop.ts:621-650`, carry the target
through `external-drop-utils.ts:453-457,512-525`, and reach native prepared
placement via `useAssetManagement.ts:303-317`. These callers were inspected,
not modified.

**main infrastructure touched:** none; the correction is App projection logic
only and leaves Main infrastructure/helpers untouched.

The required merge-forward helper was invoked immediately before final checks.
It was a no-op because HOME `tl/integration` was already the worker base, and
the sandbox rejected its `ORIG_HEAD` lock update as read-only. No direct merge,
commit, rebase, push, or branch/ref mutation was performed.

## Recommended next step

Reconcile the post-exit harness commit SHA/tree, then merge this approved
two-file result. Keep the product unqualified until the later real parent
original case supplies browser/actual evidence.
