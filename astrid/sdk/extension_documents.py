"""Narrow extension document facade over Documents and its authenticated client.

This is a trusted local host binding, not a Python sandbox. No credentials,
project selection, schema, source roots or grants come from extension input.
"""

from __future__ import annotations

import copy
import hashlib
import importlib
from collections.abc import Mapping
from types import MappingProxyType, ModuleType
from typing import Any

import jsonschema

from astrid.core.pack.document_access import (
    MEDIA_TRANSCRIPT_KIND,
    document_kinds,
)
from astrid.core.pack.document_access import check_document_source as check_source

from .contracts import DomainResult
from .documents import _failure, _timeline_document


def _shared_transcript_helpers() -> ModuleType | None:
    try:
        return importlib.import_module("astrid.sdk.managed_transcript")
    except ModuleNotFoundError as exc:
        if exc.name != "astrid.sdk.managed_transcript":
            raise
        return None


def _exact_strings(value: Any, keys: set[str], label: str) -> dict[str, str]:
    if not isinstance(value, Mapping) or set(value) != keys:
        raise ValueError(f"{label} must contain exactly {', '.join(sorted(keys))}")
    selected = dict(value)
    if any(not isinstance(item, str) or not item or item != item.strip() for item in selected.values()):
        raise ValueError(f"{label} identities must be exact nonempty strings")
    return selected


def _content_digest(helpers: ModuleType, record: Mapping[str, Any], media_duration_s):
    canonical_json = helpers.canonical_transcript_json(
        record, media_duration_s=media_duration_s
    )
    if not isinstance(canonical_json, str):
        raise ValueError("shared transcript canonical JSON must return a string")
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


