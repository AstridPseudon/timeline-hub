"""Bounded observer for the one original-nine qualification run."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

EVIDENCE = Path(os.environ["ORIGINAL9_EVIDENCE"])
EVIDENCE.mkdir(parents=True, exist_ok=True)
_counter = 0


def _json(value):
    try:
        json.dumps(value)
    except TypeError:
        if hasattr(value, "bundle") and hasattr(value, "records"):
            return {
                "type": type(value).__name__,
                "bundle": _json(value.bundle),
                "records": _json(value.records),
                "commands": _json(getattr(value, "commands", [])),
                "sequential_execution": _json(getattr(value, "_sequential_execution", [])),
            }
        return {"type": type(value).__name__, "repr": repr(value)}
    return copy.deepcopy(value)


def _hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _db_hash(port):
    try:
        return _hash(list(port._RequestCommitPort__store.conn.iterdump()))
    except Exception as exc:  # pragma: no cover - diagnostics must not affect the run
        return {"observer_error": repr(exc)}


def _credential_keys(value, path=()):
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if any(token in lowered for token in ("password", "secret", "token", "credential", "api_key", "authorization")):
                found.append(".".join((*path, str(key))))
            found.extend(_credential_keys(child, (*path, str(key))))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_credential_keys(child, (*path, str(index))))
    return found


def _write(record):
    global _counter
    path = EVIDENCE / f"original9-capture-{_counter:02d}.json"
    _counter += 1
    encoded = json.dumps(record, sort_keys=True, indent=2) + "\n"
    path.write_text(encoded, encoding="utf-8")
    destination = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design")
    (destination / ("runtime-R2r-history-1543-" + hashlib.sha256(encoded.encode()).hexdigest()[:20] + ".json")).write_text(encoded)


def pytest_configure(config):
    del config
    module = __import__("astrid.sdk.timeline._commit_preview", fromlist=["capture_sequential_execution"])
    helper = module.capture_sequential_execution

    def wrapped(port, context, original, plan, replay_bindings, prepared):
        original_capture = port.capture_sequential_execution
        original_accept = getattr(port, "accept", None)
        original_preview = getattr(port, "preview", None)
        record = {
            "kind": "original9",
            "context": _json(context),
            "request": _json(context["request"]),
            "prepared": _json(prepared),
            "provider_original": _json(original),
            "provider_plan": _json(plan),
            "provider_replay_bindings": _json(replay_bindings),
            "database_before_validation": _db_hash(port),
            "outcome": None,
            "database_after_attempt": None,
            "exception": None,
        }

        def receive(capture):
            # Durable evidence is written before the detached proof crosses
            # the port and before preview/accept invokes normal validation.
            record["capture"] = _json(capture)
            try:
                record["base_closure"] = _json(port.revision_closure(context["request"]["base_revision_id"]))
            except Exception as exc:
                record["base_closure_error"] = repr(exc)
            try:
                record["source_closure"] = _json(port.revision_closure(prepared["expected_head"]["revision_id"]))
            except Exception as exc:
                record["source_closure_error"] = repr(exc)
            try:
                record["history"] = _json(port.history(prepared["expected_head"], limit=100))
            except Exception as exc:
                record["history_error"] = repr(exc)
            record["credential_keys"] = sorted(set(_credential_keys(record)))
            record["credential_clean"] = not record["credential_keys"]
            _write(record)
            return original_capture(capture)

        port.capture_sequential_execution = receive

        def attempt(method, name, candidate):
            try:
                result = method(candidate)
                record["outcome"] = {"method": name, "status": "returned", "result": _json(result)}
                return result
            except Exception as exc:
                record["outcome"] = {"method": name, "status": "raised", "type": type(exc).__name__}
                record["exception"] = repr(exc)
                raise
            finally:
                record["database_after_attempt"] = _db_hash(port)
                record["no_write"] = record["database_before_validation"] == record["database_after_attempt"]
                _write({"kind": "original9-outcome", **record})

        if callable(original_accept):
            port.accept = lambda candidate: attempt(original_accept, "accept", candidate)
        if callable(original_preview):
            port.preview = lambda candidate: attempt(original_preview, "preview", candidate)
        return helper(port, context, original, plan, replay_bindings, prepared)

    module.capture_sequential_execution = wrapped


def pytest_runtest_logreport(report):
    value = {"nodeid": report.nodeid, "when": report.when, "outcome": report.outcome,
             "longrepr": report.longreprtext, "sections": report.sections,
             "duration": report.duration}
    encoded = json.dumps(value, sort_keys=True, indent=2) + "\n"
    token = hashlib.sha256((report.nodeid + ":" + report.when).encode()).hexdigest()[:20]
    (EVIDENCE / ("pytest-report-" + token + ".json")).write_text(encoded)
    destination = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design")
    (destination / ("runtime-R2r-history-1543-report-" + token + ".json")).write_text(encoded)
