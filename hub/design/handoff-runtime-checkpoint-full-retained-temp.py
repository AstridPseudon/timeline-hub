#!/usr/bin/env python3
"""Run a pytest command with a private, retained real-filesystem temp root."""

import os
import signal
import stat
import subprocess
import sys
import tempfile


def _pytest_command(command, root):
    try:
        module = command.index("-m")
    except ValueError:
        return command
    if command[module + 1 : module + 2] == ["pytest"]:
        return [*command, "--basetemp", root]
    return command


def _report(root):
    print(
        f"runtime-full-retained-temp: retained owned root {root}",
        file=sys.stderr,
        flush=True,
    )


def main(command):
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        print(
            "usage: runtime-full-retained-temp.py -- command [args ...]",
            file=sys.stderr,
        )
        return 2

    root = tempfile.mkdtemp(prefix="rt-full-", dir="/tmp")
    os.chmod(root, stat.S_IRWXU)
    environment = os.environ.copy()
    for name in ("TMPDIR", "TMP", "TEMP"):
        environment[name] = root

    def reportable_signal(signum, _frame):
        raise SystemExit(128 + signum)

    for signum in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, reportable_signal)

    try:
        completed = subprocess.run(
            _pytest_command(command, root), env=environment, check=False
        )
    finally:
        _report(root)

    if completed.returncode < 0:
        signum = -completed.returncode
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
