"""SPEC-v2 clash-back journeys against a real Runtime."""

from __future__ import annotations

import copy
import uuid

import pytest

from tests.sdk.test_timeline_editing_acceptance_runtime import _history, _media_file

pytest_plugins = ("tests.sdk.test_timeline_editing_acceptance_runtime",)


def _peer(daemon, project, tmp_path, *, actor="clash-peer", outbox=None):
    from astrid.sdk.timeline import Timeline
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    _, credential = daemon.credentials.provision(
        actor,
        [
            "handshake",
            "projects:read",
            "projects:write",
            "objects:read",
            "objects:write",
            "tasks:read",
            "tasks:write",
        ],
    )
    client = open_client(daemon, actor=actor, credential=credential)
    path = outbox if outbox is not None else tmp_path / f"{actor}.json"
    return client, Timeline.open(project, "film", client=client, outbox_path=path)


def _seed_clip(timeline, tmp_path):
    timeline.commit(
        lambda t: t.add(_media_file(tmp_path / "b.png"), at=0, hold=3, track="V1", id="b"),
        label="Seed b",
        key="clash-seed-b",
    )


def _move_commands(timeline, *, on, label):
    return timeline.commit(
        lambda t: t.move("parent/clip:b", on=on),
        label=label,
        dry_run=True,
    )["data"]["commands"]


def _assert_closed(timeline, pending_id, *, how=None):
    record = timeline.pending_show(pending_id)
    assert record["state"] == "landed"
    assert record["closed_by"]["publication_id"]
    if how is not None:
        assert record["closed_by"]["how"] == how
    return record


def _injected_conflict(timeline, *, current=None, ref="parent/clip:b", path=("at",)):
    from astrid_runtime_client import ApiError

    return ApiError(409, "conflict", "injected definitive conflict", details={
        "status": "conflict",
        "reason": "value_conflict",
        "conflicts": [{"ref": ref, "path": list(path)}],
        "current": dict(current or timeline.head),
    })


def test_j1_overlapping_list_survives_restart_and_rederive_closes_record(
    editing_case,
    tmp_path,
):
    daemon, client, project, timeline = editing_case
    _seed_clip(timeline, tmp_path)
    stale = type(timeline).open(project, "film", client=client, outbox_path=tmp_path / "stale.json")
    peer_client, peer = _peer(daemon, project, tmp_path)
    commands = _move_commands(stale, on=4, label="Reviewed recut")

    peer.commit(lambda t: t.move("parent/clip:b", on=6), label="W2 move b", key="j1-peer-move")
    from astrid.sdk.timeline.sync import CommitConflict

    with pytest.raises(CommitConflict) as caught:
        stale.commit(commands, label="Reviewed recut", key="j1-reviewed-recut")
    runtime_conflicts = caught.value.failure["details"]["conflicts"]
    pending_id = caught.value.pending_id
    assert pending_id
    saved = stale.pending_show(pending_id)
    assert saved["state"] == "pending"
    assert saved["clash"]["schema"] == "astrid.clash/2"
    assert any(
        row["label"] == "W2 move b" and row["touches_conflict"]
        and any(site["ref"] == "parent/clip:b" and site["path"] == ["at"]
                for site in row["touched"])
        for row in saved["clash"]["receipts"]
    )
    assert saved["clash"]["conflicts"] == runtime_conflicts

    # The CLI's discard path clears recoverable work but preserves the saved clash.
    from astrid.packs.timeline.cli_working import _discard_recoverable_outbox

    with stale.session.outbox.locked():
        scope = stale.session._state()["scope"]
    discarded, kept = _discard_recoverable_outbox(
        stale.session.outbox, scope, return_kept_count=True
    )
    assert discarded in {"clear", "cleared"}
    assert kept == 1

    # Reopen the outbox to prove the refused list, rather than in-memory state, drives recovery.
    reopened = type(timeline).open(
        project, "film", client=client, outbox_path=tmp_path / "stale.json"
    )
    retry = reopened.retry(pending_id)
    assert retry["status"] == "re_derive"
    assert retry["data"]["conflicts"]
    assert retry["data"]["receipts"][0]["label"] == "W2 move b"

    preview = reopened.commit(
        lambda t: t.move("parent/clip:b", on=8), label="Reviewed recut", dry_run=True
    )
    landed = reopened.commit(
        preview["data"]["commands"],
        label="Reviewed recut",
        key="j1-reviewed-recut",
        pending=pending_id,
    )
    assert landed["receipt"]["receipt_id"]
    assert _assert_closed(reopened, pending_id)["closed_by"]["how"] == "rederive"
    assert (
        _history(peer_client, project)[-1]["receipt"]["result"]["canonical_document"]
        == landed["data"]["canonical_document"]
    )


