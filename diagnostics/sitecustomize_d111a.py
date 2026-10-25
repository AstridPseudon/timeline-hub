"""Passive whole-request sampler for the private D111a native diagnostic."""
from __future__ import annotations

import atexit
import json
import os
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path


CONFIG_PATH = Path(__file__).with_name("d111a-config.json")
try:
    CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8")) if CONFIG_PATH.exists() else {}
except (OSError, ValueError):
    CONFIG = {}
DEFAULT_ROOT = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111a-element-sample-0811/evidence")
DEFAULT_MARKER = DEFAULT_ROOT / "d111a-request.marker"
PROFILE_ENABLED = True
ROOT = Path(os.environ.get("D111A_PROFILE_ROOT", CONFIG.get("root", DEFAULT_ROOT)))
MARKER = Path(os.environ.get("D111A_REQUEST_MARKER", CONFIG.get("marker", DEFAULT_MARKER)))
INTERVAL = float(os.environ.get("D111A_SAMPLING_INTERVAL", "0.02"))
REAL_RUNTIME = Path(os.environ.get("D111_REAL_RUNTIME", CONFIG.get("runtime", "/home/user/work/wt/rt-pin-1daca2a3"))).resolve()
AGENT_ROOT = Path(os.environ.get("ASTRID_CHECKOUT", CONFIG.get("agent", "/home/user/work/wt/agt-pin-070dfc5e"))).resolve()
INTERESTING = {
    "finite_json", "validate_commit_value", "_historical_sequential",
    "_verify_accepted_replay", "validate_sequential_capture", "_verify_accepted",
    "_verify_accepted_record", "_validate_closure", "_verify_parent_rows",
    "_validate", "_validate_sequential_execution", "_capture_records",
    "_check_history_objects", "canonical_json", "digest", "_timeline_commit",
    "_execute_timeline_commit", "execute", "accept", "_publish",
    "_read_history_object", "_read", "validate",
}

LOCK = threading.RLock()
STOP = threading.Event()
CALL_STACK: dict[int, list[dict[str, object]]] = defaultdict(list)
REQUESTS: list[dict[str, object]] = []
ACTIVE: dict[int, dict[str, object]] = {}
COUNTS: defaultdict[str, int] = defaultdict(int)
CPU_NS: defaultdict[str, int] = defaultdict(int)
STACK_COUNTS: defaultdict[tuple[str, str, int], int] = defaultdict(int)
SAMPLE_TOTAL = 0
LOST_SAMPLES = 0
SAMPLER_CPU_NS = 0
SAMPLER_ERRORS: list[str] = []
COMMIT_CALLS = 0


def marker_active() -> bool:
    try:
        return MARKER.read_text(encoding="utf-8") == "active"
    except OSError:
        return False


def safe_frame(frame) -> tuple[str, str, int] | None:
    code = frame.f_code
    filename = code.co_filename.replace("\\", "/")
    if "/runtime_protocol/" in filename:
        root = str(REAL_RUNTIME).replace("\\", "/").rstrip("/") + "/"
        filename = filename.replace(root, "<runtime>/")
    elif "/astrid/" in filename:
        root = str(AGENT_ROOT).replace("\\", "/").rstrip("/") + "/"
        filename = filename.replace(root, "<agent>/")
    elif "/lib/python" in filename:
        filename = "<stdlib>/" + filename.rsplit("/", 1)[-1]
    else:
        return None
    return filename, code.co_name, frame.f_lineno


def identity() -> dict[str, object]:
    try:
        stat = Path(f"/proc/{os.getpid()}/stat").read_text().rsplit(")", 1)[1].split()
        birth_ticks = int(stat[19])
    except (OSError, ValueError, IndexError):
        birth_ticks = None
    try:
        executable = os.path.basename(os.readlink(f"/proc/{os.getpid()}/exe"))
    except OSError:
        executable = None
    return {"pid": os.getpid(), "birth_ticks": birth_ticks, "executable": executable}


def label(frame) -> str | None:
    code = frame.f_code
    filename = code.co_filename.replace("\\", "/")
    name = code.co_name
    if "/runtime_protocol/" in filename and name in INTERESTING:
        return filename.rsplit("/", 1)[-1] + ":" + name
    if "/astrid/sdk/timeline/" in filename and name == "commit":
        return "<agent>/commit.py:commit"
    return None


