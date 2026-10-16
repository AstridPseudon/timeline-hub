"""Synthetic/nonproduction SDK/host boundary fixtures; no Runtime store or server."""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping

import pytest
import yaml

from astrid.core.execution.generic_host import GenericPackHost, HostError
from astrid.core.pack.canonical import CanonicalPackValidationError, validate_canonical_pack
from astrid.core.pack.data_namespace import OwnerData
from astrid.core.pack.document_access import document_kinds, document_source_digest
from astrid.sdk.documents import Documents, stable_document_id
from astrid.sdk.workspace_client import WorkspaceClientError


def manifest():
    return {
        "schema_version": 3,
        "id": "demo",
        "name": "Demo",
        "version": "1.0.0",
        "documents": {
            "analysis": {
                "format_version": 1,
                "schema": {
                    "$id": "demo.analysis/v1",
                    "type": "object",
                    "required": ["text"],
                    "properties": {"text": {"type": "string"}},
                    "additionalProperties": False,
                },
                "runtime": {
                    "kind": "demo.analysis",
                    "schema_id": "demo.analysis",
                    "schema_version": 1,
                    "identity": "subject-source-v1",
                    "access": ["read", "list", "write"],
                },
            }
        },
        "extensions": {
            "data_namespace": {
                "owner": "pack_demo",
                "schema_id": "demo.data",
                "version": 1,
                "writable": ["notes"],
                "schema": {
                    "$id": "demo.data/v1",
                    "type": "object",
                    "required": ["v"],
                    "properties": {"v": {"const": 1}, "notes": {}},
                    "additionalProperties": True,
                },
            }
        },
    }


def admit(tmp_path, payload=None):
    root = tmp_path / "demo"
    root.mkdir(exist_ok=True)
    (root / "pack.yaml").write_text(yaml.safe_dump(payload or manifest()))
    return validate_canonical_pack(root)


class SyntheticRuntime:
    """Explicit CRUD/CAS/grant model, not evidence of real Runtime acceptance."""

    def __init__(self):
        self.rows, self.replays, self.calls, self.mutations = {}, {}, [], []
        self.endpoint = "http://synthetic.invalid"
        self._last_handshake = {"realm_id": "synthetic-realm", "actor_id": "actor-a"}
        self.actor, self.allowed = "actor-a", {("actor-a", "project-a")}
        self.write_allowed = True

    def grant(self, project, *, write=False):
        if (self.actor, project) not in self.allowed or (write and not self.write_allowed):
            raise WorkspaceClientError(403, "forbidden", "project/actor grant denied", {})

    def get_project(self, project):
        self.grant(project)
        return {"project_id": project}

    def get_document(self, project, document):
        self.grant(project)
        self.calls.append(("get", document))
        if document not in self.rows:
            raise WorkspaceClientError(404, "not_found", "not found", {})
        return copy.deepcopy(self.rows[document])

    def list_documents(self, project, *, cursor, limit, kind=None):
        self.grant(project)
        self.calls.append(("list", cursor, kind))
        # Force real SDK pagination despite the default page size.
        rows = [r for r in self.rows.values() if r["kind"] == kind]
        offset = int(cursor or "0")
        return [
            copy.deepcopy(rows[offset : offset + 1]),
            str(offset + 1) if offset + 1 < len(rows) else None,
        ]

    def mutate(self, project, document, kind, content, expected, key, *, create):
        self.grant(project, write=True)
        body = [project, document, kind, content, expected, create]
        self.mutations.append(copy.deepcopy(body))
        if key in self.replays:
            previous, row = self.replays[key]
            if previous != body:
                raise WorkspaceClientError(409, "idempotency_conflict", "changed body/key", {})
            return {"data": copy.deepcopy(row), "receipt": None}
        current = self.rows.get(document)
        if (create and current is not None) or (
            not create and (current is None or current["version"] != expected)
        ):
            raise WorkspaceClientError(409, "version_conflict", "stale expected_version", {})
        row = dict(
            project_id=project,
            document_id=document,
            kind=kind,
            content=copy.deepcopy(content),
            version=expected + 1,
        )
        self.rows[document] = row
        self.replays[key] = copy.deepcopy([body, row])
        return {"data": copy.deepcopy(row), "receipt": None}

    def create_document(self, project, document, kind, content, *, idempotency_key):
        return self.mutate(project, document, kind, content, 0, idempotency_key, create=True)

    def update_document(self, project, document, *, content, expected_version, idempotency_key):
        return self.mutate(
            project,
            document,
            self.rows[document]["kind"],
            content,
            expected_version,
            idempotency_key,
            create=False,
        )


