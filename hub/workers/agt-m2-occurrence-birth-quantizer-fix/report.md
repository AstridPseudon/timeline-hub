Implemented the P2 fix.

- Quantizer `ValueError`/`OverflowError` now maps to permanent `unsupported_timing`, matching `move`.
- Added capture and real Runtime no-write/history regressions for `on=1e308`.
- No schema, Runtime source, writer, or cap changes.

Tests:

- Birth/duplicate/delete: 87 passed.
- Real Runtime lifecycle: 2 passed.
- Typed-ID/media/placement neighbors: 140 passed.
- `git diff --check`: passed.
- Ruff unavailable: `No module named ruff`.
- No full suite run.

Commit message and detailed report written; `DONE` created. Next step: manager review before cohort/schema join.