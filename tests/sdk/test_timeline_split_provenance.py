"""Equivalent native split surfaces retain complete replay and inverse evidence."""
import copy
import json
from dataclasses import replace
from pathlib import Path

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands, inverse
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.identity import cut_reservations, retain_cut_reservation_mark
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.transaction import edit_transaction
from astrid.sdk.timeline_sheet import apply_sheet, render_sheet

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")

PLATE = "occurrence:occ-A/clip:a-plate"
MEMBER = "occurrence:occ-A/clip:a-rocket"
RESERVATION = "config.app.astrid.cut_id_high_water"


@pytest.fixture
def document():
    path = Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json"
    return Checkout(json.loads(path.read_text())).document()


def apply(document, *calls):
    tl = Checkout(copy.deepcopy(document))
    with edit_transaction(tl, "split proof", quiet=True, persist=False) as tx:
        tx.canonical = True
        for call in calls:
            commands.execute(tl, call)
    return tl.document(), tx.plan


def split(document, surface, on='"went"', **kwargs):
    tl = Checkout(copy.deepcopy(document))
    with edit_transaction(tl, "split proof", quiet=True, persist=False) as tx:
        if surface == "cut":
            tl.cut("c1").split(on, **kwargs)
        elif surface == "add-cut":
            tl.add_cut(on, **kwargs)
        else:
            # The original sheet gesture, through its actual parser/producer.
            sheet = render_sheet(tl, cuts=["c1"])
            sheet = sheet.replace(
                '  1.30   sprite  rocket  sprite      R  on "viral"  x=60\n'
                '         why: the opener',
                '         why: the opener\n  0.90 ┃ c1a on "went"\n'
                '         plate   plate   snap-plate  P\n'
                '  1.30   sprite  rocket  sprite      R  on "viral"  x=60',
            )
            assert '┃ c1a on "went"' in sheet
            apply_sheet(tl, sheet)
    return tl.document(), tx.plan


def assert_record(plan):
    assert len(plan.calls) == 1
    call = plan.calls[0]
    assert call.op == "cut.split" and call.select == "c1"
    assert call.resolved == ("cut:c1",)
    assert call.created == ("cut:c1a", "occurrence:occ-A/clip:c1a-00-am-snap-plate-01")
    picture = call.created[1]
    direct = {f"{PLATE}::intent.until", f"{PLATE}::hold", f"{MEMBER}::intent.cut"}
    consequences = {"cut:c1a::", f"{picture}::", f"parent::{RESERVATION}"}
    assert call.authorship == {**dict.fromkeys(direct, "direct"),
                               **dict.fromkeys(consequences, "consequence")}
    assert set(call.expect) == direct
    assert call.expect[f"{PLATE}::intent.until"] == {"state": "absent"}
    assert call.expect[f"{PLATE}::hold"] == {"state": "present", "value": 4.0}
    assert call.expect[f"{MEMBER}::intent.cut"] == {"state": "present", "value": "c1"}
    assert {(w["id"], w["path"]) for w in plan.direct_writes} == {
        (PLATE, "intent.until"), (PLATE, "hold"), (MEMBER, "intent.cut")}
    assert {(w["id"], w["path"]) for w in plan.consequences} == {
        ("cut:c1a", ""), (picture, ""), ("parent", RESERVATION)}
    for effect in plan.consequences:
        assert "cause" in effect
        assert effect["cause"] == 0
        assert effect["before"] == {"state": "absent"}
        assert effect["after"]["state"] == "present"
    return call


@pytest.mark.parametrize("on", ['"went"', 0.9, "c1 +0.9s"])
def test_equivalent_split_surfaces_record_the_same_complete_policy(document, on):
    expected, native = split(document, "cut", on)
    actual, added = split(document, "add-cut", on)
    call = assert_record(added)
    assert call.to_json() == assert_record(native).to_json()
    assert added.direct_writes == native.direct_writes
    assert added.consequences == native.consequences
    assert actual == expected
    assert call.bindings
    assert apply(document, *added.calls)[0] == expected
    replay = rebase(added.calls, document)
    assert not replay.conflicts
    assert replay.document == expected
    assert replay.plan.calls == added.calls
    assert replay.plan.consequences == added.consequences


