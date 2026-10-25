"""Private, request-scoped whole-request sampler for D111a."""
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

DEFAULT_ROOT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/rt-D111a-scope-return-0827/evidence"
)
DEFAULT_MARKER = DEFAULT_ROOT / "d111a-request.marker"
ROOT = Path(os.environ.get("D111A_PROFILE_ROOT", CONFIG.get("root", DEFAULT_ROOT)))
MARKER = Path(os.environ.get("D111A_REQUEST_MARKER", CONFIG.get("marker", DEFAULT_MARKER)))
INTERVAL = float(os.environ.get("D111A_SAMPLING_INTERVAL", "0.02"))
REAL_RUNTIME = Path(
    os.environ.get("D111_REAL_RUNTIME", CONFIG.get("runtime", "/home/user/work/wt/rt-pin-1daca2a3"))
).resolve()
AGENT_ROOT = Path(
    os.environ.get("ASTRID_CHECKOUT", CONFIG.get("agent", "/home/user/work/wt/agt-pin-070dfc5e"))
).resolve()
RUN_ID = os.environ.get("D111A_RUN_ID", "unidentified")
SOURCE = os.environ.get("D111A_SOURCE", "tl/rt-D111a-scope-return-0827")

INTERESTING = {
    "_body", "_commit_body", "_dispatch", "_route", "_send", "_timeline_commit",
    "_execute_timeline_commit", "execute", "accept", "validate", "_read", "_publish",
    "_read_history_object", "_check_history_objects", "_historical_sequential",
    "_verify_accepted_replay", "_verify_accepted", "_verify_accepted_record",
    "_validate_closure", "_verify_parent_rows", "_validate", "_validate_sequential_execution",
    "_capture_records", "validate_sequential_capture", "validate_commit_value", "finite_json",
    "detached", "canonical_json", "digest", "deepcopy", "commit",
}

LOCK = threading.RLock()
STOP = threading.Event()
CALL_STACK: dict[int, list[dict[str, object]]] = defaultdict(list)
REQUESTS: list[dict[str, object]] = []
ACTIVE: dict[int, dict[str, object]] = {}
COUNTS: defaultdict[str, int] = defaultdict(int)
CPU_NS: defaultdict[str, int] = defaultdict(int)
ERRORS: list[str] = []


def marker_active() -> bool:
    try:
        return MARKER.read_text(encoding="utf-8").strip() == "active"
    except OSError:
        return False


def safe_frame(frame) -> tuple[str, str, int] | None:
    code = frame.f_code
    filename = code.co_filename.replace("\\", "/")
    runtime_root = str(REAL_RUNTIME).replace("\\", "/").rstrip("/") + "/"
    agent_root = str(AGENT_ROOT).replace("\\", "/").rstrip("/") + "/"
    if "/runtime_protocol/" in filename:
        filename = filename.replace(runtime_root, "<runtime>/")
    elif "/astrid/" in filename:
        filename = filename.replace(agent_root, "<agent>/")
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
    if filename.endswith("/copy.py") and name == "deepcopy":
        return "<stdlib>/copy.py:deepcopy"
    if "/astrid/sdk/timeline/" in filename and name == "commit":
        return "<agent>/commit.py:commit"
    return None


def new_request(boundary: str) -> dict[str, object]:
    now = time.perf_counter_ns()
    request = {
        "ordinal": len(REQUESTS),
        "run_id": RUN_ID,
        "source": SOURCE,
        "boundary": boundary,
        "start_ns": now,
        "end_ns": None,
        "pid": os.getpid(),
        "process_identity": identity(),
        "counts": defaultdict(int),
        "timing": {},
        "sample_total": 0,
        "lost_samples": 0,
        "sampling_interval_ms": INTERVAL * 1000,
        "observer_cpu_ns": 0,
        "sample_offsets_ms": [],
        "sampled_frames": defaultdict(int),
        "last_sample_ns": None,
        "internal_start_ns": None,
        "internal_end_ns": None,
    }
    with LOCK:
        REQUESTS.append(request)
    return request


