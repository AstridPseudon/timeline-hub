"""Admitted legacy mirrors through the public API and disposable Runtime.

Uses the existing explicit synthetic scene answers; no native renderer, socket,
real media, or live store is involved. Runtime source is selected explicitly.
"""
from __future__ import annotations

import copy
import io
import json
import os
import sys
from email.message import Message
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.timeline.authoring_bundle import (
    AuthoringBundleError, compile_authoring_candidate, diff_authoring_candidate,
    open_authoring_bundle,
)
from astrid.core.timeline.shot_composition_projection import (
    ShotCompositionProjectionError, resolve_parent_tracks,
)
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline import store
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.workspace_client import WorkspaceClient
from banodoco_workspace_client import WorkspaceClient as GeneratedClient

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


def seed():
    tracks = [dict(id="track-film-001", kind="visual", label="Footage"),
              dict(id="track-caption-001", kind="visual", label="Captions")]
    internal = dict(tracks=copy.deepcopy(tracks), clips=[
        dict(id="film-clip", track="track-film-001", clipType="media", at=0, hold=1),
        dict(id="caption-clip", track="track-caption-001", clipType="media", at=0, hold=1),
    ], effects=[], audio=[], layout={}, registry={}, assets=[])
    shot = dict(metadata={}, items=[], pools=[], selected_variants={}, provenance={},
                generation_inputs={}, audio_bindings=[], text_bindings=[],
                internal_timeline_revision_id="legacy-internal")
    parent = dict(config=dict(tracks=tracks), clips=[], registry={}, occurrences=[
        dict(occurrence_id="film-occ", shot_id="film-shot", shot_revision_id="legacy-shot",
             at_ms=0, duration_ms=1000, source_offset=0, speed=1, track="track-film-001",
             transform={}, gain=1, muted=False, provenance={})])
    return dict(parent_composition=parent,
                shot_revisions=[dict(shot_id="film-shot", revision_id="legacy-shot",
                                     internal_timeline_revision_id="legacy-internal", payload=shot)],
                internal_timeline_revisions=[dict(timeline_id="inner", revision_id="legacy-internal", payload=internal)])


def label(value="Footage B", expected="Footage", track="track-film-001"):
    return dict(op="timeline.set", select="parent/track:" + track,
                args=dict(values=dict(label=value), clear=[]),
                expect=dict(label=dict(state="present", value=expected)))


