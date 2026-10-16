"""Trusted, request-scoped transcript publication adapter.

This is a local Host boundary, not a sandbox for hostile Python reflection.
Only the selected built-in SDK publisher receives the context. Ordinary pack
functions and serialized user values never receive caller authority.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, fields
from types import SimpleNamespace
from typing import Callable

from astrid.core.pack.document_access import (
    MEDIA_TRANSCRIPT_KIND,
    TRANSCRIPT_PUBLISH_ACTION,
    check_document_source,
    select_transcript_writer,
)
from astrid.sdk.workspace_client import WorkspaceClient
from banodoco_workspace_client.generated import ByteResponse, MutationResult, ProjectDocument


def _identity(value):
    if type(value) is not str or not value or value != value.strip():
        raise ValueError("exact nonempty identity required")
    return value


class _Private:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise TypeError("document invocation objects are minted only by the Host")

    def __reduce_ex__(self, protocol):
        raise TypeError("document invocation authority cannot be serialized or copied")


@dataclass(frozen=True, slots=True, init=False, repr=False)
class _Documents(_Private):
    get_document: Callable[[str], ProjectDocument]
    create_document: Callable[..., MutationResult]
    update_document: Callable[..., MutationResult]


@dataclass(frozen=True, slots=True, init=False, repr=False)
class _Objects(_Private):
    ingest_project_object: Callable[..., MutationResult]
    get_object: Callable[[str], ByteResponse]


@dataclass(frozen=True, slots=True, init=False, repr=False)
class BoundDocumentInvocation(_Private):
    project_id: str
    document_id: str
    actor_id: str
    session_id: str
    realm_id: str
    action_id: str
    capability_id: str
    source_digest: str
    source_root: str
    resource_closure: tuple[tuple[str, str], ...]
    document_kind: str
    schema_id: str
    schema_version: int
    access: tuple[str, ...]
    producer_id: str
    request_id: str
    documents: _Documents
    objects: _Objects


def _mint(cls, **values):
    obj = object.__new__(cls)
    if set(values) != {f.name for f in fields(cls)}:
        raise TypeError("invalid private invocation fields")
    for key, value in values.items():
        object.__setattr__(obj, key, value)
    return obj


def _authenticated(client):
    # No duck-typed wrappers, worker transport, cached credential dictionaries,
    # or subclass with replacement authentication behavior is admitted.
    if type(client) is not WorkspaceClient:
        raise ValueError("an explicit authenticated WorkspaceClient is required")
    handshake = client._last_handshake
    if type(handshake) is not dict:
        raise ValueError("caller has no authenticated handshake")
    binding = tuple(_identity(handshake.get(k)) for k in ("actor_id", "session_id", "realm_id"))
    if client.actor_id != binding[0]:
        raise ValueError("caller actor differs from authenticated connection")
    from astrid.sdk.client import _validate_handshake
    from banodoco_workspace_client.contract_metadata import PROTOCOL, SCHEMA_DIGEST
    _validate_handshake(handshake, expected_protocol=PROTOCOL, expected_digest=SCHEMA_DIGEST,
                        expected_actor=binding[0], expected_realm=binding[2])
    return binding


def _invoke(entry, params, *, caller_connection, project_id, request_id, expected_source_digest):
    """Called only after Host root selection; returns D's original result object."""
    action, kind = select_transcript_writer(entry, expected_source_digest)
    actor, session, realm = _authenticated(caller_connection)
    project_id, request_id = _identity(project_id), _identity(request_id)
    project = caller_connection.get_project(project_id)
    if not isinstance(project, dict) or project.get("project_id") != project_id:
        raise ValueError("caller project differs from canonical selection")

    # Import only the trusted SDK implementation, never the declared Python
    # function and never function(**user_values). D's frozen DTO is data only.
    from astrid.sdk.transcript_publication import (
        PreparedTranscriptPublication,
        publish_transcript_source,
    )
    if type(params) is not PreparedTranscriptPublication:
        raise TypeError("an exact prepared publication request is required")
    if (params.project_id, params.request_id, params.admitted_action_id, params.producer_digest) != (
        project_id, request_id, TRANSCRIPT_PUBLISH_ACTION, expected_source_digest
    ):
        raise ValueError("prepared project/request/action/source differs")
    from astrid.sdk.managed_transcript import (
        canonical_transcript_json,
        transcript_document_id,
        validate_transcript_record,
    )
    record = validate_transcript_record(json.loads(params.canonical_record_json))
    if canonical_transcript_json(record) != params.canonical_record_json:
        raise ValueError("prepared transcript bytes are not canonical")
    if (record["source"]["producer_id"] != TRANSCRIPT_PUBLISH_ACTION
            or record["source"]["producer_digest"] != expected_source_digest):
        raise ValueError("transcript producer differs from selected writer")
    bound_document_id = transcript_document_id(project_id, record["subject"], record["source"])
    digest = hashlib.sha256(params.canonical_record_json.encode("utf-8")).hexdigest()
    if params.document_id != bound_document_id or params.content_digest != digest:
        raise ValueError("prepared document/content identity differs")
    if params.snapshot_object_id != "sha256:" + digest:
        raise ValueError("prepared snapshot identity differs")

    from astrid.core.execution.executor.actions import _json_safe, action_executor_definition
    from astrid.sdk.actions import (
        validate_action_inputs_definition,
        validate_action_output_definition,
    )
    definition = action_executor_definition(
        SimpleNamespace(id=entry.id, root=entry.root, version=entry.definition.version),
        "transcript_publish", action,
    )
    validate_action_inputs_definition(definition, _json_safe(params))
    active = True

    def check():
        if not active:
            raise ValueError("document invocation has expired")
        check_document_source(entry)
        if _authenticated(caller_connection) != (actor, session, realm):
            raise ValueError("authenticated caller binding changed")

    def document(selected):
        check()
        if selected != bound_document_id:
            raise ValueError("document is outside the selected transcript source")

    def content_check(content, selected_kind):
        if selected_kind != MEDIA_TRANSCRIPT_KIND:
            raise ValueError("document kind is outside the selected transcript source")
        if canonical_transcript_json(content) != params.canonical_record_json:
            raise ValueError("document content is outside the prepared source")

    def get_document(document_id: str) -> ProjectDocument:
        document(document_id)
        result = caller_connection.get_document(project_id, document_id, _preserve_dto=True)
        if not isinstance(result, ProjectDocument) or (
            result.project_id, result.document_id, result.kind
        ) != (project_id, bound_document_id, MEDIA_TRANSCRIPT_KIND):
            raise ValueError("Runtime document is outside the selected scope")
        old = validate_transcript_record(result.content)
        if old["subject"] != record["subject"] or any(
            old["source"][k] != record["source"][k]
            for k in ("producer_id", "source_id", "producer_digest")
        ):
            raise ValueError("Runtime document source differs")
        return result

    def mutation_key(idempotency_key, replay_only):
        _identity(idempotency_key)
        if type(replay_only) is not bool:
            raise ValueError("replay_only must be a boolean")

    def create_document(document_id, kind, content, *, idempotency_key, replay_only=False) -> MutationResult:
        document(document_id)
        content_check(content, kind)
        mutation_key(idempotency_key, replay_only)
        return caller_connection.create_document(
            project_id, document_id, kind, content, idempotency_key=idempotency_key,
            replay_only=replay_only, _preserve_dto=True,
        )

    def update_document(document_id, *, expected_version, idempotency_key, content,
                        kind=None, replay_only=False) -> MutationResult:
        document(document_id)
        content_check(content, MEDIA_TRANSCRIPT_KIND if kind is None else kind)
        mutation_key(idempotency_key, replay_only)
        if type(expected_version) is not int or expected_version < 1:
            raise ValueError("an exact positive document version is required")
        return caller_connection.update_document(
            project_id, document_id, expected_version=expected_version,
            idempotency_key=idempotency_key, content=content, kind=kind,
            replay_only=replay_only, _preserve_dto=True,
        )

    def ingest_project_object(data: bytes, *, media_type, idempotency_key, filename=None) -> MutationResult:
        check()
        _identity(idempotency_key)
        if type(data) is not bytes or data != params.canonical_record_json.encode("utf-8"):
            raise ValueError("object bytes differ from prepared transcript snapshot")
        return caller_connection.ingest_project_object(
            project_id, data, media_type=media_type, idempotency_key=idempotency_key,
            filename=filename, _preserve_dto=True,
        )

    def get_object(object_id: str) -> ByteResponse:
        check()
        if object_id != params.snapshot_object_id:
            raise ValueError("object is outside the selected snapshot")
        # get_object has no project parameter. Check existing project membership
        # through the same caller before fetching its globally addressed bytes.
        caller_connection.get_project_object_location(project_id, object_id)
        result = caller_connection.get_object(object_id, _preserve_dto=True)
        if not isinstance(result, ByteResponse) or hashlib.sha256(result.data).hexdigest() != digest:
            raise ValueError("Runtime snapshot bytes differ")
        return result

    invocation = _mint(
        BoundDocumentInvocation, project_id=project_id, document_id=bound_document_id, actor_id=actor,
        session_id=session, realm_id=realm, action_id=TRANSCRIPT_PUBLISH_ACTION,
        capability_id=definition.id, source_digest=expected_source_digest,
        source_root=str(entry.root),
        resource_closure=tuple(sorted((h.path, h.sha256) for h in (entry.manifest, *entry.resources))),
        document_kind=kind.kind, schema_id=kind.schema_id, schema_version=kind.schema_version,
        access=kind.access, producer_id=TRANSCRIPT_PUBLISH_ACTION, request_id=request_id,
        documents=_mint(_Documents, get_document=get_document, create_document=create_document,
                        update_document=update_document),
        objects=_mint(_Objects, ingest_project_object=ingest_project_object, get_object=get_object),
    )
    try:
        check()
        result = publish_transcript_source(invocation, params)
        validate_action_output_definition(definition, _json_safe(result))
        return result
    finally:
        active = False