@pytest.fixture
def bound(tmp_path):
    entry = admit(tmp_path)
    runtime = SyntheticRuntime()
    docs = Documents(runtime)
    facade = docs.for_pack(entry, project="project-a", subject="media:one", source="producer:one")
    kind = document_kinds(entry.definition, entry.resources)["demo.analysis"]
    return entry, runtime, docs, facade, kind


def write(facade, kind, text="synthetic", *, version=0, key="create"):
    return facade.write(
        kind.kind,
        "media:one",
        "producer:one",
        content=kind.envelope("media:one", "producer:one", {"text": text}),
        expected_version=version,
        idempotency_key=key,
    )


def test_manifest_roundtrip_identity_and_shared_host_helper(bound):
    entry, runtime, docs, facade, kind = bound
    digest = document_source_digest(entry)
    assert entry.definition.normalized["documents"]["analysis"]["runtime"]["schema_version"] == 1
    with pytest.raises(TypeError):
        entry.definition.documents["analysis"]["runtime"]["kind"] = "other"
    (entry.root / "pack.yaml").write_text(yaml.safe_dump(entry.definition.to_dict()))
    refreshed = validate_canonical_pack(entry.root)
    assert refreshed.provenance.provenance_identity == entry.provenance.provenance_identity
    assert document_source_digest(refreshed) != digest  # exact source bytes differ
    host = GenericPackHost(pack_roots=[entry.root])
    selected = host.document_facade(
        entry.root,
        documents=docs,
        project="project-a",
        subject="media:one",
        source="producer:one",
        expected_source_digest=document_source_digest(refreshed),
    )
    assert write(selected, kind).ok
    assert selected.read(kind.kind, "media:one", "producer:one").data[
        "document_id"
    ] == kind.document_id("project-a", "media:one", "producer:one")
    with pytest.raises(HostError, match="digest"):
        host.document_facade(
            entry.root,
            documents=docs,
            project="project-a",
            subject="media:one",
            source="producer:one",
            expected_source_digest=digest,
        )
    with pytest.raises(HostError, match="outside"):
        host.document_facade(
            entry.root.parent / "foreign",
            documents=docs,
            project="project-a",
            subject="m",
            source="s",
            expected_source_digest=digest,
        )
    assert (
        stable_document_id("p", "demo.analysis") == "document:bce253c3-c0dd-58d5-81cb-6aadbf89e6dd"
    )


@pytest.mark.parametrize(
    "change",
    [
        lambda d: d["documents"]["analysis"]["runtime"].update(schema_version=True),
        lambda d: d["documents"]["analysis"]["runtime"].update(identity="future-v2"),
        lambda d: d["documents"]["analysis"]["runtime"].update(kind="transcript.source"),
        lambda d: d["documents"]["analysis"].update(schema="../escape.json"),
        lambda d: d["documents"]["analysis"]["schema"].update(
            {"$ref": "https://example.invalid/schema"}
        ),
        lambda d: d["documents"]["analysis"]["schema"].update({"$id": "demo.analysis/v2"}),
        lambda d: d["documents"]["analysis"]["schema"].update(type="future"),
        lambda d: d["extensions"]["data_namespace"].update(owner="astrid"),
        lambda d: d["extensions"]["data_namespace"].update(owner="pack_other"),
        lambda d: d["extensions"]["data_namespace"].update(version=False),
        lambda d: d["extensions"]["data_namespace"].update(writable=["v"]),
    ],
)
def test_malformed_declarations_fail_closed(tmp_path, change):
    d = manifest()
    change(d)
    with pytest.raises(CanonicalPackValidationError):
        admit(tmp_path, d)


