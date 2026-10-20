# Runtime current HTTP/CLI suite fail-fast fix

Date: 2026-10-20 UTC

## Change

The named `current-http-cli-durability` suite now invokes the small strict
wrapper at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-current-http-cli.sh`

Script SHA-256:

`c66acf7042677867788b2b0826f00f81cb084386dcce3649d18675ee8ab3ec07`

The only `suites.conf` line replacement is:

```text
runtime current-http-cli-durability bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-current-http-cli.sh
```

Suite-line SHA-256:

`823ca7aec2d4b5ae4daae0e976a3a5a172fbd5b91169469b32ccbae3b8ed7833`

The wrapper uses `set -euo pipefail`, so a failing Agent invocation cannot be
masked by the Runtime invocation. A private smoke injects failure into its
first command and verifies that the second command does not execute.

## Guards and source proof

- Runtime server source is exactly `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`,
  guarded through `refs/heads/tl/rt-m2-cli-current6ab-actual`.
- Agent test source is exactly `2f8b9cc53648a392da8684016c6ee15e589ea060`.
- The wrapper logs Runtime server `6ab…`, immutable producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and Agent `2f8…`
  separately.
- Before the test-helper `vendored_runtime_commit` source-selection override,
  the wrapper checks Agent `runtime.lock.json` for producer `2c4…`, schema
  digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
  and artifact version
  `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- It compares the current server and producer artifact manifests and verifies
  all 75 listed artifact byte strings and their SHA-256 values are identical.
- The frozen Runtime source is materialized in a private temporary clone;
  producer metadata is not rewritten and no shared dependency is modified.

## Central test request

Request:

`request-test rt-m2-cli-suite-failfast-fix current-http-cli-durability`

Result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-cli-suite-failfast-fix-current-http-cli-durability-1020164442-248/`

Snapshot:

```text
tree=94c5ffbc0b636e25475c0f351bfb384dd06ee8ab
key=a8cf47328832264e9519ac7f79058ecb
```

Result: **pass, exit 0**. The Agent invocation ran the existing M1 and
provider files: **12 passed in 43.88s**. The Runtime invocation ran the one
existing HTTP durability case: **1 passed in 3.17s**. The pre-test smoke and
75-entry artifact proof also passed.

No full, broad, render, or other suite was run.

## Boundaries

The existing positive assertions and actor, realm, health/epoch, and provider
authorization checks remain untouched. The Agent “CLI” cases invoke the CLI
parser and handler in-process, not a spawned OS CLI subprocess. The lost-ACK
case uses the existing post-durable-acceptance response-send fault seam; it is
not an OS-level socket-EOF test. This result is bounded evidence for the
existing 12+1 cases, not a claim of subprocess or physical socket-drop proof.
Historical 12+1 reports remain bounded historical evidence; this run does not
turn them into an all-green or full-suite claim.
