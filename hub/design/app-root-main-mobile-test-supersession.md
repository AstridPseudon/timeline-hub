# App root MAIN mobile label test supersession

Owner-approved decision: MAIN touch product UI remains unchanged. Touch track
editing is delegated to the Agent, while native track-label command capture is
covered only on desktop. This is a staged test supersession authorized by the
owner, not a product-code change or unilateral weakening.

Source SHA: `35ebae007d848ff22d8da89461bdb66efc93472f`

## Exact old/new mapping

The following eight staged c866 phone/tablet `it.fails` cases were removed from
the staged source and are **never claimed passing**. Every one is **superseded
by the owner's mobile overhaul (44f0b9ca9)**:

- `captures the phone edit before typing and retains it across a remote label change` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `submits an empty phone name on blur as a value` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `keeps phone input and a visible reason after command refusal` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `captures the tablet edit before typing and retains it across a remote label change` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `submits an empty tablet name on blur as a value` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `keeps tablet input and a visible reason after command refusal` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `forwards the phone name edit through the canvas and memoized row` — superseded by the owner's mobile overhaul (44f0b9ca9).
- `forwards the tablet name edit through the canvas and memoized row` — superseded by the owner's mobile overhaul (44f0b9ca9).

Desktop behavior is retained exactly: `TrackListRenderer.test.tsx` keeps its
three desktop capture cases and `TimelineCanvas.test.tsx` keeps its one desktop
capture case, including their original inputs and assertions. The new mapping
adds real phone/tablet label-click coverage in both files: selection remains
available to Agent context, while label-capture callbacks stay untouched. No
missing Track settings-control assertion was added.

## Scope and counts

- `TrackListRenderer.test.tsx`: remove 6 phone/tablet expected-failure cases
  and its `labelTest` alias; retain 3 desktop capture cases; add 2 touch
  no-capture cases (phone and tablet).
- `TimelineCanvas.test.tsx`: remove 2 phone/tablet expected-failure cases and
  its `labelTest` alias; retain 1 desktop capture case; add 2 touch no-capture
  cases (phone and tablet).
- Exactly the two allowlisted test files were modified. Product code, old boot,
  render, root semantics, policy, and unrelated tests were not changed.
- Current known failure marker count: **3**, the three pre-existing audited
  drag markers in `useClipDrag.test.tsx`; forbidden-marker gate passes at
  maximum 0.
- Actual current pair/browser qualification remains **OPEN** and is not
  claimed by this unit-test-only change.

## Worker report and evidence

- `npm run check:known-failures` — PASS; 3 authorized drag markers, 0
  forbidden markers (maximum 0).
- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx` — PASS; 2 files, 110 tests.
- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism --testNamePattern='(captured track names|track label command capture forwarding|agent-owned)' src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx` — PASS; 11 selected tests, 99 skipped by pattern.
- An initial `--minWorkers=1` invocation was rejected by this installed Vitest
  (unknown option). `--configLoader=runner` was also incompatible with this
  repo config because it uses `__dirname`; the successful cache-free run used
  Vitest's default config loader and `--maxWorkers=1`.
- No full suite, build, browser, socket, TypeScript, or install command was
  run.
