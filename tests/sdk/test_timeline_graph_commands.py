"""Synthetic occurrence graph producer fixtures; no App or installed Runtime proof."""
import copy

import pytest
from test_timeline_commit import Port, request
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


@pytest.fixture
def closure():
    internal = dict(tracks=[dict(id="picture", kind="visual")], clips=[], registry={}, assets=[], effects=[], audio=[], layout={})
    shot = dict(items=[dict(item_id="item-1", metadata=dict(source_item_id="item-1", opaque_literal="item-1"))], metadata=dict(settings=None, opaque=7), provenance=dict(name="old", opaque=None), internal_timeline_revision_id="int-1")
    occurrence = dict(occurrence_id="a", shot_id="s", shot_revision_id="shot-1", placement=dict(start_ms=0, opaque=None), duration_ms=1000, track="picture", source_offset=0, opaque="keep")
    sibling = dict(copy.deepcopy(occurrence), occurrence_id="b", placement=dict(start_ms=1000))
    parent = dict(config={}, registry={}, clips=[], occurrences=[occurrence, sibling])
    return dict(parent_revision=dict(project_id="p", timeline_id="t", revision_id="rev-0", payload=parent, content_digest=_digest(parent)), shot_revisions=[dict(project_id="p", shot_id="s", revision_id="shot-1", internal_timeline_revision_id="int-1", internal_timeline_id="inner", payload=shot, content_digest=_digest(shot))], internal_timeline_revisions=[dict(project_id="p", timeline_id="inner", revision_id="int-1", payload=internal, content_digest=_digest(internal))])


def opened(closure):
    bundle = open_authoring_bundle(closure["parent_revision"], shot_revisions=closure["shot_revisions"], internal_timeline_revisions=closure["internal_timeline_revisions"])
    for row in bundle["source_mapping"]["shots"].values():
        row["linked"] = True
    return bundle


def source(oid="a", parent="rev-0"):
    return dict(parent_revision_id=parent, occurrence_id=oid, shot_id="s", shot_revision_id="shot-1", internal_revision_id="int-1")


def shot_call(**kwargs):
    return dict(op="shot.set", select="occurrence:a/shot", args=dict(source=source(), **kwargs))


def add_call(mode="independent", **kwargs):
    identities = dict(occurrence_id="new")
    if mode == "independent":
        identities.update(shot_id="new-shot", shot_revision_id="new-shot-rev", internal_revision_id="new-int-rev")
    args = dict(source=source(), mode=mode, placement=dict(start_ms=2000, duration_ms=1000, track="picture"), identities=identities)
    args.update(kwargs)
    return dict(op="occurrence.add", select="occurrence:new", args=args)


def apply(bundle, *calls):
    return RuntimeCommitService._apply(bundle, calls)[:2]


def port_for(closure, *calls):
    body = request(*calls)
    port = Port(body)
    port.revision_closure = lambda rid: copy.deepcopy(closure)
    return body, port


def test_shot_selected_only_null_clear_and_opaque(closure):
    before = opened(closure)
    after, plan = apply(before, shot_call(values=dict(name="new", settings=None)))
    states = commands.entity_states(Checkout(after))
    original = commands.entity_states(Checkout(before))
    assert states["occurrence:b/shot"] == original["occurrence:b/shot"]
    assert states["occurrence:a/shot"]["provenance"] == dict(name="new", opaque=None)
    assert states["occurrence:a/shot"]["metadata"] == dict(settings=None, opaque=7)
    assert plan.calls[0].resolved == ("occurrence:a/shot",)
    assert plan.calls[0].expect["provenance.name"] == dict(state="present", value="old")
    cleared, _ = apply(after, shot_call(clear=["settings"]))
    assert "settings" not in commands.entity_states(Checkout(cleared))["occurrence:a/shot"]["metadata"]
    assert before == opened(closure)


@pytest.mark.parametrize("mode", ["linked", "independent"])
def test_add_compiles_exact_pins_and_reservations(closure, mode):
    before = opened(closure)
    after, plan = apply(before, add_call(mode))
    compiled = compile_authoring_candidate(after)
    mapping = compiled.identity_mapping["placements"]["new"]
    assert mapping["shot_id"] == ("s" if mode == "linked" else "new-shot")
    assert mapping["shot_revision_id"] == ("shot-1" if mode == "linked" else "new-shot-rev")
    assert "occurrence:new" in plan.calls[0].created
    assert rebase(plan.calls, before).conflicts == ()
    assert rebase(plan.calls, before).document == after
    with pytest.raises(commands.CommandError):
        apply(after, add_call(mode))


