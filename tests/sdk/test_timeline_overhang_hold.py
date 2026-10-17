"""Exact W44 producer through real SDK compilation and synthetic acceptance."""
# ruff: noqa: F811 -- imported pytest fixtures share parameter names.
import copy
import json

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401
from test_timeline_shot_group_transfer import content, history_draft
from test_timeline_writer_direct_receipts import (  # noqa: F401
    acceptance_port,
    accepted,
    bundle,
    fixture,
)

from astrid.core.timeline.cuts import clip_duration
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.overhang import APPEARANCE, OP, _inventory
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.shot_groups import identity

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


def serialized(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def roundtrip(before, after, plan, result):
    """Also compare the complete authored JSON at each replay/inverse boundary."""
    from astrid.sdk.timeline.inverse import inverse_command
    assert serialized(RuntimeCommitService._apply(before, plan.calls)[0]) == serialized(after)
    undo = inverse_command(plan.calls, before, after, result["accepted_publication_id"], consequences=plan.consequences)
    restored, undo_plan, undone = accepted(after, [undo], result)
    assert serialized(restored) == serialized(before)
    assert serialized(RuntimeCommitService._apply(after, undo_plan.calls)[0]) == serialized(before)
    redo = inverse_command(undo_plan.calls, after, restored, undone["accepted_publication_id"], consequences=undo_plan.consequences)
    redone, _, _ = accepted(restored, [redo], undone)
    assert serialized(redone) == serialized(after)
    return undo


def owned(tl, sid):
    return commands.authored_owner(tl, sid, selected=True)


def source(bundle, scope="parent", fps=30, held=False):
    tl = Checkout(fixture(bundle, scope))
    if scope != "parent":
        tl.bundle["placements"][0]["duration_ms"] = 10000
        tl.bundle["placements"][1]["placement"]["start_ms"] = 10000
    clip = owned(tl, scope + "/clip:movie")
    clip.data.update(at=.2, to=8.0, x=12.0, y=-3.0, width=720.0, height=480.0,
                     cropTop=.1, cropBottom=.2, cropLeft=.3, cropRight=.4)
    clip.data["app"]["opaque"] = {"number": 1.0, "zero": -0.0, "nested": [1, 1.0, None, False, "雪"]}
    if held:
        clip.data["hold"] = 7
    entry = tl._registry(clip.shot_id)["movie"]
    entry["duration"] = 6
    if fps != "absent":
        entry["fps"] = fps
    clips = tl._internal(clip.shot_id)["clips"]
    clips.insert(0, dict(id="before", track="V2", asset="movie", clipType="media", at=0, hold=.1))
    clips.append(dict(id="tail", track="V1", asset="movie", clipType="media", at=7, hold=1))
    return tl.document()


def conversion(before, scope="parent"):
    tl = Checkout(copy.deepcopy(before))
    sid = scope + "/clip:movie"
    states = commands.entity_states(tl)
    clip = owned(tl, sid)
    entry = tl._registry(clip.shot_id)["movie"]
    fps = entry.get("fps")
    safe_fps = fps if isinstance(fps, (int, float)) and not isinstance(fps, bool) and fps > 0 else 30
    duration = entry["duration"]
    playable = max(.05, max(0, duration - clip.data["from"]) / clip.data["speed"])
    registry = "parent" if scope == "parent" else scope + "/registry"
    path = ('registry.assets' if scope == 'parent' else 'assets') + '["movie"]'
    inventory = _inventory(tl, sid)
    value = dict(op=OP, select=sid, args=dict(child=scope + "/clip:allocated", kind="hold", relation_inventory=inventory,
        source_duration=duration, frame_rate=fps, out_s=clip.data["from"] + playable * clip.data["speed"],
        hold_from=max(0, duration - 1 / safe_fps), hold_to=duration,
        hold_duration=max(.05, clip_duration(clip.data)) - playable),
        created=[scope + "/clip:allocated"], expect={
            sid + "::": commands.state_at(states, sid, ""),
            sid + "::clip_order": commands.state_at(states, sid, "clip_order"),
            registry + "::" + path: commands.state_at(states, registry, path)})
    entities = [scope + "/track:" + clip.track]
    if scope != "parent":
        entities += [scope, scope + "/shot", scope + "/source"]
    entities += [r["target"] for r in inventory["authored"]]
    value["expect"].update({entity + "::": commands.state_at(states, entity, "") for entity in entities})
    return value


@pytest.mark.parametrize("scope,fps,held", [
    ("parent", "absent", False), ("parent", None, False), ("parent", 0, False),
    ("parent", -2, False), ("parent", "invalid", False), ("parent", True, False),
    ("parent", 24, False), ("parent", 29.97, True), ("occurrence:occ-A", 60, False),
    ("occurrence:occ-A", "absent", True)])
def test_exact_caller_geometry_receipts_publication_inverse_and_redo(bundle, scope, fps, held):
    before = source(bundle, scope, fps, held)
    value = conversion(before, scope)
    after, plan, result = accepted(before, [value])
    old = owned(Checkout(before), scope + "/clip:movie")
    tl = Checkout(after)
    clip, child = owned(tl, scope + "/clip:movie"), owned(tl, scope + "/clip:allocated")
    assert clip.data == {**old.data, "to": 6, **({"hold": 5} if held else {})}
    assert clip.duration == 4 and child.duration == pytest.approx(1.6)
    assert child.start == clip.end and child.end == old.end
    assert child.data == dict(id="allocated", asset="movie", track="V1", clipType="hold", at=4.2,
        hold=value["args"]["hold_duration"], **{"from": value["args"]["hold_from"], "to": 6},
        speed=1, volume=0, **{key: old.data[key] for key in APPEARANCE})
    assert serialized({key: child.data[key] for key in APPEARANCE}) == serialized({key: old.data[key] for key in APPEARANCE})
    assert [c["id"] for c in tl._internal(clip.shot_id)["clips"]] == ["before", "movie", "allocated", "tail"]
    assert [c["id"] for c in tl._internal(clip.shot_id)["clips"] if c["track"] == "V1"] == ["movie", "allocated", "tail"]
    assert plan.calls[0].created == (scope + "/clip:allocated",)
    assert plan.calls[0].select == scope + "/clip:movie"
    assert plan.calls[0].args["relation_inventory"] == dict(authored=[], groups=[], beds={})
    writes = {(w["id"], w["path"]): w for w in result["change"]["direct_writes"]}
    assert set(writes) == {(clip_id, path) for clip_id, path in
        [(scope + "/clip:movie", "to"), (scope + "/clip:allocated", "")] +
        ([(scope + "/clip:movie", "hold")] if held else [])}
    assert writes[(scope + "/clip:allocated", "")]["before"] == dict(state="absent")
    assert writes[(scope + "/clip:allocated", "")]["after"] == dict(state="present", value=child.data)
    undo = roundtrip(before, after, plan, result)
    changed = copy.deepcopy(after)
    owned(Checkout(changed), scope + "/clip:allocated").data["cropLeft"] = .9
    refuse(changed, undo)
    assert rebase(plan.calls, after).conflicts


def refuse(before, value):
    value = commands.EditCommand.coerce(value).to_json()
    snapshot = copy.deepcopy(before)
    tl = Checkout(copy.deepcopy(before))
    with pytest.raises(commands.TimelineEditError):
        commands.run(tl, value)
    assert serialized(tl.document()) == serialized(snapshot)
    service, port, body = acceptance_port(before, [value])
    result = service.commit(body, port)
    assert result["status"] in {"refused", "conflict"}, result
    assert not port.accepts and serialized(before) == serialized(snapshot)


@pytest.mark.parametrize("damage", ["child-owner", "child-source", "child-existing", "created", "unscoped",
    "source-duration", "duration", "out", "from", "to", "fps", "kind", "no-overhang", "missing-source",
    "missing-order", "missing-asset", "missing-track", "missing-inventory", "zero-source-duration", "negative-duration", "bool-duration", "epsilon"])
def test_invalid_inputs_refuse_atomically(bundle, damage):
    before = source(bundle)
    value = conversion(before)
    changes = {"child-owner": ("child", "occurrence:occ-A/clip:allocated"),
               "child-source": ("child", "parent/clip:movie"), "child-existing": ("child", "parent/clip:tail"),
               "source-duration": ("source_duration", 5), "duration": ("hold_duration", 2), "out": ("out_s", 5.9),
               "from": ("hold_from", 5), "to": ("hold_to", 7), "fps": ("frame_rate", 24), "kind": ("kind", "media"),
               "zero-source-duration": ("source_duration", 0), "negative-duration": ("hold_duration", -1),
               "bool-duration": ("hold_duration", True)}
    if damage in changes:
        key, val = changes[damage]
        value["args"][key] = val
        if key == "child":
            value["created"] = [val]
    elif damage == "created":
        value["created"].append("parent/clip:extra")
    elif damage == "unscoped":
        value["select"] = "movie"
    elif damage == "missing-inventory":
        del value["args"]["relation_inventory"]
    elif damage == "missing-track":
        del value["expect"]["parent/track:V1::"]
    elif damage == "epsilon":
        before["parent"]["clips"][1]["to"] = 6 + .00005 * 1.25
        value = conversion(before)
    elif damage.startswith("missing-"):
        suffix = {"missing-source": "::", "missing-order": "::clip_order", "missing-asset": '::registry.assets["movie"]'}[damage]
        value["expect"] = {k: v for k, v in value["expect"].items() if not k.endswith(suffix)}
    else:
        before["parent"]["clips"][1]["to"] = 5
        value = conversion(before)
    refuse(before, value)


@pytest.mark.parametrize("damage", ["source", "order", "asset-duration", "asset-fps", "track", "owner", "new-relation"])
def test_recorded_guard_refuses_changed_inputs(bundle, damage):
    before = source(bundle, "occurrence:occ-A")
    _, plan, _ = accepted(before, [conversion(before, "occurrence:occ-A")])
    changed = copy.deepcopy(before)
    tl = Checkout(changed)
    clip = owned(tl, "occurrence:occ-A/clip:movie")
    if damage == "source":
        clip.data["x"] = 99
    elif damage == "order":
        tl._internal(clip.shot_id)["clips"].reverse()
    elif damage.startswith("asset-"):
        tl._registry(clip.shot_id)["movie"]["duration" if damage == "asset-duration" else "fps"] = 25
    elif damage == "track":
        tl._tracks(clip.shot_id)[0]["label"] = "changed"
    elif damage == "owner":
        changed["placements"][0]["at_ms"] = 100
    else:
        intent.set_on(owned(tl, "occurrence:occ-A/clip:tail").data, 'clip-end "occurrence:occ-A/clip:movie"')
    refuse(tl.document(), plan.calls[0])
    assert rebase(plan.calls, tl.document()).conflicts


def test_end_relation_requires_choice_and_detach_roundtrips(bundle):
    before = source(bundle)
    clip = owned(Checkout(before), "parent/clip:movie")
    intent.set_for(clip.data, clip.duration)
    value = conversion(before)
    refuse(before, value)
    value["args"]["relation_choices"] = [dict(target=value["select"], edge="end", choice="keep")]
    refuse(before, value)
    value["args"]["relation_choices"][0]["choice"] = "detach"
    after, plan, result = accepted(before, [value])
    assert owned(Checkout(after), "parent/clip:movie").end == 4.2
    roundtrip(before, after, plan, result)
    value["args"]["relation_choices"][0].update(choice="adjust-offset", offset_seconds=.5)
    refuse(before, value)


def test_explicit_group_keep_preserves_opaque_group_and_inverse(bundle):
    before = source(bundle)
    group = dict(shotId="synthetic", trackId="V1", clipIds=["movie"], opaque={"snapshot": [None, False]})
    before["parent"]["config"]["pinnedShotGroups"] = [group]
    value = conversion(before)
    refuse(before, value)
    value["args"]["group_choices"] = [dict(group=identity(dict(shotId="synthetic", trackId="V1")), choice="keep")]
    after, plan, result = accepted(before, [value])
    assert after["parent"]["config"]["pinnedShotGroups"] == [group]
    roundtrip(before, after, plan, result)
    changed = copy.deepcopy(before)
    changed["parent"]["config"]["pinnedShotGroups"][0]["opaque"] = None
    refuse(changed, plan.calls[0])


def test_subframe_media_clamp_and_missing_null_appearance(bundle):
    before = source(bundle)
    clip = owned(Checkout(before), "parent/clip:movie")
    clip.data.update({"from": 0, "to": 1, "speed": 1, "opacity": None})
    del clip.data["cropLeft"]
    before["parent"]["registry"]["assets"]["movie"]["duration"] = .01
    after, plan, result = accepted(before, [conversion(before)])
    tl = Checkout(after)
    assert owned(tl, "parent/clip:movie").data["to"] == .05  # caller's minimum playable duration
    child = owned(tl, "parent/clip:allocated")
    assert child.data["from"] == 0 and child.data["to"] == .01
    assert child.data["opacity"] is None and "cropLeft" not in child.data
    roundtrip(before, after, plan, result)


def test_fractional_source_geometry_uses_caller_seconds_without_frame_quantization(bundle):
    before = source(bundle, fps=29.97)
    owned(Checkout(before), "parent/clip:movie").data.update(at=.123456789, speed=1.3)
    before["parent"]["registry"]["assets"]["movie"]["duration"] = 6.123456789
    value = conversion(before)
    after, plan, result = accepted(before, [value])
    source_row, child_row = after["parent"]["clips"][1:3]
    assert child_row["at"] == source_row["at"] + (value["args"]["out_s"] - source_row["from"]) / 1.3
    assert child_row["from"] == 6.123456789 - 1 / 29.97
    assert clip_duration(source_row) + clip_duration(child_row) == pytest.approx(7 / 1.3)
    roundtrip(before, after, plan, result)


def test_publication_history_save_reload_retry_and_exact_content_undo_redo(bundle, tmp_path, monkeypatch):
    from astrid.sdk.workspace_client import WorkspaceClientError
    before = source(bundle)
    draft, runtime, client = history_draft(before, tmp_path, monkeypatch)
    captured = draft.document()
    original = content(captured)
    commands.run(draft, conversion(captured))
    runtime.lose = True
    with pytest.raises(WorkspaceClientError, match="timed out"):
        draft.publish("convert overhang", client=client)
    draft = Checkout.load(draft.path)
    converted = draft.publish(client=client)
    assert converted["status"] == "accepted", converted
    assert runtime.commits[0][0] == runtime.commits[1][0]
    assert len(runtime.publications) == 1
    assert converted["change"]["commands"][0]["created"] == ["parent/clip:allocated"]
    converted_content = content(converted["canonical_document"])
    replayed, _, _ = RuntimeCommitService._apply(captured, converted["change"]["commands"])
    assert content(replayed) == converted_content
    draft = Checkout.load(draft.path)
    draft.undo(client=client, publication=converted["accepted_publication_id"])
    undone = draft.publish("undo overhang", client=client)
    assert undone["status"] == "accepted", undone
    assert serialized(content(undone["canonical_document"])) == serialized(original)
    draft = Checkout.load(draft.path)
    draft.undo(client=client, publication=undone["accepted_publication_id"])
    redone = draft.publish("redo overhang", client=client)
    assert redone["status"] == "accepted", redone
    assert content(redone["canonical_document"]) == converted_content
    (tmp_path / "accepted-overhang-proof.json").write_text(json.dumps(dict(
        scope="real SDK with synthetic Runtime acceptance only", before=captured,
        converted=converted, undone=undone, redone=redone), indent=2, sort_keys=True) + "\n")
    # Python numeric equality alone hides integral float -> integer rewrites in
    # the shared inverse recorder. W44 requires the exact authored JSON too.
    assert json.dumps(content(redone["canonical_document"]), sort_keys=True) == json.dumps(converted_content, sort_keys=True)


def test_shared_inverse_records_literal_payload_without_changing_numeric_arguments_or_digests(bundle):
    import hashlib

    from astrid.core.foundation.hash import canonical_json_digest
    from astrid.core.receipts.canonical import canonical_json, request_hash
    from astrid.sdk.timeline.commit import _digest

    tl = Checkout(source(bundle))
    sid = "parent/clip:movie"
    prior = copy.deepcopy(owned(tl, sid).data)
    payload = {**prior, "width": 721.0, "cropTop": -0.0,
               "app": {"opaque": [1.0, -0.0, 1, None, False, {"雪": 2.0}]}}
    writes = [dict(id=sid, path="", before=dict(state="present", value=prior),
                   after=dict(state="present", value=payload))]
    command = dict(op="timeline.inverse", select=None, args=dict(writes=writes, publication="synthetic"))
    plan = commands.run(tl, command)
    assert serialized(plan.calls[0].args["writes"]) == serialized(writes)
    assert serialized(owned(tl, sid).data) == serialized(payload)
    replay = Checkout(source(bundle))
    commands.run(replay, json.loads(serialized(plan.calls[0].to_json())))
    assert serialized(replay.document()) == serialized(tl.document())
    ordinary = commands.run(tl, dict(op="clip.trim", select=sid, args=dict(out_s=5.0)))
    assert type(ordinary.calls[0].args["out_s"]) is int
    look = commands.run(tl, dict(op="clip.set-look", select=sid, args=dict(volume=0.0, opacity=1.0)))
    # The clip-field codec's existing normalized float spelling also survives.
    assert type(look.calls[0].args["volume"]) is float
    assert type(look.calls[0].args["opacity"]) is float
    # Existing protocol hashes distinguish JSON numeric spellings. The inverse
    # exception must not become a global normalization or identity-policy change.
    for value in [command, ordinary.calls[0].to_json(), {"number": 1}, {"number": 1.0}]:
        expected = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                             ensure_ascii=False, allow_nan=False).encode()).hexdigest()
        assert canonical_json_digest(value) == expected
        assert _digest(value) == "sha256:" + expected
        assert canonical_json(value) == json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert request_hash("timeline.edit", {"number": 1.0, "created_at": "first"}) == request_hash(
        "timeline.edit", {"created_at": "retry", "number": 1.0})
    assert request_hash("timeline.edit", {"number": 1.0}) != request_hash("timeline.edit", {"number": 1})
    assert canonical_json_digest({"number": 1}) != canonical_json_digest({"number": 1.0})


