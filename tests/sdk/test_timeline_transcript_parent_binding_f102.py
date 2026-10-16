"""F102 exact preserved parent request at the binding/compiler source boundary.

The literal request and canonical snapshot are copied without modification from
A's bind-final evidence. Disposable document/scene readers below model admitted
inputs; these tests do not claim an authenticated Runtime or mounted App journey.
"""
import copy
import hashlib
import json
from types import SimpleNamespace

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401
from test_timeline_transcript_projection_f101 import setup as nested_checkout

from astrid.core.timeline import moments as mo
from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
from astrid.sdk.timeline.compiler import TimingInputs, compile_timing
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.managed_transcript import canonical_transcript_json
from astrid.sdk.timeline.source_hydration import hydrate_transcript_sources
from astrid.sdk.timeline.transaction import edit_transaction
from astrid.sdk.timeline.transcript_binding import (
    FrozenTranscript, bound_source_words, follow_bound_anchors, source_words, word_source,
)
from astrid.sdk.timeline.transcripts import (
    RequestBoundTranscriptResolver, install_timing_dependencies, verify_pinned_entries,
)

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")

REQUEST = json.loads(r'''{
  "api_version": 1,
  "project_id": "2e79bc4be70a44c69460b000f1db27b2",
  "timeline_id": "timeline-3bc4c82629e34138ba933bf02bc296e4",
  "request_id": "bind-final-3bc4c82629e34138ba933bf02bc296e4",
  "session_id": "8a98caf21ef54c309797d5585a5dea0f",
  "session_sequence": 1,
  "base_revision_id": "parent-3bc4c82629e34138ba933bf02bc296e4",
  "base_publication_id": "parent-3bc4c82629e34138ba933bf02bc296e4",
  "scope": {
    "target": "parent",
    "complete": [],
    "projection_version": 1
  },
  "change": {
    "commands": [
      {
        "op": "transcript.bind",
        "select": null,
        "args": {
          "target": {
            "clip_id": "clip-3bc4c82629e34138ba933bf02bc296e4",
            "occurrence_id": null
          },
          "expect": {
            "binding": {
              "state": "absent"
            }
          },
          "next": {
            "schema_version": 1,
            "document": {
              "id": "document:10f0a400-9c91-5b2a-88c6-3edbf3db8280",
              "version": 2,
              "content_digest": "sha256:65e6af94a67bfa397d426315fbf51d9bb0020b945811528aabea8ee7f9be2de5"
            },
            "snapshot": {
              "object_id": "sha256:65e6af94a67bfa397d426315fbf51d9bb0020b945811528aabea8ee7f9be2de5",
              "sha256": "65e6af94a67bfa397d426315fbf51d9bb0020b945811528aabea8ee7f9be2de5"
            },
            "subject": {
              "media_object_id": "sha256:d5506b2e6822af73d42a6bc8c2413da9c81dc70d467927f1b48f2b8a38b8f3a6",
              "media_sha256": "sha256:d5506b2e6822af73d42a6bc8c2413da9c81dc70d467927f1b48f2b8a38b8f3a6"
            },
            "source": {
              "producer_id": "media.transcript_publish",
              "source_id": "source-3bc4c82629e34138ba933bf02bc296e4",
              "lineage_id": "lineage-3bc4c82629e34138ba933bf02bc296e4",
              "revision_id": "9b0056c2-f10c-5ed4-bb5d-391dcbe73cae",
              "producer_digest": "sha256:7e6d90eea977fc5be864bd92eab21d1df5e001d3004d41a2d058355dc1bb2d49"
            },
            "clock": {
              "kind": "media",
              "origin_seconds": 0,
              "unit": "seconds"
            },
            "occurrence_id": null,
            "word_ids": [
              "word-3bc4c82629e34138ba933bf02bc296e4"
            ]
          },
          "correspondence": []
        }
      }
    ]
  },
  "source": {
    "via": "script"
  },
  "asserted_actor": {
    "kind": "script",
    "id": "transcript-proof-3bc4c82629e34138ba933bf02bc296e4"
  },
  "dry_run": false
}
''')
SNAPSHOT = b'{"clock":{"kind":"media","origin_seconds":0,"unit":"seconds"},"schema_version":1,"segments":[{"id":"segment-3bc4c82629e34138ba933bf02bc296e4","word_ids":["word-3bc4c82629e34138ba933bf02bc296e4"]}],"source":{"lineage_id":"lineage-3bc4c82629e34138ba933bf02bc296e4","parent_revision_id":"87d2f391-af99-5685-9481-95a1e4d4c0a8","producer_digest":"sha256:7e6d90eea977fc5be864bd92eab21d1df5e001d3004d41a2d058355dc1bb2d49","producer_id":"media.transcript_publish","revision_id":"9b0056c2-f10c-5ed4-bb5d-391dcbe73cae","source_id":"source-3bc4c82629e34138ba933bf02bc296e4"},"subject":{"media_object_id":"sha256:d5506b2e6822af73d42a6bc8c2413da9c81dc70d467927f1b48f2b8a38b8f3a6","media_sha256":"sha256:d5506b2e6822af73d42a6bc8c2413da9c81dc70d467927f1b48f2b8a38b8f3a6"},"words":[{"end_s":0.5,"id":"word-3bc4c82629e34138ba933bf02bc296e4","start_s":0.0,"text":"Correction caf\xc3\xa9"}]}'

