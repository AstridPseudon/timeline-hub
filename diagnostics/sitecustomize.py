"""Private D112 observation hooks; active only when the metric path is set."""
from __future__ import annotations

import json
import os
import signal
import time
from pathlib import Path


def _install() -> None:
    metric_path = os.environ.get("D112_METRIC_PATH")
    if not metric_path:
        return

    from runtime_protocol.timeline_commit_store import (
        TimelineCommitStore,
        _HistoryReadCursor,
    )

    counters = {"verification_calls": 0, "verification_records": 0, "history_object_reads": 0, "cursor_reads": 0,
                "store_version_checks": 0}

    def dump(_signum: int, _frame: object) -> None:
        payload = {"monotonic": time.monotonic(), "pid": os.getpid(), "counters": dict(counters)}
        destination = Path(metric_path)
        temporary = destination.with_name(destination.name + ".tmp")
        temporary.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, destination)

    def count(name: str, method):
        def wrapped(self, *args, **kwargs):
            counters[name] += 1
            return method(self, *args, **kwargs)

        return wrapped

    TimelineCommitStore._verify_accepted = count("verification_calls", TimelineCommitStore._verify_accepted)
    TimelineCommitStore._verify_accepted_record = count("verification_records", TimelineCommitStore._verify_accepted_record)
    TimelineCommitStore._read_history_object = count("history_object_reads", TimelineCommitStore._read_history_object)
    TimelineCommitStore._store_version = count("store_version_checks", TimelineCommitStore._store_version)
    _HistoryReadCursor._read = count("cursor_reads", _HistoryReadCursor._read)
    signal.signal(signal.SIGUSR1, dump)
    dump(signal.SIGUSR1, None)


try:
    _install()
except (ImportError, OSError, RuntimeError):
    # An observation hook must never change Runtime admission or startup.
    del _install
