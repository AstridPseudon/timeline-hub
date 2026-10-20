# Runtime door audit failure triage

## Classification

The additional `full16608` failure is an inherited response-before-audit timing race, not a product regression.

- Current Runtime: `7f6dd8920e1ceec41b137358df5e7fecc304888d` (tree `4cccb2d6`).
- Exact main comparison: `29d0954b6d78a7d7937d81bc36567b6dee7ca976`.
- Last full comparison: `129493b2aff614560d9b7ac2577957e799cf30ec`.
- Before this change, `tests/test_door_transport.py` was identical at all three refs.
- `runtime_protocol/door.py` has no diff between `129493b` and current. The exact-main diff contains only route-table additions; the audit implementation is unchanged.

In `runtime_protocol/door.py`, `_door()` sends the route response through `_dispatch()` and calls `_audit()` in its `finally` block (lines 511–520). `_audit()` appends the JSONL record afterward (lines 674–688). The client can therefore finish `response.read()` before the handler's audit append. The pre-change central run reproduced the failure on the current tree: `rt-m2-door-audit-race-triage-targeted-1020142315-2933`, `1 failed, 5 passed`; the target failed with two JSONL entries and `ValueError: not enough values to unpack (expected 3, got 2)`. Historical targeted/full logs show the same node before this work.

## Change

`tests/test_door_transport.py` now uses `_read_complete_audit_lines(audit, 3)`. It polls for at most one second in 10 ms intervals, returning once three newline-terminated JSONL entries exist. It does not slice or discard entries:

- Missing entries remain fewer than three after the bound and still fail at the existing three-way unpack.
- Extra entries are returned and still fail at the existing three-way unpack.
- Corrupt complete lines are passed to `json.loads` and still fail immediately; an incomplete final line is parsed at the bound and fails likewise.
- All existing credential-absence, field-set, status, path, byte-count, origin, and token assertions remain unchanged.

No Runtime product code, auth/origin/token policy, audit schema, endpoint, or fixed long sleep was changed.

## Evidence

Central targeted run after the change:

```text
request: rt-m2-door-audit-race-triage-targeted-1020142429-156
tree snapshot: 6a6ba82cb05200bb822669c19fab2aed40a73076
command: pytest -q tests/test_door_transport.py::test_audit_lines_without_credentials \
  tests/test_door_transport.py::test_admission_order_host_origin_and_route \
  tests/test_door_transport.py::test_allowed_health_read_and_response_headers \
  tests/test_door_transport.py::test_object_reads_range_head_and_caching \
  tests/test_door_transport.py::test_preflight_refuses_repeated_request_headers_and_browser_credentials
result: 6 passed in 8.33s
```

The required direct local socket run was attempted but is blocked by the sandbox with `PermissionError: [Errno 1] Operation not permitted`; the central socket run above is the transport evidence.

## Commit diff

One test file changed: 19 added lines and 1 replacement in `tests/test_door_transport.py`. No full suite was requested or run.
