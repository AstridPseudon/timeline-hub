"""Deterministic multi-actor clash-back journey against a real Runtime."""

from __future__ import annotations

import copy

import pytest

from tests.sdk.test_timeline_editing_acceptance_runtime import _media_file

pytest_plugins = ("tests.sdk.test_timeline_editing_acceptance_runtime",)


def _actor(daemon, project, tmp_path, name, *, outbox=None):
    from astrid.sdk.timeline import Timeline
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    _, credential = daemon.credentials.provision(
        name,
        ["handshake", "projects:read", "projects:write", "objects:read", "objects:write",
         "tasks:read", "tasks:write"],
    )
    client = open_client(daemon, actor=name, credential=credential)
    timeline = (Timeline.open(project, "film", client=client) if outbox is None else
                Timeline.open(project, "film", client=client, outbox_path=outbox))
    return client, timeline


def _injected_conflict(timeline, *, ref, path):
    from astrid_runtime_client import ApiError

    return ApiError(409, "conflict", "injected definitive conflict", details={
        "status": "conflict",
        "reason": "value_conflict",
        "conflicts": [{"ref": ref, "path": list(path)}],
        "current": dict(timeline.head),
    })


def _set_clip(timeline, clip_id, **values):
    parent = timeline.bundle["parent"]
    for root in (parent, parent.get("config", {})):
        clip = next((row for row in root.get("clips", []) if row["id"] == clip_id), None)
        if clip is not None:
            clip.update(values)


def _clips(document):
    return {
        row["id"]: {key: row[key] for key in ("at", "volume", "opacity") if key in row}
        for row in document["parent"]["clips"]
    }


def _a5_clash_process(endpoint, credential, realm, project, result_queue):
    from astrid.sdk.client import AstridClient
    from astrid.sdk.timeline import Timeline
    from astrid.sdk.timeline.sync import CommitConflict

    client = AstridClient.open(
        endpoint=endpoint,
        credential=credential,
        realm_id=realm,
        actor_id="j6-a5",
        client_name="j6-clash-recovery",
        client_version="1",
        protocol_version="workspace.v1",
    )
    timeline = Timeline.open(project, "film", client=client)
    generated = client._remote._transport._generated
    original = generated.commit_timeline
    injected = []
    evaluations = []

    def exhaust_a5(project_id, timeline_id, body, **kwargs):
        if body.get("label") == "A5 opacity" and len(injected) < 3:
            injected.append(body)
            raise _injected_conflict(timeline, ref="parent/clip:c6", path=("opacity",))
        return original(project_id, timeline_id, body, **kwargs)

    generated.commit_timeline = exhaust_a5

    def a5_edit(t):
        evaluations.append(1)
        _set_clip(t, "c6", opacity=0.5)

    try:
        timeline.commit(a5_edit, label="A5 opacity", key="j6-a5")
    except CommitConflict as caught:
        result_queue.put({
            "pending_id": caught.pending_id,
            "injected": len(injected),
            "evaluations": len(evaluations),
        })
    else:
        result_queue.put({"error": "A5 commit unexpectedly succeeded"})


