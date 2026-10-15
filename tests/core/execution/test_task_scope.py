from __future__ import annotations

import os
import subprocess
import sys
import time

import pytest

from astrid.core.execution import generic_host, task_scope
from astrid.core.execution.task_scope import TaskScopeUnresolved, spawn

PY = sys.executable
pytestmark = pytest.mark.skipif(not sys.platform.startswith(("darwin", "linux")), reason="posix only")

GRANDCHILDREN = (
    "import subprocess,sys,time;"
    "c=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)']);"
    "print(c.pid,flush=True);time.sleep(60)"
)
STUBBORN = (
    "import signal,sys,time,subprocess;"
    "signal.signal(signal.SIGTERM,signal.SIG_IGN);"
    "c=subprocess.Popen([sys.executable,'-c','import signal,time;"
    "signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(60)']);"
    "print(c.pid,flush=True);time.sleep(60)"
)
ESCAPEE = (
    "import subprocess,sys,time;"
    "c=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'],start_new_session=True);"
    "print(c.pid,flush=True);time.sleep(60)"
)


def alive(pid: int) -> bool:
    out = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return bool(out) and not out.startswith("Z")


def launch(code: str):
    process = spawn([PY, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process, int(process.stdout.readline())


def test_group_with_grandchildren_is_killed_at_teardown():
    process, child = launch(GRANDCHILDREN)
    assert alive(child)
    assert task_scope.stop(process, 1.0).status == "settled"
    assert not alive(child) and process.returncode is not None


def test_kill_escalation_for_term_ignorers():
    process, child = launch(STUBBORN)
    time.sleep(0.3)
    started = time.monotonic()
    assert task_scope.stop(process, 0.3).status == "settled"
    assert time.monotonic() - started >= 0.3
    assert not alive(child)


def test_cancel_midrun_leaves_nothing():
    process, child = launch(GRANDCHILDREN)
    assert process.poll() is None
    generic_host._terminate_process_group(process, grace_seconds=0.5)
    assert not alive(child) and not alive(process.pid)


def test_leader_exits_before_helper():
    code = ("import subprocess,sys;"
            "c=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)']);"
            "print(c.pid,flush=True)")
    process, helper = launch(code)
    process.wait()
    assert alive(helper)
    assert task_scope.stop(process, 0.5).status == "settled"
    assert not alive(helper)


def test_setsid_escapee_is_reported_unresolved_and_not_signalled():
    process, escapee = launch(ESCAPEE)
    try:
        with pytest.raises(TaskScopeUnresolved) as raised:
            generic_host._terminate_process_group(process, grace_seconds=0.3)
        report = raised.value.report
        assert report.status == "unresolved"
        assert [s.pid for s in report.survivors] == [escapee]
        assert str(escapee) in str(raised.value)
        assert alive(escapee)  # a census finding is never signal authority
        # Unresolved fails the task, it is not a host-latching custody error.
        assert not issubclass(TaskScopeUnresolved, generic_host.CleanupUncertainError)
    finally:
        os.kill(escapee, 9)
