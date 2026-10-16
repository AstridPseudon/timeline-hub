"""Narrow extension document facade over Documents and its authenticated client.

This is a trusted local host binding, not a Python sandbox. No credentials,
project selection, schema, source roots or grants come from extension input.
"""

from __future__ import annotations

from collections.abc import Mapping

import jsonschema

from astrid.core.pack.document_access import check_document_source as check_source
from astrid.core.pack.document_access import document_kinds

from .contracts import DomainResult
from .documents import _failure, _timeline_document


class DeclaredDocuments:
    def __init__(self, documents, entry, *, project, subject, source):
        check_source(entry)
        self._documents, self._entry = documents, entry
        self._project, self._subject, self._source = project, subject, source
        self._kinds = document_kinds(entry.definition, entry.resources)
        # Even an empty declaration must not admit malformed request scope.
        if any(
            not isinstance(v, str) or not v.strip() or v != v.strip()
            for v in (project, subject, source)
        ):
            raise ValueError("exact project, subject and source are required")

    def _select(self, operation, kind, subject, source):
        check_source(self._entry)
        if not isinstance(kind, str):
            raise ValueError("an exact declared document kind is required")
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
