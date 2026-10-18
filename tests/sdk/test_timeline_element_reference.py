"""W12 real runner/commit receipts over synthetic immutable composition closures."""
import copy
import hashlib
import json
from pathlib import Path

import pytest
from test_timeline_fade_history_receipts import accept, literal, reverse_receipt, port_for
from test_timeline_commit import CoreService, request
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.transaction import edit_transaction

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")
REF = dict(id="local-glow", kind="effect", revision="source-r1")
ROW = dict(kind="effect", revision="source-r1", source="export default () => null;", opaque={"nested": [None, 6.0, {"x": "keep"}]})
SID = "parent/clip:owned"


def apply(document, *calls):
    tl = Checkout(copy.deepcopy(document))
    with edit_transaction(tl, "element reference", quiet=True, persist=False) as tx:
        tx.canonical = True
        for call in calls:
            commands.execute(tl, call)
    return tl.document(), tx.plan


def base_document(source=True):
    fixture = Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json"
    document = json.loads(fixture.read_text())
    document["parent"]["config"]["tracks"] = copy.deepcopy(document["shots"]["A"]["internal_timeline"]["tracks"])
    document["parent"]["clips"] = [dict(id="owned", track="type", clipType="hold", at=1, hold=1, params={"opaque": [None, 6.0]})]
    document, _ = apply(document, dict(op="timeline.resolve", select=None, args={}))
    document["parent"]["config"]["app"]["astrid"]["cut_id_high_water"] = {"number": 2, "suffixes": {}}
    if source:
        document["parent"]["config"]["app"]["elements"] = {REF["id"]: copy.deepcopy(ROW), "sibling": {"opaque": [1, None]}}
    return document


