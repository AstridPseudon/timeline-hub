"""Spike: confirm fcntl.flock honors exclusive locks across processes on macOS APFS."""

from __future__ import annotations

import fcntl
import json
import multiprocessing
import os
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path


def _append_event_workload(path: str, iterations: int = 1, *, hold_seconds: float = 0.0) -> None:
    """Simulate append_event workload: open, flock, append JSON line, flush, fsync, unlock."""
    payload = {
        "kind": "test_event",
        "pid": os.getpid(),
        "timestamp": time.time(),
    }
    for i in range(iterations):
        with open(path, "a", encoding="utf-8") as fh:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            try:
                if hold_seconds > 0:
                    time.sleep(hold_seconds)
                json.dump(payload, fh, sort_keys=True, separators=(",", ":"))
                fh.write("\n")
                fh.flush()
                os.fsync(fh.fileno())
            finally:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        payload["iteration"] = i


def _append_worker(
    path: str,
    barrier: multiprocessing.Barrier,
    result_queue: multiprocessing.Queue,
    worker_id: int,
    iterations: int,
    hold_seconds: float = 0.0,
) -> None:
    """Worker that appends iterations times, synchronized by barrier."""
    barrier.wait()  # synchronize start
    try:
        _append_event_workload(path, iterations, hold_seconds=hold_seconds)
        result_queue.put({"worker_id": worker_id, "status": "ok"})
    except Exception as exc:
        result_queue.put({"worker_id": worker_id, "status": f"error: {exc}"})


def _check_no_interleaved_lines(path: str) -> bool:
    """Verify that every line in the file is a valid JSON object."""
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError:
                return False
    return True


def _write_worker_script() -> Path:
    """Write a temporary multi-line Python script for subprocess-based flock tests."""
    script_content = textwrap.dedent("""\
    import fcntl
    import json
    import os
    import sys

    path = sys.argv[1]
    iterations = int(sys.argv[2])
    payload = {"kind": "test", "pid": os.getpid(), "idx": 0}
    for i in range(iterations):
        payload["idx"] = i
        with open(path, "a") as fh:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(payload, fh, sort_keys=True, separators=(",", ":"))
                fh.write("\\n")
                fh.flush()
                os.fsync(fh.fileno())
            finally:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
    """)
    script = Path(tempfile.mkdtemp(prefix="astrid-flock-spike-")) / "flock_worker.py"
    script.write_text(script_content)
    return script


def test_flock_exclusive_prevents_interleaved_writes() -> None:
    """Two child processes flock(LOCK_EX)+append to same file, 100 iterations, assert no interleaved lines."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        events_path = tf.name

    worker_script = _write_worker_script()

    try:
        p1 = subprocess.Popen(
            [sys.executable, str(worker_script), events_path, "100"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        p2 = subprocess.Popen(
            [sys.executable, str(worker_script), events_path, "100"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        p1_out, p1_err = p1.communicate(timeout=30)
        p2_out, p2_err = p2.communicate(timeout=30)

        assert p1.returncode == 0, f"P1 failed: {p1_err.decode() if p1_err else 'unknown'}"
        assert p2.returncode == 0, f"P2 failed: {p2_err.decode() if p2_err else 'unknown'}"

        # Verify no interleaved lines: every line must be valid JSON
        assert _check_no_interleaved_lines(events_path), (
            "Interleaved writes detected — flock did not provide mutual exclusion!"
        )

        # Check total event count (200 events = 100 from each)
        with open(events_path, "r", encoding="utf-8") as fh:
            line_count = sum(1 for line in fh if line.strip())
        assert line_count == 200, f"Expected 200 events, got {line_count}"
    finally:
        os.unlink(events_path)
        worker_script.unlink(missing_ok=True)
        worker_script.parent.rmdir()


def test_flock_blocks_until_release() -> None:
    """A contender sees the held lock, then acquires only after the holder releases it."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        events_path = tf.name

    p1 = p2 = None
    release = None
    try:
        ctx = multiprocessing.get_context("spawn")
        held, attempted, release, acquired = (ctx.Event() for _ in range(4))
        p1 = ctx.Process(target=_flock_event_holder, args=(events_path, held, release))
        p2 = ctx.Process(target=_flock_event_contender, args=(events_path, held, attempted, acquired))
        p1.start()
        p2.start()
        assert attempted.wait(10), "contender did not observe the held lock"
        assert not acquired.is_set(), "contender acquired while the holder owned the lock"
        release.set()
        assert acquired.wait(10), "contender did not acquire after release"
        p1.join(timeout=10)
        p2.join(timeout=10)
        assert p1.exitcode == 0 and p2.exitcode == 0
    finally:
        if release is not None:
            release.set()
        for process in (p1, p2):
            if process is not None:
                process.join(timeout=5)
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=5)
        os.unlink(events_path)


