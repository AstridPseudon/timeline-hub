"""Owner-local execution exclusion; the command ledger is the only journal."""
from __future__ import annotations

import hashlib
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
_MAX_DIAGNOSTIC_BYTES = 4096
_MAX_METADATA_BYTES = 128
_SAFE_CLASS_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(?:\.(?:[A-Za-z_][A-Za-z0-9_]*|<locals>))*$"
)
_SAFE_FILENAME_RE = re.compile(r"^(?:[A-Za-z0-9_.-]+|<[^<>\r\n]{1,64}>)$")
_SAFE_REASON_RE = re.compile(r"^(?:[a-z_]+|catchall:[A-Za-z0-9_.<>:-]{1,256})$")


def _new_request_id():
    """Create the private Runtime correlation value for one commit request."""
    return secrets.token_hex(16)


def _validated_request_id(value):
    if type(value) is str and _REQUEST_ID_RE.fullmatch(value):
        return value
    return _new_request_id()


def _metadata_digest(value):
    if not isinstance(value, str):
        return "sha256:invalid"
    return "sha256:" + hashlib.sha256(value.encode("utf-8", "surrogatepass")).hexdigest()


def _safe_metadata(value, pattern):
    if not isinstance(value, str):
        return "sha256:invalid"
    try:
        if (len(value.encode("utf-8", "surrogatepass")) <= _MAX_METADATA_BYTES
                and pattern.fullmatch(value)):
            return value
    except (UnicodeError, TypeError):
        pass
    return _metadata_digest(value)


def _exception_class(kind):
    try:
        module = _safe_metadata(kind.__module__, _SAFE_CLASS_RE)
        qualname = _safe_metadata(kind.__qualname__, _SAFE_CLASS_RE)
    except BaseException:  # noqa: BLE001 - diagnostics cannot affect the result
        return "sha256:invalid"
    return f"{module}.{qualname}"


def _exception_class_chain(error):
    classes = []
    seen = set()
    current = error
    while current is not None and id(current) not in seen and len(classes) < _MAX_EXCEPTION_CLASSES:
        seen.add(id(current))
        classes.append(_exception_class(type(current)))
        try:
            current = current.__cause__ or current.__context__
        except BaseException:  # noqa: BLE001 - diagnostics cannot affect the result
            break
    return classes


def _exception_frames(error):
    frames = []
    seen = set()
    current = error
    while current is not None and id(current) not in seen and len(frames) < _MAX_FRAMES:
        seen.add(id(current))
        try:
            traceback = current.__traceback__
        except BaseException:  # noqa: BLE001 - diagnostics cannot affect the result
            traceback = None
        while traceback is not None and len(frames) < _MAX_FRAMES:
            try:
                code = traceback.tb_frame.f_code
                filename = _safe_metadata(code.co_filename, _SAFE_FILENAME_RE)
                function = _safe_metadata(code.co_name, _SAFE_CLASS_RE)
                lineno = traceback.tb_lineno
                if type(lineno) is not int or not 0 <= lineno <= 1_000_000_000:
                    lineno = 0
                frames.append(f"{filename}:{lineno}:{function}")
                traceback = traceback.tb_next
            except BaseException:  # noqa: BLE001 - diagnostics cannot affect the result
                frames.append("sha256:invalid:0:sha256:invalid")
                break
        try:
            current = current.__cause__ or current.__context__
        except BaseException:  # noqa: BLE001 - diagnostics cannot affect the result
            break
    return frames


def _diagnostic_line(payload):
    def fits(value):
        return len((value + "\n").encode("utf-8")) <= _MAX_DIAGNOSTIC_BYTES

    line = "runtime.timeline_commit.error " + json.dumps(
        payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )
    if fits(line):
        return line
    compact = dict(payload)
    compact["exception_class_chain"] = [_metadata_digest(json.dumps(
        payload["exception_class_chain"], separators=(",", ":")
    ))]
    compact["frames"] = [_metadata_digest(json.dumps(
        payload["frames"], separators=(",", ":")
    ))]
    line = "runtime.timeline_commit.error " + json.dumps(
        compact, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )
    if fits(line):
        return line
    compact["exception_class_chain"] = []
    compact["frames"] = []
    return "runtime.timeline_commit.error " + json.dumps(
        compact, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )


def _diagnostic_reason(error, reason):
    if reason is None:
        if error is None:
            return "catchall:unknown"
        return "catchall:" + _exception_class(type(error))
    if isinstance(reason, str) and _SAFE_REASON_RE.fullmatch(reason):
        return reason
    return "catchall:invalid"


def _emit_redacted_diagnostic(request_id, error=None, *, reason=None):
    """Write one bounded, source-only diagnostic without inspecting exception data."""
    try:
        payload = {
            "event": "timeline_commit_error",
            "request_id": _validated_request_id(request_id),
            "reason": _diagnostic_reason(error, reason),
            "exception_class_chain": _exception_class_chain(error),
            "frames": _exception_frames(error),
        }
        sys.stderr.write(_diagnostic_line(payload) + "\n")
    except BaseException:  # noqa: BLE001, S110 - diagnostics cannot affect the result
        # Diagnostics must never replace the original commit outcome.
        pass