class DeclaredDocuments:
    def __init__(self, documents, entry, *, project, subject, source):
        check_source(entry)
        self._documents, self._entry = documents, entry
        self._project = project
        self._kinds = document_kinds(entry.definition, entry.resources)
        if not isinstance(project, str) or not project or project != project.strip():
            raise ValueError("an exact canonical project is required")
        if isinstance(subject, Mapping) or isinstance(source, Mapping):
            if not isinstance(subject, Mapping) or not isinstance(source, Mapping):
                raise ValueError("transcript subject and source must both be identity mappings")
            self._subject = _exact_strings(
                subject, {"media_object_id", "media_sha256"}, "transcript subject"
            )
            source_keys = {
                "producer_id",
                "source_id",
                "lineage_id",
                "revision_id",
                "producer_digest",
            }
            if isinstance(source, Mapping) and "parent_revision_id" in source:
                source_keys.add("parent_revision_id")
            self._source = _exact_strings(source, source_keys, "transcript source")
            self._subject = MappingProxyType(self._subject)
            self._source = MappingProxyType(self._source)
            self._transcript_scope = True
        else:
            if any(
                not isinstance(v, str) or not v.strip() or v != v.strip()
                for v in (subject, source)
            ):
                raise ValueError("exact project, subject and source are required")
            self._subject, self._source = subject, source
            self._transcript_scope = False

    def _select(self, operation, kind, subject, source, *, transcript=False):
        check_source(self._entry)
        if not isinstance(kind, str):
            raise ValueError("an exact declared document kind is required")
        if kind == MEDIA_TRANSCRIPT_KIND and not transcript:
            raise ValueError("media.transcript/v1 must use the transcript selector")
        if operation == "write" and _timeline_document(kind):
            raise ValueError("timeline documents require validated EditCommands")
        if (subject, source) != (self._subject, self._source):
            raise ValueError("request subject/source differs from host-selected scope")
        declaration = self._kinds.get(kind)
        if declaration is None or operation not in declaration.access:
            raise ValueError("document operation is undeclared")
        if operation == "write":
            ns = self._entry.definition.extensions.get("data_namespace")
            if ns is None or ns["version"] != 1:
                raise ValueError("unsupported owner namespace version; owner writes unavailable")
        return declaration

    def _row(self, declaration, row, subject, source):
        if (
            not isinstance(row, Mapping)
            or row.get("project_id") != self._project
            or row.get("kind") != declaration.kind
            or row.get("document_id") != declaration.document_id(self._project, subject, source)
        ):
            raise ValueError("Runtime document identity differs from requested scope")
        if type(row.get("version")) is not int or row["version"] < 1:
            raise ValueError("invalid Runtime document version")
        declaration.validate(row.get("content"), subject, source)
        return row

    def read(self, kind, subject, source):
        try:
            declaration = self._select("read", kind, subject, source)
            result = self._documents._typed(
                "get_document",
                self._project,
                declaration.document_id(self._project, subject, source),
            )
            if not result.ok:
                return result
            self._row(declaration, result.data, subject, source)
            return result
        except (ValueError, TypeError, OSError, jsonschema.ValidationError) as exc:
            return _failure("document_refused", str(exc))

    def list(self, kind, subject, source):
        """Complete bounded kind pagination, then client-side subject/source filter."""
        try:
            declaration = self._select("list", kind, subject, source)
            result = self._documents._list_project(self._project, kind=kind)
            if not result.ok:
                return result
            selected = []
            for row in result.data:
                if (
                    not isinstance(row, Mapping)
                    or row.get("kind") != kind
                    or row.get("project_id") != self._project
                    or not isinstance(row.get("content"), dict)
                ):
                    raise ValueError("malformed Runtime document list row")
                content = row["content"]
                # No substring, display-name or latest-source selection.
                if (content.get("subject"), content.get("source")) == (subject, source):
                    selected.append(self._row(declaration, row, subject, source))
            if len(selected) > 1:
                raise ValueError("duplicate deterministic document identity")
            return DomainResult.success(selected)
        except (ValueError, TypeError, OSError, jsonschema.ValidationError) as exc:
            return _failure("document_refused", str(exc))

    def write(self, kind, subject, source, *, content, expected_version, idempotency_key):
        """expected_version=0 creates; positive versions CAS-update. No pre-CAS replay check."""
        try:
            if kind == MEDIA_TRANSCRIPT_KIND:
                raise ValueError("media.transcript/v1 is a read-only source")
            declaration = self._select("write", kind, subject, source)
            declaration.validate(content, subject, source)
            if type(expected_version) is not int or expected_version < 0:
                raise ValueError("an explicit nonnegative expected_version is required")
            if not isinstance(idempotency_key, str) or not idempotency_key.strip():
                raise ValueError("an explicit idempotency key is required")
            doc_id = declaration.document_id(self._project, subject, source)
            if expected_version == 0:
                result = self._documents._typed(
                    "create_document",
                    self._project,
                    doc_id,
                    kind,
                    key=idempotency_key,
                    content=content,
                    idempotency_key=idempotency_key,
                )
            else:
                result = self._documents._typed(
                    "update_document",
                    self._project,
                    doc_id,
                    key=idempotency_key,
                    content=content,
                    expected_version=expected_version,
                    idempotency_key=idempotency_key,
                )
            if result.ok:
                self._row(declaration, result.data, subject, source)
            return result
        except (ValueError, TypeError, OSError, jsonschema.ValidationError) as exc:
            return _failure("document_refused", str(exc))

    def select_transcript(
        self,
        *,
        media_duration_s: float | None = None,
        authenticated_source_pin: Mapping[str, Any] | None = None,
        pinned_record: Mapping[str, Any] | None = None,
    ):
        """Select one exact transcript or validate an already-resolved immutable pin.

        The pin path deliberately performs no Runtime document read/list: the
        caller supplies the record resolved from that immutable snapshot.
        """
        try:
            if not self._transcript_scope:
                raise ValueError("transcript selection requires host-bound media/source identities")
            declaration = self._select(
                "read", MEDIA_TRANSCRIPT_KIND, self._subject, self._source, transcript=True
            )
            self._select(
                "list", MEDIA_TRANSCRIPT_KIND, self._subject, self._source, transcript=True
            )
            if "write" in declaration.access or set(declaration.access) != {"read", "list"}:
                raise ValueError("media.transcript/v1 declaration must be read/list-only")
            helpers = _shared_transcript_helpers()
            if helpers is None:
                raise ValueError(
                    "D's astrid.sdk.managed_transcript helper is not joined"
                )
            if helpers.TRANSCRIPT_DOCUMENT_KIND != MEDIA_TRANSCRIPT_KIND:
                raise ValueError("shared transcript helper kind differs from the admitted kind")
            if (
                helpers.TRANSCRIPT_SCHEMA_ID != helpers.TRANSCRIPT_DOCUMENT_KIND
                or helpers.TRANSCRIPT_RECORD_SCHEMA.get("$id") != helpers.TRANSCRIPT_SCHEMA_ID
            ):
                raise ValueError("shared transcript helper schema ID differs from the admitted wire ID")
            expected_id = helpers.transcript_document_id(
                self._project, self._subject, self._source
            )
            if not isinstance(expected_id, str) or not expected_id:
                raise ValueError("shared transcript helper returned no deterministic document ID")
            if authenticated_source_pin is not None:
                if pinned_record is None:
                    raise ValueError(
                        "a pinned transcript requires its already-resolved immutable snapshot record"
                    )
                return DomainResult.success(
                    self._transcript_selection(
                        pinned_record,
                        expected_id,
                        None,
                        helpers,
                        media_duration_s,
                        authenticated_source_pin,
                    )
                )
            if pinned_record is not None:
                raise ValueError("a snapshot record requires its authenticated source pin")
            listed = self._documents._list_project(self._project, kind=MEDIA_TRANSCRIPT_KIND)
            if not listed.ok:
                return listed
            matches = []
            for row in listed.data:
                if (
                    not isinstance(row, Mapping)
                    or row.get("kind") != MEDIA_TRANSCRIPT_KIND
                    or row.get("project_id") != self._project
                    or not isinstance(row.get("content"), Mapping)
                ):
                    raise ValueError("malformed transcript document list row")
                record = row["content"]
                if record.get("subject") == self._subject and record.get("source") == self._source:
                    matches.append(
                        self._transcript_selection(
                            record,
                            expected_id,
                            row,
                            helpers,
                            media_duration_s,
                            None,
                        )
                    )
            if len(matches) > 1:
                raise ValueError("duplicate exact transcript document matches")
            if not matches:
                return _failure("not_found", "No document exists for the exact transcript source.")
            return DomainResult.success(matches[0])
        except (ValueError, TypeError, KeyError, OSError, jsonschema.ValidationError) as exc:
            return _failure("document_refused", str(exc))

    def _transcript_selection(
        self,
        record,
        expected_id,
        row,
        helpers,
        media_duration_s,
        authenticated_source_pin,
    ):
        if not isinstance(record, Mapping):
            raise ValueError("transcript document content must be one flat record")
        if record.get("subject") != self._subject or record.get("source") != self._source:
            raise ValueError("transcript subject/source differs from host-selected identity")
        validated_record = helpers.validate_transcript_record(
            record, media_duration_s=media_duration_s
        )
        if not isinstance(validated_record, Mapping):
            raise ValueError("shared transcript validator must return a record mapping")
        content_digest = _content_digest(helpers, validated_record, media_duration_s)
        if row is not None:
            if (
                row.get("project_id") != self._project
                or row.get("kind") != MEDIA_TRANSCRIPT_KIND
                or row.get("document_id") != expected_id
            ):
                raise ValueError("transcript Runtime identity differs from the deterministic source")
            version = row.get("version")
            if type(version) is not int or version < 1:
                raise ValueError("transcript Runtime document version must be positive")
        else:
            version = None
        pin = None
        if authenticated_source_pin is not None:
            pin = copy.deepcopy(dict(authenticated_source_pin))
            document = pin.get("document")
            snapshot = pin.get("snapshot")
            if not isinstance(document, Mapping) or not isinstance(snapshot, Mapping):
                raise ValueError("authenticated source pin needs document and snapshot identities")
            document_digest = document.get("content_digest")
            if (
                document.get("id") != expected_id
                or type(document.get("version")) is not int
                or document["version"] < 1
                or not isinstance(document_digest, str)
                or document_digest.removeprefix("sha256:") != content_digest
                or snapshot.get("sha256") != content_digest
                or not isinstance(snapshot.get("object_id"), str)
                or not snapshot["object_id"].strip()
                or snapshot["object_id"] != snapshot["object_id"].strip()
            ):
                raise ValueError("pinned document/content/snapshot identity differs from transcript bytes")
            if pin.get("subject") != self._subject or pin.get("source") != self._source:
                raise ValueError("pinned transcript subject/source differs from host selection")
            version = document["version"]
        record_copy = copy.deepcopy(dict(validated_record))
        return {
            "record": record_copy,
            "document": {
                "id": expected_id,
                "version": version,
                "content_digest": (
                    pin["document"]["content_digest"] if pin is not None else content_digest
                ),
            },
            "subject": copy.deepcopy(dict(self._subject)),
            "source": copy.deepcopy(dict(self._source)),
            "snapshot_pin": pin,
        }
