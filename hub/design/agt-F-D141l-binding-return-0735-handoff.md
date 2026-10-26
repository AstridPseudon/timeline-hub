# D141l handoff

The delivered packet is owned at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-return-0735/evidence/
```

`controller-continuation.sh dispatch OUTPUT_DIR` is the later real action.
At that invocation it records one disk witness at 4,714,564,096 bytes,
serially CASes the existing `agent-core-full` row, calls the existing
`bin/request-test integration:agent agent-core-full --no-cache`, takes the
actual returned result-directory ID and request bytes, writes an immutable
brief and dispatch receipt, then calls the existing `bin/test-run ID` and
`bin/wait-test ID 100`. The per-phase row is restored only after the terminal
result. The current old row is untouched during source preparation.

The service floor is preserved: `bin/test-run` classifies `agent-core-full`
as heavy with its 4,700,000,000-byte service floor; the controller's recorded
D89d floor is 4,714,564,096 bytes. The two phases share the existing one-heavy
route and do not lower that service floor or add a kit/interface. Continuous
command monitoring retains the 5-second cadence and 4,000,000,000-byte stop.

The request consumer authenticates the genuine test-service request fields
(`target`, `repo`, `suite`, `files`, `nocache`, `requested`) and the returned
directory ID. It does not validate or invent the Runtime commit-v2 payload;
that remains the unchanged Runtime `commitTimeline`/provider caller. The
receipt binds request bytes, native registered row, command manifest,
distinct source manifest, current/pristine tuple, brief, and later terminal
result. A receipt is produced only after the real future request returns, and
the terminal result is separate, so there is no request-ID/row/admission hash
cycle or placeholder ID.

The source-only checker exercises the same producer/consumer functions with
private tiny doubles and labels them isolated; those artifacts cannot qualify
live admission. The live 0309/0249 row and the historical 0638/0707 reports
remain disclosed, not promoted. The final App input is the authenticated
82e9e13ddf1d7ec6c736521b2eb091dca9877598/tree6a6e49eb4461b5ca1a7fa1247653bc794f26d710;
the retained 0545 App receipt remains historical 4de, and the 0734 final
catch-up receipt is bound separately.
