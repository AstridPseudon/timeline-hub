# Gate7 source group1: custody/platform current-cause report

Date: 2026-10-21 UTC

## Scope and identities

This is the nine-node group from
`agent-full21969-unclassified-owner-disposition.md`. I used the current
`tl/integration` source in this worktree:

```text
Agent HEAD:       6accf0f7be925f47d7fb9b4b522bb66ecf0d89ef
Agent tree:       a3282e5b7b03135bfa499433f36449d6ee7986a6
Main497:          origin/main 497714c73531f164082555ec81b61ca5bc8b6554
Main497 tree:     daaeb1149898dd327947e21c554b484094f960b2
Runtime source:   /home/user/work/runtime @ b92d3e7a05eec65c142294ef4873edd059e9b31d
Runtime tree:     6abc2f117391de8e7e35c0283f575a002199894d
Python:           private profile venv, CPython 3.13.16
```

The private profile was the existing read-only coherent profile at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging`.
The test process used `PYTHONPATH="$PWD:/home/user/work/runtime"`, so the
worktree's Agent source won and Runtime b92 was explicit; an origin probe
resolved `astrid` to this worktree and `runtime_protocol` to
`/home/user/work/runtime`. No shared dependency or checkout was modified.

## Permitted test run

Exact command (only the nine compact nodes; no full, browser, renderer, or
child suite):

```sh
PROFILE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging
RUNROOT=$(mktemp -d /tmp/agt-m4-custody-compact-XXXXXX)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  "$PROFILE/venv/bin/python" -m pytest -q -p no:cacheprovider --basetemp="$RUNROOT" \
  'tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]' \
  'tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]' \
  'tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-register]' \
  'tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-bind-launch]' \
  'tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-register]' \
  'tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-bind-launch]' \
  tests/core/execution/test_platform_boundary.py::test_agent_native_process_and_lock_boundary \
  'tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[False]' \
  'tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[True]'
```

Result: **9 failed in 9.36s**.

The two wrapper nodes failed during test setup at line 149 of the test:
the sandbox denied the test's parent `socket.AF_INET` creation with
`PermissionError: [Errno 1] Operation not permitted`. They did not reach the
wrapper or the `denied == True` assertion. This is an execution-environment
boundary, not evidence of a current source failure. The retained full run's
older `denied == False` observation remains unverified here. Current wrapper
source and this test have no relevant diff from Main497.

The other seven nodes reached their assertions:

* Four pidfd nodes failed at `test_pidfd_callers.py:138`: the patched
  `custody.os.close` was called zero times instead of once with fd 73.
* The boundary scan failed with
  `root_preparation.py:48 os.getuid` and `outbox.py:4,35 fcntl`.
* Both private-directory nodes failed at `test_platform_helpers.py:85`:
  `created == []` instead of `[root]`.

## Node-by-node disposition

### 1–2. Isolated wrapper target, command and engine

**Disposition: inherited unchanged seam; unverified because of the local
network-socket test boundary, not a product correction.** The test creates a
loopback AF_INET listener before invoking the wrapper. The sandbox rejects
that setup, so neither the network-policy hook nor environment restoration is
observed. `custody_wrapper_argv()` and `child_exec_from_environment()` are
unchanged against Main497 in the relevant region. Do not weaken the strict
`denied`, custody-key, hook, environment, and engine-fd assertions. A later
outside-sandbox compact rerun is needed before classifying the retained
`denied == False` result as source-owned.

### 3–6. Post-open pidfd cleanup, four parametrizations

**Disposition: actual Agent custody defect.** In current
`astrid/core/execution/custody_broker.py:3121-3140`, the code opens fd 73,
then performs the second identity read and `os.set_inheritable()` without an
outer `retained`/`finally` guard. If either identity lookup or inheritability
setup raises, the descriptor is not closed. Main497 had the required
`retained = False` guard and closed the descriptor in `finally` whenever
ownership was not transferred. Current later code adds `_PidfdExitProof`, but
that does not replace the missing untransferred-handle cleanup.

The original strict tests are unchanged and correctly assert both that the
fd closes once at the failure and that a later `release_pidfds()` does not
close it a second time. No test or custody code was changed.

Exact narrow repair draft for the owner gate (not applied): retain the current
`_PidfdExitProof` setup, but wrap every post-open operation through proof
registration in the Main497 shape:

```python
descriptor = platform.pidfd_open(pid)
retained = False
try:
    if identify(pid) != birth:
        if held:
            raise CustodyError("descendant changed during pidfd binding")
        return
    os.set_inheritable(descriptor, False)
    proofs = getattr(self, "_pidfd_exit_proofs", None)
    if proofs is None:
        proofs = self._pidfd_exit_proofs = {}
    terminal_births = getattr(self, "_pidfd_terminal_births", None)
    if terminal_births is None:
        terminal_births = self._pidfd_terminal_births = {}
    proof = _PidfdExitProof(descriptor)
    self._handles[pid] = (birth, descriptor)
    proofs[pid] = proof
    terminal_births.pop(pid, None)
    retained = True