def test_schema_file_digest_and_safe_symlink_admission(tmp_path):
    d = manifest()
    schema = d["documents"]["analysis"]["schema"]
    root = tmp_path / "demo"
    root.mkdir()
    (root / "schema.json").write_text(json.dumps(schema))
    d["documents"]["analysis"]["schema"] = "schema.json"
    entry = admit(tmp_path, d)
    assert document_kinds(entry.definition, entry.resources)
    (root / "schema.json").write_text("{}")
    with pytest.raises(ValueError, match="changed"):
        document_kinds(entry.definition, entry.resources)
    (root / "schema.json").unlink()
    (root / "schema.json").symlink_to(tmp_path / "outside.json")
    with pytest.raises(CanonicalPackValidationError):
        validate_canonical_pack(root)


def test_defaults_readonly_and_source_fence(tmp_path):
    d = manifest()
    del d["documents"]["analysis"]["runtime"]
    entry = admit(tmp_path, d)
    runtime = SyntheticRuntime()
    facade = Documents(runtime).for_pack(
        entry, project="project-a", subject="media:one", source="producer:one"
    )
    assert not facade.read("demo.analysis", "media:one", "producer:one").ok
    assert runtime.calls == []
    d = manifest()
    d["documents"]["analysis"]["runtime"]["access"] = ["read", "list"]
    entry = admit(tmp_path, d)
    facade = Documents(runtime).for_pack(
        entry, project="project-a", subject="media:one", source="producer:one"
    )
    kind = document_kinds(entry.definition, entry.resources)["demo.analysis"]
    assert not write(facade, kind).ok and runtime.mutations == []
    assert not facade.read(kind.kind, "other", "producer:one").ok
    assert not facade.list(kind.kind, "media:one", "other").ok
    (entry.root / "pack.yaml").write_text("# source changed")
    assert not facade.read(kind.kind, "media:one", "producer:one").ok
    assert not runtime.calls


def test_cas_idempotency_and_exact_binding(bound):
    _, runtime, _, facade, kind = bound
    first = write(facade, kind)
    assert first.ok
    assert write(facade, kind).data == first.data
    assert write(facade, kind, "changed").error.code == "idempotency_conflict"
    assert write(facade, kind, key="different-key").error.code == "version_conflict"
    second = write(facade, kind, "updated", version=1, key="update")
    assert second.ok
    assert write(facade, kind, "updated", version=1, key="update").data == second.data
    assert write(facade, kind, "stale", version=1, key="stale").error.code == "version_conflict"
    before = len(runtime.mutations)
    for field, value in [
        ("subject", "wrong"),
        ("source", "wrong"),
        ("kind", "demo.other"),
        ("schema_id", "demo.other"),
        ("schema_version", True),
        ("data", {"text": 42}),
    ]:
        content = kind.envelope("media:one", "producer:one", {"text": "x"})
        content[field] = value
        assert not facade.write(
            kind.kind,
            "media:one",
            "producer:one",
            content=content,
            expected_version=2,
            idempotency_key="bad",
        ).ok
    for version, key in [(True, "x"), (-1, "x"), (2, "")]:
        assert not write(facade, kind, version=version, key=key).ok
    assert len(runtime.mutations) == before
    row = next(iter(runtime.rows.values()))
    row["document_id"] = "wrong"
    assert not facade.read(kind.kind, "media:one", "producer:one").ok


def test_complete_pagination_and_runtime_actor_project_grants(bound):
    _, runtime, docs, facade, kind = bound
    for subject, source in [
        ("media:other", "producer:one"),
        ("media:one", "producer:other"),
        ("media:one", "producer:one"),
    ]:
        scoped = docs.for_pack(facade._entry, project="project-a", subject=subject, source=source)
        assert scoped.write(
            kind.kind,
            subject,
            source,
            content=kind.envelope(subject, source, {"text": "fixture"}),
            expected_version=0,
            idempotency_key=subject + source,
        ).ok
    result = facade.list(kind.kind, "media:one", "producer:one")
    assert result.ok and len(result.data) == 1
    assert [c[1] for c in runtime.calls if c[0] == "list"] == [None, "1", "2"]
    runtime.actor = "actor-b"
    for result in [
        facade.read(kind.kind, "media:one", "producer:one"),
        facade.list(kind.kind, "media:one", "producer:one"),
        write(facade, kind),
    ]:
        assert result.error.code == "forbidden"
    runtime.actor = "actor-a"
    runtime.write_allowed = False
    assert facade.read(kind.kind, "media:one", "producer:one").ok
    assert write(facade, kind, version=1, key="denied").error.code == "forbidden"
    assert (
        not docs.for_pack(
            facade._entry, project="project-b", subject="media:one", source="producer:one"
        )
        .list(kind.kind, "media:one", "producer:one")
        .ok
    )