def test_commit_accept_and_response_loss_replay(closure):
    body, port = port_for(closure, add_call())
    service = RuntimeCommitService()
    result = service.commit(body, port)
    assert result["status"] == "accepted", result
    assert result["id_map"]["occurrence:new/shot"] == "new-shot"
    assert result["id_map"]["occurrence:new::internal_revision_id"] == "new-int-rev"
    assert service.commit(body, port) == result
    assert len(port.accepts) == 1


def test_inverse_shot_edit_and_move(closure):
    before = opened(closure)
    move = dict(op="occurrence.set", select="occurrence:a", args=dict(source=source(), placement=dict(start_ms=3000)))
    after, plan = apply(before, shot_call(values=dict(name="new")), move)
    inverse = inverse_command(plan.calls, before, after, "pub-1")
    restored, _ = apply(after, inverse)
    assert commands.entity_states(Checkout(restored)) == commands.entity_states(Checkout(before))


def test_moved_head_disjoint_and_same_property_conflict(closure):
    before = opened(closure)
    _, plan = apply(before, shot_call(values=dict(name="new")))
    head, _ = apply(before, dict(op="occurrence.set", select="occurrence:b", args=dict(source=source("b"), placement=dict(start_ms=4000))))
    assert not rebase(plan.calls, head).conflicts
    same, _ = apply(before, shot_call(values=dict(name="theirs")))
    assert rebase(plan.calls, same).conflicts


def test_late_failure_atomic_and_stale_pin_refusal(closure):
    before = opened(closure)
    bad = shot_call(values=dict(name="new"))
    bad["args"]["source"]["internal_revision_id"] = "stale"
    with pytest.raises(commands.CommandError):
        apply(before, bad)
    body, port = port_for(closure, shot_call(values=dict(name="new")), shot_call(values=dict(arbitrary=True)))
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "refused", result
    assert port.accepts == []
    assert opened(closure) == before


@pytest.mark.parametrize("mode", ["linked", "independent"])
def test_inverse_add_is_one_root_and_one_undo(closure, mode):
    before = opened(closure)
    after, plan = apply(before, add_call(mode))
    inverse = inverse_command(plan.calls, before, after, "pub-add")
    assert len(inverse["args"]["writes"]) == 1
    restored, _ = apply(after, inverse)
    assert commands.entity_states(Checkout(restored)) == commands.entity_states(Checkout(before))


def test_replace_external_exact_source_and_inverse_after_reload(closure):
    before = opened(closure)
    external = copy.deepcopy(closure)
    external["parent_revision"]["revision_id"] = "external-parent"
    external["shot_revisions"][0]["revision_id"] = "shot-2"
    for row in external["parent_revision"]["payload"]["occurrences"]:
        row["shot_revision_id"] = "shot-2"
    external["parent_revision"]["content_digest"] = _digest(external["parent_revision"]["payload"])
    external["shot_revisions"][0]["payload"]["provenance"]["name"] = "replacement"
    external["shot_revisions"][0]["content_digest"] = _digest(external["shot_revisions"][0]["payload"])
    before["source_mapping"]["imports"] = {"external-parent": opened(external)}
    replacement = dict(source(parent="external-parent"), shot_revision_id="shot-2")
    edit = dict(op="occurrence.set", select="occurrence:a", args=dict(source=source(), replacement=replacement))
    after, plan = apply(before, edit)
    states = commands.entity_states(Checkout(after))
    assert states["occurrence:a/shot"]["provenance"]["name"] == "replacement"
    assert states["occurrence:b/shot"] == commands.entity_states(Checkout(before))["occurrence:b/shot"]
    inverse = inverse_command(plan.calls, before, after, "pub-replace")
    assert inverse["args"]["writes"][0]["source"] == source()
    # Compile and reopen the actual immutable closure. The replaced old source
    # is absent from that closure and must be read through inverse's exact pin.
    publication = compile_authoring_candidate(after).publication
    shot_rows = {r["revision_id"]: dict(r, project_id="p") for r in closure["shot_revisions"] + external["shot_revisions"] + publication["shot_revisions"]}
    internal_rows = {r["revision_id"]: dict(r, project_id="p") for r in closure["internal_timeline_revisions"] + publication["internal_timeline_revisions"]}
    payload = publication["parent_composition"]
    exact = dict(parent_revision=dict(project_id="p", timeline_id="t", revision_id="accepted", payload=payload, content_digest=_digest(payload)), shot_revisions=list(shot_rows.values()), internal_timeline_revisions=list(internal_rows.values()))
    reloaded = opened(exact)
    reloaded["source_mapping"]["imports"] = {"rev-0": opened(closure), "external-parent": opened(external)}
    inverse = inverse_command(plan.calls, before, reloaded, "pub-replace")
    restored, _ = apply(reloaded, inverse)
    original = commands.entity_states(Checkout(before))
    # Sibling's authoring identity is independently materialized, with identical
    # authored payload; the selected root restores its captured source exactly.
    for sid, value in commands.entity_states(Checkout(restored)).items():
        if sid == "occurrence:b":
            value = {**value, "shot_id": original[sid]["shot_id"]}
        assert value == original[sid]


