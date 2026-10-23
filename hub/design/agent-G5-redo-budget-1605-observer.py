#!/usr/bin/env python3
"""Lossless capture harness for the single authorized G5 diagnostic.

The 1534 source remains the behavioral reproducer.  This file loads it
unchanged, replacing only its observer clone and capture wrappers.  It also
has an offline smoke mode which never imports the fixture or calls a service.
"""
from __future__ import annotations

import base64
import dataclasses
import hashlib
import importlib
import importlib.util
import inspect
import json
import math
import os
import sys
import tempfile
import time
import traceback
from collections.abc import Mapping
from pathlib import Path
from typing import Any


ORCH_DESIGN = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design"
)
ORIGINAL_SOURCE = ORCH_DESIGN / "agent-G5-redo-reproducer-1534-7e4b.py"
ORIGINAL_SOURCE_SHA256 = "153be3ff0db9e473bde9289e9964ea7900e8666713073677a8d4251c42c91740"
MAX_EVENT_LINES = 4096
CAPTURE_TAG = "__astrid_capture__"
_ACTIVE_RECORDERS: list["DurableCapture"] = []


def _sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except (OSError, ValueError):
        return None


def _source_hash(value: Any) -> str | None:
    try:
        source = inspect.getsourcefile(value)
    except (OSError, TypeError):
        return None
    return _sha256_file(Path(source)) if source else None


def _type_metadata(value: Any) -> dict[str, Any]:
    value_type = value if isinstance(value, type) else type(value)
    return {
        "module": getattr(value_type, "__module__", None),
        "qualname": getattr(value_type, "__qualname__", getattr(value_type, "__name__", None)),
        "sourcefile_sha256": _source_hash(value_type),
    }


def _callable_metadata(value: Any) -> dict[str, Any]:
    return {
        "module": getattr(value, "__module__", None),
        "qualname": getattr(value, "__qualname__", getattr(value, "__name__", None)),
        "sourcefile_sha256": _source_hash(value),
    }