@pytest.mark.parametrize(
    "kind", ["timeline", "timeline:film", "edit-timeline", "edit-timeline/film"]
)
def test_timeline_refusal_including_legacy_update_and_checkin(bound, tmp_path, kind):
    _, runtime, docs, facade, _ = bound
    assert not facade.write(
        kind, "media:one", "producer:one", content={}, expected_version=1, idempotency_key="no"
    ).ok
    assert not docs.create(kind=kind, content={}, project="project-a").ok
    runtime.rows["opaque-id"] = dict(
        project_id="project-a", document_id="opaque-id", kind=kind, content={}, version=1
    )
    assert (
        docs.update("opaque-id", content={}, expected_version=1, project="project-a").error.code
        == "command_required"
    )
    path = tmp_path / "checkout.json"
    assert docs.checkout("opaque-id", file=path, project="project-a").ok
    path.write_text('{"changed":true}')
    assert docs.checkin(path).error.code == "command_required"
    assert runtime.mutations == []


def test_namespace_preservation_clear_and_wrong_owner(bound):
    entry, _, _, _, _ = bound
    codec = OwnerData(entry)
    assert codec.clear({}, codec.owner, "notes") == {}
    from astrid.core.pack.loader import load_pack_manifest
    projected = load_pack_manifest(entry.manifest.resolved).to_dict()
    assert projected["extensions"]["data_namespace"]["owner"] == codec.owner
    carrier = {
        "app": {
            "astrid": {"v": 2, "_intent": [None]},
            "foreign": "{bad json",
            "transcript": False,
            "pack_demo": {"v": 1, "notes": None, "_opaque": {"bad": True}, "future": [1, 2]},
        }
    }
    original = copy.deepcopy(carrier)
    opaque = json.dumps(
        {k: v for k, v in carrier["app"].items() if k != codec.owner}, separators=(",", ":")
    )
    read = codec.read(carrier)
    with pytest.raises(TypeError):
        read["v"] = 2
    updated = codec.set(carrier, codec.owner, "notes", {"op": "clear"})
    assert updated["app"][codec.owner]["notes"] == {"op": "clear"}
    cleared = codec.clear(updated, codec.owner, "notes")
    assert "notes" not in cleared["app"][codec.owner]
    assert cleared["app"][codec.owner]["_opaque"] == original["app"][codec.owner]["_opaque"]
    assert (
        json.dumps(
            {k: v for k, v in cleared["app"].items() if k != codec.owner}, separators=(",", ":")
        )
        == opaque
    )
    assert carrier == original
    for owner, key in [
        ("astrid", "notes"),
        ("transcript", "notes"),
        (codec.owner, "v"),
        (codec.owner, "undeclared"),
    ]:
        with pytest.raises(ValueError):
            codec.set(carrier, owner, key, "x")
    for value in [None, [], {"v": True}, {"v": 2}, {"v": "1"}, {}]:
        malformed = {"app": {codec.owner: value, "foreign": {"_x": 1}}}
        before = copy.deepcopy(malformed)
        with pytest.raises(ValueError):
            codec.clear(malformed, codec.owner, "notes")
        assert malformed == before


def test_future_owner_version_disables_writes_without_hiding_reads(tmp_path):
    d = manifest()
    ns = d["extensions"]["data_namespace"]
    ns.update(version=2)
    ns["schema"]["$id"] = "demo.data/v2"
    ns["schema"]["properties"]["v"]["const"] = 2
    entry = admit(tmp_path, d)
    runtime = SyntheticRuntime()
    docs = Documents(runtime)
    kind = document_kinds(entry.definition, entry.resources)["demo.analysis"]
    content = kind.envelope("media:one", "producer:one", {"text": "synthetic fixture"})
    runtime.rows[kind.document_id("project-a", "media:one", "producer:one")] = dict(
        project_id="project-a",
        document_id=kind.document_id("project-a", "media:one", "producer:one"),
        kind=kind.kind,
        version=1,
        content=content,
    )
    facade = docs.for_pack(entry, project="project-a", subject="media:one", source="producer:one")
    assert facade.read(kind.kind, "media:one", "producer:one").ok
    assert not write(facade, kind).ok and runtime.mutations == []
    with pytest.raises(ValueError, match="unsupported"):
        OwnerData(entry).set({}, "pack_demo", "notes", "x")


