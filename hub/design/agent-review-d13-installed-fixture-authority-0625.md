# D13 installed fixture authority review

**REQUEST CHANGES / HOLD native gate.** Reviewed the exact committed
`tl/agt-m2-d13-installed-native-command-complete-preflight-0609` at
`61f730f2d7bfad7e6c8797ce67f93ffeab118ab7`, tree
`36fb0f2cfcdbad4483f56b76175daca4c2acad59`. The commit is test-only: it
changes `tests/packs/video_editing/test_runtime_publication_chain.py` by
`+352/-132` and adds no product authority, Runtime profile field, grant, or
credential route. I made no repository source changes.

## Installed tuple and source freshness

The coherent6f report identifies the staged tuple as:

| component | exact source | installed identity |
| --- | --- | --- |
| Agent | `6f2d8c350ad6838d2a2cd8da98e49465b1ab2406`, tree `698ae4df6ea9e9e89746fffabfaab15ac0c7d47f` | `astrid==0.1.0`, wheel SHA-256 `fa2f824d1068f6233dc852960726d597f21a243d768ff0cafe258b7afe391346` |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31`, tree `6abc2f117391de8e7e35c0283f575a002199894d` | wheel SHA-256 `12df54644e1acac46b9c396135ef345808a98515965f1f12f479f32adf3c9b0a` |
| client/artifacts | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00` | `astrid-runtime-client==0.2.14`, SHA-256 `567605b13254f88ddeddad7b570553a2c50b5092908e6c4153553f9867e37254` |

The profile at the reported private stage contains exactly the existing four
fields (`profile`, `runtime_checkout`, `source_checkout`,
`runtime_environment`) and selects the same non-symlink site-packages tree for
Agent, Runtime, and client. The installed origin probe covers the required
eight keys (`host`, `child`, `action`, `client`, `sdk`, `runtime_protocol`,
`runtime_protocol.platform`, `astrid_runtime`) and rejects origins outside
that selected tree. The staged interpreter, package origins, Node, Remotion
lock, browser, ffmpeg, and ffprobe were present with the expected hashes at
review time; the offline control below passed.

This is not yet immutable source/profile binding. `_D13_PROFILE` is entirely
caller-selected through `ASTRID_D13_SOURCE_PROFILE`; the preflight computes a
fresh `source_checkout_digest` from that supplied path and only asserts that
the digest is nonempty. It does not compare the profile to Agent `6f2d8c…`,
tree `698ae4…`, or the installed wheel SHA, and teardown reuses the original
in-memory profile mapping rather than rereading and locking the profile file.
Thus a different regular, non-symlink installed tree can satisfy the same
preflight if its eight origins and resources are coherent. The independent
coherent6f report supplies the missing exact-artifact evidence, but this
committed fixture does not enforce that binding itself.

## Authority, credentials, and custody review

The positive fixture uses the normal Runtime CLI path:

```text
astrid-runtime workspace create --profile astrid --source-manifest <profile>
  --data-root <private support> --realm-root <private realm> --hosted-origin off --json
astrid-runtime up --profile astrid --source-manifest <profile>
  --data-root <private support> --hosted-origin https://astrid.local
  --door-port 0 --wait --json
```

It reads the Runtime-created owner and worker credential files, constructs
the normal `AstridClient` and `RuntimeProtocolClient`, and starts the existing
pack host through `ensure_pack_host`. It does not construct a fake accepted
receipt, fake Runtime service, SQL fixture, or direct local publication. The
child media are real ffmpeg-generated MP4 bytes settled through the normal
worker API; the authoring and render tasks are then polled from Runtime. The
fixture removes ambient `PYTHONPATH` before creating the `GenericPackHost`,
uses the selected installed pack root, and passes the installed interpreter
and source manifest through explicit environment values. The test harness
itself may use an explicit `PYTHONPATH=$PWD` to import the snapshot’s tests;
that is not product import authority for the launched Runtime/pack-host
process, but the command must keep that distinction explicit.

No helper bypass or fabricated native result was found. Replacing direct
`host.run_task` calls with the real installed pack host is the intended
custody correction. The fixture does not, however, assert from the returned
task that the author/render attempts were executed by the expected
`astrid-pack-host` actor rather than another executor. That is a small
process-custody assertion gap for the native run, not evidence of a bypass.
It also does not independently validate credential-file regularity, mode,
scope, or actor identity; those remain Runtime/bootstrap contract evidence,
not this offline preflight’s assertions.

