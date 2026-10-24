## Report

- Added only the approved A4 witness support pair, changing worker/output paths and qualified source constants. Function-body and non-constant source comparisons passed.
- Live App output was accepted by Runtime:
  - Input SHA: `d6f4ca73…`
  - Output SHA: `d4b3cf78…`
  - Receipt: `txn-418b6223d071463c9d673b737b9ba566`
  - Exact retry: passed.
- Witness stopped at the existing `parent.foreign_pin()` helper with `KeyError: 'attempt_id'` at `test_commit_runtime_parent_media.py:303`. Foreign/changed-key no-write, inverse, reopen, and final-result assertions are explicitly recorded as not run. Evidence is preserved under the worker evidence directory.
- Production path identified: `useMountedCommands().commands.addClip` → `useTimelineSave.applyEdit` → local save/outbox → `RuntimeDataProvider.commitTimeline` → generated Runtime client.

Checks:

- Targeted witness test: `1 passed` (one existing unknown-mark warning).
- Ruff, private mypy, py_compile, vendor lock, artifact manifest, and `git diff --check`: passed.
- No product/App/Runtime changes; no full suite run.

`BLOCKED` marker and commit message were written.