@pytest.mark.parametrize("same_process", [True, False])
def test_j3_exhausted_function_retry_lands_and_closes_record(
    editing_case,
    tmp_path,
    monkeypatch,
    same_process,
):
    daemon, client, project, timeline = editing_case
    _seed_clip(timeline, tmp_path)
    from astrid.sdk.timeline.sync import CommitConflict
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    _, credential = daemon.credentials.provision(
        "j3-peer",
        [
            "handshake",
            "projects:read",
            "projects:write",
            "objects:read",
            "objects:write",
            "tasks:read",
            "tasks:write",
        ],
    )
    peer_client = open_client(daemon, actor="j3-peer", credential=credential)
    peer = type(timeline).open(
        project, "film", client=peer_client, outbox_path=tmp_path / "j3-peer.json"
    )
    peer_session = [peer]
    generated = client._remote._transport._generated
    original = generated.commit_timeline
    evaluations = []
    peer_writes = []

    def inject_peer_before_primary(project_id, timeline_id, body, **kwargs):
        peer_limit = 3 if same_process else 2
        if body.get("label") == "J3 function" and len(peer_writes) < peer_limit:
            peer_writes.append(
                peer_session[0].commit(
                    lambda t: t.move("parent/clip:b", on=10 + len(peer_writes)),
                    label=f"J3 peer {len(peer_writes) + 1}",
                    key=f"j3-peer-{len(peer_writes)}",
                )
            )
            peer_session[0] = type(timeline).open(
                project, "film", client=peer_client, outbox_path=tmp_path / "j3-peer.json"
            )
        elif body.get("label") == "J3 function" and not same_process:
            raise _injected_conflict(timeline, current=peer_session[0].head)
        return original(project_id, timeline_id, body, **kwargs)

    monkeypatch.setattr(generated, "commit_timeline", inject_peer_before_primary)

    def edit(t):
        evaluations.append(t.bundle["parent"]["clips"][0]["at"])
        t.move("parent/clip:b", on=20)

    with pytest.raises(CommitConflict) as caught:
        timeline.commit(edit, label="J3 function", key="j3-function")
    assert len(evaluations) == 3
    assert len(peer_writes) == (3 if same_process else 2)
    assert caught.value.pending_id
    if same_process:
        monkeypatch.setattr(generated, "commit_timeline", original)
        landed = timeline.retry(caught.value)
    else:
        reopened = type(timeline).open(
            project, "film", client=client, outbox_path=timeline.session.outbox.path
        )
        monkeypatch.setattr(generated, "commit_timeline", original)
        retry = reopened.retry(caught.value.pending_id)
        assert retry["status"] == "preview"
        landed = reopened.commit(retry)
        assert str(uuid.UUID(landed["receipt"]["idempotency_key"])) == landed["receipt"]["idempotency_key"]
        assert _history(client, project)[-1]["group_id"] == caught.value.pending_id
        timeline = reopened
    assert landed["receipt"]["receipt_id"]
    assert len(evaluations) == (4 if same_process else 3)
    assert _assert_closed(timeline, caught.value.pending_id)["state"] == "landed"


