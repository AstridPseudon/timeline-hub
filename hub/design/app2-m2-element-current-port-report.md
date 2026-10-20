# App2 M2 element current-root packet report

## Completed

Built the current-root element packet from `ea38656fe` while preserving MAIN574 and TrackInspector. The worktree contains only the row-local element/property changes: the new `elementGesture.ts` helper and the `AstridElementParams` consumer/test. Shared session/hook/state/type changes are emitted only as the four-file private proposal.

The qualified literal existing-clip path uses native capture/finish/submit through the existing command session and outbox. Selected-pack edits retain their existing producer. Overlay, transition, remove, full-panel, and multi-target producers remain reachable; no automatic owner/subscribe construction was edited.

## Decisions

- Kept the shared proposal at exactly four files by treating `elementGesture.ts` as part of the row-local helper/consumer patch, matching the established current-root packet split.
- Recorded the refreshed current-root result as 235 tests rather than repeating the older 229 count; the six-test difference is from current-root additions, not a weakened or skipped test.
- Left the actual Runtime Door row and whole-element-row migration open. No claim of browser, socket, reload/undo, or production zero-legacy qualification is made.

## Exact verification

- Combined 9-file Vitest lane: **235 passed**.
- Adjacent element-adapter/useClipEditing Vitest lane: **37 passed**.
- `node_modules/.bin/tsc --noEmit --pretty false --incremental false`: **passed**.
- Targeted ESLint command with `--no-cache --max-warnings 0`: **passed**.
- `git diff --check`: **passed**.
- Shared and row-local `git apply --check --whitespace=error-all`: **passed**.

No full, browser, localhost, live-socket, Runtime Door, dependency, pin, generated-file, or Git-ref suite was run.