def test_original_sheet_split_matches_native_record_and_guards(document):
    expected, native = split(document, "cut")
    actual, sheet = split(document, "sheet")
    call = assert_record(sheet)
    assert call.args == {"on": '"went"', "id": "c1a", "picture": "P"}
    assert call.bindings == {'"went"': "word:s1:1", "c1a": "cut:c1a:start"}
    assert call.to_json() == assert_record(native).to_json()
    assert sheet.direct_writes == native.direct_writes
    assert sheet.consequences == native.consequences
    assert actual == expected
    assert apply(document, *sheet.calls)[0] == expected


def test_explicit_split_identity_picture_and_add_cut_after_validation(document):
    expected, native = split(document, "cut", id="c1d", picture="P")
    actual, added = split(document, "add-cut", after="c1", id="c1d", picture="P")
    assert actual == expected
    assert added.calls == native.calls
    assert added.consequences == native.consequences
    assert added.calls[0].args["id"] == "c1d"
    assert "cut:c1d" in added.calls[0].created
    assert apply(document, *added.calls)[0] == expected
    tl = Checkout(document)
    before = tl.document()
    with pytest.raises(commands.TimelineEditError, match="inside c1, not c2"):
        tl.add_cut('"went"', after="c2")
    assert tl.document() == before
    with pytest.raises(commands.CommandError, match="missing required argument"):
        commands.run(tl, dict(op="timeline.add-cut", select=None, args={}))
    assert tl.document() == before


def test_split_uses_the_same_recording_context_with_an_adopted_music_bed(document):
    from astrid.sdk.timeline.bed_adoption import adopt_music_bed

    owner = "occurrence:occ-A/clip:a-music"
    document = adopt_music_bed(document, [owner], alignment={
        owner: {"confidence": 1, "source_offset_s": 0}})
    expected, native = split(document, "cut")
    actual, added = split(document, "add-cut")
    assert actual == expected
    assert added.calls == native.calls
    assert added.direct_writes == native.direct_writes
    assert added.consequences == native.consequences
    assert apply(document, *added.calls)[0] == expected


@pytest.mark.parametrize("surface", ["cut", "add-cut", "sheet"])
def test_split_rebases_over_unrelated_work(document, surface):
    _, plan = split(document, surface)
    head, _ = apply(document, dict(op="clip.set", select="b-type", args={"text": "later"}))
    original = copy.deepcopy(head)
    result = rebase(plan.calls, head)
    assert not result.conflicts and result.id_map == {}
    assert result.plan.calls == plan.calls
    assert result.plan.consequences == plan.consequences
    assert Checkout(result.document).clip("b-type").params["text"] == "later"
    assert Checkout(result.document).clip("a-plate").end == pytest.approx(0.9)
    assert head == original


@pytest.mark.parametrize("surface", ["cut", "add-cut", "sheet"])
@pytest.mark.parametrize("conflict", ["source", "member", "binding", "occupied-id", "authorship",
                                     "consequence-authorship", "lost-precondition", "lost-created"])