def test_j4_lost_ack_on_retry_is_confirmed_once_and_record_closes(
    editing_case,
    tmp_path,
    monkeypatch,
):
    daemon, client, project, timeline = editing_case
    _seed_clip(timeline, tmp_path)
    stale = type(timeline).open(
        project, "film", client=client, outbox_path=tmp_path / "j4-stale.json"
    )
    commands = _move_commands(stale, on=4, label="J4 reviewed move")
    from astrid.sdk.timeline.sync import CommitConflict, CommitOutcomeUnknown
    from astrid_runtime_client import ApiError

    generated = client._remote._transport._generated
    original = generated.commit_timeline
    initial_conflicts = []

    def inject_initial_conflict(project_id, timeline_id, body, **kwargs):
        if body.get("label") == "J4 reviewed move" and not initial_conflicts:
            initial_conflicts.append(body)
            raise _injected_conflict(stale)
        return original(project_id, timeline_id, body, **kwargs)

    monkeypatch.setattr(generated, "commit_timeline", inject_initial_conflict)

    with pytest.raises(CommitConflict) as caught:
        stale.commit(commands, label="J4 reviewed move", key="j4-list")
    pending_id = caught.value.pending_id
    assert pending_id and len(initial_conflicts) == 1
    monkeypatch.setattr(generated, "commit_timeline", original)
    retry = stale.retry(pending_id)
    assert retry["status"] == "preview"
    before = _history(client, project)
    calls = []

    def lose_retry_reply(project_id, timeline_id, body, **kwargs):
        result = original(project_id, timeline_id, body, **kwargs)
        if body.get("label") == "J4 reviewed move" and not calls:
            calls.append((kwargs["idempotency_key"], body.get("group_id")))
            raise ApiError(503, "not_ready", "simulated lost retry response after acceptance")
        return result

    monkeypatch.setattr(generated, "commit_timeline", lose_retry_reply)
    with pytest.raises(CommitOutcomeUnknown):
        stale.commit(retry)
    monkeypatch.setattr(generated, "commit_timeline", original)
    landed = stale.commit()
    assert landed["receipt"]["receipt_id"]
    assert calls[0][0] != "j4-list"
    assert str(uuid.UUID(calls[0][0])) == calls[0][0]
    assert calls[0][1] == pending_id
    assert len(_history(client, project)) == len(before) + 1
    assert _history(client, project)[-1]["group_id"] == pending_id
    closed = _assert_closed(stale, pending_id)
    assert closed["receipts"] == [landed["receipt"]["receipt_id"]]
    assert closed["closed_by"]["publication_id"] == landed["receipt"]["receipt_id"]


