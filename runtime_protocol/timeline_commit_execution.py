"""Owner-local execution exclusion; the command ledger is the only journal."""
from __future__ import annotations

import threading
from contextlib import contextmanager
from dataclasses import dataclass, field

from .errors import ProtocolError, RuntimeErrorBase
from .timeline_commit_store import detached, reject, request_identity, scope


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
        from .timeline_commit import CommitRejected
        from .errors import AuthorizationError, ForbiddenError

        try:
            return self.commit_store.lookup(context, authorize=authorize)
        except (CommitRejected, AuthorizationError, ForbiddenError):
            raise
        except Exception as exc:
            raise CommitOutcomeUnknown() from exc

    def execute(self, context, provider, port_factory, *, authorize):
        with self.commit_store.verification_scope():
            return self._execute(context, provider, port_factory, authorize=authorize)

    def _execute(self, context, provider, port_factory, *, authorize):
        context = detached(context)
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
