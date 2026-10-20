# Real pack-host helper handoff

2026-10-20. Agent branch `tl/agt-m2-host-final-compose`, worktree
`/home/user/work/wt/agt-m2-host-final-compose`. Handoff branch only: the helper
source and approved production ownership fix both remain M2 HELD until PLAN
records M1 exit. Viewing owns the App wrapper and may qualify this exact source
on its branch; this document grants no integration merge or consumer pin change.

## Source and production seam

Base `c9284b892e76394c511e0b2b8d81473979f211a8` supplies the unchanged 248-line
`tests/packs/rendering/real_pack_host.py`. The exact reviewed files from
`b894d2651c8bf990ed7600025c616ee7e77acd5c` supply `astrid/sdk/host_bootstrap.py`,
`tests/sdk/test_host_bootstrap_source_identity.py`, and
`tests/sdk/test_host_launch_ownership.py`. The only composition edit migrates the
progressing-startup offline fixture to a real custody-owned Popen and a
`terminate_group` spy that delegates real cleanup. All existing source,
foreign-ownership, marker, signal-at-logical-10 and before-handler cleanup
assertions remain; reaping and group-absence assertions are strengthened.

The helper calls the existing production launcher-owned `ensure_pack_host`
function with real discovery plus the selected Agent checkout. DirectHarness
starts Runtime with arbitrary realm/support roots; `ensure_runtime()` expects a
neutral-launcher data-root/catalog shape and is not this connection seam. No
alternate launcher, owner credential, fabricated validation, Runtime change,
readiness-policy change or scope expansion is introduced.

## Caller inputs and environment

The caller owns a running local Runtime and a dedicated fresh host support root.
Supply absolute local paths for realmDir, supportDir, discoveryFile (exactly
`supportDir/discovery.json`), and the selected Agent source checkout, plus the
expected real Runtime instance ID. The paths pass production safe-local-path
checks; discovery must identify that realm and Runtime instance. Neither
`generic-host.json` nor `generic-host.ready.json` may already exist. Create
support privately (0700), as DirectHarness does.

Runtime must provision its actual production worker credential under
`supportDir/credentials` (file mode 0600), declared in discovery with actor
`astrid-pack-host` and exactly these production scopes: `handshake`,
`worker:register`, `worker:execute`, `projects:read`, `tasks:read`, `objects:read`,
`objects:write`. The helper reads that file, checks live Runtime health and
worker authentication/realm identity, and never provisions or prints a token.
No owner credential or ambient bearer is a substitute.

Spawn the selected Agent Python from cwd=agentCheckout with
PYTHONPATH=agentCheckout and stdin/stdout pipes. The shared test interpreter is
`/home/user/work/venv-agent/bin/python`; optional production
`ASTRID_PACK_HOST_PYTHON` must name an approved absolute executable. Inherit the
caller-owned selected render/browser environment; do not manufacture validation
markers, disable validation or replace selected toolchain paths. The qualified
central environment uses:

- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`
- `ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion`
- `ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`
- `ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages`
- Node v20.19.4 first on PATH; shared Agent Python on PATH.

`orch/tests/agent-remotion.env` records the render selections. The production
launcher owns source/installed profile behavior, dependency filtering, removal
of job-local tags and `ASTRID_PACKS_PATH`, boot manifest construction, source and
closure identity, managed-source inventory and Remotion validation. This helper
does not alter those policies. The integration test removes only pytest's own
unsupported `PYTHONPYCACHEPREFIX` override before spawning the CLI; the helper
itself inherits the supplied environment.

## CLI and Python protocol

```sh
/home/user/work/venv-agent/bin/python -m tests.packs.rendering.real_pack_host \
  --realm-dir /absolute/realm \
  --support-dir /absolute/support \
  --discovery-file /absolute/support/discovery.json \
  --source-checkout /home/user/work/wt/agt-m2-host-final-compose \
  --runtime-instance-id EXPECTED_INSTANCE_ID
```

Each stdout message is one JSON line. Wait for `status=ready` before using the
host. That line includes host PID, Runtime identity/epoch, ready-file path,
ready capabilities, source/closure/inventory digests, boot-manifest path/hash.
It carries no bearer. Readiness requires both production host readiness with
`rendering.render` and that capability being `ready` in the actual worker-readable
Runtime catalog. Production validates source/closure/manifest/launch identity;
no fake host, catalog or executor owner-only observation is used.

Keep stdin open for the lifetime of the wrapper. Write `stop\n` or close stdin
(EOF) to request cleanup, then await `status=stopped` with the same host PID and
exit 0. Stop/EOF sent during startup is queued input consumed after readiness;
it does not cancel startup. Other input fails. Ordinary exceptions emit
`status=failed` with exception type/location only and exit 1. SIGINT/SIGTERM/
SIGALRM use the CLI's raising handler and exit 1; they need not emit `stopped`.
Collect process exit as well as JSON, and retain stderr for diagnostics.

Python callers use the context manager, with Path-valued inputs:

```python
from tests.packs.rendering.real_pack_host import start_real_pack_host

