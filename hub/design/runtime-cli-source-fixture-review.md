# Runtime current HTTP/CLI source-fixture review

Date: 2026-10-20 UTC

## Decision

**REJECT as a qualification result for `current-http-cli-durability`.**

The underlying source/artifact pairing is compatible and is approved only as
bounded source evidence below. The named test-service command is not an
acceptable gate because its two pytest invocations are separated by `;`:

```sh
... pytest(...); cd "$RUNTIME_SOURCE"; ... pytest ...
```

The shell therefore returns the second pytest status. A failure in the first
Agent invocation can be masked by a passing Runtime invocation. The observed
`exit=0` does not prove that both invocations passed. The command must be
fail-fast (`&&`) or capture and return both statuses before this evidence can
qualify.

## Source and artifact bounds verified

- Runtime candidate: commit `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`,
  tree `c225a680c645c67c3fe1f43b5e564b2a77a05d80`.
- Agent candidate: commit `2f8b9cc53648a392da8684016c6ee15e589ea060`,
  tree `8f15471af6928e166cfbeedf6d00d7cf6454cfbe`.
- Agent `runtime.lock.json` still names immutable producer commit
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, not `6ab`, with schema/client
  digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`
  and artifact version
  `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- Read-only verification of `contract/artifacts.json` found 75 entries on
  both `6ab` and producer `2c4`. Every listed blob's SHA-256 matched its
  manifest entry on both refs, and the two manifests were byte-identical.
  Thus no producer-2c4 metadata rewrite as 6ab or artifact-byte mismatch was
  found.

The above is independent git-object verification, not a guard performed by
the named suite. The suite's `runtime.vendored_runtime_commit = lambda:
"6ab..."` bypasses the helper's normal lock-derived selection. It is safe for
this pair only because the independent 75-entry check above passes; the
command does not enforce that fact and could hide a future mismatch.

## Historical test-service evidence and exact limits

Result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-current-http-cli-durability-current-http-cli-durability-1020163359-18619/`

Exact configured command (abridged only by line wrapping here; the stored
`tests/suites.conf` line is the command audited):

```sh
RUNTIME_SOURCE=$PWD; AGENT_SOURCE=/home/user/work/wt/agt-pin-2f8b9cc5;
test "$(git -C /home/user/work/wt/rt-m2-current-http-cli-durability rev-parse HEAD)" = 6ab3243972f8dc49105819e6d7ba7aef1a2888b8;
test "$(git -C "$AGENT_SOURCE" rev-parse HEAD)" = 2f8b9cc53648a392da8684016c6ee15e589ea060;
cd "$AGENT_SOURCE"; env ASTRID_RUNTIME_CHECKOUT="$RUNTIME_SOURCE" ASTRID_CHECKOUT="$AGENT_SOURCE" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGENT_SOURCE:$RUNTIME_SOURCE" /home/user/work/venv-agent/bin/python -c 'import pytest, tests.helpers.runtime as runtime; runtime.vendored_runtime_commit = lambda: "6ab3243972f8dc49105819e6d7ba7aef1a2888b8"; raise SystemExit(pytest.main(["-q", "-p", "no:cacheprovider", "-m", "integration", "tests/editing_conformance/test_commit_runtime_m1.py", "tests/sdk/test_timeline_commit_provider_runtime.py"]))';
cd "$RUNTIME_SOURCE"; env ASTRID_RUNTIME_CHECKOUT="$RUNTIME_SOURCE" ASTRID_CHECKOUT="$AGENT_SOURCE" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$RUNTIME_SOURCE:$AGENT_SOURCE" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider
```

The service log reports `12 passed in 31.79s`, then `1 passed in 2.62s`, and
`exit=0`. No live/full rerun was performed for this review.

The tested source locations are:

- Agent `tests/editing_conformance/test_commit_runtime_m1.py` and
  `tests/sdk/test_timeline_commit_provider_runtime.py`;
- Runtime
  `tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider`.

The cases provide bounded positive evidence for a real Runtime daemon/provider,
HTTP route, restart, durable acceptance/retry, outbox A/B preservation,
disjoint rebase versus touched conflict, guarded undo/history readback, and
the existing actor/realm scope, health-epoch, and handshake assertions. No
provider mock, auth relaxation, or capability bypass was found.

They do **not** prove a spawned CLI subprocess or a physical socket-EOF
failure: the Agent “CLI” calls `build_parser(...).parse_args(...); handler(...)`
in-process, and lost-ACK uses the existing post-acceptance `_send` fault seam.
The Runtime door case uses direct HTTP and discards the response before
restart rather than cutting a live connection.

## Required next step

Keep the existing positive assertions and replace the suite command with a
fail-fast or explicit-status form. Add small command-level source guards for
the exact Runtime/Agent heads, immutable `source_commit=2c4`, schema
`8de823...`, artifact `6f000...`, and the 75-entry manifest/byte parity (or
use the explicitly named private fixture environment if only prefix proof is
available). Do not silently repin metadata, weaken auth/realm checks, mock the
provider, or relabel this historical result as a complete subprocess/socket
transport gate.

