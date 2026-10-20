"""First historical admission of a real PARAM edit consuming portable pack bytes."""
from __future__ import annotations

import base64
import copy
import io
import json
import shutil
import sys
import wave
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from test_canonical_render_admission import _digest, _publication, _snapshot
from test_canonical_render_admission import canonical_scene as canonical_scene
from test_render_historical_admission import _admissions, _request, _selector, _state

from runtime_protocol.errors import ConflictError, NotFoundError
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_port import RequestCommitPort, route_path
from runtime_protocol.util import canonical_json

pytestmark = pytest.mark.integration
REF = "occurrence:effect-occurrence/clip:effect"
OPAQUE = {"literal": [None, False, {}, "ƒ(keep literal)"], "shot_id": "opaque-owner"}


def _unavailable(*args, **kwargs):
    raise AssertionError("save or historical admission used source/cache/launcher/renderer")


@pytest.fixture
def retained_pack(canonical_scene, astrid_importable, tmp_path, monkeypatch):  # noqa: F811
    from astrid.core.element import project_packs as packs
    from astrid.sdk.contracts import DomainResult, ErrorObject
    from astrid.sdk.timeline import commit
    from astrid.sdk.timeline._scalar_commands import capture_clip_set_params

    assert Path(commit.__file__).resolve().is_relative_to(astrid_importable)
    f = canonical_scene
    service, project = f["service"], f["project"]
    realm = service.realm["id"]
    case = SimpleNamespace(service=service, project=project, root=service.store.root)
    monkeypatch.setenv(packs.ROOT_ENV, str(tmp_path / "authoring"))
    monkeypatch.setenv(packs.ARTIFACT_ENV, str(tmp_path / "build-cache"))
    # Same configured admission build verifier as Agent's project-pack tests.
    verifier = tmp_path / "build-verifier.py"
    verifier.write_text(
        "import json,sys,hashlib\nfrom pathlib import Path\n"
        "p=Path(sys.argv[1]);x=json.loads(p.read_text());print(json.dumps({"
        "'schema':'astrid.element-build/v1',"
        "'selectionDigest':'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest(),"
        "'elements':[{'projectId':e['projectId'],**{k:e['descriptor'][k] "
        "for k in ('packId','id','kind','revision')}} for e in x['elements']]}))\n"
    )
    monkeypatch.setenv(packs.BUILD_ENV, json.dumps([sys.executable, str(verifier)]))

    class Documents:
        def _identity(self):
            return {"realm_id": realm}

        def show(self, document, *, project):
            try:
                return DomainResult.success(case.service.get_document(project, document))
            except NotFoundError:
                return DomainResult.failure(ErrorObject("not_found", "missing", {}))

        def create(self, *, project, kind, document_id, content, idempotency_key):
            return DomainResult.success(case.service.create_document(
                project, {"kind": kind, "document_id": document_id, "content": content},
                idempotency_key=idempotency_key)["data"])

        def update(self, document, *, project, content, expected_version, idempotency_key):
            return DomainResult.success(case.service.update_document(
                project, document, {"content": content, "expected_version": expected_version},
                idempotency_key=idempotency_key)["data"])

    class Media:
        def import_bytes(self, *, project, data, filename, media_type, idempotency_key):
            return DomainResult.success(case.service.ingest(
                project, data, media_type=media_type, idempotency_key=idempotency_key)["data"])

        def read_bytes(self, object_id):
            return case.service.cas.read(object_id.removeprefix("sha256:"))

    @contextmanager
    def connected():
        yield SimpleNamespace(documents=Documents(), media=Media())

    monkeypatch.setattr(packs, "_open_client", connected)
    context = packs.init_project_pack(realm, project)
    source = Path(context["packRoot"])
    directory = source / "rendering/elements/effects/reveal"
    directory.mkdir(parents=True)
    (directory / "component.tsx").write_text(
        "import React from 'react';\nimport {AbsoluteFill} from 'remotion';\n"
        "export default function Reveal(){return <AbsoluteFill/>;}\n")
    definition = {"schema_version": 1, "id": "reveal", "kind": "effect", "pack_id": context["packId"],
                  "short_description": "Retained render effect.", "defaults": {"seed": 4},
                  "schema": {"type": "object", "properties": {"seed": {"type": "number", "maximum": 10}}},
                  "runtime": {"adapter": "remotion"}}
    path = directory / "element.yaml"
    path.write_text(yaml.safe_dump(definition))
    manifest = yaml.safe_load((source / "pack.yaml").read_text())
    manifest["rendering"] = {"effects/reveal": {"type": "element",
        "path": "rendering/elements/effects/reveal/element.yaml", "resources": [
            {"kind": "implementation", "path": "rendering/elements/effects/reveal/component.tsx"}]}}
    (source / "pack.yaml").write_text(yaml.safe_dump(manifest))
    first = packs.admit_project_pack(realm, project)
    selected = {key: first["elements"][0]["descriptor"][key] for key in ("id", "kind", "packId", "revision")}
    document = service.get_document(project, first["documentId"])
    pin = {"document_id": document["document_id"], "version": document["version"],
           "content_digest": commit._digest(document["content"])}
    descriptor = document["content"]["admissions"][0]["snapshot_object"]
    portable = service.object(descriptor["object_id"])[1]
    objects = {descriptor["object_id"]: {**descriptor, "bytes_base64": base64.b64encode(portable).decode("ascii")}}
    options = {"schema_source": pin, "realm_id": realm,
               "schema_inputs": [({"pin": pin, "document": document}, objects)]}

    # Preserve the original valid scene rendering fixture, with real WAV media.
    stream = io.BytesIO()
    with wave.open(stream, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(b"\0\0" * 8000 * 15)
    f["audio"] = service.ingest(project, stream.getvalue(), media_type="audio/wav", idempotency_key="real-wave")["data"]
    service.create_project_shot(project, {"shot_id": "effect-shot", "name": "Effect"}, idempotency_key="effect-shot")
    seed = _publication(f, revision="retained-render-seed")
    seed["parent_composition"]["config"]["tracks"].append({"id": "fx", "kind": "visual"})
    seed["internal_timeline_revisions"] = [{"timeline_id": "main", "revision_id": "effect-internal-v0", "payload": {
        "tracks": [{"id": "fx", "kind": "visual"}], "clips": [
            {"id": "effect", "clipType": selected["id"], "elementRef": selected, "at": 0, "hold": 2,
             "track": "fx", "params": {"seed": 4, "future": OPAQUE}, "app": {"opaque": OPAQUE}}],
        "registry": {"assets": {}}, "effects": [], "audio": [], "layout": {}, "assets": []}}]
    seed["internal_timeline_revisions"][0]["payload"]["clips"].append({
        "id": "child-picture", "clipType": "haus.astrid.liveScene", "at": 0,
        "from": 55, "to": 59, "speed": 2, "track": "fx", "app": {"liveScene": copy.deepcopy(f["envelope"])}})
    seed["shot_revisions"] = [{"shot_id": "effect-shot", "revision_id": "effect-shot-v0",
        "internal_timeline_revision_id": "effect-internal-v0", "payload": {
            "metadata": {"opaque": OPAQUE}, "items": [], "pools": [], "selected_variants": {},
            "provenance": {}, "generation_inputs": {}, "audio_bindings": [], "text_bindings": []}}]
    seed["parent_composition"]["occurrences"] = [{"occurrence_id": "effect-occurrence", "shot_id": "effect-shot",
        "shot_revision_id": "effect-shot-v0", "placement": {"start_ms": 0, "track": "fx"},
        "source_offset": 0, "duration_ms": 3000, "speed": 1, "track": "fx", "transform": {},
        "gain": 1, "mute": False, "provenance": {"opaque": OPAQUE}}]
    # Bootstrap only; every measured A/C edit uses native capture and acceptance.
    service.publish_parent_composition(project, "main", seed, idempotency_key="seed")
    service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    case.reads, case.object_reads = [], []
    for name, observed in (("config_source", case.reads), ("document_object", case.object_reads)):
        original = getattr(RequestCommitPort, name)
        def watch(port, *args, original=original, observed=observed):
            result = original(port, *args)
            observed.append(copy.deepcopy(result))
            return result
        monkeypatch.setattr(RequestCommitPort, name, watch)

    def bundle():
        head = case.service.get_project_timeline(project, "main")
        closure = case.service._timeline_commits()[0].revision_closure(project, "main", head["head_revision_id"])
        return commit.bundle_from_document(closure)

    def params(value, key):
        head = case.service.get_project_timeline(project, "main")
        body = {"api_version": 1, "project_id": project, "timeline_id": "main",
                "base_revision_id": head["head_revision_id"], "base_publication_id": head["head_publication_id"],
                "commands": []}
        with monkeypatch.context() as save:
            save.setattr(packs, "_open_client", _unavailable)
            save.setattr(packs, "resolve_admitted_element", _unavailable)
            import runtime_protocol.service as service_module
            from runtime_protocol import visual_seam

            save.setattr(service_module, "evaluate_closure", _unavailable)
            save.setattr(visual_seam, "evaluate_closure", _unavailable)
            body["commands"] = [capture_clip_set_params(bundle(), REF, values={"seed": value}, **options)]
            result = case.service.commit_timeline(project, "main", body, idempotency_key=key,
                publisher="retained-pack-editor", invocation_path=route_path(project, "main"), authorize=lambda: None)
        assert result["data"]["status"] == "accepted"
        assert result["receipt"]["result"] == result["data"]
        return result

    case.params = params
    case.a = params(8, "actual-PARAM-A")
    assert case.reads and all(value == {"pin": pin, "document": document} for value in case.reads)
    assert case.object_reads and all(value == objects[descriptor["object_id"]] for value in case.object_reads)
    assert case.a["data"]["canonical_document"]["dependency_manifest"]["documents"] == [pin]
    definition["schema"]["properties"]["seed"]["maximum"] = 20
    path.write_text(yaml.safe_dump(definition))
    newer = packs.admit_project_pack(realm, project)
    assert newer["elements"][0]["descriptor"]["revision"] != selected["revision"]
    assert service.get_document(project, pin["document_id"])["version"] == pin["version"] + 1
    case.c = params(9, "actual-PARAM-C")
    case.foreign = service.create_project({"slug": "foreign-pack", "name": "Foreign pack"})["id"]
    assert case.a["data"]["accepted_revision_id"] != case.c["data"]["accepted_revision_id"]
    # Remove mutable pack and timeline configuration, never accepted rows.
    service.store.conn.execute("DELETE FROM project_documents WHERE id IN (?, ?)",
                               (pin["document_id"], "timeline:main"))
    shutil.rmtree(source)
    shutil.rmtree(tmp_path / "build-cache")
    assert _admissions(service) == ([], [])
    case.pin, case.document, case.descriptor, case.portable = pin, document, descriptor, portable
    case.media = {item["object_id"]: service.object(item["object_id"])[1]
                  for item in (f["audio"], f["entry"], f["package"])}
    service.close()
    case.service = RuntimeService(case.root)
    monkeypatch.setattr(packs, "_open_client", _unavailable)
    monkeypatch.setattr(packs, "resolve_admitted_element", _unavailable)
    monkeypatch.setattr(packs, "artifact_root", _unavailable)
    monkeypatch.setattr(packs, "authoring_root", _unavailable)
    try:
        assert _admissions(case.service) == ([], [])
        yield case
    finally:
        case.service.close()


def _assert_retained(case):
    commits = case.service._timeline_commits()[0]
    original = case.a["data"]["canonical_document"]
    assert commits.revision_closure(case.project, "main", _selector(case)["revision_id"]) == original
    assert commits.history_entry(case.project, "main", _selector(case)["publication_id"])["receipt"] == case.a["receipt"]
    retained = case.service.store.conn.execute(
        "SELECT content_json FROM timeline_document_input_contents WHERE content_digest=?", (case.pin["content_digest"],)
    ).fetchone()
    assert retained[0] == canonical_json(case.document["content"])
    assert case.service.object(case.descriptor["object_id"])[1] == case.portable
    assert _digest(case.portable) == case.descriptor["digest"]
    head = case.service.get_project_timeline(case.project, "main")
    assert (head["head_revision_id"], head["head_publication_id"]) == (
        case.c["data"]["accepted_revision_id"], case.c["receipt"]["receipt_id"])
    a_child = original["shot_revisions"][0]
    c_child = case.c["data"]["canonical_document"]["shot_revisions"][0]
    assert a_child["shot_id"] == c_child["shot_id"]
    assert a_child["revision_id"] != c_child["revision_id"]
    latest = case.service.store.conn.execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id=?",
                                            (a_child["shot_id"],)).fetchone()
    assert latest[0] == c_child["revision_id"]
    internal = original["internal_timeline_revisions"][0]["payload"]
    assert internal["clips"][0]["params"] == {"seed": 8, "future": OPAQUE}
    assert internal["clips"][0]["app"]["opaque"] == OPAQUE
    assert a_child["payload"]["metadata"]["opaque"] == OPAQUE
    for object_id, data in case.media.items():
        assert case.service.object(object_id)[1] == data


