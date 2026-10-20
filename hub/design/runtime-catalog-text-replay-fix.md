# Runtime catalog text replay fix

## Source and test counts

- Source diff: `runtime_protocol/service.py`, 56 insertions / 25 deletions.
- Test diff: `tests/test_shot_text_bindings.py`, 62 insertions / 0 deletions.
- Changed files: 2.
- Final central targeted result: 190 passed in 134.41s.

## Change

Both `set_project_shot_text_binding` and `rebind_project_shot_text_binding`
derive the immutable project-scoped binding identity and request hash before
resolving or checking mutable binding state. Exact receipts therefore replay
before stale-head, placement, binding-integrity, or candidate-media checks;
project lookup/authentication and changed-payload idempotency refusal remain.
New requests retain the existing CAS, event, MIME, scope, and compare-and-set
guards. Friendly nonzero-head selectors retain their existing resolved natural
identity before recording.

One control covers set A, later rebind B, restart, and exact A retry. It checks
the same receipt, unchanged head/resource, unchanged binding events, and
unchanged CAS bytes; the live binding resolver is fenced in the retry.

## Evidence

Final central targeted command:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_shot_text_bindings.py tests/test_timeline_shot_authority.py tests/test_timeline_text_selection.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_legacy_custody.py tests/test_timeline_verified_media_http.py
=> 190 passed in 134.41s (0:02:14)
```

Local checks:

```text
/home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/service.py tests/test_shot_text_bindings.py
=> passed

Direct RuntimeService set/replay/restart, rebind/replay/restart, and friendly-selector probes
=> passed
```

The same pytest command was attempted locally; 119 non-socket tests passed,
while 70 daemon/HTTP cases errored because this sandbox denies socket creation
(`PermissionError: [Errno 1] Operation not permitted`). The central run above
is the authoritative result. No full suite was run.

The requested input path `design/runtime-catalog-text-replay-fix.md` did not
exist before this report; the supplied final-review document and settled plan
were used as the source of truth.

No merge, pin, publication, DTO, endpoint, table, writer bypass, or catalog
framework work was performed. The existing catalog-promotion/composition
changes were left untouched.
