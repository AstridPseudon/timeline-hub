"""Positive Runtime coverage for the ordinary occurrence-owned text command.

The retired shot writer remains covered by ``test_shot_text_bindings``.  These
tests use the Agent command provider on a normally bootstrapped timeline and
an occurrence born through the same command path.
"""
from __future__ import annotations

import copy
import hashlib

import pytest

from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import TEXT_MEDIA_TYPE

pytestmark = pytest.mark.integration

OWNER = "occurrence:occurrence-1"
VOICE = {"kind": "voiceover_script", "slot": None}
TEXT_TYPE = TEXT_MEDIA_TYPE


def descriptor(data: bytes) -> dict:
    identity = "sha256:" + hashlib.sha256(data).hexdigest()
    return {"object_id": identity, "digest": identity, "size": len(data), "media_type": TEXT_TYPE}


def _head(editing):
    return editing.service.get_project_timeline(editing.project, editing.timeline)


def _document(editing, revision=None):
    from runtime_protocol.timeline_commit_store import TimelineCommitStore
    from test_timeline_commit_acceptance import validate_prepared

    head = _head(editing)
    return TimelineCommitStore(editing.service.store, validate_prepared=validate_prepared).revision_closure(
        editing.project, editing.timeline, revision or head["head_revision_id"]
    )


def _body(editing, commands, *, dry_run=False):
    head = _head(editing)
    return {
        "api_version": 1,
        "project_id": editing.project,
        "timeline_id": editing.timeline,
        "base_revision_id": head["head_revision_id"],
        "base_publication_id": head["head_publication_id"],
        "commands": copy.deepcopy(commands),
        "dry_run": dry_run,
    }


def _commit(editing, request, key):
    from runtime_protocol.timeline_commit_port import route_path

    return editing.service.commit_timeline(
        editing.project,
        editing.timeline,
        request,
        idempotency_key=key,
        publisher="text-editor",
        invocation_path=route_path(editing.project, editing.timeline),
        authorize=lambda: None,
    )


def _text_command(bundle, capture, pin=None, *, clear=False, select=OWNER):
    return capture(
        bundle,
        select,
        VOICE,
        text=None if clear else pin,
        clear=clear,
        verified_text=[] if clear else [{**pin, "utf8": True}],
    )


def _live(editing):
    return editing.service.list_project_shot_text_bindings(
        editing.project, kind="voiceover_script", slot=None
    )["items"]


@pytest.fixture
def editing(tmp_path, astrid_importable):
    """A fresh Runtime realm using the supplied Agent provider checkout."""
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    from astrid.sdk.timeline.native_initialize import capture_initialize
    from astrid.sdk.timeline import commands
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({"slug": "native-text", "name": "Native text"}, idempotency_key="project")["id"]
    service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    service.create_timeline(project, "main", idempotency_key="timeline")
    state = type("Editing", (), {})()
    state.service, state.project, state.timeline, state.root = service, project, "main", root

    base = _document(state)
    bundle = bundle_from_document(base)
    init = capture_initialize(
        bundle,
        name="Main",
        slug="main",
        output={
            "resolution": "1280x720",
            "fps": 30,
            "file": "output.mp4",
            "background": None,
            "background_scale": None,
        },
    )
    bundle = commands.execute(bundle, [init]).bundle
    track = capture_track_create(
        bundle,
        "parent",
        {"id": "V1", "kind": "visual", "label": "V1", "scale": 1, "fit": "contain", "opacity": 1, "blendMode": "normal"},
    )
    _commit(state, _body(state, [init, track]), "initialize")

    bundle = bundle_from_document(_document(state))
    birth = capture_occurrence_create(
        bundle,
        "occurrence-1",
        "shot-1",
        name="Native text shot",
        track="V1",
        on=0,
        duration=8,
    )
    _commit(state, _body(state, [birth]), "birth")
    try:
        yield state
    finally:
        service.close()


def _put(editing, data: bytes, *, project=None):
    pin = descriptor(data)
    editing.service.ingest(
        project or editing.project,
        data,
        media_type=pin["media_type"],
        idempotency_key="text-" + pin["digest"][7:],
    )
    return pin


def _capture(editing, pin=None, *, clear=False):
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_text_binding import capture_text_binding_set

    return _text_command(bundle_from_document(_document(editing)), capture_text_binding_set, pin, clear=clear)


def _raw_command(editing, pin, *, select=OWNER):
    """Capture once, then alter only the submitted selection under test."""
    command = _capture(editing, _put(editing, b"valid"))
    command["select"] = select
    command["args"]["text"] = pin
    return command


def _restart(editing):
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    editing.service.close()
    editing.service = RuntimeService(editing.root)
    editing.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))