_HISTORY_MESSAGE_TAGS = {
    "publication/revision pins disagree": "port_ancestor_pin_mismatch",
    "publication is outside request ancestry": "port_ancestor_outside_request",
    "history bounds disagree": "port_history_bounds_mismatch",
    "revision is outside request ancestry or declared source": "port_revision_outside_ancestry",
    "base pins disagree": "port_base_pins_mismatch",
    "candidate head was not observed through this port": "port_candidate_head_unobserved",
}

_HISTORY_SOURCE_TAGS = frozenset({
    "history_baseline_publication_dependency",
    "history_baseline_corrupt_publication_facts",
    "history_baseline_source_publication_missing",
    "history_baseline_unretained_document_dependency",
    "history_provider_or_store_guard",
    "port_ancestor_pin_mismatch",
    "port_ancestor_outside_request",
    "port_history_bounds_mismatch",
    "port_revision_outside_ancestry",
    "port_base_pins_mismatch",
    "port_candidate_head_unobserved",
    "store_membership_missing",
    "store_head_missing",
    "store_head_revision_mismatch",
    "store_head_canonical_mismatch",
    "store_head_catalog_corrupt",
    "store_archived_scope_missing",
    "store_history_entry_missing",
    "store_history_ledger_mismatch",
    "store_history_bound_revision_mismatch",
    "store_history_bound_order_invalid",
    "store_history_chain_break",
    "store_history_through_mismatch",
    "store_revision_scope_missing",
    "store_revision_missing",
    "store_revision_dependency_missing",
    "store_shot_input_closure_ambiguous",
    "store_shot_parent_missing",
    "store_occurrence_rows_mismatch",
    "store_occurrence_row_mismatch",
    "store_dependency_rows_mismatch",
    "store_shot_revision_scope_missing",
    "store_history_ancestry_cycle",
    "store_history_base_outside_ancestry",
    "store_inverse_stage_targets_unavailable",
    "store_request_base_mismatch",
    "store_adopt_existing_head",
    "store_adopt_nonempty_scope",
    "store_adopt_existing_parent",
    "store_adopt_legacy_shell_mismatch",
    "store_adopt_prior_publication",
    "store_bootstrap_unpublished_head",
    "store_reference_projection_prepare_history",
    "store_reference_projection_apply_history",
})


def _history_diagnostic_reason(failure, *, source_reason=None):
    """Map an intentional history refusal to a bounded private source tag."""
    if not isinstance(failure, dict):
        return None
    details = failure.get("details")
    if not isinstance(details, dict) or details.get("reason") != "history_unavailable":
        return None
    if source_reason is not None:
        return source_reason if source_reason in _HISTORY_SOURCE_TAGS else None
    integrity_reason = details.get("integrity_reason")
    if isinstance(integrity_reason, str):
        if integrity_reason.startswith("publication_dependency_unavailable:"):
            return "history_baseline_publication_dependency"
        if integrity_reason.startswith("missing_or_corrupt_publication_facts:"):
            return "history_baseline_corrupt_publication_facts"
        if integrity_reason == "source_publication_missing":
            return "history_baseline_source_publication_missing"
        if integrity_reason == "unretained_document_dependency":
            return "history_baseline_unretained_document_dependency"
    message = failure.get("message")
    if message in _HISTORY_MESSAGE_TAGS:
        return _HISTORY_MESSAGE_TAGS[message]
    return "history_provider_or_store_guard"


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

    def _lookup(self, context, authorize, *, diagnostic_request_id=None):
        from .errors import AuthorizationError, ForbiddenError
        from .timeline_commit import CommitRejected

        try:
            return self.commit_store.lookup(context, authorize=authorize)
        except (CommitRejected, AuthorizationError, ForbiddenError):
            raise
        except Exception as exc:
            _emit_redacted_diagnostic(diagnostic_request_id, exc)
            raise CommitOutcomeUnknown() from exc

    def execute(self, context, provider, port_factory, *, authorize, diagnostic_request_id=None):
        with self.commit_store.verification_scope():
            return self._execute(context, provider, port_factory, authorize=authorize,
                                 diagnostic_request_id=diagnostic_request_id)

    def _execute(self, context, provider, port_factory, *, authorize, diagnostic_request_id=None):
        context = detached(context)
        if request_identity(context) != context["request_hash"]:
            reject("invocation_mismatch", status=422)
        # There is intentionally no optimistic dependency/head read here. Even
        # callers with an earlier cache miss repeat this lookup after waiting.
        with self._execution(context) as acquired:
            replay = self._lookup(context, authorize, diagnostic_request_id=diagnostic_request_id)
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
            replay = self._lookup(context, authorize, diagnostic_request_id=diagnostic_request_id)
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
