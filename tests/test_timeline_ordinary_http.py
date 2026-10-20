"""Supported literal parent edits and explicit media refusals over the real door.

No legacy media seed: positive parent media trim/split needs native insertion.
"""
from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

import pytest

from astrid_runtime_client import ApiError, CONTRACT_VERSION, WorkspaceClient
from astrid_runtime_client.contract_metadata import SCHEMA_DIGEST as CLIENT_SCHEMA_DIGEST
from runtime_protocol.contract_metadata import SCHEMA_DIGEST
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.door import DoorConfig
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from tests.door_helpers import HOSTED, PRODUCT_ACTOR, DoorWorld, write_owner_only

pytestmark = pytest.mark.integration


def test_ordinary_http_empty_bootstrap_must_be_reachable(
    tmp_path, monkeypatch, astrid_importable,
):
    def forbidden(*args, **kwargs):
        raise AssertionError("ordinary editing called a legacy writer or renderer")

    class RendererStopped:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(("astrid.packs.rendering", "astrid.core.rendering",
                                    "astrid.sdk.authoring_render_preview",
                                    "astrid.core.timeline.compatibility",
                                    "composition", "remotion")) or "scene" in fullname:
                raise AssertionError("ordinary editing imported renderer: " + fullname)

    # Install before startup and empty bootstrap, including already-imported
    # evaluator aliases. Persistence primitives used by commit remain real.
    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam

    monkeypatch.setattr(sys, "meta_path", [RendererStopped(), *sys.meta_path])
    monkeypatch.setattr(service_module, "evaluate_closure", forbidden)
    monkeypatch.setattr(visual_seam, "evaluate_closure", forbidden)
    for name in (
        "publish_parent_composition", "replace_parent_composition_media",
        "replace_timeline_clip", "update_timeline", "create_timeline_document",
        "create_document", "update_document", "create_project_shot",
        "update_project_shot", "create_shot", "update_shot",
        "publish_timeline_render", "_publication_replay_result",
    ):
        monkeypatch.setattr(RuntimeService, name, forbidden)

    from astrid.sdk.timeline import commit as agent

    assert Path(agent.__file__).resolve().is_relative_to(astrid_importable)
    assert CONTRACT_VERSION == "0.2.3"
    assert CLIENT_SCHEMA_DIGEST == SCHEMA_DIGEST
    agent_metadata = (astrid_importable / "astrid_runtime_client" / "contract_metadata.py").read_text()
    assert f"CONTRACT_VERSION = {CONTRACT_VERSION!r}" in agent_metadata
    assert f"SCHEMA_DIGEST = {SCHEMA_DIGEST!r}" in agent_metadata

    credential = tmp_path / "product.json"
    RealmStore.initialize(tmp_path / "realm").close()
    daemon = RuntimeDaemon(
        tmp_path / "realm", support_root=tmp_path / "support", authoring_profile="astrid",
        door=DoorConfig(origin=HOSTED, port=0, credential_file=credential),
    ).start()
    world = DoorWorld(tmp_path, daemon, credential)
    try:
        world.provision()

        responses = []
        lose_ack = False
        flight_file = tmp_path / "inflight.json"

        def transport(method, path, headers, body):
            losing = lose_ack and method == "POST" and path.endswith("/commit")
            if losing:
                # A durable flight fixture, not a production client outbox.
                write_owner_only(flight_file, {
                    "method": method, "path": path, "headers": dict(headers),
                    "body_hex": body.hex(), "realm_id": identity.realm_id,
                    "actor_id": identity.actor_id,
                })
                with flight_file.open("rb") as persisted:
                    os.fsync(persisted.fileno())
                directory = os.open(tmp_path, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
            response = world.call("/api/runtime" + path, method, headers=headers, body=body)
            responses.append(response)
            if losing:
                raise TimeoutError("lost acknowledgement after durable acceptance")
            return response.status, response.headers, response.body

        # The generated client serializes real requests; this adapter only adds
        # the browser door prefix/Origin and opens a real HTTP connection.
        client = WorkspaceClient(daemon.door_endpoint, transport=transport)
        health = client.health()
        assert health.status == "ok" and health.schema_digest == SCHEMA_DIGEST
        identity = client.handshake("ordinary-http", "1", ["projects:read", "projects:write"])
        assert identity.actor_id == PRODUCT_ACTOR and identity.schema_digest == SCHEMA_DIGEST
        assert daemon.service._timeline_commit_provider.__class__ is agent.RuntimeCommitService
        assert daemon.service._timeline_commit_provider.contract_digest == SCHEMA_DIGEST
        project = client.create_project("Ordinary HTTP", slug="ordinary-http", idempotency_key="project")["project_id"]
        bootstrap_error = None
        try:
            client.create_timeline(project, "film", idempotency_key="empty-bootstrap")
        except ApiError as error:
            bootstrap_error = error
        assert bootstrap_error is None, (
            "ordinary_http_empty_bootstrap_must_be_reachable: normal create_timeline must reach "
            "the Astrid-profile bootstrap before track.create/clip.add; "
            f"HTTP {responses[-1].status}: {responses[-1].body!r}"
        )
        page = client.list_timeline_commits(project, "film", limit=100)
        assert page["head"]["revision_id"] and page["head"]["publication_id"]
        assert len(page["items"]) == 1 and page["items"][0]["records"] is None

        for field, value in (
            ("config", {"clips": []}), ("canonical_document", {}),
            ("project_id", "foreign-project"), ("unknown", None),
        ):
            before = tuple(daemon.service.store.conn.iterdump())
            response = world.call(
                f"/api/runtime/v1/projects/{project}/timelines", "POST",
                headers={"Content-Type": "application/json", "Idempotency-Key": "reject-" + field},
                body=json.dumps({"timeline_id": "refused-" + field, field: value}).encode(),
            )
            assert response.status == 400, (
                "ordinary_http_create_timeline_body_is_closed: " + field, response.body,
            )
            assert tuple(daemon.service.store.conn.iterdump()) == before

        create_path = f"/api/runtime/v1/projects/{project}/timelines"
        create_body = b'{"timeline_id":"refused"}'
        create_headers = {"Content-Type": "application/json", "Idempotency-Key": "refused"}
        before = tuple(daemon.service.store.conn.iterdump())
        for origin in (None, "https://foreign.test"):
            response = world.call(create_path, "POST", origin=origin,
                                  headers=create_headers, body=create_body)
            assert response.status == 403, response.body
        response = world.call(create_path, "POST", body=create_body,
                              headers={"Content-Type": "application/json"})
        assert response.status == 400, response.body
        response = world.call(create_path, "POST", body=create_body,
                              headers={**create_headers, "Authorization": "Bearer browser"})
        assert response.status == 403, response.body
        assert tuple(daemon.service.store.conn.iterdump()) == before

        product_credential = json.loads(credential.read_text())
        readonly_token, _ = daemon.credentials.provision(
            "ordinary-readonly", ["handshake", "projects:read"],
        )
        try:
            write_owner_only(credential, {**product_credential, "actor_id": "ordinary-readonly",
                                          "token": readonly_token})
            response = world.call(create_path, "POST", headers=create_headers, body=create_body)
            assert response.status == 503, response.body
            assert response.json() == {"error": "runtime_identity_mismatch"}
            credential.unlink()
            response = world.call(create_path, "POST", headers=create_headers, body=create_body)
            assert response.status == 503, response.body
        finally:
            write_owner_only(credential, product_credential)
        assert tuple(daemon.service.store.conn.iterdump()) == before

        from astrid.core.timeline.authoring_bundle import open_authoring_bundle
        from astrid.sdk.timeline._clip_commands import capture_clip_add
        from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
        from astrid.sdk.timeline._command_state import equal
        from astrid.sdk.timeline._scalar_commands import capture_track_set
        from astrid.sdk.timeline.capture import capture_clip_delete, capture_track_create
        from astrid.sdk.timeline.commands import validate_command

        parent = client.get_project_parent_composition_revision(
            project, "film", page["head"]["revision_id"],
        )
        bundle = open_authoring_bundle(parent, shot_revisions=[], internal_timeline_revisions=[])
        assert bundle["parent"]["clips"] == []

        def history():
            return client.list_timeline_commits(project, "film", limit=100)

        def snapshot():
            return (tuple(daemon.service.store.conn.iterdump()),
                    {path.relative_to(daemon.service.cas.root): path.read_bytes()
                     for path in daemon.service.cas.root.rglob("*") if path.is_file()})

        def request(commands):
            head = client.list_timeline_commits(project, "film", limit=100)["head"]
            return {
                "api_version": 1, "project_id": project, "timeline_id": "film",
                "base_revision_id": head["revision_id"],
                "base_publication_id": head["publication_id"], "commands": commands,
            }

        def readback(accepted, commands):
            document = accepted["data"]["canonical_document"]
            assert accepted["receipt"]["result"] == accepted["data"]
            recorded_commands = accepted["data"]["commands"]
            assert len(recorded_commands) == len(commands)
            for supplied, recorded in zip(commands, recorded_commands):
                if supplied["op"] == "timeline.inverse":
                    assert {key: recorded[key] for key in supplied} == supplied
                else:
                    assert recorded == supplied
            assert document["project_id"] == project and document["timeline_id"] == "film"
            assert document["shot_revisions"] == document["internal_timeline_revisions"] == []
            assert document["dependency_manifest"] == parent["dependency_manifest"]
            stored = client.get_project_parent_composition_revision(
                project, "film", accepted["data"]["accepted_revision_id"],
            )
            assert {key: stored[key] for key in document["parent_revision"]} == document["parent_revision"]
            assert stored["dependency_manifest"] == document["dependency_manifest"]
            entry = next(item for item in history()["items"]
                         if item["publication_id"] == accepted["receipt"]["receipt_id"])
            assert entry["receipt"] == accepted["receipt"]
            assert entry["receipt"]["result"]["canonical_document"] == document
            assert entry["revision_id"] == accepted["data"]["accepted_revision_id"]
            assert entry["publisher"] == PRODUCT_ACTOR
            assert [record["command"] for record in entry["records"]["commands"]] == recorded_commands
            return document

        accepted_commits = {}

        def commit(commands, key):
            commands = commands if isinstance(commands, list) else [commands]
            for command in commands:
                if command["op"] != "timeline.inverse":
                    assert {"reads", "selections", "bindings", "created", "expect", "authorship"} <= command.keys()
            original = history()
            accepted = client.commit_timeline(project, "film", request(commands), idempotency_key=key)
            accepted_commits[key] = accepted
            current = history()
            assert current["items"][:-1] == original["items"]
            assert current["items"][-1]["previous"] == original["head"]
            assert current["head"] == {
                "revision_id": accepted["data"]["accepted_revision_id"],
                "publication_id": accepted["receipt"]["receipt_id"],
            }
            return readback(accepted, commands)

        def inverse(key):
            return {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
                    "args": {"publications": [accepted_commits[key]["receipt"]["receipt_id"]]}}

        track = {"id": "picture", "kind": "visual", "role": "output", "opaque": [None, False]}
        tracked = commit(capture_track_create(bundle, "parent", track), "track-create")
        assert tracked["parent_revision"]["payload"]["config"]["tracks"] == [track]
        row = {"id": "title", "clipType": "text", "track": "picture", "at": 0, "hold": 4,
               "params": {"text": "Ordinary HTTP"}, "opaque": [None, False, 0, {}, []]}
        created = commit(capture_clip_add(agent.bundle_from_document(tracked), "parent", row), "clip-add")
        assert created["parent_revision"]["payload"]["clips"] == [row]
        assert created["parent_revision"]["payload"]["config"]["clips"] == [row]
        held = commit(capture_clip_set(agent.bundle_from_document(created), "parent/clip:title",
                                       values={"hold": 3}), "hold-set")
        assert held["parent_revision"]["payload"]["clips"] == [{**row, "hold": 3}]

        # These are schema-valid operations, refused by the real semantic
        # provider. A literal hold has no surviving source window to clear;
        # trim/split need registry-backed parent media, not this text clip.
        refusals = [
            ("clip.set", "parent/clip:title", {"values": {}, "clear": ["hold"]},
             "unsupported_timing", "hold clear requires a surviving source window"),
            ("clip.trim", "parent/clip:title", {"in_s": 0, "out_s": 2},
             "invalid_edit_command", "clip.trim applies to media clips"),
            ("clip.split", "parent/clip:title", {"on": 1, "right_id": "title-right"},
             "invalid_edit_command", "clip.split v1 requires registry-backed media"),
        ]
        for changes, reason, message in (
            ({"clipType": "media"}, "unsupported_media", "clip.add v1 does not support media clips"),
            ({"asset": None}, "unsupported_media", "clip.add v1 does not support asset"),
            ({"from": 0, "to": 3}, "unsupported_timing", "clip.add v1 does not support from"),
        ):
            refusals.append(("clip.add", "parent", {"row": {**row, "id": "unsupported", **changes}},
                             reason, message))
        for index, (op, select, args, reason, message) in enumerate(refusals):
            command = {"schema_version": 1, "op": op, "version": "1", "select": select, "args": args}
            validate_command(command)
            original = history()
            body = request([command])
            before = snapshot()
            response = world.call(
                f"/api/runtime/v1/projects/{project}/timelines/film/commit", "POST",
                headers={"Content-Type": "application/json", "Idempotency-Key": f"unsupported-{index}"},
                body=json.dumps(body).encode(),
            )
            assert response.status == 409, response.body
            failure = response.json()
            assert failure["code"] == "conflict", failure
            assert failure["message"] == message
            assert failure["details"]["status"] == "refused"
            assert failure["details"]["reason"] == reason
            assert snapshot() == before
            assert history() == original

        other = {"id": "other", "kind": "visual", "role": "output", "label": "B",
                 "opaque": {"null": None, "ordered": [False, 0, [], {}]}}
        before_batch = commit(capture_track_create(agent.bundle_from_document(held), "parent", other),
                              "second-track")
        deleted = commit(capture_clip_delete(agent.bundle_from_document(before_batch), "parent/clip:title"),
                         "clip-delete")
        expected_deleted = copy.deepcopy(before_batch["parent_revision"]["payload"])
        expected_deleted["clips"] = expected_deleted["config"]["clips"] = []
        assert equal(deleted["parent_revision"]["payload"], expected_deleted)
        restored = commit(inverse("clip-delete"), "undo-clip-delete")
        assert equal(restored["parent_revision"]["payload"], before_batch["parent_revision"]["payload"])
        assert restored["parent_revision"]["content_digest"] == before_batch["parent_revision"]["content_digest"]
        assert history()["items"][-1]["records"]["undo_of"] == [
            accepted_commits["clip-delete"]["receipt"]["receipt_id"],
        ]
        before_batch = restored
        bundle = agent.bundle_from_document(before_batch)
        batch = [capture_clip_set(bundle, "parent/clip:title", values={"hold": 2}),
                 capture_track_set(bundle, "parent/track:picture", values={"label": "B"})]
        original = history()
        batch_request = request(batch)
        frozen_batch = copy.deepcopy(batch)
        lose_ack = True
        with pytest.raises(ApiError) as lost:
            client.commit_timeline(project, "film", batch_request, idempotency_key="scalar-label-batch")
        lose_ack = False
        assert lost.value.code == "transport_timeout"
        lost_response = responses[-1]
        assert lost_response.status == 200, lost_response.body
        accepted = lost_response.json()  # Server-side oracle; client received no ACK.
        accepted_commits["scalar-label-batch"] = accepted
        assert history()["items"][:-1] == original["items"]
        assert history()["items"][-1]["previous"] == original["head"]
        batched = readback(accepted, frozen_batch)
        expected_batch = copy.deepcopy(before_batch["parent_revision"]["payload"])
        expected_batch["config"]["tracks"][0]["label"] = "B"
        expected_batch["clips"][0]["hold"] = expected_batch["config"]["clips"][0]["hold"] = 2
        assert equal(batched["parent_revision"]["payload"], expected_batch)
        assert batch == frozen_batch

        newer_command = capture_track_set(agent.bundle_from_document(batched), "parent/track:other",
                                          values={"label": "C"})
        newer = commit(newer_command, "disjoint-label-C")
        expected_newer = copy.deepcopy(expected_batch)
        expected_newer["config"]["tracks"][1]["label"] = "C"
        assert equal(newer["parent_revision"]["payload"], expected_newer)
        original_history = history()
        old_instance = daemon.instance_id
        original_identity = identity
        world.stop()

        daemon = RuntimeDaemon(
            tmp_path / "realm", support_root=tmp_path / "support", authoring_profile="astrid",
            door=DoorConfig(origin=HOSTED, port=0, credential_file=credential),
        ).start()
        world = DoorWorld(tmp_path, daemon, credential)
        client = WorkspaceClient(daemon.door_endpoint, transport=transport)
        assert daemon.instance_id != old_instance
        assert client.health().schema_digest == SCHEMA_DIGEST
        identity = client.handshake("ordinary-http-restarted", "1", ["projects:read", "projects:write"])
        flight = json.loads(flight_file.read_text())
        assert flight["realm_id"] == identity.realm_id == original_identity.realm_id
        assert flight["actor_id"] == identity.actor_id == original_identity.actor_id == PRODUCT_ACTOR
        assert daemon.service._timeline_commit_provider.__class__ is agent.RuntimeCommitService
        assert daemon.service._timeline_commit_provider.contract_digest == SCHEMA_DIGEST
        assert flight["method"] == "POST"
        assert flight["path"] == f"/v1/projects/{project}/timelines/film/commit"
        assert flight["headers"]["Idempotency-Key"] == "scalar-label-batch"
        persisted_body = bytes.fromhex(flight["body_hex"])
        assert json.loads(persisted_body) == batch_request
        assert history() == original_history
        before = snapshot()
        with monkeypatch.context() as retry:
            retry.setattr(agent.RuntimeCommitService, "commit", forbidden)
            response = world.call("/api/runtime" + flight["path"], flight["method"],
                                  headers=flight["headers"], body=persisted_body)
        assert response.status == 200, response.body
        assert response.json() == accepted
        assert response.body == lost_response.body
        assert snapshot() == before
        assert history() == original_history
        assert readback(response.json(), frozen_batch) == batched
        assert readback(accepted_commits["disjoint-label-C"], [newer_command]) == newer

        changed = {**json.loads(persisted_body), "rationale": "changed flight"}
        response = world.call("/api/runtime" + flight["path"], flight["method"],
                              headers=flight["headers"], body=json.dumps(changed).encode())
        assert response.status == 409, response.body
        assert response.json()["details"]["reason"] == "idempotency_mismatch"
        assert snapshot() == before

        undone = commit(inverse("scalar-label-batch"), "undo-whole-batch")
        expected_undone = copy.deepcopy(before_batch["parent_revision"]["payload"])
        expected_undone["config"]["tracks"][1]["label"] = "C"
        assert equal(undone["parent_revision"]["payload"], expected_undone)
        assert history()["items"][-1]["records"]["undo_of"] == [
            accepted_commits["scalar-label-batch"]["receipt"]["receipt_id"],
        ]
        for result in accepted_commits.values():
            readback(result, result["data"]["commands"])
    finally:
        world.stop()
