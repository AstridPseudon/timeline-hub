"""Source-bound V3 document declarations. Metadata never supplies Runtime grants.

subject-source-v1 is an opt-in identity for pack-owned records only. It is not
an asserted ID/schema rule for an unadmitted upstream transcript producer.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import uuid
from dataclasses import dataclass
from typing import Mapping

import jsonschema
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012


def stable_document_id(project_id: str, kind: str, name: str = "default") -> str:
    """Compatibility identity for existing one-per-project documents."""
    if any(not isinstance(v, str) or not v.strip() for v in (project_id, kind, name)):
        raise ValueError("project_id, kind and name must be nonempty strings")
    return "document:" + str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps([project_id, kind, name])))


def plain(value):
    if isinstance(value, Mapping):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def canonical(value):
    return json.dumps(
        plain(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )


def timeline_document(value) -> bool:
    """Kinds/IDs reserved for the command-only timeline path."""
    return isinstance(value, str) and (
        value.lower() in {"timeline", "edit-timeline", "edit_timeline"}
        or value.lower().startswith(("timeline:", "timeline/", "edit-timeline:", "edit-timeline/"))
    )


def owner_namespace(pack_id: str) -> str:
    # Manifest identity is selected by trusted source admission, never a request
    # argument or a display label. Prefixing prevents claiming app.transcript.
    if not isinstance(pack_id, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", pack_id):
        raise ValueError("invalid admitted pack identity")
    if pack_id == "astrid":
        raise ValueError("astrid is a reserved namespace owner")
    return "pack_" + pack_id


def validate_schema(schema, schema_id, version):
    schema = plain(schema)
    if not isinstance(schema, dict) or schema.get("$id") != f"{schema_id}/v{version}":
        raise ValueError("schema $id must bind the exact schema identity/version")
    if (
        schema.get("$schema", "https://json-schema.org/draft/2020-12/schema")
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        raise ValueError("only JSON Schema draft 2020-12 is supported")

    references = []

    def refs(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in {"$ref", "$dynamicRef"} and (
                    not isinstance(value, str) or not value.startswith("#")
                ):
                    raise ValueError("document schemas support only local references")
                if key in {"$ref", "$dynamicRef"}:
                    references.append(value)
                refs(value)
        elif isinstance(node, list):
            for value in node:
                refs(value)

    refs(schema)
    jsonschema.Draft202012Validator.check_schema(schema)
    resource = Resource.from_contents(schema, default_specification=DRAFT202012)
    resolver = Registry().with_resource(schema["$id"], resource).resolver(schema["$id"])
    for reference in references:
        try:
            resolver.lookup(reference)
        except Unresolvable as exc:
            raise ValueError("document schema has an unresolved local reference") from exc
    canonical(schema)
    return schema


@dataclass(frozen=True)
class DocumentKind:
    kind: str
    schema_id: str
    schema_version: int
    access: tuple[str, ...]
    schema_json: str

    def document_id(self, project, subject, source):
        for value in (project, subject, source):
            if not isinstance(value, str) or not value.strip() or value != value.strip():
                raise ValueError("project, subject and source must be exact nonempty identities")
        return stable_document_id(project, self.kind, canonical([subject, source]))

    def envelope(self, subject, source, data):
        value = dict(
            kind=self.kind,
            schema_id=self.schema_id,
            schema_version=self.schema_version,
            subject=subject,
            source=source,
            data=copy.deepcopy(data),
        )
        self.validate(value, subject, source)
        return value

    def validate(self, content, subject, source):
        if not isinstance(content, dict) or set(content) != {
            "kind",
            "schema_id",
            "schema_version",
            "subject",
            "source",
            "data",
        }:
            raise ValueError("invalid typed document envelope")
        if (
            content["kind"],
            content["schema_id"],
            content["schema_version"],
            content["subject"],
            content["source"],
        ) != (self.kind, self.schema_id, self.schema_version, subject, source) or type(
            content["schema_version"]
        ) is not int:
            raise ValueError("document kind/schema/subject/source binding differs")
        canonical(content)
        jsonschema.Draft202012Validator(json.loads(self.schema_json)).validate(content["data"])


def document_kinds(definition, resources, *, resolve_schemas=True):
    handles = {h.path: h for h in resources}
    result = {}
    seen = set()
    for declaration in definition.documents.values():
        runtime = declaration.get("runtime")
        if runtime is None:
            continue  # Existing authored document formats grant no facade access.
        kind = runtime["kind"]
        if not kind.startswith(definition.id + ".") or not runtime["schema_id"].startswith(
            definition.id + "."
        ):
            raise ValueError("document kind/schema must belong to the admitted pack identity")
        if kind in seen:
            raise ValueError("duplicate Runtime document kind")
        seen.add(kind)
        schema = declaration["schema"]
        if isinstance(schema, str):
            if not resolve_schemas:
                continue
            handle = handles.get(schema)
            if handle is None or handle.file_kind != "file":
                raise ValueError("document schema must be an admitted file resource")
            raw = handle.resolved.read_bytes()
            if hashlib.sha256(raw).hexdigest() != handle.sha256:
                raise ValueError("admitted document schema changed")
            schema = json.loads(raw)
        schema = validate_schema(schema, runtime["schema_id"], runtime["schema_version"])
        result[kind] = DocumentKind(
            kind,
            runtime["schema_id"],
            runtime["schema_version"],
            tuple(sorted(runtime["access"])),
            canonical(schema),
        )
    return result


def validate_document_declarations(definition, resources, *, resolve_schemas=True):
    try:
        document_kinds(definition, resources, resolve_schemas=resolve_schemas)
        ns = definition.extensions.get("data_namespace")
        if ns is not None:
            if ns["owner"] != owner_namespace(definition.id) or not ns["schema_id"].startswith(
                definition.id + "."
            ):
                raise ValueError("namespace owner/schema differs from admitted manifest identity")
            schema = validate_schema(ns["schema"], ns["schema_id"], ns["version"])
            if (
                schema.get("type") != "object"
                or schema.get("properties", {}).get("v") != {"const": ns["version"]}
                or "v" not in schema.get("required", [])
            ):
                raise ValueError("namespace schema must require its exact v")
            if "v" in ns["writable"] or any(
                k not in schema.get("properties", {}) for k in ns["writable"]
            ):
                raise ValueError("namespace writable keys must be declared properties excluding v")
    except (ValueError, jsonschema.SchemaError) as exc:
        from astrid.core.pack.canonical import CanonicalPackValidationError

        raise CanonicalPackValidationError(str(exc)) from exc


def document_source_digest(entry):
    """Bind selection to manifest and its complete admitted resource closure."""
    closure = {h.path: h.sha256 for h in (entry.manifest, *entry.resources)}
    return (
        "sha256:"
        + hashlib.sha256(
            canonical(
                {
                    "source_root": str(entry.root),
                    "manifest": entry.definition.to_dict(),
                    "closure": closure,
                }
            ).encode()
        ).hexdigest()
    )


def check_document_source(entry):
    """Refuse a stale selection before any document request or owner-data edit."""
    if entry.definition.schema_version != 3:
        raise ValueError("document facade requires an admitted V3 pack")
    for handle in (entry.manifest, *entry.resources):
        if handle.file_kind == "file" and (
            handle.resolved.is_symlink()
            or hashlib.sha256(handle.resolved.read_bytes()).hexdigest() != handle.sha256
        ):
            raise ValueError("admitted document facade source changed; rediscover the pack")