def _inverse(result):
    return {
        "schema_version": 1,
        "op": "timeline.inverse",
        "version": "1",
        "select": None,
        "args": {"publications": [result["receipt"]["receipt_id"]]},
    }


@pytest.mark.parametrize("data", [b"h\xc3\xa9llo\r\n", b""])
def test_native_first_use_is_project_scoped_deterministic_and_replays(editing, data):
    pin = _put(editing, data)
    command = _capture(editing, pin)
    request = _body(editing, [command])
    accepted = _commit(editing, request, "first-text")
    live = _live(editing)[0]
    assert (live["media_id"], live["content_hash"], live["byte_size"], live["mime_type"], live["head"]) == (
        pin["object_id"], pin["digest"], pin["size"], pin["media_type"], 1
    )
    assert editing.service.object(pin["object_id"])[1] == data
    assert _commit(editing, request, "first-text") == accepted
    assert _live(editing)[0] == live
    assert editing.service.store.integrity_report()["ok"]


def test_native_rebind_preserves_event_order_and_exact_inverse_after_restart(editing):
    first, second = _put(editing, b"V1 exact\r\n"), _put(editing, b"V2")
    one = _commit(editing, _body(editing, [_capture(editing, first)]), "v1")
    two = _commit(editing, _body(editing, [_capture(editing, second)]), "v2")
    _restart(editing)
    undone = _commit(editing, _body(editing, [_inverse(two)]), "undo-v2")
    assert undone["data"]["canonical_document"] == one["data"]["canonical_document"]
    assert _live(editing)[0]["media_id"] == first["object_id"]
    redone = _commit(editing, _body(editing, [_inverse(undone)]), "redo-v2")
    assert redone["data"]["canonical_document"] == two["data"]["canonical_document"]
    events = [
        (row["seq"], row["kind"])
        for row in editing.service.store.conn.execute(
            "SELECT seq, kind FROM shot_text_binding_events ORDER BY binding_id, seq"
        )
    ]
    assert events == [(1, "shot.text_binding.created"), (2, "shot.text_binding.rebound"), (3, "shot.text_binding.rebound"), (4, "shot.text_binding.rebound")]


@pytest.mark.parametrize("damage", ["utf8", "limit", "foreign", "size", "digest", "mime"])
def test_native_invalid_text_selection_is_zero_write(editing, damage):
    from runtime_protocol.errors import RuntimeErrorBase

    data = b"invalid text selection"
    project = None
    if damage == "utf8":
        data = b"\xff\xfe"
    elif damage == "limit":
        data = b"x" * (1048576 + 1)
    elif damage == "foreign":
        project = editing.service.create_project({"slug": "foreign", "name": "Foreign"})["id"]
    pin = _put(editing, data, project=project)
    if damage == "size":
        pin["size"] += 1
    elif damage == "digest":
        pin["digest"] = descriptor(b"other")["digest"]
    elif damage == "mime":
        pin["media_type"] = "text/plain"
    command = _raw_command(editing, pin)
    before = tuple(editing.service.store.conn.iterdump())
    with pytest.raises(RuntimeErrorBase):
        _commit(editing, _body(editing, [command]), "invalid-text")
    assert tuple(editing.service.store.conn.iterdump()) == before
    assert _live(editing) == []


def test_native_identity_digest_and_empty_present_clear_inverse(editing):
    empty = _put(editing, b"")
    accepted = _commit(editing, _body(editing, [_capture(editing, empty)]), "empty")
    live = _live(editing)[0]
    assert live["content_hash"] == "sha256:" + hashlib.sha256(b"").hexdigest()
    assert live["byte_size"] == 0 and live["mime_type"] == TEXT_TYPE
    cleared = _commit(editing, _body(editing, [_capture(editing, clear=True)]), "clear")
    assert _live(editing) == []
    _restart(editing)
    restored = _commit(editing, _body(editing, [_inverse(cleared)]), "undo-clear")
    assert restored["data"]["canonical_document"] == accepted["data"]["canonical_document"]
    assert _live(editing)[0]["content_hash"] == empty["digest"]
    assert editing.service.store.integrity_report()["ok"]


def test_unplaced_project_shot_target_is_not_claimed_by_occurrence_command(editing):
    """The old unplaced project-shot capability stays open pending its owner."""
    pin = _put(editing, b"unplaced")
    command = _raw_command(editing, pin, select="shot:unplaced")
    before = tuple(editing.service.store.conn.iterdump())
    from runtime_protocol.errors import RuntimeErrorBase

    with pytest.raises(RuntimeErrorBase):
        _commit(editing, _body(editing, [command]), "unplaced-text")
    assert tuple(editing.service.store.conn.iterdump()) == before
    assert _live(editing) == []
