"""SPEC-v2 clash-back journeys against a real Runtime."""

from __future__ import annotations

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


def _inject_current_base_conflict(monkeypatch, transport, label):
    """Save a refusal without making the request's guarded writes stale."""
    from astrid_runtime_client import ApiError

    original = transport.commit_timeline
    injected = []

    def conflict_once(project_id, timeline_id, body, **kwargs):
        if body.get("label") == label and not injected:
            injected.append(body)
            raise ApiError(
                409,
                "conflict",
                "injected definitive conflict before Runtime execution",
                details={
                    "status": "conflict",
                    "reason": "intervening_write",
                    "current": {
                        "revision_id": body["base_revision_id"],
                        "publication_id": body["base_publication_id"],
                    },
                    "conflicts": [],
                },
            )
        return original(project_id, timeline_id, body, **kwargs)

    monkeypatch.setattr(transport, "commit_timeline", conflict_once)
    return original, injected


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
    assert any(
        conflict["ref"] == "parent/clip:b" and conflict["path"] == ["at"]
        for conflict in saved["clash"]["conflicts"]
    )

    # The CLI's discard path clears recoverable work but preserves the saved clash.
    from astrid.packs.timeline.cli_working import _discard_recoverable_outbox

    with stale.session.outbox.locked():
        scope = stale.session._state()["scope"]
    discarded, kept = _discard_recoverable_outbox(
        stale.session.outbox, scope, return_kept_count=True
    )
    assert discarded == "cleared"
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
        if body.get("label") == "J3 function" and len(peer_writes) < (3 if same_process else 2):
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
        elif body.get("label") == "J3 function" and not same_process and len(peer_writes) == 2:
            # The saved function attempt is based on the current head after two
            # real clashes. Refuse it before Runtime execution so its guards
            # still apply when the process restarts and retries it.
            from astrid_runtime_client import ApiError

            raise ApiError(
                409,
                "conflict",
                "injected definitive final conflict before Runtime execution",
                details={
                    "status": "conflict",
                    "reason": "intervening_write",
                    "current": {
                        "revision_id": body["base_revision_id"],
                        "publication_id": body["base_publication_id"],
                    },
                    "conflicts": [],
                },
            )
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
        assert retry["_retry_request"]["base_revision_id"] == (
            reopened.session._state()["base"]["revision_id"]
        )
        assert retry["_retry_request"]["base_publication_id"] == (
            reopened.session._state()["base"]["publication_id"]
        )
        landed = reopened.commit(retry)
        timeline = reopened
    assert landed["receipt"]["receipt_id"]
    assert len(evaluations) == (4 if same_process else 3)
    assert _assert_closed(timeline, caught.value.pending_id)["state"] == "landed"


def test_j4_lost_ack_on_retry_is_confirmed_once_and_record_closes(
    editing_case,
    tmp_path,
    monkeypatch,
):
    _, client, project, timeline = editing_case
    _seed_clip(timeline, tmp_path)
    stale = type(timeline).open(
        project, "film", client=client, outbox_path=tmp_path / "j4-stale.json"
    )
    commands = _move_commands(stale, on=4, label="J4 reviewed move")
    generated = client._remote._transport._generated
    original, injected = _inject_current_base_conflict(
        monkeypatch, generated, "J4 reviewed move"
    )
    from astrid.sdk.timeline.sync import CommitConflict, CommitOutcomeUnknown
    from astrid_runtime_client import ApiError

    with pytest.raises(CommitConflict) as caught:
        stale.commit(commands, label="J4 reviewed move", key="j4-list")
    pending_id = caught.value.pending_id
    retry = stale.retry(pending_id)
    assert retry["status"] == "preview"
    assert retry["_retry_request"]["base_revision_id"] == (
        stale.session._state()["base"]["revision_id"]
    )
    assert retry["_retry_request"]["base_publication_id"] == (
        stale.session._state()["base"]["publication_id"]
    )
    before = _history(client, project)
    calls = []

    def lose_retry_reply(project_id, timeline_id, body, **kwargs):
        result = original(project_id, timeline_id, body, **kwargs)
        if body.get("label") == "J4 reviewed move" and not calls:
            calls.append(kwargs["idempotency_key"])
            raise ApiError(503, "not_ready", "simulated lost retry response after acceptance")
        return result

    monkeypatch.setattr(generated, "commit_timeline", lose_retry_reply)
    with pytest.raises(CommitOutcomeUnknown):
        stale.commit(retry)
    monkeypatch.setattr(generated, "commit_timeline", original)
    assert len(injected) == 1
    landed = stale.commit()
    assert landed["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(before) + 1
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
    original, injected = _inject_current_base_conflict(
        monkeypatch, owner_transport, "J5 reviewed move"
    )
    with pytest.raises(CommitConflict) as caught:
        owner.commit(commands, label="J5 reviewed move", key="j5-list")
    pending_id = caught.value.pending_id
    assert pending_id
    assert [item["id"] for item in peer.pending_list(actors="all")] == [pending_id]

    owner_preview = owner.retry(pending_id)
    peer_preview = peer.retry(pending_id)
    assert owner_preview["status"] == peer_preview["status"] == "preview"
    assert owner_preview["_retry_request"]["base_revision_id"] == (
        owner.session._state()["base"]["revision_id"]
    )
    assert owner_preview["_retry_request"]["base_publication_id"] == (
        owner.session._state()["base"]["publication_id"]
    )
    history_before = _history(client, project)
    nested = []

    def let_peer_win(project_id_arg, timeline_id_arg, body, **kwargs):
        if body.get("label") == "J5 reviewed move" and not nested:
            nested.append(peer.commit(peer_preview))
        return original(project_id_arg, timeline_id_arg, body, **kwargs)

    monkeypatch.setattr(owner_transport, "commit_timeline", let_peer_win)
    peer_result = owner.commit(owner_preview)
    assert nested[0]["receipt"]["receipt_id"]
    assert peer_result["status"] == "landed"
    assert peer_result["data"]["receipt"]["receipt_id"] == nested[0]["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(history_before) + 1
    assert _history(client, project)[-1]["group_id"] == pending_id
    owner_record = _assert_closed(owner, pending_id)
    assert owner_record["closed_by"]["actor_id"] == "j5-peer"
    assert owner_record["closed_by"]["how"] == "retry"
    assert peer.pending_show(pending_id)["state"] == "landed"
    assert len(injected) == 1
