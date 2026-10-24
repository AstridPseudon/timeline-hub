Implemented the attachment in two new files only:

- `tests/helpers/run_wc6_completion_capture.py`
- `tests/sdk/test_wc6_completion_capture_runner.py`

The runner preserves pinned Agent/Runtime guards, exact original selector, 45s pytest budget, authenticated helper hash/origin, and bounded byte-exact JSONL retention through service logs. Missing/partial packets remain explicit.

Tests:

```text
20 passed
Ruff passed
mypy passed
git diff --check passed
```

Exact test command included the reviewed 19 controls plus the new offline test, with XML retained at:

`/tmp/w-09e7c3de01/agt-F-ABA-capture-attach-1004.xml`

No original ABA body, registry, existing helper/test, production code, or managed row was modified. No live/original execution or installation was performed.

Candidate row and owner-controlled retention/install input are ready for independent review; live durable receipt/history remains unverified.