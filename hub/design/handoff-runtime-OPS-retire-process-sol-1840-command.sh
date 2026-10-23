python3 - <<'PY'
#!/usr/bin/env python3
"""Read-only observation: output metadata only; never authorize retirement."""
import errno
import os
import stat

PROC_ROOT = os.environ.get("TL_RETIRE_DIAG_PROC_ROOT", "/proc")
MAX_PIDS = 4096
MAX_CMDLINE = 1048576
ALLOWED = frozenset("proc_root_visible proc_root_readable proc_entries_visible mountinfo_visible mountinfo_readable pid_ns_self_visible pid_ns_init_visible pid_ns_same pid pid_exists_before pid_exists_after_cmdline pid_exists_after_exe cmdline_empty cmdline_bytes exe_errno race classification result observation".split())
FIELDS = {}


def emit(**fields):
    if set(fields) - ALLOWED:
        raise RuntimeError("internal output field")
    print(" ".join(f"{key}={value}" for key, value in fields.items()), flush=True)


def stop(result, classification="unknown", code=3):
    emit(**dict(FIELDS, classification=classification, result=result))
    raise SystemExit(code)


def observe(label, operation, *args):
    FIELDS["observation"] = label
    try:
        return operation(*args)
    except OSError as exc:
        # No further observation, including a PID existence check, on denial.
        if isinstance(exc, PermissionError) or exc.errno in (errno.EACCES, errno.EPERM):
            if label == "exe-readlink":
                FIELDS["exe_errno"] = errno.errorcode.get(exc.errno, "UNKNOWN")
            stop("stop-permission-denied", "permission-denied")
        raise


def probe(path, label):
    info = observe(label + "-stat", os.stat, path)
    fd = observe(label + "-open", os.open, path, os.O_RDONLY | os.O_CLOEXEC)
    os.close(fd)
    return info


def namespace_summary():
    info = probe(PROC_ROOT, "proc-root")
    if not stat.S_ISDIR(info.st_mode):
        stop("stop-proc-root-unavailable")
    FIELDS.update(proc_root_visible="yes", proc_root_readable="yes")
    # Probe namespace/mount metadata before enumerating any PID entries.
    probe(os.path.join(PROC_ROOT, "self", "mountinfo"), "mountinfo")
    FIELDS.update(mountinfo_visible="yes", mountinfo_readable="yes")
    a = probe(os.path.join(PROC_ROOT, "self", "ns", "pid"), "pid-ns-self")
    FIELDS["pid_ns_self_visible"] = "yes"
    b = probe(os.path.join(PROC_ROOT, "1", "ns", "pid"), "pid-ns-init")
    FIELDS.update(pid_ns_init_visible="yes",
                  pid_ns_same="yes" if (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino) else "no")
    def entries():
        with os.scandir(PROC_ROOT) as items:
            return [item.name for item in items]
    names = observe("proc-root-scan", entries)
    FIELDS["proc_entries_visible"] = "yes"
    emit(**FIELDS)
    return names


def pid_exists(proc, label):
    try:
        info = observe(label, os.stat, proc)
    except FileNotFoundError:
        stop("unknown-race", "pid-vanished", 4)
    if not stat.S_ISDIR(info.st_mode):
        stop("unknown-race", "pid-entry-changed", 4)
    return "yes"


def cmdline_length(path):
    # procfs st_size is commonly zero even for non-empty argv. Count bytes,
    # like the handler's wc -c, without decoding or emitting their contents.
    fd = observe("cmdline-open", os.open, path, os.O_RDONLY | os.O_CLOEXEC)
    count = 0
    try:
        while count <= MAX_CMDLINE:
            chunk = observe("cmdline-read", os.read, fd, min(65536, MAX_CMDLINE + 1 - count))
            if not chunk:
                return count
            count += len(chunk)
        stop("unknown-cmdline-limit")
    finally:
        os.close(fd)


def main():
    try:
        names = namespace_summary()
        pids = sorted(int(name) for name in names if name.isascii() and name.isdecimal())
        namespace_fields = dict(FIELDS)
        for pid in pids[:MAX_PIDS]:
            FIELDS.clear()
            FIELDS.update(namespace_fields, pid=pid)
            proc = os.path.join(PROC_ROOT, str(pid))
            FIELDS["pid_exists_before"] = pid_exists(proc, "pid-before")
            count = cmdline_length(os.path.join(proc, "cmdline"))
            FIELDS.update(cmdline_bytes=count, cmdline_empty="yes" if count == 0 else "no")
            FIELDS["pid_exists_after_cmdline"] = pid_exists(proc, "pid-after-cmdline")
            try:
                observe("exe-readlink", os.readlink, os.path.join(proc, "exe"))
            except OSError as exc:
                FIELDS["exe_errno"] = errno.errorcode.get(exc.errno, "UNKNOWN")
                FIELDS["pid_exists_after_exe"] = pid_exists(proc, "pid-after-exe")
                FIELDS["race"] = "not-observed"
                if count == 0:
                    stop("handler-continues-exe-branch", "observed-empty-cmdline-exe-failure", 0)
                stop("refused", "executable-unreadable", 2)
            FIELDS["pid_exists_after_exe"] = pid_exists(proc, "pid-after-exe")
        if len(pids) > MAX_PIDS:
            stop("unknown-scan-limit")
        stop("no-failing-exe-observed", "none", 0)
    except OSError as exc:
        if exc.errno == errno.ENOENT and "pid" in FIELDS:
            stop("unknown-race", "pid-or-metadata-unavailable", 4)
        stop("stop-tool-refusal", "unknown")


if __name__ == "__main__":
    main()
PY
