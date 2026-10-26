# F D141l binding review — FAIL

Reviewed commit `6a2d1c22ec800229812f4d756d7198aece8111ed` in the original author worktree. No source or product repair was made.

## F-D141L-BIND-001 — blocking: delivery is at the wrong coordinates

The required directory
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-controller-binding-prep-0718/evidence`
contains only `manager-disk-trace.txt`. The committed files are instead under
`/home/user/work/wt/agt-F-D141l-controller-binding-prep-0718/evidence`.
This is the exact path clarification the author brief required. The source
scripts also hardcode the author worktree path (`command-*.sh:8`,
`tiny-controls.sh:3`) and the continuation hardcodes the absent ORCH author
evidence path (`controller-continuation.sh:7`). Therefore the required
delivered packet is not runnable from its required location.

## F-D141L-BIND-002 — blocking: no production binding producer exists

`controller-continuation.sh:32-79` accepts an externally supplied
`BINDING.json`; it never invokes `bin/request-test`, `bin/test-run`, or
`wait-test`, and only writes private `MATERIALIZED_NOT_INSTALLED` rows. The
only production steps named in `controller-plan.md:1-24` are prose saying that
an undefined future controller will supply the JSON. `rows.txt:1-17` is
explicitly a non-installed template. This is a consumer for a future artifact,
not a concrete runnable continuation that generates the current request,
service ID, receipt, brief, row and tuple through the existing route.

The existing route confirms the gap: `request-test` validates the suite row,
writes `tests/<id>/request`, and queues `pending/test-<id>`; `test-run` resolves
the already registered `suites.conf` command, snapshots the tree, optionally
validates a measured-floor receipt, and writes status/exit/log. Neither script
emits the binding JSON consumed here, nor does this packet connect a returned
ID to a current service row and receipt producer.

## F-D141L-BIND-003 — blocking: the binding consumer is not authenticated

`binding-source.py:91-125` validates an arbitrary JSON file and ordinary file
hashes, but does not verify the full v2 request body or its canonical hash,
`api_version`, scope/base IDs, command envelope, label/steps, merge/reads,
idempotency key, or request/receipt association. It only requires that the
declared `request_id` occur somewhere in the request bytes (`:103-105`).

It also does not bind the receipt to the request ID, the service row to the
actual test-run service/result directory, or the owner brief to the same
controller invocation. `record["service_id"]` and the dispatch/admission
fields are trusted as self-contained JSON claims (`:111-123`). The service
row is checked only against the same caller-provided binding (`:70-87`), so a
caller that manufactures a consistent JSON/row/receipt/brief set can pass.
`source_tuple` checks only manifest literals (`:57-67`), not an authenticated
producer binding to the dispatch.

This fails the contract's real receipt producer and complete ordering
requirement. Fixture positives do not authorize admission, and no guessed
receipt or service ID can be accepted.

## F-D141L-BIND-004 — blocking: production remains on the stale route

The live registration at `orch/tests/suites.conf:31` remains:

```text
agent agent-core-full /bin/bash .../agt-F-D141i-terminal-floor-return-sol-0309/evidence/measurement-command.sh .../agt-F-D141i-cut-controller-0249/evidence/admission.json .../agt-F-D141i-cut-controller-0249/brief.md
```

The pristine registration at line 188 is also the old 0030-era comparator.
`source-manifest.json:205-206` records those same legacy rows as
`production_rows`, and `check-source.py:433-438` asserts that the old bytes
remain. The new packet's rows are not registered, installed, or reachable by
the normal caller. The old 0249 receipt is a genuine terminal refusal and is
not a current admission witness. The packet correctly says it is waiting, but
that means the requested existing-controller continuation is not complete.

## F-D141L-BIND-005 — blocking: claimed checker coverage misses the real seam

The exact author check passed:

```text
control_status=PASS pair_status=WAITING_FOR_GENUINE_CONTROLLER_BINDING admission_cases=10 lifecycle_cases=36
```

However, `check-source.py:433-475` never calls its own `admitted_dispatch`.
The 10 admission cases are created as isolated fixtures at `:270-349` and
invoke `binding-source.py fixture`, which explicitly enables fixture use. The
real `check-source.py admission` path at `:482-487` still calls the old fixed
0249 receipt/brief validator and then unconditionally raises the seam at
`:149-153`. The checker can therefore PASS while no real current admission is
verified. This is a control coverage limitation, not evidence of a current
binding.

The source-only checks are still useful as control evidence: bash syntax,
Python AST, positive launcher 17/call 1, poison 1/call 0, and lifecycle
fixtures reportedly pass. They cannot qualify the missing production binding.

## F-D141L-BIND-006 — blocking: disk trace is historical, not current

The committed `evidence/disk-trace.txt` starts at
`2026-10-26T06:38:43.577699+00:00` and ends at
`2026-10-26T07:02:33.677822+00:00`. It is the copied 0638 trace. The author's
source dispatch witness is `2026-10-26T07:17:49.555834+00:00`. The manager's
actual source dispatch named for this review is
`2026-10-26T07:29:17.258026+00:00` with 4,648,656,896 free bytes. There is no
continuous 5-second trace that starts before this worker's review and spans
its work. The retained manifest explicitly says the older trace is historical;
that disclosure prevents fabrication but does not satisfy current trace
custody.

The review's own post-start samples are recorded separately in this packet's
`disk-trace.txt`; they are disclosed as post-start samples and are not used to
backfill the missing pre-work interval.

## Non-findings / preserved decisions

The current integrated and pristine tuples, 22 cut roots, 17 pristine roots,
22cut/17pristine settings, D89d floor arithmetic, current App metadata pointer,
pristine roots, old 19479/8912 holds, tiny controls, and the historical trace
gap were not changed. No product source, schema, guard, test, pin, kit,
registry, shared environment, request, row installation, body, or full suite
was run or modified.

## Smallest same-branch fix

The minimum repair is two-part and must remain on this existing branch:

1. Deliver the exact packet to the required absolute ORCH evidence directory
   and make every operational script resolve that delivered packet's own
   absolute root; do not leave `EVIDENCE_ROOT`/`ROOT` pointing at the author
   worktree.
2. Replace the undefined `BINDING.json` handoff with a real existing-route
   controller step that obtains the actual ID from `request-test`, lets the
   existing `test-run`/wait path produce the terminal result, and records the
   request, service row/ID, receipt, brief, current/pristine tuples and
   distinct command/source manifests from that same invocation. The consumer
   must validate the complete v2 request and authenticated request→service→
   receipt→brief ordering before writing the two private rows. No new schema,
   auth flag, interface, service-ID invention, or admission gate is needed.

Only after those two fixes can the current rows be installed and the pair be
dispatched once at `4714564096` bytes. This review does not authorize that
dispatch.
