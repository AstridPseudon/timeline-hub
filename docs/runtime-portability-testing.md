# Runtime portability checks

The portability CI job runs the platform boundary, native process custody,
foreground lifecycle, and installed-wheel lifecycle checks on Ubuntu, macOS,
and Windows. It invokes the selected tests with `-m ""` because pytest's
default configuration excludes integration-marked tests.

Run the same host-specific subset locally after installing the test and
generated-client packages:

```sh
python -m pip install -e '.[test]'
python -m pip install -e packages/python
python -m pytest -q -m "" \
  tests/test_platform.py \
  tests/test_platform_windows.py \
  tests/test_platform_filesystem.py \
  tests/test_foreground.py \
  tests/test_native_custody.py \
  tests/test_portable_lifecycle.py
```

The broader `tests/test_real_bootstrap.py` cases remain marked
`darwin_native`: they exercise the previous Darwin-specific bootstrap and
restart paths directly. The portable lifecycle module instead validates the
installed command surface on each CI host. Platform-specific Windows and
POSIX process-tree cases in `tests/test_platform.py` retain their own
skip-if-other-host markers.

## OS boundary

`runtime_protocol/platform.py` owns `file_lock` (including owner-only file
creation), `lock_file`/`unlock_file` for retained descriptors,
`spawn_tree`/`stop_tree`, `process_identity`, `owner_only`/`is_owner_only`,
`current_user`, `data_root`, and `log_dir`. Narrow helpers handle isolated
session creation, process observation/signaling, and stop handlers. No new
runtime dependency is required. `RuntimePaths.current` replaces the old
macOS-specific constructor; there is no compatibility alias.

macOS keeps its audit-token owner broker and durable birth-marker spelling.
Linux uses `/proc` birth ticks and identity-checked pidfds for adopted signals;
Linux 5.3+ with Python's pidfd support is required for detached stop/restart.
Windows uses process creation FILETIMEs and SID-derived numeric user identity,
identity-checked process handles, and kill-on-close Job Objects. Children start
suspended until assigned to their Job. A detached owner inherits the Job handle
and clears its inheritance before launching descendants.

The existing `dirfd.py` filesystem boundary also has a Windows implementation:
retained native directory handles reject reparse points and prevent parent
renames while descriptor-relative operations execute. SQLite connections close
across fresh-realm publication on Windows while the owner file lock remains
held. Backup verification copies pinned SQLite bytes to a private immutable
snapshot; it never relies on `/dev/fd` there.

Windows permission helpers are intentional no-ops. The installation and logs
must be in the user's private profile (normally LOCALAPPDATA); this port does
not configure ACLs for arbitrary shared data roots. Windows directory admission
uses an abandoned-aware named mutex plus an in-process gate; those directory
locks must be released by their acquiring thread. Ordinary file locks use
LockFileEx. Windows sends CTRL_BREAK for cooperative stopping where a console
exists and otherwise terminates through the identity-checked native handle.

## Remaining execution work

The Runtime and browser-door lifecycle has native backends. Windows local
Worker descriptor transfer and independent listener custody still fail closed
with explicit errors: SCM_RIGHTS/Unix peer credentials have no Windows
implementation here. The delegated host/relay audit-token role broker remains
macOS-specific, so those execution profiles also need the agent-port transport
work on Linux. These paths are not required to serve projects, timelines, or
media through the door. Installer/service registration and real GPU/chat
qualification belong to the subsequent installer and agent workstreams.

## Verification in the restricted macOS worktree

Port-binding and process-signaling integration tests are written and collected
but require an unrestricted runner. Exploratory server tests were rejected by
the sandbox before binding; the full macOS suite could not be completed here.
Windows-native APIs cannot be executed on this host. The three-host CI job is
the remaining native validation gate, not a claim that it has already passed.
The safe test selection and final result are recorded below.

