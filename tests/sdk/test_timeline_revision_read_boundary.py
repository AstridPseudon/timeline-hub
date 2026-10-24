"""Revision inspection and authenticated capture have distinct source custody."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline import store
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet
from tests.sdk.test_timeline_restructure import restructure_runtime  # noqa: F401
from tests.sdk.test_timeline_restructure_guarded_runtime import (
    restructure_inverse_runtime,  # noqa: F401
)


def test_revision_inspection_does_not_replace_authenticated_session_capture(
    restructure_inverse_runtime, tmp_path,  # noqa: F811
):
    env = restructure_inverse_runtime
    session = TimelineSession.open(env.project, "t", client=env.client,
                                   outbox_path=tmp_path / "boundary.json")
    state = session.outbox.read()
    base = state["base"]
    ordinary = store.fetch_bundle(env.project, "t", client=env.client,
                                  revision_id=base["revision_id"])
    original = copy.deepcopy(ordinary)
    assert "_runtime_document" not in ordinary["source_mapping"]
    assert "publication_id" not in ordinary["base_parent"]
    command = capture_move(ordinary, "occurrence:occ-film/clip:cross", 4)
    preview = execute(ordinary, [command]).bundle
    assert preview["source_mapping"] == ordinary["source_mapping"]
    assert ordinary == original

    document = env.document()
    authenticated = {
        **ordinary,
        "base_parent": {**ordinary["base_parent"], "publication_id": base["publication_id"]},
        "source_mapping": {**ordinary["source_mapping"], "_runtime_document": document},
    }
    assert session._bundle(state) == authenticated
    assert NativeSheet.export(session)._bundle == authenticated
    assert NativeSheet.load(session)._bundle == authenticated
    canonical = bundle_from_document(document)
    assert canonical["source_mapping"] == authenticated["source_mapping"]
    opened = timeline.open(env.project, "t", client=env.client,
                           outbox_path=tmp_path / "public.json")
    assert opened.bundle["source_mapping"] == ordinary["source_mapping"]
    assert opened._execution_bundle(opened.bundle) == authenticated


def test_clean_session_capture_refuses_a_mismatched_pair_without_writes(
    restructure_inverse_runtime, tmp_path,  # noqa: F811
):
    env = restructure_inverse_runtime
    session = TimelineSession.open(env.project, "t", client=env.client,
                                   outbox_path=tmp_path / "wrong-pair.json")
    state = session.outbox.read()
    history = env.client.timelines.history(env.project, "t", limit=200).data
    historical = next(row for row in history["items"]
                      if row["revision_id"] != state["base"]["revision_id"])
    state["base"]["publication_id"] = historical["publication_id"]
    stored = tuple(env.service.store.conn.iterdump())
    outbox = session.outbox.path.read_bytes()
    calls = copy.deepcopy(env.calls)
    with pytest.raises(TimelineEditError, match="original revision/publication pair changed"):
        session._bundle(state)
    assert tuple(env.service.store.conn.iterdump()) == stored
    assert session.outbox.path.read_bytes() == outbox
    assert env.calls == calls
