## D39 report

- Audited the pinned fixture/lock and production path at base `2c55d0ed89`.
- Generated client and fixture hashes match `runtime.lock.json`.
- Production path is wired: `RemoteTimelines.commit` → `WorkspaceClient.commit_timeline` → generated `commit_timeline` → `_request`.

Findings:

1. Missing transmitted-key assertion: `tests/sdk/test_runtime_response_conformance.py:112-144` captures only `(method, path, body)`. The transport receives headers, and generated `commit_timeline` sends `Idempotency-Key`, but the helper never records or asserts it.

2. The conflict reply’s status, code, request ID, and complete `details` are asserted. The outer error `message` and fixture response headers are not asserted.

3. The fixture request is not a full C0 request: it omits `steps`, `reads`, `dry_run`, `source`, `rationale`, and `group_id`. Exact body equality proves only the fields present in the fixture.

4. Existing accepted/preview and public-commit tests use mocked/in-process clients; they do not observe actual HTTP headers or generated-client response parsing.

No product, fixture, generated-client, or test changes made. Retired-route 410 coverage remains untouched. No tests run per the read-only/source-inspection brief; `git diff --check` passed. Commit message and `DONE` sentinel were prepared.