# Runtime handoff: OPS-retire-process return 1832

## Exact bounded HOST diagnostic

Run the following command once, on the actual App2 HOST lead. It selects the first
failing PID in sorted visible PID order. It is read-only and has no target, queue,
daemon, request, cleanup, retry, chmod, install, or provision operation. Do not set
`TL_RETIRE_DIAG_PROC_ROOT` on HOST; the command therefore uses the real `/proc`.
Retain stdout, stderr, exit status, and the command text together. A nonzero exit is
diagnostic evidence, not cleanup approval.

The command emits one namespace/proc visibility line and at most one PID observation.
It never opens or copies cmdline bytes, never prints cmdline contents, executable
paths/contents, process arguments, credentials, credential files, or raw mountinfo.
It stops at the first permission/tool refusal. A vanished PID is explicitly
`classification=pid-vanished result=unknown-race`; it is not a cleanup decision.

```sh
python3 - <<'PY'
#!/usr/bin/env python3
"""Bounded, read-only process observation; never disclose proc payloads."""
import errno
import os

PROC_ROOT = os.environ.get("TL_RETIRE_DIAG_PROC_ROOT", "/proc")
MAX_PIDS = 4096


def emit(**fields):
    allowed = {
        "proc_root_visible", "proc_root_readable", "proc_entries_visible",
        "mountinfo_visible", "mountinfo_readable", "pid_ns_self_visible",
        "pid_ns_init_visible", "pid_ns_same", "pid", "pid_exists_before",
        "pid_exists_after_cmdline", "pid_exists_after_exe", "cmdline_empty",
        "cmdline_bytes", "exe_errno", "race", "classification", "result",
    }
    if set(fields) - allowed:
        raise RuntimeError("internal output field")
    print(" ".join(f"{key}={fields[key]}" for key in fields), flush=True)


def visible(path):
    try:
        os.stat(path)
        return "yes"
    except FileNotFoundError:
        return "no"
    except PermissionError:
        return "denied"
    except OSError as exc:
        return f"error-{errno.errorcode.get(exc.errno, 'UNKNOWN')}"


def readable_without_payload(path):
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0))
    os.close(fd)


def namespace_summary():
    root_visible = visible(PROC_ROOT)
    if root_visible != "yes":
        emit(proc_root_visible=root_visible, proc_root_readable="no",
             proc_entries_visible="no", mountinfo_visible="unknown",
             mountinfo_readable="unknown", pid_ns_self_visible="unknown",
             pid_ns_init_visible="unknown", pid_ns_same="unknown",
             result="stop-proc-root-unavailable")
        raise SystemExit(3)
    try:
        readable_without_payload(PROC_ROOT)
        with os.scandir(PROC_ROOT) as entries:
            names = [entry.name for entry in entries]
    except PermissionError:
        emit(proc_root_visible="yes", proc_root_readable="denied",
             proc_entries_visible="denied", mountinfo_visible="unknown",
             mountinfo_readable="unknown", pid_ns_self_visible="unknown",
             pid_ns_init_visible="unknown", pid_ns_same="unknown",
             result="stop-permission-denied")
        raise SystemExit(3)
    except OSError as exc:
        emit(proc_root_visible="yes", proc_root_readable="error",
             proc_entries_visible=f"error-{errno.errorcode.get(exc.errno, 'UNKNOWN')}",
             mountinfo_visible="unknown", mountinfo_readable="unknown",
             pid_ns_self_visible="unknown", pid_ns_init_visible="unknown",
             pid_ns_same="unknown", result="stop-proc-tool-refusal")
        raise SystemExit(3)

    def probe(path):
        state = visible(path)
        if state != "yes":
            return state, "unknown"
        try:
            readable_without_payload(path)
        except PermissionError:
            return "yes", "denied"
        except OSError as exc:
            return "yes", f"error-{errno.errorcode.get(exc.errno, 'UNKNOWN')}"
        return "yes", "yes"

    mount_visible, mount_readable = probe(os.path.join(PROC_ROOT, "self", "mountinfo"))
    ns_self_visible, ns_self_readable = probe(os.path.join(PROC_ROOT, "self", "ns", "pid"))
    ns_init_visible, ns_init_readable = probe(os.path.join(PROC_ROOT, "1", "ns", "pid"))
    same_ns = "unknown"
    if ns_self_readable == "yes" and ns_init_readable == "yes":
        try:
            a = os.stat(os.path.join(PROC_ROOT, "self", "ns", "pid"))
            b = os.stat(os.path.join(PROC_ROOT, "1", "ns", "pid"))
            same_ns = "yes" if (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino) else "no"
        except PermissionError:
            same_ns = "denied"
        except OSError:
            same_ns = "unknown"
    emit(proc_root_visible="yes", proc_root_readable="yes",
         proc_entries_visible="yes", mountinfo_visible=mount_visible,
         mountinfo_readable=mount_readable, pid_ns_self_visible=ns_self_visible,
         pid_ns_init_visible=ns_init_visible, pid_ns_same=same_ns)
    return names


def main():
    names = namespace_summary()
    pids = sorted((int(name) for name in names if name.isdecimal()), key=int)
    for pid in pids[:MAX_PIDS]:
        proc = os.path.join(PROC_ROOT, str(pid))
        before = os.path.isdir(proc)
        if not before:
            continue
        try:
            cmdline_bytes = os.stat(os.path.join(proc, "cmdline")).st_size
            empty = "yes" if cmdline_bytes == 0 else "no"
            after_cmdline = os.path.isdir(proc)
        except PermissionError:
            emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="denied",
                 pid_exists_after_exe="unknown", cmdline_empty="unknown",
                 cmdline_bytes="unknown", exe_errno="unknown", race="unknown",
                 classification="permission-denied", result="stop-permission-denied")
            return 3
        except FileNotFoundError:
            emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="no",
                 pid_exists_after_exe="unknown", cmdline_empty="unknown",
                 cmdline_bytes="unknown", exe_errno="ENOENT", race="yes",
                 classification="pid-vanished", result="unknown-race")
            return 4
        except OSError as exc:
            emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="unknown",
                 pid_exists_after_exe="unknown", cmdline_empty="unknown",
                 cmdline_bytes="unknown", exe_errno=errno.errorcode.get(exc.errno, "UNKNOWN"),
                 race="unknown", classification="cmdline-tool-refusal",
                 result="stop-tool-refusal")
            return 3
        if not after_cmdline:
            emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="no",
                 pid_exists_after_exe="unknown", cmdline_empty=empty,
                 cmdline_bytes=cmdline_bytes, exe_errno="unknown", race="yes",
                 classification="pid-vanished", result="unknown-race")
            return 4
        try:
            os.readlink(os.path.join(proc, "exe"))
            after_exe = os.path.isdir(proc)
        except PermissionError:
            after_exe = os.path.isdir(proc)
            emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="yes",
                 pid_exists_after_exe="yes" if after_exe else "no",
                 cmdline_empty=empty, cmdline_bytes=cmdline_bytes, exe_errno="EACCES",
                 race="yes" if not after_exe else "no",
                 classification="permission-denied", result="stop-permission-denied")
            return 3
        except OSError as exc:
            after_exe = os.path.isdir(proc)
            err = errno.errorcode.get(exc.errno, "UNKNOWN")
            if not after_exe:
                emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="yes",
                     pid_exists_after_exe="no", cmdline_empty=empty,
                     cmdline_bytes=cmdline_bytes, exe_errno=err, race="yes",
                     classification="pid-vanished", result="unknown-race")
                return 4
            if empty == "yes":
                emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="yes",
                     pid_exists_after_exe="yes", cmdline_empty="yes",
                     cmdline_bytes=cmdline_bytes, exe_errno=err, race="no",
                     classification="approved-empty-cmdline-exe-failure",
                     result="handler-continues")
                return 0
            emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="yes",
                 pid_exists_after_exe="yes", cmdline_empty="no",
                 cmdline_bytes=cmdline_bytes, exe_errno=err, race="no",
                 classification="executable-unreadable", result="refused")
            return 2
        if not after_exe:
            emit(pid=pid, pid_exists_before="yes", pid_exists_after_cmdline="yes",
                 pid_exists_after_exe="no", cmdline_empty=empty,
                 cmdline_bytes=cmdline_bytes, exe_errno="none", race="yes",
                 classification="pid-vanished", result="unknown-race")
            return 4
    emit(pid="none", pid_exists_before="none", pid_exists_after_cmdline="none",
         pid_exists_after_exe="none", cmdline_empty="none", cmdline_bytes="none",
         exe_errno="none", race="no", classification="none",
         result="no-failing-exe-observed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

PY
```

