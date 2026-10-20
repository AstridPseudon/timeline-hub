"""Native selected PARAM custody through the authenticated, renderer-free door."""
from __future__ import annotations

import base64
import copy
import http.client
import json
import shutil
import socket
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.door import DoorConfig
from runtime_protocol.errors import NotFoundError
from runtime_protocol.server import RuntimeHandler
from runtime_protocol.timeline_commit_port import RequestCommitPort
from runtime_protocol.util import atomic_json_write
from tests.door_helpers import HOSTED, PRODUCT_ACTOR, DoorWorld
from test_timeline_commit_integration import (
    Editing,
    agent,  # noqa: F401 (shared renderer-off/native provider fixture)
    film,  # noqa: F401 (shared immutable M1 film fixture)
    inverse,
    positions,
    rows,
)

pytestmark = pytest.mark.integration
REF = "parent/clip:selected-effect"


def _admit(service, tmp_path, monkeypatch):
    from astrid.core.element import project_packs as packs
    from astrid.sdk.contracts import DomainResult, ErrorObject

    monkeypatch.setenv(packs.ROOT_ENV, str(tmp_path / "authoring"))
    monkeypatch.setenv(packs.ARTIFACT_ENV, str(tmp_path / "artifacts"))
    # The existing pack-input fixture's build verifier: admission/custody proof,
    # without starting a renderer or claiming build/render qualification.
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

    class Media:
        def import_bytes(self, *, project, data, filename, media_type, idempotency_key):
            return DomainResult.success(service.ingest(
                project, data, media_type=media_type, idempotency_key=idempotency_key,
            )["data"])

        def read_bytes(self, object_id):
            return service.cas.read(object_id.removeprefix("sha256:"))

    return packs, SimpleNamespace(documents=Documents(), media=Media())


def _snapshot(service):
    trees = []
    for root in (service.cas.root, service.store.staging_root):
        trees.append({str(path.relative_to(root)): (path.stat().st_mtime_ns,
                      path.read_bytes() if path.is_file() else None)
                      for path in [root, *root.rglob("*")]})
    return rows(service), trees


def _forbidden(*args, **kwargs):
    raise AssertionError("PARAM save/retry/inverse used authoring, launcher, cache, or evaluation")


def _isolate(patch, packs):
    for name in ("_open_client", "resolve_admitted_element", "authoring_root", "artifact_root"):
        patch.setattr(packs, name, _forbidden)


