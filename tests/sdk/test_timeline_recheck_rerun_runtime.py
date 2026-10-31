"""Regression coverage for retrying an exhausted function by pending id."""
from __future__ import annotations

import json

import pytest

from tests.sdk.test_timeline_editing_acceptance_runtime import _media_file

pytest_plugins = ("tests.sdk.test_timeline_editing_acceptance_runtime",)


def test_retry_pending_id_overwrite_rebases_same_timeline_after_function_clash(
    editing_case, tmp_path,
):
    daemon, client, project, timeline = editing_case
    from astrid.sdk.timeline import Timeline
    from astrid.sdk.timeline.sync import CommitConflict
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    source = _media_file(tmp_path / "retry-overwrite-seed.png")
    timeline.commit(
        lambda t: [t.add(source, at=index * 5, hold=4, track="V1", id=f"clip-{index}")
                   for index in range(1, 4)],
        label="Seed retry clips",
    )
    _, credential = daemon.credentials.provision("retry-overwrite-peer", [
        "handshake", "projects:read", "projects:write", "objects:read", "objects:write",
        "tasks:read", "tasks:write",
    ])
    peer = Timeline.open(
        project,
        "film",
        client=open_client(daemon, actor="retry-overwrite-peer", credential=credential),
        outbox_path=tmp_path / "retry-overwrite-peer.json",
    )
    peer.clip("clip-3").set_duration(3.0)
    peer_edit = peer.commit(label="Peer clip duration", key="retry-overwrite-peer-edit")
    assert peer_edit["receipt"]["receipt_id"]

    def set_all_durations(t):
        for index in range(1, 4):
            t.clip(f"clip-{index}").set_duration(2.0)

    with pytest.raises(CommitConflict) as caught:
        timeline.commit(set_all_durations, label="Retry overwrite durations", key="retry-overwrite")
    pending_id = caught.value.pending_id
    assert pending_id

    rebased = timeline.retry(pending_id, overwrite=True)

    assert rebased["status"] == "rebased"
    assert "Rebased" in rebased["summary"]
    assert timeline.pending_show(pending_id)["state"] == "landed"
    assert json.loads(timeline.session.outbox.path.read_text())["flight"] is None

    subsequent = timeline.commit(
        lambda t: t.bundle["parent"].update({"custom": {"after_retry": True}}),
        label="Commit after retry",
        key="retry-overwrite-followup",
    )
    assert subsequent["receipt"]["receipt_id"]
    assert timeline.bundle["parent"]["custom"] == {"after_retry": True}
