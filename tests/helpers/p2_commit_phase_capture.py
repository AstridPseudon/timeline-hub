"""Opt-in, harness-only observation for one mounted timeline commit.

This module is deliberately a test helper, not a Runtime hook.  It uses the
existing Python trace seam to observe the mounted HTTP handler, coordinator,
provider and store methods after the harness explicitly enables it.  It keeps
only a fixed phase vocabulary, relative monotonic times and bounded counts;
request bodies, headers, credentials, URLs, identifiers and exception text
never cross the observation boundary.

The normal App launcher does not import test helpers.  A launcher that wants
this diagnostic must start the Runtime worker with this checkout on
``PYTHONPATH`` and explicitly call ``P2CommitPhaseCapture(..., enabled=True)``
in that worker before starting its HTTP server, then call ``stop()`` after the
bounded request.  Existing launchers remain unchanged when the helper is not
enabled.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path
from types import TracebackType
from typing import Any, Self

PHASES = (
    "handler_entry",
    "authorization",
    "coordinator_admission",
    "coordinator_lock",
    "provider",
    "accept",
    "receipt",
    "http_response",
)


class P2CommitPhaseCapture:
    """Bounded observer for mounted Runtime commit calls.

    Observation is disabled unless ``enabled=True`` and ``start()`` is called.
    The observer is process-local and must be stopped in the same lifecycle
    owner that started it.  It is safe to use while Runtime request threads
    are active; each request gets a fresh local ordinal.
    """

    def __init__(
        self,
        sink: Path | str | None = None,
        *,
        enabled: bool = False,
        max_requests: int = 8,
        max_events: int = 128,
        max_bytes: int = 64 * 1024,
    ) -> None:
        if max_requests < 1 or max_events < 1 or max_bytes < 256:
            raise ValueError("capture bounds must be positive")
        self.enabled = enabled
        self.max_requests = max_requests
        self.max_events = max_events
        self.max_bytes = max_bytes
        self.sink = Path(sink).absolute() if sink is not None else None
        self.events: list[dict[str, Any]] = []
        self.failures = 0
        self.truncated = False
        self.active = False
        self._stream: Any = None
        self._start_ns = 0
        self._previous_trace: Any = None
        self._previous_thread_trace: Any = None
        self._frames: dict[int, dict[str, Any]] = {}
        self._handler_requests: dict[int, int] = {}
        self._thread_requests: dict[int, int] = {}
        self._requests: dict[int, dict[str, Any]] = {}
        self._next_request = 0
        self._lock = threading.Lock()

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None,
                 tb: TracebackType | None) -> None:
        self.stop()

    def start(self) -> Self:
        if not self.enabled or self.active:
            return self
        if sys.gettrace() is not None or threading.gettrace() is not None:
            raise ValueError("P2 phase capture requires no existing trace hook")
        if self.sink is not None:
            temporary = Path(os.environ.get("TMPDIR", "/tmp")).resolve()
            if not self.sink.parent.resolve().is_relative_to(temporary) or self.sink.is_symlink():
                raise ValueError("P2 phase sink must be a new file under TMPDIR")
            self._stream = os.fdopen(
                os.open(self.sink, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600),
                "w",
            )
        self._start_ns = time.monotonic_ns()
        self._previous_trace = sys.gettrace()
        self._previous_thread_trace = threading.gettrace()
        self.active = True
        threading.settrace(self._trace)
        sys.settrace(self._trace)
        return self

    def stop(self) -> None:
        if not self.active:
            return
        self.active = False
        if sys.gettrace() == self._trace:
            sys.settrace(self._previous_trace)
        if threading.gettrace() == self._trace:
            threading.settrace(self._previous_thread_trace)
        for request in list(self._requests.values()):
            self._summary(request)
        if self._stream is not None:
            try:
                self._stream.flush()
                self._stream.close()
            except Exception:  # noqa: BLE001 - observer failure cannot affect the operation
                self.failures += 1
            self._stream = None

    def _at_ms(self) -> float:
        return round((time.monotonic_ns() - self._start_ns) / 1_000_000, 3)

    def _write(self, event: dict[str, Any]) -> None:
        if len(self.events) >= self.max_events:
            self.truncated = True
            return
        encoded = json.dumps(event, separators=(",", ":"), sort_keys=True)
        current_bytes = sum(len(json.dumps(item, separators=(",", ":"))) + 1 for item in self.events)
        if current_bytes + len(encoded) + 1 > self.max_bytes:
            self.truncated = True
            return
        self.events.append(event)
        if self._stream is not None:
            try:
                self._stream.write(encoded + "\n")
                self._stream.flush()
            except Exception:  # noqa: BLE001 - observer failure cannot affect the operation
                # Diagnostics can never replace the operation being observed.
                self.failures += 1

    def _new_request(self, *, handler: Any = None, emit_handler: bool = False) -> int | None:
        with self._lock:
            if self._next_request >= self.max_requests:
                self.truncated = True
                return None
            self._next_request += 1
            ordinal = self._next_request
            self._requests[ordinal] = {
                "ordinal": ordinal,
                "phases": {phase: {"count": 0, "start_ms": None, "end_ms": None, "error": False}
                            for phase in PHASES},
                "last_phase": None,
                "handler": id(handler) if handler is not None else None,
                "thread": threading.get_ident(),
            }
            if handler is not None:
                self._handler_requests[id(handler)] = ordinal
            self._thread_requests[threading.get_ident()] = ordinal
        if emit_handler:
            self._begin(ordinal, "handler_entry")
        return ordinal

    def _request_for_frame(self, frame: Any) -> int | None:
        handler = frame.f_locals.get("self")
        if handler is not None:
            ordinal = self._handler_requests.get(id(handler))
            if ordinal is not None:
                return ordinal
        ordinal = self._thread_requests.get(threading.get_ident())
        if ordinal is not None:
            return ordinal
        parent = frame.f_back
        while parent is not None:
            handler = parent.f_locals.get("self")
            ordinal = self._handler_requests.get(id(handler)) if handler is not None else None
            if ordinal is not None:
                return ordinal
            parent = parent.f_back
        return None

    def _begin(self, ordinal: int, phase: str, **fields: Any) -> None:
        request = self._requests.get(ordinal)
        if request is None or phase not in PHASES:
            return
        state = request["phases"][phase]
        state["count"] = min(state["count"] + 1, 32)
        now = self._at_ms()
        state["start_ms"] = now if state["start_ms"] is None else state["start_ms"]
        request["last_phase"] = phase
        safe_fields = {"status": fields["status"]} if phase == "http_response" and type(fields.get("status")) is int else {}
        self._write({"schema_version": 1, "request": ordinal, "phase": phase,
                     "state": "start", "at_ms": now, "count": state["count"], **safe_fields})

    def _end(self, ordinal: int, phase: str, *, error: bool = False, **fields: Any) -> None:
        request = self._requests.get(ordinal)
        if request is None or phase not in PHASES:
            return
        state = request["phases"][phase]
        state["end_ms"] = self._at_ms()
        state["error"] = state["error"] or error
        safe_fields = {"status": fields["status"]} if phase == "http_response" and type(fields.get("status")) is int else {}
        self._write({"schema_version": 1, "request": ordinal, "phase": phase,
                     "state": "raised" if error else "end", "at_ms": state["end_ms"],
                     "count": state["count"], **safe_fields})

    def _summary(self, request: dict[str, Any]) -> None:
        phases = {}
        for phase in PHASES:
            state = request["phases"][phase]
            phases[phase] = {
                "status": "UNKNOWN" if state["count"] == 0 else "observed",
                "count": state["count"],
                "start_ms": state["start_ms"],
                "end_ms": state["end_ms"],
            }
            if state["error"]:
                phases[phase]["status"] = "raised"
        self._write({"schema_version": 1, "request": request["ordinal"], "phase": "summary",
                     "last_phase": request["last_phase"] or "UNKNOWN", "phases": phases,
                     "truncated": self.truncated})

    @staticmethod
    def _phase(frame: Any) -> str | None:
        module = frame.f_globals.get("__name__")
        qualname = frame.f_code.co_qualname
        if module == "runtime_protocol.server":
            return {
                "RuntimeHandler._timeline_commit": "handler_entry",
                "RuntimeHandler._authorize_timeline_commit": "authorization",
                "RuntimeHandler._send": "http_response",
            }.get(qualname)
        if module == "runtime_protocol.timeline_commit_execution":
            return "coordinator_admission" if qualname == "CommitExecutionCoordinator._execution" else None
        if module == "runtime_protocol.timeline_commit_port":
            return "accept" if qualname == "RequestCommitPort.accept" else None
        if module == "runtime_protocol.timeline_commit_store":
            return "receipt" if qualname == "TimelineCommitStore.accept" else None
        return None

    @staticmethod
    def _code_for(value: Any) -> Any:
        function = getattr(value, "__func__", value)
        return getattr(function, "__code__", None)

    def _trace(self, frame: Any, event: str, arg: Any) -> Any:
        if not self.active:
            return None
        try:
            return self._trace_inner(frame, event, arg)
        except Exception:  # noqa: BLE001 - observer failure cannot affect the operation
            self.failures += 1
            return self._trace

    def _trace_inner(self, frame: Any, event: str, arg: Any) -> Any:
        if event == "call":
            phase = self._phase(frame)
            if phase == "handler_entry":
                ordinal = self._new_request(handler=frame.f_locals.get("self"), emit_handler=True)
                if ordinal is None:
                    return None
                self._frames[id(frame)] = {"phase": phase, "ordinal": ordinal, "error": False}
                return self._trace
            ordinal = self._request_for_frame(frame)
            if phase is None and frame.f_code.co_qualname == "CommitExecutionCoordinator.execute":
                ordinal = ordinal or self._new_request()
                provider = frame.f_locals.get("provider")
                code = self._code_for(getattr(provider, "commit", None))
                if code is not None:
                    self._frames[code] = {"dynamic": "provider"}
            if phase is None:
                if ordinal is None:
                    return None
                dynamic = self._frames.get(frame.f_code)
                phase = dynamic.get("dynamic") if dynamic else None
            if phase is None or ordinal is None:
                return None
            self._begin(ordinal, phase,
                        **({"status": frame.f_locals.get("status")}
                           if phase == "http_response" and type(frame.f_locals.get("status")) is int else {}))
            self._frames[id(frame)] = {"phase": phase, "ordinal": ordinal, "error": False,
                                       "yielded": False, "acquired": False}
            if phase == "coordinator_admission":
                return self._trace
            return self._trace

        state = self._frames.get(id(frame))
        if state is None:
            return self._trace
        phase = state["phase"]
        ordinal = state["ordinal"]
        if event == "exception":
            state["error"] = True
            return self._trace
        if event != "return":
            return self._trace
        if phase == "coordinator_admission" and not state["yielded"]:
            if state["error"]:
                self._end(ordinal, phase, error=True)
                del self._frames[id(frame)]
                return self._trace
            state["yielded"] = True
            state["acquired"] = arg is True
            if state["acquired"]:
                self._begin(ordinal, "coordinator_lock")
            return self._trace
        if phase == "coordinator_admission" and state["yielded"]:
            if state["acquired"]:
                self._end(ordinal, "coordinator_lock", error=state["error"])
            self._end(ordinal, phase, error=state["error"])
        else:
            fields = {}
            if phase == "http_response" and type(frame.f_locals.get("status")) is int:
                fields["status"] = frame.f_locals["status"]
            self._end(ordinal, phase, error=state["error"], **fields)
        del self._frames[id(frame)]
        return self._trace


CommitPhaseCapture = P2CommitPhaseCapture


def install_p2_commit_phase_capture(*args: Any, **kwargs: Any) -> P2CommitPhaseCapture:
    """Explicit activation convenience for a harness-owned worker."""
    capture = P2CommitPhaseCapture(*args, enabled=True, **kwargs)
    return capture.start()
