# OPS-retire-process repair 1840

PASS — private diagnostic and source checks only. Actual App2 HOST/remote execution: **UNRUN**. Independent Luna review is required before forwarding this staged author command to the App2 HOST lead. This supersedes return1832 (script SHA256 `582405d5d6478e80560a35bb2cb523adae7b7a80e7dda4a068449ece69b2ff69`) after independent1837 FAIL; it does not qualify the remote refusal cause or authorize cleanup.

## Exact staged command (not executed against HOST)

The first shell fence is the entire self-contained command. Its script is also retained as `handoff-runtime-OPS-retire-process-sol-1840-diagnostic.py`; the identical command is retained as `handoff-runtime-OPS-retire-process-sol-1840-command.sh`. The fixture seam must not be set for a future HOST observation. Retain command, stdout, stderr and exit status together. No HOST run is requested by this report.

```sh
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
```

## What changed and why

All namespace, mount, proc directory, cmdline open/read and executable observations pass through one immediate permission stop. `PermissionError` (even without errno), `EACCES`, and `EPERM` emit only accumulated allowlisted metadata and exit 3 before another observation. There is no permission-handler existence recheck, alternate probe, PID enumeration, or retry. Directory checks use explicit stat, because `isdir()` suppresses permission errors. Namespace/mount probes precede PID enumeration. File descriptor close is resource release, not another metadata observation.

Source inspection also exposed a return1832 overclaim: procfs cmdline `st_size=0` does not prove empty argv. The diagnostic now counts bytes without decoding or emitting payload, matching the handler's `wc -c` input distinction. It reads cmdline in chunks up to 1 MiB per PID; exceeding the bound is explicit unknown, exit 3. Unlike return1832, it does open/read cmdline solely to count it. It never emits cmdline bytes, arguments, executable paths, credentials, exception text, namespace payload, or raw mountinfo. Executable readlink values are discarded. Mount/namespace files are opened for availability only; their contents are never read. Limits remain 4,096 visible PIDs and at most two metadata output lines; there is no elapsed-time guarantee.

The output key allowlist is `proc_root_visible proc_root_readable proc_entries_visible mountinfo_visible mountinfo_readable pid_ns_self_visible pid_ns_init_visible pid_ns_same pid pid_exists_before pid_exists_after_cmdline pid_exists_after_exe cmdline_empty cmdline_bytes exe_errno race classification result observation`. Missing fields mean not observed, never an inferred negative. `observation` identifies the last attempted operation with a fixed label. Permission errno is retained for executable denial when available.

## Source semantics and limits

Installed handler SHA256 remains `954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791`; installed request remains `21f61833a6718794ab2a06a3a96d34ca58c050ccd0151622e16866ac78758139`. The source route remains `request-retire-venv -> RETIREVENV -> retire-child-venv`.

For verified empty cmdline, a failed exe read with a still-existing process continues only the handler's exe branch; subsequent cwd/fd/reference/age/containment checks still apply. For non-empty cmdline, exe failure with present PID refuses. A disappearing PID is skipped by installed source, while this diagnostic stops with exit 4 and explicit unknown-race. A metadata ENOENT alone does not prove process disappearance; the diagnostic labels it `pid-or-metadata-unavailable`. Directory disappearance observations are `pid-vanished`; PID reuse and other races remain possible even when `race=not-observed`.

The diagnostic is deliberately stricter on permission denial than the unchanged empty-cmdline handler branch. It has no target parameter and does not check target references, cwd, fds, ancestry exclusion, queue state, age or deletion guards. It observes sorted visible numeric entries, not necessarily the handler's first refusal. A readable executable referencing a candidate therefore produces `no-failing-exe-observed`, **not** target-use clearance. Readlink success does not establish symlink target existence or liveness. Root readability and namespace inode comparison do not establish complete proc visibility or absence of hidepid restrictions. Empty/hidden proc views, unknowns, limits, successful exit 0, and race observations never authorize retirement.

## Fresh evidence and exact commands

All fixture directories and extraction files are below `/tmp/w-ef8d3fdfde`; no live `/proc`, HOST, remote, installed handler, or request was executed. Only `bash -n` inspected installed shell scripts. The permanent test script executes the exact diagnostic bytes, plus the exact shell command once on private on-disk fixtures. These are author checks, not independent review.

Commands executed (all final checks exit 0):

```bash
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
D="$O/design/handoff-runtime-OPS-retire-process-sol-1840"
python3 "$D-checks.py" "$D-diagnostic.py" "$D-command.sh" /tmp/w-ef8d3fdfde/permanent-tests > "$D-checks.txt"
python3 "$D-verify.py" > "$D-sourcechecks.txt"
```

The checks cover 24 successful-trace observations x three independent denial forms (72); three more denials after exe failure; sentinel enforcement that any subsequent observation fails; mountinfo stat/open, both PID namespaces, proc root stat/open/scandir/iteration, both PIDs, cmdline open/read, exe readlink, and post-observation existence checks. All emitted keys and values are allowlisted, with secret/path sentinels checked on every model run. Additional cases: empty/nonempty + exe ENOENT (exits 0/2), hidden root (3), missing cmdline and PID races before/after cmdline/after exe (4), readable target-use explicitly unqualified (0), empty visible table (0), cmdline byte limit and PID scan limit (3), unknown exe error (2), mountinfo ENOENT and namespace EIO (3). Real private files include secret payloads and a dangling exe symlink; exact shell command exits 0 with no payload disclosure. No permissions are changed to simulate denial.

`-verify.py` compiles only the diagnostic/check/verify bytes in memory; compares staged/permanent script and command with `cmp`; extracts this handoff's first command fence and compares it exactly; verifies predecessor/handler/request hashes; runs handler/request `bash -n`; checks actual source structure and request/dispatcher route; runs Runtime `git diff --check`, `git diff --exit-code`, and `git status --porcelain` (all exit 0, empty output); and asserts HEAD `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. Source checks do not dynamically exercise deletion-policy branches. Raw results are in `-checks.txt` and `-sourcechecks.txt` beside this report.

During authoring, one private checker assertion used wrong trace indexes and failed (exit 1); correcting the checker to the actual stat indexes yielded the final passing run. A path-discovery probe for absent `bin/handle-request`/`bin/daemon*` returned exit 2; the actual route was read from `bin/dispatcher-daemon`. Neither failure affected installed state or qualification claims.

No full/product suite was requested or run. No product/test/generated/pin files, production queue, target, cleanup/chmod, retirement, daemon, provisioning, tool installation, or tracked files changed. Production route/guards, full C0v2 shapes and frozen34e remain unchanged. Evidence-only: never merge this worker. Next: independent Luna reviews these exact bytes, then the orchestrator decides whether to send the command to App2 HOST lead. Remote cause remains unknown.

## New exact-byte hashes

Script SHA256: `15890ed6fa650527751e6c3c6de3312ed9e2dc87a0176133eaf28c494f57c55f`.

Command SHA256: `a7a3a54d6f04c0be0f753519f3214d4c4403cf8395c85173a12043d0b3fcff27`.

Other artifact hashes and byte sizes are recorded by the scoped verifier in `-sourcechecks.txt`. Permanent evidence is below 1 MiB. No execution result here is a HOST result.