def test_five_agents_deterministic(editing_case, tmp_path, monkeypatch):
    daemon, _client, project, setup = editing_case
    monkeypatch.setenv("ASTRID_RUNTIME_DATA_ROOT", str(tmp_path / "astrid-data"))

    from astrid.sdk.timeline import Timeline
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.sync import CommitConflict

    source = _media_file(tmp_path / "five-agents.png")

    def seed(t):
        for index in range(1, 7):
            t.add(source, at=(index - 1) * 5, hold=2, track="V1", id=f"c{index}")

    setup.commit(seed, label="Seed six clips", key="j6-seed")
    initial_head = dict(setup.head)
    baseline = copy.deepcopy(_clips(setup._base_bundle))

    actors = {
        name: _actor(
            daemon,
            project,
            tmp_path,
            name,
            outbox=None if name == "j6-a1" else tmp_path / f"{name}.json",
        )
        for name in ("j6-a1", "j6-a2", "j6-a3", "j6-a4")
    }
    a1_client, a1 = actors["j6-a1"]
    _, a2 = actors["j6-a2"]
    a3_client, a3 = actors["j6-a3"]
    a4_client, a4 = actors["j6-a4"]
    assert all(timeline.head == initial_head for _, timeline in actors.values())

    def a1_edit(t):
        _set_clip(t, "c1", volume=0.5)

    a3_runs = []

    def a3_edit(t):
        a3_runs.append(1)
        t.move("parent/clip:c2", on=6.0)
        _set_clip(t, "c3", opacity=0.8)

    a4_runs = []

    def a4_edit(t):
        a4_runs.append(1)
        _set_clip(t, "c4", volume=0.3)
        _set_clip(t, "c5", volume=0.3)
        t.move("parent/clip:c2", on=8.0)

    # Capture both reviewed lists from the same head before releasing any writer.
    a2_commands = a2.commit(
        lambda t: t.move("parent/clip:c2", on=4.0), label="A2 move", dry_run=True
    )["data"]["commands"]
    a3_commands = a3.commit(a3_edit, label="A3 edits", dry_run=True)["data"]["commands"]
    a4_commands = a4.commit(a4_edit, label="A4 batch", dry_run=True)["data"]["commands"]
    assert len(a3_runs) == len(a4_runs) == 1

    # Functions retain their default atomic merge mode; no reads override is supplied.
    accepted = a1.commit(a1_edit, label="A1 volume", key="j6-a1")
    assert accepted["status"] == "accepted"

    merged = a2.commit(a2_commands, label="A2 move", key="j6-a2")
    assert merged["status"] == "merged"

    with pytest.raises(CommitConflict) as a3_caught:
        a3.commit(a3_commands, label="A3 edits", key="j6-a3-list")
    a3_id = a3_caught.value.pending_id
    assert a3_id
    assert a3.retry(a3_id)["status"] == "re_derive"
    a3 = Timeline.open(project, "film", client=a3_client, outbox_path=a3.session.outbox.path)
    def a3_rederive(t):
        a3_edit(t)

    a3_preview = a3.commit(a3_rederive, label="A3 edits", dry_run=True)
    assert a3_preview["status"] == "preview"
    a3_landed = a3.commit(
        a3_preview["data"]["commands"], label="A3 edits", key="j6-a3-list", pending=a3_id
    )
    assert a3_landed["status"] in {"accepted", "merged", "landed"}
    assert len(a3_runs) == 2
    assert a3.pending_show(a3_id)["state"] == "landed"

    with pytest.raises(CommitConflict) as a4_caught:
        a4.commit(a4_commands, label="A4 batch", key="j6-a4-list")
    a4_id = a4_caught.value.pending_id
    assert a4_id
    assert a4.retry(a4_id)["status"] == "re_derive"
    a4 = Timeline.open(project, "film", client=a4_client, outbox_path=a4.session.outbox.path)
    def a4_rederive(t):
        a4_edit(t)

    a4_preview = a4.commit(a4_rederive, label="A4 batch", dry_run=True)
    assert a4_preview["status"] == "preview"
    a4_landed = a4.commit(
        a4_preview["data"]["commands"], label="A4 batch", key="j6-a4-list", pending=a4_id
    )
    assert a4_landed["status"] in {"accepted", "merged", "landed"}
    assert len(a4_runs) == 2
    assert a4.pending_show(a4_id)["state"] == "landed"

    import multiprocessing

    _, a5_credential = daemon.credentials.provision(
        "j6-a5",
        ["handshake", "projects:read", "projects:write", "objects:read", "objects:write",
         "tasks:read", "tasks:write"],
    )
    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue()
    a5_process = context.Process(
        target=_a5_clash_process,
        args=(daemon.endpoint, a5_credential, daemon.service.realm["id"], project, result_queue),
    )
    a5_process.start()
    a5_process.join(timeout=60)
    if a5_process.is_alive():
        a5_process.terminate()
        a5_process.join(timeout=10)
        pytest.fail("A5 child process did not exit")
    assert a5_process.exitcode == 0
    a5_result = result_queue.get(timeout=5)
    assert "error" not in a5_result, a5_result
    a5_id = a5_result["pending_id"]
    assert a5_id and a5_result["injected"] == 3 and a5_result["evaluations"] == 3
    result_queue.close()

    # A5 has exited. A1 discovers the durable record and publishes its saved-list fallback.
    assert any(record["id"] == a5_id for record in a1.pending_list(actors="all"))
    fallback = a1.retry(a5_id)
    assert fallback["status"] == "preview"
    assert a1.commit(fallback)["status"] in {"accepted", "merged", "landed"}

    all_records = a1.pending_list(actors="all")
    assert not [record for record in all_records if record["state"] == "pending"]
    closed = a1.pending_show(a5_id)
    assert closed["state"] == "landed"
    assert closed["closed_by"]["actor_id"] == "j6-a1"

    expected = copy.deepcopy(baseline)
    expected["c1"]["volume"] = 0.5
    expected["c2"]["at"] = 8.0
    expected["c3"]["opacity"] = 0.8
    expected["c4"]["volume"] = 0.3
    expected["c5"]["volume"] = 0.3
    expected["c6"]["opacity"] = 0.5
    assert _clips(bundle_from_document(a1._runtime_document)) == expected