def test_j5_two_actors_retry_one_record_and_group_id_closes_other_actor(
    editing_case,
    tmp_path,
    monkeypatch,
):
    daemon, client, project, timeline = editing_case
    _seed_clip(timeline, tmp_path)
    # Default actor-specific outboxes make records discoverable to the other actor.
    data_root = tmp_path / "astrid-data"
    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(data_root))
    from astrid.sdk.timeline import Timeline
    from astrid.sdk.timeline.sync import CommitConflict
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    owner = Timeline.open(project, "film", client=client)
    _, credential = daemon.credentials.provision(
        "j5-peer",
        [
            "handshake",
            "projects:read",
            "projects:write",
            "objects:read",
            "objects:write",
            "tasks:read",
            "tasks:write",
        ],
    )
    peer_client = open_client(daemon, actor="j5-peer", credential=credential)
    # Use the peer's default actor outbox under the same configured data root.
    peer = Timeline.open(project, "film", client=peer_client)
    commands = _move_commands(owner, on=4, label="J5 reviewed move")
    owner_transport = client._remote._transport._generated
    original = owner_transport.commit_timeline
    initial_conflicts = []

    def inject_initial_conflict(project_id_arg, timeline_id_arg, body, **kwargs):
        if body.get("label") == "J5 reviewed move" and not initial_conflicts:
            initial_conflicts.append(body)
            raise _injected_conflict(owner)
        return original(project_id_arg, timeline_id_arg, body, **kwargs)

    monkeypatch.setattr(owner_transport, "commit_timeline", inject_initial_conflict)
    with pytest.raises(CommitConflict) as caught:
        owner.commit(commands, label="J5 reviewed move", key="j5-list")
    pending_id = caught.value.pending_id
    assert pending_id and len(initial_conflicts) == 1
    monkeypatch.setattr(owner_transport, "commit_timeline", original)
    assert [item["id"] for item in peer.pending_list(actors="all")] == [pending_id]

    owner_preview = owner.retry(pending_id)
    peer_preview = peer.retry(pending_id)
    assert owner_preview["status"] == peer_preview["status"] == "preview"
    history_before = _history(client, project)
    nested = []
    retry_requests = []

    def let_peer_win(project_id_arg, timeline_id_arg, body, **kwargs):
        if body.get("label") == "J5 reviewed move" and not nested:
            retry_requests.append((kwargs["idempotency_key"], body.get("group_id")))
            nested.append(peer.commit(peer_preview))
        return original(project_id_arg, timeline_id_arg, body, **kwargs)

    monkeypatch.setattr(owner_transport, "commit_timeline", let_peer_win)
    peer_result = owner.commit(owner_preview)
    assert nested[0]["receipt"]["receipt_id"]
    assert retry_requests[0][0] != "j5-list"
    assert retry_requests[0][1] == pending_id
    assert peer_result["status"] == "landed"
    assert peer_result["data"]["receipt"]["receipt_id"] == nested[0]["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(history_before) + 1
    assert _history(client, project)[-1]["group_id"] == pending_id
    winner_key = nested[0]["receipt"]["idempotency_key"]
    assert winner_key != "j5-list"
    assert str(uuid.UUID(winner_key)) == winner_key
    owner_record = _assert_closed(owner, pending_id)
    assert owner_record["closed_by"]["actor_id"] == "j5-peer"
    assert owner_record["closed_by"]["how"] == "retry"
    assert peer.pending_show(pending_id)["state"] == "landed"


def test_five_agents_deterministic(editing_case, tmp_path, monkeypatch):
    daemon, client, project, setup = editing_case
    data_root = tmp_path / "astrid-data"
    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(data_root))
    from astrid.sdk.timeline import Timeline
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.sync import CommitConflict
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    source = _media_file(tmp_path / "five-agents.png")

    def seed(t):
        for index in range(1, 7):
            t.add(source, at=(index - 1) * 5, hold=2, track="V1", id=f"c{index}")

    setup.commit(seed, label="Seed six agents", key="j6-seed")
    baseline = copy.deepcopy(setup._base_bundle)
    initial_head = dict(setup.head)

    actors = {}
    for name in ("j6-a1", "j6-a2", "j6-a3", "j6-a4", "j6-a5"):
        _, credential = daemon.credentials.provision(
            name,
            ["handshake", "projects:read", "projects:write", "objects:read",
             "objects:write", "tasks:read", "tasks:write"],
        )
        actor_client = open_client(daemon, actor=name, credential=credential)
        outbox = None if name in {"j6-a1", "j6-a5"} else tmp_path / f"{name}.json"
        actors[name] = (actor_client, Timeline.open(
            project, "film", client=actor_client, outbox_path=outbox
        ))

    a1_client, a1 = actors["j6-a1"]
    _, a2 = actors["j6-a2"]
    a3_client, a3 = actors["j6-a3"]
    a4_client, a4 = actors["j6-a4"]
    a5_client, a5 = actors["j6-a5"]
    assert all(timeline.head == initial_head for _, timeline in actors.values())

    def set_clip_fields(t, clip_id, **values):
        for parent in (t.bundle["parent"], t.bundle["parent"]["config"]):
            clips = parent.get("clips", [])
            clip = next((clip for clip in clips if clip["id"] == clip_id), None)
            if clip is not None:
                clip.update(values)

    def set_volume(clip_id, value):
        def edit(t):
            set_clip_fields(t, clip_id, volume=value)
        return edit

    def a3_producer(t):
        t.move("parent/clip:c2", on=6.0)
        set_clip_fields(t, "c3", opacity=0.8)

    def a4_producer(t):
        set_clip_fields(t, "c4", volume=0.3)
        set_clip_fields(t, "c5", volume=0.3)
        t.move("parent/clip:c2", on=8.0)

    def reviewed_commands(timeline, producer):
        working = Timeline(timeline.session, timeline._base_bundle, initial_head, evaluating=True)
        producer(working)
        working._capture_free_edits()
        return working._commands

    a3_commands = reviewed_commands(a3, a3_producer)
    a4_commands = reviewed_commands(a4, a4_producer)

    accepted = a1.commit(set_volume("c1", 0.5), label="A1 volume", key="j6-a1")
    assert accepted["status"] == "accepted"

    moved = a2.commit(lambda t: t.move("parent/clip:c2", on=4.0),
                      label="A2 move", key="j6-a2")
    assert moved["status"] in {"accepted", "merged"}

    with pytest.raises(CommitConflict) as a3_caught:
        a3.commit(a3_commands, label="A3 reviewed edits", key="j6-a3-list")
    a3_id = a3_caught.value.pending_id
    assert a3_id
    assert a3.retry(a3_id)["status"] == "re_derive"
    a3 = Timeline.open(project, "film", client=a3_client, outbox_path=a3.session.outbox.path)
    a3_evaluations = []

    def a3_rederive(t):
        a3_evaluations.append(t.bundle["parent"]["clips"])
        a3_producer(t)

    a3_preview = a3.commit(a3_rederive, label="A3 reviewed edits", dry_run=True)
    a3_landed = a3.commit(a3_preview["data"]["commands"], label="A3 reviewed edits",
                          key="j6-a3-list", pending=a3_id)
    assert a3_landed["status"] in {"accepted", "merged"}
    assert len(a3_evaluations) == 1
    assert _assert_closed(a3, a3_id)["closed_by"]["how"] == "rederive"

    with pytest.raises(CommitConflict) as a4_caught:
        a4.commit(a4_commands, label="A4 batch", key="j6-a4-list")
    a4_id = a4_caught.value.pending_id
    assert a4_id
    assert a4.retry(a4_id)["status"] == "re_derive"
    a4 = Timeline.open(project, "film", client=a4_client, outbox_path=a4.session.outbox.path)
    a4_evaluations = []

    def a4_rederive(t):
        a4_evaluations.append(t.bundle["parent"]["clips"])
        a4_producer(t)

    a4_preview = a4.commit(a4_rederive, label="A4 batch", dry_run=True)
    a4_landed = a4.commit(a4_preview["data"]["commands"], label="A4 batch",
                          key="j6-a4-list", pending=a4_id)
    assert a4_landed["status"] in {"accepted", "merged"}
    assert len(a4_evaluations) == 1
    assert _assert_closed(a4, a4_id)["closed_by"]["how"] == "rederive"

    generated = a5_client._remote._transport._generated
    original = generated.commit_timeline
    injected = []

    def exhaust_a5(project_id_arg, timeline_id_arg, body, **kwargs):
        if body.get("label") == "A5 function" and len(injected) < 3:
            injected.append(body)
            raise _injected_conflict(a5, ref="parent/clip:c6", path=("opacity",))
        return original(project_id_arg, timeline_id_arg, body, **kwargs)

    monkeypatch.setattr(generated, "commit_timeline", exhaust_a5)
    a5_evaluations = []

    def a5_producer(t):
        a5_evaluations.append(t.bundle["parent"]["clips"])
        set_clip_fields(t, "c6", opacity=0.5)

    with pytest.raises(CommitConflict) as a5_caught:
        a5.commit(a5_producer, label="A5 function", key="j6-a5", reads=[])
    a5_id = a5_caught.value.pending_id
    assert a5_id and len(injected) == 3 and len(a5_evaluations) == 3
    monkeypatch.setattr(generated, "commit_timeline", original)

    # A5's process is gone: A1 finds its durable record and takes the saved list path.
    found = a1.pending_list(actors="all")
    assert any(record["id"] == a5_id for record in found)
    a5_retry = a1.retry(a5_id)
    assert a5_retry["status"] == "preview"
    a5_preview = a1.commit(a5_retry)
    assert a5_preview["status"] in {"accepted", "merged", "landed"}

    records = a1.pending_list(actors="all")
    assert all(record["state"] != "pending" for record in records)
    a5_record = a1.pending_show(a5_id)
    assert a5_record["state"] == "landed"
    assert a5_record["closed_by"]["actor_id"] == "j6-a1"

    expected = copy.deepcopy(baseline)
    for parent in (expected["parent"], expected["parent"]["config"]):
        for clip in parent.get("clips", []):
            if clip["id"] == "c1":
                clip["volume"] = 0.5
            elif clip["id"] == "c2":
                clip["at"] = 8.0
                astrid = clip.setdefault("app", {}).setdefault("astrid", {})
                astrid["fixed_start"] = True
                astrid.setdefault("for", 2.0)
            elif clip["id"] == "c3":
                clip["opacity"] = 0.8
            elif clip["id"] in {"c4", "c5"}:
                clip["volume"] = 0.3
            elif clip["id"] == "c6":
                clip["opacity"] = 0.5
    actual = bundle_from_document(a1._runtime_document)
    assert actual["parent"]["clips"] == expected["parent"]["clips"]
    assert actual["parent"]["registry"] == expected["parent"]["registry"]
    actual_config = {key: value for key, value in actual["parent"]["config"].items()
                     if key != "clips"}
    expected_config = {key: value for key, value in expected["parent"]["config"].items()
                       if key != "clips"}
    assert actual_config == expected_config
    assert actual["placements"] == expected["placements"]
    assert actual["shots"] == expected["shots"]
    assert len(a3_evaluations) == len(a4_evaluations) == 1