def test_authenticated_client_legacy_document_mutation_refuses_timeline():
    from astrid.sdk.workspace_client import WorkspaceClient

    class Client(WorkspaceClient):
        def __init__(self):
            self.calls = []
            self.row_kind = "timeline"

        def _call_generated(self, operation, *args, **kwargs):
            self.calls.append(operation)
            return {"kind": self.row_kind}

    client = Client()
    for action in [
        lambda: client.update_document(
            "p", "opaque", content={}, expected_version=1, idempotency_key="key"
        ),
        lambda: client.update_document(
            "p", "opaque", kind="edit-timeline", expected_version=1, idempotency_key="key"
        ),
        lambda: client.create_document("p", "timeline:film", "other", {}, idempotency_key="key"),
        lambda: client.create_document("p", "opaque", "timeline", {}, idempotency_key="key"),
    ]:
        with pytest.raises(WorkspaceClientError) as error:
            action()
        assert error.value.code == "command_required"
    assert "update_document" not in client.calls and "create_document" not in client.calls
    client.row_kind = "demo.analysis"
    client.update_document("p", "opaque", content={}, expected_version=2, idempotency_key="key")
    assert client.calls[-1] == "update_document"


def test_undeclared_namespace_disables_owner_write(tmp_path):
    d = manifest()
    del d["extensions"]["data_namespace"]
    entry = admit(tmp_path, d)
    runtime = SyntheticRuntime()
    facade = Documents(runtime).for_pack(
        entry, project="project-a", subject="media:one", source="producer:one"
    )
    kind = document_kinds(entry.definition, entry.resources)["demo.analysis"]
    assert not write(facade, kind).ok
    assert runtime.mutations == []
    with pytest.raises(ValueError, match="undeclared"):
        OwnerData(entry)


@pytest.mark.parametrize("mode", ["cyclic", "malformed", "late-denial"])
def test_list_refuses_incomplete_pagination(bound, mode):
    _, runtime, _, facade, kind = bound
    assert write(facade, kind).ok
    row = next(iter(runtime.rows.values()))

    def pages(project, *, cursor, limit, kind=None):
        if cursor is None:
            return [[copy.deepcopy(row)], "next"]
        if mode == "cyclic":
            return [[], "next"]
        if mode == "malformed":
            return {"unexpected": []}
        raise WorkspaceClientError(403, "forbidden", "grant revoked on later page", {})

    runtime.list_documents = pages
    result = facade.list(kind.kind, "media:one", "producer:one")
    assert not result.ok
    assert result.data is None


def test_reserved_manifest_owner_and_unresolved_schema(tmp_path):
    d = manifest()
    d["documents"]["analysis"]["schema"]["$ref"] = "#/$defs/absent"
    with pytest.raises(CanonicalPackValidationError, match="unresolved"):
        admit(tmp_path, d)
    d = manifest()
    d["id"] = "astrid"
    d["documents"] = {}
    d["extensions"]["data_namespace"].update(owner="pack_astrid", schema_id="astrid.data")
    d["extensions"]["data_namespace"]["schema"]["$id"] = "astrid.data/v1"
    root = tmp_path / "astrid"
    root.mkdir()
    (root / "pack.yaml").write_text(yaml.safe_dump(d))
    with pytest.raises(CanonicalPackValidationError, match="reserved"):
        validate_canonical_pack(root)


def test_facade_never_reresolves_host_project_scope(bound):
    _, runtime, _, facade, kind = bound
    runtime.get_project = lambda project: (_ for _ in ()).throw(
        AssertionError("facade must use exact host-selected canonical project")
    )
    assert write(facade, kind).ok
    assert facade.read(kind.kind, "media:one", "producer:one").ok
    assert facade.list(kind.kind, "media:one", "producer:one").ok