def test_transitive_anchor_choice(bundle):
    before = source(bundle)
    tl = Checkout(before)
    intent.set_on(owned(tl, "parent/clip:tail").data, 'clip-end "parent/clip:movie"')
    owned(tl, "parent/clip:tail").data["at"] = owned(tl, "parent/clip:movie").end
    value = conversion(before)
    refuse(before, value)
    value["args"]["relation_choices"] = [dict(target="parent/clip:tail", edge="start", choice="detach")]
    after, plan, result = accepted(before, [value])
    assert owned(Checkout(after), "parent/clip:tail").start == 5.8
    roundtrip(before, after, plan, result)


def test_invalid_composite_rolls_back_preceding_batch_write(bundle):
    before = source(bundle)
    value = conversion(before)
    value["args"]["hold_duration"] = -1
    refuse(before, dict(op="timeline.batch", select=None, args=dict(commands=[
        dict(op="clip.set-look", select="parent/clip:tail", args=dict(opacity=.3)), value])))


def test_explicit_sequence_detach_preserves_full_inverse(bundle):
    before = source(bundle)
    tl = Checkout(before)
    intent.set_sequence(owned(tl, "parent/clip:movie").data, "captured", 0)
    intent.set_sequence(owned(tl, "parent/clip:tail").data, "captured", 1)
    value = conversion(before)
    refuse(before, value)
    value["args"]["relation_choices"] = [dict(target="parent/clip:" + c, edge="sequence", choice="detach")
                                              for c in ("movie", "tail")]
    after, plan, result = accepted(before, [value])
    assert intent.sequence(owned(Checkout(after), "parent/clip:movie").data) is None
    assert plan.calls[0].authorship["parent/clip:tail::at"] == "direct"
    assert type(plan.calls[0].expect["parent/clip:tail::at"]["value"]) is int
    roundtrip(before, after, plan, result)


