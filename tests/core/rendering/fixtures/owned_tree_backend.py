"""Test writer tree with backend and browser session escapes."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path


def main() -> None:
    role, output_raw, registry_raw = sys.argv[1:4]
    output = Path(output_raw)
    registry = Path(registry_raw)
    registry.mkdir(parents=True, exist_ok=True)
    (registry / f"{role}.pid").write_text(str(os.getpid()))
    if role == "worker":
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        expected_roles = ("backend", "node", "browser", "worker")
        while not all((registry / f"{name}.pid").is_file() for name in expected_roles):
            time.sleep(0.01)
        (output / "writer.txt").write_text("owned fixture writer")
        (registry / "last-write.txt").write_text(str(time.monotonic_ns()))
        ready = registry / "ready.tmp"
        ready.write_text("ready")
        ready.replace(registry / "ready.txt")
        while True:
            (output / "writer.txt").write_text("owned fixture writer")
            (registry / "last-write.txt").write_text(str(time.monotonic_ns()))
            time.sleep(0.01)
        return

    # Child readiness also proves each ancestor installed its cleanup handler.
    signal.signal(signal.SIGTERM, lambda *_: None)
    child_role = {"pack": "backend", "backend": "node", "node": "browser", "browser": "worker"}[role]
    child = subprocess.Popen(
        [sys.executable, __file__, child_role, str(output), str(registry)],
        start_new_session=child_role in {"backend", "browser"},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Keep each ancestor available until its owned child exits.
    try:
        while child.poll() is None:
            time.sleep(0.01)
    finally:
        if child.poll() is None:
            child.kill()
        child.wait()


if __name__ == "__main__":
    main()
