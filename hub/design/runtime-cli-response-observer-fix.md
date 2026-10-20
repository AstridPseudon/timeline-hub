# Runtime CLI response observer fix

Date: 2026-10-20 UTC

## Change

`tests/test_timeline_public_s2_mixed_cli_journey.py` now observes a timeline
commit only when `RuntimeHandler._send` is performing the post-dispatch socket
write (`_defer_response` is false). Runtime stages the response during
`_route` and flushes it afterward, so the old deferred-only predicate observed
no final response and raised `StopIteration` before reporting the real result.

The observer keeps the existing raw prefetched body, path, idempotency key and
status. For Runtime refusals it records `kwargs["error"]`, which is the payload
that `_send` serializes when `payload` is `None`; accepted responses continue
to use the original payload. The lost-ACK injection remains on the accepted
final-send path and still raises before socket bytes reach the SDK.

## Bounded proof

The unchanged journey now proves, over the real Runtime door:

- one accepted peer commit is attributed by its own idempotency key and path,
  with the wire `data`/`receipt` matching the SDK result;
- one stale label commit is sent with a distinct key and the original base,
  returns HTTP 409, records exactly one final observer row with the exact raw
  body/path/key/status, exposes `conflict` / `dependency_changed`, and leaves
  the durable store unchanged;
- the original CLI trim request remains attributed by its own key and retains
  the existing exact body/path/key/count and lost-ACK/restart/retry/undo/source/
  film/response assertions.

No fixture or product source changed. No auth, schema, health route, synthetic
success, or alternate writer was introduced.

## Evidence

Final central socket-capable run:

```text
capture-legacy-integration --files tests/test_timeline_public_s2_mixed_cli_journey.py --no-cache
1 passed, 1 xfailed in 15.28s
```

The xfail is the pre-existing historical-audio capture gap. The final run used
the mutable current Agent checkout. The frozen f97 tuple remains separately
reported as an actual HTTP 409 `dependency_changed` caused by Agent's
over-broad track read; this Runtime test observer change does not make that
tuple green or alter that guard.

Static checks also passed:

```text
git diff --check
AST parse of tests/test_timeline_public_s2_mixed_cli_journey.py
```

No full suite was run or requested.

Exact final observer evidence: service run rt-m2-real-cli-response-observer-capture-legacy-integration-1020180747-17219 froze Runtime tree2dfb32a211d84b220f577efa1454f7fa0e6ad94f, equal committed18d0d62d tree. Its recorded external Agent source was3f770a45769361a17fe2c350cd5f54db9231a898. This is not the separate frozen f97/7d original failed-node pair, and it does not qualify historical media.
