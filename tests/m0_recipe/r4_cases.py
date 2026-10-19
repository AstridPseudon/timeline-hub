"""Subprocess cases: real R4 recorder, compiler, inverse and rebase.

Only immutable read/acceptance data is synthetic. Product code is never patched.
"""
# R4 must be selected before importing its product modules.
# ruff: noqa: E402
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT))
sys.path.insert(1, str(ROOT / "tests/sdk"))

from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands, inverse
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
from astrid.sdk.timeline.identity import retain_cut_reservations
from astrid.sdk.timeline.rebase import rebase

SID = "occurrence:occ-A/clip:a-rocket"


def tiny():
    raw = json.loads((ROOT / "tests/fixtures/timeline_editing/tiny_publishable.json").read_text())
    return retain_cut_reservations(Checkout(raw).document())


def call(op="clip.set", select=SID, **args):
    return dict(op=op, select=select, args=args)


def apply(bundle, *calls):
    return RuntimeCommitService._apply(copy.deepcopy(bundle), calls)[:2]


def restored(before, after, plan):
    command = inverse.inverse_command(plan.calls, before, after, "pub-original",
                                      consequences=plan.consequences)
    undo, _ = apply(after, command)
    return undo, command


def assert_roundtrip_or_version_upgrade(before, undo):
    original = commands.entity_states(Checkout(before))
    restored_states = commands.entity_states(Checkout(undo))
    # R4 deliberately upgrades the representation during timing compilation.
    # Characterize the exact exception rather than comparing a reduced model.
    paths = set(commands.changed_paths(original, restored_states))
    assert paths == {("parent", "config.app.astrid.v")}, paths
    assert commands.state_at(original, "parent", "config.app.astrid.v") == {"state": "absent"}
    assert commands.state_at(restored_states, "parent", "config.app.astrid.v") == {"state": "present", "value": 2}
    print("round-trip exception: parent config.app.astrid.v absent -> 2")


def clears_and_unchanged_writes():
    base = tiny()
    opaque = call(opaque=None, _allow_new=True)
    after, plan = apply(base, opaque)
    assert plan.calls[0].expect["params.opaque"] == {"state": "absent"}
    assert Checkout(after).clip(SID).params["opaque"] is None
    cleared, clear = apply(after, call("clip.clear", keys=["opaque"]))
    assert "opaque" not in Checkout(cleared).clip(SID).params
    assert clear.direct_writes[0]["after"] == {"state": "absent"}
    undone, _ = restored(after, cleared, clear)
    assert Checkout(undone).clip(SID).params["opaque"] is None
    head, _ = apply(base, opaque)
    assert rebase(plan.calls, head).conflicts[0]["kind"] == "same-property"
    # 10 stored sprite units == 60 canvas px: intentional no-op still guards x.
    _, noop = apply(base, call(x=60))
    assert noop.calls[0].authorship["params.x"] == "direct"
    assert noop.calls[0].expect["params.x"] == {"state": "present", "value": 10}
    assert not noop.direct_writes  # GAP: no-op exists in calls, not write output.
    print("null/absent/clear round-trip; no-op guarded in call but omitted from direct_writes")


def ripple_concurrent_membership():
    base = tiny()
    after, plan = apply(base, call("timeline.insert-time", None, at=2, seconds=1))
    assert Checkout(after).clip("b-plate").start == Checkout(base).clip("b-plate").start + 1
    replay = rebase(plan.calls, base)
    assert not replay.conflicts and replay.document == after
    head = copy.deepcopy(base)
    extra = copy.deepcopy(Checkout(head).clip("b-type").data)
    extra["id"] = "concurrent"
    head["shots"]["B"]["internal_timeline"]["clips"].append(extra)
    result = rebase(plan.calls, head)
    # Characterize whether R4 refuses or silently includes a new ripple member.
    print("ripple concurrent membership:", result.conflicts)
    assert not result.conflicts
    assert Checkout(result.document).clip("concurrent").start == Checkout(head).clip("concurrent").start + 1
    assert "occurrence:occ-B/clip:concurrent" not in plan.calls[0].resolved
    assert "selections" not in plan.calls[0].to_json()  # GAP: no membership guard.
    # Delete is the other structural ripple; its authored inverse restores IDs.
    deleted, deletion = apply(base, call("timeline.ripple-delete", None, start=2, end=3))
    undo, _ = restored(base, deleted, deletion)
    assert_roundtrip_or_version_upgrade(base, undo)


