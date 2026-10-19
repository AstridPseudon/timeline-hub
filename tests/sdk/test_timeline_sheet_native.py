"""Bound cut-sheet cells use native capture and the real durable session, offline."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.sync import CommitConflict
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline_sheet import NativeSheet, SheetError, apply_sheet
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.sdk.test_timeline_sync import connected, initial_bundle, open_session  # noqa: F401


def sheet_for(bundle):
    return NativeSheet(bundle, basis={"revision_id": bundle["base_parent"]["revision_id"],
                                      "publication_id": "pub0"})


def edit_cell(text, ref, value, *, label=False):
    """Act like an editor keeping the hidden ID binding beside its cell."""
    lines = text.splitlines()
    suffix = " # ref " + json.dumps(ref)
    for i, line in enumerate(lines):
        if line.endswith(suffix):
            body = line[:-len(suffix)]
            if label:
                body = body[:body.index("label=")] + "label=" + value
            else:
                body = body.replace(body.split()[0], value, 1)
            lines[i] = body + suffix
            return "\n".join(lines) + "\n"
    raise AssertionError(f"no bound row for {ref}")


def test_preview_and_unchanged_cells_have_no_writes_or_io(connected, monkeypatch):  # noqa: F811
    session = open_session(connected)
    client, generated, path = connected
    before = path.read_bytes()
    bundle = initial_bundle()
    original = copy.deepcopy(bundle)
    sheet = sheet_for(bundle)
    monkeypatch.setattr(Checkout, "save", lambda *a, **kw: pytest.fail("legacy save"))
    monkeypatch.setattr(Checkout, "__init__", lambda *a, **kw: pytest.fail("legacy projection"))
    bundle["parent"]["clips"].clear()  # caller mutation cannot change the pinned original
    plan = sheet.apply(sheet.text, session=session)
    assert plan.commands == plan.records == []
    assert plan.bundle == original
    edited = edit_cell(sheet.text, "parent/clip:a", "5")
    plan = sheet.apply(edited, session=session)
    assert plan.commands == [capture_move(original, "parent/clip:a", 5)]
    assert State(plan.bundle).entity("parent/clip:b") == State(original).entity("parent/clip:b")
    assert generated.calls == client.reads == []
    assert path.read_bytes() == before
    assert sheet.preview(edit_cell(sheet.text, "parent/clip:a", "0.00")).commands == []


@pytest.mark.parametrize("before", ["absent", None, "", "Old", "clear"])
@pytest.mark.parametrize("value", ['""', "clear", '"clear"'])
def test_label_clear_is_distinct_from_empty_and_literal_clear(before, value):
    original = initial_bundle()
    track = State(original).entity("parent/track:picture")
    if before != "absent":
        track["label"] = before
    sheet = sheet_for(original)
    edited = edit_cell(sheet.text, "parent/track:picture", value, label=True)
    plan = sheet.preview(edited)
    expected = copy.deepcopy(track)
    if value == "clear":
        expected.pop("label", None)
    else:
        expected["label"] = json.loads(value)
    assert State(plan.bundle).entity("parent/track:picture") == expected
    if expected == track:
        assert plan.commands == []
    else:
        assert plan.commands == [capture_track_set(original, "parent/track:picture",
            values={} if value == "clear" else {"label": json.loads(value)},
            clear=["label"] if value == "clear" else [])]
    assert sheet.preview(sheet.text).commands == []


@pytest.mark.parametrize("label", ['say " # keep', 'path\\" # keep', "café", "line\nnew", "clear"])
def test_label_json_text_round_trips_without_comment_truncation(label):
    original = initial_bundle()
    sheet = sheet_for(original)
    plan = sheet.preview(edit_cell(sheet.text, "parent/track:picture", json.dumps(label), label=True))
    assert plan.commands == [capture_track_set(original, "parent/track:picture", values={"label": label})]
    State(original).entity("parent/track:picture")["label"] = label
    sheet = sheet_for(original)
    assert sheet.preview(sheet.text).commands == []


@pytest.mark.parametrize("change", [
    lambda text: text.replace("  type", "  other", 1),
    lambda text: text.replace("picture  a", "elsewhere  a", 1),
    lambda text: text.replace('"parent/clip:a"', '"parent/clip:missing"', 1),
    lambda text: text.replace('"parent/clip:a"', '"parent/clip:b"', 1),
    lambda text: text.replace(' # ref "parent/clip:a"', "", 1),
    lambda text: text.replace('"publication_id": "pub0"', '"publication_id": "different"'),
    lambda text: "\n".join(line for line in text.splitlines() if '"parent/clip:a"' not in line),
    lambda text: text + '  2  picture new media # ref "parent/clip:new"\n',
    lambda text: text.replace(" # ref", " extra=lost # ref", 1),
    lambda text: text.replace(" # ref", " ~ignored # ref", 1),
])
def test_unsupported_or_unbound_edits_are_refused_before_queueing(connected, change):  # noqa: F811
    session = open_session(connected)
    _, generated, path = connected
    sheet = sheet_for(initial_bundle())
    before = path.read_bytes()
    with pytest.raises(SheetError):
        sheet.apply(change(sheet.text), session=session, dry_run=False)
    assert path.read_bytes() == before and generated.calls == []


def test_native_rows_cannot_fall_into_the_legacy_sheet_writer():
    with pytest.raises(SheetError, match="NativeSheet"):
        apply_sheet(Checkout({}), sheet_for(initial_bundle()).text)
    with pytest.raises(SheetError, match="NativeSheet"):
        apply_sheet(Checkout({}), "clips\ntracks\n")


def test_bad_basis_and_unsupported_native_timing_fail_explicitly():
    original = initial_bundle()
    with pytest.raises(SheetError, match="revision"):
        NativeSheet(original, basis={"revision_id": "wrong", "publication_id": "pub0"})
    for basis in ({}, {"revision_id": "r0", "publication_id": ""}):
        with pytest.raises(ValueError, match="verified publication"):
            NativeSheet(original, basis=basis)
    original["parent"]["clips"][0]["time_map"] = {"kind": "piecewise"}
    sheet = sheet_for(original)
    with pytest.raises(CommandError, match="time_map"):
        sheet.preview(edit_cell(sheet.text, "parent/clip:a", "5"))


def test_atomic_batch_commit_lost_ack_restart_and_undo(connected):  # noqa: F811
    session = open_session(connected)
    client, generated, path = connected
    sheet = sheet_for(initial_bundle())
    edited = edit_cell(sheet.text, "parent/clip:a", "5")
    edited = edit_cell(edited, "parent/track:picture", '"Picture"', label=True)
    expected = sheet.preview(edited).commands
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        sheet.apply(edited, session=session, dry_run=False, idempotency_key="sheet-once")
    flight = json.loads(path.read_bytes())["flight"]
    assert json.loads(flight["body"])["commands"] == expected
    assert json.loads(flight["body"])["source"] == {"via": "sheet"}
    assert len(generated.accepted) == 1
    session = open_session(connected)
    reads = list(client.reads)
    result = sheet.apply(edited, session=session, dry_run=False)
    assert client.reads == reads  # retry uses original capture without fetching a newer head
    assert generated.calls[0] == generated.calls[1]
    assert result["data"]["accepted_revision_id"] == "r1"
    assert json.loads(path.read_bytes())["pending"] == []
    session.undo(["pub1"])
    assert generated.bundles["r2"] == initial_bundle()


@pytest.mark.parametrize("mismatch", ["project", "timeline", "revision", "publication", "bundle", "pending"])
def test_commit_requires_exact_pinned_session_and_never_replaces_pending(connected, mismatch):  # noqa: F811
    session = open_session(connected)
    _, generated, path = connected
    original = initial_bundle()
    if mismatch == "bundle":
        original["parent"]["clips"][0]["params"]["opaque"] = True
    sheet = sheet_for(original)
    if mismatch in ("project", "timeline"):
        sheet._bundle[mismatch + "_id"] = "other"
    if mismatch in ("revision", "publication"):
        sheet._basis[mismatch + "_id"] = "other"
    if mismatch == "pending":
        session.queue_move("parent/clip:b", 8)
    before = path.read_bytes()
    with pytest.raises(SheetError):
        sheet.apply(edit_cell(sheet.text, "parent/clip:a", "5"), session=session, dry_run=False)
    assert path.read_bytes() == before and generated.calls == []


def test_stale_original_guards_conflict_without_refreshing(connected):  # noqa: F811
    session = open_session(connected)
    _, generated, path = connected
    original = initial_bundle()
    sheet = sheet_for(original)
    edited = edit_cell(sheet.text, "parent/clip:a", "5")
    generated.bundles["other"] = execute(original, [capture_move(original, "parent/clip:a", 7)]).bundle
    generated.head = {"revision_id": "other", "publication_id": "other-pub"}
    with pytest.raises(CommitConflict):
        sheet.apply(edited, session=session, dry_run=False)
    state = json.loads(path.read_bytes())
    assert state["pending"] == [capture_move(original, "parent/clip:a", 5)]
    assert state["flight"] is not None and state["conflict"]
    assert generated.accepted == {}


def test_disjoint_head_edit_rebases_without_writing_unchanged_cells(connected):  # noqa: F811
    session = open_session(connected)
    _, generated, _ = connected
    original = initial_bundle()
    sheet = sheet_for(original)
    other = capture_move(original, "parent/clip:b", 7)
    generated.bundles["other"] = execute(original, [other]).bundle
    generated.head = {"revision_id": "other", "publication_id": "other-pub"}
    result = sheet.apply(edit_cell(sheet.text, "parent/clip:a", "5"), session=session, dry_run=False)
    assert result["data"]["status"] == "rebased"
    assert len(result["data"]["commands"]) == 1
    assert State(generated.bundles["r1"]).entity("parent/clip:b")["at"] == 7
