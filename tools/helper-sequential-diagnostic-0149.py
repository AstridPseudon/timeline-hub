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
import json
import math
import os
import re
import subprocess
import sys
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
MAX_EVIDENCE = 24 * 1024 * 1024
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
    _finite(normalized)
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
    print(json.dumps({"finite_float": decoded["finite_float"], "path": decoded["source_path"],
                      "rejected": rejected}, sort_keys=True))
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
    def __init__(self) -> None:
        evidence = os.environ.get("HELPER_SEQUENTIAL_EVIDENCE")
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
        self._auth_path: Path | None = None
        self._durable_phase: str | None = None
        self._installed = False
        self._finalized = False

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
                self.evidence.write_text(payload, encoding="utf-8")
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
        ]
        runtime_paths = [
            self.runtime / "runtime_protocol/timeline_commit_port.py",
            self.runtime / "runtime_protocol/timeline_commit_auth.py",
            self.runtime / "runtime_protocol/timeline_commit_store.py",
        ]
        hashes = {str(path): _sha256(path) for path in [*(Path.cwd() / path for path in source_paths), *runtime_paths]}
        self.packet["preflight"] = {
            "agent_root": str(Path.cwd().resolve()),
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

    def _install(self, env: Any) -> None:
        if self._installed:
            return
        self._env = env
        runtime_port = importlib.import_module("runtime_protocol.timeline_commit_port")
        runtime_auth = importlib.import_module("runtime_protocol.timeline_commit_auth")
        self._auth_path = Path(runtime_auth.__file__).resolve()
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
        ):
            module = importlib.import_module(name)
            origin = Path(module.__file__).resolve()
            origins[name] = {"path": str(origin), "sha256": _sha256(origin)}
            if name.startswith("runtime_protocol") and not origin.is_relative_to(self.runtime):
                raise ObserverFailure(f"Runtime module origin escaped pinned checkout: {name}={origin}")
        self.packet["preflight"]["module_origins"] = origins
        def capture_wrapper(original):
            def wrapped(port, capture):
                self.packet["capture"] = _copy(capture)
                # Persist the complete carrier before touching Runtime's
                # validation seam.  A later observer/test exception must not
                # erase an already captured original/landing map.
                self._write("capture_observed", required=True)
                self.packet["request"] = _copy(capture["context"]["request"])
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
                self.packet["wire_attempts"].append(attempt)

        env.generated.commit_timeline = send
        self._trace_previous = sys.gettrace()
        sys.settrace(self._trace)
        self._installed = True

    def _trace(self, frame, event, arg):  # noqa: ARG002 - sys.settrace protocol
        if event == "line" and self._auth_path is not None and Path(frame.f_code.co_filename).resolve() == self._auth_path:
            if frame.f_code.co_name == "validate_sequential_capture" and frame.f_lineno in (2195, 2196):
                local = frame.f_locals
                self.packet["runtime_comparison"] = {
                    "expected_map": _copy(local.get("expected_map")),
                    "seen_map": _copy(local.get("seen_map")),
                    "replay": _copy(local.get("replay")),
                    "entry": _copy(local.get("entry")),
                    "map_key": _copy(local.get("map_key")),
                    "line": frame.f_lineno,
                }
                # This is deliberately written at the authenticated map
                # boundary, not deferred to pytest teardown.
                self._write(f"runtime_comparison_line_{frame.f_lineno}", required=True)
        return self._trace

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
    return pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=90", TARGET], plugins=[observer])


if __name__ == "__main__":
    raise SystemExit(main())
