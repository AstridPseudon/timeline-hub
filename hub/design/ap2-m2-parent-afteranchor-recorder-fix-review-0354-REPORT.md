# After-anchor recorder repair review

Decision: **HOLD** exact App repair `0fa122179fdd15ba18f6c37346308049edb52cd5` (tree `3132426eb5f07cacfc18404ada8ad98880ddc278`). It is mechanically correct for the accepted positive-hold slice, but the requested missing/null-hold contract cannot be approved against frozen Agent `3b3208c43903b770010de0649691cfa566447822` (tree `84120e176540fbc2281dcff4b7186ec8ae413274`).

## What was verified

- The old append-then-synthetic-recorder repair is gone. The dormant path uses the existing `MoveRecording` seam for raw anchor/peer reads, same-track peer writes, mirror compilation before creation, boundary insertion, and final compilation.
- The exact Agent comparison matched four complete command/record/bundle cases and deterministic replay, including the two natural mirror `derived_writes` entries. It also matched six refusals.
- `at_ms` is no longer stripped/restored. A source row carrying it refuses with the Agent-compatible unsupported-timing result.
- Incoming transition and opaque fields survive cloning; explicit null effect IDs remain null; a positive sub-0.05 duration uses the 0.05 floor. Zero hold is refused after the same floor computation, matching Agent behavior.
- The optional seam callback is only used by the dormant after-anchor path. Existing append behavior remains on its original path. No UI, session, Provider, service, HTTP, generated contract, pin, activation, or live `afterClipId` caller changed. Live callers changed: **none**.

## Remaining concrete defect/blocker

Agent's raw-window helper can derive a missing/null hold from `from`/`to`, but the authoritative `ClipAddMediaArgs.row` schema requires a positive numeric `hold` before that helper runs. Exact Agent results are:

- missing hold: `invalid_edit_command: 'hold' is a required property`;
- null hold: `invalid_edit_command: None is not of type 'number'`;
- zero hold: `invalid_edit_command: 0 is less than or equal to the minimum of 0`.

The App repair therefore refuses missing/null hold and retains two strict expected-failure tests for the requested positive behavior. This is faithful to the frozen Agent, but it does not satisfy the requested from/to-derived missing/null acceptance. Agent ownership must resolve the schema/handler disagreement before this candidate can be approved or activated. No App-only normalization or new carrier is justified.

## Evidence

The repair worker ran the following focused Vitest lane with a private config/cache and shared dependencies read-only:

```sh
TMPDIR=/tmp/w-d5d5a74fca PARENT_AFTER_PARITY_OUTPUT=/tmp/w-d5d5a74fca/parity.json ./node_modules/.bin/vitest run --config /tmp/w-d5d5a74fca/vitest.config.ts --no-cache src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/commitSession.parentMedia.test.ts src/tools/video-editor/services/parentMediaCommands.test.ts
```

Result: 4 existing files, 45 passed and 2 expected failures (47 total); two nonexistent filters were not counted. Neighbor session/media lane:

```sh
TMPDIR=/tmp/w-d5d5a74fca ./node_modules/.bin/vitest run --config /tmp/w-d5d5a74fca/vitest.config.ts --no-cache src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/media.test.ts
```

Result: 2 files, 82 passed.

Exact Agent parity command matched 4 complete commands/records/bundles/replays and 6 refusals. Focused ESLint, focused TypeScript, and `git diff --check` passed. No full suite, browser, live service, HTTP, native Door, or unchanged UI/session qualification was run.

The review worktree itself has no product edits. The candidate is dormant and must remain unmerged/unactivated pending the Agent contract decision.

