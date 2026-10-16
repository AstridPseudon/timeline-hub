"""W13/W14/W29 synthetic producer proofs through the existing runner."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.element import catalog
from astrid.core.timeline import clip_fields as cf
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.transaction import edit_transaction

FIXTURE = Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json"
SID = "occurrence:occ-A/clip:a-next"
PREV = "occurrence:occ-A/clip:a-transition-from"


@pytest.fixture(scope="module")
def baseline():
    value = Checkout(json.loads(FIXTURE.read_text())).document()
    rows = value["shots"]["A"]["internal_timeline"]["clips"]
    previous = copy.deepcopy(next(r for r in rows if r["id"] == "a-rocket"))
    # Independent clips on a dedicated visual lane avoid plate/cut autofit.
    previous.update(id="a-transition-from", track="transition-test", app={}, at=0, hold=2)
    rows.extend([previous, {**copy.deepcopy(previous), "id": "a-next", "at": 2, "hold": 2}])
    value["shots"]["A"]["internal_timeline"]["tracks"].append(
        {"id": "transition-test", "kind": "visual"}
    )
    value = apply(value, {"op": "timeline.resolve", "select": None, "args": {}})[0]
    # Existing inverse semantics retain the cut identity high-water mark.
    value["parent"]["config"]["app"]["astrid"]["cut_id_high_water"] = {"number": 2, "suffixes": {}}
    return value


@pytest.fixture
def bundle(baseline):
    return copy.deepcopy(baseline)


@pytest.fixture(scope="module")
def ref():
    row = catalog._element_descriptor(catalog._registry().get("transitions", "cross-fade"))
    return {
        "id": row["id"],
        "revision": row["revision"],
        "kind": row["kind"],
        "packId": row["packId"],
    }


def call(op="clip.set-fade", **args):
    return {"op": op, "select": SID, "args": args}


def transition(ref, **changes):
    return call(
        "clip.set-transition",
        from_clip=PREV,
        elementRef=copy.deepcopy(ref),
        transition={
            "type": ref["id"],
            "duration": 0.317123456789,
            "revision": ref["revision"],
            **changes,
        },
    )


def apply(bundle, *calls):
    tl = Checkout(copy.deepcopy(bundle))
    with edit_transaction(tl, "composite test", quiet=True, persist=False) as tx:
        tx.canonical = True
        for value in calls:
            commands.execute(tl, value)
    return tl.document(), tx.plan


def row(bundle):
    return Checkout(bundle).clip("a-next").data


def undo(before, after, plan):
    inverse = inverse_command(
        plan.calls, before, after, "synthetic-publication", consequences=plan.consequences
    )
    return apply(after, inverse)[0]


def test_fade_one_side_preserves_other_effects_and_phase_siblings(bundle):
    original = row(bundle)
    original.update(
        effects={"fade_in": None, "fade_out": 0.8, "opaque": {"x": None}},
        entrance={"type": "slide", "duration": 0.1, "opaque": [None, {}]},
        exit={"type": "fade-out", "duration": 0.8},
    )
    after, plan = apply(bundle, call(fade_in=0.37123456789))
    result = row(after)
    assert result["effects"] == {**original["effects"], "fade_in": 0.37123456789}
    assert result["entrance"] == {**original["entrance"], "type": "fade", "duration": 0.37123456789}
    assert result["exit"] == original["exit"]
    assert len(plan.calls) == 1
    assert undo(bundle, after, plan) == bundle


@pytest.mark.parametrize(
    "initial",
    [
        {},
        {"effects": {}},
        {"effects": None},
        {"effects": {"opaque": None}},
        {"effects": {"fade_in": None}, "entrance": None},
    ],
)
def test_fade_both_sides_and_exact_container_presence_inverse(bundle, initial):
    row(bundle).update(copy.deepcopy(initial))
    after, plan = apply(bundle, call(fade_in=0, fade_out=0.2))
    assert row(after)["entrance"] == {"type": "fade", "duration": 0}
    assert row(after)["exit"] == {"type": "fade-out", "duration": 0.2}
    assert undo(bundle, after, plan) == bundle
    replay, _ = apply(bundle, *[c.to_json() for c in plan.calls])
    assert replay == after


def test_fade_null_and_clear_are_distinct_and_undo_exact(bundle):
    row(bundle).update(
        effects={"fade_in": 0.4, "opaque": None}, entrance={"type": "fade", "duration": 0.4}
    )
    after, plan = apply(bundle, call(fade_in=None))
    assert row(after)["effects"]["fade_in"] is None and row(after)["entrance"] is None
    assert undo(bundle, after, plan) == bundle
    cleared, plan = apply(after, call(clear=["fade_in"]))
    assert row(cleared)["effects"] == {"opaque": None} and "entrance" not in row(cleared)
    assert undo(after, cleared, plan) == after


@pytest.mark.parametrize(
    "args",
    [
        {},
        {"fade_in": -1},
        {"fade_out": True},
        {"fade_in": "8f"},
        {"fade_in": 0.2, "clear": ["fade_in"]},
        {"clear": []},
        {"clear": ["fade_in", "fade_in"]},
        {"unknown": 1},
    ],
)
def test_fade_closed_contract_and_atomic_failure(bundle, args):
    tl = Checkout(copy.deepcopy(bundle))
    before = tl.document()
    view = tl.clip("a-next")
    with pytest.raises(commands.TimelineEditError):
        with edit_transaction(tl, "late refusal", quiet=True, persist=False):
            commands.execute(tl, call(fade_in=0.1))
            commands.execute(tl, call(**args))
    assert tl.document() == before and view.data == row(before)


def test_transition_seconds_reference_and_opaque_payload_replay_inverse(bundle, ref):
    row(bundle).update(
        transition={"id": "fade", "durationFrames": 8, "opaque": [None, {"x": 2}]},
        elementRef=None,
        opaque={"untouched": None},
    )
    request = transition({**ref, "opaque": {"null": None}}, params={"extra": [None, {}]})
    after, plan = apply(bundle, request)
    assert row(after)["elementRef"] == request["args"]["elementRef"]
    assert row(after)["transition"] == {"opaque": [None, {"x": 2}], **request["args"]["transition"]}
    assert "id" not in row(after)["transition"] and "durationFrames" not in row(after)["transition"]
    assert row(after)["opaque"] == {"untouched": None}
    replay, _ = apply(bundle, *json.loads(json.dumps([c.to_json() for c in plan.calls])))
    assert replay == after
    assert undo(bundle, after, plan) == bundle


@pytest.mark.parametrize("params", ["absent", None, {}, {"opaque": None}])
def test_property_only_exact_reference_and_params_presence(bundle, ref, params):
    initial, _ = apply(bundle, transition(ref, params={"old": None}))
    retained = copy.deepcopy(row(initial)["elementRef"])
    authored = {
        "type": ref["id"],
        "duration": 0.1234567890123,
        "revision": ref["revision"],
        "future": None,
    }
    if params != "absent":
        authored["params"] = params
    after, plan = apply(initial, call("clip.set-transition", transition=authored))
    assert row(after)["elementRef"] == retained
    assert row(after)["transition"] == authored
    assert undo(initial, after, plan) == initial


def test_explicit_frames_convert_once_at_pinned_fps_and_seconds_do_not_round(bundle, ref):
    bundle["parent"]["config"]["theme_overrides"]["visual"]["canvas"]["fps"] = 24
    request = transition(ref)
    request["args"]["duration_frames"] = 7
    del request["args"]["transition"]["duration"]
    after, plan = apply(bundle, request)
    assert row(after)["transition"]["duration"] == 7 / 24
    assert plan.calls[0].args == request["args"]
    assert apply(bundle, *[c.to_json() for c in plan.calls])[0] == after
    changed = copy.deepcopy(bundle)
    changed["parent"]["config"]["theme_overrides"]["visual"]["canvas"]["fps"] = 30
    assert rebase(plan.calls, changed).conflicts
    seconds, _ = apply(bundle, transition(ref))
    assert row(seconds)["transition"]["duration"] == 0.317123456789


@pytest.mark.parametrize(
    "change",
    ["stale", "mismatch", "type", "kind", "owner", "params", "frames", "double", "unknown"],
)
def test_transition_invalid_reference_payload_and_revision_roll_back(bundle, ref, change):
    request = transition(ref)
    args = request["args"]
    if change == "stale":
        args["elementRef"]["revision"] = args["transition"]["revision"] = "sha256:stale"
    elif change == "mismatch":
        args["transition"]["revision"] = "other"
    elif change == "type":
        args["transition"]["type"] = "fade"
    elif change == "kind":
        args["elementRef"]["kind"] = "effect"
    elif change == "owner":
        args["elementRef"]["packId"] = "foreign"
    elif change == "params":
        args["transition"]["params"] = []
    elif change == "frames":
        args["duration_frames"] = True
        del args["transition"]["duration"]
    elif change == "double":
        args["duration_frames"] = 8
    else:
        args["unknown"] = None
    tl = Checkout(copy.deepcopy(bundle))
    before = tl.document()
    with pytest.raises(commands.TimelineEditError):
        with edit_transaction(tl, "atomic", quiet=True, persist=False):
            commands.execute(tl, call(fade_out=0.2))
            commands.execute(tl, request)
    assert tl.document() == before


@pytest.mark.parametrize(
    "change", ["track", "gap", "overlap", "between", "scope", "fit", "missing", "implicit"]
)
def test_transition_adjacency_scope_track_fit_refusal(bundle, ref, change):
    request = transition(ref)
    if change == "track":
        row(bundle)["track"] = "sprite"
    elif change == "gap":
        row(bundle)["at"] = 2.1
    elif change == "overlap":
        row(bundle)["at"] = 1.9
    elif change == "between":
        internal = bundle["shots"]["A"]["internal_timeline"]
        internal["clips"].append(
            {**copy.deepcopy(row(bundle)), "id": "middle", "at": 1.9, "hold": 0.1}
        )
    elif change == "scope":
        request["args"]["from_clip"] = "occurrence:occ-B/clip:a-plate"
    elif change == "fit":
        request["args"]["transition"]["duration"] = 2.01
    elif change == "missing":
        del request["args"]["elementRef"]
    else:
        del request["args"]["from_clip"]
    with pytest.raises(commands.TimelineEditError):
        apply(bundle, request)


def test_transition_clear_and_null_exact_inverse(bundle, ref):
    initial, _ = apply(bundle, transition(ref, params=None))
    for request in (
        call("clip.set-transition", clear=True),
        call("clip.set-transition", transition=None),
    ):
        after, plan = apply(initial, request)
        if request["args"].get("clear"):
            assert "transition" not in row(after) and "elementRef" not in row(after)
        else:
            assert row(after)["transition"] is None and row(after)["elementRef"] is None
        assert undo(initial, after, plan) == initial


def test_composite_rebase_preserves_disjoint_side_and_conflicts_same_side(bundle):
    row(bundle)["effects"] = {"opaque": None}
    _, plan = apply(bundle, call(fade_in=0.4))
    head, _ = apply(bundle, call(fade_out=0.2))
    result = rebase(plan.calls, head)
    assert not result.conflicts
    assert row(result.document)["effects"] == {"fade_in": 0.4, "fade_out": 0.2, "opaque": None}
    conflicting, _ = apply(bundle, call(fade_in=0.3))
    assert rebase(plan.calls, conflicting).conflicts


def test_legacy_reads_do_not_fabricate_revision_and_shared_codec_keeps_authored(ref):
    for legacy in (
        "cross-fade",
        {"id": "cross-fade", "durationFrames": 8},
        {"type": "fade", "duration": 0.3},
    ):
        clip = {"transition": copy.deepcopy(legacy)}
        assert cf.read(clip, "transition") == legacy
        cf.describe(clip)
        assert clip == {"transition": legacy}
    authored = {
        "type": "cross-fade",
        "duration": 0.1234567890123,
        "revision": ref["revision"],
        "params": None,
        "opaque": {"x": None},
    }
    assert cf.coerce("transition", authored)[1] == authored
    assert cf.read({"transition": authored}, "transition") == authored


def test_transition_declaration_must_bind_component(bundle, ref, monkeypatch):
    import astrid.sdk.invocation as invocation

    original = invocation._admitted_timeline_element_resources

    def unbound(*args, **kwargs):
        bindings = original(*args, **kwargs)
        for value in bindings.values():
            value["declaration"]["resources"] = []
        return bindings

    monkeypatch.setattr(invocation, "_admitted_timeline_element_resources", unbound)
    with pytest.raises(commands.TimelineEditError, match="not bound"):
        apply(bundle, transition(ref))


def test_transition_params_follow_declaration_schema(bundle, ref, monkeypatch):
    original = catalog._element_descriptor

    def descriptor(element):
        result = original(element)
        result["schema"] = {
            "type": "object",
            "properties": {
                "strength": {"type": "number", "maximum": 1},
                "durationFrames": {"type": "number"},
            },
            "additionalProperties": False,
        }
        return result

    monkeypatch.setattr(catalog, "_element_descriptor", descriptor)
    with pytest.raises(commands.TimelineEditError, match="invalid transition declaration"):
        apply(bundle, transition(ref, params={"strength": 2}))


def test_transition_duration_param_cannot_bypass_declaration_validation(bundle, ref):
    with pytest.raises(commands.TimelineEditError, match="invalid transition declaration"):
        apply(bundle, transition(ref, params={"durationFrames": -1}))


@pytest.mark.parametrize("op", ["fade", "transition"])
def test_shared_source_occurrence_changes_only_selected_payload(bundle, ref, op):
    bundle["placements"][1]["shot_id"] = "A"
    source = copy.deepcopy(bundle["shots"]["A"])
    request = call(fade_in=0.25) if op == "fade" else transition(ref)
    after, plan = apply(bundle, request)
    states = commands.entity_states(Checkout(after))
    assert bundle["shots"]["A"] == source
    original_clip = next(r for r in source["internal_timeline"]["clips"] if r["id"] == "a-next")
    assert states["occurrence:occ-B/clip:a-next"] == original_clip
    assert states[SID] != states["occurrence:occ-B/clip:a-next"]
    assert plan.calls[0].resolved == (SID,)


def test_shared_source_late_refusal_restores_source_graph(bundle, ref):
    bundle["placements"][1]["shot_id"] = "A"
    tl = Checkout(copy.deepcopy(bundle))
    before = tl.document()
    stale = transition(ref)
    stale["args"]["elementRef"]["revision"] = "stale"
    with pytest.raises(commands.TimelineEditError):
        with edit_transaction(tl, "shared rollback", quiet=True, persist=False):
            commands.execute(tl, call(fade_in=0.3))
            commands.execute(tl, stale)
    assert tl.document() == before


def test_invalid_declaration_refuses_before_shared_materialization(bundle, ref, monkeypatch):
    from astrid.sdk.timeline import music_beds

    bundle["placements"][1]["shot_id"] = "A"
    stale = transition(ref)
    stale["args"]["transition"]["revision"] = stale["args"]["elementRef"]["revision"] = "stale"
    monkeypatch.setattr(
        music_beds, "prepare", lambda *a: pytest.fail("materialized before declaration validation")
    )
    with pytest.raises(commands.TimelineEditError, match="stale transition resource revision"):
        apply(bundle, stale)


def test_shared_codec_authored_transition_set_look_remains_lossless_on_replay(bundle, ref):
    authored = {
        "type": ref["id"],
        "revision": ref["revision"],
        "duration": 0.2345678901,
        "params": None,
        "opaque": [None, {}],
    }
    after, plan = apply(bundle, call("clip.set-look", transition=authored))
    assert plan.calls[0].args["transition"] == authored
    assert apply(bundle, *[c.to_json() for c in plan.calls])[0] == after


def test_transition_explicit_predecessor_rebase_mapping_does_not_rewrite_opaque(bundle, ref):
    request = transition(ref, params={"opaque_identity": PREV})
    _, plan = apply(bundle, request)
    renamed = copy.deepcopy(bundle)
    row(renamed)["id"] = "renamed-to"
    Checkout(renamed).clip("a-transition-from").data["id"] = "renamed-from"
    mapped = {SID: "occurrence:occ-A/clip:renamed-to", PREV: "occurrence:occ-A/clip:renamed-from"}
    result = rebase(plan.calls, renamed, id_map=mapped)
    assert not result.conflicts
    assert result.plan.calls[0].args["from_clip"] == mapped[PREV]
    assert Checkout(result.document).clip("renamed-to").data["transition"]["params"] == {
        "opaque_identity": PREV
    }


def test_new_transition_then_late_failure_restores_live_data_and_bindings(bundle, ref):
    tl = Checkout(copy.deepcopy(bundle))
    before = tl.document()
    selected = tl.clip("a-next")
    with pytest.raises(commands.TimelineEditError):
        with edit_transaction(tl, "late failure", quiet=True, persist=False):
            commands.execute(tl, transition(ref))
            commands.execute(tl, call(fade_out=-1))
    assert tl.document() == before and selected.data == row(before)
    assert tl._pending_calls == [] and tl._journal == []


@pytest.mark.parametrize(
    "initial",
    [
        {},
        {"transition": None, "elementRef": None},
        {"transition": {"id": "fade", "durationFrames": 8, "opaque": None}},
        {"transition": {"type": "fade", "duration": 0.333333333, "params": None}},
    ],
)
def test_transition_restores_exact_prior_absence_null_and_legacy_fields(bundle, ref, initial):
    row(bundle).update(copy.deepcopy(initial))
    after, plan = apply(bundle, transition(ref))
    assert undo(bundle, after, plan) == bundle


def test_composite_exact_destination_with_colliding_other_occurrence(bundle, ref):
    other = bundle["shots"]["B"]["internal_timeline"]
    other["clips"].append(copy.deepcopy(row(bundle)))
    other["tracks"].append({"id": "transition-test", "kind": "visual"})
    before = copy.deepcopy(other)
    after, _ = apply(bundle, call(fade_out=0.25), transition(ref))
    assert after["shots"]["B"]["internal_timeline"] == before
    with pytest.raises(commands.TimelineEditError, match="exact clip ScopedId"):
        apply(bundle, {"op": "clip.set-fade", "select": "a-next", "args": {"fade_in": 0.1}})


def test_parent_scope_and_sdk_adapters_use_same_producers(bundle, ref):
    internal = bundle["shots"]["A"]["internal_timeline"]
    bundle["parent"]["clips"] = [
        copy.deepcopy(r) for r in internal["clips"] if r["id"] in {"a-next", "a-transition-from"}
    ]
    bundle["parent"]["tracks"] = [{"id": "transition-test", "kind": "visual"}]
    fade = {"op": "clip.set-fade", "select": "parent/clip:a-next", "args": {"fade_in": 0.3}}
    assigned = transition(ref)
    assigned["select"], assigned["args"]["from_clip"] = (
        "parent/clip:a-next",
        "parent/clip:a-transition-from",
    )
    after, plan = apply(bundle, fade, assigned)
    assert plan.calls[0].select == "parent/clip:a-next"
    assert (
        next(r for r in after["parent"]["clips"] if r["id"] == "a-next")["entrance"]["duration"]
        == 0.3
    )
    tl = Checkout(copy.deepcopy(bundle))
    with edit_transaction(tl, "SDK", quiet=True, persist=False) as tx:
        tx.canonical = True
        selected = commands.recorded_owner(
            tl,
            commands.EditCommand(
                "clip.set-fade", "parent/clip:a-next", {}, resolved=("parent/clip:a-next",)
            ),
            "clip",
        )
        selected.set_fade(fade_in=0.3)
        selected.set_transition(**assigned["args"])
    assert tl.document() == after
    assert [c.op for c in tx.plan.calls] == ["clip.set-fade", "clip.set-transition"]


@pytest.mark.usefixtures("synthetic_scene_answers")
def test_composite_commit_replay_and_late_refusal_keep_existing_acceptance_path(bundle, ref):
    from test_timeline_commit import core, request

    body = request(call(fade_in=0.25), transition(ref, params=None))
    service, port = core(body, bundle)
    before = copy.deepcopy(bundle)
    result = service.commit(body, port)
    assert result["status"] == "accepted", result
    assert len(port.accepts) == 1 and bundle == before
    assert row(result["canonical_document"])["transition"]["params"] is None
    assert service.commit(body, port) == result and len(port.accepts) == 1
    body = request(transition(ref), call(fade_out=-1))
    service, port = core(body, bundle)
    assert service.commit(body, port)["status"] == "refused"
    assert port.accepts == [] and bundle == before
