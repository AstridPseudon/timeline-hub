"""Run one original sequential-helper case with a lossless private observer.

The observer wraps existing seams and always calls their original methods with
the original arguments.  It is intentionally a runner rather than a pytest
fixture or a product hook, so the test body and the Runtime guard remain
unchanged.
"""

from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any

import pytest

TARGET = "tests/sdk/test_timeline_helper_capture.py::test_contiguous_helpers_keep_sequential_steps[True]"
RUNTIME_HEAD = "8ea0766f5e9fb23cea26c7398770a8aaac06b258"
RUNTIME_TREE = "6047ac3033c3594b8f83db3afd8bb2c47cafa6d6"
MAX_DEPTH = 80
MAX_ITEMS = 200_000
MAX_STRING = 8 * 1024 * 1024
MAX_EVIDENCE = 12 * 1024 * 1024
AGENT_HEAD = "415181d983d6d1d56a912da16ad4c5690e663187"
CAPTURE_KEYS = {"schema_version", "context", "original", "landing", "replay_bindings", "prepared_digest"}
FRAME_FIELDS = (
    "expected_base", "expected_landing", "original_records", "landing_records",
    "binding_pairs", "source_to_landing", "landing_to_source", "replay_required",
    "expected_map", "seen_map", "replay", "entry", "map_key", "kind",
    "ordinal", "index", "command_ordinal", "change_ordinal", "command", "record",
    "binding", "original_binding", "landing_binding", "binding_candidates", "landing_candidates",
    "source_physical", "landing_physical", "source_key", "landing_key",
    "chain", "terminal", "source_step_ordinals", "node", "step", "owners", "original_owners",
    "original_transition", "landing_transition", "target_original", "target_landing", "continued",
    "boundary", "original", "accepted", "touched", "output", "indices", "ref", "read",
)
SECRET_TEXT = re.compile(
    r"(?:-----BEGIN [A-Z ]*PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\bBearer\s+\S+|\bsk-[A-Za-z0-9]{20,})"
)
SECRET_KEY = re.compile(r"(?:authorization|api[_-]?key|secret|password|private[_-]?key|access[_-]?token|refresh[_-]?token)", re.I)


class ObserverFailure(RuntimeError):
    """The observer could not safely retain an exact packet."""


def _runtime_root() -> Path:
    value = os.environ.get("ASTRID_RUNTIME_SOURCE_ROOT") or os.environ.get("ASTRID_RUNTIME_CHECKOUT")
    if not value:
        raise ObserverFailure("missing ASTRID_RUNTIME_CHECKOUT/ASTRID_RUNTIME_SOURCE_ROOT")
    return Path(value).expanduser().resolve()


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)
    if result.returncode:
        raise ObserverFailure(f"git {' '.join(args)} failed in {root}: {result.stderr.strip()}")
    return result.stdout.strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _jsonable(value: Any, *, path: str = "$", depth: int = 0) -> Any:
    """Normalize only values whose JSON meaning can be retained exactly.

    In particular, floats stay numbers and non-finite floats are refused before
    a JSON encoder can turn them into JavaScript extensions such as ``NaN``.
    ``Path`` is the one intentional non-JSON value in the real capture shape;
    its source spelling is retained as a string.  There is no lossy fallback
    for any other value.
    """
    if depth > MAX_DEPTH:
        raise ObserverFailure(f"JSON depth limit exceeded at {path}")
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ObserverFailure(f"non-finite JSON number at {path}")
        return value
    if isinstance(value, str):
        if len(value) > MAX_STRING:
            raise ObserverFailure(f"JSON string limit exceeded at {path}")
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (bool, int)) or value is None:
        return value
    if isinstance(value, dict):
        if len(value) > MAX_ITEMS:
            raise ObserverFailure(f"JSON object item limit exceeded at {path}")
        result: dict[str, Any] = {}
        for key, item in value.items():
            if isinstance(key, Path):
                json_key = str(key)
            elif isinstance(key, str):
                json_key = key
            elif isinstance(key, (bool, int, float)):
                # Validate a numeric key before JSON's required string
                # coercion, so NaN/Infinity cannot evade the finite check.
                checked_key = _jsonable(key, path=f"{path}.<key>", depth=depth + 1)
                json_key = str(checked_key)
            else:
                raise ObserverFailure(f"unsupported JSON key {type(key).__name__} at {path}.<key>")
            if json_key in result:
                raise ObserverFailure(f"JSON key collision after normalization at {path}.{json_key}")
            result[json_key] = _jsonable(item, path=f"{path}.{json_key}", depth=depth + 1)
        return result
    if isinstance(value, (list, tuple, set, frozenset)):
        if len(value) > MAX_ITEMS:
            raise ObserverFailure(f"JSON array item limit exceeded at {path}")
        values = [_jsonable(item, path=f"{path}[{index}]", depth=depth + 1)
                  for index, item in enumerate(value)]
        if isinstance(value, (set, frozenset)):
            return sorted(values, key=lambda item: json.dumps(item, sort_keys=True,
                                                              separators=(",", ":"), allow_nan=False))
        return values
    raise ObserverFailure(f"unsupported JSON value {type(value).__name__} at {path}")


