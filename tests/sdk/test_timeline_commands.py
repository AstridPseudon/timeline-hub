"""Focused producer proofs over disposable detached timeline fixtures."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.packs.timeline import cli
from astrid.sdk import timeline_checkout as tc
from astrid.sdk.timeline import commands, journal, store
from astrid.sdk.timeline.checkout import Checkout, Clip, Cut
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline_sheet import apply_sheet, render_sheet

FIXTURE = Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json"


@pytest.fixture
def draft(tmp_path, monkeypatch):
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    bundle = json.loads(FIXTURE.read_text())
    for seam in [tc, store]:
        monkeypatch.setattr(seam, "resolve_ids", lambda *a, **k: ("p", "t", "rev-0"))
        monkeypatch.setattr(seam, "fetch_bundle", lambda *a, **k: copy.deepcopy(bundle))
    return Checkout.draft("P", "t")


def command(op="clip.set", select="c1.rocket", **args):
    return dict(op=op, select=select, args=args)


def test_restore_is_registered_but_local_config_cannot_grant_image_authority(draft):
    before = draft.document()
    value = command("timeline.restore", None, revision_id="opaque", content_digest="sha256:" + "a" * 64)
    assert commands.REGISTRY["timeline.restore"].boundary == "image"
    with pytest.raises(commands.CommandError, match="verified image"):
        commands.run(draft, value)
    assert draft.document() == before
    with pytest.raises(commands.CommandError, match="must run alone"):
        commands.execute(draft, value)
    assert draft.document() == before


def files(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_mutator_enumeration_is_closed_and_detects_a_new_public_method(monkeypatch):
    assert commands.unregistered_mutators([Clip, Checkout, Cut]) == []
    monkeypatch.setattr(Clip, "unregistered_write", lambda self: self.data.update(hold=10), raising=False)
    assert commands.unregistered_mutators([Clip, Checkout, Cut]) == ["Clip.unregistered_write"]


def test_registry_covers_every_inventory_and_current_edit_flag():
    inventory = json.loads((FIXTURE.parents[2] / "parity/inventory.json").read_text())
    table = commands.flag_inventory_table(inventory)
    assert len(table) == len(inventory["commands"]["timelines.edit"]["flags"])
    assert table == json.loads((FIXTURE.parents[2] / "parity/edit-command-flags.json").read_text())
    parser = cli.build_parser(None)._subparsers._group_actions[0].choices["edit"]
    for action in parser._actions:
        if action.option_strings and action.dest != "help":
            assert commands.EDIT_FLAG_OPERATIONS[action.dest] in commands.REGISTRY


def test_skill_edit_flag_reference_matches_canonical_sources():
    from tools.parity.edit_flag_reference import TARGET, render_reference

    assert TARGET.read_text(encoding="utf-8") == render_reference()


def test_command_preview_is_populated_replayable_and_writes_nothing(draft):
    root = Path(draft.path).parents[3]
    before, disk = draft.document(), files(root)
    preview = commands.run(draft, command(x=120), dry_run=True)
    assert preview.changed and preview.calls
    assert draft.document() == before
    assert files(root) == disk
    assert preview.calls[0].to_json()["op"] == "clip.set"
    assert preview.calls[0].resolved == ("occurrence:occ-A/clip:a-rocket",)
    committed = commands.run(draft, preview.calls[0])
    assert committed.changed and draft.clip("c1.rocket").get("x") == 120
    assert journal.read(journal.journal_path("p", "t"))[-1].calls
    assert journal.verify(journal.journal_path("p", "t")) == []
    assert len(list(store._history_dir(Path(draft.path)).glob("*.json"))) == 1


def test_timeline_skill_collection_batch_recipe_runs_as_one_undo_step(draft):
    selected = draft.clips(element="am-sprite")
    calls = [
        {"op": "clip.set", "select": clip.address,
         "args": {"x": 120}}
        for clip in selected
    ]
    batch = {"op": "timeline.batch", "select": None, "args": {"commands": calls}}
    before, disk = draft.document(), files(Path(draft.path).parents[3])
    before_x = draft.clip("c1.rocket").params.get("x", 0)
    preview = commands.run(draft, batch, dry_run=True)
    assert preview.changed and preview.calls
    assert draft.document() == before
    assert files(Path(draft.path).parents[3]) == disk
    with draft.edit("Set selected sprite positions"):
        draft.batch(calls)
    assert draft.clip("c1.rocket").params.get("x", 0) != before_x
    assert draft.undo(1)
    assert draft.clip("c1.rocket").params.get("x", 0) == before_x


@pytest.mark.parametrize("value", [None, [], {}, {"op":"clip.set","select":2,"args":{}},
    {"op":"not.registered","select":None,"args":{}}, command(x=float("nan")),
    command(op="clip.set-duration", seconds="bad"), command(op="clip.set-duration", seconds=None),
    command(op="clip.set-duration", seconds=-1), command(op="clip.clear", keys=["bad"])])
def test_invalid_commands_are_typed_and_leave_memory_and_file_unchanged(draft, value):
    before, text = draft.document(), Path(draft.path).read_bytes()
    with pytest.raises(TimelineEditError):
        commands.run(draft, value)
    assert draft.document() == before
    assert Path(draft.path).read_bytes() == text
    assert not list(store._history_dir(Path(draft.path)).glob("*.json"))


def test_batch_failure_restores_earlier_writes_and_does_not_make_undo(draft):
    before, disk = draft.document(), Path(draft.path).read_bytes()
    with pytest.raises(TimelineEditError):
        commands.run(draft, command(op="timeline.batch", select=None, commands=[command(x=120), command(zzbogus=2)]))
    assert draft.document() == before
    assert Path(draft.path).read_bytes() == disk
    assert not draft._journal and not draft._pending_calls
    assert journal.read(journal.journal_path("p", "t"))[-1].outcome == "rolled-back"


@pytest.mark.parametrize("mutation", ["curve", "unrelated"])
def test_compiler_prefix_refuses_unrecorded_state_after_audio_fade(draft, mutation):
    before, disk = draft.document(), Path(draft.path).read_bytes()
    clip = draft.clip("a-music")
    data = clip.data
    with pytest.raises(commands.CommandError, match="Compiler prefix evidence does not match the executed candidate"):
        with draft.edit("Unrecorded audio curve"):
            clip.set_look(fade_out=0.5)
            if mutation == "curve":
                clip.params["fadeOutCurve"] = "equal-power"
            else:
                draft.clip("c1.rocket").data.setdefault("app", {})["foreign"] = {"nested": [True, None, 7]}
    assert draft.document() == before and Path(draft.path).read_bytes() == disk
    assert clip.data is data and clip.data == draft.clip("a-music").data
    assert not draft._journal and not draft._pending_calls
    assert not list(store._history_dir(Path(draft.path)).glob("*.json"))
    assert journal.read(journal.journal_path("p", "t"))[-1].outcome == "rolled-back"
    assert journal.verify(journal.journal_path("p", "t")) == []


def test_failed_timing_and_quick_check_restore_the_whole_transaction(draft, monkeypatch):
    before, text = draft.document(), Path(draft.path).read_bytes()
    def crash(*a, **k):
        raise RuntimeError("injected compiler fault")
    monkeypatch.setattr(draft, "resolve", crash)
    with pytest.raises(RuntimeError, match="injected compiler fault"):
        commands.run(draft, command(x=120))
    assert draft.document() == before and Path(draft.path).read_bytes() == text


def test_null_is_a_value_and_clear_removes_presence_including_formula(draft):
    card = draft.clip("c2.card")
    card.set(italicWord="Live")
    draft.save(quiet=True)
    before = draft.document()
    with pytest.raises(TimelineEditError, match=r"--clear italicWord"):
        commands.run(draft, command(select="c2.card", italicWord=None))
    assert draft.document() == before
    preview = commands.run(draft, command(op="clip.clear", select="c2.card", keys=["italicWord"]), dry_run=True)
    assert preview.changed and "italicWord" in draft.clip("c2.card").params
    commands.run(draft, preview.calls[0])
    assert "italicWord" not in draft.clip("c2.card").params
    assert not commands.run(draft, command(op="clip.clear", select="c2.card", keys=["italicWord"])).changed


def test_pixels_convert_once_for_add_set_and_replay(draft):
    add = command(op="timeline.add", select=None, element="am-sprite", at='"now"',
                  layer="pin", hold=1.5, params={"x":600,"y":300})
    preview = commands.run(draft, add, dry_run=True)
    commands.run(draft, preview.calls[0])
    clip = draft.clip("c2.pin")
    assert clip.params["x"] == 100 and clip.get("x") == 600
    assert clip.params["y"] == 50 and clip.get("y") == 300
    commands.run(draft, command(select="c2.pin", x=600))
    assert draft.clip("c2.pin").params["x"] == 100
    assert not commands.run(draft, command(select="c2.pin", x=600)).changed


def test_sheet_zero_take_gap_keeps_its_existing_lead_in_semantics(draft):
    # A take gap of zero and closing silence before a spoken word are distinct
    # requests. Keep this projection behavior while the conformance scenario now
    # uses the explicit close-gap OpCall to express its actual intent.
    text = render_sheet(draft, cuts=["c1"]).replace('s1  "It went viral."', 's1  "It went viral."  gap 0')
    apply_sheet(draft, text)
    assert draft.voice("s1").gap_after == 0
    assert draft.time('"Live"') == pytest.approx(1.8)


def test_harness_never_counts_a_programming_crash_as_refusal():
    from tests.editing_conformance.runner import parse_scenario, run_scenario, evaluate
    scenario = parse_scenario(dict(id="code.crash.refusal", source="RUNNER", intent="crash is not refusal",
        fixture="tiny", expect="refused", python='raise RuntimeError("programming fault")'))
    result = run_scenario(scenario)
    assert not result["python"].refused
    assert ("python", "runs") in evaluate(scenario, result)


def test_cli_json_command_and_clear_preview(draft, capsys):
    capsys.readouterr()
    parsed = cli.build_parser(None).parse_args(["edit","t","--project","P","--command",json.dumps(command(x=120)),"--dry-run"])
    before = files(Path(draft.path).parents[3])
    assert parsed.handler(parsed) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["changed"] and payload["calls"]
    assert files(Path(draft.path).parents[3]) == before


def test_timing_cannot_overwrite_an_explicit_param(draft, monkeypatch):
    before = draft.document()
    text = Path(draft.path).read_bytes()
    clip = draft.clip("c1.rocket")
    def overwrite():
        draft.clip("c1.rocket").data["params"]["x"] = 999
        return []
    monkeypatch.setattr(draft, "resolve", overwrite)
    with pytest.raises(commands.CommandError, match="timing replaced an explicit write"):
        commands.run(draft, command(x=120))
    assert draft.document() == before
    assert Path(draft.path).read_bytes() == text
    assert clip.get("x") == 60


def test_future_version_refuses_before_mutation(draft):
    draft.bundle["parent"]["config"].setdefault("app", {}).setdefault("astrid", {})["v"] = 99
    before = draft.document()
    with pytest.raises(TimelineEditError, match="unknown Astrid feature version"):
        commands.run(draft, command(x=120))
    assert draft.document() == before


def test_clearing_a_formula_is_presence_aware(draft):
    from astrid.sdk import timeline_intent as intent
    draft.clip("c1.rocket").set(x='"went"')
    assert "params.x" in intent.formulas(draft.clip("c1.rocket").data)
    commands.run(draft, command(op="clip.clear", keys=["x"]))
    clip = draft.clip("c1.rocket")
    assert "x" not in clip.params
    assert "params.x" not in intent.formulas(clip.data)


def test_emitted_calls_use_the_existing_opcall_schema(draft):
    import jsonschema
    schema = json.loads((FIXTURE.parents[3] / "schemas/change-contract/opcall.schema.json").read_text())
    plan = commands.run(draft, command(x=120), dry_run=True)
    for call in plan.calls:
        jsonschema.Draft202012Validator(schema).validate(call.to_json())


def test_cli_refusal_returns_a_typed_error_and_does_not_ignore_other_flags(draft, capsys):
    capsys.readouterr()
    before = draft.document()
    parsed = cli.build_parser(None).parse_args(["edit", "t", "--project", "P", "--command", json.dumps(command(x=120)), "--set", "y=200"])
    assert parsed.handler(parsed) == 2
    error = json.loads(capsys.readouterr().err)["error"]
    assert error["code"] == "invalid_edit_command"
    assert "cannot be combined" in error["message"]
    assert Checkout.draft("P", "t").document() == before


def test_file_edit_and_words_keep_their_cli_and_journal_paths(draft, tmp_path, capsys):
    target = tmp_path / "disposable.checkout.json"
    draft.save(target, quiet=True)
    assert cli.build_parser(None).parse_args(["edit", "--file", str(target), "--clip", "c1.rocket", "--set", "x=120"]).handler(
        cli.build_parser(None).parse_args(["edit", "--file", str(target), "--clip", "c1.rocket", "--set", "x=120"])) == 0
    words = cli.build_parser(None).parse_args(["words", "--file", str(target), "--find", "viral"])
    assert words.handler(words) == 0
    log = target.with_suffix(target.suffix + ".journal.jsonl")
    assert log.is_file() and journal.verify(log) == []
    rows = journal.read(log)
    assert rows[-1].calls and rows[-1].outcome == "changed"
    assert "viral" in capsys.readouterr().out


def test_history_boundaries_are_runner_entries_and_keep_multi_step_undo_redo(draft):
    before = draft.document()
    commands.run(draft, command(x=120))
    commands.run(draft, command(y=300))
    after = draft.document()
    # History restores content while materializing legacy cut reservations.
    for expected in (before, after):
        expected["parent"]["config"]["app"]["astrid"]["cut_id_high_water"] = {"number": 2, "suffixes": {}}
    assert draft.undo(2) and draft.document() == before
    assert draft.redo(2) and draft.document() == after
    records = journal.read(journal.journal_path("p", "t"))
    assert records[-2].calls[0]["op"] == "timeline.undo"
    assert records[-1].calls[0]["op"] == "timeline.redo"
    assert getattr(Checkout.save, "__edit_operation__") == "timeline.save"
    assert journal.verify(journal.journal_path("p", "t")) == []


def test_clear_and_null_flags_preserve_element_defaults(draft, capsys):
    draft.clip("c2.card").set(italicWord="Live")
    draft.save(quiet=True)
    before = Path(draft.path).read_bytes()
    parsed = cli.build_parser(None).parse_args(["edit", "t", "--project", "P", "--clip", "c2.card", "--set", "italicWord=null"])
    assert parsed.handler(parsed) == 2
    assert "--clear italicWord" in capsys.readouterr().err
    assert Path(draft.path).read_bytes() == before
    parsed = cli.build_parser(None).parse_args(["edit", "t", "--project", "P", "--clip", "c2.card", "--clear", "italicWord", "--no-sweep"])
    assert parsed.handler(parsed) == 0
    assert "italicWord" not in Checkout.draft("P", "t").clip("c2.card").params


def test_legacy_journal_without_calls_still_logs_and_verifies(draft, capsys):
    path = journal.journal_path("p", "t")
    row = json.loads(path.read_text().splitlines()[0])
    row.pop("calls")
    row.pop("hash")
    row["hash"] = journal._hash(None, row)
    path.write_text(json.dumps(row) + "\n")
    assert journal.read(path)[0].calls == ()
    for args in [["log", "t", "--project", "P"], ["log", "t", "--project", "P", "--verify"]]:
        parsed = cli.build_parser(None).parse_args(args)
        assert parsed.handler(parsed) == 0
    assert journal.verify(path) == []
    assert "chain intact" in capsys.readouterr().out


def test_preview_and_commit_have_the_same_film_length_digest(draft):
    edit = command(op="clip.extend", select="c2.plate", seconds=1)
    preview = commands.run(draft, edit, dry_run=True)
    applied = commands.run(draft, edit)
    assert preview.digests == applied.digests
    assert applied.digests["after"] == journal.document_digest(draft.document())
    assert journal.read(journal.journal_path("p", "t"))[-1].after == applied.digests["after"]


# W46 source preparation only. This detached authority fixture exercises captured
# media_record semantics; it is not a Runtime acquisition or acceptance receipt.
def w46_clone_fixture():
    from astrid.sdk.timeline.commit import _digest
    bundle = json.loads(FIXTURE.read_text())
    source = dict(id="source", track="V1", at=1, clipType="media", asset="old", from_=2)
    source.pop("from_")
    source.update({"from": 2, "to": 6, "speed": 2, "volume": 0.4, "opacity": 0.8,
                   "params": {"opaque": {"op": "clear", "value": None}},
                   "entrance": {"name": "fade"}, "app": {"reference": {"revision": "r1", "null": None}}})
    follower = dict(id="follower", track="V1", at=5, clipType="hold", hold=1)
    bundle["parent"] = {"config": {"tracks": [{"id": "V1", "kind": "visual"}],
                                   "output": {"resolution": "1920x1080", "fps": 30, "file": "out.mp4"}},
                        "clips": [source, follower], "registry": {"assets": {"old": {"type": "video/mp4", "duration": 8}}}}
    from astrid.sdk.timeline.identity import retain_cut_reservations
    retain_cut_reservations(bundle)
    detached = dict(realm_id="unit-realm", project_id=bundle["project_id"], asset="replacement",
                    generation_id="unit-generation", variant_id="unit-variant", object_id="sha256:"+"a"*64,
                    generation={"opaque": None}, variant={"op": "clear"},
                    entry={"object_id": "sha256:"+"a"*64, "media_type": "video/mp4", "duration_seconds": 8})
    record = {**detached, "catalog_digest": _digest(detached)}
    selection = {key: record[key] for key in ("asset", "generation_id", "variant_id", "object_id", "catalog_digest")}
    call = {"op": "timeline.add", "select": None, "args": {"from": "parent/clip:source", "at": 3, "media": selection},
            "created": ["parent/clip:child"], "expect": {"parent/clip:source::": {"state": "present", "value": copy.deepcopy(source)},
            "parent/clip:source::clip_order": {"state": "present", "value": ["parent/clip:source", "parent/clip:follower"]},
            "parent/clip:child::": {"state": "absent"}, "parent/clip:follower::": {"state": "present", "value": copy.deepcopy(follower)},
            "parent::registry.assets.replacement": {"state": "absent"}}}
    return Checkout(bundle), record, call


def w46_capture(tl, record, calls):
    from types import SimpleNamespace
    from astrid.sdk.timeline.commit import RuntimeCommitService
    return RuntimeCommitService._capture_media(SimpleNamespace(selected_media=lambda selection: copy.deepcopy(record)),
                                               {"project_id": tl.bundle["project_id"]}, calls)


def test_w46_captured_clone_preserves_whole_row_registry_ripple_inverse_and_replay(tmp_path):
    tl, record, call = w46_clone_fixture()
    before = copy.deepcopy(tl.document())
    nudge = {"op": "clip.nudge", "select": "parent/clip:follower", "args": {"frames": 60}}
    captured = w46_capture(tl, record, [call, nudge])
    with tl.edit("W46 source-only clone", quiet=True) as tx:
        for value in captured:
            commands.execute(tl, value)
    assert not tx.plan.blocking
    forward = copy.deepcopy(tl.document())
    source = before["parent"]["clips"][0]
    child = next(row for row in forward["parent"]["clips"] if row["id"] == "child")
    mark = child["app"]["astrid"]["media_registry_insert"]
    expected = {**copy.deepcopy(source), "id": "child", "at": 3, "asset": "replacement"}
    expected["app"]["astrid"] = {"media_registry_insert": mark}
    assert child == expected
    assert next(row for row in forward["parent"]["clips"] if row["id"] == "follower")["at"] == 7
    entry = forward["parent"]["registry"]["assets"]["replacement"]
    assert entry["media_id"] == record["object_id"] and entry["format"] == record["entry"]
    # Replaying the captured command batch on the exact base is byte-stable.
    replay, _, _ = w46_clone_fixture()
    with replay.edit("W46 replay", quiet=True):
        for value in captured:
            commands.execute(replay, value)
    assert replay.document() == forward
    writes = tx.plan.direct_writes
    inverse = {"op": "timeline.inverse", "select": None, "args": {"publication": "unit-publication", "writes": [
        {**copy.deepcopy(w), "before": copy.deepcopy(w["after"]), "after": copy.deepcopy(w["before"]),
         **({"order": ["parent/clip:source", "parent/clip:follower", "parent/clip:child"]} if w["path"] == "" else {})}
        for w in writes]}}
    with tl.edit("W46 inverse", quiet=True):
        commands.execute(tl, inverse)
    assert tl.document() == before
    with tl.edit("W46 redo", quiet=True):
        for value in captured:
            commands.execute(tl, value)
    assert tl.document() == forward
    saved = tmp_path / "clone.json"
    tl.save(saved, quiet=True)
    assert Checkout.load(saved).document() == forward


@pytest.mark.parametrize("kind", ["duration", "wrong project", "wrong object", "wrong variant", "catalog", "collision", "stale source", "stale order", "stale registry", "dependent source", "unreserved child", "wrong track"])
def test_w46_clone_refusal_has_no_effect(kind):
    from astrid.sdk.timeline.commit import _digest
    tl, record, call = w46_clone_fixture()
    if kind == "duration": record["entry"]["duration_seconds"] = 5
    if kind == "wrong project": record["project_id"] = "different-project"
    if kind == "wrong object": record["entry"]["object_id"] = "sha256:"+"b"*64
    if kind == "wrong variant": record["variant_id"] = "different-variant"
    if kind == "catalog": record["variant"]["changed"] = True
    if kind == "unreserved child": call.pop("created")
    if kind == "wrong track": call["args"]["track"] = "different-track"
    if kind in {"duration", "wrong object"}:
        record["catalog_digest"] = _digest({k: v for k, v in record.items() if k != "catalog_digest"})
        call["args"]["media"]["catalog_digest"] = record["catalog_digest"]
    rows = tl.bundle["parent"]["clips"]
    if kind == "collision": rows.append({"id": "child", "track": "V1", "at": 9, "hold": 1})
    if kind == "stale source": rows[0]["opacity"] = 0.1
    if kind == "stale order": rows.reverse()
    if kind == "stale registry": tl.bundle["parent"]["registry"]["assets"]["replacement"] = {"media_id": "sha256:"+"c"*64}
    if kind == "dependent source": rows[1].setdefault("app", {})["astrid"] = {"on": 'clip-end "parent/clip:source"'}
    before = copy.deepcopy(tl.document())
    from astrid.sdk.timeline.commit import _Refusal
    with pytest.raises((TimelineEditError, _Refusal)):
        with tl.edit("W46 refused", quiet=True):
            for value in w46_capture(tl, record, [call, {"op": "clip.nudge", "select": "parent/clip:follower", "args": {"frames": 60}}]):
                commands.execute(tl, value)
    assert tl.document() == before


@pytest.mark.parametrize("kind", ["edited child", "dependent child"])
def test_w46_later_child_prevents_whole_inverse(kind):
    tl, record, call = w46_clone_fixture()
    captured = w46_capture(tl, record, [call, {"op": "clip.nudge", "select": "parent/clip:follower", "args": {"frames": 60}}])
    with tl.edit("W46 source preparation", quiet=True) as tx:
        for value in captured:
            commands.execute(tl, value)
    writes = [{**copy.deepcopy(w), "before": copy.deepcopy(w["after"]), "after": copy.deepcopy(w["before"]),
               **({"order": ["parent/clip:source", "parent/clip:follower", "parent/clip:child"]} if w["path"] == "" else {})}
              for w in tx.plan.direct_writes]
    if kind == "edited child":
        next(row for row in tl.bundle["parent"]["clips"] if row["id"] == "child")["opacity"] = 0.2
    else:
        tl.bundle["parent"]["clips"].append(dict(id="dependent", track="V1", at=5, clipType="hold", hold=1,
                                               app={"astrid": {"on": 'clip-end "parent/clip:child"'}}))
    before = copy.deepcopy(tl.document())
    with pytest.raises(TimelineEditError):
        with tl.edit("W46 refused inverse", quiet=True):
            commands.execute(tl, {"op": "timeline.inverse", "select": None,
                                 "args": {"publication": "unit-publication", "writes": writes}})
    assert tl.document() == before
