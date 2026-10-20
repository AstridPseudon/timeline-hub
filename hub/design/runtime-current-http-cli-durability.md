# Runtime current HTTP/CLI durability gate

Date: 2026-10-20 UTC

## Scope and source pins

The central test service ran the existing Agent durability tests from Agent
`2f8b9cc53648a392da8684016c6ee15e589ea060` against Runtime `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`.
The named suite checked both worktree HEADs before running. Its Runtime
snapshot tree was `c225a680c645c67c3fe1f43b5e564b2a77a05d80`, the exact tree
of Runtime `6ab3243…`; the snapshot commit itself is synthetic test-service
plumbing.

The Agent M1 test normally reads the Agent lock's older Runtime commit. The
run preserved the test source and temporarily replaced the already-imported
`tests.helpers.runtime.vendored_runtime_commit` function at invocation time
with the required `6ab3243…` value. This changes only the selected Runtime
archive, not test behavior or provider logic.

## Existing cases located

- Agent history: `87b9900f` added
  `tests/editing_conformance/test_commit_runtime_m1.py`; later commits
  `3e293dae`, `fc696847`, `905a4f0f`, and `bfaa241c` modified it. It was not
  moved or removed at the pinned Agent commit.
- Agent current M1 file:
  `tests/editing_conformance/test_commit_runtime_m1.py`.
- Agent provider restart file:
  `tests/sdk/test_timeline_commit_provider_runtime.py`.
- Runtime HTTP door case:
  `tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider`.

## Proof actually executed

Central command: `current-http-cli-durability` from
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`.

Result: Agent M1 plus provider files: **12 passed in 31.79s**. Runtime door
case: **1 passed in 2.62s**. No full suite was requested or run.

The Agent M1 cases prove, through a real Runtime daemon and HTTP transport:

- CLI edit, show, layers, and visualize handlers produce and read accepted
  revisions;
- Python A is durably accepted before its acknowledgement is lost, and its
  exact path/body/idempotency key remains in the outbox;
- dependent B remains queued byte-for-byte unchanged while A is unacknowledged;
- restart restores the in-flight A identity and exact retry returns the
  original receipt without a second history entry;
- a disjoint intervening edit rebases B, while a touched basis refuses B and
  retains the pending command/conflict;
- undo preserves the intervening edit and the prior accepted revision remains
  readable and exact;
- renderer imports/evaluation are tripwired during commit, including the
  restarted provider;
- provider reservation and restore/inverse receipts survive Runtime restart
  and exact retry without re-running semantic provider work.

The Runtime door case independently uses the real loopback HTTP door and
actual Runtime provider. It restarts the daemon, retries the exact original
request after a newer disjoint commit, checks idempotency mismatch refusal,
then verifies undo and historical readback.

## Boundaries and gaps

The requested Agent M1 file's “CLI” path calls `astrid.packs.timeline.cli`
`build_parser(...).parse_args(...); parsed.handler(...)` in-process. It is not
a spawned CLI subprocess. The Runtime door case uses direct HTTP client calls,
not a CLI subprocess. The M1 lost-ACK seam monkeypatches RuntimeHandler's
response send after durable acceptance; the daemon, provider, HTTP route,
outbox, restart, and persistence are real, but this is not a physical socket
EOF test. The Runtime door case discards the received response before restart
rather than cutting a live socket.

Therefore this is positive evidence for the named real-daemon HTTP/provider
durability cases, not proof of a real CLI subprocess or network-level
connection-drop fault. No current-live-Agent source mix, full suite, or
renderer-enabled save claim is included.

## Next step

If the gate requires subprocess-level CLI and socket-EOF proof, add those as
separate explicit cases while retaining the existing assertions; do not call
this run a complete subprocess transport gate.
