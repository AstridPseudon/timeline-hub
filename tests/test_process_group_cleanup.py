from __future__ import annotations

import os
import sys

import pytest


def test_isolated_child_group_is_reaped_after_interrupted_journey(owned_process_groups):
    process = owned_process_groups.popen(
        [sys.executable, "-c", "import time; time.sleep(60)"], start_new_session=True
    )
    pgid = os.getpgid(process.pid)
    try:
        with pytest.raises(TimeoutError, match="simulated pytest timeout"):
            raise TimeoutError("simulated pytest timeout during host journey")
    finally:
        owned_process_groups.terminate_all()
    with pytest.raises(ProcessLookupError):
        os.killpg(pgid, 0)
