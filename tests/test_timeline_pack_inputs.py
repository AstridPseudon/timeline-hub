"""Exact project-pack Documents at the Runtime host boundary.

The admission inventory is retained here. Snapshot resource custody is a
separate missing prerequisite; these tests do not claim the inventory contains
an element declaration or substitute for Agent's selected-schema validation.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest
import test_timeline_commit_port as support
from test_timeline_commit_port import PreparedProvider, commit, prepared, request

from runtime_protocol.errors import NotFoundError, RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_inputs import (
    PROJECT_PACK_KIND,
    PROJECT_PACK_SCHEMA,
    capture_document_input,
)
from runtime_protocol.timeline_commit_port import digest

service = support.service


def pin(document):
    return {"document_id": document["document_id"], "version": document["version"],
            "content_digest": digest(document["content"])}


def create_pack(service, *, collection="default", **changes):
    project = service.test_project
    realm = service.realm["id"]
    owner = "project_" + hashlib.sha256(f"{realm}:{project}:default".encode()).hexdigest()[:20]
    if collection != "default":
        owner = collection
    content = {"schema": PROJECT_PACK_SCHEMA, "pack_id": owner, "source_binding_key": "project-packs",
               "relative_manifest": f"{realm}/{project}/packs/{owner}/pack.yaml",
               "admissions": [{"id": "reveal", "kind": "effect", "revision": "sha256:" + "1" * 64,
                               "snapshot_digest": "2" * 64}]}
    document_id = "document:" + str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps([project, PROJECT_PACK_KIND, collection])))
    body = {"document_id": document_id, "kind": PROJECT_PACK_KIND, "content": content}
    body.update(changes)
    return service.create_document(project, body, idempotency_key="pack-" + collection)["data"]


def install_source_provider(service, source_pin, *, before_accept=None, seen=None):
    def action(context, port):
        candidate = prepared(context, port)
        value = port.config_source(source_pin)
        if seen is not None:
            seen.append(value)
        candidate["canonical_document"]["dependency_manifest"]["documents"] = [source_pin]
        candidate["records"]["commands"][0]["dependencies"] = [
            {"key": "selected-pack", "kind": "source", "pin": source_pin, "policy": "exact"},
        ]
        candidate["document_digest"] = digest(candidate["canonical_document"])
        if before_accept:
            before_accept(value, candidate)
        return port.accept(candidate)
    provider = PreparedProvider(action)
    if hasattr(service, "test_provider"):
        service.test_provider.__dict__.update(provider.__dict__)
        provider = service.test_provider
    else:
        service.register_timeline_commit_provider(provider)
        service.test_provider = provider
    return provider


def source_request(service, source_pin, *, declare=True):
    body = request(service)
    body["commands"][0].update(op="fixture.pack-input", args={"source": source_pin} if declare else {})
    return body


def snapshot(service):
    return tuple(service.store.conn.iterdump())


@pytest.mark.parametrize("collection", ["default", "special_effects"])
def test_exact_pack_inventory_retained_after_update_restart_and_retry(service, collection):
    source = create_pack(service, collection=collection)
    source_pin = pin(source)
    seen = []
    install_source_provider(service, source_pin, seen=seen)
    body = source_request(service, source_pin)
    accepted = commit(service, body)
    assert seen == [{"pin": source_pin, "document": source}]
    assert seen[0]["document"]["kind"] == PROJECT_PACK_KIND
    original_bytes = service.store.conn.execute(
        "SELECT content_json FROM timeline_document_input_contents WHERE content_digest=?",
        (source_pin["content_digest"],),
    ).fetchone()[0]
    changed = copy.deepcopy(source["content"])
    changed["admissions"].append({**changed["admissions"][0], "revision": "sha256:" + "3" * 64,
                                  "snapshot_digest": "4" * 64})
    updated = service.update_document(service.test_project, source["document_id"],
                                      {"expected_version": 1, "content": changed}, idempotency_key="pack-v2")["data"]
    assert updated["version"] == 2
    project, root = service.test_project, service.store.root
    service.close()
    restarted = RuntimeService(root)
    try:
        restarted.test_project = project
        provider = install_source_provider(restarted, source_pin, seen=seen)
        before = snapshot(restarted)
        assert commit(restarted, body) == accepted
        assert snapshot(restarted) == before
        assert provider.calls == 0  # Ledger retry needs no provider/source reads.
        next_body = source_request(restarted, source_pin, declare=False)
        commit(restarted, next_body, key="historical-input")
        assert seen == [{"pin": source_pin, "document": source}] * 2
        assert restarted.get_document(project, source["document_id"]) == updated
        assert restarted.store.conn.execute(
            "SELECT content_json FROM timeline_document_input_contents WHERE content_digest=?",
            (source_pin["content_digest"],),
        ).fetchone()[0] == original_bytes
    finally:
        restarted.close()


@pytest.mark.parametrize("damage", ["kind", "schema", "binding", "owner", "project", "id", "revision", "digest", "duplicate"])
def test_invalid_pack_identity_refuses_without_writes(service, damage):
    source = create_pack(service)
    content = copy.deepcopy(source["content"])
    if damage == "kind":
        service.store.conn.execute("UPDATE project_documents SET kind=? WHERE id=?", (PROJECT_PACK_SCHEMA, source["document_id"]))
    elif damage in {"schema", "binding", "owner", "project"}:
        field = {"schema": "schema", "binding": "source_binding_key", "owner": "pack_id", "project": "relative_manifest"}[damage]
        content[field] = "wrong"
    elif damage == "id":
        content["admissions"][0]["id"] = ""
    elif damage == "revision":
        content["admissions"][0]["revision"] = "not-a-revision"
    elif damage == "digest":
        content["admissions"][0]["snapshot_digest"] = "not-a-digest"
    else:
        content["admissions"].append(copy.deepcopy(content["admissions"][0]))
    if damage != "kind":
        source = service.update_document(service.test_project, source["document_id"],
                                          {"expected_version": 1, "content": content}, idempotency_key="invalid-pack")["data"]
    source_pin = pin(source)
    install_source_provider(service, source_pin)
    before = snapshot(service)
    with pytest.raises(RuntimeErrorBase):
        commit(service, source_request(service, source_pin))
    assert snapshot(service) == before


@pytest.mark.parametrize("damage", ["undeclared", "foreign", "stale-version", "wrong-digest", "arbitrary-document"])
def test_source_port_does_not_broaden_document_authority(service, damage):
    source = create_pack(service)
    source_pin = pin(source)
    if damage == "foreign":
        foreign = service.create_project({"name": "Foreign pack", "slug": "foreign-pack"})["id"]
        service.store.conn.execute("UPDATE project_documents SET project_id=? WHERE id=?", (foreign, source["document_id"]))
    elif damage == "stale-version":
        source_pin["version"] += 1
    elif damage == "wrong-digest":
        source_pin["content_digest"] = "sha256:" + "0" * 64
    elif damage == "arbitrary-document":
        service.store.conn.execute("UPDATE project_documents SET kind='notes' WHERE id=?", (source["document_id"],))
    install_source_provider(service, source_pin)
    before = snapshot(service)
    with pytest.raises(RuntimeErrorBase):
        commit(service, source_request(service, source_pin, declare=damage != "undeclared"))
    assert snapshot(service) == before


def test_guessed_retained_pack_pin_is_not_authority_in_another_timeline(service):
    source = create_pack(service)
    source_pin = pin(source)
    install_source_provider(service, source_pin)
    commit(service, source_request(service, source_pin))
    service.create_timeline(service.test_project, "other", idempotency_key="other-timeline")
    body = source_request(service, source_pin)
    other = service.get_project_timeline(service.test_project, "other")
    body.update(timeline_id="other", base_revision_id=other["head_revision_id"],
                base_publication_id=other["head_publication_id"])
    before = snapshot(service)
    with pytest.raises(RuntimeErrorBase, match="authorized closure"):
        service.commit_timeline(service.test_project, "other", body, idempotency_key="guess-pack",
                                publisher="editor", invocation_path=f"/v1/projects/{service.test_project}/timelines/other/commit",
                                authorize=lambda: None)
    assert snapshot(service) == before


@pytest.mark.parametrize("damage", ["stale-capture", "detached-mutation", "corrupt-retention"])
def test_acceptance_revalidates_pack_bytes_before_writes(service, damage):
    source = create_pack(service)
    source_pin = pin(source)
    if damage == "corrupt-retention":
        install_source_provider(service, source_pin)
        commit(service, source_request(service, source_pin))
        service.store.conn.execute("UPDATE timeline_document_input_contents SET content_json='{}'")

    def before_accept(value, candidate):
        if damage == "stale-capture":
            content = copy.deepcopy(source["content"])
            content["admissions"] = []
            service.update_document(service.test_project, source["document_id"],
                                    {"expected_version": 1, "content": content}, idempotency_key="racing-pack")
        else:
            value["document"]["content"]["admissions"] = []  # Detached return cannot mutate private capture.

    install_source_provider(service, source_pin, before_accept=before_accept)
    before = snapshot(service)
    if damage == "detached-mutation":
        commit(service, source_request(service, source_pin))
        captured = capture_document_input(service.store.conn, service.test_project, source_pin,
                                          reachable_pins=[source_pin], expected_kind=PROJECT_PACK_KIND,
                                          expected_schema=PROJECT_PACK_SCHEMA)
        assert captured.document == source
    else:
        with pytest.raises(RuntimeErrorBase):
            commit(service, source_request(service, source_pin), key="invalid-capture")
        if damage == "corrupt-retention":
            assert snapshot(service) == before
        assert service.store.conn.execute("SELECT COUNT(*) FROM timeline_document_input_links").fetchone()[0] == (
            1 if damage == "corrupt-retention" else 0)


@pytest.fixture
def admitted_pack(service, tmp_path, astrid_importable, monkeypatch):
    import yaml
    from astrid.core.element import project_packs as packs
    from astrid.sdk.contracts import DomainResult, ErrorObject

    monkeypatch.setenv(packs.ROOT_ENV, str(tmp_path / "authoring"))
    monkeypatch.setenv(packs.ARTIFACT_ENV, str(tmp_path / "artifacts"))
    verifier = tmp_path / "verify-build.py"
    verifier.write_text(
        "import hashlib,json,sys\nfrom pathlib import Path\n"
        "p=Path(sys.argv[1]);v=json.loads(p.read_bytes())\n"
        "print(json.dumps({'schema':'astrid.element-build/v1',"
        "'selectionDigest':'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest(),"
        "'elements':[{'projectId':e['projectId'],**{k:e['descriptor'][k] "
        "for k in ('packId','id','kind','revision')}} for e in v['elements']]}))\n"
    )
    monkeypatch.setenv(packs.BUILD_ENV, json.dumps([sys.executable, str(verifier)]))

    class Documents:
        def _identity(self):
            return {"realm_id": service.realm["id"]}

        def show(self, document, *, project):
            try:
                return DomainResult.success(service.get_document(project, document))
            except NotFoundError:
                return DomainResult.failure(ErrorObject("not_found", "missing", {}))

        def create(self, *, project, kind, document_id, content, idempotency_key):
            return DomainResult.success(service.create_document(
                project, {"kind": kind, "document_id": document_id, "content": content},
                idempotency_key=idempotency_key,
            )["data"])

        def update(self, document, *, project, content, expected_version, idempotency_key):
            return DomainResult.success(service.update_document(
                project, document, {"content": content, "expected_version": expected_version},
                idempotency_key=idempotency_key,
            )["data"])

    client = SimpleNamespace(documents=Documents())
    realm, project = service.realm["id"], service.test_project
    context = packs.init_project_pack(realm, project, client=client)
    root = Path(context["packRoot"])
    directory = root / "rendering/elements/effects/reveal"
    directory.mkdir(parents=True)
    component = directory / "component.tsx"
    component.write_text("import React from 'react';export default function Reveal(){return <div/>;}\n")
    declaration = {"schema_version": 1, "id": "reveal", "kind": "effect", "pack_id": context["packId"],
                   "short_description": "Selected schema test.", "defaults": {"seed": 4},
                   "schema": {"type": "object", "properties": {"seed": {"type": "number", "maximum": 10}}},
                   "runtime": {"adapter": "remotion"}}
    descriptor_path = directory / "element.yaml"
    descriptor_path.write_text(yaml.safe_dump(declaration))
    manifest = yaml.safe_load((root / "pack.yaml").read_text())
    manifest["rendering"] = {"effects/reveal": {"type": "element",
        "path": "rendering/elements/effects/reveal/element.yaml", "resources": [
            {"kind": "implementation", "path": "rendering/elements/effects/reveal/component.tsx"},
        ]}}
    (root / "pack.yaml").write_text(yaml.safe_dump(manifest))
    admission = packs.admit_project_pack(realm, project, client=client)
    source = service.get_document(project, admission["documentId"])
    record = admission["elements"][0]
    reference = {key: record["descriptor"][key] for key in ("packId", "id", "kind", "revision")}

    def resolve(verified, reference=reference):
        class VerifiedDocuments:
            def _identity(self):
                return {"realm_id": realm}

            def show(self, document, *, project):
                if document == verified["pin"]["document_id"] and project == service.test_project:
                    return DomainResult.success(copy.deepcopy(verified["document"]))
                return DomainResult.failure(ErrorObject("not_found", "missing", {}))
        # Host-boundary proof: the existing resolver still reads its local
        # immutable artifact cache. Runtime CAS custody is not claimed here.
        return packs.resolve_admitted_element(realm, project, reference,
                                              client=SimpleNamespace(documents=VerifiedDocuments()))

    def update_source():
        declaration["schema"]["properties"]["seed"]["maximum"] = 20
        descriptor_path.write_text(yaml.safe_dump(declaration))
        component.write_text(component.read_text() + "// source v2\n")
        return packs.admit_project_pack(realm, project, client=client)

    def no_renderer(*args, **kwargs):
        raise AssertionError("save called renderer or launcher")

    import runtime_protocol.service as service_module
    from runtime_protocol import visual_seam
    monkeypatch.setattr(service_module, "evaluate_closure", no_renderer)
    monkeypatch.setattr(visual_seam, "evaluate_closure", no_renderer)
    monkeypatch.setattr(packs, "_open_client", no_renderer)
    return SimpleNamespace(source=source, record=record, reference=reference, resolve=resolve,
                           update_source=update_source, packs=packs)


@pytest.mark.integration
def test_real_admission_inventory_retention_keeps_exact_selected_revision(service, admitted_pack):
    case = admitted_pack
    source_pin = pin(case.source)
    selected = []

    def select(verified, candidate):
        descriptor = case.resolve(verified)["descriptor"]
        assert descriptor == case.record["descriptor"]
        selected.append(descriptor)

    install_source_provider(service, source_pin, before_accept=select)
    body = source_request(service, source_pin)
    accepted = commit(service, body)
    original_files = {item["path"]: (Path(case.record["snapshot"]["root"]) / item["path"]).read_bytes()
                      for item in case.record["snapshot"]["files"]}
    new_admission = case.update_source()
    assert new_admission["elements"][0]["descriptor"]["revision"] != case.reference["revision"]
    assert new_admission["elements"][0]["descriptor"]["schema"]["properties"]["seed"]["maximum"] == 20
    project, root = service.test_project, service.store.root
    service.close()
    restarted = RuntimeService(root)
    try:
        restarted.test_project = project
        provider = install_source_provider(restarted, source_pin, before_accept=select)
        before = snapshot(restarted)
        assert commit(restarted, body) == accepted
        assert snapshot(restarted) == before and provider.calls == 0
        commit(restarted, source_request(restarted, source_pin, declare=False), key="exact-old-admission")
        assert len(selected) == 2
        assert selected[-1]["schema"]["properties"]["seed"]["maximum"] == 10
        assert {item["path"]: (Path(case.record["snapshot"]["root"]) / item["path"]).read_bytes()
                for item in case.record["snapshot"]["files"]} == original_files
    finally:
        restarted.close()


@pytest.mark.integration
@pytest.mark.parametrize("damage", ["owner", "id", "kind", "revision", "snapshot", "build-receipt"])
def test_real_exact_selection_refuses_without_acceptance_writes(service, admitted_pack, damage):
    from runtime_protocol.timeline_commit_port import refused

    case = admitted_pack
    reference = copy.deepcopy(case.reference)
    if damage in {"owner", "id", "kind", "revision"}:
        reference[{"owner": "packId"}.get(damage, damage)] = "wrong"
    else:
        root = Path(case.record["snapshot"]["root"])
        path = root / (case.record["snapshot"]["componentPath"] if damage == "snapshot" else ".build-receipt.json")
        path.write_text("{}")

    def select(verified, candidate):
        try:
            case.resolve(verified, reference)
        except (ValueError, OSError) as exc:
            raise refused("dependency_unavailable", "exact admitted declaration is unavailable") from exc
        raise AssertionError("damaged selection unexpectedly resolved")

    source_pin = pin(case.source)
    install_source_provider(service, source_pin, before_accept=select)
    before = snapshot(service)
    with pytest.raises(RuntimeErrorBase, match="exact admitted declaration"):
        commit(service, source_request(service, source_pin))
    assert snapshot(service) == before
