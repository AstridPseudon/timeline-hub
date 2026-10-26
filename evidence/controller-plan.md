# F D141l existing-controller binding continuation

## Result

This packet is source/control-ready and remains explicitly waiting for the
genuine current controller binding. It does not claim executable qualification,
admission, body, REG0, gate, or ship credit.

The manager's 2026-10-26T07:17:49.555834+00:00 witness records 4,512,456,704
free bytes against the 4,500,000,000 source-only floor. The later controller
must perform the single normal `request-test`/`test-run` route at the recorded
D89d floor 4,714,564,096, then hand this packet the exact receipt, request,
service rows, owner brief, current tuple, command hashes and distinct manifest
hashes.

## Continuation

1. The existing controller calls `bin/request-test` and `bin/test-run` using
   the existing `agent-core-full` route. This packet does not call either.
2. The controller passes its real materialized binding path to
   `controller-continuation.sh materialize BINDING OUTPUT_DIR`.
3. `binding-source.py` verifies exact absolute paths and bytes for the request,
   cut/pristine service rows, controller receipt and brief; service ID and
   dispatch witness; integrated/pristine source tuples; command hashes; and
   separate command/source-manifest hashes.
4. The continuation writes two native rows and `readiness.json` only under the
   private `OUTPUT_DIR`. It never edits `tests/suites.conf`, submits a request,
   polls a service, or starts a body.
5. The eventual rows invoke the unchanged cut/pristine recipes. Each recipe
   consumes the same binding once before source-admission disk sampling, then
   preserves source, body, monitor, raw/JUnit, KEEP, status and final custody.

The exact expected native row shape is emitted only after validation:

```text
agent agent-core-full /bin/bash <owned command-cut.sh> <receipt> <brief>
agent d141b-pristine-comparator-2358 /bin/bash <owned command-pristine.sh> <receipt> <brief>
```

The current `rows.txt` is intentionally a non-installed template. The old
0309/0249 row remains an immutable disclosed route fact and is never promoted
to current admission.

## Controls retained

The recipes keep `-q -n3 -o addopts= -p no:cacheprovider --timeout=45`, the
existing D73 tiny positive exit 17/call 1 and Agent-SHA-only poison exit 1/call
0, one-heavy lock, continuous 5-second/4,000,000,000-byte stop, and one-time
4,714,564,096-byte controller floor. No preparation re-gate is added.