def transition_endpoints():
    from astrid.sdk.timeline.composite_effects import _predecessor
    from astrid.sdk.timeline.transitions import TransitionAuthoringError
    visual = Checkout(tiny())
    destination = copy.deepcopy(visual.clip("a-plate").data)
    destination.update(id="next-picture", at=4, hold=1)
    visual._internal("A")["clips"].append(destination)
    target = visual.clip("next-picture")
    source_id = "occurrence:occ-A/clip:a-plate"
    trial = {"transition": {"duration": .2}}
    assert _predecessor(target, {"from_clip": source_id}, trial).id == "a-plate"
    inserted = copy.deepcopy(destination)
    inserted.update(id="concurrent-picture", at=3.5, hold=.5)
    visual._internal("A")["clips"].append(inserted)
    with pytest.raises(commands.TimelineEditError, match="exact adjacent"):
        _predecessor(target, {"from_clip": source_id}, trial)
    visual._internal("A")["clips"].remove(inserted)
    for at in (3.5, 4.5):
        target.data["at"] = at
        with pytest.raises(commands.TimelineEditError, match="overlap|adjacent"):
            _predecessor(target, {"from_clip": source_id}, trial)
    base = tiny()
    Checkout(base).clip("a-vo").data["track"] = "music"
    Checkout(base).clip("a-music").data["at"] = 2
    # Audio crossfade records both endpoints even when one curve is unchanged.
    after, plan = apply(base, call("timeline.crossfade", None, first="a-vo", second="a-music"))
    record = plan.calls[0]
    paths = {commands.write_target(k, record.resolved) for k in record.expect}
    assert ("occurrence:occ-A/clip:a-vo", "params.fadeOutCurve") in paths
    assert ("occurrence:occ-A/clip:a-music", "params.fadeInCurve") in paths
    head = copy.deepcopy(base)
    Checkout(head).clip("a-music").data["id"] = "replacement-endpoint"
    assert rebase(plan.calls, head).conflicts
    # New visual transitions currently require renderer admission. This is a
    # concrete save-path violation, not permission to carry that boundary forward.
    from astrid.sdk.timeline.transitions import admit_transition_changes
    tl = Checkout(copy.deepcopy(base))
    tl.clip("a-plate").data["transition"] = {"type": "crossfade", "duration": .2}
    tl._open_edit = SimpleNamespace(calls=[])
    with pytest.raises(TransitionAuthoringError, match="renderer|Renderer|admission|transition") as caught:
        admit_transition_changes(tl, Checkout(copy.deepcopy(base)))
    print("visual transition unavailable without renderer:", type(caught.value).__name__, str(caught.value))


def track_dependencies():
    base = tiny()
    sid = "occurrence:occ-A/track:new"
    add = call("timeline.add", sid, track={"id": "new", "kind": "visual", "label": "New"})
    add["expect"] = {sid + "::": {"state": "absent"}}
    after, plan = apply(base, add)
    assert sid in plan.calls[0].created
    undo, command = restored(base, after, plan)
    assert sid not in commands.entity_states(Checkout(undo))
    populated = copy.deepcopy(after)
    Checkout(populated).clip(SID).data["track"] = "new"
    original = copy.deepcopy(populated)
    with pytest.raises(commands.TimelineEditError, match="depend|track|occup|used"):
        apply(populated, command)
    assert populated == original
    with pytest.raises(commands.TimelineEditError, match="move or remove|depend|track"):
        apply(populated, call("timeline.remove", sid))
    deleted, removal = apply(after, call("timeline.remove", sid))
    recreated, _ = restored(after, deleted, removal)
    assert commands.entity_states(Checkout(recreated))[sid] == commands.entity_states(Checkout(after))[sid]
    print("create inverse refuses new dependent; populated delete refuses; empty deletion restores payload")


