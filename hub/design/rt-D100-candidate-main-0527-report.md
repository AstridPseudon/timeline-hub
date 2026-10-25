## Report

- Prepared exact Agent baseline `6aefd11766` and candidate `d3b5cfef76` with Runtime `0c62dfa6`, App `1e34f8ea`, Composition `635f4de0`.
- Central old-RED: `14 failed, 12 passed` using both reviewed new regression files on the true baseline.
- Central candidate GREEN: `16 failed, 38 passed, 5 errors`.
  - Failures included `source_offset` authoring rejection, `at_ms` Fraction handling, Runtime `internal timeline scope mismatch`, and inverse materialization/text-binding refusals.
- Positive/poison controls passed: exits `17` and `1`.
- Registry was CAS-restored to `4fbde9…`; a later unrelated worker appended its own row, which I preserved.
- Runtime worktree remains clean; no source/test/product changes made. No local body or collection tests run.
- Evidence: ~1.2 MB in the worker evidence directory.
- Wrote commit message and `BLOCKED` marker. D100 does not qualify for merge or D72 fixture entry.