def test_recorded_split_refuses_changed_dependencies_atomically(document, surface, conflict):
    _, plan = split(document, surface)
    calls = [plan.calls[0].to_json()]
    head = Checkout(copy.deepcopy(document))
    if conflict == "source":
        head.clip("a-plate").data["hold"] = 3.5
        message, path = "same-property", "hold"
    elif conflict == "member":
        intent.set_cut(head.clip("a-rocket").data, "c2")
        message, path = "same-property", "intent.cut"
    elif conflict == "binding":
        calls[0]["bindings"]['"went"'] = "word:s1:0"
        message, path = "bindings", "bindings"
    elif conflict == "occupied-id":
        row = copy.deepcopy(head.clip("a-plate").data)
        row["id"] = calls[0]["created"][1].split("/clip:")[1]
        head._internal("A")["clips"].append(row)
        message, path = "created", "created"
    elif conflict == "authorship":
        calls[0]["authorship"][f"{MEMBER}::intent.cut"] = "consequence"
        message, path = "Replay changed direct paths", ""
    elif conflict == "consequence-authorship":
        calls[0]["authorship"]["cut:c1a::"] = "direct"
        message, path = "Replay changed direct paths", ""
    elif conflict == "lost-precondition":
        del calls[0]["expect"][f"{MEMBER}::intent.cut"]
        message, path = "missing its original precondition", ""
    else:
        calls[0]["created"] = ["cut:c1a"]
        message, path = "unrecorded identity allocation", ""
    before, recorded = head.document(), copy.deepcopy(calls)
    with pytest.raises(commands.TimelineEditError, match=message):
        with edit_transaction(head, "refused replay", quiet=True, persist=False) as tx:
            tx.canonical = True
            commands.execute(head, calls[0])
    # Rebase may remap occupied generated IDs using the existing cut fork
    # policy; exact replay above must refuse an occupied ID, never overwrite it.
    if conflict != "occupied-id":
        result = rebase(calls, before)
        assert result.conflicts and result.document is None and result.plan is None
        assert result.conflicts[0]["path"] == path
    else:
        # A caller-supplied mapping cannot bypass collision protection either.
        occupied = copy.deepcopy(head.clip("a-plate").data)
        occupied["id"] = "occupied-picture"
        head._internal("A")["clips"].append(occupied)
        result = rebase(plan.calls, head.document(), id_map={
            plan.calls[0].created[1]: "occurrence:occ-A/clip:occupied-picture"})
        assert result.conflicts[0]["path"] == "created" and result.document is None
        head._internal("A")["clips"].pop()
    assert head.document() == before and calls == recorded


@pytest.mark.parametrize("surface", ["cut", "add-cut", "sheet"])
@pytest.mark.parametrize("notes", ["absent", "empty", "populated"])
def test_exact_authored_inverse_redo_and_fresh_allocation(document, surface, notes):
    if notes != "absent":
        intent._film_w(document)["cut_notes"] = {} if notes == "empty" else {
            "c2": {"why": "keep later notes", "opaque": {"null": None, "empty": {}}}}
    # Opaque authored data participates in exact restoration and picture copy.
    tl = Checkout(document)
    tl.clip("a-plate").data["opaque"] = {"null": None, "values": [False, 0, {}]}
    tl.clip("a-rocket").data["opaque"] = {"future": "member"}
    document = tl.document()
    after, plan = split(document, surface)
    undo = inverse.inverse_command(plan.calls, document, after, "split-publication",
                                   consequences=plan.consequences)
    restored, undo_plan = apply(after, undo)
    mark = cut_reservations(after)
    expected = copy.deepcopy(document)
    retain_cut_reservation_mark(expected, mark)
    assert restored == expected
    assert cut_reservations(restored) == mark
    assert apply(after, *undo_plan.calls)[0] == restored
    redo = inverse.inverse_command(undo_plan.calls, after, restored, "undo-publication",
                                   consequences=undo_plan.consequences)
    redone, redo_plan = apply(restored, redo)
    assert redone == after
    assert apply(restored, *redo_plan.calls)[0] == after
    fresh, fresh_plan = split(restored, "cut")
    assert fresh_plan.calls[0].args["id"] == "c1b"
    assert set(fresh_plan.calls[0].created).isdisjoint(plan.calls[0].created)
    assert cut_reservations(fresh)["suffixes"]["1"] == 2


@pytest.mark.parametrize("mutation", ["expect", "binding", "created", "authorship", "cause",
                                     "missing-cause", "consequences"])
def test_planted_loss_or_tampering_is_detected_by_complete_record_assertions(document, mutation):
    _, plan = split(document, "cut")
    call = plan.calls[0]
    if mutation == "cause":
        bad = replace(plan, consequences=tuple({**w, "cause": 1} for w in plan.consequences))
    elif mutation == "missing-cause":
        bad = replace(plan, consequences=tuple({k: v for k, v in w.items() if k != "cause"}
                                               for w in plan.consequences))
    elif mutation == "consequences":
        bad = replace(plan, consequences=())
    elif mutation == "binding":
        bad = replace(plan, calls=(replace(call, bindings={}),))
    else:
        field = "expect" if mutation == "expect" else mutation
        value = () if mutation == "created" else {}
        bad = replace(plan, calls=(replace(call, **{field: value}),))
    with pytest.raises(AssertionError):
        assert_record(bad)
        assert bad.calls[0].bindings == {'"went"': "word:s1:1", "c1a": "cut:c1a:start"}
