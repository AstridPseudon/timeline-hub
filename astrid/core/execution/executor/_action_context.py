"""Private custody of one managed Python producer invocation.

The host extends its existing private admission envelope from the retained claim.
Only the verified runner installs the ephemeral view; action inputs and ambient
client/environment state are never identity sources. Runtime still owns settlement.
"""
from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

_PRODUCER_FIELDS = ("task_id", "attempt_id", "executor_id", "fence", "runtime_epoch")
_TARGET_FIELDS = ("project_id", "timeline_id", "base_revision_id", "base_publication_id")
_current: ContextVar[_ActionContext | None] = ContextVar("_astrid_action_context", default=None)


def _text(value: Any) -> bool:
    return type(value) is str and bool(value.strip())


def _positive_int(value: Any) -> bool:
    return type(value) is int and value > 0


def _producer_action_admission(definition, admission: Mapping[str, Any], task: Mapping[str, Any],
                               *, executor_id: str, runtime_epoch: int) -> Mapping[str, Any]:
    """Bind only existing managed producer outputs, leaving other actions alone."""
    invocation = definition.metadata.get("action_invocation", {})
    if invocation.get("kind") != "python" or not any(
            port.artifact_type == "timeline/authoring-proposal" for port in definition.outputs):
        return admission
    from astrid.core.execution.generic_host import HostError, _admitted_task_spec

    producer = {key: task.get(key) for key in _PRODUCER_FIELDS}
    producer["task_id"] = task.get("id")
    if (any(not _text(producer[key]) for key in _PRODUCER_FIELDS[:3])
            or any(not _positive_int(producer[key]) for key in _PRODUCER_FIELDS[3:])
            or any(producer[key] != admission.get(key) for key in ("task_id", "attempt_id", "fence"))
            or producer["executor_id"] != executor_id
            or type(runtime_epoch) is not int or producer["runtime_epoch"] != runtime_epoch
            or task.get("capability") != definition.id):
        raise HostError("managed Python producer requires a matching live claim identity")
    dependencies = _admitted_task_spec(task).get("runtime_dependencies")
    publication = dependencies.get("publication") if isinstance(dependencies, Mapping) else None
    target = publication.get("admitted_target") if isinstance(publication, Mapping) else None
    if (not isinstance(target, Mapping) or set(target) != set(_TARGET_FIELDS)
            or any(not _text(target[key]) for key in _TARGET_FIELDS)
            or target["project_id"] != task.get("project_id")):
        raise HostError("managed Python producer requires its admitted publication target")
    return {**admission, **producer, "admitted_target": dict(target)}


class _ActionContext:
    def __init__(self, request, admission: Mapping[str, Any]) -> None:
        producer = {key: admission.get(key) for key in _PRODUCER_FIELDS}
        target = admission.get("admitted_target")
        if (any(not _text(producer[key]) for key in _PRODUCER_FIELDS[:3])
                or any(not _positive_int(producer[key]) for key in _PRODUCER_FIELDS[3:])
                or not isinstance(target, Mapping) or set(target) != set(_TARGET_FIELDS)
                or any(not _text(target[key]) for key in _TARGET_FIELDS)
                or request.invocation != "runtime" or request.run_id != producer["task_id"]
                or request.project != target["project_id"]
                or request.out in (None, "") or request.run_root in (None, "")):
            raise ValueError("managed Python producer invocation context is missing or inconsistent")
        root, out = Path(request.run_root), Path(request.out)
        if (not root.is_absolute() or not out.is_absolute() or root.is_symlink() or out.is_symlink()
                or out.resolve() != root.resolve() / "outputs" or not out.is_dir()):
            raise ValueError("managed Python producer output root does not match its attempt")
        self._producer = MappingProxyType(producer)
        self._target = MappingProxyType(dict(target))
        self._out = out.resolve()
        self._directory = self._out.stat()
        self._owner = (os.getpid(), threading.get_ident())
        self._active = True

    def _check(self) -> None:
        if (not self._active or _current.get() is not self
                or self._owner != (os.getpid(), threading.get_ident())):
            raise ValueError("trusted Python action context is outside its invocation lifetime")
        observed = self._out.stat()
        if (self._out.is_symlink() or (observed.st_dev, observed.st_ino)
                != (self._directory.st_dev, self._directory.st_ino)):
            raise ValueError("trusted Python action output directory changed")

    @property
    def producer(self) -> Mapping[str, Any]:
        self._check()
        return self._producer

    @property
    def admitted_target(self) -> Mapping[str, str]:
        self._check()
        return self._target

    @property
    def out(self) -> Path:
        self._check()
        return self._out