def _encode(value: Any, *, active: dict[int, str], path: str) -> Any:
    """Turn observed values into finite JSON without repr or silent omission.

    JSON-shaped values retain their shape and scalar values exactly.  Values
    outside JSON are represented by explicit tagged records.  ``active`` is a
    recursion stack, so repeated non-cyclic values are copied while cycles are
    represented by a stable path rather than a process-local object id.
    """
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        scalar = "nan" if math.isnan(value) else ("inf" if value > 0 else "-inf")
        return {CAPTURE_TAG: "float", "value": scalar}
    if isinstance(value, bytes):
        return {
            CAPTURE_TAG: "bytes",
            "base64": base64.b64encode(value).decode("ascii"),
        }
    if isinstance(value, (bytearray, memoryview)):
        return _encode(bytes(value), active=active, path=path)
    if inspect.isroutine(value) or inspect.ismethod(value) or inspect.isfunction(value):
        return {CAPTURE_TAG: "callable", **_callable_metadata(value)}
    if isinstance(value, type):
        return {CAPTURE_TAG: "type", **_type_metadata(value)}
    if isinstance(value, BaseException):
        return {
            CAPTURE_TAG: "exception",
            "type": _type_metadata(value),
            "message": str(value),
            "args": _encode(tuple(value.args), active=active, path=f"{path}.args"),
        }

    value_id = id(value)
    if value_id in active:
        return {CAPTURE_TAG: "cycle", "path": active[value_id]}
    active[value_id] = path
    try:
        if isinstance(value, Mapping):
            if all(isinstance(key, str) for key in value):
                return {
                    str(key): _encode(item, active=active, path=f"{path}.{key}")
                    for key, item in value.items()
                }
            return {
                CAPTURE_TAG: "mapping",
                "items": [
                    [
                        _encode(key, active=active, path=f"{path}.key{index}"),
                        _encode(item, active=active, path=f"{path}.value{index}"),
                    ]
                    for index, (key, item) in enumerate(value.items())
                ],
            }
        if isinstance(value, list):
            return [
                _encode(item, active=active, path=f"{path}[{index}]")
                for index, item in enumerate(value)
            ]
        if isinstance(value, tuple):
            return {
                CAPTURE_TAG: "tuple",
                "items": [
                    _encode(item, active=active, path=f"{path}[{index}]")
                    for index, item in enumerate(value)
                ],
            }
        if isinstance(value, (set, frozenset)):
            items = [
                _encode(item, active=active, path=f"{path}[{index}]")
                for index, item in enumerate(value)
            ]
            items.sort(key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
            return {CAPTURE_TAG: "set", "frozen": isinstance(value, frozenset), "items": items}
        if dataclasses.is_dataclass(value) and not isinstance(value, type):
            return {
                CAPTURE_TAG: "dataclass",
                "type": _type_metadata(value),
                "fields": {
                    field.name: _encode(
                        getattr(value, field.name),
                        active=active,
                        path=f"{path}.{field.name}",
                    )
                    for field in dataclasses.fields(value)
                },
            }
        # Unknown values are never stringified.  Type metadata is the only
        # safe representation when an object exposes arbitrary credentials or
        # environment-backed state through __dict__.
        return {CAPTURE_TAG: "object", "type": _type_metadata(value)}
    finally:
        active.pop(value_id, None)


def safe_json(value: Any) -> Any:
    """Return a finite JSON-compatible capture value."""
    encoded = _encode(value, active={}, path="$")
    json.dumps(encoded, allow_nan=False, sort_keys=True, separators=(",", ":"))
    return encoded


def safe_clone(value: Any) -> Any:
    """Observer clone used by the original reproducer's capture points."""
    return safe_json(value)


class DurableCapture:
    """Append-only flat JSONL packet store with content-hash deduplication."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = path.open("a", encoding="utf-8")
        self._payload_first: dict[str, int] = {}
        self._lines = 0
        self._sequence = 0
        self._started = time.monotonic()

    def append(self, kind: str, stage: str, payload: Any) -> dict[str, Any]:
        if self._lines >= MAX_EVENT_LINES:
            raise RuntimeError("durable capture event bound exceeded")
        encoded_payload = safe_json(payload)
        payload_bytes = json.dumps(
            encoded_payload, allow_nan=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        content_hash = hashlib.sha256(payload_bytes).hexdigest()
        self._sequence += 1
        record: dict[str, Any] = {
            "elapsed_seconds": round(time.monotonic() - self._started, 6),
            "sequence": self._sequence,
            "kind": kind,
            "stage": stage,
            "content_hash": content_hash,
        }
        first = self._payload_first.get(content_hash)
        if first is None:
            self._payload_first[content_hash] = self._sequence
            record["payload"] = encoded_payload
        else:
            record["duplicate_of"] = first
        line = json.dumps(record, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self._handle.write(line + "\n")
        self._handle.flush()
        os.fsync(self._handle.fileno())
        self._lines += 1
        return record

    def close(self) -> None:
        self._handle.close()


def _load_original() -> Any:
    if _sha256_file(ORIGINAL_SOURCE) != ORIGINAL_SOURCE_SHA256:
        raise RuntimeError("the preserved 1534 diagnostic source hash changed")
    spec = importlib.util.spec_from_file_location("g5_original_reproducer", ORIGINAL_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load preserved G5 diagnostic source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _install_lossless_wrappers(original: Any) -> Any:
    def install_wrappers(env: Any, report: dict[str, Any], phase: dict[str, str]):
        event_path = Path(os.environ["ASTRID_G5_DURABLE_EVENTS"])
        recorder = _ACTIVE_RECORDERS[0] if _ACTIVE_RECORDERS else DurableCapture(event_path)
        if recorder not in _ACTIVE_RECORDERS:
            _ACTIVE_RECORDERS.append(recorder)
        report["durable_capture"] = {
            "path": str(event_path),
            "format": "jsonl",
            "max_unique_payload_lines": MAX_EVENT_LINES,
            "content_hash": "sha256(canonical-finite-json-payload)",
            "precall_is_durable": True,
        }
        restores: list[tuple[Any, str, Any, bool]] = []

        def replace(owner: Any, name: str, wrapper: Any) -> None:
            existed = name in getattr(owner, "__dict__", {})
            old = getattr(owner, name)
            restores.append((owner, name, old, existed))
            setattr(owner, name, wrapper)

        def durable(kind: str, stage: str, payload: Any) -> None:
            recorder.append(kind, stage, payload)

        old_generated = env.generated.commit_timeline

        def generated_commit(project: Any, timeline: Any, body: Any, *, idempotency_key: str):
            event = {
                "phase": phase["name"],
                "project": project,
                "timeline": timeline,
                "idempotency_key": idempotency_key,
                "request": safe_clone(body),
            }
            durable("transport.commit_timeline", "precall", event)
            report["transport_calls"].append({**event, "request_audit": original.audit_request(body)})
            try:
                result = old_generated(project, timeline, body, idempotency_key=idempotency_key)
            except BaseException as exc:
                durable(
                    "transport.commit_timeline",
                    "throw",
                    {**event, "exception": original.exception_record(exc)},
                )
                raise
            durable(
                "transport.commit_timeline",
                "return",
                {**event, "reply": safe_clone(result)},
            )
            report["transport_calls"][-1]["reply"] = safe_clone(result)
            report["transport_calls"][-1]["reply_audit"] = original.audit_reply(result)
            return result

        replace(env.generated, "commit_timeline", generated_commit)

        provider = env.service._timeline_commit_provider
        if provider is None:
            recorder.close()
            raise AssertionError("faithful fixture did not install the astrid provider")
        old_provider_commit = provider.commit

        def provider_commit(context: Any, port: Any):
            event = {
                "phase": phase["name"],
                "context": safe_clone(context),
                "request": safe_clone(context.get("request")),
                "port_calls": [],
            }
            durable("provider.commit", "precall", event)
            report["provider_calls"].append(event)
            port_restores: list[tuple[str, Any, bool]] = []
            for method_name in original.PORT_METHODS:
                if not hasattr(port, method_name):
                    continue
                existed = method_name in getattr(port, "__dict__", {})
                old_method = getattr(port, method_name)
                port_restores.append((method_name, old_method, existed))

                def port_method(*args: Any, _name=method_name, _old=old_method, **kwargs: Any):
                    port_event = {
                        "phase": phase["name"],
                        "method": _name,
                        "args": safe_clone(args),
                        "kwargs": safe_clone(kwargs),
                    }
                    # This is intentionally before preview/accept and every
                    # other port invocation; a later serializer cannot erase it.
                    durable(f"provider.port.{_name}", "precall", port_event)
                    event["port_calls"].append(port_event)
                    try:
                        value = _old(*args, **kwargs)
                    except BaseException as exc:
                        durable(
                            f"provider.port.{_name}",
                            "throw",
                            {**port_event, "exception": original.exception_record(exc)},
                        )
                        port_event["exception"] = original.exception_record(exc)
                        raise
                    durable(
                        f"provider.port.{_name}",
                        "return",
                        {**port_event, "return": safe_clone(value)},
                    )
                    port_event["return"] = safe_clone(value)
                    if _name in {"accept", "preview"} and args and isinstance(args[0], dict):
                        port_event["prepared"] = safe_clone(args[0])
                    return value

                setattr(port, method_name, port_method)
            try:
                value = old_provider_commit(context, port)
            except BaseException as exc:
                durable(
                    "provider.commit",
                    "throw",
                    {**event, "exception": original.exception_record(exc)},
                )
                event["exception"] = original.exception_record(exc)
                event["provider_traceback_locals"] = original.traceback_locals(exc)
                raise
            else:
                durable("provider.commit", "return", {**event, "outcome": safe_clone(value)})
                event["outcome"] = safe_clone(value)
                return value
            finally:
                for method_name, old_method, existed in reversed(port_restores):
                    if existed:
                        setattr(port, method_name, old_method)
                    else:
                        delattr(port, method_name)

        replace(provider, "commit", provider_commit)

        for module_name in original.GUARD_MODULES:
            module = importlib.import_module(module_name)
            if not hasattr(module, "guard"):
                continue
            old_guard = module.guard

            def guard_wrapper(
                state: Any,
                ref: Any,
                path: Any,
                expected: Any,
                *,
                _module=module_name,
                _old=old_guard,
                **kwargs: Any,
            ):
                event = {
                    "phase": phase["name"],
                    "module": _module,
                    "ref": safe_clone(ref),
                    "path": safe_clone(path),
                    "expected": safe_clone(expected),
                    "kwargs": safe_clone(kwargs),
                }
                try:
                    event["actual_before"] = safe_clone(state.get(ref, path))
                except BaseException as exc:
                    event["actual_before_error"] = original.exception_record(exc)
                durable(f"guard.{_module}", "precall", event)
                report["guard_calls"].append(event)
                try:
                    value = _old(state, ref, path, expected, **kwargs)
                except BaseException as exc:
                    durable(
                        f"guard.{_module}",
                        "throw",
                        {**event, "exception": original.exception_record(exc)},
                    )
                    event["exception"] = original.exception_record(exc)
                    try:
                        event["actual_after"] = safe_clone(state.get(ref, path))
                    except BaseException:
                        pass
                    raise
                durable(f"guard.{_module}", "return", {**event, "return": safe_clone(value)})
                event["return"] = safe_clone(value)
                return value

            replace(module, "guard", guard_wrapper)

        return restores

    original.install_wrappers = install_wrappers
    original.clone = safe_clone
    return original


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def offline_smoke() -> int:
    """Exercise the capture codec and durability without fixture/service code."""
    @dataclasses.dataclass
    class Nested:
        callback: Any
        metadata: dict[str, Any]

    def callback(value: Any) -> Any:
        return value

    critical = {
        "request": {
            "api_version": "v2",
            "commands": [{"kind": "doc.patch", "patch": {"path": "x", "value": 2}}],
            "steps": [{"id": "s1", "label": "x", "intent": "x", "tags": [], "command_ordinals": [0], "patch": {}}],
        },
        "history": [{"revision_id": "r1", "status": "accepted", "records": [{"id": 3}]}],
        "prepared": {"native": {"clip_id": "c1"}, "effects": [{"name": "gain", "value": 0.5}]},
    }
    encoded_critical = safe_json(critical)
    decoded_critical = json.loads(json.dumps(encoded_critical, allow_nan=False, sort_keys=True))
    assert decoded_critical == encoded_critical
    assert decoded_critical["request"] == critical["request"]

    error_locals = {"callback": callback, "nested": Nested(callback, {"source": "offline"})}
    encoded_locals = safe_json(error_locals)
    assert encoded_locals["callback"][CAPTURE_TAG] == "callable"
    assert encoded_locals["callback"]["module"] == __name__
    assert encoded_locals["nested"][CAPTURE_TAG] == "dataclass"
    assert encoded_locals["nested"]["fields"]["callback"][CAPTURE_TAG] == "callable"
    assert encoded_locals["nested"]["type"]["sourcefile_sha256"]

    with tempfile.TemporaryDirectory(prefix="g5-lossless-smoke-") as directory:
        event_path = Path(directory) / "events.jsonl"
        recorder = _ACTIVE_RECORDERS[0] if _ACTIVE_RECORDERS else DurableCapture(event_path)
        recorder.append("provider.port.preview", "precall", {"prepared": critical, "locals": error_locals})
        recorder.close()
        durable_records = _read_jsonl(event_path)
        assert len(durable_records) == 1
        assert durable_records[0]["stage"] == "precall"
        assert durable_records[0]["payload"]["prepared"] == encoded_critical
        final_report = safe_json({"verdict": "synthetic-final-exception", "locals": error_locals})
        json.dumps(final_report, allow_nan=False, sort_keys=True)
    print(json.dumps({"offline_smoke": "PASS", "checks": 5}, sort_keys=True))
    return 0


def detailed_exception(original: Any, old: Any, exc: BaseException) -> dict[str, Any]:
    result = old(exc)
    frames = []
    cursor = exc.__traceback__
    while cursor is not None:
        frame = cursor.tb_frame
        filename = str(Path(frame.f_code.co_filename).resolve())
        # Capture actual throw frames, never trace service execution.
        if "/astrid/sdk/timeline/" in filename or "/runtime_protocol/" in filename:
            frames.append({"file": filename, "source_sha256": _sha256_file(Path(filename)),
                           "function": frame.f_code.co_name, "line": cursor.tb_lineno,
                           "locals": safe_json(frame.f_locals)})
        cursor = cursor.tb_next
    result["dynamic_throw_frames"] = frames
    result["traceback"] = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    return result


def run_live() -> int:
    original = _install_lossless_wrappers(_load_original())
    args = original.parse_args()
    if not args.net:
        raise RuntimeError("--net required")
    agent_root, runtime_root = args.agent_root.resolve(), args.runtime_root.resolve()
    if original.git_head(agent_root) != original.AGENT_HEAD:
        raise RuntimeError("Agent pin mismatch")
    if original.git_head(runtime_root) != original.RUNTIME_HEAD:
        raise RuntimeError("Runtime pin mismatch")
    if not args.tmpdir.is_dir():
        raise RuntimeError("--tmpdir must name the existing actual directory")
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    recorder = DurableCapture(output / "g5-redo-events.jsonl")
    _ACTIVE_RECORDERS.append(recorder)
    os.environ["ASTRID_G5_DURABLE_EVENTS"] = str(recorder.path)
    report = {"task": "agt-G5-redo-budget-sol-1605", "outer_budget_seconds": 180,
              "transport_calls": [], "provider_calls": [], "guard_calls": [], "closure_checks": []}
    generator = monkeypatch = context = None
    restores = []
    old_exception = original.exception_record
    original.exception_record = lambda exc: detailed_exception(original, old_exception, exc)
    old_snapshot = original.state_snapshot

    def snapshot(env: Any, **kwargs: Any):
        recorder.append("state_snapshot", "precall", {"origins": original.module_origins(),
                         "sql": original.sql_snapshot(env)})
        value = old_snapshot(env, **kwargs)
        recorder.append("state_snapshot", "return", value)
        return value

    original.state_snapshot = snapshot

    class Phase(dict):
        def __setitem__(self, key: str, value: Any):
            recorder.append("phase", "precall", {"phase": value, "previous": self.get(key),
                            "sql": original.sql_snapshot(env),
                            "head": env.service.get_project_timeline(env.project, "t"),
                            "origins": original.module_origins()})
            super().__setitem__(key, value)

    try:
        recorder.append("setup.import", "precall", {"agent_root": str(agent_root),
                        "runtime_root": str(runtime_root), "agent_head": original.AGENT_HEAD,
                        "runtime_head": original.RUNTIME_HEAD, "observer_sha256": _sha256_file(Path(__file__)),
                        "original_sha256": _sha256_file(ORIGINAL_SOURCE)})
        sys.path[:0] = [str(agent_root), str(runtime_root), str(runtime_root / "packages/python")]
        target = importlib.import_module("tests.sdk.test_timeline_restructure_guarded_runtime")
        body = original.target_body(Path(target.__file__))
        assert body == (original.TARGET_BODY_SHA256, original.TARGET_BODY_BYTES)
        report["source"] = {"body": body, "origins_boot": original.module_origins()}
        recorder.append("setup.import", "return", report["source"])
        import pytest
        monkeypatch = pytest.MonkeyPatch()
        context = tempfile.TemporaryDirectory(prefix="g5-budget-1605-", dir=args.tmpdir)
        tmp_path = Path(context.name)
        recorder.append("setup.fixture", "precall", {"tmp_path": str(tmp_path)})
        generator = target.restructure_runtime.__wrapped__(tmp_path, monkeypatch)
        env = next(generator)
        recorder.append("setup.fixture", "return", {"sql": original.sql_snapshot(env),
                        "origins": original.module_origins()})
        recorder.append("setup.inverse_fixture", "precall", {})
        env = target.restructure_inverse_runtime.__wrapped__(env, monkeypatch)
        report["boot"] = {"realm": safe_clone(env.service.realm),
                          "admission": safe_clone(getattr(env.service.store, "admission_report", None)),
                          "provider": _type_metadata(env.service._timeline_commit_provider),
                          "origins": original.module_origins()}
        recorder.append("setup.inverse_fixture", "return", report["boot"])
        phase = Phase(name="bootstrap")
        restores = original.install_wrappers(env, report, phase)
        recorder.append("scenario", "precall", {"sql": original.sql_snapshot(env)})
        original.run_scenario(env, report, phase, tmp_path)
        recorder.append("scenario", "return", {"verdict": report.get("verdict"),
                        "redo_no_write_on_refusal": report.get("redo_no_write_on_refusal")})
    except BaseException as exc:
        report["fatal"] = original.exception_record(exc)
        report["verdict"] = "FAIL: diagnostic failed; no retry authorized"
        recorder.append("diagnostic", "throw", report["fatal"])
    finally:
        report["origins_final"] = original.module_origins()
        recorder.append("origins", "final", report["origins_final"])
        # The flat packet owns the complete aggregate, including full redo/error/SQL data.
        recorder.append("diagnostic", "final", report)
        for owner, name, old, existed in reversed(restores):
            if existed:
                setattr(owner, name, old)
            elif name in getattr(owner, "__dict__", {}):
                delattr(owner, name)
        if generator is not None:
            generator.close()
        if monkeypatch is not None:
            monkeypatch.undo()
        if context is not None:
            context.cleanup()
        recorder.close()
        _ACTIVE_RECORDERS.clear()
    print(json.dumps({"verdict": report.get("verdict"), "packet": str(recorder.path)}))
    return 0 if report.get("verdict", "").startswith("PASS:") else 1


def main() -> int:
    if "--offline-smoke" in sys.argv:
        return offline_smoke()
    return run_live()


if __name__ == "__main__":
    raise SystemExit(main())