def test_external_closure_request_read_and_refusal(closure):
    replacement = source(parent="external-parent")
    external = copy.deepcopy(closure)
    external["parent_revision"]["revision_id"] = "external-parent"
    edit = dict(op="occurrence.set", select="occurrence:a", args=dict(source=source(), replacement=replacement))
    body, port = port_for(closure, edit)
    reads = []
    def read(rid):
        reads.append(rid)
        return copy.deepcopy(external if rid == "external-parent" else closure)
    port.revision_closure = read
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "no_change", result
    assert "external-parent" in reads
    body, port = port_for(closure, edit)
    refused = RuntimeCommitService().commit(body, port)
    assert refused["status"] == "refused"
    assert port.accepts == []


def test_overlap_and_implicit_child_trim_refuse(closure):
    before = opened(closure)
    for placement in [dict(start_ms=500), dict(track="other")]:
        edit = dict(op="occurrence.set", select="occurrence:a", args=dict(source=source(), placement=placement))
        with pytest.raises(commands.CommandError):
            apply(before, edit)
    before["shots"][before["placements"][0]["shot_id"]]["internal_timeline"]["clips"].append(dict(id="clip", track="picture", clipType="media", at=0, hold=1))
    trim = dict(op="occurrence.set", select="occurrence:a", args=dict(source=source(), placement=dict(duration_ms=500)))
    with pytest.raises(commands.CommandError, match="explicit child"):
        apply(before, trim)


def test_shared_revision_selected_publication_keeps_sibling_pin(closure):
    body, port = port_for(closure, shot_call(values=dict(name="selected")))
    body["scope"] = dict(target="occurrence:a", content="this-occurrence", shot_id="s", shot_revision_id="shot-1", internal_revision_id="int-1", complete=[], projection_version=1)
    port.body = copy.deepcopy(body)
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "accepted", result
    publication = port.accepts[0]["publication"]
    sibling = next(r for r in publication["parent_composition"]["occurrences"] if r["occurrence_id"] == "b")
    assert sibling == closure["parent_revision"]["payload"]["occurrences"][1]
    assert len(publication["shot_revisions"]) == 1
    assert len(publication["internal_timeline_revisions"]) == 1


def test_graph_inverse_conflicts_on_intervening_child_payload(closure):
    before = opened(closure)
    after, plan = apply(before, add_call())
    inverse = inverse_command(plan.calls, before, after, "pub-add")
    edited = copy.deepcopy(after)
    row = next(r for r in edited["placements"] if r["occurrence_id"] == "new")
    edited["shots"][row["shot_id"]]["payload"]["provenance"]["opaque"] = "intervening"
    with pytest.raises(commands.SemanticConflict):
        apply(edited, inverse)


def test_operation_schema_vectors():
    import json
    from pathlib import Path

    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    root = Path(__file__).parents[2] / "schemas/change-contract"
    envelope = json.loads((root / "opcall.schema.json").read_text())
    schema = json.loads((root / "occurrence-commands.schema.json").read_text())
    registry = Registry().with_resource(envelope["$id"], Resource.from_contents(envelope))
    validator = Draft202012Validator(schema, registry=registry)
    for command in (shot_call(values=dict(name="new", settings=None)), add_call(), add_call("linked"), dict(op="occurrence.set", select="occurrence:a", args=dict(source=source(), placement=dict(start_ms=3000)))):
        validator.validate(command)
    bad = shot_call(values=dict(arbitrary=True))
    assert list(validator.iter_errors(bad))
    overlap = shot_call(values=dict(name="new"), clear=["name"])
    assert list(validator.iter_errors(overlap))