def stable_ids_and_collision():
    base = tiny()
    after, plan = apply(base, call("timeline.add", None, element="am-sprite", at=1, hold=1, layer="pin"))
    ids = plan.calls[0].created
    assert ids
    first, second = rebase(plan.calls, base), rebase(plan.calls, base)
    assert first.document == second.document == after
    assert first.plan.calls[0].created == second.plan.calls[0].created == ids
    collision = rebase(plan.calls, after)
    assert collision.conflicts[0]["path"] == "created"
    assert collision.document is None
    mapped = ids[0].split("/clip:")[0] + "/clip:explicit-fork"
    # Renaming the identity does not silently change a duplicate authored name.
    duplicate_name = rebase(plan.calls, after, id_map={ids[0]: mapped})
    assert duplicate_name.conflicts[0]["kind"] == "dependent"
    assert "layer named 'pin'" in duplicate_name.conflicts[0]["ours"]
    # An ID-only collision with no layer-name collision can be explicitly mapped.
    collided = copy.deepcopy(base)
    row = copy.deepcopy(Checkout(after).clip(ids[0]).data)
    intent.set_layer(row, "other-layer")
    collided["shots"]["A"]["internal_timeline"]["clips"].append(row)
    replay = rebase(plan.calls, collided, id_map={ids[0]: mapped})
    assert not replay.conflicts and replay.id_map == {ids[0]: mapped}, replay.conflicts
    print("stable deterministic replay IDs; collision refuses; explicit injective map succeeds")


def music_authored_and_derived():
    from astrid.sdk.timeline.compiler import compile_timing
    from astrid.sdk.timeline.music_beds import collection
    base = tiny()
    Checkout(base).clip("a-music").data["to"] = 8
    source = copy.deepcopy(Checkout(base).clip("a-music").data)
    after, plan = apply(base, call("timeline.insert-time", None, at=2, seconds=1))
    owner = "occurrence:occ-A/clip:a-music"
    bed = collection(Checkout(after))[owner]
    assert bed["source"] == source
    assert bed["ripple_basis"] == [{"at_s": 2., "delta_s": 1.}]
    assert len(bed["outputs"]) == 2
    assert compile_timing(after).bundle == after
    undo, _ = restored(base, after, plan)
    assert_roundtrip_or_version_upgrade(base, undo)
    changed, gain = apply(after, call("clip.set-look", owner, volume=.3))
    assert collection(Checkout(changed))[owner]["source"]["volume"] == .3
    gain_undo, _ = restored(after, changed, gain)
    assert collection(Checkout(gain_undo)) == collection(Checkout(after))
    print("authored source/ripple basis survive; outputs deterministic; insertion and gain inverses restore")