def test_dependent_bed_inventory_requires_choice_and_preserves_owner_inverse(bundle):
    from astrid.sdk.timeline import music_beds

    tl = Checkout(source(bundle))
    bed_owner = "parent/clip:tail"
    tail = owned(tl, bed_owner)
    tail.data.update(track="A1", asset="song", **{"from": 0.0, "to": 1.0})
    tl._registry(None)["song"] = dict(type="audio/mp3", media_id="sha256:" + "b" * 64)
    intent.set_on(tail.data, 'clip-end "parent/clip:movie"')
    tail.data["at"] = owned(tl, "parent/clip:movie").end
    music_beds.collection(tl, create=True)[bed_owner] = dict(owner=bed_owner,
        source=copy.deepcopy(tail.data), ripple_basis=[], outputs=["tail"])
    before = tl.document()
    value = conversion(before)
    assert set(value["args"]["relation_inventory"]["beds"]) == {bed_owner}
    refuse(before, value)
    value["args"]["relation_choices"] = [dict(target=bed_owner, edge="start", choice="detach")]
    after, plan, result = accepted(before, [value])
    assert set(music_beds.sources(Checkout(after))) == {bed_owner}
    assert intent.on(owned(Checkout(after), bed_owner).data) is None
    roundtrip(before, after, plan, result)
    changed = copy.deepcopy(before)
    music_beds.collection(Checkout(changed))[bed_owner]["ripple_basis"] = [dict(at_s=8.0, delta_s=1.0)]
    refuse(changed, plan.calls[0])
