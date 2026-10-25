"""Private D111a sampling-only wall phase and separate value accounting phase."""
from __future__ import annotations

import atexit
import copy
import hashlib
import json
import os
import sys
import threading
import time
from collections import Counter
from functools import wraps
from itertools import pairwise
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("d111a-config.json")
CONFIG = json.loads(CONFIG_PATH.read_text()) if CONFIG_PATH.exists() else {}
ROOT = Path(CONFIG.get("root", os.environ.get("D111A_PROFILE_ROOT", "/tmp")))
MARKER = Path(CONFIG.get("marker", os.environ.get("D111A_REQUEST_MARKER", "/tmp/d111a-inactive")))
RUN_ID = CONFIG.get("run_id", os.environ.get("D111A_RUN_ID", "unidentified"))
MODE = CONFIG.get("mode", "sample")
INTERVAL = 0.02
STOP = threading.Event()
ACTIVE = {}
REQUESTS = []
ERRORS = []
LOCAL = threading.local()


def private_json(path, value):
    with path.open("w", encoding="utf-8", opener=lambda p, flags: os.open(p, flags, 0o600)) as stream:
        json.dump(value, stream, sort_keys=True)
        stream.write("\n")


def identity():
    stat = Path("/proc/self/stat").read_text().rsplit(")", 1)[1].split()
    return {"pid": os.getpid(), "birth_ticks": int(stat[19]),
            "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}


def normalized(frame):
    name = frame.f_code.co_filename.replace("\\", "/")
    for anchor, prefix in (("/runtime_protocol/", "<runtime>/"), ("/astrid/", "<agent>/")):
        if anchor in name:
            name = prefix + name.split(anchor, 1)[1]
            break
    else:
        if "/lib/python" in name:
            name = "<stdlib>/" + name.rsplit("/", 1)[-1]
        else:
            return None
    # Definition line, rather than executing line: recursive function membership.
    return f"{name}:{frame.f_code.co_name}:{frame.f_code.co_firstlineno}"


def sample_stack():
    while not STOP.is_set():
        cpu = time.thread_time_ns()
        frames = sys._current_frames()
        for tid, request in list(ACTIVE.items()):
            now = time.monotonic_ns()
            frame = frames.get(tid)
            if frame is None:
                request["missing_thread_samples"] += 1
                continue
            members = set()
            while frame is not None:
                item = normalized(frame)
                if item is not None:
                    members.add(item)
                frame = frame.f_back
            request["samples"].append({"monotonic_ns": now, "thread_id": tid,
                                       "frames": sorted(members)})
            request["observer_cpu_ns"] += time.thread_time_ns() - cpu
        STOP.wait(INTERVAL)


def account(request, operation, value, provenance):
    cpu, wall = time.thread_time_ns(), time.monotonic_ns()
    row = {"ordinal": len(request["values"]), "operation": operation, "provenance": provenance,
           "encoding": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')"}
    try:
        data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
        row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except (TypeError, ValueError, UnicodeError, RecursionError) as error:
        row.update(bytes=None, sha256=None, exact_limit=type(error).__name__)
    request["values"].append(row)
    request["accounting_cpu_ns"] += time.thread_time_ns() - cpu
    request["accounting_wall_ns"] += time.monotonic_ns() - wall


def counter(operation, function, output=False):
    @wraps(function)
    def measured(*args, **kwargs):
        request = getattr(LOCAL, "request", None)
        depths = getattr(LOCAL, "depths", {})
        if request is None:
            return function(*args, **kwargs)
        request["calls"][operation] += 1
        depth = depths.get(operation, 0)
        depths[operation] = depth + 1
        LOCAL.depths = depths
        provenance = {}
        try:
            if depth == 0:
                request["outer_calls"][operation] += 1
                caller = sys._getframe(1)
                provenance = {"caller": normalized(caller), "caller_line": caller.f_lineno,
                              "value_side": "return" if output else "argument[0]"}
                if output:
                    call = args[1]
                    provenance["callback"] = f"{call.__module__}:{call.__qualname__}"
                else:
                    account(request, operation, args[0], provenance)
            result = function(*args, **kwargs)
            if depth == 0 and output:
                account(request, operation, result, provenance)
            return result
        finally:
            depths[operation] = depth
    return measured


def summarize(request):
    samples = [s for s in request["samples"] if request["start_ns"] <= s["monotonic_ns"] <= request["end_ns"]]
    start, end = request["start_ns"], request["end_ns"]
    counts = Counter(frame for sample in samples for frame in sample["frames"])
    times = [s["monotonic_ns"] for s in samples]
    gaps = [b - a for a, b in pairwise(times)]
    union = sum(any(":deepcopy:" in f or ":finite_json:" in f for f in s["frames"]) for s in samples)
    # Coverage means the union of nominal observation windows, not continuous observation.
    windows = [(max(start, t - 10_000_000), min(end, t + 10_000_000)) for t in times]
    covered, right = 0, start
    for left, bound in windows:
        covered += max(0, bound - max(right, left))
        right = max(right, bound)
    values = {}
    for operation in request["outer_calls"]:
        rows = [r for r in request["values"] if r["operation"] == operation]
        distinct = {r["sha256"]: r["bytes"] for r in rows if r["bytes"] is not None}
        values[operation] = {"values_captured": len(rows), "unknown_values": sum(r["bytes"] is None for r in rows),
                             "repeated_total_bytes": sum(r["bytes"] or 0 for r in rows),
                             "distinct_serialized_values": len(distinct), "unique_serialized_bytes": sum(distinct.values())}
    return {k: v for k, v in request.items() if k not in ("samples", "values")} | {
        "sample_total": len(samples), "runtime_elapsed_ms": (end - start) / 1e6,
        "first_sample_ns": times[0] if times else None, "last_sample_ns": times[-1] if times else None,
        "sample_intervals_ns": gaps, "max_gap_ns": max(gaps, default=0),
        "expected_interval_ns": 20_000_000, "nominal_window_coverage_ns": covered,
        "nominal_window_coverage_share": covered / (end - start),
        "uncovered_window_ns": end - start - covered,
        "deepcopy_finite_json_union_samples": union,
        "deepcopy_finite_json_union_frequency": union / len(samples) if samples else None,
        "top_inclusive_frames": [{"frame_sha256": hashlib.sha256(f.encode()).hexdigest(),
                                  "sample_count": c, "frequency": c / len(samples)}
                                 for f, c in counts.most_common(10)],
        "value_summary": values,
        "limits": "Instantaneous sample frequency estimates wall occupancy; frames overlap and are not additive. Nominal windows are not continuous observation. Bytes are JSON representation lengths, not allocation/IO bytes. Unique means distinct serialized values per operation, not unique object identity. Counts cover intercepted outer operations; stdlib recursion through bound default arguments is EXACTMISSING. Bytes cover outer operations only. Accounting CPU/wall includes serialization/hash only; remaining wrapper overhead unmeasured. Counter phase is observer-confounded and is never production wall."}


def install():
    from runtime_protocol import (
        server,
        timeline_commit_port,
        timeline_commit_validation,
    )

    print(f"D111asamples startup {MODE} {json.dumps(identity(), sort_keys=True)}", file=sys.stderr, flush=True)
    send = server.RuntimeHandler._send

    @wraps(send)
    def tagged_send(self, status, *args, **kwargs):
        tag = self.headers.get("X-D111A-Refusal-Tag")
        if tag:
            print(f"D111asamples refusal {tag} status={status}", file=sys.stderr, flush=True)
        return send(self, status, *args, **kwargs)

    server.RuntimeHandler._send = tagged_send
    original = server.RuntimeHandler._dispatch
    if MODE == "counter":
        old_copy = copy.deepcopy
        copy.deepcopy = counter("deepcopy", old_copy)
        old_finite = timeline_commit_validation.finite_json
        timeline_commit_validation.finite_json = counter("finite_json", old_finite)
        # Account for aliases already imported before sitecustomize installed wrappers.
        for module in list(sys.modules.values()):
            namespace = getattr(module, "__dict__", {})
            if str(namespace.get("__name__", "")).startswith(("runtime_protocol.", "astrid.")):
                for key, value in list(namespace.items()):
                    if value is old_copy:
                        namespace[key] = copy.deepcopy
                    elif value is old_finite:
                        namespace[key] = timeline_commit_validation.finite_json
        timeline_commit_port.RequestCommitPort._read = counter("port_read", timeline_commit_port.RequestCommitPort._read, output=True)

    @wraps(original)
    def dispatch(self):
        if self.command != "POST" or not self.path.endswith("/commit"):
            return original(self)
        try:
            active = MARKER.read_text().strip() == "active"
        except OSError:
            active = False
        if not active:
            return original(self)
        request = {"run_id": RUN_ID, "mode": MODE, "boundary": "server._dispatch",
                   "process_identity": identity(), "thread_id": threading.get_ident(),
                   "start_ns": time.monotonic_ns(), "end_ns": None, "samples": [], "values": [],
                   "calls": Counter(), "outer_calls": Counter(), "missing_thread_samples": 0,
                   "observer_cpu_ns": 0, "accounting_cpu_ns": 0, "accounting_wall_ns": 0}
        REQUESTS.append(request)
        LOCAL.request = request
        if MODE == "sample":
            ACTIVE[threading.get_ident()] = request
        try:
            return original(self)
        finally:
            request["end_ns"] = time.monotonic_ns()
            ACTIVE.pop(threading.get_ident(), None)
            LOCAL.request = None

    server.RuntimeHandler._dispatch = dispatch
    if MODE == "sample":
        threading.Thread(target=sample_stack, daemon=True, name="d111a-sampler").start()


def write_profile():
    STOP.set()
    ROOT.mkdir(parents=True, exist_ok=True)
    complete = [r for r in REQUESTS if r["end_ns"] is not None]
    if complete:
        ident = identity()
        stem = f"{os.getpid()}-{ident['birth_ticks']}"
        private_json(ROOT / f"raw-samples-{stem}.json", complete)
        private_json(ROOT / f"profile-{stem}.json", {
            "run_id": RUN_ID, "mode": MODE, "pid": os.getpid(), "process_identity": ident,
            "sys_setprofile": False, "requests": [summarize(r) for r in complete],
            "request_count": len(complete), "sampler_errors": ERRORS})


if CONFIG.get("enabled"):
    install()
    atexit.register(write_profile)
