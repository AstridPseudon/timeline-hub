"""Explicit central launcher for the current integration transport tests."""
from pathlib import Path
import os
import subprocess
import sys


def test_operation_handle_integration():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([
        sys.executable, "-m", "pytest", "-q", "-o", "addopts=", "-p", "no:cacheprovider",
        "-m", "integration", "tests/test_operation_handle_integration.py",
    ], cwd=root, env={
        **os.environ,
        "ASTRID_CHECKOUT": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-init-current-private-qualification/agent-source",
    }, capture_output=True, text=True)
    print(result.stdout)
    assert result.returncode == 0, result.stdout + result.stderr