def command(document, overlay=False, clear=False, params=None, row=None):
    from astrid.sdk.timeline.element_reference import source_path
    tl = Checkout(copy.deepcopy(document))
    states = commands._recording_states(tl)
    target = "parent/clip:reserved" if overlay else SID
    ref = copy.deepcopy(REF)
    config = document["parent"]["config"]
    source = config.get("app", {}).get("elements", {}).get(ref["id"], row)
    binding = dict(reference=ref, row=dict(state="present", value=copy.deepcopy(source)))
    encoded = json.dumps(binding["row"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    binding.update(owner="parent", key=ref["id"], row_json=encoded,
                   content_digest="sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest())
    path = source_path(config, ref)
    after_parent = copy.deepcopy(document["parent"])
    after_parent["config"].setdefault("app", {}).setdefault("elements", {})[ref["id"]] = copy.deepcopy(source)
    after_states = {"parent": after_parent}
    old = states.get(target, {})
    fields = {k: commands.state_at(states, target, k) for k in ("elementRef", "params", "entrance")}
    fields["elementRef"] = dict(state="absent") if clear else dict(state="present", value=ref)
    if clear and old.get("entrance", {}).get("type") == ref["id"]:
        fields["entrance"] = dict(state="absent")
    if params is not None:
        fields["params"] = copy.deepcopy(params)
    args = dict(intent="overlay" if overlay else "clear" if clear else "assign", fields=fields,
                params_mode="keep" if params is None else "replace", binding=binding, source_path=path,
                source=commands.state_at(after_states, "parent", path))
    expect = {"parent::" + path: commands.state_at(states, "parent", path)}
    call = dict(op="timeline.add" if overlay else "clip.set-element", select=None if overlay else target, resolved=[target], args=args, expect=expect)
    if overlay:
        order = [r["id"] for r in document["parent"]["clips"]]
        args.update(clip_id="reserved", track="type", at=1.25, duration=.75, time_domain="timeline-seconds",
                    clip_type=ref["id"], expected_order=order, insertion_index=0)
        call["created"] = [target]
        expect.update({target + "::": dict(state="absent"), target + "::clip_order": dict(state="present", value=["parent/clip:" + id for id in order]),
                       "parent/track:type::kind": commands.state_at(states, "parent/track:type", "kind")})
    else:
        expect.update({k: commands.state_at(states, target, k) for k in fields})
    return call


def body(call, index=1):
    value = request(call)
    value.update(request_id=f"request-{index}", session_sequence=index, base_revision_id=f"parent-r{index}", base_publication_id=f"pub-parent-r{index}")
    return value


@pytest.mark.parametrize("overlay", [False, True])
def test_reference_source_receipt_accepted_save_reload_undo_redo(overlay):
    before = base_document()
    call = command(before, overlay=overlay, params=dict(state="present", value={"opaque": [None, 6.0], "gain": .7}))
    result = accept(before, body(call))
    after = result["canonical_document"]
    row = next(r for r in after["parent"]["clips"] if r["id"] == ("reserved" if overlay else "owned"))
    assert row["elementRef"] == REF
    assert after["parent"]["config"]["app"]["elements"] == before["parent"]["config"]["app"]["elements"]
    writes = result["change"]["direct_writes"]
    assert {(w["id"], w["path"]) for w in writes} == ({("parent/clip:reserved", "")} if overlay else {(SID, "elementRef"), (SID, "params")})
    undo_call = reverse_receipt(result)
    if overlay:
        undo_call["args"]["writes"][0]["order"] = ["parent/clip:reserved", SID]
    undone = accept(after, body(undo_call, 2))
    assert literal(undone["canonical_document"]) == literal(before)
    redo = reverse_receipt(undone)
    if overlay:
        redo["args"]["writes"][0]["order"] = ["parent/clip:reserved", SID]
    redone = accept(undone["canonical_document"], body(redo, 3))
    assert literal(redone["canonical_document"]) == literal(after)


@pytest.mark.parametrize("presence", ["absent", "null", "value"])
def test_reference_tagged_params_preserve_null_and_clear(presence):
    before = base_document()
    target = before["parent"]["clips"][0]
    target.pop("params", None)
    if presence != "absent":
        target["params"] = None if presence == "null" else {"a": [1, None]}
    after, plan = apply(before, command(before, params=dict(state="absent")))
    assert "params" not in after["parent"]["clips"][0]
    changed = next((w for w in plan.direct_writes if w["path"] == "params"), None)
    assert (changed is None) == (presence == "absent")
    if changed:
        assert changed["before"] == dict(state="present", value=target["params"])


@pytest.mark.parametrize("container", ["elements-absent", "row-absent"])
def test_reference_new_source_exact_container_roundtrip_and_later_user_refusal(container):
    before = base_document(source=False)
    if container == "row-absent":
        before["parent"]["config"]["app"]["elements"] = {"sibling": {"opaque": [1, None]}}
    call = command(before, row=ROW)
    result = accept(before, body(call))
    assert any(w["id"] == "parent" and w["path"] == call["args"]["source_path"] for w in result["change"]["direct_writes"])
    undone = accept(result["canonical_document"], body(reverse_receipt(result), 2))
    assert literal(undone["canonical_document"]) == literal(before)
    later = copy.deepcopy(result["canonical_document"])
    later["parent"]["clips"].append(dict(id="dependent", track="type", clipType="hold", at=2, hold=1, elementRef=REF))
    snapshot = literal(later)
    with pytest.raises(Exception, match="dependent reference user"):
        apply(later, reverse_receipt(result))
    assert literal(later) == snapshot


def test_reference_detach_leaves_source_clip_and_unrelated_entrance():
    before = base_document()
    before["parent"]["clips"][0].update(elementRef=REF, entrance=dict(type=REF["id"], duration=.4), unrelated=[None, 6.0])
    after, plan = apply(before, command(before, clear=True))
    row = after["parent"]["clips"][0]
    assert "elementRef" not in row and "entrance" not in row and row["unrelated"] == [None, 6.0]
    assert after["parent"]["config"]["app"]["elements"] == before["parent"]["config"]["app"]["elements"]
    before["parent"]["clips"][0]["entrance"] = dict(type="fade", duration=.5)
    after, _ = apply(before, command(before, clear=True))
    assert after["parent"]["clips"][0]["entrance"] == dict(type="fade", duration=.5)


@pytest.mark.parametrize("bad", ["stale-source", "stale-reference", "stale-order", "pack", "revision", "collision", "later-edit", "missing-expect", "ambiguous-user", "digest", "source-key", "row-json", "entrance"])
def test_reference_refusals_are_atomic(bad):
    before = base_document()
    call = command(before, overlay=bad in {"stale-order", "collision"})
    if bad == "stale-source":
        before["parent"]["config"]["app"]["elements"][REF["id"]]["opaque"] = "changed"
    elif bad == "stale-reference":
        before["parent"]["clips"][0]["elementRef"] = None
    elif bad in {"pack", "revision"}:
        call["args"]["binding"]["reference"]["packId" if bad == "pack" else "revision"] = "wrong"
    elif bad == "stale-order":
        before["parent"]["clips"].append(dict(id="late", clipType="hold", hold=1, at=2, track="type"))
    elif bad == "collision":
        before["parent"]["clips"].append(dict(id="reserved", clipType="hold", hold=1, at=2, track="type"))
    elif bad == "missing-expect":
        call["expect"].pop("elementRef")
    elif bad == "digest":
        call["args"]["binding"]["content_digest"] = "sha256:" + "0" * 64
    elif bad == "source-key":
        call["args"]["binding"]["key"] = "other"
    elif bad == "row-json":
        call["args"]["binding"]["row_json"] = '{"state":"absent","state":"present"}'
    elif bad == "entrance":
        call["args"]["fields"]["entrance"] = dict(state="present", value=dict(type="unrelated", duration=.5))
    elif bad == "ambiguous-user":
        before["parent"]["clips"][0]["elementRef"] = {**REF, "revision": "other"}
    else:
        forward = accept(before, body(call)); before = forward["canonical_document"]
        call = reverse_receipt(forward)
        before["parent"]["clips"][0]["elementRef"] = {**REF, "revision": "later"}
    snapshot = literal(before)
    with pytest.raises(Exception):
        apply(before, call)
    assert literal(before) == snapshot


def bridge(payload):
    """Only for the focused App test: real SDK, in-memory acceptance double."""
    from test_timeline_saved_publish import synthetic_scene_answers
    patch = pytest.MonkeyPatch()
    synthetic_scene_answers.__wrapped__(patch)
    try:
        if payload.get("base"):
            return base_document()
        return accept(payload["before"], payload["request"])
    finally:
        patch.undo()


if __name__ == "__main__":
    import sys
    print(json.dumps(bridge(json.load(sys.stdin)), ensure_ascii=False))


def test_animation_assignment_from_present_null_reference_has_exact_coupled_receipt(monkeypatch):
    monkeypatch.setitem(REF, "kind", "animation")
    monkeypatch.setitem(ROW, "kind", "animation")
    before = base_document()
    before["parent"]["clips"][0]["elementRef"] = None
    call = command(before, params=dict(state="present", value={"gain": .5, "opaque": [None, 6.0]}))
    call["args"]["fields"]["entrance"] = dict(state="present", value=dict(type=REF["id"], duration=.4, params={"gain": .5}))
    forward = accept(before, body(call))
    writes = forward["change"]["direct_writes"]
    assert {w["path"] for w in writes} == {"elementRef", "params", "entrance"}
    assert next(w for w in writes if w["path"] == "elementRef")["before"] == dict(state="present", value=None)
    assert forward["canonical_document"]["parent"]["clips"][0]["entrance"] == call["args"]["fields"]["entrance"]["value"]
    undone = accept(forward["canonical_document"], body(reverse_receipt(forward), 2))
    assert literal(undone["canonical_document"]) == literal(before)
    redone = accept(undone["canonical_document"], body(reverse_receipt(undone), 3))
    assert literal(redone["canonical_document"]) == literal(forward["canonical_document"])