def test_metadata_only_admission_still_refuses_wrong_namespace_owner(tmp_path):
    from astrid.core.pack.canonical import read_normalize_validate
    d = manifest()
    entry = admit(tmp_path, d)
    d["extensions"]["data_namespace"]["owner"] = "pack_foreign"
    entry.manifest.resolved.write_text(yaml.safe_dump(d))
    with pytest.raises(CanonicalPackValidationError, match="owner"):
        read_normalize_validate(entry.manifest.resolved, source="local", resolve_resources=False)


TRANSCRIPT_KIND = "media.transcript/v1"
TRANSCRIPT_SUBJECT = {
    "media_object_id": "media-object-a",
    "media_sha256": "a" * 64,
}
TRANSCRIPT_SOURCE = {
    "producer_id": "caption-foundry",
    "source_id": "stream-a",
    "lineage_id": "lineage-a",
    "revision_id": "revision-a",
    "producer_digest": "b" * 64,
}


def transcript_manifest():
    result = manifest()
    result["documents"]["transcript"] = {
        "format_version": 1,
        "schema": {
            "$id": "media.transcript/v1",
            "type": "object",
            "required": ["schema_version", "subject", "source", "clock", "words", "segments"],
            "properties": {"schema_version": {"const": 1}},
            "additionalProperties": True,
        },
        "runtime": {
            "kind": TRANSCRIPT_KIND,
            "schema_id": "media.transcript",
            "schema_version": 1,
            "identity": "media-transcript-v1",
            "access": ["read", "list"],
        },
    }
    return result


def transcript_record(*, subject=None, source=None):
    return {
        "schema_version": 1,
        "subject": copy.deepcopy(subject if subject is not None else TRANSCRIPT_SUBJECT),
        "source": copy.deepcopy(source if source is not None else TRANSCRIPT_SOURCE),
        "clock": {"kind": "media", "unit": "seconds", "origin_seconds": 0},
        "words": [{"id": "word-a", "text": "hello", "start_s": 0.1, "end_s": 0.4}],
        "segments": [{"id": "segment-a", "word_ids": ["word-a"]}],
        "opaque_vendor_field": {"keep": ["in", "place"]},
    }


