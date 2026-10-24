Implemented **U4a-D39-idempotency**. Only [test_runtime_response_conformance.py](/home/user/work/wt/agt-D39-idempotency-sol-0801/tests/sdk/test_runtime_response_conformance.py:111) changed: optional per-client capture copies actual transport headers, preserving existing call tuples and helper behavior.

The production path now proves:

```text
WorkspaceClient.commit_timeline → generated client → transport
POST /v1/projects/project-1/timelines/main/commit
Idempotency-Key: commit-conflict-409
```

Removing the wire header fails with `KeyError`; replacing it with `wrong-wire-key` fails the exact equality assertion. Both controls reach that assertion after existing request/error checks pass.

All **18 conformance scenarios** remain, with this cumulative property inventory:

| Scenario | Preserved assertions |
|---|---|
| Shape comparator | Missing, extra, retyped, optional and free-form members |
| Fixture census | Exact nine recorded cases |
| Task admission | Success, task ID/state, receipt kind, recorded request |
| Task read | Task ID/state/capability, recorded request |
| Events page 1 | Success, cursor, sequences, aggregate IDs, GET route |
| Events page 2 | Same properties, null terminal cursor |
| Managed outputs | Pagination, association, lifecycle, producer, request |
| Not found | Error code, exception class, request |
| Validation error | Code, message, exception class, POST route |
| Canonical conflict | 409/code, complete details, request ID, exception class, exact method/path/body; **exact wire key added** |
| Invalid cursor | Status, code, message, generic error mapping |
| Thumbnail admission fake | Recorded response shape |
| Thumbnail task fake | Recorded response shape |
| Activation task fake | Recorded response shape |
| Managed-output listing fake | Recorded response shape |
| Managed-output task fake | Recorded response shape |
| Journey admission | Recorded status and shape |
| Journey task read | Recorded status and shape |

The neighboring **9 contract cases** preserve accepted envelope/key forwarding, preview null receipt, explicit view key, history page, typed 409 and 503 details, actionable absent-method error, remote scope/key/history forwarding, and body-scope rejection.

Validation commands and results:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-becfe6db" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp="$TMPDIR/pytest-contract" tests/sdk/test_runtime_response_conformance.py tests/sdk/test_workspace_client_timeline_commit.py
```

**27 passed in 0.86s.** One earlier invocation stopped before collection because `runtime_protocol` was absent from `PYTHONPATH`; using the existing pinned checkout resolved it without dependency changes.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-becfe6db" /home/user/work/venv-agent/bin/python "$TMPDIR/wire_controls.py"
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$TMPDIR/preservation_check.py"
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/sdk/test_runtime_response_conformance.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-becfe6db
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

All passed. Preservation checks verified compilation, every previous assertion, unchanged original test bodies except the established publish→commit conflict migration, and **15/15 byte matches** against Runtime `becfe6db88b2cc034dba3fafa6c050117cdf2b06`. The original `publish_conflict_409` fixture still maps to canonical `commit_conflict_409`.

Full v2 request/reply DTOs, durable receipts, and retired-410 contracts remain unchanged. Richer accepted/merged/undo behavior was not independently executed by this bounded repair. No full, browser, live-socket, or gate runs occurred.

No blockers. Commit message and `DONE` marker are written; no Git writes or deletions occurred. Next step: independent read-only review, then harness commit.