The extracted Python script bytes are exactly the bytes between the heredoc markers
above (including the final newline), SHA-256:

```
582405d5d6478e80560a35bb2cb523adae7b7a80e7dda4a068449ece69b2ff69
```

The script's output allowlist is fixed to:
`proc_root_visible proc_root_readable proc_entries_visible mountinfo_visible
mountinfo_readable pid_ns_self_visible pid_ns_init_visible pid_ns_same pid
pid_exists_before pid_exists_after_cmdline pid_exists_after_exe cmdline_empty
cmdline_bytes exe_errno race classification result`.

Interpretation is deliberately limited:

- `classification=executable-unreadable result=refused` with non-empty cmdline
  matches the installed handler's refusal branch.
- `classification=approved-empty-cmdline-exe-failure result=handler-continues`
  matches the installed handler's approved empty-cmdline case; it does not authorize
  cleanup.
- `classification=pid-vanished result=unknown-race` says only that this observation
  raced with process exit. Source skips a vanished PID only where the handler actually
  does; this does not prove remote proc visibility or safety.
- `stop-permission-denied`, `stop-tool-refusal`, or an unknown/error visibility
  value is a hard stop. Do not scan around it or retry it.
- `result=no-failing-exe-observed` is not proof that a target is absent, live, safe,
  or remotely visible. Symlink liveness and target use remain unproven by this
  diagnostic.

The installed source remains unchanged: `request-retire-venv -> RETIREVENV ->
retire-child-venv`, handler SHA-256
`954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791`, request
SHA-256 `21f61833a6718794ab2a06a3a96d34ca58c050ccd0151622e16866ac78758139`.
No production guard/state is changed. Runtime C0v2 request/reply and frozen34e remain
unchanged.

