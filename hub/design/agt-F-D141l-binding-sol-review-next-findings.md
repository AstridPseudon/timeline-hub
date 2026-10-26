# F D141l independent binding review

Verdict: `FAIL_SOURCE`. The Sol derivative improves the 0731 packet and its
source controls pass, but it is not `READY_SOURCE` for the required current
Composition tuple or complete future controller path.

## Adjudication of the 0731 six findings

1. Absolute delivery is fixed: the author packet exists under the required
   absolute ORCH root and its source hashes are internally consistent.
2. The undefined caller-supplied `BINDING.json` producer is removed at source
   level. `controller-continuation.sh` now has existing row-CAS,
   `request-test`, dispatcher-owned `test-run`, `wait-test`, and native result
   inspection functions. It still refuses before those functions run.
3. The old self-authored receipt authority is not preserved. The consumer
   rejects `admission`, `consume`, and `dispatch-readiness`; `inspect-result`
   reads the native result directory instead. The test-service request remains
   `target/repo/suite/files/nocache/requested`, not the Runtime v2 commit wire.
4. Source-only non-installation is not itself a failure. The current ORCH
   registry has the historical `agent agent-core-full` row, and the supported
   installer can CAS-replace that owned row before a future request. No row was
   installed here, as required.
5. Fixture-only controls remain correctly limited: they prove source behavior,
   not live admission. This is an expected prospective-output boundary, not a
   claim of passing product behavior.
6. The author trace belongs to the author and reports its real gaps. It cannot
   be upgraded into continuous admission evidence.

## All five native 0828 findings

U2-001 is closed in source: `queue_and_wait` invokes `request-test` and then
`wait-test`; it does not invoke `test-run`, leaving the queued dispatcher as
the normal owner. U2-002 is closed in source: a nonzero cut terminal result is
recorded and the pair proceeds to pristine before returning the cut result.
U2-004 is closed in source: both phases use `agent-core-full`, retain the
native 4,700,000,000-byte heavy floor, use one controller witness at
4,714,564,096 bytes, and retain the 4,000,000,000-byte sampler stop.

U2-005 is sufficient at plain artifact scope, but only source-only. The native
result directory supplies the returned service ID and request bytes; `snap`
supplies the source tree/worktree; `summary` supplies the actually resolved
command; `status`, `exit`, and `log.txt` supply the terminal; the command
terminal verifies JUnit/custody; and the D73 launcher checks its request-id and
runmanifest against the same service ID and command manifest. This is the
existing producer/consumer route identified by D66. It does not need a signed
receipt or a new handshake.

U2-003 must therefore be narrowed, not accepted as a demand for new
cryptographic custody. The current source still fails the required complete
future path for three concrete reasons:

- `binding-source.py` rejects `dispatch-readiness` before any native route,
  so no genuine request ID, request bytes, registered row, immutable brief,
  dispatch witness, or terminal artifacts can be produced by this packet.
- The controller writes `dispatch-witness.txt` but has no immutable owner
  brief producer or binding field for one.
- `install_p4_launcher.py` locks only the registry update. The lock is released
  before `request-test` queues and before dispatcher `test-run` resolves the
  row. A concurrent row edit can make the daemon run a stale command; the
  post-body summary check can refuse it, but cannot prevent the stale body.

This is the smallest real native seam. The existing plain request/result
artifacts are enough for association; the remaining decision is how the
existing controller/daemon route is allowed to preserve the owned row and
produce the brief without adding a new authority protocol. If that cannot be
done with existing orchestration scope, it is an orchestrator scope decision,
not an implied Runtime contract change.

## Current tuple blocker

The author `source-manifest.json` binds Composition commit
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148`. This review base is Composition
commit `6a2d1c22ec800229812f4d756d7198aece8111ed`, tree
`57f68e1fad9c84ce0c0a2fa10f9a2f8defb1a847`. The App binding is correctly the
new `82e9e13ddf1d7ec6c736521b2eb091dca9877598` / `6a6e49eb4461b5ca1a7fa1247653bc794f26d710` tuple; no historical App receipt was retargeted.

## Controls and limits

The exact author checker exited 0 with `control_status=PASS`,
`pair_status=BLOCKED_U2_003_NATIVE_CUSTODY`, 10 admission cases and 38
lifecycle cases. Shell syntax and Python AST both exited 0. The retained
launcher controls are positive exit 17/call 1 and Agent-SHA-only poison exit
1/call 0. No request, row installation, test-run, wait-test, body, collection,
pytest, full suite, product import, or behavioral qualification was run.

The full Runtime `commit-v2` shapes remain contract context only; no
test-service request was incorrectly validated as a v2 commit request.
