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
  tests/test_platform_signaling.py \
  tests/test_platform_windows.py \
  tests/test_platform_filesystem.py \
  tests/test_m1_review.py \
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
Linux 5.3+ is required for detached stop/restart. When Python lacks a pidfd
wrapper, the platform module calls libc `syscall()` on verified Linux ABIs.
Unverified ABIs fail closed; signaling still pins a pidfd before checking the
process birth identity, and never falls back to signaling a bare PID.
Retained-descriptor consumers share the public Linux helpers
`platform.pidfd_open(pid, flags=0)` and
`platform.pidfd_send_signal(fd, signum, siginfo=None, flags=0)`. The opener
transfers descriptor ownership to its caller; the sender leaves it open.
Callers must check process identity after opening the pidfd and before
signaling. `signal_process` owns the combined pin, identity-check and signal
sequence. The syscall fallback accepts only `None` for siginfo.
Windows uses process creation FILETIMEs and SID-derived numeric user identity,
identity-checked process handles, and kill-on-close Job Objects. Children start
suspended until assigned to their Job. A detached owner inherits the Job handle
and clears its inheritance before launching descendants.

The existing `dirfd.py` Windows filesystem adapter is **M2 (unqualified)**.
It remains in place for subsequent native qualification; it is not part of
M1's completed portability claims. Its intended design uses retained native
directory handles to reject reparse points and prevent parent renames.
SQLite connections close
across fresh-realm publication on Windows while the owner file lock remains
held. Backup verification copies pinned SQLite bytes to a private immutable
snapshot; it never relies on `/dev/fd` there.

Windows credential and discovery directories and files are created with an
explicit protected DACL granting access only to the token owner and SYSTEM.
Existing credential/discovery files are read through the same handle whose
owner and DACL are validated with `GetSecurityInfo`. Unsafe owners, public or
unprotected/NULL DACLs, unfamiliar ACEs and reparse points fail closed with a
reason; existing shared credential directories are rejected. Stat metadata
alone cannot authorize Windows credentials. This uses ctypes and native APIs,
without new dependencies. See Microsoft's [handle-based security API](https://learn.microsoft.com/windows/win32/api/aclapi/nf-aclapi-getsecurityinfo).

Both Windows listeners disable address reuse and enable exclusive address use
before binding. POSIX socket options are unchanged. Linux tree teardown holds
the Popen wait lock and observes the leader using `waitid(WNOWAIT)` until the
final group signal, then reaps it. Already-reaped or externally-reaped children
cannot authorize group signals. macOS keeps its previous tree teardown path.

Foreground startup scopes cancellation through launcher/admission locks,
snapshot copying, SQLite progress, CAS inspection and readiness polling.
Cancellation exits nonzero with a reason and runs cleanup outside the scope.
Readiness GETs poll with short transport timeouts during this scope, retaining
their original total request budgets. Outside startup their timeouts are unchanged.

Windows directory admission
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

## Verification boundary

This page gives maintained commands and platform boundaries; it is not a
qualification report. The Linux M4 target runs the default Runtime lane plus
the relevant integration lane on an unrestricted runner. macOS may run the
portable subset above, but `darwin_native` tests require native macOS APIs and
the sandbox cannot stand in for that evidence. Windows-only APIs and the
Windows filesystem adapter require the native CI jobs.

Do not infer Timeline, browser, renderer, physical audio/video parity, or
owner-film qualification from a portable subset. Record the exact commit,
platform, command, and result for each native run.

