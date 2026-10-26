# F D141z native whole-path findings

## Verdict

FAIL remains controlling. F1 is a finite App-venue receiving-input gap. F5 is
an intrinsic candidate lifecycle gap: the candidate is not mounted under the
qualified normal dispatcher cancellation/parent-death/control-pipe contract.
Its local process-group stop/reap is real source behavior, but the outer local
supervision does not cover the missing inner semantics.

## F1 — exact missing inputs, not proof of Runtime-main absence

`run-final-delivery.py:25-35,232-235` retains exact path/hash guards for the
Runtime core runner, inventory, and canonical D68 wrapper. At this App venue,
the three exact coordinates are absent; the SAFE0812 D68 copy exists only under
`design/` and is not a canonical install. This prevents genuine Runtime
caller/readback qualification, but does not establish that Runtime `main()` is
absent. Runtime peer0857 owns genuine readback/publication. No replacement was
fabricated.

## F2 — source/control PASS

The candidate parses the seven-field sampler binding and binds physical parents
with `O_NOFOLLOW` (`delivery_lifecycle.py:92-156`), retains the trace descriptor
and checks identity on every read (`:159-197`), then delegates terminal append
and validation through the donor helper (`:200-219,406-413`). The unchanged
acceptance's pathname-replacement case is retained. This is source/control
evidence only, not a production-install claim.

## F3 — no private admission, but ownership is not proved

The candidate source no longer carries the prior private flock or second local
dispatch gate. `install-map.json:10-15` records external normal-dispatcher
one-heavy ownership and the 4.86-GB external floor. The map is metadata and the
candidate does not invoke/authenticate `test-run`; it cannot prove that real
heavy ownership was mounted. This is an operational qualification gap, not a
new private lock.

## F4 — bounded route control only

`check.sh:61-65` calls `candidate.main()` with four harmless Git fixtures and
the SAFE D68 wrapper fixture, and checks the builder mark/receipt. The candidate
main path checks the genuine Runtime runner/inventory/wrapper/builder before it
constructs the D68 command (`run-final-delivery.py:213-245`). The D68 wrapper
stages repositories and calls `main_with_args`/`main` in-process
(`design/runtime-D141z-input-0812-delivery_gate_build.py:308-328` and
`:249-285`). This establishes the bounded source route, not a live normal
dispatcher or production delivery build.

## F5 — intrinsic missing mounted cancellation and parent control

The qualified `56f2` private normal service has one-heavy admission, heavy
markers, floor checks and body ownership (`privateops-d141-measured-floor/bin/test-run:19-59`);
mounted `D/CANCELLED` and bench-store lease ownership (`:123-159`);
`PR_SET_CHILD_SUBREAPER`, `PR_SET_PDEATHSIG`, and initial/repeated
`os.getppid()` checks (`:161-181,224-249`); an `O_CLOEXEC|O_NONBLOCK` control
pipe, `BENCH_CONTROL_FD`, advertised process groups, EOF/FD lifetime, TERM/KILL,
`waitpid`, and cancellation/timeout ownership (`:186-249,285-290`); and final
trace custody before terminal status and marker release (`:294-310`).

The candidate has only local signal handlers and optional local
`cancel_path.exists()` (`delivery_lifecycle.py:283-288,369-375`), enables child
subreaping only (`:291`), and starts the D68 process locally (`:320-323`). Its
`/proc` descendant census and local group TERM/KILL/reap (`:334-391`, `_reap`
at `:71-79`) do not implement the donor's mounted `CANCELLED`,
`BENCH_CONTROL_FD`/EOF, or parent-death contract. There is no
`PR_SET_PDEATHSIG` or `os.getppid()` seam. The local early-leader, local
cancel-file, and orphan controls in `check.sh:77-102` cannot qualify the
installed production stop surface.

## Full route and historical controls

The concrete normal route is dispatcher `test-run` admission → existing heavy
body/lease and cancellation supervisor → delivery caller → D68 staging wrapper
→ builder. Within the candidate source, the delivery caller is
`run-final-delivery.py:213-245`, lifecycle delegation is `:171-201`, D68 is
`delivery_gate_build.py:308-328`, and builder execution is `:249-285`.
The candidate route is nested beneath the normal dispatcher only if Runtime
actually mounts it; the candidate itself does not supply that supervision.

The 0741 record is an interrupted/stopped invocation: the stop receipt names
PIDs 3209 and 3191, raw stdout contains only partial Agent (29s) and Runtime
(7s) PASS lines, and App/Composition result, raw CLI exit, report/DONE, and
host reaping remain unknown. A harness exit 0 is not a delivery-build PASS.
The candidate's harmless normal/main fixture is a bounded control and must not
be rewritten into evidence of a normal 0741 production exit.

F6 is exact: base-to-candidate contains four declared source modifications and
only the two authorized tracked CPython 3.13 bytecode deletions. C0 request and
reply examples were read through accepted/merged/conflict/invalid/preview;
no wire/schema/payload-validator change is in scope.
