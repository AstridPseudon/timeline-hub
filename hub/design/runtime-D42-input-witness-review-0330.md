## PASS — D42 input-witness review

- Verified `42080f33d` against `36760ee0a`.
- Production diff: none.
- Only changed path: `tests/test_timeline_history_memo_inputs.py`.
- Seven witnesses confirm unchanged accepted row bytes/digest do not authorize changed:
  - source closure, even with recomputed digest;
  - event-prefix hash;
  - project sequence.
- Exact retries wrap the verifier’s `ProtocolError` as `CommitOutcomeUnknown`, preserving the cause.
- Single-byte `records_json` mutation is refused repeatedly.
- History and retry paths perform no writes.

Tests:

```text
22 passed in 4.58s
ruff check tests/test_timeline_history_memo_inputs.py: passed
git diff --check: passed
pyright tests/test_timeline_history_memo_inputs.py: 0 errors
```

The requested C0 behavior remains untouched; no full/145/browser/provider suite was run. The assigned `tmpdir` was unexpectedly a regular file, so pytest used `/tmp/w-d216899617/memo-tests`.

No blockers. Completion marker and commit message were recorded.