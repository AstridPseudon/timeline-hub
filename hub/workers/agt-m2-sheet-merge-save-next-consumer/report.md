## Report

Implemented AG03 CLI cutover:

- `timelines apply` now always uses retained `NativeSheet` + `TimelineSession`.
- Removed detached `apply_sheet`/local merge/`Checkout.save` writer path.
- Legacy parsing remains available for read/preview callers.
- Unbound legacy sheets visibly refuse while preserving edited text.
- Added unit and Runtime HTTP coverage.

Tests:

- Native targeted suite: **72 passed**
- Runtime HTTP lane: **9 passed**
- Ruff on touched tests: passed
- `git diff --check`: passed
- Full conformance was not run. Diagnostic conformance showed legacy unsupported grammar remains OPEN: 2056 passed, 46 failed.

The manager-owned AG03 ledger remains `in-progress`, not deleted. Commit message, report, and `DONE` marker were written.