finally:
    if not retained:
        os.close(descriptor)
```

The four existing parametrizations are the equivalent assertions for this
small repair; rerun exactly those four nodes after an owner-approved patch.

### 7. Agent native process/lock boundary scan

**Disposition: two separate source findings, not one blanket failure.**

* Viewing-owned rendering source: `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:48`
  directly uses `os.getuid`. The exact evidence was sent to Viewing in
  `hub/inbox/viewing.md`; no competing edit was made. This file is absent
  from Main497, so it is current inherited/unrelated to the Agent custody
  repair.
* Agent-owned outbox source: `astrid/sdk/timeline/outbox.py:4,35` imports and
  calls `fcntl.flock`. This is a real platform-boundary defect against the
  existing rule, not a stale mock. The file is a current addition absent from
  Main497.

The existing Runtime b92 replacement is:
`runtime_protocol.platform.lock_file(fd, exclusive=True, blocking=True)` and
`runtime_protocol.platform.unlock_file(fd)`. On POSIX, `lock_file` delegates
to `fcntl.flock` with `LOCK_EX` (and `LOCK_NB` when nonblocking); when Runtime
cancellation is active, its blocking form retries with cancellation checks.
On Windows it uses `LockFileEx`, maps sharing contention to
`BlockingIOError`, and `unlock_file` uses `UnlockFileEx`; POSIX unlock uses
`flock(..., LOCK_UN)`. Runtime b92 explicitly documents that callers own fd
closure.

Exact narrow outbox port draft (not applied):

```python
from runtime_protocol import platform

...
with self.path.with_suffix(self.path.suffix + ".lock").open("a") as lock:
    platform.lock_file(lock.fileno())
    try:
        yield
    finally:
        platform.unlock_file(lock.fileno())
```

This preserves the existing exclusive/blocking lock and file-context lifetime
while moving the OS operation to Runtime. The current outbox's directory and
atomic-write behavior was not broadened or corrected. The independent owner
gate should retain the existing outbox lock serialization/release assertions
and rerun the boundary scan; no assertion weakening is proposed.

### 8–9. Windows attempt directory private-from-creation, configured and ephemeral

**Disposition: actual Agent platform-security defect, with a strict existing
assertion—not a stale mock.** Current
`astrid/core/execution/generic_host.py:5319-5337` calls `Path.mkdir()` and
POSIX `chmod(0o700)` regardless of the patched Windows platform. It never
calls Runtime's `platform.private_directory`, so the test's `created` list is
empty. Main497's same method called `platform.private_directory(root)` for the
configured Windows base and for a Windows ephemeral root, preserving private
creation through Runtime's Windows DACL implementation. Plain mkdir/chmod is
not an equivalent Windows private-creation operation.

Exact small source direction (not applied): restore the Main497 branch points:

```python
if sys.platform == "win32":
    platform.private_directory(root)
else:
    root.mkdir()
    root.chmod(0o700)
```

and, for the no-`attempt_root` Windows path, allocate under
`Path(tempfile.gettempdir())` and call `platform.private_directory(root)`
before returning. The two existing parametrized tests already provide the
equivalent owner assertions (`root.exists()`, exactly one helper call, and
the expected parent); they remain unchanged.

## All failures and non-results

```text
FAILED tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]
  setup blocked by sandbox AF_INET PermissionError; no source assertion reached.
FAILED tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]
  setup blocked by sandbox AF_INET PermissionError; no source assertion reached.
FAILED tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-register]
  source defect: untransferred fd not closed.
FAILED tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-bind-launch]
  source defect: untransferred fd not closed.
FAILED tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-register]
  source defect: untransferred fd not closed.
FAILED tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-bind-launch]
  source defect: untransferred fd not closed.
FAILED tests/core/execution/test_platform_boundary.py::test_agent_native_process_and_lock_boundary
  Viewing-owned root_preparation os.getuid; Agent-owned outbox fcntl.
FAILED tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[False]
  source defect: Windows private_directory helper not called.
FAILED tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[True]
  source defect: Windows private_directory helper not called.
```

No source/test edits, no assertion changes, no broad security correction, and
no full or named suite request were made. The only shared-environment write was
the required Viewing peer note and this report. The worktree remains clean.

## Recommended next steps

1. Viewing decides the `root_preparation.py` platform-boundary repair from the
   peer evidence.
2. Agent owner reviews the two narrow drafts: pidfd `finally` cleanup and
   outbox Runtime lock API port; preserve all existing strict assertions.
3. After any approved Agent patch, rerun only the nine compact nodes outside
   the sandbox restriction, still with Runtime b92 explicitly selected.
4. Do not use the retained full21969 `denied == False` result as current
   source evidence until the wrapper nodes reach their assertion.