Hard-coded resources remain a portability problem. The profile is explicit,
but Node, Remotion, browser, ffmpeg, and ffprobe are fixed at
`/home/user/work/...`, `/opt/pw-browsers/...`, and `/usr/bin/...` in the test
module. A worker on another permitted machine cannot supply an equivalent
resource set through test environment alone. The fixture is therefore
portable only inside this worker layout, not through a fully explicit test
environment. Resource paths should be supplied by the existing test-lane
environment/profile recipe (without adding a Runtime profile field), and
the preflight should bind the expected final source/tree and Agent wheel
identity before the one native run.

## Required output/assertion preservation

The active integration test remains the original positive node and is not
xfail/skipped. Its retained assertions still cover: ordered managed-media
selection, `rendering.assemble_timeline` admission, settled authoring
proposal and command/object identity, `producer.guard`, lost commit ACK,
durable flight identity, restart/exact retry, accepted revision/publication
IDs, ordinary revision-pinned render admission, nonempty MP4 plus `ffprobe`
duration, render timeline authority, and guarded undo. The neighboring
canonical-proposal and legacy-refusal tests remain unchanged. The test-only
delta replaces local direct claim/run calls with the real pack-host polling
path and keeps the real output assertions; it does not turn a passing
behavior into refusal.

The committed preflight does not execute Runtime, HTTP, browser, native,
renderer, or full suites. The historical exact D13 command in the coherent6f
report is explicitly stale and unsafe as current proof because it uses
`ASTRID_RUNTIME_CHECKOUT`, checkout `PYTHONPATH`, and the old C13 child:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-main95bd \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-main95bd/node_modules \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages \
  /home/user/work/venv-agent-child-c13-a8a40afd/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

The only later authorized lane remains the single named
`d13-native-positive-render-integration` node above, but it must be rebuilt
with the final installed profile and explicit resource environment after the
authority repair. No native execution was performed here.

## Current merge-forward required before calling the gate current

The installed Agent is not current. It predates the public custody/security
merge `8e567cdbf65dc675228e532eab6046a3830a9dd7` (current `tl/integration`
contains that merge at tip `18a89a0d29766bd3cec31391042836ba7c951fa1`, tree
`6802b125647c6b836749e661b6c534e1f2e9d811`) and predates the pending
document-diff repair `fa36a85f41aef1ff6270edc3b9e296b5c16c74e7`, tree
`83c3d869e2d82a3ae1bb2c2df07b5bd34ffef4f2`. The corresponding authenticated
document-diff test is `35128794acd7ce1ecd41114aafd1b3729cae2787`; it is
separate test evidence, not a substitute for the source repair.

Required sequence:

1. Merge-forward the reviewed D13 source onto the current Agent base while
   preserving the public `8e567cdbf…` custody fix and then the reviewed
   `fa36a85f…` presence-loss repair. The current integration tip is not an
   ancestor of 6f2d8c, so this is a deliberate source composition, not a
   claim that the old installed wheel is current.
2. Freeze the resulting exact Agent commit/tree and build a new noneditable
   Agent wheel in the private wheelhouse with the existing offline recipe:

   ```text
   python3.13 -m pip wheel --no-index --no-build-isolation --no-deps \
     --wheel-dir "$PRIVATE_ROOT/wheelhouse" "$PRIVATE_ROOT/source/agent"
   "$PRIVATE_ROOT/venv/bin/pip" install --no-index --no-deps --force-reinstall \
     "$PRIVATE_ROOT/wheelhouse/astrid-0.1.0-*.whl"
   ```

   Record the new wheel SHA-256, final Agent commit/tree, package RECORD
   closure, and the final profile/source digest. Re-run the eight installed
   origins, no-symlink/containment, hermetic help/doctor, and resource-lock
   controls against that exact wheel. Do not reuse the old Agent wheel hash
   `fa2f824d…` or silently reuse the 6f profile.
3. Keep Runtime b92/client 95 and the existing 164-entry lock byte-identical
   unless a real compatibility change requires their separately reviewed
   refresh. Do not add Runtime profile fields, grants, routes, or credentials.
4. Only then issue the one named native command with the final installed
   interpreter/profile and explicit tool/resource environment, preserving the
   exact positive test node and all assertions.

## Evidence run

The smallest permitted offline control was:

```sh
ASTRID_D13_SOURCE_PROFILE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging/profile/astrid.json \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging/venv/bin/python \
-m pytest -q -p no:cacheprovider \
tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight
```

Result: **1 passed in 1.22s**. This checked the four-field profile, selected
interpreter, eight origins, path containment/no symlinks, current resource
hashes, fonts, private writable attempt root, and disk headroom. It did not
open Runtime or a browser and did not execute native/render/full/HTTP lanes.

No full suite or named native suite was requested. No shared dependency or
worktree was modified. The installed profile remains a valid coherent6f
preflight record, but the native gate is **not current and not cleared** until
the binding/portability issues and current merge-forward/wheel refresh above
are resolved.