Final safe selection: **453 passed, 13 skipped, 9 deselected** on macOS.
Skipped tests need Windows APIs; deselected tests include the process-tree,
installed lifecycle, and Darwin-native lanes, plus the real TCP health test.
Compilation, `git diff --check`, and `scripts/artifact_manifest.py --check`
also passed. The pytest session's pre-existing process guard could not invoke
`ps` under the sandbox and printed a warning.

```sh
.venv/bin/python -m pytest -q \
  tests/test_bootstrap.py tests/test_runtime_boundary.py \
  tests/test_role_custody_authority.py tests/test_data_root.py \
  tests/test_foreground.py tests/test_native_custody.py \
  tests/test_dirfd_publication.py tests/test_platform.py \
  tests/test_platform_windows.py tests/test_platform_filesystem.py \
  tests/test_realm_tiered_admission.py tests/test_workspace_adopt.py \
  tests/test_relocation_plan.py tests/test_local_worker_composition.py \
  tests/test_local_execution_supervisor.py tests/test_verified_host_launch.py \
  tests/test_portable_lifecycle.py -k 'not slow_healthy_runtime'
```

## Files left uncommitted

### Runtime source

- `astrid_runtime/__init__.py`
- `astrid_runtime/bootstrap.py`
- `astrid_runtime/cli.py`
- `astrid_runtime/custody_broker.py`
- `astrid_runtime/io.py`
- `astrid_runtime/operator_upgrade.py`
- `astrid_runtime/paths.py`
- `astrid_runtime/relocation.py`
- `astrid_runtime/runtime_boundary.py`
- `astrid_runtime/workspace_adopt.py`
- `runtime_protocol/auth.py`
- `runtime_protocol/backup.py`
- `runtime_protocol/cas.py`
- `runtime_protocol/catalog.py`
- `runtime_protocol/cli.py`
- `runtime_protocol/daemon.py`
- `runtime_protocol/dirfd.py`
- `runtime_protocol/door.py`
- `runtime_protocol/fsclone.py`
- `runtime_protocol/local_execution_handoff.py`
- `runtime_protocol/local_execution_supervisor.py`
- `runtime_protocol/local_worker.py`
- `runtime_protocol/local_worker_composition.py`
- `runtime_protocol/local_worker_handoff.py`
- `runtime_protocol/platform.py`
- `runtime_protocol/service.py`
- `runtime_protocol/snapshot_refs.py`
- `runtime_protocol/store.py`
- `runtime_protocol/upgrade.py`

### Tests

- `tests/conftest.py`
- `tests/process_groups.py`
- `tests/test_astrid_activation_join.py`
- `tests/test_bootstrap.py`
- `tests/test_data_root.py`
- `tests/test_door_lifecycle.py`
- `tests/test_foreground.py`
- `tests/test_installed_wheel_source_parity.py`
- `tests/test_local_execution_supervisor.py`
- `tests/test_local_worker_composition.py`
- `tests/test_local_worker_placement.py`
- `tests/test_native_custody.py`
- `tests/test_operator_upgrade.py`
- `tests/test_platform.py`
- `tests/test_platform_filesystem.py`
- `tests/test_platform_windows.py`
- `tests/test_portable_lifecycle.py`
- `tests/test_process_group_cleanup.py`
- `tests/test_realm_admission_hardening.py`
- `tests/test_relocation_plan.py`
- `tests/test_relocation_real_e2e.py`
- `tests/test_replay_policy_process.py`
- `tests/test_role_custody_authority.py`
- `tests/test_runtime_boundary.py`
- `tests/test_runtime_e2e.py`
- `tests/test_runtime_upgrade.py`
- `tests/test_t4_replacement_foundation.py`
- `tests/test_workspace_adopt.py`
- `tests/test_workspace_lifecycle.py`

### Documentation and CI

- `.github/workflows/ci.yml`
- `README.md`
- `docs/runtime-portability-testing.md`