def original():
    body = copy.deepcopy(REQUEST)
    binding = body["change"]["commands"][0]["args"]["next"]
    reference = {k: copy.deepcopy(v) for k, v in binding.items()
                 if k not in ("occurrence_id", "word_ids")}
    assert hashlib.sha256(SNAPSHOT).hexdigest() == reference["snapshot"]["sha256"]
    return body, binding, reference


def parent_base(body, binding):
    # An empty shot supplies the film span; the bound target remains the exact
    # parent clip from A's request, never a nested replacement.
    parent = dict(config={}, registry={}, occurrences=[dict(occurrence_id="span", shot_id="span",
        shot_revision_id="span-shot", placement=dict(start_ms=0), duration_ms=5000, track="picture")], clips=[dict(
        id=body["change"]["commands"][0]["args"]["target"]["clip_id"],
        clipType="media", object_id=binding["subject"]["media_object_id"], at=0, hold=1)])
    shot = dict(internal_timeline_revision_id="span-internal", items=[])
    internal = dict(tracks=[], clips=[])
    return open_authoring_bundle(dict(project_id=body["project_id"], timeline_id=body["timeline_id"],
        revision_id=body["base_revision_id"], payload=parent, content_digest=_digest(parent)),
        shot_revisions=[dict(project_id=body["project_id"], shot_id="span", revision_id="span-shot",
            internal_timeline_id="span-timeline", internal_timeline_revision_id="span-internal",
            payload=shot, content_digest=_digest(shot))],
        internal_timeline_revisions=[dict(project_id=body["project_id"], timeline_id="span-timeline",
            revision_id="span-internal", payload=internal, content_digest=_digest(internal))])


def apply_original():
    body, binding, reference = original()
    base = parent_base(body, binding)
    before = copy.deepcopy((body, base))
    record = json.loads(SNAPSHOT)
    reads = []
    def document(docid):
        reads.append(("document", docid))
        return dict(project_id=body["project_id"], document_id=docid, kind="media.transcript/v1",
                    version=reference["document"]["version"], content=copy.deepcopy(record))
    def obj(oid):
        reads.append(("object", oid))
        return dict(data=SNAPSHOT, status=200, headers={})
    port = RequestBoundTranscriptResolver(body, SimpleNamespace(get_document=document),
        SimpleNamespace(get_object=obj), accepted_base=base)
    hydrated = copy.deepcopy(base)
    calls = body["change"]["commands"]
    hydrate_transcript_sources(port, body, hydrated, calls)
    after, plan, _ = RuntimeCommitService._apply(hydrated, calls)
    assert (body, base) == before
    assert body == REQUEST
    assert reads == [("document", reference["document"]["id"]),
                     ("object", reference["snapshot"]["object_id"])]
    return after, plan, binding, reference


def checkout_original():
    after, _, binding, reference = apply_original()
    tl = Checkout(after)
    assert install_timing_dependencies(tl)
    return tl, binding, reference