def function_timing(request: dict[str, object], current_label: str) -> dict[str, float | int]:
    timings = request["timing"]
    assert isinstance(timings, dict)
    bucket = timings.get(current_label)
    if bucket is None:
        bucket = {
            "count": 0, "inclusive_cpu_ns": 0, "inclusive_wall_ns": 0,
            "self_cpu_ns": 0, "self_wall_ns": 0,
        }
        timings[current_label] = bucket
    assert isinstance(bucket, dict)
    return bucket


def profile(frame, event, arg) -> None:
    del arg
    thread_id = threading.get_ident()
    stack = CALL_STACK[thread_id]
    current_label = label(frame)
    if event == "call":
        if current_label is None:
            return
        if (current_label == "<stdlib>/copy.py:deepcopy" and stack
                and stack[-1]["label"] == current_label):
            # copy.deepcopy recurses through the same Python function. Keep one
            # outer timing/count per operation; its inclusive time includes the
            # recursive work without profiling every child call.
            return
        request = stack[-1]["request"] if stack else None
        if frame.f_code.co_name == "_dispatch" and marker_active() and request is None:
            request = new_request("server._dispatch")
            with LOCK:
                ACTIVE[thread_id] = request
        elif frame.f_code.co_name == "_timeline_commit" and marker_active() and request is None:
            request = new_request("service._timeline_commit_fallback")
            request["boundary_missing"] = True
            with LOCK:
                ACTIVE[thread_id] = request
        if request is None:
            return
        node = {
            "frame": id(frame),
            "name": frame.f_code.co_name,
            "label": current_label,
            "request": request,
            "cpu": time.thread_time_ns(),
            "wall": time.perf_counter_ns(),
            "children_cpu": 0,
            "children_wall": 0,
        }
        stack.append(node)
        if request is not None and current_label is not None:
            request["counts"][current_label] += 1
            if frame.f_code.co_name == "_timeline_commit" and request["internal_start_ns"] is None:
                request["internal_start_ns"] = node["wall"]
        if current_label is not None:
            COUNTS[current_label] += 1
        return
    if event != "return" or not stack or stack[-1]["frame"] != id(frame):
        return
    node = stack.pop()
    cpu = max(0, time.thread_time_ns() - int(node["cpu"]))
    wall = max(0, time.perf_counter_ns() - int(node["wall"]))
    self_cpu = max(0, cpu - int(node["children_cpu"]))
    self_wall = max(0, wall - int(node["children_wall"]))
    if stack:
        stack[-1]["children_cpu"] += cpu
        stack[-1]["children_wall"] += wall
    current_label = node["label"]
    request = node["request"]
    if current_label is not None:
        CPU_NS[current_label] += cpu
        if request is not None:
            bucket = function_timing(request, current_label)
            bucket["count"] += 1
            bucket["inclusive_cpu_ns"] += cpu
            bucket["inclusive_wall_ns"] += wall
            bucket["self_cpu_ns"] += self_cpu
            bucket["self_wall_ns"] += self_wall
    if request is not None and node["name"] == "_timeline_commit":
        request["internal_end_ns"] = time.perf_counter_ns()
    if request is not None and node["name"] == "_dispatch":
        request["end_ns"] = time.perf_counter_ns()
        with LOCK:
            ACTIVE.pop(thread_id, None)


def sample_stack() -> None:
    try:
        while not STOP.is_set():
            started_cpu = time.thread_time_ns()
            now = time.perf_counter_ns()
            frames = sys._current_frames()
            with LOCK:
                active = list(ACTIVE.items())
            for thread_id, request in active:
                previous = request["last_sample_ns"]
                if previous is not None:
                    request["lost_samples"] += max(
                        0, int((now - int(previous)) / (INTERVAL * 1_000_000_000)) - 1
                    )
                request["last_sample_ns"] = now
                request["sample_total"] += 1
                request["sample_offsets_ms"].append((now - int(request["start_ns"])) / 1_000_000)
                frame = frames.get(thread_id)
                while frame is not None:
                    item = safe_frame(frame)
                    if item is not None:
                        key = f"{item[0]}:{item[1]}:{item[2]}"
                        request["sampled_frames"][key] += 1
                    frame = frame.f_back
            observer_cpu = time.thread_time_ns() - started_cpu
            with LOCK:
                active = list(ACTIVE.values())
            for request in active:
                request["observer_cpu_ns"] += observer_cpu // max(1, len(active))
            STOP.wait(INTERVAL)
    except BaseException as error:  # pragma: no cover - serialized below
        ERRORS.append(type(error).__name__)


