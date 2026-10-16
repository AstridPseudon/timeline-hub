"""Synthetic/nonproduction SDK/host boundary fixtures; no Runtime store or server."""

from __future__ import annotations

import copy
import json

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