def test_exact_preserved_parent_request_binds_and_compiles_without_identity_changes():
    after, plan, binding, reference = apply_original()
    clip = after["parent"]["clips"][0]
    target = REQUEST["change"]["commands"][0]["args"]["target"]
    assert target == dict(clip_id=clip["id"], occurrence_id=None)
    assert clip["app"]["transcript"]["binding"] == binding
    assert binding["occurrence_id"] is None
    assert plan.calls[0].args["target"] == target
    tl = Checkout(after)
    assert install_timing_dependencies(tl)
    assert source_words(binding, tl._transcript_dependencies, None) == tuple(json.loads(SNAPSHOT)["words"])
    words = list(tl.words())
    assert [(w.id, w.start, w.end, w.clip_id, w.shot_id) for w in words] == [
        (binding["word_ids"][0], 0, .5, clip["id"], None)]
    assert words[0].source == (reference["document"]["id"], reference["source"]["lineage_id"],
        reference["source"]["revision_id"], "parent/clip:" + clip["id"], reference["snapshot"]["sha256"])
    compiled = compile_authoring_candidate(after).publication
    assert compiled["parent_composition"]["clips"][0]["app"]["transcript"]["binding"] == binding
    assert reference["snapshot"]["object_id"] in {r["media_id"] for r in compiled["dependency_manifest"]["media"]}


@pytest.mark.parametrize("source_in,speed,expected", [(0, 2, [(3, 3.25)]), (.1, 2, [])])
def test_parent_uses_existing_media_clock_trim_and_speed(source_in, speed, expected):
    tl, binding, _ = checkout_original()
    tl.bundle["parent"]["clips"][0].update(at=3, speed=speed, **{"from": source_in, "to": .5})
    tl.resolve()
    assert [(w.start, w.end) for w in tl.words()] == expected
    assert source_words(binding, tl._transcript_dependencies, None)[0]["start_s"] == 0
    assert source_words(binding, tl._transcript_dependencies, None)[0]["end_s"] == .5


@pytest.mark.parametrize("failure", ["missing", "corrupt", "document", "source", "media", "clock", "selection", "duplicate", "absent-occurrence", "fabricated-occurrence"])
def test_parent_refusals_still_precede_timing(failure):
    tl, binding, _ = checkout_original()
    clip_binding = tl.bundle["parent"]["clips"][0]["app"]["transcript"]["binding"]
    if failure == "missing":
        tl._transcript_dependencies = ()
    elif failure == "corrupt":
        dep = tl._transcript_dependencies[0]
        tl._transcript_dependencies = (FrozenTranscript(dep.reference, dep.snapshot_bytes + b" "),)
    elif failure in ("document", "source", "media", "clock"):
        key, field = dict(document=("document", "id"), source=("source", "revision_id"),
                          media=("subject", "media_object_id"), clock=("clock", "unit"))[failure]
        clip_binding[key][field] = "wrong"
    elif failure in ("selection", "duplicate"):
        clip_binding["word_ids"] = ["Correction café"] if failure == "selection" else binding["word_ids"] * 2
    elif failure == "absent-occurrence":
        del clip_binding["occurrence_id"]
    else:
        clip_binding["occurrence_id"] = "fabricated-parent"
    before = copy.deepcopy(tl.bundle)
    with pytest.raises(TimelineEditError):
        compile_timing(TimingInputs(tl.bundle, {"_transcript_dependencies": tl._transcript_dependencies}))
    assert tl.bundle == before


def test_parent_source_order_is_checked_without_deriving_ids():
    _, binding, reference = original()
    # The exact snapshot contains one word. A separate two-row source probes the
    # existing order check rather than claiming that one-row arrangement proves it.
    content = json.loads(SNAPSHOT)
    row = dict(content["words"][0], id="another-opaque-id", start_s=.6, end_s=.8)
    content["words"].append(row)
    raw = json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(raw).hexdigest()
    for pin in (binding, reference):
        pin["snapshot"].update(sha256=digest, object_id="sha256:" + digest)
        pin["document"]["content_digest"] = "sha256:" + digest
    ids = [w["id"] for w in content["words"]]
    binding["word_ids"] = ids
    assert [w["id"] for w in bound_source_words(binding, frozen_reference=reference,
        snapshot_bytes=raw, occurrence_id=None)] == ids
    binding["word_ids"] = ids[::-1]
    with pytest.raises(TimelineEditError, match="source order"):
        bound_source_words(binding, frozen_reference=reference, snapshot_bytes=raw, occurrence_id=None)