def _require_action_context() -> _ActionContext:
    context = _current.get()
    if context is None:
        raise ValueError("trusted Python action context requires a managed host invocation")
    context._check()
    return context


@contextmanager
def _action_context_scope(request, admission: Mapping[str, Any]):
    # Ordinary Python actions retain their existing invocation and result ABI.
    # Missing producer context remains a refusal if an action asks for it.
    if _current.get() is not None:
        raise ValueError("trusted Python action context cannot be nested or reused")
    context = _ActionContext(request, admission) if "admitted_target" in admission else None
    token = _current.set(context)
    try:
        yield
    finally:
        if context is not None:
            context._active = False
        _current.reset(token)


class _PreparationClient:
    """Ephemeral adapter for the shared helper's existing context read seam.

    Never set identity on AstridClient: the underlying client may carry caller
    attributes. Reads use its existing facilities; publication stays forbidden.
    """

    def __init__(self, client, context: _ActionContext) -> None:
        self._client, self._context = client, context

    @property
    def trusted_execution_context(self) -> Mapping[str, Any]:
        return self._context.producer

    def open_authoring_target(self, *args, **kwargs):
        self._context._check()
        return _PreparationTarget(self._client.open_authoring_target(*args, **kwargs), self._context)

    def __getattr__(self, name):
        self._context._check()
        return getattr(self._client, name)


class _PreparationTarget:
    def __init__(self, target, context: _ActionContext) -> None:
        self._target, self._context = target, context

    def publish(self, *args, **kwargs):
        raise ValueError("managed producer preparation cannot publish; requester submission is required")

    def __getattr__(self, name):
        self._context._check()
        return getattr(self._target, name)


@contextmanager
def _managed_read_client(context: _ActionContext):
    """Open the host's existing worker read connection without launcher startup.

    The generic host already supplies this endpoint and bearer to ordinary
    Python actions.  Negotiate only the worker's existing execution/read
    scopes, then bind the authenticated actor to the admitted executor.  This
    keeps the action on the normal SDK read surface while avoiding the
    user-client launcher handshake, which also requests write scopes.
    """
    context._check()
    from astrid.sdk import AstridClient
    from astrid.sdk.remote import RemoteAstridClient
    from astrid.sdk.workspace_client import WorkspaceClient

    endpoint = os.environ.get("ASTRID_RUNTIME_ENDPOINT", "").strip()
    credential = os.environ.get("ASTRID_RUNTIME_CREDENTIAL", "").strip()
    if not endpoint or not credential:
        raise ValueError("managed Python producer requires the host runtime read connection")
    transport = WorkspaceClient(endpoint, credential)
    requested_scopes = ["worker:execute", "projects:read", "tasks:read", "objects:read"]
    handshake = transport.handshake("astrid-managed-python", "stage1", requested_scopes)
    if isinstance(handshake, Mapping):
        actor_id, scopes = handshake.get("actor_id"), handshake.get("scopes")
    else:
        actor_id, scopes = getattr(handshake, "actor_id", None), getattr(handshake, "scopes", None)
    if (actor_id != context.producer["executor_id"]
            or tuple(scopes or ()) != tuple(requested_scopes)):
        raise ValueError("managed Python producer read connection identity or scopes changed")
    transport.actor_id = actor_id
    yield AstridClient(remote=RemoteAstridClient(transport))