def test_selected_params_lost_ack_retains_v1_over_restart_and_guarded_inverse(
    film, agent, tmp_path, monkeypatch,  # noqa: F811 (shared fixtures)
):
    import yaml
    from astrid.sdk.timeline import commands, commit
    from astrid.sdk.timeline._clip_commands import capture_clip_add
    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline._scalar_commands import capture_clip_set_params

    credential = tmp_path / "product.json"

    def start():
        daemon = RuntimeDaemon(
            film.fixture.duplicate_root, support_root=tmp_path / "support", authoring_profile="astrid",
            door=DoorConfig(origin=HOSTED, port=0, credential_file=credential),
        ).start()
        world = DoorWorld(tmp_path, daemon, credential)
        try:
            if not credential.exists():
                world.provision()
            reply = world.call("/api/runtime/v1/handshake", "POST", body=b"{}",
                               headers={"Content-Type": "application/json"})
            assert reply.status == 200, reply.body
            health = world.call("/api/runtime/v1/health")
            assert health.status == 200, health.body
            return world, reply.json(), health.json()
        except BaseException:
            world.stop()
            raise

    def post(world, path, encoded, key, **kwargs):
        return world.call("/api/runtime" + path, "POST", body=encoded,
                          headers={"Content-Type": "application/json", "Idempotency-Key": key}, **kwargs)

    def accept(world, edit, calls, key):
        reply = post(world, edit.path, json.dumps(edit.body(calls)).encode(), key)
        assert reply.status == 200, reply.body
        return reply.json()

    world, identity, health = start()
    try:
        edit = Editing(world.daemon.service, film, agent)
        edit.assert_baseline()
        packs, client = _admit(edit.service, tmp_path, monkeypatch)
        realm, project = identity["realm_id"], edit.project
        assert identity["actor_id"] == PRODUCT_ACTOR
        context = packs.init_project_pack(realm, project, client=client)
        source_root = Path(context["packRoot"])
        directory = source_root / "rendering/elements/effects/reveal"
        directory.mkdir(parents=True)
        (directory / "component.tsx").write_text(
            "import React from 'react';export default function Reveal(){return <div/>;}\n")
        declaration = {"schema_version": 1, "id": "reveal", "kind": "effect", "pack_id": context["packId"],
                       "short_description": "Selected PARAM durability.", "defaults": {"seed": 4},
                       "schema": {"type": "object", "properties": {"seed": {"type": "number", "maximum": 10}},
                                  "required": ["unrelated"], "additionalProperties": False},
                       "runtime": {"adapter": "remotion"}}
        declaration_path = directory / "element.yaml"
        declaration_path.write_text(yaml.safe_dump(declaration))
        manifest = yaml.safe_load((source_root / "pack.yaml").read_text())
        manifest["rendering"] = {"effects/reveal": {"type": "element",
            "path": "rendering/elements/effects/reveal/element.yaml", "resources": [
                {"kind": "implementation", "path": "rendering/elements/effects/reveal/component.tsx"}]}}
        (source_root / "pack.yaml").write_text(yaml.safe_dump(manifest))
        admitted = packs.admit_project_pack(realm, project, client=client)
        record = admitted["elements"][0]
        selected = {key: record["descriptor"][key] for key in ("id", "kind", "packId", "revision")}
        source = edit.service.get_document(project, admitted["documentId"])
        pin = {"document_id": source["document_id"], "version": source["version"],
               "content_digest": commit._digest(source["content"])}
        objects = {}
        for admission in source["content"]["admissions"]:
            descriptor = admission["snapshot_object"]
            data = edit.service.cas.read(descriptor["object_id"].removeprefix("sha256:"))
            objects[descriptor["object_id"]] = {
                **descriptor, "bytes_base64": base64.b64encode(data).decode("ascii")}
        assert packs.admitted_element_snapshot_descriptor(
            realm, project, selected, {"pin": pin, "document": source},
            next(iter(objects.values())),
        )["schema"]["properties"]["seed"]["maximum"] == 10
        accept(world, edit, [agent.track(agent.bundle(edit.document()), "parent",
               {"id": "params-picture", "kind": "visual"})], "params-track")
        clip = {"id": "selected-effect", "clipType": selected["id"], "elementRef": selected,
                "at": 0, "hold": 2, "track": "params-picture",
                "params": {"seed": 4, "future": {"keep": [None, False, {}, "ƒ(literal)"]}}}
        accept(world, edit, [capture_clip_add(agent.bundle(edit.document()), "parent", clip)], "params-clip")
        initial = copy.deepcopy(edit.document())
        original = State(agent.bundle(initial)).entity(REF)
        command = capture_clip_set_params(
            agent.bundle(initial), REF, values={"seed": 8}, schema_source=pin, realm_id=realm,
            schema_inputs=[({"pin": pin, "document": source}, objects)],
        )
        request = edit.body([command])
        encoded = json.dumps(request, sort_keys=True, ensure_ascii=False).encode()
        flight_path = tmp_path / "in-flight.json"
        flight = {"path": edit.path, "body_base64": base64.b64encode(encoded).decode("ascii"),
                  "key": "params-lost-ack", "realm_id": realm, "actor_id": identity["actor_id"]}
        atomic_json_write(flight_path, flight)
        before_history = copy.deepcopy(edit.history())
        observed = []
        send = RuntimeHandler._send

        def drop_ack(handler, status, payload=None, **kwargs):
            if handler.path == edit.path and handler.headers.get("Idempotency-Key") == flight["key"]:
                assert status == 200, payload
                observed.append(copy.deepcopy(payload))
                handler.close_connection = True
                handler.connection.shutdown(socket.SHUT_RDWR)
                return
            return send(handler, status, payload, **kwargs)

        with monkeypatch.context() as saving:
            _isolate(saving, packs)
            saving.setattr(RuntimeHandler, "_send", drop_ack)
            with pytest.raises(http.client.RemoteDisconnected):
                post(world, flight["path"], encoded, flight["key"])
        assert len(observed) == 1
        accepted = observed[0]  # Server-side observer only; the client received no ACK.
        assert len(edit.history()) == len(before_history) + 1
        accepted_history = copy.deepcopy(edit.history())
        assert accepted_history[-1]["records"]["commands"][0]["command"] == command
        assert accepted["data"]["canonical_document"]["dependency_manifest"]["documents"] == [pin]
        assert State(agent.bundle(accepted["data"]["canonical_document"])).entity(REF)["params"] == {
            **original["params"], "seed": 8}
        newer = accept(world, edit, [edit.move("music-other", 2)], "params-disjoint-c")
        declaration["schema"]["properties"]["seed"]["maximum"] = 20
        declaration_path.write_text(yaml.safe_dump(declaration))
        v2 = packs.admit_project_pack(realm, project, client=client)
        assert v2["elements"][0]["descriptor"]["revision"] != selected["revision"]
        assert v2["elements"][0]["descriptor"]["schema"]["properties"]["seed"]["maximum"] == 20
        current = edit.service.get_document(project, pin["document_id"])
        edit.service.update_document(project, pin["document_id"], {
            "expected_version": current["version"], "content": {**current["content"], "admissions": []},
        }, idempotency_key="params-remove-current-selection")
        shutil.rmtree(tmp_path / "authoring")
        shutil.rmtree(tmp_path / "artifacts")
        history = copy.deepcopy(edit.history())
    finally:
        world.stop()

    _isolate(monkeypatch, packs)
    world, restarted_identity, restarted_health = start()
    try:
        assert restarted_identity["session_id"] != identity["session_id"]
        for key in ("realm_id", "actor_id", "schema_digest"):
            assert restarted_identity[key] == identity[key]
        assert restarted_health["runtime_instance_id"] != health["runtime_instance_id"]
        assert restarted_health["runtime_epoch"] > health["runtime_epoch"]
        recovered = json.loads(flight_path.read_bytes())
        assert recovered == flight
        encoded_retry = base64.b64decode(recovered["body_base64"])
        assert encoded_retry == encoded
        assert json.loads(encoded_retry) == request
        edit = Editing(world.daemon.service, film, agent)
        assert edit.head()["publication_id"] == newer["receipt"]["receipt_id"]
        before = _snapshot(edit.service)
        refused = post(world, recovered["path"], encoded_retry, recovered["key"], origin="https://foreign.test")
        assert refused.status == 403, refused.body
        assert _snapshot(edit.service) == before
        with monkeypatch.context() as retry:
            retry.setattr(type(edit.service._timeline_commit_provider), "commit", _forbidden)
            retry.setattr(commands, "execute", _forbidden)
            reply = post(world, recovered["path"], encoded_retry, recovered["key"])
        assert reply.status == 200, reply.body
        assert reply.json() == accepted
        assert _snapshot(edit.service) == before
        assert edit.history() == history
        assert sum(entry["publication_id"] == accepted["receipt"]["receipt_id"] for entry in history) == 1
        edit.assert_readback(accepted)
        edit.assert_readback(newer)
        assert edit.document() == newer["data"]["canonical_document"]

        # Raw wire bypasses capture: V2's maximum=20 cannot authorize this V1 element.
        raw = {"schema_version": 1, "op": "clip.set-params", "version": "1", "select": REF,
               "args": {"values": {"seed": 16}, "clear": [], "schema_source": pin}}
        refused = post(world, edit.path, json.dumps(edit.body([raw])).encode(), "params-invalid-16")
        assert refused.status == 409, refused.body
        failure = refused.json()
        assert failure["details"]["reason"] == "invalid_edit_command"
        assert failure["message"] == "16 is greater than the maximum of 10"
        assert _snapshot(edit.service) == before

        consumed = []
        read_object = RequestCommitPort.document_object

        def observe_object(port, source_pin, object_id):
            result = read_object(port, source_pin, object_id)
            consumed.append((copy.deepcopy(source_pin), object_id, copy.deepcopy(result)))
            return result

        monkeypatch.setattr(RequestCommitPort, "document_object", observe_object)
        undone = accept(world, edit, [inverse(accepted["receipt"]["receipt_id"])], "params-native-inverse")
        closure = undone["data"]["canonical_document"]
        assert consumed and all(item[0] == pin and item[1] in objects for item in consumed)
        assert all(item[2] == objects[item[1]] for item in consumed)
        assert State(agent.bundle(closure)).entity(REF) == original
        assert positions(closure)["music-other"] == 2
        expected_parent = copy.deepcopy(newer["data"]["canonical_document"]["parent_revision"]["payload"])
        for container in (expected_parent, expected_parent["config"]):
            for index, row in enumerate(container["clips"]):
                if row["id"] == "selected-effect":
                    container["clips"][index] = copy.deepcopy(original)
        assert closure["parent_revision"]["payload"] == expected_parent
        assert closure["dependency_manifest"] == newer["data"]["canonical_document"]["dependency_manifest"]
        assert closure["dependency_manifest"]["documents"] == [pin]
        assert closure["shot_revisions"] == initial["shot_revisions"]
        assert closure["internal_timeline_revisions"] == initial["internal_timeline_revisions"]
        assert edit.history()[:-1] == history
        assert edit.history()[-1]["records"]["undo_of"] == [accepted["receipt"]["receipt_id"]]
        assert edit.history()[:len(accepted_history)] == accepted_history
        edit.assert_readback(accepted)
        edit.assert_readback(undone)
        assert edit.document() == closure
        assert json.loads(flight_path.read_bytes()) == flight
        assert not (tmp_path / "authoring").exists()
        assert not (tmp_path / "artifacts").exists()
        edit.assert_baseline()
    finally:
        world.stop()