@pytest.mark.parametrize("value", [None, "", "wrong", "fabricated-occurrence", "absent"])
def test_nested_binding_requires_the_actual_nonempty_occurrence(value):
    tl = nested_checkout()
    binding = tl.bundle["shots"]["A"]["internal_timeline"]["clips"]
    binding = next(c for c in binding if c["id"] == "a-vo")["app"]["transcript"]["binding"]
    if value == "absent":
        del binding["occurrence_id"]
    else:
        binding["occurrence_id"] = value
    with pytest.raises(TimelineEditError, match="occurrence"):
        compile_timing(TimingInputs(tl.bundle, {"_transcript_dependencies": tl._transcript_dependencies}))


def test_nested_occurrences_keep_distinct_exact_word_identities():
    tl = nested_checkout()
    tl.resolve()
    first, second = list(tl.words())
    assert first.id == second.id == "opaque-beta"
    assert first.source[3] == "occurrence:occ-A/clip:a-vo"
    assert second.source[3] == "occurrence:occ-B/clip:b-vo"
    assert first.source != second.source
    with pytest.raises(TimelineEditError, match="ambiguous"):
        tl.word(first.id)


def parent_anchor():
    tl, binding, reference = checkout_original()
    tl.bundle["parent"]["clips"].append(dict(id="observer", clipType="media",
        object_id=binding["subject"]["media_object_id"], at=1, hold=1, params={}))
    w = next(iter(tl.words()))
    observer = next(c for c in tl.clips() if c.id == "observer")
    intent.set_on(observer.data, mo.format_moment(mo.word_moment(w, tl.words())))
    intent.set_formula(observer.data, "params.x", dict(word=w.id, source=list(w.source), **{"as": "timeline_seconds"}))
    return tl, binding, reference, observer


def test_parent_continuation_retains_exact_owner_and_orphans_cleared_anchors():
    tl, binding, _, observer = parent_anchor()
    clip = tl.bundle["parent"]["clips"][0]
    follow_bound_anchors(tl, clip_id=clip["id"], occurrence_id=None,
        previous_binding=binding, next_binding=binding)
    tl.resolve()
    assert mo.parse(intent.on(observer.data)).source == word_source(binding, clip["id"], parent=True)
    assert not intent.orphan(observer.data)
    del clip["app"]["transcript"]["binding"]
    follow_bound_anchors(tl, clip_id=clip["id"], occurrence_id=None,
        previous_binding=binding, next_binding=None)
    assert "ORPHAN" in intent.orphan(observer.data)
    assert "ORPHAN" in intent.formulas(observer.data)["params.x"]["orphan"]


def test_parent_continuation_rejects_another_clip_before_anchor_writes():
    tl, binding, _, observer = parent_anchor()
    before = copy.deepcopy(observer.data)
    with pytest.raises(TimelineEditError, match="target"):
        follow_bound_anchors(tl, clip_id="observer", occurrence_id=None,
            previous_binding=binding, next_binding=binding)
    assert observer.data == before


def nested_command_case():
    """Independent nested-target probes; never substitute for A's parent request."""
    body, binding, reference = original()
    base = parent_base(body, binding)
    clip = base["parent"]["clips"].pop()
    base["shots"]["span"]["internal_timeline"]["clips"].append(clip)
    args = body["change"]["commands"][0]["args"]
    args["target"]["occurrence_id"] = args["next"]["occurrence_id"] = "span"
    record = json.loads(SNAPSHOT)
    port = RequestBoundTranscriptResolver(body, SimpleNamespace(get_document=lambda docid: dict(
        project_id=body["project_id"], document_id=docid, kind="media.transcript/v1",
        version=reference["document"]["version"], content=record)),
        SimpleNamespace(get_object=lambda oid: dict(data=SNAPSHOT, status=200, headers={})), accepted_base=base)
    hydrate_transcript_sources(port, body, base, body["change"]["commands"])
    return body, base


def test_nested_command_accepts_only_its_exact_occurrence_target():
    body, base = nested_command_case()
    after, _, _ = RuntimeCommitService._apply(base, body["change"]["commands"])
    value = after["shots"]["span"]["internal_timeline"]["clips"][0]["app"]["transcript"]["binding"]
    assert value["occurrence_id"] == "span"
    assert not after["parent"]["clips"]