def evidence(name, value):
    if root := os.environ.get("ASTRID_LEGACY_TRACK_EVIDENCE"):
        Path(root, name + ".json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


@pytest.fixture
def public(tmp_path, monkeypatch):
    source = os.environ.get("ASTRID_GRAPH_RUNTIME_ROOT")
    if not source:
        pytest.skip("explicit Runtime source required for coupled proof")
    # Older authoring tests load a historical Runtime in this same process.
    # Bind this fixture to its explicitly selected source, then restore those
    # modules so test order cannot silently select another Runtime version.
    previous = {k: v for k, v in sys.modules.items()
                if k == "runtime_protocol" or k.startswith("runtime_protocol.")}
    for key in previous:
        monkeypatch.delitem(sys.modules, key)
    monkeypatch.syspath_prepend(source)
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.paired_session import PairedSessionAuthority
    from runtime_protocol.server import RuntimeHandler
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol import authoring_scene as scene
    import runtime_protocol
    assert Path(runtime_protocol.__file__).resolve().is_relative_to(Path(source).resolve())
    RealmStore.initialize(tmp_path / "realm").close()
    service = RuntimeService(tmp_path / "realm")
    credentials = CredentialStore(tmp_path / "credentials")
    token, _ = credentials.provision("legacy-track-fixture", ["projects:read", "projects:write"])
    service._task_credentials = credentials

    # Reuse the established narration Runtime test seam. Request fencing and
    # atomic acceptance remain real; only the renderer binding/answers are
    # synthetic. No native owner or production renderer is started.
    class Relay:
        def __init__(self):
            from astrid.core.execution import authoring_scene_protocol as protocol
            self.config = SimpleNamespace(binding={
                key: (1 if key == "owner_generation" else "astrid-v1" if key == "provider_id"
                      else "sha256:" + "a" * 64 if key.endswith("digest") or key == "renderer_closure" else key)
                for key in protocol.CONTEXT_FIELDS
            })
            self.closed = False

        def check_live(self):
            assert not self.closed

        def exchange(self, request, *, guard, cancelled):
            from astrid.core.execution import authoring_scene_protocol as protocol
            guard()
            protocol.validate_request(request, self.config.binding)
            return [dict(frame=frame, layers=[], coverage="GAP", content=None, findings=[])
                    for frame in request["frames"]]

        def close(self):
            self.closed = True

    relay = service._authoring_scene_relay = Relay()
    from astrid.core.timeline import scene_answers
    synthetic_client = scene_answers._client
    monkeypatch.setattr(scene_answers, "_client", lambda: getattr(scene_answers._local, "client", None) or synthetic_client())
    monkeypatch.setattr(scene, "check_binding", lambda _service, relay: relay.check_live())
    server = SimpleNamespace(runtime=service, credentials=credentials,
                             accepting_authenticated_requests=True,
                             paired_sessions=PairedSessionAuthority(),
                             daemon_runtime=SimpleNamespace(instance_id="legacy-track-fixture"))
    traffic = []

    def transport(method, path, headers, body=None):
        handler = object.__new__(RuntimeHandler)
        handler.server, handler.command, handler.path, handler.headers = server, method, path, Message()
        for key, value in headers.items():
            handler.headers.add_header(key, value)
        payload = bytes(body or b"")
        if handler.headers.get("Content-Length") is None:
            handler.headers.add_header("Content-Length", str(len(payload)))
        handler.rfile = io.BytesIO(payload)
        reply = {}

        def send(status, value=None, **kwargs):
            raw = kwargs.get("body")
            if raw is None:
                raw = json.dumps(kwargs.get("error", value)).encode()
            reply.update(status=status, headers=kwargs.get("headers", {}), body=raw)

        handler._send = send
        try:
            handler._route()
        except RuntimeErrorBase as exc:
            send(exc.status, exc.as_dict())
        traffic.append(dict(method=method, path=path, request=json.loads(payload) if payload else None,
                            status=reply["status"], response=json.loads(reply["body"])))
        assert reply["status"] < 400, traffic[-1]
        return reply["status"], reply["headers"], reply["body"]

    client = WorkspaceClient("http://127.0.0.1:1", token)
    client._generated = GeneratedClient(client.endpoint, token, transport=transport)
    service.register_timeline_commit_provider(RuntimeCommitService())
    try:
        project = client.create_project("Synthetic legacy tracks", slug="legacy-tracks", idempotency_key="project")["data"]["project_id"]
        client.create_timeline(project, "film", idempotency_key="film")
        client.create_timeline(project, "inner", idempotency_key="inner")
        yield service, client, project, traffic
    finally:
        evidence("traffic-" + tmp_path.name, traffic)
        service.close()
        assert relay.closed
        for key in list(sys.modules):
            if key == "runtime_protocol" or key.startswith("runtime_protocol."):
                del sys.modules[key]
        sys.modules.update(previous)


def publish(public, value):
    _, client, project, _ = public
    return client.publish_parent_composition(project, "film", dict(
        value, project_id=project, timeline_id="film", expected_head=None,
        parent_revision_id="legacy-parent"), idempotency_key="seed")


def closure(public, revision="legacy-parent"):
    service, _, project, _ = public
    return service._commit_revision_closure(project, "film", revision)


def opened(public, revision="legacy-parent"):
    return open_authoring_bundle(**closure(public, revision))


def body(public, key, calls, *, base="legacy-parent", dry_run=False):
    service, _, project, _ = public
    return dict(api_version=1, project_id=project, timeline_id="film", request_id=key,
                session_id="legacy-track-session", session_sequence=1,
                base_revision_id=base, base_publication_id=service.head(project, "film")["publication_id"],
                scope=dict(target="parent", complete=[], projection_version=1),
                change=dict(commands=calls), source=dict(via="python"), dry_run=dry_run)


def test_public_legacy_label_noop_immutable_retry_undo_replay(public):
    original_seed = seed()
    publish(public, original_seed)
    original = closure(public)
    evidence("original-closure", original)
    before = opened(public)
    service, client, project, _ = public
    preview = client.commit_timeline(body(public, "preview", [label()], dry_run=True))
    evidence("first-label-preview", preview)
    assert preview["status"] == "preview", preview
    assert closure(public) == original
    assert before["base_parent_payload"]["config"]["tracks"] == original_seed["parent_composition"]["config"]["tracks"]
    assert before["shots"]["film-shot"]["base_internal_timeline"] == original_seed["internal_timeline_revisions"][0]["payload"]
    assert before["shots"]["film-shot"]["internal_timeline"]["tracks"] == []
    assert diff_authoring_candidate(before)["change_count"] == 0
    assert store.checkout_change_units(Checkout(copy.deepcopy(before)), complete=True) == (True, [])
    no_op_publication = compile_authoring_candidate(before).publication
    assert no_op_publication["parent_composition"] == original["parent_revision"]["payload"]
    assert no_op_publication["shot_revisions"] == no_op_publication["internal_timeline_revisions"] == []
    noop = client.commit_timeline(body(public, "noop", []))
    assert noop["status"] == "no_change", noop
    assert closure(public) == original
    request = body(public, "edit", [label()])
    result = client.commit_timeline(request)
    assert result["status"] == "accepted", result
    rid = result["accepted_revision_id"]
    accepted = closure(public, rid)
    assert accepted["parent_revision"]["payload"]["config"]["tracks"][0]["label"] == "Footage B"
    child = accepted["internal_timeline_revisions"][0]
    assert child["revision_id"] != "legacy-internal"
    assert child["payload"]["tracks"] == []
    assert child["payload"]["clips"] == original_seed["internal_timeline_revisions"][0]["payload"]["clips"]
    assert opened(public, rid)["parent"]["config"]["tracks"][0]["label"] == "Footage B"
    assert closure(public) == original
    assert client.commit_timeline(request) == result
    assert len(service.revisions(project, "film", {})) == 1  # one command publication, including retry
    assert len(service.list_project_parent_composition_revisions(project, "film", limit=200)["items"]) == 2
    after = opened(public, rid)
    inverse = inverse_command(result["change"]["commands"], before, after, result["accepted_publication_id"])
    undo = client.commit_timeline(body(public, "undo", [inverse], base=rid))
    assert undo["status"] == "accepted", undo
    restored = opened(public, undo["accepted_revision_id"])
    assert restored["parent"]["config"]["tracks"] == before["parent"]["config"]["tracks"]
    replayed = rebase(result["change"]["commands"], restored)
    assert not replayed.conflicts
    assert replayed.document["parent"]["config"]["tracks"] == after["parent"]["config"]["tracks"]
    newer = client.commit_timeline(body(public, "newer", [label("newer")], base=undo["accepted_revision_id"]))
    assert newer["status"] == "accepted", newer
    head = service.head(project, "film")
    guarded = client.commit_timeline(body(public, "stale-undo", [inverse], base=newer["accepted_revision_id"]))
    assert guarded["status"] == "refused", guarded
    assert "same-property" in guarded["error"]["message"]
    assert guarded["accepted_revision_id"] is None
    assert service.head(project, "film") == head
    assert closure(public) == original
    evidence("positive", dict(noop=noop, preview=preview, result=result, accepted=accepted, undo=undo,
                              newer=newer, guarded=guarded))


def test_public_disjoint_metadata_and_moved_head_rebase(public):
    value = seed()
    value["parent_composition"]["config"]["tracks"][0]["app"] = dict(parentOpaque=[True, None])
    value["internal_timeline_revisions"][0]["payload"]["tracks"][0]["app"] = dict(
        scaleAppliesToPositionedClips={"opaque": [False, 1, None]}, childOpaque="keep")
    publish(public, value)
    before = opened(public)
    merged = before["parent"]["config"]["tracks"][0]["app"]
    assert merged == dict(parentOpaque=[True, None], scaleAppliesToPositionedClips={"opaque": [False, 1, None]}, childOpaque="keep")
    assert diff_authoring_candidate(before)["change_count"] == 0
    assert compile_authoring_candidate(before).publication["parent_composition"] == closure(public)["parent_revision"]["payload"]
    _, client, _, _ = public
    pending = body(public, "pending", [label()])
    other = client.commit_timeline(body(public, "other", [label("Captions B", "Captions", "track-caption-001")]))
    assert other["status"] == "accepted", other
    result = client.commit_timeline(pending)
    assert result["status"] == "accepted", result
    assert result["rebased_onto"] == other["accepted_revision_id"]
    fresh = opened(public, result["accepted_revision_id"])
    assert fresh["parent"]["config"]["tracks"][0]["app"] == merged
    assert fresh["shots"]["film-shot"]["internal_timeline"]["tracks"] == []
    conflict = client.commit_timeline(body(public, "stale", [label("stale")]))
    assert conflict["status"] == "conflict", conflict
    evidence("metadata-rebase", dict(result=result, other=other, conflict=conflict, fresh=fresh))


@pytest.mark.parametrize("bad", ["label", "app", "ambiguous"])
def test_initial_conflict_refuses_without_effect(public, bad):
    value = seed()
    parent = value["parent_composition"]
    child = value["internal_timeline_revisions"][0]["payload"]
    if bad == "label":
        child["tracks"][0]["label"] = "different"
    elif bad == "app":
        parent["config"]["tracks"][0]["app"] = dict(scaleAppliesToPositionedClips=True)
        child["tracks"][0]["app"] = dict(scaleAppliesToPositionedClips=False)
    else:
        parent["tracks"] = copy.deepcopy(parent["config"]["tracks"])
    publish(public, value)
    immutable = closure(public)
    service, client, project, _ = public
    head = service.head(project, "film")
    with pytest.raises((AuthoringBundleError, ShotCompositionProjectionError)):
        opened(public)
    result = client.commit_timeline(body(public, "refuse-" + bad, [label()]))
    assert result["status"] == "refused", result
    assert result["accepted_revision_id"] is None
    assert service.head(project, "film") == head
    assert closure(public) == immutable
    if bad != "ambiguous":
        with pytest.raises(ShotCompositionProjectionError):
            resolve_parent_tracks(parent, [child])
    evidence("initial-" + bad, dict(closure=immutable, result=result))
