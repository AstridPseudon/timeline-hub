from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from runtime_protocol.store import RealmStore


def test_real_daemon_group_is_reaped_after_interrupted_journey(tmp_path, owned_process_groups):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    support = tmp_path / "support"
    support.mkdir()
    process = owned_process_groups.popen(
        [sys.executable, "-m", "runtime_protocol", "start", "--root", str(root), "--support-root", str(support)],
        cwd=Path(__file__).parents[1],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    pgid = os.getpgid(process.pid)
    time.sleep(0.2)
    assert process.poll() is None, "real runtime daemon did not stay up for interruption check"
    try:
        with pytest.raises(TimeoutError, match="simulated pytest timeout"):
            raise TimeoutError("simulated pytest timeout during daemon journey")
    finally:
            owned_process_groups.terminate_all()
    with pytest.raises(ProcessLookupError):
        os.killpg(pgid, 0)