@pytest.mark.parametrize("side", ["target", "next"])
@pytest.mark.parametrize("value", [None, "", "wrong", "fabricated-occurrence", "absent"])
def test_nested_command_refuses_null_missing_wrong_or_fabricated_occurrence(side, value):
    body, base = nested_command_case()
    args = body["change"]["commands"][0]["args"]
    if value == "absent":
        del args[side]["occurrence_id"]
    else:
        args[side]["occurrence_id"] = value
    before = copy.deepcopy(base)
    with pytest.raises(ValueError):
        RuntimeCommitService._apply(base, body["change"]["commands"])
    assert base == before


def continuation(binding, next_binding, correspondence=()):
    call = copy.deepcopy(REQUEST["change"]["commands"][0])
    call["args"].update(expect=dict(binding=dict(state="present", value=copy.deepcopy(binding))),
                        next=copy.deepcopy(next_binding), correspondence=list(correspondence))
    return call


def test_exact_parent_fresh_bind_inverse_and_redo_preserve_identity():
    after, plan, binding, _ = apply_original()
    body, _, _ = original()
    base = parent_base(body, binding)
    inverse = inverse_command(plan.calls, base, after, "parent-fresh-bind")
    undone, undo_plan, _ = RuntimeCommitService._apply(after, [inverse])
    assert undone["parent"] == base["parent"]
    redo = inverse_command(undo_plan.calls, after, undone, "parent-fresh-undo")
    redone, _, _ = RuntimeCommitService._apply(undone, [redo])
    assert redone["parent"] == after["parent"]
    assert redone["source_mapping"]["pinned_transcripts"] == after["source_mapping"]["pinned_transcripts"]
    cleared, clear_plan, _ = RuntimeCommitService._apply(after, [continuation(binding, {"op": "clear"})])
    assert "binding" not in cleared["parent"]["clips"][0]["app"]["transcript"]
    clear_inverse = inverse_command(clear_plan.calls, after, cleared, "parent-clear")
    restored, _, _ = RuntimeCommitService._apply(cleared, [clear_inverse])
    assert restored["parent"] == after["parent"]


def test_parent_command_retains_same_source_then_clear_orphans_and_blocks_acceptance():
    tl, binding, _, _ = parent_anchor()
    before = copy.deepcopy(tl.document())
    retained, _, _ = RuntimeCommitService._apply(before, [continuation(binding, binding)])
    assert retained["parent"] == before["parent"]
    clear = continuation(binding, {"op": "clear"})
    with pytest.raises(ValueError, match="ORPHAN"):
        RuntimeCommitService._apply(retained, [clear])
    candidate = Checkout(copy.deepcopy(retained))
    with edit_transaction(candidate, "parent clear", quiet=True, persist=False) as tx:
        commands.execute(candidate, clear)
    owner, observer = candidate.document()["parent"]["clips"]
    assert "binding" not in owner["app"]["transcript"]
    assert "ORPHAN" in intent.orphan(observer)
    assert "ORPHAN" in intent.formulas(observer)["params.x"]["orphan"]
    assert tx.plan.blocking
    assert retained["parent"] == before["parent"]
    assert before == tl.document()


@pytest.mark.parametrize("anchored", [True, False])
def test_parent_command_rebind_inverse_keeps_verified_old_new_offline_closure(anchored):
    check_command_rebind_offline_closure(anchored)


def test_nested_command_rebind_records_only_its_changed_anchor_paths():
    check_command_rebind_offline_closure(True, occurrence_id="span", extra_anchors=True)


