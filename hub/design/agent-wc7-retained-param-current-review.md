# WC7 selected-PARAM retained-original-pin review

Date: 2026-10-20T23:54:16Z

Verdict: **APPROVE** for the bounded new attached selected-PARAM case. The
candidate source introduces no new resolver, public API, Runtime route, DTO,
history store, or authority mechanism. The attached adapter calls the existing
WC4 selected-authority reader and persists its exact source pin in the normal
outbox command.

## Reviewed source

Candidate Agent is `e499bb604` (`tl/agt-m2-wc7-retained-param-local-capture`).
The product delta is limited to:

- `astrid/sdk/timeline/native_checkout.py`: attached pending-bundle materialization,
  selected `.set()`, publishability, and reload/retry handling;
- `astrid/sdk/timeline_elements.py`: the internal retained-input reader;
- `astrid/sdk/timeline/checkout.py`: documentation of the existing attached
  publish boundary.

The new reader delegates source selection to the pre-existing
`astrid.sdk.timeline._selected_param_authority.resolve_selected_param_source`
and obtains the exact verified document/object through the existing Runtime
read operations. It does not introduce a competing resolver or caller-owned
schema authority.

## Qualification

Added one central HTTP/provider case in
`tests/sdk/test_timeline_selected_schema_runtime.py`:
`test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart`.
Its setup uses `ASTRID_RUNTIME_CHECKOUT` (defaulting only when absent) to select
the existing `/home/user/work/runtime`, `real_runtime`, the real authenticated
`AstridClient.open` client, `TimelineSession`, and `Checkout.attach`. Pack
admission uses the real HTTP document/media client. The selected element and
PARAM acceptance/refusal use the normal Agent command factory and Runtime
commit provider; no fake provider, fake history, inline schema, old pin, or
skipped/xfail assertion is involved.

The case proves:

- P1 is the exact last accepted selection pin and is present in the queued
  command; `.set(seed=8)` does not commit immediately;
- the durable outbox contains the rationale, exact body, and idempotency key
  after a deliberately lost acknowledgement;
- P2/max20 admission, removal of current admissions, local source/artifact
  deletion, Runtime restart, and reattached reload do not replace P1 bytes;
- retry sends the exact original body/key and accepts once;
- raw `seed=16` is refused by the actual HTTP/provider path under retained
  P1/max10;
- inverse/undo restores the original row.

Existing focused neighboring coverage remains unchanged for mixed pending
intent and detached/global outbox isolation. The original same-alias HOLD
case remains untouched.

## Evidence

Final central run on the exact final tree:

```text
gate3-agent-current-integration with
tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart
28 passed in 30.55s
```

The named integration lane included the new real HTTP/provider case and its
existing focused integration neighbors. A prior central attempt exposed only
an incomplete test fixture (timeline shell without a parent head); the fixture
was repaired to publish the ordinary empty baseline through Runtime before
pack setup, then the final run passed.

Local checks:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ... pytest ... test_native_retained_schema_replay_inverse_reload_and_exact_retry
1 passed in 2.21s

... pytest ... test_unrelated_and_detached_publish_never_consume_global_pending_or_flight
1 passed in 1.20s

ruff check --no-cache tests/sdk/test_timeline_selected_schema_runtime.py
All checks passed!

git diff --check
passed
```

The new HTTP test was not run locally because this worker sandbox forbids
localhost sockets; it was run centrally as above. No full or full-* suite was
requested. No product source was changed by this review; only test setup and
qualification coverage were added.

## Decision and next step

Approve this bounded source slice and its new actual retained-original-pin
case. Do not infer broader App/browser or full-suite qualification from this
review; those remain separate gates.
