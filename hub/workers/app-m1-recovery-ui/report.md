## Done

- Added `TimelineCommandRecovery` with:
  - Explicit owner recovery only.
  - Exact `data-owner-id` selectors.
  - `Recover saved edits` / ordinal session labels.
  - `Retry exact request`.
  - Busy/error handling and retained-work messaging.
  - Distinct conflict vs transport/lock/storage states.
- Mounted it in `TimelineEditorShellCore`.
- Added component and shell interaction tests.
- Published the selector/label seam in `app-m1-coordination.md`.
- Wrote the harness commit message.

## Tests

- Targeted Vitest: **100 passed**
- File-scoped ESLint: **passed**
- `git diff --check`: **passed**
- Typecheck attempted; four pre-existing errors remain in unrelated Runtime/data-provider/AgentChat files.

## Blocked / next steps

Browser/full journey remains unverified per orchestration rules. When editor wiring merges, keep this component as the sole recovery UI and remove/avoid its provisional inline banner to prevent duplicate controls.