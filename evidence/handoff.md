# F D141l handoff

Status: `WAITING_FOR_GENUINE_CONTROLLER_BINDING`.

The finite seam is now executable at the source boundary: a future controller
receipt and normal request/service/brief materialization can be consumed by one
owned command without changing the reviewed commands or inventing an
admission. The packet is not `READY` for the real pair because no current
service ID, request, receipt or installable row exists yet.

The exact unsupported/stale producer boundary is the live suite registration
at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`:

- line 31 still invokes the old 0309 measurement command with the fixed 0249
  receipt/brief and terminal service `agent-agent-core-full-1026025151-24049`;
- line 188 still points at the old 0030-era pristine comparator route.

The consumers are the existing `bin/request-test` request/queue path and
`bin/test-run` row/snapshot/receipt path. This worker did not alter either.
The old 0249 record is a genuine terminal refusal and is rejected by the new
consumer as current admission. The next controller action is therefore to
create the real current request/service binding once at 4,714,564,096 bytes,
then run `controller-continuation.sh materialize` and only afterward dispatch
the existing recipes one heavy at a time.

Preserved: current Agent/Runtime/App/Composition tuple, pristine Agent/Runtime
tuple, 22 cut roots, 17 pristine roots and source-backed absent-pristine N/A
roots; original receipts 26496/27388/10086; KEEP/raw/JUnit custody controls;
the historical trace gap; old 19479/8912 held unstarted; D89d floor arithmetic;
and the no-product-change boundary.