with start_real_pack_host(
    realm_dir=realm_dir, support_dir=support_dir,
    discovery_file=support_dir / "discovery.json",
    source_checkout=agent_checkout, runtime_instance_id=instance_id,
) as host:
    # host.ready is production metadata; the caller may use the running host.
    pass
```

Launch happens on context entry; the owning finally covers the caller body.
`RealPackHost.close()` is idempotent after successful cleanup.

## Ownership, cancellation and limits

During launch, INT/TERM/ALRM raise a private BaseException to unwind production
startup even while progress continues. Children inherit an unblocked signal
mask. Once cancellation starts, those signals are blocked through cleanup and
original handler delivery is deferred. Production now retains the actual
returned Popen's incarnation-bound custody from handle assignment through log
close, birth capture, state writing, progress polling and ready validation.
On failure it calls real `terminate_group(process)` and polls the original
child. Cleanup authority never comes from a possibly replaced registration.
Markers are removed only after successful custody cleanup and exact expected
launch bindings, PID and retained birth match. Changed or malformed records
remain; they do not grant authority over another process.

The helper recovers return/adoption gaps only under the existing lifecycle lock:
returned PID (when available), live OS birth, own-child status, selected source,
Runtime/support identity and production command identity must agree. A wrong
source/birth/command, replacement or nonchild never constructs a cleanup handle.
Close checks full marker equality and process ownership, invokes existing real
production retirement, verifies no birth-anchored group survivors and reaps the
owned leader before original handlers run. The Runtime stays alive. Cleanup
uncertainty/errors are surfaced; they are never permission to kill foreign work.

The CLI alarm requests cancellation at 180 seconds; production uses a 30-second
progress-idle window. **There is no universal startup or total-exit deadline.**
Ongoing production progress normally resets its idle deadline; cleanup, census,
locks and waitpid can extend exit. Linux/main-thread behavior is qualified only
for the tested boundaries. Interruption inside Popen/custody internals before a
handle returns, repeated-signal stress, SIGKILL, interpreter death, uninterruptible
native calls and macOS are outside certification. The reviewed fix closes the
returned-handle birth/registration gap; it does not certify pre-return internals.
A populated external managed-source inventory is not separately qualified.

## Qualification

Frozen Agent combined tree: `687f077c4771e3dbb66bfb7ff2b98f310ac054b6`.
Runtime: clean `/home/user/work/runtime`, commit
`9f9b25c000485e919f30f1411831fe2d5a3c1316`, tree
`5c3a7e7141047d7295ab130a8f05359f4fcb34bc`.
Agent pack-source digest:
`365136a31323f0556fd7af465f86d246a43b0285659503622b7a533a1b6c3af7`;
production executable closure digest:
`df3f607f68ceed56bc5f2e1a626dbd38f42150e1e0c41a33a430c587c09626d4`.
The harness will assign the handoff branch commit after worker exit; the tree
above identifies tested source independently of that future commit SHA.

Offline command (worktree cwd):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m 'not integration' tests/packs/rendering/test_real_pack_host.py tests/sdk/test_host_launch_ownership.py tests/sdk/test_host_bootstrap_source_identity.py tests/sdk/test_host_recovery.py tests/sdk/test_child_host_union.py tests/sdk/test_host_ready_empty_inventory.py tests/stage1/test_host_bootstrap_manifest_luna.py tests/core/execution/test_process_group.py tests/test_process_group_cleanup.py
```

Result: **234 passed, 5 skipped, 6 deselected in 83.41s**. The five skips are
existing native-Darwin cases on Linux; the six integration cases run centrally.
Scoped Ruff and `git diff --check` passed.

Single central request:
`agt-m2-host-final-compose-real-pack-host-integration-1020010913-22865`.
Result pending; source frozen before submission and unchanged afterward.
Absolute result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-host-final-compose-real-pack-host-integration-1020010913-22865/`.
 Offline
real-custody tests establish the production returned-handle cleanup guarantee,
including birth/registration failures and preservation of live foreign children;
helper-only mocked tests are not the sole evidence. The central six cases cover
early stop, EOF and synchronized registered-startup SIGTERM, plus after-ready
stop/EOF/SIGTERM and competing actual CLI refusal.

No final saving, renderer-independent save, render output, browser, App wrapper,
frame/audio parity, full-suite or make-check qualification is claimed. Viewing
owns App wrapper implementation and any later exact-source App qualification.
