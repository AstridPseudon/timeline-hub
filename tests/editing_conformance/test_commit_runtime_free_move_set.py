"""Authenticated Runtime acceptance for the reviewed free multi-clip move.

The offline recipe golden proves the recorder. These cases prove that the
same sealed commands cross the real Runtime door, survive its durable retry
boundary, and retain the guarded rebase/inverse semantics after reload.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._move_set import capture_move_set
from astrid.sdk.timeline.capture import capture_move, capture_track_create
from astrid.sdk.timeline.commands import execute
from tests.editing_conformance.test_commit_runtime_m1 import open_client
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration

TIMELINE = "film"
MEMBERS = [
    {"clip": "parent/clip:clip-2", "track": "parent/track:V3"},
    {"clip": "parent/clip:clip-1", "track": "parent/track:V2"},
]


@pytest.fixture
def lost_ack(monkeypatch):
    """Drop one HTTP response after Runtime has durably accepted it."""

    use_runtime()
    from runtime_protocol.server import RuntimeHandler

    original = RuntimeHandler._send
    observed = []
    lose = set()

    def send(handler, status, payload=None, **kwargs):
        if (handler.command == "POST" and handler.path.endswith("/commit")
                and getattr(handler, "_defer_response", False)):
            key = handler.headers["Idempotency-Key"]
            observed.append({
                "path": handler.path,
                "key": key,
                "body": handler._prefetched_body,
                "status": status,
                "response": copy.deepcopy(payload),
            })
            if status == 200 and key in lose:
                lose.remove(key)
                raise ConnectionError("injected lost ACK after durable acceptance")
        return original(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, "_send", send)
    return observed, lose


def _bundle(client, project):
    result = client.timelines.open_bundle(project, TIMELINE)
    assert result.ok, result.as_dict()
    return result.data["bundle"]


def _history(client, project):
    result = client.timelines.history(project, TIMELINE, limit=100)
    assert result.ok, result.as_dict()
    return result.data


def _commit(client, project, commands, key, *, base=None):
    head = base or _history(client, project)["head"]
    body = {
        "api_version": 1,
        "project_id": project,
        "timeline_id": TIMELINE,
        "base_revision_id": head["revision_id"],
        "base_publication_id": head["publication_id"],
        "commands": copy.deepcopy(commands),
    }
    result = client.timelines.commit(project, TIMELINE, body, idempotency_key=key)
    return result, body


def _row(clip_id, track, at, *, hold=2):
    return {
        "id": clip_id,
        "clipType": "hold",
        "track": track,
        "at": at,
        "hold": hold,
        "opaque": {"literal": clip_id, "ordered": [None, False, {}, []]},
        "app": {"future": {"keep": None}, "astrid": {"opaque": [clip_id, None]}},
    }


def _seed(real_runtime, *, include_v3=False, include_other=False):
    """Create a normal Runtime project and seed through registered commands."""

    daemon = real_runtime(authoring_profile="astrid")
    project = daemon.service.create_project({"slug": "free-move", "name": "Free move"})["id"]
    daemon.service.create_timeline(project, TIMELINE, idempotency_key="create-film")
    client = open_client(daemon)

    tracks = [{"id": "V1", "kind": "visual"}, {"id": "V2", "kind": "visual"}]
    if include_v3:
        tracks.append({"id": "V3", "kind": "visual"})
    staged = _bundle(client, project)
    track_commands = []
    for row in tracks:
        command = capture_track_create(staged, "parent", row)
        track_commands.append(command)
        staged = execute(staged, [command]).bundle
    result, _ = _commit(client, project, track_commands, "seed-tracks")
    assert result.ok, result.as_dict()

    rows = [_row("clip-1", "V1", 0), _row("clip-2", "V2", 2)]
    if include_other:
        rows.append(_row("clip-other", "V1", 10, hold=1))
    staged = _bundle(client, project)
    clip_commands = []
    for row in rows:
        command = capture_clip_add(staged, "parent", row)
        clip_commands.append(command)
        staged = execute(staged, [command]).bundle
    result, _ = _commit(client, project, clip_commands, "seed-clips")
    assert result.ok, result.as_dict()
    return daemon, client, project


def _assert_geometry(document, *, moved):
    parent = document["parent_revision"]["payload"]
    by_id = {row["id"]: row for row in parent["clips"]}
    expected = {
        "clip-1": {"track": "V2", "at": 1},
        "clip-2": {"track": "V3", "at": 3},
    } if moved else {
        "clip-1": {"track": "V1", "at": 0},
        "clip-2": {"track": "V2", "at": 2},
    }
    for clip_id, values in expected.items():
        assert {key: by_id[clip_id][key] for key in values} == values
        assert by_id[clip_id]["hold"] == 2
        assert by_id[clip_id]["opaque"] == {
            "literal": clip_id, "ordered": [None, False, {}, []]
        }
        expected_app = {
            "future": {"keep": None}, "astrid": {"opaque": [clip_id, None]}
        }
        if moved:
            expected_app["astrid"].update(fixed_start=True, **{"for": 2.0})
        assert by_id[clip_id]["app"] == expected_app
    track_ids = [row["id"] for row in parent["config"]["tracks"]]
    assert track_ids == (["V1", "V2", "V3"] if moved else ["V1", "V2"])
    assert "pinnedShotGroups" not in parent["config"]


def _reload(client, project, accepted):
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle

    document = accepted["data"]["canonical_document"]
    revision = accepted["data"]["accepted_revision_id"]
    stored = client._remote._transport.get_project_parent_composition_revision(
        project, TIMELINE, revision,
    )
    assert stored["project_id"] == project
    assert stored["timeline_id"] == TIMELINE
    for key, value in document["parent_revision"].items():
        assert stored[key] == value
    assert stored["dependency_manifest"] == document["dependency_manifest"]
    opened = client.timelines.open_bundle(project, TIMELINE, revision_id=revision)
    assert opened.ok, opened.as_dict()
    assert opened.data["revision_id"] == revision
    expected = open_authoring_bundle(
        {**document["parent_revision"], "project_id": project, "timeline_id": TIMELINE},
        shot_revisions=[
            {**row, "project_id": project} for row in document["shot_revisions"]
        ],
        internal_timeline_revisions=[
            {**row, "project_id": project}
            for row in document["internal_timeline_revisions"]
        ],
    )
    assert opened.data["bundle"] == expected
    return document


def _free_move_commands(session):
    def track(state):
        command = capture_track_create(session._bundle(state), "parent", {
            "id": "V3", "kind": "visual",
        })
        command["group_id"] = "free-drag-1"
        return command

    create = session._queue(track)

    def move(state):
        command = capture_move_set(
            session._bundle(state), MEMBERS, "parent/clip:clip-2", 3,
        )
        command["group_id"] = "free-drag-1"
        return command

    move_command = session._queue(move)
    return create, move_command


def test_free_move_runtime_lost_ack_restart_reload_undo_redo_and_exact_history(
    tmp_path: Path, real_runtime, lost_ack,
):
    use_runtime()
    from astrid.sdk.timeline.sync import TimelineSession
    from astrid.sdk.workspace_client import WorkspaceClientError

    daemon, client, project = _seed(real_runtime)
    baseline = _history(client, project)
    outbox = tmp_path / "free-move-outbox.json"
    session = TimelineSession.open(project, TIMELINE, client=client, outbox_path=outbox)
    create, move = _free_move_commands(session)
    assert create["op"] == "track.create"
    assert move["op"] == "clip.move-set"
    assert move["args"]["members"] == MEMBERS
    assert move["args"]["anchor"] == "parent/clip:clip-2"
    assert move["args"]["on"] == 3

    observed, lose = lost_ack
    lose.add("free-move-flight")
    with pytest.raises(WorkspaceClientError):
        session.flush(idempotency_key="free-move-flight")
    first_wire = copy.deepcopy(observed[-1])
    assert json.loads(first_wire["body"])["commands"] == [create, move]
    persisted = json.loads(outbox.read_text())
    assert persisted["flight"]["key"] == first_wire["key"]
    assert persisted["flight"]["body"].encode() == first_wire["body"]
    accepted = first_wire["response"]
    publication = accepted["receipt"]["receipt_id"]
    assert len(_history(client, project)["items"]) == len(baseline["items"]) + 1

    port = daemon.httpd.server_port
    instance = daemon.instance_id
    daemon.stop()
    daemon = real_runtime(
        daemon.root, support_root=tmp_path / "support", port=port,
        authoring_profile="astrid",
    )
    assert daemon.instance_id != instance
    client = open_client(daemon)
    session = TimelineSession.open(project, TIMELINE, client=client, outbox_path=outbox)
    assert json.loads(outbox.read_text())["flight"]["body"].encode() == first_wire["body"]
    before_retry = _history(client, project)
    retried = session.flush()
    assert retried["receipt"] == accepted["receipt"]
    assert _history(client, project) == before_retry
    document = _reload(client, project, retried)
    _assert_geometry(document, moved=True)
    final_entry = _history(client, project)["items"][-1]
    assert final_entry["publication_id"] == publication
    assert [record["command"] for record in final_entry["records"]["commands"]] == [create, move]
    assert final_entry["records"]["commands"][0]["created"] == [
        {"ref": "parent/track:V3", "kind": "track", "owner": "parent"}
    ]

    reloaded = TimelineSession.open(
        project, TIMELINE, client=client, outbox_path=tmp_path / "reload-outbox.json",
    )
    undone = reloaded.undo([publication])
    undo_document = _reload(client, project, undone)
    _assert_geometry(undo_document, moved=False)
    undo_entry = _history(client, project)["items"][-1]
    assert undo_entry["records"]["undo_of"] == [publication]
    assert any(
        write["ref"] == "parent/clip:clip-1"
        for write in undo_entry["records"]["commands"][0]["writes"]
    )
    assert any(
        write["ref"] == "parent/track:V3"
        for write in undo_entry["records"]["commands"][0]["writes"]
    )
    undo_refs = [write["ref"] for write in undo_entry["records"]["commands"][0]["writes"]]
    assert undo_refs[-1] == "parent/track:V3"

    redone = reloaded.undo([undo_entry["publication_id"]])
    redo_document = _reload(client, project, redone)
    _assert_geometry(redo_document, moved=True)
    redo_entry = _history(client, project)["items"][-1]
    assert redo_entry["records"]["undo_of"] == [undo_entry["publication_id"]]
    assert {item["ref"] for item in redo_entry["records"]["commands"][0]["created"]} >= {
        "parent/track:V3",
    }


def test_free_move_runtime_later_dependent_refuses_undo_without_history_change(
    tmp_path: Path, real_runtime,
):
    use_runtime()
    from astrid.sdk.timeline.sync import TimelineSession, CommitConflict

    _, client, project = _seed(real_runtime)
    session = TimelineSession.open(project, TIMELINE, client=client, outbox_path=tmp_path / "outbox.json")
    _, _ = _free_move_commands(session)
    accepted = session.flush()
    publication = accepted["receipt"]["receipt_id"]
    before = _history(client, project)

    bundle = _bundle(client, project)
    dependent = capture_clip_add(bundle, "parent", _row("dependent", "V3", 8))
    result, _ = _commit(client, project, [dependent], "dependent-clip")
    assert result.ok, result.as_dict()
    dependent_head = _history(client, project)
    reloaded = TimelineSession.open(
        project, TIMELINE, client=client, outbox_path=tmp_path / "undo.json",
    )
    with pytest.raises(CommitConflict) as error:
        reloaded.undo([publication])
    # The later accepted clip is an intervening guarded collection write. The
    # Runtime refuses before inverse staging, which is the safe refusal path.
    assert error.value.failure["details"]["reason"] == "intervening_write"
    assert _history(client, project) == dependent_head
    assert before["items"][-1]["publication_id"] == publication


@pytest.mark.parametrize("intervening", ["disjoint", "lane-entry-aba"])
def test_free_move_runtime_rebases_disjoint_lane_and_refuses_relevant_lane_aba(
    tmp_path: Path, real_runtime, intervening,
):
    use_runtime()
    _, client, project = _seed(real_runtime, include_v3=True, include_other=True)
    base = _history(client, project)["head"]
    plan_bundle = _bundle(client, project)
    move = capture_move_set(plan_bundle, MEMBERS, "parent/clip:clip-2", 3)

    other_bundle = _bundle(client, project)
    if intervening == "disjoint":
        other = capture_move(other_bundle, "parent/clip:clip-other", 11)
        result, _ = _commit(client, project, [other], "other-disjoint")
        assert result.ok, result.as_dict()
    else:
        # Move the same lane entry away, then back, so final JSON equals the
        # stale basis while accepted history still contains the ABA writes.
        other = capture_move_set(
            other_bundle,
            [{"clip": "parent/clip:clip-other", "track": "parent/track:V3"}],
            "parent/clip:clip-other", 10,
        )
        result, _ = _commit(client, project, [other], "other-to-v3")
        assert result.ok, result.as_dict()
        back_bundle = _bundle(client, project)
        back = capture_move_set(
            back_bundle,
            [{"clip": "parent/clip:clip-other", "track": "parent/track:V1"}],
            "parent/clip:clip-other", 10,
        )
        result, _ = _commit(client, project, [back], "other-back-v1")
        assert result.ok, result.as_dict()

    before = _history(client, project)
    result, _ = _commit(client, project, [move], "stale-free-move", base=base)
    if intervening == "disjoint":
        assert result.ok, result.as_dict()
        assert result.data["status"] == "rebased"
        document = _reload(client, project, result.as_dict())
        _assert_geometry(document, moved=True)
        other = next(row for row in document["parent_revision"]["payload"]["clips"]
                     if row["id"] == "clip-other")
        assert other["at"] == 11
    else:
        assert not result.ok, result.as_dict()
        assert result.error.details["reason"] == "intervening_write"
        assert _history(client, project) == before