def _flock_event_holder(path: str, held, release) -> None:
    with open(path, "a", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        held.set()
        assert release.wait(10)
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def _flock_event_contender(path: str, held, attempted, acquired) -> None:
    assert held.wait(10)
    with open(path, "a", encoding="utf-8") as fh:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            attempted.set()
        else:
            raise AssertionError("nonblocking flock succeeded while holder owned lock")
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        acquired.set()
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def _flock_holder(path: str, barrier: multiprocessing.Barrier, nb_queue: multiprocessing.Queue) -> None:
    """P1: acquire lock and hold it. Then write an event."""
    with open(path, "a", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            # Signal P2 that we're holding the lock
            barrier.wait()

            # Give P2 time to attempt acquisition
            time.sleep(0.5)

            # Write our event
            fh.write(json.dumps({"kind": "holder", "pid": os.getpid()}) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def _flock_nonblocking_attempter(path: str, barrier: multiprocessing.Barrier, nb_queue: multiprocessing.Queue) -> None:
    """P2: wait for P1 to acquire lock, then try LOCK_EX|LOCK_NB."""
    barrier.wait()  # Wait for P1 to acquire

    # Small sleep to ensure P1 has the lock
    time.sleep(0.05)

    try:
        fh = open(path, "a", encoding="utf-8")
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            # If we get here, the non-blocking acquire succeeded (unexpected)
            nb_queue.put({"status": "acquired_unexpectedly", "pid": os.getpid()})
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        except BlockingIOError:
            nb_queue.put({"status": "blocked_as_expected", "pid": os.getpid()})
        except OSError:
            nb_queue.put({"status": "blocked_as_expected", "pid": os.getpid()})
        finally:
            fh.close()
    except Exception as exc:
        nb_queue.put({"status": f"error: {exc}", "pid": os.getpid()})


def test_flock_nonblocking_fails_when_held() -> None:
    """LOCK_EX|LOCK_NB fails immediately when another process holds the lock."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tf:
        events_path = tf.name

    try:
        ctx = multiprocessing.get_context("spawn")
        barrier = ctx.Barrier(2)
        nb_result_queue: multiprocessing.Queue = ctx.Queue()

        p1 = ctx.Process(target=_flock_holder, args=(events_path, barrier, nb_result_queue))
        p2 = ctx.Process(target=_flock_nonblocking_attempter, args=(events_path, barrier, nb_result_queue))

        p1.start()
        p2.start()

        p1.join(timeout=10)
        p2.join(timeout=10)

        nb_results = []
        while not nb_result_queue.empty():
            nb_results.append(nb_result_queue.get_nowait())

        # Find the non-blocking attempt result
        nb_attempts = [r for r in nb_results if r.get("pid") != p1.pid]
        assert len(nb_attempts) > 0, "Non-blocking worker did not produce a result"

        nb_attempt = nb_attempts[0]
        assert nb_attempt["status"] == "blocked_as_expected", (
            f"Expected LOCK_EX|LOCK_NB to fail, but it {nb_attempt['status']}. "
            "Non-blocking flock acquisition should fail when lock is held."
        )
    finally:
        os.unlink(events_path)