def as_plain(value):
    if isinstance(value, defaultdict):
        return {key: as_plain(item) for key, item in value.items()}
    if isinstance(value, dict):
        return {key: as_plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [as_plain(item) for item in value]
    return value


def summarize_request(request: dict[str, object]) -> dict[str, object]:
    result = as_plain(request)
    start_ns = int(result["start_ns"])
    end_ns = result["end_ns"]
    if end_ns is None:
        end_ns = time.perf_counter_ns()
        result["complete"] = False
    else:
        result["complete"] = True
    runtime_elapsed_ms = max(0, int(end_ns) - start_ns) / 1_000_000
    result["runtime_start_ns"] = start_ns
    result["runtime_end_ns"] = int(end_ns)
    result["end_ns"] = end_ns
    result["runtime_elapsed_ms"] = runtime_elapsed_ms
    result["sample_wall_ms"] = int(result["sample_total"]) * INTERVAL * 1000
    result["sample_wall_share"] = result["sample_wall_ms"] / runtime_elapsed_ms if runtime_elapsed_ms else 0.0
    result["observer_cpu_ms"] = int(result.pop("observer_cpu_ns", 0)) / 1_000_000
    result["internal_elapsed_ms"] = (
        (int(result["internal_end_ns"]) - int(result["internal_start_ns"])) / 1_000_000
        if result["internal_start_ns"] is not None and result["internal_end_ns"] is not None else None
    )
    result.pop("internal_start_ns", None)
    result.pop("internal_end_ns", None)
    result.pop("last_sample_ns", None)
    result.pop("start_ns", None)
    for bucket in result["timing"].values():
        for key in ("inclusive_cpu_ns", "inclusive_wall_ns", "self_cpu_ns", "self_wall_ns"):
            bucket[key.replace("_ns", "_ms")] = bucket.pop(key) / 1_000_000
    result["top_inclusive_frames"] = [
        {
            "frame": frame,
            "sample_count": count,
            "sample_wall_share": count / result["sample_total"] if result["sample_total"] else 0.0,
            "sample_wall_ms": count * INTERVAL * 1000,
        }
        for frame, count in sorted(result["sampled_frames"].items(), key=lambda item: (-item[1], item[0]))[:80]
    ]
    result.pop("sampled_frames", None)
    return result


def write_profile() -> None:
    STOP.set()
    ROOT.mkdir(parents=True, exist_ok=True)
    with LOCK:
        requests = [summarize_request(request) for request in REQUESTS]
        payload = {
            "run_id": RUN_ID,
            "source": SOURCE,
            "pid": os.getpid(),
            "process_identity": identity(),
            "runtime_source": str(REAL_RUNTIME),
            "agent_source": str(AGENT_ROOT),
            "sampling_interval_ms": INTERVAL * 1000,
            "requests": requests,
            "request_count": len(requests),
            "sampler_errors": ERRORS,
            "inclusive_overlap": "frame samples and inclusive timings overlap by design; shares are not additive and are not self CPU",
            "timing_definition": "self timings exclude only other named diagnostic functions; uninstrumented Python work remains in self",
            "observer_scope": "observer_cpu_ms is measured only while the sampled request is active",
        }
    birth = payload["process_identity"].get("birth_ticks")
    path = ROOT / f"profile-{os.getpid()}-{birth}.json"
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


sys.setprofile(profile)
threading.setprofile(profile)
try:
    threading.Thread(target=sample_stack, name="d111a-request-sampler", daemon=True).start()
except BaseException as error:  # pragma: no cover - serialized below
    ERRORS.append(type(error).__name__)
atexit.register(write_profile)
