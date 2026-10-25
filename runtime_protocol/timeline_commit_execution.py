"""Owner-local execution exclusion; the command ledger is the only journal."""
from __future__ import annotations

import json
import re
import secrets
import sys
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field

from .errors import ProtocolError, RuntimeErrorBase
from .timeline_commit_store import detached, reject, request_identity, scope


_REQUEST_ID_RE = re.compile(r"^[a-f0-9]{32}$")
_MAX_EXCEPTION_CLASSES = 8
_MAX_FRAMES = 32


def _new_request_id():
    """Create the private Runtime correlation value for one commit request."""
    return secrets.token_hex(16)


def _validated_request_id(value):
    if type(value) is str and _REQUEST_ID_RE.fullmatch(value):
        return value
    return _new_request_id()


def _exception_class_chain(error):
    classes = []
    seen = set()
    current = error
    while current is not None and id(current) not in seen and len(classes) < _MAX_EXCEPTION_CLASSES:
        seen.add(id(current))
        kind = type(current)
        classes.append(f"{kind.__module__}.{kind.__qualname__}")
        current = current.__cause__ or current.__context__
    return classes


def _exception_frames(error):
    frames = []
    seen = set()
    current = error
    while current is not None and id(current) not in seen and len(frames) < _MAX_FRAMES:
        seen.add(id(current))
        traceback = current.__traceback__
        while traceback is not None and len(frames) < _MAX_FRAMES:
            code = traceback.tb_frame.f_code
            frames.append(f"{code.co_filename}:{traceback.tb_lineno}:{code.co_name}")
            traceback = traceback.tb_next
        current = current.__cause__ or current.__context__
    return frames


def _emit_redacted_diagnostic(request_id, error):
    """Write one bounded, source-only diagnostic without inspecting exception data."""
    try:
        payload = {
            "event": "timeline_commit_error",
            "request_id": _validated_request_id(request_id),
            "exception_class_chain": _exception_class_chain(error),
            "frames": _exception_frames(error),
        }
        line = "runtime.timeline_commit.error " + json.dumps(
            payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")
        )
        sys.stderr.write(line + "\n")
    except BaseException:  # noqa: BLE001, S110 - diagnostics cannot affect the result
        # Diagnostics must never replace the original commit outcome.
        pass


class CommitOutcomeUnknown(RuntimeErrorBase):
    code = "not_ready"
    status = 503

    def __init__(self):
        super().__init__("Timeline commit outcome unavailable; retry the exact request",
                         details={"reason": "runtime_unavailable"})


@dataclass
class _Entry:
    request_hash: str
    users: int = 0
    lock: object = field(default_factory=threading.Lock)


class CommitExecutionCoordinator:
    def __init__(self, commit_store):
        self.commit_store = commit_store
        self._guard = threading.Lock()
        self._entries = {}

    @contextmanager
    def _execution(self, context):
        key = (scope(context), context["idempotency_key"])
        with self._guard:
            entry = self._entries.get(key)
            if entry is None:
                entry = self._entries[key] = _Entry(context["request_hash"])
            mismatch = entry.request_hash != context["request_hash"]
            if not mismatch:
                entry.users += 1
        if mismatch:
            # A changed request may have entered after the original accepted.
            # The durable winner takes precedence over this transient hash.
            yield False
            return
        try:
            with entry.lock:
                yield True
        finally:
            with self._guard:
                entry.users -= 1
                if entry.users == 0:
                    del self._entries[key]

    def _lookup(self, context, authorize):
        from .errors import AuthorizationError, ForbiddenError
        from .timeline_commit import CommitRejected

        try:
            return self.commit_store.lookup(context, authorize=authorize)
        except (CommitRejected, AuthorizationError, ForbiddenError):
            raise
        except Exception as exc:
            _emit_redacted_diagnostic(context.get("request_id"), exc)
            raise CommitOutcomeUnknown() from exc

    def execute(self, context, provider, port_factory, *, authorize):
        with self.commit_store.verification_scope():
            return self._execute(context, provider, port_factory, authorize=authorize)

    def _execute(self, context, provider, port_factory, *, authorize):
        context = detached(context)
        context["request_id"] = _validated_request_id(context.get("request_id"))
        if request_identity(context) != context["request_hash"]:
            reject("invocation_mismatch", status=422)
        # There is intentionally no optimistic dependency/head read here. Even
        # callers with an earlier cache miss repeat this lookup after waiting.
        with self._execution(context) as acquired:
            replay = self._lookup(context, authorize)
            if replay is not None:
                return replay
            if not acquired:
                reject("idempotency_mismatch")
            outcome = error = port = None
            try:
                port = port_factory(detached(context))
                provider_context = detached(port._provider_context()) if hasattr(port, "_provider_context") else detached(context)
                if any(provider_context[k] != context[k] for k in ("invocation", "idempotency_key", "request_hash", "realm_id", "publisher")):
                    raise ProtocolError("request port changed invocation identity")
                outcome = detached(provider.commit(provider_context, port))
                if hasattr(port, "verify_outcome"):
                    port.verify_outcome(outcome)
            except BaseException as exc:
                error = exc
            finally:
                if port is not None:
                    try:
                        port.close()
                    except BaseException as exc:
                        if error is None:
                            error = exc
            # No provider completion, including a close/hook exception, can
            # supersede a committed winner. A failed read is an unknown outcome.
            replay = self._lookup(context, authorize)
            if replay is not None:
                return replay
            if error is not None:
                raise error
            if not isinstance(outcome, dict):
                raise ProtocolError("provider returned no commit outcome")
            if "receipt" in outcome:
                if outcome["receipt"] is not None:
                    raise ProtocolError("provider claimed acceptance without a durable receipt")
                if outcome.get("data", {}).get("status") != "preview" or not context["request"].get("dry_run", False):
                    raise ProtocolError("provider returned an invalid preview")
            elif outcome.get("details", {}).get("status") not in {"conflict", "refused", "invalid"}:
                raise ProtocolError("provider returned an invalid commit failure")
            else:
                self.commit_store.clear_replay_memo()
            return outcome
