**BLOCKED at the D42 input seam; no production memo implemented.** Returned early as permitted by the brief.

Base: Runtime `36760ee0ad4b064a849edb3fc6e5a60a43fe8f48`, tree `11389911c2eec5acc901ab3b70e234fad9e1bc5d`.

Added [seven independent regression tests](/home/user/work/wt/rt-R-D42-history-memo-sol-0322/tests/test_timeline_history_memo_inputs.py). They demonstrate that identical accepted receipt/history rows—and identical SHA-256—still require refusal after external event-prefix, project-sequence, or source corruption, through history reads and exact retries.

The source witness changes its payload and recomputes its digest: `revision_closure` passes, while accepted replay correctly refuses. Thus, authenticating a self-consistent closure is insufficient before skipping replay.

The precise seam is `_verify_accepted`’s live `source`, `original`, continuations, and inverse-history inputs at lines 248–269, plus event-prefix/project-sequence checks at lines 270–295. Accepted canonical/receipt/record bytes do not contain that complete input set. A whole-verifier hit based solely on those bytes would suppress existing checks. This does **not** establish that a narrower memo is impossible.

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
/home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
--basetemp=/tmp/w-5fa30eca12/memo-input-tests-final \
tests/test_timeline_history_memo_inputs.py
```

**7 passed in 2.36s.** Includes single-byte record mutation, repeated refusal, and no-write assertions.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
/home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
--basetemp=/tmp/w-5fa30eca12/history-neighbor-tests \
tests/test_timeline_history_authenticated_read.py
```

**15 passed in 4.87s.**

- `ruff check tests/test_timeline_history_memo_inputs.py`: passed.
- `git diff --check` and new-file `git diff --no-index --check`: passed.
- Initial new-test run: 4 passed, 3 failed because retries wrap corruption in `CommitOutcomeUnknown`; corrected the new tests to assert its `ProtocolError` cause.
- Production code, existing tests, server guards, mutex, and all 61 protected contract/schema/client files remain byte-identical. Protected path/hash manifest SHA-256: `e77bac6ca17865c19ac92a23e4d7d69e59e69bca540702531d1cf370ed5f1ead`.

No 145-lane, inverse-stage lane, Pyright, timing, browser, or full-suite run was performed after taking the early-return path. No warm-read savings, version-miss behavior, bounded memo, or D42 readiness claim is made. Prior `079` transcript-failure evidence remains unchanged.

Next: independently review these witnesses and establish the authenticated replay-input boundary before implementing reuse. Commit message and `BLOCKED` marker are written; no Git writes or deletions.