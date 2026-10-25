"""Private D111b instrumentation for the real Runtime commit process.

This module is loaded only by the diagnostic's throwaway Runtime overlay.  It
does not use ``sys.setprofile`` and records hashes, counts, byte totals, and
durations only; request payloads and values never leave the child process.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import threading
import time
from pathlib import Path

if os.environ.get("D111B_ENABLED") == "1":
    _log_dir = Path(os.environ["D111B_LOG_DIR"])
    _log_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    _mode = os.environ.get("D111B_MODE", "sample")
    _max_capture = 8 * 1024 * 1024
    _lock = threading.RLock()
    _local = threading.local()
    _states: dict[int, dict] = {}
    _records: list[dict] = []

    def _state_stack() -> list[dict]:
        stack = getattr(_local, "stack", None)
        if stack is None:
            stack = []
            _local.stack = stack
        return stack

    def _active() -> dict | None:
        stack = _state_stack()
        return stack[-1] if stack else None

    def _encoded_size(value) -> tuple[int | None, bool]:
        if _mode != "counter":
            return None, False
        try:
            encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
        except (TypeError, ValueError, RecursionError):
            return None, True
        if len(encoded) > _max_capture:
            return _max_capture, True
        return len(encoded), False

    def _add_bytes(record: dict, key: str, value) -> None:
        size, limited = _encoded_size(value)
        if size is not None:
            record[key] += size
        record[f"{key}_calls"] += 1
        if limited:
            record[f"{key}_limited"] += 1

    def _sha(value) -> str:
        try:
            encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
        except (TypeError, ValueError, RecursionError):
            return "unhashable"
        return hashlib.sha256(encoded).hexdigest()

    def _new_read() -> dict:
        return {
            "storecall_ns": 0,
            "port_read_ns": 0,
            "detached_ns": 0,
            "deepcopy_ns": 0,
            "finite_json_ns": 0,
            "detached_calls": 0,
            "deepcopy_calls": 0,
            "finite_json_calls": 0,
            "detached_bytes": 0,
            "deepcopy_bytes": 0,
            "finite_json_bytes": 0,
            "detached_bytes_calls": 0,
            "deepcopy_bytes_calls": 0,
            "finite_json_bytes_calls": 0,
            "detached_bytes_limited": 0,
            "deepcopy_bytes_limited": 0,
            "finite_json_bytes_limited": 0,
            "source_document_ns": 0,
            "source_document_calls": 0,
            "source_document_bytes": 0,
            "source_document_bytes_calls": 0,
            "source_document_bytes_limited": 0,
            "source_store_ns": 0,
            "source_store_calls": 0,
            "source_store_bytes": 0,
            "source_store_bytes_calls": 0,
            "source_store_bytes_limited": 0,
        }

    def _new_state(port) -> dict:
        request = getattr(port, "_RequestCommitPort__request", {})
        return {
            "label": request.get("label"),
            "request_sha256": _sha(request),
            "request_bytes": len(json.dumps(request, ensure_ascii=False, separators=(",", ":")).encode("utf-8")),
            "reads": [],
            "repeat_revision_hashes": [],
            "revision_hashes": {},
            "mutation_leak": False,
            "sys_setprofile": False,
        }

    def _state_for(port) -> dict:
        key = id(port)
        with _lock:
            state = _states.get(key)
            if state is None:
                state = _new_state(port)
                _states[key] = state
            return state

    def _flush(port) -> None:
        state = _states.pop(id(port), None)
        if state is None or not state["reads"]:
            return
        record = {"kind": "request", **state, "pid": os.getpid()}
        with _lock:
            _records.append(record)
            destination = _log_dir / "port-metrics.json"
            destination.write_text(json.dumps({"sys_setprofile": False, "records": _records}, sort_keys=True) + "\n", encoding="utf-8")
            destination.chmod(0o600)

    original_deepcopy = copy.deepcopy

    def measured_deepcopy(value, memo=None):
        record = _active()
        started = time.perf_counter_ns()
        result = original_deepcopy(value) if memo is None else original_deepcopy(value, memo)
        elapsed = time.perf_counter_ns() - started
        if record is not None:
            record["deepcopy_ns"] += elapsed
            record["deepcopy_calls"] += 1
            _add_bytes(record, "deepcopy_bytes", value)
        return result

    copy.deepcopy = measured_deepcopy

    from runtime_protocol import timeline_commit_inputs as _inputs_module
    from runtime_protocol import timeline_commit_port as _port_module
    from runtime_protocol import timeline_commit_store as _store_module
    from runtime_protocol import timeline_commit_validation as _validation_module

    original_finite_json = _validation_module.finite_json
    original_detached = _validation_module.detached
    original_port_detached = _port_module.detached
    original_read = _port_module.RequestCommitPort._read
    original_document = _port_module.RequestCommitPort._document
    original_close = _port_module.RequestCommitPort.close
    original_revision_closure = _port_module.RequestCommitPort.revision_closure
    original_capture_input = _inputs_module.capture_document_input
    original_capture_document = getattr(_store_module.TimelineCommitStore, "_capture_document_input", None)

    def measured_finite_json(value) -> None:
        record = _active()
        started = time.perf_counter_ns()
        result = original_finite_json(value)
        if record is not None:
            record["finite_json_ns"] += time.perf_counter_ns() - started
            record["finite_json_calls"] += 1
            _add_bytes(record, "finite_json_bytes", value)
        return result

    def measured_detached(value):
        record = _active()
        started = time.perf_counter_ns()
        result = original_detached(value)
        if record is not None:
            record["detached_ns"] += time.perf_counter_ns() - started
            record["detached_calls"] += 1
            _add_bytes(record, "detached_bytes", value)
        return result

    def measured_port_detached(value):
        return measured_detached(value)

    _validation_module.finite_json = measured_finite_json
    _inputs_module.finite_json = measured_finite_json
    _validation_module.detached = measured_detached
    _port_module.detached = measured_port_detached
    _store_module.detached = measured_port_detached

    def measured_document(self, pin, transcript):
        record = _active()
        started = time.perf_counter_ns()
        result = original_document(self, pin, transcript)
        if record is not None:
            record["source_document_ns"] += time.perf_counter_ns() - started
            record["source_document_calls"] += 1
            _add_bytes(record, "source_document_bytes", result)
        return result

    def measured_capture_input(*args, **kwargs):
        record = _active()
        started = time.perf_counter_ns()
        result = original_capture_input(*args, **kwargs)
        if record is not None:
            record["source_store_ns"] += time.perf_counter_ns() - started
            record["source_store_calls"] += 1
            _add_bytes(record, "source_store_bytes", result)
        return result

    def measured_capture_document(self, *args, **kwargs):
        record = _active()
        started = time.perf_counter_ns()
        assert original_capture_document is not None
        result = original_capture_document(self, *args, **kwargs)
        if record is not None:
            record["source_store_ns"] += time.perf_counter_ns() - started
            record["source_store_calls"] += 1
            _add_bytes(record, "source_store_bytes", result)
        return result

    def measured_read(self, call):
        state = _state_for(self)
        record = _new_read()
        stack = _state_stack()
        stack.append(record)
        started = time.perf_counter_ns()

        def timed_store_call():
            call_started = time.perf_counter_ns()
            try:
                return call()
            finally:
                record["storecall_ns"] += time.perf_counter_ns() - call_started

        try:
            return original_read(self, timed_store_call)
        finally:
            record["port_read_ns"] = time.perf_counter_ns() - started
            stack.pop()
            state["reads"].append(record)

    def measured_revision_closure(self, revision_id):
        result = original_revision_closure(self, revision_id)
        state = _state_for(self)
        if isinstance(result, dict):
            value_hash = _sha(result)
            revision_key = _sha(revision_id)
            previous = state["revision_hashes"].get(revision_key)
            if previous is not None and previous != value_hash:
                state["mutation_leak"] = True
            state["revision_hashes"][revision_key] = value_hash
            state["repeat_revision_hashes"].append({"revision": revision_key, "value": value_hash})
        return result

    def measured_close(self):
        try:
            return original_close(self)
        finally:
            _flush(self)

    _port_module.RequestCommitPort._read = measured_read
    _port_module.RequestCommitPort._document = measured_document
    _port_module.RequestCommitPort.revision_closure = measured_revision_closure
    _port_module.RequestCommitPort.close = measured_close
    if original_capture_document is None:
        _inputs_module.capture_document_input = measured_capture_input
    else:
        _store_module.TimelineCommitStore._capture_document_input = measured_capture_document

    from runtime_protocol import server as _server_module

    original_send = _server_module.RuntimeHandler._send

    def measured_send(self, status, *args, **kwargs):
        tag = self.headers.get("X-D111B-Refusal-Tag")
        if tag:
            print(f"D111b refusal tag={tag} status={status}", file=sys.stderr, flush=True)
        return original_send(self, status, *args, **kwargs)

    _server_module.RuntimeHandler._send = measured_send
    print(f"D111b startup run={os.environ.get('D111B_RUN_ID', 'unknown')} mode={_mode}", file=sys.stderr, flush=True)