def profile(frame, event, arg) -> None:
    global COMMIT_CALLS
    del arg
    current_label = label(frame)
    if current_label is None:
        return
    thread_id = threading.get_ident()
    stack = CALL_STACK[thread_id]
    if event == "call":
        request = stack[-1]["request"] if stack else None
        if frame.f_code.co_name == "_timeline_commit":
            COMMIT_CALLS += 1
        target_commit = frame.f_code.co_name == "_timeline_commit" and (marker_active() or COMMIT_CALLS >= 2)
        if target_commit:
            request = {
                "ordinal": len(REQUESTS), "commit_call_ordinal": COMMIT_CALLS,
                "start_ns": time.perf_counter_ns(),
                "pid": os.getpid(), "identity": identity(), "counts": defaultdict(int),
                "inclusive_cpu_ns": defaultdict(int), "wall_ns": defaultdict(int),
            }
            with LOCK:
                REQUESTS.append(request)
                ACTIVE[thread_id] = request
        node = {"frame": id(frame), "label": current_label,
                "cpu": time.thread_time_ns(), "wall": time.perf_counter_ns(),
                "children": 0, "request": request}
        stack.append(node)
        if request is not None:
            request["counts"][current_label] += 1
        COUNTS[current_label] += 1
        return
    if event != "return" or not stack or stack[-1]["frame"] != id(frame):
        return
    node = stack.pop()
    cpu = max(0, time.thread_time_ns() - int(node["cpu"]))
    wall = max(0, time.perf_counter_ns() - int(node["wall"]))
    exclusive = max(0, cpu - int(node["children"]))
    if stack:
        stack[-1]["children"] += cpu
    CPU_NS[current_label] += cpu
    request = node["request"]
    if request is not None:
        request["inclusive_cpu_ns"][current_label] += cpu
        request["wall_ns"][current_label] += wall
        if frame.f_code.co_name == "_timeline_commit":
            request["end_ns"] = time.perf_counter_ns()
            request["elapsed_ns"] = int(request["end_ns"]) - int(request["start_ns"])
            request["selected_exclusive_cpu_ns"] = exclusive
            ACTIVE.pop(thread_id, None)


def sample_stack() -> None:
    global SAMPLE_TOTAL, LOST_SAMPLES, SAMPLER_CPU_NS
    previous = time.perf_counter()
    while not STOP.is_set():
        started_cpu = time.thread_time_ns()
        now = time.perf_counter()
        elapsed = now - previous
        previous = now
        if elapsed > INTERVAL * 1.5:
            LOST_SAMPLES += max(0, int(elapsed / INTERVAL) - 1)
        if marker_active() or ACTIVE:
            frames = sys._current_frames()
            with LOCK:
                request_threads = set(ACTIVE)
            for thread_id in request_threads:
                frame = frames.get(thread_id)
                if frame is None:
                    continue
                SAMPLE_TOTAL += 1
                while frame is not None:
                    item = safe_frame(frame)
                    if item is not None:
                        STACK_COUNTS[item] += 1
                    frame = frame.f_back
        STOP.wait(INTERVAL)
        SAMPLER_CPU_NS += time.thread_time_ns() - started_cpu


def start_sampler() -> None:
    try:
        thread = threading.Thread(target=sample_stack, name="d111a-passive-sampler", daemon=True)
        thread.start()
    except BaseException as error:  # pragma: no cover - startup failure is serialized
        SAMPLER_ERRORS.append(type(error).__name__)


def as_plain(value):
    if isinstance(value, defaultdict):
        return {key: as_plain(item) for key, item in value.items()}
    if isinstance(value, dict):
        return {key: as_plain(item) for key, item in value.items()}
    return value


def write_profile() -> None:
    STOP.set()
    ROOT.mkdir(parents=True, exist_ok=True)
    frames = []
    with LOCK:
        for (filename, function, line), count in sorted(STACK_COUNTS.items(), key=lambda item: (-item[1], item[0])):
            frames.append({
                "file": filename, "function": function, "line": line,
                "sample_count": count, "sample_total": SAMPLE_TOTAL,
                "sample_wall_share": count / SAMPLE_TOTAL if SAMPLE_TOTAL else 0.0,
                "sample_wall_ms": count * INTERVAL * 1000,
            })
        payload = {
            "pid": os.getpid(), "process_identity": identity(),
            "sampling_interval_ms": INTERVAL * 1000, "lost_samples": LOST_SAMPLES,
            "observer_cpu_ms": SAMPLER_CPU_NS / 1_000_000,
            "observer_overhead_limit": "sampling interval fixed at 20ms; CPU reported, no reset/cache hook",
            "sample_total": SAMPLE_TOTAL, "top_inclusive_frames": frames[:80],
            "function_counts": dict(COUNTS), "function_inclusive_cpu_ns": dict(CPU_NS),
            "requests": [as_plain(item) for item in REQUESTS],
            "sampler_errors": SAMPLER_ERRORS,
            "inclusive_overlap": "frame sample counts overlap by design; shares are not additive and are not self CPU",
        }
    path = ROOT / f"profile-{os.getpid()}.json"
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


if PROFILE_ENABLED:
    sys.setprofile(profile)
    threading.setprofile(profile)
    start_sampler()
    atexit.register(write_profile)
