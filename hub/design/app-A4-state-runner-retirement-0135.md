## Report

Implemented A4 state-runner retirement.

- Removed `useTimelineState`’s `editorCommandRunner`, `validate`, `dryRun`, and `apply` APIs.
- Retained media add/swap builders and independent runner consumers.
- Updated state types and pre-sync store defaults.
- Changed only 3 assigned files; provider/staging tests, history, media, and runner remain untouched.

Validation:

- Targeted current-base suite: 9 files, 175/175 passed.
- Reviewed `40bcff` private-overlay mounted persistence fixture: 6/6 passed.
- Root/App/Node TypeScript checks: passed.
- Scoped ESLint (`--max-warnings 0`): passed.
- `git diff --check`: passed.

The current base’s original mounted fixture had 6 expected failures due missing Runtime `MediaSelection` fields; the reviewed overlay resolves them.

Remaining runner edges: history undo/redo, media helper internals, public exports, and runner/media tests. No full/browser suite run.

Commit message and `DONE` marker created as required.