def _finite(value: Any, *, path: str = "$", depth: int = 0) -> None:
    """Validate an already-normalized value for callers that need a predicate."""
    _jsonable(value, path=path, depth=depth)


def _serialize(value: Any) -> str:
    normalized = _jsonable(value)
    return json.dumps(normalized, ensure_ascii=True, allow_nan=False, indent=2, sort_keys=True) + "\n"


def _offline_probe() -> int:
    """Exercise the observer serializer without importing the test/runtime."""
    sample = {
        "finite_float": 0.625,
        "source_path": Path("/capture/source.json"),
        "nested": {"frame": 12.5, "items": (1, 2)},
    }
    payload = _serialize(sample)
    decoded = json.loads(payload)
    if decoded["finite_float"] != sample["finite_float"]:
        raise ObserverFailure("finite float changed during telemetry serialization")
    if decoded["source_path"] != str(sample["source_path"]):
        raise ObserverFailure("Path changed during telemetry serialization")
    rejected: list[str] = []
    for value in (float("nan"), float("inf"), float("-inf")):
        try:
            _serialize({"number": value})
        except ObserverFailure as exc:
            rejected.append(str(exc))
    if len(rejected) != 3:
        raise ObserverFailure("non-finite telemetry number was not rejected")
    # This synthetic function exercises only the observer; no test module or
    # product executor is imported or invoked by the offline checks.
    def selected():
        expected_map = {(1, "patch", 0)}
        seen_map = set()
        map_key = (1, "patch", 0)
        binding_pairs = {(1, 0): {"owner": "offline"}}
        if map_key in expected_map and map_key not in seen_map and binding_pairs:
            raise ValueError("offline exception retention")

    def unrelated():
        total = 0
        for number in range(25):
            total += number
        return total

    from unittest.mock import patch

    scratch = Path(tempfile.mkdtemp(prefix="helper-observer-offline-"))
    observer = Observer(scratch / "packet.json")
    observer.packet["target"] = "offline observer selfcheck only"
    observer._cache_auth(importlib.import_module("runtime_protocol.timeline_commit_auth"))
    runtime_map_lines = sorted(observer._map_lines)
    observer._active_attempt = {"validator_events": []}
    observer.packet["attempts"].append(observer._active_attempt)
    observer._sequential_code = selected.__code__
    selected_lines, start = inspect.getsourcelines(selected)
    observer._map_lines = frozenset(start + index for index, line in enumerate(selected_lines)
                                    if "if map_key in expected_map" in line)
    source_packet = {"finite": 0.625, "path": Path("/capture/source.json")}
    observer.packet["capture"] = _copy(source_packet)
    source_packet["finite"] = 7.0
    observer._write("offline_before_validation", required=True)
    previous_trace = sys.gettrace()
    try:
        with patch.object(Path, "resolve", side_effect=AssertionError("per-event Path.resolve")):
            sys.settrace(observer._trace)
            try:
                selected()
            except ValueError as exc:
                observer._record_exception(exc, boundary="offline selected")
            finally:
                sys.settrace(previous_trace)
    finally:
        sys.settrace(previous_trace)
    observer._write("offline_after_exception", required=True)
    retained = json.loads(observer.evidence.read_text())
    if retained["capture"]["finite"] != 0.625 or not retained["exceptions"]:
        raise ObserverFailure("immutable capture or exception was not retained")
    fields = retained["runtime_comparison"]["fields"]
    if fields["expected_map"] != [[1, "patch", 0]] or fields["seen_map"] != []:
        raise ObserverFailure("selected validator frame was not retained")
    if fields["binding_pairs"] != [{"coordinates": [1, 0], "pair": {"owner": "offline"}}]:
        raise ObserverFailure("tuple-keyed binding coordinates were not retained")
    durable = observer.evidence.read_bytes()
    observer.packet["bad_number"] = float("nan")
    if observer._write("offline_refused_nan") or observer.evidence.read_bytes() != durable:
        raise ObserverFailure("failed flush damaged previously durable capture")
    observer.packet.pop("bad_number")
    observer.packet["api_key"] = "offline fake credential"
    if observer._write("offline_refused_credentials") or observer.evidence.read_bytes() != durable:
        raise ObserverFailure("credential refusal damaged previously durable capture")
    observer.packet.pop("api_key")
    with patch.object(os, "replace", side_effect=OSError("offline interrupted replace")):
        if observer._write("offline_interrupted_replace") or observer.evidence.read_bytes() != durable:
            raise ObserverFailure("interrupted replace damaged previously durable capture")
    observer._write("offline_incremental_final", required=True)
    if not json.loads(observer.evidence.read_text())["exceptions"]:
        raise ObserverFailure("incremental final flush lost the exception")

    count = 10_000
    baseline_start = time.perf_counter()
    for _ in range(count):
        unrelated()
    baseline = time.perf_counter() - baseline_start
    start_time = time.perf_counter()
    try:
        with patch.object(Path, "resolve", side_effect=AssertionError("per-event Path.resolve")):
            sys.settrace(observer._trace)
            for _ in range(count):
                unrelated()
    finally:
        sys.settrace(previous_trace)
    traced = time.perf_counter() - start_time
    if traced - baseline > 1.0 or observer._trace(sys._getframe(), "call", None) is not None:
        raise ObserverFailure(f"unrelated-frame observer overhead exceeded 1s: {traced - baseline}")
    events = observer._active_attempt["validator_events"]
    if [entry["event"] for entry in events] != ["line", "exception"]:
        raise ObserverFailure("trace selection admitted unrelated frames or lines")
    print(json.dumps({"finite_float": decoded["finite_float"], "path": decoded["source_path"],
                      "rejected": rejected, "durable_exception_retained": True,
                      "failed_flush_preserved_packet": True, "credential_refusal": True,
                      "path_resolve_calls_while_tracing": 0, "unrelated_calls": count,
                      "selected_events": len(events),
                      "runtime_map_lines": runtime_map_lines,
                      "baseline_seconds": baseline, "traced_seconds": traced,
                      "overhead_seconds": traced - baseline,
                      "offline_evidence": str(observer.evidence)}, sort_keys=True))
    return 0


