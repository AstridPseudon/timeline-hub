"""Existing parent media through normal Astrid startup and the generated door client.

The neutral public publisher constructs the pre-existing film before tripwires.
This deliberately makes no claim about creating media from an empty timeline.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid_runtime_client import ApiError, CONTRACT_VERSION, WorkspaceClient
from astrid_runtime_client.contract_metadata import SCHEMA_DIGEST as CLIENT_SCHEMA_DIGEST
from runtime_protocol.contract_metadata import SCHEMA_DIGEST
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.door import DoorConfig
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from tests.door_helpers import HOSTED, PRODUCT_ACTOR, DoorWorld

pytestmark = pytest.mark.integration
TARGET = "parent/clip:picture"
RIGHT = "picture-right"


def seed_film(tmp_path, variant):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "parent-media", "name": "Existing film"})["id"]
        service.create_timeline(project, "film", idempotency_key="seed-timeline")
        media = {}
        for name, inputs, codec, suffix, mime, kind in (
            ("picture", ["color=c=blue:s=16x16:r=24"],
             ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p"], ".mp4", "video/mp4", "video"),
            ("bed", ["sine=frequency=440:sample_rate=8000"],
             ["-vn", "-c:a", "pcm_s16le"], ".wav", "audio/wav", "audio"),
        ):
            path = tmp_path / (name + suffix)
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", inputs[0],
                            "-t", "8", *codec, str(path)], check=True)
            probe = json.loads(subprocess.run(
                ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                check=True, capture_output=True, text=True,
            ).stdout)
            assert float(probe["format"]["duration"]) == 8
            assert probe["streams"][0]["codec_type"] == kind
            if kind == "video":
                assert probe["streams"][0]["r_frame_rate"] == "24/1"
            data = path.read_bytes()
            identity = service.ingest(project, data, media_type=mime, original_name=path.name,
                                      idempotency_key="seed-" + name)["data"]["object_id"]
            assert identity == "sha256:" + hashlib.sha256(data).hexdigest()
            assert service.cas.read(identity.removeprefix("sha256:")) == data
            media[name] = (identity, data)
            path.unlink()
        target = {"id": "picture", "clipType": "media", "asset": "picture", "track": "picture",
                  "at": 1, "from": 1, "to": 5, "hold": 4, "speed": 1,
                  "params": None, "opaque": {"nested": [None, False, 0, {}, []]}}
        if variant == "intent":
            target["app"] = {"astrid": {"until": "end"}}
        elif variant == "effect":
            target["effects"] = [{"id": "fade", "type": "fade", "params": {"duration": .25}}]
        clips = [target,
                 {"id": "bed", "clipType": "audio", "asset": "bed", "track": "music",
                  "at": 0, "from": 0, "to": 8, "hold": 8, "speed": 1, "volume": .65,
                  "effects": [{"id": "bed-fade", "type": "fade", "params": {"duration": .25}}],
                  "opaque": {"null": None}},
                 {"id": "title", "clipType": "text", "track": "titles", "at": 6, "hold": 1,
                  "params": {"text": "Keep me"}, "opaque": [None, False, {"literal": RIGHT}]}]
        payload = {
            "config": {"output": {"fps": 24}, "tracks": [
                {"id": "picture", "kind": "visual", "role": "output"},
                {"id": "music", "kind": "audio", "label": "Original bed"},
                {"id": "titles", "kind": "visual"}], "clips": copy.deepcopy(clips),
                "opaque": {"null": None, "values": [False, 0, {}, []]}},
            "registry": {"assets": {
                name: {"media_id": media[name][0], "type": kind, "duration": 8,
                       "opaque": {"null": None}}
                for name, kind in (("picture", "video"), ("bed", "audio"))}, "opaque": None},
            "clips": clips, "occurrences": [], "opaque": {"keep": [None, False]},
        }
        published = service.publish_parent_composition(project, "film", {
            "project_id": project, "timeline_id": "film", "expected_head": None,
            "parent_revision_id": "existing-parent-media", "parent_composition": payload,
        }, idempotency_key="seed-existing-film")
        assert published["data"]["payload"] == payload
        return SimpleNamespace(root=root, project=project, media=media, payload=payload,
                               realm=service.store.realm["id"])
    finally:
        service.close()


@pytest.fixture
def film(tmp_path, monkeypatch, astrid_importable, request):
    assert subprocess.check_output(
        ["git", "-C", str(astrid_importable), "rev-parse", "HEAD"], text=True,
    ).strip() == "f423074778f4220df808799a4f7b308e56885397"
    assert not subprocess.check_output(
        ["git", "-C", str(astrid_importable), "status", "--porcelain"], text=True,
    ).strip(), "the leased Agent source must be exactly f423"
    seeded = seed_film(tmp_path, getattr(request, "param", None))

    def forbidden(*args, **kwargs):
        raise AssertionError("existing-media edit called a legacy writer or evaluator")

    class RendererStopped:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(("astrid.packs.rendering", "astrid.core.rendering",
                                    "astrid.sdk.authoring_render_preview",
                                    "astrid.core.timeline.compatibility", "composition", "remotion")) or "scene" in fullname:
                raise AssertionError("existing-media edit imported renderer: " + fullname)

    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam

    monkeypatch.setattr(sys, "meta_path", [RendererStopped(), *sys.meta_path])
    monkeypatch.setattr(service_module, "evaluate_closure", forbidden)
    monkeypatch.setattr(visual_seam, "evaluate_closure", forbidden)
    for name in (
        "publish_parent_composition", "replace_parent_composition_media", "replace_timeline_clip",
        "update_timeline", "create_timeline_document", "create_document", "update_document",
        "create_project_shot", "update_project_shot", "create_shot", "update_shot",
        "publish_timeline_render", "_publication_replay_result",
    ):
        monkeypatch.setattr(RuntimeService, name, forbidden)

    from astrid.sdk.timeline import commit as agent

    assert Path(agent.__file__).resolve().is_relative_to(astrid_importable)
    assert CONTRACT_VERSION == "0.2.3" and CLIENT_SCHEMA_DIGEST == SCHEMA_DIGEST
    metadata = (astrid_importable / "astrid_runtime_client" / "contract_metadata.py").read_text()
    assert f"SCHEMA_DIGEST = {SCHEMA_DIGEST!r}" in metadata
    assert f"CONTRACT_VERSION = {CONTRACT_VERSION!r}" in metadata
    case = ParentMediaDoor(tmp_path, seeded, agent)
    try:
        case.start()
        yield case
    finally:
        case.world.stop()


class ParentMediaDoor:
    def __init__(self, tmp, seed, agent):
        self.tmp, self.seed, self.agent = tmp, seed, agent
        self.flight = None
        self.lose_ack = False

    def start(self):
        credential = self.tmp / "product.json"
        daemon = RuntimeDaemon(
            self.seed.root, support_root=self.tmp / "support", authoring_profile="astrid",
            door=DoorConfig(origin=HOSTED, port=0, credential_file=credential),
        ).start()
        self.world = DoorWorld(self.tmp, daemon, credential)
        if not credential.exists():
            self.world.provision()
        self.client = WorkspaceClient(daemon.door_endpoint, transport=self.transport)
        identity = self.client.handshake("parent-media-http", "1", ["projects:read", "projects:write"])
        assert identity.actor_id == PRODUCT_ACTOR and identity.realm_id == self.seed.realm
        assert {"projects:read", "projects:write"} <= set(identity.scopes)
        assert identity.schema_digest == SCHEMA_DIGEST
        assert type(daemon.service._timeline_commit_provider) is self.agent.RuntimeCommitService
        assert daemon.service._timeline_commit_provider.contract_digest == SCHEMA_DIGEST

    def transport(self, method, path, headers, body):
        response = self.world.call("/api/runtime" + path, method, headers=headers, body=body)
        if method == "POST" and path.endswith("/commit"):
            self.flight = (method, path, copy.deepcopy(headers), body, response)
            if self.lose_ack:
                self.lose_ack = False
                assert response.status == 200, response.body
                raise TimeoutError("lost durable acknowledgement")
        return response.status, response.headers, response.body

    def history(self):
        return self.client.list_timeline_commits(self.seed.project, "film", limit=100)

    def parent(self, revision=None):
        return self.client.get_project_parent_composition_revision(
            self.seed.project, "film", revision or self.history()["head"]["revision_id"])

    def bundle(self):
        from astrid.core.timeline.authoring_bundle import open_authoring_bundle

        return open_authoring_bundle(self.parent(), shot_revisions=[], internal_timeline_revisions=[])

    def body(self, commands):
        head = self.history()["head"]
        return {"api_version": 1, "project_id": self.seed.project, "timeline_id": "film",
                "base_revision_id": head["revision_id"], "base_publication_id": head["publication_id"],
                "commands": commands, "source": {"via": "python"}}

    def submit(self, body, key):
        return self.client.commit_timeline(self.seed.project, "film", body, idempotency_key=key)

    def undo(self, accepted, key):
        command = {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
                   "args": {"publications": [accepted["receipt"]["receipt_id"]]}}
        return self.submit(self.body([command]), key)

    def rows(self):
        return tuple(self.world.daemon.service.store.conn.iterdump())

    def assert_accepted(self, accepted, expected):
        data, receipt = accepted["data"], accepted["receipt"]
        document = data["canonical_document"]
        assert receipt["result"] == data
        assert data["publisher"] == PRODUCT_ACTOR
        assert document["project_id"] == self.seed.project and document["timeline_id"] == "film"
        assert document["parent_revision"]["payload"] == expected
        stored = self.parent(data["accepted_revision_id"])
        assert {key: stored[key] for key in document["parent_revision"]} == document["parent_revision"]
        assert document["shot_revisions"] == document["internal_timeline_revisions"] == []
        assert document["dependency_manifest"] == stored["dependency_manifest"] == self.manifest
        assert self.agent.bundle_from_document(document)["parent"]["clips"] == expected["clips"]
        for identity, original in self.seed.media.values():
            assert self.client.get_object(identity).data == original
            assert "sha256:" + hashlib.sha256(original).hexdigest() == identity


def replace_target(payload, target, right=None):
    expected = copy.deepcopy(payload)
    expected["clips"][:1] = [target] if right is None else [target, right]
    expected["config"]["clips"] = copy.deepcopy(expected["clips"])
    return expected


def test_existing_parent_media_clear_trim_split_retry_inverse_and_retired_id(film, monkeypatch):
    from astrid.core.timeline.duration import clip_end_frame, clip_start_frame
    from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
    from astrid.sdk.timeline._scalar_commands import capture_track_set
    from astrid.sdk.timeline._split_commands import capture_clip_split
    from astrid.sdk.timeline._trim_commands import capture_clip_trim

    initial = film.parent()
    assert initial["payload"] == film.seed.payload
    film.manifest = initial["dependency_manifest"]
    assert {pin["media_id"] for pin in film.manifest["media"]} == {
        identity for identity, _ in film.seed.media.values()}
    baseline = film.history()["items"]
    assert baseline and all(entry["records"] is None for entry in baseline)
    command = capture_clip_set(film.bundle(), TARGET, clear=["hold"])
    body = film.body([command])
    path = f"/api/runtime/v1/projects/{film.seed.project}/timelines/film/commit"
    headers = {"Content-Type": "application/json", "Idempotency-Key": "refused-scope"}
    before = film.rows()
    for options in ({"origin": None}, {"origin": "https://foreign.test"},
                    {"headers": {**headers, "Authorization": "Bearer browser"}}):
        response = film.world.call(path, "POST", body=json.dumps(body).encode(),
                                   **{"headers": headers, **options})
        assert response.status == 403, response.body
    foreign = {**body, "project_id": "foreign-project"}
    with pytest.raises(ApiError) as scope:
        film.submit(foreign, "wrong-project")
    assert scope.value.status in (400, 409)
    assert film.rows() == before

    def edit(command, key, expected):
        frozen = copy.deepcopy(command)
        assert {"reads", "selections", "bindings", "created", "expect", "authorship"} <= command.keys()
        accepted = film.submit(film.body([command]), key)
        assert command == frozen
        assert film.history()["items"][-1]["records"]["commands"][0]["command"] == frozen
        film.assert_accepted(accepted, expected)
        return accepted

    cleared_row = copy.deepcopy(initial["payload"]["clips"][0])
    cleared_row.pop("hold")
    cleared = replace_target(initial["payload"], cleared_row)
    clear = edit(command, "clear-hold", cleared)
    clear_undo = film.undo(clear, "undo-clear")
    film.assert_accepted(clear_undo, initial["payload"])
    film.assert_accepted(film.undo(clear_undo, "redo-clear"), cleared)
    row = film.bundle()["parent"]["clips"][0]
    assert (clip_start_frame(row, 24), clip_end_frame(row, 24)) == (24, 120)

    trimmed_row = {**cleared_row, "from": 2, "to": 6, "hold": 4}
    trimmed = replace_target(cleared, trimmed_row)
    trim = edit(capture_clip_trim(film.bundle(), TARGET, in_s=2, out_s=6), "trim", trimmed)
    trim_undo = film.undo(trim, "undo-trim")
    film.assert_accepted(trim_undo, cleared)
    film.assert_accepted(film.undo(trim_undo, "redo-trim"), trimmed)
    row = film.bundle()["parent"]["clips"][0]
    assert (clip_start_frame(row, 24), clip_end_frame(row, 24)) == (24, 120)

    left = {**trimmed_row, "to": 4, "hold": 2}
    right = {**trimmed_row, "id": RIGHT, "at": 3, "from": 4, "hold": 2}
    split = replace_target(trimmed, left, right)
    command = capture_clip_split(film.bundle(), TARGET, on=3, right_id=RIGHT)
    assert command["created"] == ["parent/clip:" + RIGHT]
    body = film.body([command])
    frozen = copy.deepcopy(body)
    film.lose_ack = True
    with pytest.raises(ApiError) as lost:
        film.submit(body, "split-lost-ack")
    assert lost.value.code == "transport_timeout"
    flight = film.flight
    accepted = flight[-1].json()
    film.assert_accepted(accepted, split)
    assert body == frozen
    assert (clip_start_frame(left, 24), clip_end_frame(left, 24),
            clip_start_frame(right, 24), clip_end_frame(right, 24)) == (24, 72, 72, 120)
    assert clip_end_frame(trimmed_row, 24) == 120

    labelled = copy.deepcopy(split)
    labelled["config"]["tracks"][1]["label"] = "C survives undo"
    edit(capture_track_set(film.bundle(), "parent/track:music", values={"label": "C survives undo"}),
         "intervening-C", labelled)
    history = copy.deepcopy(film.history())
    instance = film.world.daemon.instance_id
    film.world.stop()
    film.start()
    assert film.world.daemon.instance_id != instance
    before = film.rows()

    def forbidden(*args, **kwargs):
        raise AssertionError("durable exact retry executed the semantic provider")

    with monkeypatch.context() as retry:
        retry.setattr(type(film.world.daemon.service._timeline_commit_provider), "commit", forbidden)
        replay = film.submit(body, "split-lost-ack")
    assert replay == accepted
    assert film.flight[0:2] == flight[0:2] and film.flight[3] == flight[3]
    assert film.flight[2]["Idempotency-Key"] == flight[2]["Idempotency-Key"]
    assert body == frozen
    assert film.rows() == before and film.history() == history
    film.assert_accepted(replay, split)
    changed = copy.deepcopy(body)
    changed["rationale"] = "changed retry body"
    with pytest.raises(ApiError) as mismatch:
        film.submit(changed, "split-lost-ack")
    assert mismatch.value.status == 409
    assert film.rows() == before

    restored = copy.deepcopy(trimmed)
    restored["config"]["tracks"][1]["label"] = "C survives undo"
    undone = film.undo(accepted, "undo-split")
    film.assert_accepted(undone, restored)
    assert film.history()["items"][:-1] == history["items"]
    before = film.rows()
    reuse = capture_clip_split(film.bundle(), TARGET, on=3, right_id=RIGHT)
    with pytest.raises(ApiError) as collision:
        film.submit(film.body([reuse]), "ordinary-retired-id-reuse")
    assert collision.value.status == 409
    assert "identity_collision" in json.dumps(collision.value.details)
    assert film.rows() == before
    redone = film.undo(undone, "trusted-redo-split")
    film.assert_accepted(redone, labelled)
    assert film.history()["items"][-1]["records"]["undo_of"] == [undone["receipt"]["receipt_id"]]
    assert film.history()["items"][:len(baseline)] == baseline


@pytest.mark.parametrize("film,op,args,message", [
    ("intent", "clip.trim", {"in_s": 2, "out_s": 6}, "does not support until"),
    ("effect", "clip.split", {"on": 3, "right_id": RIGHT}, "does not support effects"),
], indirect=["film"])
def test_existing_parent_media_outside_bounded_recipe_refuses_without_writes(film, op, args, message):
    from astrid.sdk.timeline._command_state import CommandError
    from astrid.sdk.timeline._split_commands import capture_clip_split
    from astrid.sdk.timeline._trim_commands import capture_clip_trim

    before = film.rows()
    bundle = film.bundle()
    original = copy.deepcopy(bundle)
    capture = capture_clip_trim if op == "clip.trim" else capture_clip_split
    with pytest.raises(CommandError, match=message):
        capture(bundle, TARGET, **args)
    assert bundle == original and film.rows() == before
    command = {"schema_version": 1, "op": op, "version": "1", "select": TARGET, "args": args}
    with pytest.raises(ApiError) as refused:
        film.submit(film.body([command]), "unsupported-" + op)
    assert refused.value.status in (400, 409)
    assert message in str(refused.value) or message in json.dumps(refused.value.details)
    assert film.rows() == before