def check_command_rebind_offline_closure(anchored, occurrence_id=None, extra_anchors=False):
    tl, binding, reference, observer = parent_anchor()
    owner = tl.bundle["parent"]["clips"][0]
    if occurrence_id is not None:
        tl.bundle["parent"]["clips"].remove(owner)
        tl.bundle["shots"]["span"]["internal_timeline"]["clips"].append(owner)
        binding["occurrence_id"] = occurrence_id
        owner["app"]["transcript"]["binding"] = copy.deepcopy(binding)
        source = word_source(binding, owner["id"])
        moment = mo.format_moment(mo.Moment("word", source=source, word_id=binding["word_ids"][0]))
        intent.set_on(observer.data, moment)
        intent.set_formula(observer.data, "params.x", dict(word=binding["word_ids"][0],
            source=list(source), **{"as": "timeline_seconds"}))
    if extra_anchors:
        intent.set_until(observer.data, intent.on(observer.data) + " +0.5s")
        intent.set_formula(observer.data, "params.y", dict(moment=intent.on(observer.data)))
    if not anchored:
        intent.set_on(observer.data, None)
        intent.set_formula(observer.data, "params.x", None)
    observer.data["opaque"] = {"keep": [None, "parent-owner"]}
    # Compare accepted compiled states: at/hold/formula outputs are recomputed
    # consequences, not authored values for the inverse to restore verbatim.
    tl.resolve()
    before = copy.deepcopy(tl.document())
    record = json.loads(SNAPSHOT)
    record["source"].update(revision_id="parent-correction-3",
                            parent_revision_id=binding["source"]["revision_id"])
    record["words"][0]["text"] = "Second correction café"
    if extra_anchors:
        record["words"][0].update(start_s=.2, end_s=.7)
    raw = canonical_transcript_json(record).encode()
    digest = hashlib.sha256(raw).hexdigest()
    next_binding = copy.deepcopy(binding)
    next_binding["source"]["revision_id"] = record["source"]["revision_id"]
    next_binding["document"].update(version=3, content_digest="sha256:" + digest)
    next_binding["snapshot"] = dict(object_id="sha256:" + digest, sha256=digest)
    next_reference = {k: copy.deepcopy(v) for k, v in next_binding.items()
                      if k not in ("occurrence_id", "word_ids")}
    pairs = [dict(**{"from": dict(lineage_id=binding["source"]["lineage_id"],
                                  word_id=binding["word_ids"][0])},
                  to=dict(lineage_id=next_binding["source"]["lineage_id"],
                          word_id=next_binding["word_ids"][0]))]
    call = continuation(binding, next_binding, pairs)
    call["args"]["target"]["occurrence_id"] = occurrence_id
    body = copy.deepcopy(REQUEST)
    body["change"]["commands"] = [call]
    objects = {reference["snapshot"]["object_id"]: SNAPSHOT,
               next_reference["snapshot"]["object_id"]: raw}
    reads = []
    def get_object(oid):
        reads.append(oid)
        return dict(data=objects[oid], status=200, headers={})
    port = RequestBoundTranscriptResolver(body, SimpleNamespace(get_document=lambda docid: dict(
        project_id=body["project_id"], document_id=docid, kind="media.transcript/v1",
        version=3, content=copy.deepcopy(record))), SimpleNamespace(get_object=get_object),
        accepted_base=before)
    hydrated = copy.deepcopy(before)
    hydrate_transcript_sources(port, body, hydrated, [call])
    after, plan, _ = RuntimeCommitService._apply(hydrated, [call])
    owner = (after["parent"]["clips"][0] if occurrence_id is None else
             after["shots"]["span"]["internal_timeline"]["clips"][0])
    followed = next(c for c in after["parent"]["clips"] if c["id"] == "observer")
    assert owner["id"] == call["args"]["target"]["clip_id"]
    assert owner["app"]["transcript"]["binding"] == next_binding
    assert next_binding["occurrence_id"] == occurrence_id
    assert followed["opaque"] == observer.data["opaque"]
    recorded = commands.EditCommand.coerce(plan.calls[0])
    direct = {commands.write_target(key, recorded.resolved)
              for key, kind in recorded.authorship.items() if kind == "direct"}
    owner_id = word_source(binding, owner["id"], parent=occurrence_id is None)[3]
    expected_paths = {(owner_id, "app.transcript.binding")}
    if anchored:
        expected_paths.update({("parent/clip:observer", "intent.on"),
                               ("parent/clip:observer", 'intent.formulas["params.x"].source')})
    if extra_anchors:
        expected_paths.update({("parent/clip:observer", "intent.until"),
                               ("parent/clip:observer", 'intent.formulas["params.y"].moment')})
    assert direct == expected_paths
    assert {(w["id"], w["path"]) for w in plan.direct_writes if w["id"] != owner_id} == (
        expected_paths - {(owner_id, "app.transcript.binding")})
    original_states = commands.entity_states(Checkout(copy.deepcopy(hydrated)))
    for sid, path in expected_paths:
        assert recorded.expect[commands.write_key(sid, path, recorded.resolved)] == commands.state_at(original_states, sid, path)
    assert all(kind == "consequence" for key, kind in recorded.authorship.items()
               if commands.write_target(key, recorded.resolved)[1] in {"at", "hold", "params.x"})
    if extra_anchors:
        assert {("parent/clip:observer", "at"), ("parent/clip:observer", "params.x")} <= {
            (w["id"], w["path"]) for w in plan.consequences}
    if anchored:
        expected = word_source(next_binding, owner["id"], parent=occurrence_id is None)
        assert mo.parse(intent.on(followed)).source == expected
        assert tuple(intent.formulas(followed)["params.x"]["source"]) == expected
        assert not intent.orphan(followed)

    # Omitting correspondence must retain an orphan diagnostic and refuse
    # acceptance, rather than inferring continuity from matching IDs or text.
    if anchored:
        unmatched = continuation(binding, next_binding)
        unmatched["args"]["target"]["occurrence_id"] = occurrence_id
        with pytest.raises(ValueError, match="ORPHAN"):
            RuntimeCommitService._apply(hydrated, [unmatched])
        candidate = Checkout(copy.deepcopy(hydrated))
        with edit_transaction(candidate, "unmatched parent rebind", quiet=True, persist=False) as tx:
            commands.execute(candidate, unmatched)
        orphan = next(c for c in candidate.document()["parent"]["clips"] if c["id"] == "observer")
        assert "ORPHAN" in intent.orphan(orphan)
        assert "ORPHAN" in intent.formulas(orphan)["params.x"]["orphan"]
        assert tx.plan.blocking

    inverse = inverse_command(plan.calls, hydrated, after, "parent-rebind")
    assert {(w["id"], w["path"]) for w in inverse["args"]["writes"]} == expected_paths
    inverse_body = copy.deepcopy(body)
    inverse_body["change"]["commands"] = [inverse]
    readonly = SimpleNamespace(get_document=lambda *a: pytest.fail("offline must not read current document"))
    no_history = RequestBoundTranscriptResolver(inverse_body, readonly,
        SimpleNamespace(get_object=get_object), accepted_base=after)
    with pytest.raises(ValueError, match="allowlist"):
        hydrate_transcript_sources(no_history, inverse_body, copy.deepcopy(after), [inverse])
    offline = RequestBoundTranscriptResolver(inverse_body, readonly,
        SimpleNamespace(get_object=get_object), accepted_base=after,
        accepted_history=[reference, next_reference])
    restored = copy.deepcopy(after)
    reads.clear()
    hydrate_transcript_sources(offline, inverse_body, restored, [inverse])
    assert set(reads) == set(objects)
    undone, undo_plan, _ = RuntimeCommitService._apply(restored, [inverse])
    assert undone["parent"] == before["parent"]
    assert undone["shots"] == before["shots"]
    redo = inverse_command(undo_plan.calls, after, undone, "parent-rebind-undo")
    redone, _, _ = RuntimeCommitService._apply(undone, [redo])
    assert redone["parent"] == after["parent"]
    assert redone["shots"] == after["shots"]
    for state in (after, undone, redone):
        pins = verify_pinned_entries(body["project_id"], state["source_mapping"]["pinned_transcripts"])
        assert len(pins) == 2
        assert {p["canonical_record_json"].encode() for p in pins.values()} == {SNAPSHOT, raw}
        compiled = compile_authoring_candidate(state).publication
        media = {row["media_id"] for row in compiled["dependency_manifest"]["media"]}
        active_owner = (state["parent"]["clips"][0] if occurrence_id is None else
                        state["shots"]["span"]["internal_timeline"]["clips"][0])
        active = active_owner["app"]["transcript"]["binding"]
        assert active["snapshot"]["object_id"] in media
    assert before == tl.document()
    del objects[reference["snapshot"]["object_id"]]
    with pytest.raises(KeyError):
        hydrate_transcript_sources(offline, inverse_body, copy.deepcopy(after), [inverse])
