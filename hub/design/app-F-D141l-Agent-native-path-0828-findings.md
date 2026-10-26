# F D141l native whole-path second-failure investigation — FAIL_FINITE

Read-only source investigation against Composition commit
`6a2d1c22ec800229812f4d756d7198aece8111ed`, tree
`57f68e1fad9c84ce0c0a2fa10f9a2f8defb1a847`. The prior App 0820 packet was
retained for comparison but was tied to the wrong Composition tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148`; it is not reused as current
qualification. No source repair, row install, queue mutation, request, body,
CAS, registry, service, receipt admission, product import, or test run was
performed.

## Findings

### F-D141L-U2-001 — direct `test-run` races the native dispatcher

The controller queues through `request-test` at
`controller-continuation.sh:135-150`, then directly calls `test-run` at
`:154-158`. `request-test:13-15` leaves a `TEST <id>` marker in
`queue/pending`; `dispatcher-daemon:19-21` independently consumes that marker
and calls the same `test-run`. The controller does not claim/remove the queue
item or use the dispatcher’s ownership protocol. `test-run:46-59` has no
atomic per-ID claim around cache/running/heavy checks and launch: two actors can
both pass `alive`/`*.running` checks and write the same result paths. This can
duplicate launch, race status/exit/log cleanup, and make row/receipt timing
non-authoritative.

The controller’s `flock` at `:196-197` only covers controllers using its
private `.d141l-controller.lock`; the daemon does not take that lock. The
ordinary supported ownership is queue → dispatcher `test-run` → `wait-test`,
with the returned result directory as the service identity. A future binding
producer must consume that one native owner’s terminal artifacts; it must not
call `test-run` directly after queueing.

### F-D141L-U2-002 — a cut failure prevents the pristine comparison

`dispatch_phase` deliberately captures `run_rc` and `wait_rc` under
`set +e` (`controller-continuation.sh:153-159`), restores the row, and returns
nonzero at `:177` when `wait_rc` is nonzero. Top-level `dispatch` is still under
`set -Eeuo pipefail` and calls `cut` before `pristine` (`:200-201`). Therefore a
genuine failed cut reaches the function return and exits the controller before
the pristine phase. The advertised two-member/full comparison is not retained
on cut failure; the controller cannot produce a valid paired result in that
case. This is a direct source conclusion, not a test result.

### F-D141L-U2-003 — admission/floor/row custody is not one native atomic span

The controller checks free bytes against `4,714,564,096` at
`controller-continuation.sh:185-192`, before taking its private lock and before
`request-test`. `request-test` then queues normally; the daemon or direct
`test-run` rechecks its own service floor later (`test-run:49-59`). A free-space
change between the controller check and service admission is therefore not
bound to the controller witness. `agent-core-full` is classified heavy by
`test-run:19` and is subject to the ordinary heavy admission/one-heavy checks,
not to the controller lock.

The row is CAS-replaced and reread before request creation
(`:128-152`), but the private controller lock is not held by native
`request-test`/dispatcher. `test-run:16` resolves the current registry command
again; its snapshot work begins later at `:30-45`. The controller has no
shared lock that keeps the row stable through the native actor’s command
resolution and snapshot. The optional bench-store lease rechecks a registration
inside its own lease (`test-run:124-179`), but that is not the controller’s CAS
lock and does not make the controller’s pre-queue receipt authoritative.

The controller writes a claimed receipt before `test-run` (`:148-150`), with
`terminal.path` naming a future file (`:96` in `write_receipt`), and consumes it
before the native terminal exists. The later terminal JSON is assembled from
local status/exit files (`:160-172`). This is not a producer-authenticated
service receipt. `binding-source.py:90-149` verifies ordinary hashes and file
relationships, but it cannot turn this pre-body self-authored JSON into a
native receipt.

### F-D141L-U2-004 — heavy/light classification and D89c are not equivalent

Both controller phases submit the same `agent-core-full` service suite, so the
actual native `test-run` classifies both as heavy (`test-run:19`). Its native
floor is 4,700,000,000 bytes for this named heavy suite (`:52-57`), while
ordinary light suites use 5,000,000,000 and other heavy suites use
5,200,000,000. The old pristine comparator’s direct light/5-GB treatment is
not evidence for this same-suite native path. The command recipes retain a
continuous 4,000,000,000-byte stop, but that is a body sampler stop, not a
replacement for service admission.

The settled D89c arithmetic remains one controller dispatch check at
`4,714,564,096`, then the retained 4-GB sampler and one-heavy serialization.
The source does not justify a second own-preparation admission, a lower floor,
or a light classification for pristine. No live admission was run.

### F-D141L-U2-005 — launcher input is preserved, but request association is open

The cut recipe preserves the existing production
`tools/p4-d73-pinned-launch.sh` (`command-cut.sh:97-108`) and its existing
`p4-d73-v1` key/value manifest format. The launcher source validates the four
SHA/tree/clean checkout pins and consumes the manifest; this is source-only
launcher preservation. The cut and pristine controller arguments are distinct:
`positive.manifest` and `source-manifest.json` are passed separately at
`controller-continuation.sh:148-150`, and `binding-source.py:104-110` checks
their paths and hashes separately.

However, `command-cut.sh:22` uses fixed `REQUEST_ID=agent-core-full`, while
the controller receipt uses the returned service-directory name as
`request_id` (`controller-continuation.sh:89-96, 135-149`). No launcher
terminal/runmanifest is bound back to that returned service ID in the receipt
or terminal JSON. The production launcher is therefore preserved as an input
format, but end-to-end request → launcher → terminal association is UNKNOWN
until the real native producer supplies it. The future controller’s
receipt/binding writer is a self-authored producer and cannot close that gap;
using the existing queue/dispatcher owner is the minimal supported route.

## Target/tree correction and transport limits

The 0735 source publication, 0735 source manifest, and 0820 review retain
Composition tree `5ab519...`; the required immutable derivative is tree
`57f68e1...`. This report uses the required tree and does not silently promote
the old packet. The 0735 `source-manifest.json` records 45 retained historical
or control paths; all 45 are absent here. The two pristine checkout paths and
the pinned Node/profile paths named by the packet are also absent on App. The
45 private bytes are reported as missing transport inputs; none were copied,
provisioned, or substituted. App’s local `suites.conf` has no
`agent-core-full`, but Agent-manager publication separately reports the exact
named route; no Agent absence is inferred from the App view. The intrinsic
controller still proves it can only CAS-replace an existing row (`read_row` plus
`cas_row`), not create one.

Because the required current Composition tree and authenticated native
service/launcher artifacts are unavailable, any claim beyond these source
findings is UNKNOWN, not PASS. C0 v2 request/reply semantics remain unchanged.