def test_graph_argument_null_is_distinct_from_omission(closure):
    before = opened(closure)
    for key in ("values", "clear"):
        with pytest.raises(commands.CommandError, match="null is a value"):
            apply(before, shot_call(**{key: None}))
    _, plan = apply(before, shot_call(values=dict(settings=None)))
    assert not rebase(plan.calls, before).conflicts


def test_independent_copy_preserves_unknown_reference_looking_strings(closure):
    payload = closure["shot_revisions"][0]["payload"]
    payload["items"][0]["metadata"]["future_item_id"] = "item-1"
    payload["opaque_refs"] = {"source_item_id": "item-1"}
    closure["shot_revisions"][0]["content_digest"] = _digest(payload)
    before = opened(closure)
    after, _ = apply(before, add_call())
    metadata = after["shots"]["new-shot"]["payload"]["items"][0]["metadata"]
    assert after["shots"]["new-shot"]["payload"]["opaque_refs"] == {"source_item_id": "item-1"}
    assert metadata["future_item_id"] == "item-1"
    assert metadata["opaque_literal"] == "item-1"
    assert metadata["source_item_id"] == after["shots"]["new-shot"]["payload"]["items"][0]["item_id"]


@pytest.mark.parametrize("source_kind", ["parent", "direct"])
def test_saved_graph_publication_inverse_replays_local_source_evidence(closure, tmp_path, monkeypatch, source_kind):
    from test_timeline_publication_inverse import HistoryRuntime

    from astrid.sdk.timeline import saved_publish, store
    from astrid.sdk.timeline.saved_intent import read_saved_calls

    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.setattr(Checkout, "SAY_SAVED", False)
    runtime = HistoryRuntime()
    runtime.parents = {"rev-0": copy.deepcopy(closure["parent_revision"])}
    runtime.shots = {r["revision_id"]: copy.deepcopy(r) for r in closure["shot_revisions"]}
    runtime.internals = {r["revision_id"]: copy.deepcopy(r) for r in closure["internal_timeline_revisions"]}
    client = runtime.product()
    body = dict(project_id="p", timeline_id="t", base_revision_id="rev-0")
    monkeypatch.setattr(store, "resolve_ids", lambda *a, **kw: ("p", "t", runtime.current))
    monkeypatch.setattr(store, "fetch_bundle", lambda *a, revision_id=None, **kw: saved_publish._exact(client._transport, body, revision_id or runtime.current))
    draft = Checkout.draft("p", "t")
    operation = add_call()
    if source_kind == "direct":
        from astrid.sdk.timeline.saved_publish import _ClosurePort
        ref = {key: value for key, value in source().items() if key not in {"parent_revision_id", "occurrence_id"}}
        runtime.shots["shot-1"]["internal_timeline_id"] = "inner"
        original_port = runtime.port
        def direct_port(body):
            port = original_port(body)
            parent_read = port.revision_closure
            def read(selection):
                if isinstance(selection, dict):
                    return dict(shot_revision=copy.deepcopy(runtime.shots[selection["shot_revision_id"]]),
                                internal_timeline_revision=copy.deepcopy(runtime.internals[selection["internal_revision_id"]]))
                return parent_read(selection)
            port.revision_closure = read
            return port
        monkeypatch.setattr(runtime, "port", direct_port)
        record = RuntimeCommitService._load_shot_source(_ClosurePort(client._transport, "p", "t"), body, ref)
        draft.bundle["source_mapping"]["pinned_shots"] = {_digest(ref): record}
        operation = add_call(source=ref)
    commands.run(draft, operation)
    assert len(read_saved_calls(Checkout.load(draft.path))) == 1
    added = draft.publish("independent duplicate", client=client)
    assert added["status"] == "accepted", added
    draft = Checkout.load(draft.path)
    assert len(draft.undo(client=client)) == 1
    staged = read_saved_calls(Checkout.load(draft.path))
    assert len(staged) == 1 and staged[0]["op"] == "timeline.inverse"
    undone = Checkout.load(draft.path).publish("undo independent duplicate", client=client)
    assert undone["status"] == "accepted", undone
    assert {r["occurrence_id"] for r in runtime.parents[runtime.current]["payload"]["occurrences"]} == {"a", "b"}
