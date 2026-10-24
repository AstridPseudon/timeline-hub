"""Private opt-in pytest plugin; capture only the original P4 server handlers.

Load by absolute import using the existing D73 launcher's Python command.
P4_LIVE_PROFILE_DIR must name a new private output directory on the Agent host.
No client/provider/transport substitution, new daemon, or profiler attachment.
"""
from __future__ import annotations

import cProfile
import functools
import hashlib
import json
import os
from pathlib import Path
import pstats
import sys
import threading
import time

import pytest

TARGET = "tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo"
TESTS = (
    "test_p4_cli_sheet_v2_runtime.py",
    "test_p4_ten_note_v2_runtime.py",
    "test_p4_note_rerun_v2_runtime.py",
)
_capture = None


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def origins():
    prefixes = ("runtime_protocol", "astrid.sdk.timeline", "astrid_runtime_client",
                "tests.helpers.runtime", "tests.editing_conformance.test_native_batch_ingress")
    return {name: source(module.__file__) for name, module in tuple(sys.modules.items())
            if name.startswith(prefixes) and getattr(module, "__file__", None)
            and Path(module.__file__).is_file()}


def counters(stats):
    targets = {
        "history_entry": ("timeline_commit_store.py", "history_entry"),
        "_verify_accepted": ("timeline_commit_store.py", "_verify_accepted"),
        "accept_calls": ("timeline_commit_store.py", "accept"),
        "commit_timeline_calls": ("service.py", "commit_timeline"),
    }
    return {label: sum(value[1] for (filename, _, function), value in stats.stats.items()
                       if Path(filename).name == module and function == name)
            for label, (module, name) in targets.items()}


def top10(stats):
    return [{"file": file, "line": line, "function": function,
             "primitive_calls": values[0], "total_calls": values[1],
             "self_seconds": values[2], "cumulative_seconds": values[3]}
            for (file, line, function), values in sorted(
                stats.stats.items(), key=lambda item: item[1][3], reverse=True)[:10]]


class Capture:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=False)
        self.lock = threading.Lock()
        self.sequence = 0
        self.rows = []

    def event(self, row):
        with self.lock, (self.directory / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    def handler(self, original):
        @functools.wraps(original)
        def measured(handler, *args, **kwargs):
            # Only a handler belonging to the fixture's actual daemon is eligible.
            daemon = getattr(handler.server, "daemon_runtime", None)
            if (daemon is None or daemon.httpd is not handler.server
                    or daemon.service is not handler.server.runtime):
                return original(handler, *args, **kwargs)
            with self.lock:
                self.sequence += 1
                sequence = self.sequence
            key = handler.headers.get("Idempotency-Key", "")
            boundary = {"sequence": sequence, "pid": os.getpid(),
                        "thread_id": threading.get_ident(),
                        "daemon_instance": daemon.instance_id,
                        "method": handler.command, "path": handler.path,
                        "idempotency_key": key,
                        "shared_note_count": 10 if key == "p4-ten-note-commit" else None}
            began = time.perf_counter()
            self.event({"event": "handler_begin", **boundary})
            profile = cProfile.Profile()
            started = time.perf_counter()
            error = None
            try:
                return profile.runcall(original, handler, *args, **kwargs)
            except BaseException as exc:
                error = type(exc).__name__
                raise
            finally:
                stopped = time.perf_counter()
                profile.disable()
                filename = f"handler-{sequence:04d}.prof"
                profile.dump_stats(str(self.directory / filename))
                stats = pstats.Stats(profile)
                row = {"event": "handler_end", **boundary, "profile": filename,
                       "profiled_handler_wall_seconds": stopped - started,
                       "capture_seconds_excluding_end_event": time.perf_counter() - began - (stopped - started),
                       "error_type": error, "calls": counters(stats)}
                with self.lock:
                    self.rows.append(row)
                self.event(row)
        return measured

    def finish(self, wall, reports):
        paths = sorted(self.directory.glob("handler-*.prof"))
        merged = pstats.Stats(str(paths[0])) if paths else None
        if merged is not None:
            for path in paths[1:]:
                merged.add(str(path))
            merged.dump_stats(str(self.directory / "handlers.prof"))
        per_note = {}
        for row in self.rows:
            for operation in ("undo", "redo"):
                prefix = f"p4-ten-note-{operation}-"
                if row["idempotency_key"].startswith(prefix):
                    note = row["idempotency_key"][len(prefix):]
                    per_note.setdefault(note, {})[operation] = {
                        "sequence": row["sequence"], "calls": row["calls"],
                        "profiled_handler_wall_seconds": row["profiled_handler_wall_seconds"],
                        "error_type": row["error_type"],
                    }
        summary = {"scope": "actual RuntimeHandler._dispatch calls during original ten-note call",
                   "test_protocol_wall_seconds": wall, "original_timeout_seconds": 45,
                   "reports": reports, "handler_count": len(paths),
                   "calls": counters(merged) if merged else {},
                   "top10_cumulative": top10(merged) if merged else [],
                   "boundaries": sorted(self.rows, key=lambda row: row["sequence"]),
                   "per_note_undo_redo": per_note,
                   "module_origins_after": origins(),
                   "limitations": ["cProfile overhead is uncalibrated; no uninstrumented latency claim",
                                   "handler profiles cover the calling thread only",
                                   "accept/commit counts are entries, not proof of durable acceptance",
                                   "initial ten-note commit is shared; do not invent per-note allocation",
                                   "test protocol wall includes fixtures; profiles exclude client-only work",
                                   "hard process exit may leave a begin without an end/profile"]}
        (self.directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item):
    global _capture
    if item.nodeid != TARGET or not os.environ.get("P4_LIVE_PROFILE_DIR"):
        yield
        return
    capture = Capture(os.environ["P4_LIVE_PROFILE_DIR"])
    _capture = capture
    tests = Path(str(item.config.rootpath)) / "tests/editing_conformance"
    manifest = os.environ.get("P4_D73_MANIFEST")
    capture.event({"event": "test_begin", "nodeid": item.nodeid, "pid": os.getpid(),
                   "utc_ns": time.time_ns(), "argv": sys.argv,
                   "helper": source(__file__), "original_tests": [source(tests / name) for name in TESTS],
                   "d73_manifest": Path(manifest).read_text() if manifest else None,
                   "d73_request_id": os.environ.get("P4_D73_REQUEST_ID")})
    capture.reports = []
    started = time.perf_counter()
    try:
        yield
    finally:
        capture.finish(time.perf_counter() - started, capture.reports)
        capture.event({"event": "test_end", "original_tests_after": [source(tests / name) for name in TESTS]})
        _capture = None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    if item.nodeid != TARGET or _capture is None:
        yield
        return
    # Fixture setup has loaded its selected Runtime. Do not pre-import another tree.
    from runtime_protocol.server import RuntimeHandler
    original = RuntimeHandler._dispatch
    _capture.event({"event": "handler_scope_installed", "pid": os.getpid(),
                    "thread_id": threading.get_ident(), "module_origins_before": origins(),
                    "original_dispatch": {"file": original.__code__.co_filename,
                                          "line": original.__code__.co_firstlineno}})
    RuntimeHandler._dispatch = _capture.handler(original)
    try:
        yield
    finally:
        RuntimeHandler._dispatch = original


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if item.nodeid == TARGET and _capture is not None:
        report = outcome.get_result()
        _capture.reports.append({"phase": report.when, "outcome": report.outcome,
                                 "seconds": report.duration})