class InjectedTranscriptHelpers:
    MEDIA_TRANSCRIPT_KIND = TRANSCRIPT_KIND

    def __init__(self):
        self.calls = []

    def validate_transcript_source(self, record, *, media_duration_s=None):
        self.calls.append(("validate", media_duration_s))
        required = {"schema_version", "subject", "source", "clock", "words", "segments"}
        if (
            not isinstance(record, Mapping)
            or not required.issubset(record)
            or type(record.get("schema_version")) is not int
            or record["schema_version"] != 1
            or not isinstance(record.get("subject"), Mapping)
            or not isinstance(record.get("source"), Mapping)
            or not isinstance(record.get("clock"), Mapping)
            or not isinstance(record.get("words"), list)
            or not isinstance(record.get("segments"), list)
        ):
            raise ValueError("injected shared transcript validation refused malformed record")
        return copy.deepcopy(dict(record))

    def canonical_transcript_source_bytes(self, record, *, media_duration_s=None):
        self.calls.append(("canonical", media_duration_s))
        return json.dumps(
            record,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")

    def transcript_document_id(self, project_id, subject, source):
        self.calls.append(("id", project_id, dict(subject), dict(source)))
        return "document:transcript-fixture"


def transcript_row(record, *, document_id="document:transcript-fixture", version=3, project="project-a"):
    return {
        "project_id": project,
        "document_id": document_id,
        "kind": TRANSCRIPT_KIND,
        "version": version,
        "content": copy.deepcopy(record),
    }


def transcript_facade(tmp_path, runtime, *, subject=None, source=None):
    entry = admit(tmp_path, transcript_manifest())
    return Documents(runtime).for_pack(
        entry,
        project="project-a",
        subject=copy.deepcopy(subject if subject is not None else TRANSCRIPT_SUBJECT),
        source=copy.deepcopy(source if source is not None else TRANSCRIPT_SOURCE),
    )


def test_transcript_manifest_exact_shared_declaration_and_helper_selection(tmp_path):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    record = transcript_record()
    runtime.rows["row-a"] = transcript_row(record, version=4)
    facade = transcript_facade(tmp_path, runtime)

    result = facade.select_transcript(helpers=helpers, media_duration_s=2.0)

    assert result.ok
    assert result.data["record"] == record
    assert result.data["record"]["opaque_vendor_field"] == {"keep": ["in", "place"]}
    assert result.data["document"] == {
        "id": "document:transcript-fixture",
        "version": 4,
        "content_digest": hashlib.sha256(
            helpers.canonical_transcript_source_bytes(record, media_duration_s=2.0)
        ).hexdigest(),
    }
    assert result.data["subject"] == TRANSCRIPT_SUBJECT
    assert result.data["source"] == TRANSCRIPT_SOURCE
    assert [call[0] for call in helpers.calls] == ["id", "validate", "canonical", "canonical"]
    assert {call[0] for call in runtime.calls} == {"list"}
    assert runtime.mutations == []


@pytest.mark.parametrize(
    "change",
    [
        lambda declaration: declaration["runtime"].update(kind="demo.transcript"),
        lambda declaration: declaration["runtime"].update(schema_id="demo.transcript"),
        lambda declaration: declaration["runtime"].update(schema_version=2),
        lambda declaration: declaration["runtime"].update(identity="subject-source-v1"),
        lambda declaration: declaration["runtime"].update(access=["read", "list", "write"]),
        lambda declaration: declaration["runtime"].update(access=["read"]),
        lambda declaration: declaration["schema"].update({"$id": "media.transcript/v2"}),
    ],
)
def test_transcript_manifest_rejects_wrong_kind_schema_version_or_access(tmp_path, change):
    payload = transcript_manifest()
    change(payload["documents"]["transcript"])

    with pytest.raises(CanonicalPackValidationError):
        admit(tmp_path, payload)


def test_transcript_rejects_malformed_record_and_cross_subject_source(tmp_path):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    malformed = transcript_record()
    del malformed["words"]
    runtime.rows["malformed"] = transcript_row(malformed)
    facade = transcript_facade(tmp_path, runtime)
    assert not facade.select_transcript(helpers=helpers).ok

    runtime.rows.clear()
    for identity in (
        {"source": {**TRANSCRIPT_SOURCE, "source_id": "neighbor"}},
        {"subject": {**TRANSCRIPT_SUBJECT, "media_object_id": "neighbor-media"}},
    ):
        runtime.rows["other-source"] = transcript_row(transcript_record(**identity))
        result = facade.select_transcript(helpers=helpers)
        assert not result.ok and result.error.code == "not_found"
        runtime.rows.clear()
    assert runtime.mutations == []


def test_transcript_requires_exact_host_bound_source_identity(tmp_path):
    with pytest.raises(ValueError, match="exactly"):
        transcript_facade(
            tmp_path,
            SyntheticRuntime(),
            source={"producer_id": "caption-foundry"},
        )


def test_transcript_preserves_optional_correction_parent_identity(tmp_path):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    correction_source = {**TRANSCRIPT_SOURCE, "parent_revision_id": "revision-before"}
    record = transcript_record(source=correction_source)
    runtime.rows["correction"] = transcript_row(record)
    facade = transcript_facade(tmp_path, runtime, source=correction_source)

    result = facade.select_transcript(helpers=helpers)

    assert result.ok
    assert result.data["source"] == correction_source
    assert result.data["record"]["source"] == correction_source


def test_transcript_refuses_enveloped_content_instead_of_flat_record(tmp_path):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    record = transcript_record()
    envelope = {
        "kind": TRANSCRIPT_KIND,
        "schema_id": "media.transcript",
        "schema_version": 1,
        "subject": copy.deepcopy(TRANSCRIPT_SUBJECT),
        "source": copy.deepcopy(TRANSCRIPT_SOURCE),
        "data": record,
    }
    runtime.rows["envelope"] = transcript_row(envelope)
    facade = transcript_facade(tmp_path, runtime)

    result = facade.select_transcript(helpers=helpers)

    assert not result.ok and "malformed record" in result.error.message
    assert runtime.mutations == []


@pytest.mark.parametrize(
    "row_kwargs",
    [
        {"project": "project-b"},
        {"document_id": "document:wrong"},
    ],
)
def test_transcript_refuses_cross_project_and_wrong_computed_document_id(tmp_path, row_kwargs):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    runtime.rows["wrong"] = transcript_row(transcript_record(), **row_kwargs)
    facade = transcript_facade(tmp_path, runtime)

    result = facade.select_transcript(helpers=helpers)

    assert not result.ok
    assert "identity" in result.error.message or "malformed" in result.error.message
    assert runtime.mutations == []


@pytest.mark.parametrize("version", [0, True])
def test_transcript_requires_positive_integer_document_version(tmp_path, version):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    runtime.rows["wrong-version"] = transcript_row(transcript_record(), version=version)
    facade = transcript_facade(tmp_path, runtime)

    result = facade.select_transcript(helpers=helpers)

    assert not result.ok and "version" in result.error.message
    assert runtime.mutations == []


def test_transcript_refuses_duplicate_exact_matches_and_attempted_write(tmp_path):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    runtime.rows["row-a"] = transcript_row(transcript_record())
    runtime.rows["row-b"] = transcript_row(transcript_record())
    facade = transcript_facade(tmp_path, runtime)

    result = facade.select_transcript(helpers=helpers)
    assert not result.ok and "duplicate" in result.error.message
    write_result = facade.write(
        TRANSCRIPT_KIND,
        TRANSCRIPT_SUBJECT,
        TRANSCRIPT_SOURCE,
        content=transcript_record(),
        expected_version=4,
        idempotency_key="no-write",
    )
    assert not write_result.ok and "read-only" in write_result.error.message
    assert runtime.mutations == []
    assert all(call[0] == "list" for call in runtime.calls)


def test_transcript_pinned_snapshot_never_refetches_mutable_latest(tmp_path):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    old_record = transcript_record()
    latest_record = transcript_record()
    latest_record["words"][0]["text"] = "changed latest"
    runtime.rows["row-a"] = transcript_row(latest_record, version=9)
    facade = transcript_facade(tmp_path, runtime)
    content_digest = hashlib.sha256(
        helpers.canonical_transcript_source_bytes(old_record)
    ).hexdigest()
    pin = {
        "document": {
            "id": "document:transcript-fixture",
            "version": 3,
            "content_digest": "sha256:" + content_digest,
        },
        "snapshot": {"object_id": "cas:immutable-snapshot-a", "sha256": content_digest},
        "subject": copy.deepcopy(TRANSCRIPT_SUBJECT),
        "source": copy.deepcopy(TRANSCRIPT_SOURCE),
        "opaque_receipt_field": {"keep": True},
    }

    result = facade.select_transcript(
        helpers=helpers,
        authenticated_source_pin=pin,
        pinned_record=old_record,
    )

    assert result.ok
    assert result.data["record"] == old_record
    assert result.data["document"]["version"] == 3
    assert result.data["document"]["content_digest"] == "sha256:" + content_digest
    assert result.data["snapshot_pin"] == pin
    assert runtime.calls == []
    assert runtime.mutations == []

    missing_record = facade.select_transcript(
        helpers=helpers,
        authenticated_source_pin=pin,
    )
    assert not missing_record.ok and "immutable snapshot record" in missing_record.error.message
    assert runtime.calls == []


def test_transcript_pin_identity_mismatch_refuses_without_latest_fallback(tmp_path):
    runtime, helpers = SyntheticRuntime(), InjectedTranscriptHelpers()
    record = transcript_record()
    facade = transcript_facade(tmp_path, runtime)
    digest = hashlib.sha256(helpers.canonical_transcript_source_bytes(record)).hexdigest()
    pin = {
        "document": {"id": "document:wrong", "version": 3, "content_digest": digest},
        "snapshot": {"object_id": "cas:immutable-snapshot-a", "sha256": digest},
        "subject": copy.deepcopy(TRANSCRIPT_SUBJECT),
        "source": copy.deepcopy(TRANSCRIPT_SOURCE),
    }

    result = facade.select_transcript(
        helpers=helpers,
        authenticated_source_pin=pin,
        pinned_record=record,
    )

    assert not result.ok and "pinned document/content/snapshot" in result.error.message
    assert runtime.calls == []
    assert runtime.mutations == []