def transcript_identity():
    from astrid.sdk.timeline.transcript_binding import bound_source_words
    content = dict(schema_version=1,
        subject=dict(media_object_id="media", media_sha256="1" * 64),
        source=dict(producer_id="test", source_id="take", lineage_id="lineage",
                    revision_id="rev", producer_digest="2" * 64),
        clock=dict(kind="media", unit="seconds", origin_seconds=0),
        words=[dict(id="opaque-alpha", text="again", start_s=.25, end_s=.5),
               dict(id="opaque-beta", text="again", start_s=.625, end_s=1.125)],
        segments=[dict(id="segment", word_ids=["opaque-alpha", "opaque-beta"])])
    raw = json.dumps(content, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    digest = hashlib.sha256(raw).hexdigest()
    reference = dict(schema_version=1,
        document=dict(id="document", version=3, content_digest="sha256:" + digest),
        snapshot=dict(object_id="sha256:" + digest, sha256=digest),
        **{key: copy.deepcopy(content[key]) for key in ("subject", "source", "clock")})
    binding = dict(copy.deepcopy(reference), occurrence_id="occ-A", word_ids=["opaque-beta"])
    original = copy.deepcopy((binding, reference, raw))
    words = bound_source_words(binding, frozen_reference=reference, snapshot_bytes=raw, occurrence_id="occ-A")
    assert words[0]["id"] == "opaque-beta"
    assert (binding, reference, raw) == original
    for key in ("source_id", "revision_id", "lineage_id"):
        wrong = copy.deepcopy(binding)
        wrong["source"][key] = "other"
        with pytest.raises(commands.TimelineEditError, match="frozen dependency"):
            bound_source_words(wrong, frozen_reference=reference, snapshot_bytes=raw, occurrence_id="occ-A")
    wrong = copy.deepcopy(binding)
    wrong["word_ids"] = ["again"]
    with pytest.raises(commands.TimelineEditError):
        bound_source_words(wrong, frozen_reference=reference, snapshot_bytes=raw, occurrence_id="occ-A")
    # Real legacy anchor binding records text discovery once, refuses ordinal shift.
    base = tiny()
    _, plan = apply(base, call("clip.on", moment='"viral" +9f'))
    assert plan.calls[0].bindings['"viral" +9f'] == "word:s1:2"
    shifted = copy.deepcopy(base)
    Checkout(shifted).clip("a-vo").data["at"] += .2
    followed = rebase(plan.calls, shifted)
    assert not followed.conflicts
    assert Checkout(followed.document).clip(SID).start == pytest.approx(Checkout(shifted).time('"viral"') + .3)
    head = copy.deepcopy(base)
    voice = Checkout(head).clip("a-vo")
    local = intent.words(voice.data)
    local.insert(0, [0, .05, "new"])
    intent.set_line(voice.data, "s1", local)
    assert rebase(plan.calls, head).conflicts[0]["kind"] == "dependent"
    print("immutable source/word pins reject substitutes; legacy ordinal shift refuses rebind")


def inverse_aba_and_ancestry():
    base = tiny()
    first, plan = apply(base, call(x=120))
    second, later = apply(first, call(x=180))
    aba, returned = apply(second, call(x=120))
    undo = inverse.inverse_command(plan.calls, base, first, "pub-original")
    # Local value guards alone permit ABA; the provider history guard refuses it.
    local, _ = apply(aba, undo)
    assert Checkout(local).clip(SID).get("x") == 60
    evidence = {"commands": [c.to_json() for c in returned.calls], "direct_writes": list(returned.direct_writes)}
    digest = _digest(evidence)
    row = dict(publication_id="pub-returned", revision_id="rev-returned",
               previous_publication_id="pub-original", previous_revision_id="rev-original",
               evidence_digest=digest, label="someone else")
    port = SimpleNamespace(revisions=lambda options: [row], evidence=lambda _: evidence)
    result = dict(status=None, conflicts=[], choices=[])
    request = dict(project_id="p", timeline_id="t")
    refusal = RuntimeCommitService._inverse_history(port, request, [commands.EditCommand.coerce(undo)],
                dict(publication_id="pub-returned"), aba, result)
    assert refusal and refusal["conflicts"][0]["kind"] == "same-property"
    assert inverse.overlaps((SID, "params"), (SID, "params.x"))
    assert not inverse.overlaps((SID, "params"), (SID, "paramsExtra"))
    # GAP: the legacy overlap helper compares spelling rather than parsed
    # tokens, although both spellings identify the same dictionary property.
    assert not inverse.overlaps((SID, 'params["x"]'), (SID, "params.x"))
    def event(pub, prev, rev, parent):
        return SimpleNamespace(publication_id=pub, previous_publication_id=prev,
                               id=rev, parent=parent, is_current_head=True)
    chain = [event("pub-new", "pub-old", "same-revision", "same-revision"),
             event("pub-old", None, "same-revision", None)]
    assert len(inverse.publication_chain(chain, "pub-old")) == 2
    with pytest.raises(commands.TimelineEditError, match="ancestry"):
        inverse.publication_chain(chain[:1], "pub-old")
    print("local inverse permits ABA; real publication guard refuses; ancestry uses publication identity")


def immutable_media():
    from astrid.sdk.timeline.commit import _Refusal
    base = tiny()
    record = dict(realm_id="realm", project_id="p", asset="selected",
        generation_id="g", variant_id="v", object_id="sha256:" + "a" * 64,
        generation={"type": "image", "metadata": {"opaque": None}},
        variant={"variant_type": "original", "metadata": {}},
        entry={"object_id": "sha256:" + "a" * 64, "media_type": "image/png",
               "filename": "selected.png", "size": 4, "duration_seconds": None})
    selection = {k: record[k] for k in ("asset", "generation_id", "variant_id", "object_id")}
    selection["catalog_digest"] = _digest(record)
    reads = []

    def selected(value):
        reads.append(copy.deepcopy(value))
        return {**copy.deepcopy(record), "catalog_digest": _digest(record)}

    port = SimpleNamespace(selected_media=selected)
    request = dict(project_id="p")
    add = call("timeline.add", "occurrence:occ-A/track:sprite", media=selection,
               at=1, clip_id="reserved", duration=1)
    add["expect"] = {"occurrence:occ-A/clip:reserved::": {"state": "absent"}}
    captured = RuntimeCommitService._capture_media(port, request, [add])
    after, plan = apply(base, *captured)
    assert plan.calls[0].created == ("occurrence:occ-A/clip:reserved",)
    assert Checkout(after).clip("reserved").asset == "selected"
    # The server's captured bytes support deterministic replay without catalog
    # discovery. This does not replace Runtime acceptance-time authority checks.
    record["generation"]["metadata"]["opaque"] = "catalog changed"
    replay = rebase(plan.calls, base)
    assert not replay.conflicts and replay.document == after and len(reads) == 1
    with pytest.raises(_Refusal, match="mismatch|digest"):
        RuntimeCommitService._capture_media(port, request, [add])
    with pytest.raises(_Refusal, match="cannot supply trusted"):
        RuntimeCommitService._capture_media(port, request, captured)
    record["generation"]["metadata"]["opaque"] = None
    record["project_id"] = "foreign"
    with pytest.raises(_Refusal, match="project membership"):
        RuntimeCommitService._capture_media(port, request, [add])
    record["project_id"] = "p"
    swap = call("clip.swap-asset", media=selection)
    captured_swap = RuntimeCommitService._capture_media(port, request, [swap])
    swapped, swap_plan = apply(base, *captured_swap)
    assert Checkout(swapped).clip(SID).asset == "selected"
    assert Checkout(swapped).clip(SID).data["id"] == Checkout(base).clip(SID).data["id"]
    assert intent.on(Checkout(swapped).clip(SID).data) == intent.on(Checkout(base).clip(SID).data)
    undo, _ = restored(base, swapped, swap_plan)
    assert Checkout(undo).clip(SID).asset == Checkout(base).clip(SID).asset
    # A newly referenced registry entry survives undo of the add that made it.
    shared = copy.deepcopy(after)
    Checkout(shared).clip(SID).data["asset"] = "selected"
    undone, _ = restored(base, shared, plan)
    assert Checkout(undone)._registry("A")["selected"]["media_id"] == selection["object_id"]
    assert "reserved" not in {c.id for c in Checkout(undone).clips()}
    print("add/swap immutable capture; foreign/stale/forged selection refused; shared registry survives inverse")


if __name__ == "__main__":
    globals()[sys.argv[2]]()
    print("PASS", sys.argv[2])