def test_first_historical_param_admission_freezes_retained_pack_and_child(retained_pack):
    case = retained_pack
    _assert_retained(case)
    request = _request(case)
    admitted = case.service.create_task(request)
    spec = admitted["task"]["spec"]
    authority = spec["spec"]["inputs"]["timeline_authority"]
    assert authority["parent_revision_id"] == _selector(case)["revision_id"]
    assert authority["parent_content_digest"] == _selector(case)["content_digest"]
    assert authority["publication_id"] == case.a["receipt"]["receipt_id"]
    assert authority["head_event_id"] == case.a["receipt"]["event_ids"][-1]
    snapshot = _snapshot(case.service, spec)
    child = next(clip for clip in snapshot["config"]["clips"] if clip.get("elementRef"))
    assert child["params"] == {"seed": 8, "future": OPAQUE}
    assert child["app"]["opaque"] == OPAQUE
    assert child["elementRef"] == case.a["data"]["canonical_document"]["internal_timeline_revisions"][0]["payload"]["clips"][0]["elementRef"]
    assert set(case.media) <= set(spec["input_object_ids"])
    assert case.service.object(spec["spec"]["timeline_snapshot_ref"]["digest"])[1] == canonical_json(snapshot).encode()
    assert all(len(rows) == 1 for rows in _admissions(case.service))
    _assert_retained(case)
    # Advance again AFTER admission, then prove exact replay from a fresh Runtime.
    from astrid.sdk.timeline import commit

    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    case.c = case.params(7, "actual-PARAM-D-after-admission")
    _assert_retained(case)
    case.service.close()
    case.service = RuntimeService(case.root)
    before = _state(case.service)
    assert case.service.create_task(request) == admitted
    assert _state(case.service) == before
    _assert_retained(case)


