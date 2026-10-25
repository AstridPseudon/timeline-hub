Implemented A3/P2 faithful native-none bulk transition control.

- Restored canonical two-clip fixture fidelity: opaque transition/source fields, tracks, registry metadata, scene markers, occurrence ownership, and exact transition values.
- Fixed first proven product boundary in `useTimelineCommit`: row materialization now preserves authored clip extension fields while applying known edits.
- Added exact v2 command/read assertions and opaque-field preservation coverage.
- TimelineEditorCore and protected areas untouched.

Results:

- Mounted test: 10 passed.
- Adjacent suites: 113 passed.
- Typecheck: passed.
- ESLint scoped with `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Diff limited to the mounted test and `useTimelineCommit.ts`.
- No full/browser suite run.

The actual 21061 request body was unavailable; the fixture uses the retained harness source producer and records that limitation. No receipts or history were fabricated; outbox capture occurs before ACK, and canonical state is adopted only from the held accepted response.

Commit message written and `DONE` created.