def _credential_scan(value: Any, *, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            if SECRET_KEY.search(key_text):
                findings.append(f"{path}.{key_text}")
            findings.extend(_credential_scan(item, path=f"{path}.{key_text}"))
    elif isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(value):
            findings.extend(_credential_scan(item, path=f"{path}[{index}]"))
    elif isinstance(value, str) and SECRET_TEXT.search(value):
        findings.append(path)
    return findings


def _copy(value: Any) -> Any:
    try:
        return copy.deepcopy(value)
    except Exception as exc:  # pragma: no cover - observer boundary
        raise ObserverFailure(f"deepcopy failed for {type(value).__name__}: {exc}") from exc


class Observer:
    def __init__(self, evidence: Path | None = None) -> None:
        evidence = evidence or os.environ.get("HELPER_SEQUENTIAL_EVIDENCE")
        if not evidence:
            raise ObserverFailure("HELPER_SEQUENTIAL_EVIDENCE is required")
        self.evidence = Path(evidence).expanduser().resolve()
        self.runtime = _runtime_root()
        self.packet: dict[str, Any] = {
            "diagnostic": "helper-sequential-diagnostic-0149",
            "target": TARGET,
            "observer": {"path": str(Path(__file__).resolve()), "pid": os.getpid(), "python": sys.executable},
            "preflight": {},
            "capture": None,
            "prepared": None,
            "authenticated_inputs": None,
            "port_observations": {"head": [], "history": [], "history_entry": [], "revision_closure": []},
            "runtime_comparison": None,
            "attempts": [],
            "exceptions": [],
            "wire_attempts": [],
            "test_report": None,
            "observer_errors": [],
        }
        self._class_patches: list[tuple[type[Any], str, Any]] = []
        self._generated_original: Any = None
        self._generated: Any = None
        self._env: Any = None
        self._trace_previous: Any = None
        self._sequential_code: Any = None
        self._validate_code: Any = None
        self._map_lines: frozenset[int] = frozenset()
        self._active_attempt: dict[str, Any] | None = None
        self._durable_phase: str | None = None
        self._installed = False
        self._finalized = False
        self._source_functions: dict[str, Any] = {}

    def _write(self, phase: str, *, required: bool = False) -> bool:
        packet = _copy(self.packet)
        packet["phase"] = phase
        packet["credential_scan"] = {"matches": _credential_scan(packet)}
        if packet["credential_scan"]["matches"]:
            error = ObserverFailure(f"credential scan refused evidence: {packet['credential_scan']['matches']}")
        else:
            try:
                payload = _serialize(packet)
                payload_bytes = payload.encode()
                if len(payload_bytes) > MAX_EVIDENCE:
                    raise ObserverFailure(f"evidence size limit exceeded: {len(payload_bytes)} > {MAX_EVIDENCE}")
                self.evidence.parent.mkdir(parents=True, exist_ok=True)
                # Validate/scan before opening anything. Replace atomically so
                # even an interrupted flush leaves the previous packet intact.
                pending = self.evidence.with_suffix(".pending")
                with pending.open("w", encoding="utf-8") as stream:
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(pending, self.evidence)
                directory = os.open(self.evidence.parent, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
                self._durable_phase = phase
                return True
            except (ObserverFailure, OSError) as exc:
                error = exc
        if required:
            raise error
        self.packet["observer_errors"].append({"phase": phase, "type": type(error).__name__,
                                               "message": str(error)})
        return False

    def _record_exception(self, exc: BaseException, *, boundary: str) -> None:
        self.packet["exceptions"].append({
            "boundary": boundary,
            "type": type(exc).__name__,
            "module": type(exc).__module__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        })

    def preflight(self) -> None:
        if _git(Path.cwd(), "rev-parse", "HEAD") != AGENT_HEAD:
            raise ObserverFailure("run from the exact integration4151 Agent checkout")
        if _git(Path.cwd(), "status", "--porcelain", "--untracked-files=no"):
            raise ObserverFailure("integration Agent tracked sources are not clean")
        expected_source_root = os.environ.get("ASTRID_RUNTIME_SOURCE_ROOT")
        if expected_source_root and Path(expected_source_root).expanduser().resolve() != self.runtime:
            raise ObserverFailure("ASTRID_RUNTIME_SOURCE_ROOT disagrees with ASTRID_RUNTIME_CHECKOUT")
        head = _git(self.runtime, "rev-parse", "HEAD")
        tree = _git(self.runtime, "rev-parse", "HEAD^{tree}")
        if head != RUNTIME_HEAD or tree != RUNTIME_TREE:
            raise ObserverFailure(f"Runtime pin mismatch: {head} {tree}")
        tracked_diff = _git(self.runtime, "status", "--porcelain", "--untracked-files=no")
        if tracked_diff:
            raise ObserverFailure(f"Runtime checkout is not clean: {tracked_diff}")
        source_paths = [
            Path("astrid/sdk/timeline/_commit_preview.py"),
            Path("astrid/sdk/timeline/commit.py"),
            Path("tests/sdk/test_timeline_helper_capture.py"),
            Path("tests/sdk/test_timeline_restructure.py"),
            Path("astrid/sdk/timeline/commands.py"),
            Path("astrid_runtime_client/__init__.py"),
        ]
        runtime_paths = [
            self.runtime / "runtime_protocol/timeline_commit_port.py",
            self.runtime / "runtime_protocol/timeline_commit_auth.py",
            self.runtime / "runtime_protocol/timeline_commit_store.py",
        ]
        hashes = {str(path): _sha256(path) for path in [*(Path.cwd() / path for path in source_paths), *runtime_paths]}
        self.packet["preflight"] = {
            "agent_root": str(Path.cwd().resolve()),
            "agent_head": AGENT_HEAD,
            "runtime_root": str(self.runtime),
            "runtime_head": head,
            "runtime_tree": tree,
            "runtime_tracked_diff": tracked_diff,
            "source_hashes": hashes,
            "expected_runtime_head": RUNTIME_HEAD,
            "expected_runtime_tree": RUNTIME_TREE,
            "limits": {"max_depth": MAX_DEPTH, "max_items": MAX_ITEMS, "max_string": MAX_STRING,
                        "max_evidence_bytes": MAX_EVIDENCE},
            "credential_scan": {"scope": "captured JSON values and keys; no secret values retained", "matches": []},
        }
        self._write("preflight", required=True)

    def _observe_method(self, cls: type[Any], name: str, callback) -> None:
        original = getattr(cls, name)
        self._class_patches.append((cls, name, original))
        setattr(cls, name, callback(original))

    def _cache_auth(self, runtime_auth: Any) -> None:
        self._sequential_code = runtime_auth.validate_sequential_capture.__code__
        self._validate_code = runtime_auth.validate.__code__
        lines, start = inspect.getsourcelines(runtime_auth.validate_sequential_capture)
        self._map_lines = frozenset(start + index for index, line in enumerate(lines)
                                    if "require(map_key in expected_map" in line
                                    or "require(seen_map == expected_map" in line)
        if len(self._map_lines) != 2:
            raise ObserverFailure("authenticated replay map source boundaries changed")

    def _install(self, env: Any) -> None:
        if self._installed:
            return
        self._env = env
        runtime_port = importlib.import_module("runtime_protocol.timeline_commit_port")
        runtime_auth = importlib.import_module("runtime_protocol.timeline_commit_auth")
        self._cache_auth(runtime_auth)
        origins = {}
        for name in (
            "runtime_protocol",
            "runtime_protocol.timeline_commit_port",
            "runtime_protocol.timeline_commit_auth",
            "runtime_protocol.timeline_commit_store",
            "runtime_protocol.service",
            "astrid.sdk.timeline._commit_preview",
            "astrid.sdk.timeline.commit",
            "tests.sdk.test_timeline_helper_capture",
            "tests.sdk.test_timeline_restructure",
            "astrid_runtime_client",
        ):
            module = importlib.import_module(name)
            origin = Path(module.__file__).resolve()
            origins[name] = {"path": str(origin), "sha256": _sha256(origin)}
            if name.startswith("runtime_protocol") and not origin.is_relative_to(self.runtime):
                raise ObserverFailure(f"Runtime module origin escaped pinned checkout: {name}={origin}")
        self.packet["preflight"]["module_origins"] = origins
        helper_module = importlib.import_module("tests.sdk.test_timeline_helper_capture")
        self._source_functions = {
            "test_body": helper_module.test_contiguous_helpers_keep_sequential_steps,
            "peer_edit": helper_module.peer_edit,
            "auth_sequential": runtime_auth.validate_sequential_capture,
            "auth_validate": runtime_auth.validate,
            "port_capture": runtime_port.RequestCommitPort.capture_sequential_execution,
            "port_validate": runtime_port.RequestCommitPort._validate_sequential_execution,
        }
        self.packet["preflight"]["function_body_hashes"] = {
            name: hashlib.sha256(inspect.getsource(fn).encode()).hexdigest()
            for name, fn in self._source_functions.items()
        }
        self.packet["preflight"]["trace_selection"] = {
            "functions": [self._sequential_code.co_name, self._validate_code.co_name],
            "map_lines": sorted(self._map_lines), "frame_fields": list(FRAME_FIELDS),
        }
        self._write("observer_installed", required=True)
        def capture_wrapper(original):
            def wrapped(port, capture):
                self.packet["capture"] = _copy(capture)
                self._active_attempt = {"capture": self.packet["capture"], "validator_events": []}
                self.packet["attempts"].append(self._active_attempt)
                # Persist the complete carrier before touching Runtime's
                # validation seam.  A later observer/test exception must not
                # erase an already captured original/landing map.
                self._write("capture_observed", required=True)
                self.packet["request"] = _copy(capture["context"]["request"])
                self._active_attempt["port_context"] = _copy(port._RequestCommitPort__context)
                self._active_attempt["request"] = self.packet["request"]
                self._write("before_runtime_capture_validation", required=True)
                try:
                    return original(port, capture)
                except BaseException as exc:
                    self._record_exception(exc, boundary="RequestCommitPort.capture_sequential_execution")
                    self._write("capture_method_exception")
                    raise
            return wrapped

        def validation_wrapper(original):
            def wrapped(port, prepared, source, base, continuations, history):
                self.packet["prepared"] = _copy(prepared)
                capture = self.packet.get("capture")
                self.packet["authenticated_inputs"] = {
                    "base": _copy(base),
                    "head": _copy(prepared["expected_head"]),
                    "source": _copy(source),
                    "continuations": _copy(continuations),
                    "history": _copy(history),
                    "request": _copy(capture["context"]["request"] if capture else None),
                }
                if self._active_attempt is not None:
                    self._active_attempt["prepared"] = self.packet["prepared"]
                    self._active_attempt["authenticated_inputs"] = self.packet["authenticated_inputs"]
                self._write("before_runtime_sequential_validation", required=True)
                try:
                    result = original(port, prepared, source, base, continuations, history)
                except BaseException as exc:
                    self._record_exception(exc, boundary="RequestCommitPort._validate_sequential_execution")
                    self._write("after_runtime_sequential_validation_exception")
                    raise
                self.packet["runtime_validation_result"] = _copy(result)
                self._write("after_runtime_sequential_validation")
                return result
            return wrapped

        def observation_wrapper(name):
            def make(original):
                def wrapped(port, *args, **kwargs):
                    try:
                        result = original(port, *args, **kwargs)
                    except BaseException as exc:
                        self._record_exception(exc, boundary=f"RequestCommitPort.{name}")
                        raise
                    self.packet["port_observations"][name].append({"args": _copy(args), "kwargs": _copy(kwargs), "result": _copy(result)})
                    return result
                return wrapped
            return make

        self._observe_method(runtime_port.RequestCommitPort, "capture_sequential_execution", capture_wrapper)
        self._observe_method(runtime_port.RequestCommitPort, "_validate_sequential_execution", validation_wrapper)
        for name in ("head", "history", "history_entry", "revision_closure"):
            self._observe_method(runtime_port.RequestCommitPort, name, observation_wrapper(name))

        self._generated = env.generated
        self._generated_original = env.generated.commit_timeline

        def send(*args, **kwargs):
            attempt: dict[str, Any] = {"args": _copy(args), "kwargs": _copy(kwargs)}
            before = list(env.service.store.conn.iterdump())
            attempt["database_before"] = {"line_count": len(before), "sha256": hashlib.sha256("\n".join(before).encode()).hexdigest()}
            self.packet["wire_attempts"].append(attempt)
            self._write("before_wire_attempt", required=True)
            try:
                result = self._generated_original(*args, **kwargs)
            except BaseException as exc:
                attempt["exception"] = {"type": type(exc).__name__, "module": type(exc).__module__, "message": str(exc),
                                        "traceback": traceback.format_exc()}
                raise
            else:
                attempt["result"] = _copy(result)
                return result
            finally:
                after = list(env.service.store.conn.iterdump())
                attempt["database_after"] = {"line_count": len(after), "sha256": hashlib.sha256("\n".join(after).encode()).hexdigest()}
                attempt["no_write"] = before == after
                self._write("wire_attempt_finished", required=True)

        env.generated.commit_timeline = send
        self._trace_previous = sys.gettrace()
        sys.settrace(self._trace)
        self._installed = True

    def _trace(self, frame, event, arg):  # noqa: ARG002 - sys.settrace protocol
        # The global callback sees calls only. No path work, locals access or
        # local trace is allowed for unrelated frames.
        code = frame.f_code
        if code is self._sequential_code:
            return self._trace_auth
        if code is self._validate_code:
            frame.f_trace_lines = False
            return self._trace_auth
        return None

    def _trace_auth(self, frame, event, arg):
        if event == "exception" or (event == "line" and frame.f_lineno in self._map_lines):
            local = frame.f_locals
            snapshot = {"function": frame.f_code.co_name, "line": frame.f_lineno, "event": event,
                        "fields": {name: _copy(local[name]) for name in FRAME_FIELDS if name in local}}
            if "binding_pairs" in local:
                snapshot["fields"]["binding_pairs"] = [
                    {"coordinates": list(key), "pair": _copy(value)}
                    for key, value in local["binding_pairs"].items()
                ]
            if event == "exception":
                snapshot["exception"] = {"type": arg[0].__name__, "message": str(arg[1])}
            self.packet["runtime_comparison"] = snapshot
            if self._active_attempt is not None:
                self._active_attempt["validator_events"].append(snapshot)
            self._write(f"auth_{event}_{frame.f_lineno}", required=True)
        return self._trace_auth

    def pytest_runtest_call(self, item):
        if item.nodeid == TARGET:
            self._install(item.funcargs["restructure_runtime"])

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        if item.nodeid != TARGET:
            yield
            return
        outcome = yield
        report = outcome.get_result()
        if report is not None and report.when == "call":
            self.packet["test_report"] = {
                "outcome": report.outcome,
                "longrepr": str(report.longrepr) if report.longrepr else None,
                "duration": report.duration,
            }

    def pytest_runtest_teardown(self, item):
        if item.nodeid != TARGET or not self._installed:
            return
        sys.settrace(self._trace_previous)
        if self._generated is not None:
            self._generated.commit_timeline = self._generated_original
        for cls, name, original in reversed(self._class_patches):
            setattr(cls, name, original)
        hashes = self.packet["preflight"]["source_hashes"]
        self.packet["source_hashes_after"] = {path: _sha256(Path(path)) for path in hashes}
        self.packet["source_unchanged"] = hashes == self.packet["source_hashes_after"]
        self.packet["function_body_hashes_after"] = {
            name: hashlib.sha256(inspect.getsource(fn).encode()).hexdigest()
            for name, fn in self._source_functions.items()
        }
        self.packet["function_bodies_unchanged"] = (
            self.packet["function_body_hashes_after"] == self.packet["preflight"]["function_body_hashes"])
        self.packet["module_origins_after"] = {
            name: {"path": str(Path(importlib.import_module(name).__file__).resolve()),
                   "sha256": _sha256(Path(importlib.import_module(name).__file__))}
            for name in self.packet["preflight"]["module_origins"]
        }
        self.packet["module_origins_unchanged"] = (
            self.packet["module_origins_after"] == self.packet["preflight"]["module_origins"])
        self._write("final")
        self._finalized = True

    def pytest_sessionfinish(self, session, exitstatus):  # noqa: ARG002
        if not self._finalized:
            self._write("session_finish_without_target_teardown")


def main() -> int:
    if "--offline-probe" in sys.argv[1:]:
        return _offline_probe()
    observer = Observer()
    observer.preflight()
    return pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=45", TARGET], plugins=[observer])


if __name__ == "__main__":
    raise SystemExit(main())