@pytest.mark.parametrize("damage", ["missing", "wrong-custody", "same-size-corrupt"])
def test_retained_pack_refusal_precedes_all_admission_writes(retained_pack, damage, monkeypatch):
    case = retained_pack
    descriptor = case.descriptor
    path = case.service.cas.path_for(descriptor["object_id"].removeprefix("sha256:"))
    if damage == "missing":
        path.unlink()
    elif damage == "wrong-custody":
        case.service.store.conn.execute("UPDATE project_objects SET project_id=? WHERE project_id=? AND digest=?",
                                       (case.foreign, case.project, descriptor["object_id"].removeprefix("sha256:")))
    else:
        path.write_bytes(bytes([case.portable[0] ^ 1]) + case.portable[1:])
        assert path.stat().st_size == descriptor["size"]
    writes = []
    case.service.store.conn.set_trace_callback(lambda sql: writes.append(sql) if sql.split()[0].upper() in {
        "INSERT", "UPDATE", "DELETE", "REPLACE", "CREATE", "ALTER", "DROP"} else None)
    monkeypatch.setattr(case.service.store, "_publish_spec_snapshot", _unavailable)
    before = _state(case.service)
    with pytest.raises(ConflictError) as refused:
        case.service.create_task(_request(case))
    assert refused.value.details == {"reason": "render_revision_integrity", "dependency_id": (
        _selector(case)["revision_id"] if damage == "wrong-custody" else case.pin["document_id"])}
    assert writes == []
    case.service.store.conn.set_trace_callback(None)
    assert _state(case.service) == before
    assert _admissions(case.service) == ([], [])
