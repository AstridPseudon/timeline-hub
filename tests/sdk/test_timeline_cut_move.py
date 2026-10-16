"""REHOME criterion 2, over a reserved, disposable multi-layer cut."""
import copy
import json
from pathlib import Path

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.packs.timeline import cli
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands, journal, store
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase

FIXTURE = Path(__file__).parents[1] / "editing_scenarios/fixtures/cut-move.json"
pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


@pytest.fixture
def draft(tmp_path, monkeypatch):
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    tl = Checkout(json.loads(FIXTURE.read_text()))
    tl.save(tmp_path / "cut-move.json", quiet=True)
    return tl


def move(on='"now"', select="c2"):
    return dict(op="cut.move", select=select, args=dict(on=on))


def geometry(tl):
    return [(c.id, c.start, c.duration) for c in tl._cut_clips("c2")]


def test_registered_move_preview_replay_inverse_and_exact_history(draft):
    assert "cut.move" in commands.REGISTRY
    before, disk = draft.document(), draft.path.read_bytes()
    preview = commands.run(draft, move(), dry_run=True)
    assert preview.changed and len(preview.calls) == 1
    assert draft.document() == before and draft.path.read_bytes() == disk
    plan = commands.run(draft, preview.calls[0])
    assert len(plan.calls) == 1 and plan.calls[0].op == "cut.move"
    assert plan.calls[0].resolved == ("cut:c2",) and plan.calls[0].created == ()
    assert plan.calls[0].bindings['"now"'] == "word:s2:1"
    assert geometry(draft) == [("b-plate", 6.4, 1.0), ("b-sfx", 6.6, 0.5), ("b-type", 6.7, 1.0)]
    after = draft.document()
    assert after["shots"]["A"] == before["shots"]["A"]
    assert after["parent"] == before["parent"]
    old = before["shots"]["B"]["internal_timeline"]
    new = after["shots"]["B"]["internal_timeline"]
    assert [c["id"] for c in new["clips"]] == [c["id"] for c in old["clips"]]
    assert new["tracks"] == old["tracks"]
    for left, right in zip(old["clips"], new["clips"]):
        if intent.cut_of(left) != "c2":
            assert left == right
            continue
        # Only placement and its timing relations change; all payload,
        # source ranges, keyframes, opaque values and identities stay exact.
        left, right = copy.deepcopy(left), copy.deepcopy(right)
        for value in (left, right):
            value.pop("at")
            for setter in (intent.set_on, intent.set_until, intent.set_for, intent.set_orphan):
                setter(value, None)
        assert left == right
    replay = rebase(plan.calls, before)
    assert not replay.conflicts and replay.document == after
    inverse = inverse_command(plan.calls, before, after, "pub-cut-move")
    restored = Checkout(copy.deepcopy(after))
    commands.run(restored, inverse)
    assert restored.document() == before  # includes compiled timing and caches
    assert len(list(store._history_dir(draft.path).glob("*.json"))) == 1
    assert len(journal.read(draft.path.with_suffix(".json.journal.jsonl"))[-1].calls) == 1
    draft.undo()
    assert draft.document() == before
    draft.redo()
    assert draft.document() == after
    assert journal.verify(draft.path.with_suffix(".json.journal.jsonl")) == []


def test_public_cut_on_moves_instead_of_only_recording_moment(draft):
    before = draft.document()
    parsed = cli.build_parser(None).parse_args([
        "edit", "--file", str(draft.path), "--cut", "c2", "--on", '"now"', "--no-sweep"])
    assert parsed.handler(parsed) == 0
    moved = Checkout.load(draft.path)
    assert geometry(moved) == [("b-plate", 6.4, 1.0), ("b-sfx", 6.6, 0.5), ("b-type", 6.7, 1.0)]
    records = journal.read(draft.path.with_suffix(".json.journal.jsonl"))
    assert len(records[-1].calls) == 1 and records[-1].calls[0]["op"] == "cut.move"
    after = moved.document()
    moved.undo()
    assert moved.document() == before
    moved.redo()
    assert moved.document() == after


@pytest.mark.parametrize("on", ['"missing"', '"went"', "@-1", "@20", "c2 +1s", "bad ???"])
def test_invalid_or_self_dependent_move_is_atomic(draft, on):
    before, disk = draft.document(), draft.path.read_bytes()
    with pytest.raises(TimelineEditError):
        commands.run(draft, move(on))
    assert draft.document() == before and draft.path.read_bytes() == disk
    assert not list(store._history_dir(draft.path).glob("*.json"))


def test_ambiguous_moment_is_not_pinned_to_nearest(draft):
    voice = draft.clip("b-vo")
    words = intent.words(voice.data)
    words.append([0.85, 0.95, "now"])
    intent.set_line(voice.data, "s2", words)
    before = draft.document()
    with pytest.raises(TimelineEditError):
        commands.run(draft, move())
    assert draft.document() == before


def test_repeated_occurrence_refuses_without_mutation(draft):
    row = copy.deepcopy(draft.bundle["placements"][-1])
    row["occurrence_id"] = "occ-B-again"
    row["placement"]["start_ms"] = 8000
    draft.bundle["placements"].append(row)
    before = draft.document()
    with pytest.raises(TimelineEditError, match="unambiguous occurrence"):
        commands.run(draft, move())
    assert draft.document() == before


def test_rebase_refuses_changed_member_payload_and_offsets(draft):
    before = draft.document()
    plan = commands.run(draft, move())
    for key, value in (("at", 0.4), ("opaque", {"changed": True})):
        head = copy.deepcopy(before)
        card = next(c for c in head["shots"]["B"]["internal_timeline"]["clips"] if c["id"] == "b-type")
        card[key] = value
        result = rebase(plan.calls, head)
        assert result.document is None and result.conflicts
    head = copy.deepcopy(before)
    added = copy.deepcopy(head["shots"]["B"]["internal_timeline"]["clips"][1])
    added["id"] = "b-new-layer"
    head["shots"]["B"]["internal_timeline"]["clips"].append(added)
    result = rebase(plan.calls, head)
    assert result.document is None and result.conflicts


@pytest.mark.parametrize("orphan", [False, True])
def test_picture_sequence_and_orphan_members_keep_shape_and_replay(draft, orphan):
    tl = Checkout(draft.document())
    head = tl.clip("b-plate")
    head.data["hold"] = 0.5
    intent.set_for(head.data, 0.5)
    intent.set_sequence(head.data, "cut-move-steps", 0)
    intent.set_until(head.data, 'clip-start "occurrence:occ-B/clip:b-plate" +1s')
    tail = copy.deepcopy(head.data)
    tail.update(id="b-second-step", at=0.5)
    intent.set_sequence(tail, "cut-move-steps", 1)
    intent.set_until(tail, None)
    tl._internal("B")["clips"].insert(1, tail)
    if orphan:
        intent.set_on(head.data, '"lost"')
        for clip in tl._cut_clips("c2"):
            intent.set_orphan(clip.data, "synthetic lost word")
    before = tl.document()
    offsets = [(c.id, round(c.start - head.start, 6), c.duration) for c in tl._cut_clips("c2")]
    preview = commands.run(tl, move(), dry_run=True)
    plan = commands.run(tl, preview.calls[0])
    assert [(c.id, round(c.start - 6.4, 6), c.duration) for c in tl._cut_clips("c2")] == offsets
    assert all(not intent.orphan(c.data) for c in tl._cut_clips("c2"))
    assert not plan.calls[0].created
    after = tl.document()
    replay = rebase(plan.calls, before)
    assert not replay.conflicts and replay.document == after
    commands.run(tl, inverse_command(plan.calls, before, after, "pub-sequence-move"))
    assert tl.document() == before


def test_negative_layer_offset_is_translated_without_clamping(draft):
    tl = Checkout(draft.document())
    tl.clip("b-plate").data["at"] = 1.0
    tl.clip("b-type").data["at"] = 1.3
    sfx = tl.clip("b-sfx")
    sfx.data["at"] = 0.8
    intent.set_on(sfx.data, "-0.2s")
    commands.run(tl, move())
    assert geometry(tl) == [("b-sfx", 6.2, 0.5), ("b-plate", 6.4, 1.0), ("b-type", 6.7, 1.0)]


@pytest.mark.parametrize("on,target", [("@5.5", 5.5), ("+0.5s", 4.5), ('after "now" +2f', 6.766667)])
def test_existing_moment_grammar_and_idempotent_replay(draft, on, target):
    commands.run(draft, move(on))
    assert draft.clip("b-plate").start == pytest.approx(target)
    if not on.startswith("+"):
        after = draft.document()
        assert not commands.run(draft, move(on)).changed
        assert draft.document() == after
