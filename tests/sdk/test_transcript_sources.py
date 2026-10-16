"""Synthetic request-bound transcript hydration and existing command closure."""
import copy
import hashlib
from types import SimpleNamespace

import pytest
from test_timeline_commit import request
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
from astrid.sdk.managed_transcript import canonical_transcript_json, transcript_document_id
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.source_hydration import hydrate_transcript_sources
from astrid.sdk.timeline.transcripts import (
    FrozenTranscriptSource,
    RequestBoundTranscriptResolver,
    TranscriptSourceSelection,
    digest_bytes,
    verify_pinned_entries,
)

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


@pytest.fixture
def source():
    media = b"synthetic-media-only"
    record = dict(schema_version=1,
        subject=dict(media_object_id=digest_bytes(media), media_sha256=hashlib.sha256(media).hexdigest()),
        source=dict(producer_id="media.transcript_publish", source_id="take-1", lineage_id="lineage-1",
                    revision_id="revision-1", producer_digest="a" * 64),
        clock=dict(kind="media", unit="seconds", origin_seconds=0),
        words=[dict(id="opaque:1", text="Hello", start_s=0, end_s=.4)],
        segments=[dict(id="segment-1", word_ids=["opaque:1"])])
    raw = canonical_transcript_json(record).encode()
    descriptor = dict(schema_version=1,
        document=dict(id=transcript_document_id("p", record["subject"], record["source"]), version=1, content_digest=digest_bytes(raw)),
        snapshot=dict(object_id=digest_bytes(raw), sha256=hashlib.sha256(raw).hexdigest()),
        **{k: copy.deepcopy(record[k]) for k in ("subject", "source", "clock")})
    return record, raw, descriptor


@pytest.fixture
def base(source):
    record, _, _ = source
    parent = dict(config=dict(app=dict(transcript=dict(file="managed.json", opaque={"keep": True}))), registry={},
        clips=[dict(id="clip-1", clipType="media", object_id=record["subject"]["media_object_id"], at=0, hold=1)], occurrences=[dict(occurrence_id="a", shot_id="s", shot_revision_id="shot-1", placement=dict(start_ms=0), duration_ms=1000, track="picture")])
    shot = dict(internal_timeline_revision_id="int-1", items=[])
    internal = dict(tracks=[], clips=[])
    return open_authoring_bundle(dict(project_id="p", timeline_id="t", revision_id="rev-0", payload=parent,
        content_digest=_digest(parent)),
        shot_revisions=[dict(project_id="p", shot_id="s", revision_id="shot-1", internal_timeline_id="inner", internal_timeline_revision_id="int-1", payload=shot, content_digest=_digest(shot))],
        internal_timeline_revisions=[dict(project_id="p", timeline_id="inner", revision_id="int-1", payload=internal, content_digest=_digest(internal))])


def reference(source, *, expect=None, next=None):
    d = source[2]
    return dict(op="transcript.reference", select=None, args=dict(subject=d["subject"],
        source_key={k: d["source"][k] for k in ("producer_id", "source_id")},
        expect={"state": "absent"} if expect is None else expect, next=d if next is None else next))


def bind(source, *, expect=None, next=None):
    d = dict(copy.deepcopy(source[2]), occurrence_id=None, word_ids=["opaque:1"])
    return dict(op="transcript.bind", select=None, args=dict(target=dict(clip_id="clip-1", occurrence_id=None),
        expect=dict(binding={"state": "absent"} if expect is None else expect),
        next=d if next is None else next, correspondence=[]))


def resolver(body, base, source, *, version=1, raw=None, accepted_history=()):
    reads = []
    record, snapshot, descriptor = source
    def document(docid):
        reads.append(("document", docid))
        return dict(project_id="p", document_id=docid, kind="media.transcript/v1", version=version, content=copy.deepcopy(record))
    def obj(oid):
        reads.append(("object", oid))
        return dict(data=snapshot if raw is None else raw, status=200, headers={})
    port = RequestBoundTranscriptResolver(body, SimpleNamespace(get_document=document), SimpleNamespace(get_object=obj),
        accepted_base=base, accepted_history=accepted_history)
    return port, reads


def hydrated(base, source, *calls):
    body = request(*calls)
    port, reads = resolver(body, base, source)
    detached = copy.deepcopy(base)
    hydrate_transcript_sources(port, body, detached, calls)
    return detached, reads


def test_read_only_exact_capture_and_zero_document_writes(base, source):
    call = bind(source)
    body = request(call)
    port, reads = resolver(body, base, source)
    selection = TranscriptSourceSelection.from_reference("p", source[2])
    capture = port.resolve_transcript_source(body, selection)
    assert capture.snapshot_bytes == source[1]
    assert capture.request_digest == _digest(body)
    assert [r[0] for r in reads] == ["document", "object"]
    with pytest.raises(TypeError):
        FrozenTranscriptSource(selection, source[1], _digest(body))


def test_selection_allowlist_and_request_binding(base, source):
    body = request(reference(source))
    port, reads = resolver(body, base, source)
    changed = copy.deepcopy(source[2])
    changed["document"]["version"] = 2
    for req, selection in [(dict(body, request_id="other"), TranscriptSourceSelection.from_reference("p", source[2])),
                           (body, TranscriptSourceSelection.from_reference("p", changed))]:
        with pytest.raises(ValueError):
            port.resolve_transcript_source(req, selection)
    assert reads == []
    empty = request()
    port, reads = resolver(empty, base, source)
    with pytest.raises(ValueError):
        port.resolve_transcript_source(empty, TranscriptSourceSelection.from_reference("p", source[2]))
    assert reads == []


@pytest.mark.parametrize("version,raw", [(2, None), (1, b"changed"), (1, b"")])
def test_advanced_document_and_missing_changed_objects_refuse(base, source, version, raw):
    body = request(bind(source))
    port, _ = resolver(body, base, source, version=version, raw=raw)
    with pytest.raises(ValueError):
        hydrate_transcript_sources(port, body, base, body["change"]["commands"])


def test_wrong_capture_request_or_source_refuses(base, source):
    body = request(bind(source))
    port, _ = resolver(body, base, source)
    selection = TranscriptSourceSelection.from_reference("p", source[2])
    other = dict(body, request_id="other")
    other_port, _ = resolver(other, base, source)
    capture = other_port.resolve_transcript_source(other, selection)
    with pytest.raises(ValueError):
        hydrate_transcript_sources(SimpleNamespace(resolve_transcript_source=lambda *a: capture), body, base, body["change"]["commands"])


def test_reference_preserves_declaration_and_undo_redo_offline(base, source):
    call = reference(source)
    detached, _ = hydrated(base, source, call)
    after, plan, _ = RuntimeCommitService._apply(detached, [call])
    ns = after["parent"]["config"]["app"]["transcript"]
    assert ns["file"] == "managed.json" and ns["opaque"] == {"keep": True} and ns["v"] == 1
    assert len(ns["references"]) == 1
    assert "transcript" not in after["parent"]["clips"][0].get("app", {})
    inverse = inverse_command(plan.calls, detached, after, "accepted-synthetic")
    undone, inverse_plan, _ = RuntimeCommitService._apply(after, [inverse])
    assert undone["parent"] == detached["parent"]
    redo = inverse_command(inverse_plan.calls, after, undone, "undo-synthetic")
    redone, _, _ = RuntimeCommitService._apply(undone, [redo])
    assert redone["parent"] == after["parent"]
    assert redone["source_mapping"]["pinned_transcripts"] == after["source_mapping"]["pinned_transcripts"]
    assert rebase(plan.calls, detached).conflicts == ()
    damaged = copy.deepcopy(undone)
    damaged["source_mapping"]["pinned_transcripts"] = {}
    with pytest.raises(ValueError):
        RuntimeCommitService._apply(damaged, [redo])
    damaged = copy.deepcopy(undone)
    next(iter(damaged["source_mapping"]["pinned_transcripts"].values()))["canonical_record_json"] = "{}"
    with pytest.raises(ValueError):
        RuntimeCommitService._apply(damaged, [redo])


def test_binding_exact_target_words_expectation_and_clear(base, source):
    call = bind(source)
    detached, _ = hydrated(base, source, call)
    after, plan, _ = RuntimeCommitService._apply(detached, [call])
    value = after["parent"]["clips"][0]["app"]["transcript"]["binding"]
    assert plan.calls[0].expect and plan.calls[0].authorship
    clear = bind(source, expect=dict(state="present", value=value), next={"op": "clear"})
    cleared, _, _ = RuntimeCommitService._apply(after, [clear])
    assert "binding" not in cleared["parent"]["clips"][0]["app"]["transcript"]
    for mutation in [lambda c: c["args"]["next"].update(occurrence_id="other"),
                     lambda c: c["args"]["next"].update(word_ids=["missing"]),
                     lambda c: c["args"].update(expect={"binding": None})]:
        bad = copy.deepcopy(call)
        mutation(bad)
        with pytest.raises(ValueError):
            RuntimeCommitService._apply(detached, [bad])
    assert "app" not in base["parent"]["clips"][0]


def test_accepted_binding_offline_uses_cas_without_current_document(base, source):
    detached, _ = hydrated(base, source, bind(source))
    after, _, _ = RuntimeCommitService._apply(detached, [bind(source)])
    body = request()
    port, reads = resolver(body, after, source, version=99)
    hydrate_transcript_sources(port, body, after, [])
    assert [r[0] for r in reads] == ["object"]
    entries = after["source_mapping"]["pinned_transcripts"]
    assert verify_pinned_entries("p", entries) == entries
    with pytest.raises(ValueError):
        verify_pinned_entries("other", entries)


def test_one_batch_final_state_and_detached_prefix_probes(base, source, monkeypatch):
    calls = [reference(source), bind(source)]
    detached, _ = hydrated(base, source, *calls)
    from astrid.sdk.timeline import transaction
    original = Checkout.resolve
    instances = []
    def resolve(self, *args, **kwargs):
        result = original(self, *args, **kwargs)
        instances.append((self, self.document()))
        return result
    monkeypatch.setattr(Checkout, "resolve", resolve)
    # Existing prefix probes may resolve detached instances
    # Only the working
    # transaction's final compiler state counts here.
    tl = Checkout(copy.deepcopy(detached))
    with transaction.edit_transaction(tl, "bind batch", quiet=True, persist=False) as tx:
        for call in calls:
            commands.execute(tl, call)
    final_states = [state for instance, state in instances if instance is tl]
    assert final_states and all(state == final_states[0] for state in final_states)
    assert len(tx.plan.calls) == 2
    assert compile_authoring_candidate(tl.document()).publication["parent_composition"]["clips"][0]["app"]["transcript"]["binding"]["word_ids"] == ["opaque:1"]


def test_old_and_new_dependency_closure_survives_rebind_inverse_and_offline_export(base, source):
    detached, _ = hydrated(base, source, bind(source))
    old, _, _ = RuntimeCommitService._apply(detached, [bind(source)])
    old_binding = old["parent"]["clips"][0]["app"]["transcript"]["binding"]
    new_record = copy.deepcopy(source[0])
    new_record["source"].update(revision_id="revision-2", parent_revision_id="revision-1")
    new_record["words"][0]["text"] = "Corrected"
    new_raw = canonical_transcript_json(new_record).encode()
    new_descriptor = copy.deepcopy(source[2])
    new_descriptor.update(source={k: new_record["source"][k] for k in source[2]["source"]})
    new_descriptor["document"].update(version=2, content_digest=digest_bytes(new_raw))
    new_descriptor["snapshot"] = dict(object_id=digest_bytes(new_raw), sha256=hashlib.sha256(new_raw).hexdigest())
    new_source = (new_record, new_raw, new_descriptor)
    call = bind(new_source, expect=dict(state="present", value=old_binding))
    body = request(call)
    objects = {source[2]["snapshot"]["object_id"]: source[1], new_descriptor["snapshot"]["object_id"]: new_raw}
    reads = []
    def get_object(oid):
        reads.append(oid)
        return dict(data=objects[oid], status=200, headers={})
    port = RequestBoundTranscriptResolver(body,
        SimpleNamespace(get_document=lambda docid: dict(project_id="p", document_id=docid,
            kind="media.transcript/v1", version=2, content=new_record)),
        SimpleNamespace(get_object=get_object), accepted_base=old)
    hydrate_transcript_sources(port, body, old, [call])
    after, plan, _ = RuntimeCommitService._apply(old, [call])
    assert len(after["source_mapping"]["pinned_transcripts"]) == 2
    inverse = inverse_command(plan.calls, old, after, "accepted-rebind")
    # Both descriptors are retained in authenticated acceptance/history evidence.
    # Without that evidence, an inverse is only a locator and cannot read old CAS.
    inverse_body = request(inverse)
    readonly = SimpleNamespace(get_document=lambda *a: pytest.fail("offline history must not read current"))
    no_history = RequestBoundTranscriptResolver(inverse_body, readonly,
        SimpleNamespace(get_object=get_object), accepted_base=after)
    with pytest.raises(ValueError, match="allowlist"):
        hydrate_transcript_sources(no_history, inverse_body, copy.deepcopy(after), [inverse])
    offline = RequestBoundTranscriptResolver(inverse_body, readonly,
        SimpleNamespace(get_object=get_object), accepted_base=after, accepted_history=[source[2], new_descriptor])
    restored_base = copy.deepcopy(after)
    hydrate_transcript_sources(offline, inverse_body, restored_base, [inverse])
    undone, inverse_plan, _ = RuntimeCommitService._apply(restored_base, [inverse])
    assert undone["parent"]["clips"][0]["app"]["transcript"]["binding"] == old_binding
    redo = inverse_command(inverse_plan.calls, after, undone, "accepted-undo")
    redone, _, _ = RuntimeCommitService._apply(undone, [redo])
    assert redone["parent"] == after["parent"]
    for document in (after, undone, redone):
        assert len(verify_pinned_entries("p", document["source_mapping"]["pinned_transcripts"])) == 2
    media = compile_authoring_candidate(redone).publication["dependency_manifest"]["media"]
    assert new_descriptor["snapshot"]["object_id"] in {row["media_id"] for row in media}
    del objects[source[2]["snapshot"]["object_id"]]
    with pytest.raises(KeyError):
        hydrate_transcript_sources(offline, inverse_body, copy.deepcopy(after), [inverse])


def test_snapshot_descriptor_project_identity_and_clock_mismatches_refuse(source):
    for change in [lambda d: d["document"].update(id="document:wrong"),
                   lambda d: d["snapshot"].update(object_id="sha256:" + "f" * 64),
                   lambda d: d["clock"].update(origin_seconds=1),
                   lambda d: d["document"].update(version=True)]:
        descriptor = copy.deepcopy(source[2])
        change(descriptor)
        with pytest.raises(ValueError):
            TranscriptSourceSelection.from_reference("p", descriptor)


def test_commit_acceptance_retains_verified_transcript_evidence(base, source):
    from test_timeline_commit import CoreService, Port
    call = bind(source)
    body = request(call)
    port = Port(body, {"rev-0": base})
    transcript_port, reads = resolver(body, base, source)
    port.resolve_transcript_source = transcript_port.resolve_transcript_source
    result = CoreService().commit(body, port)
    assert result["status"] == "accepted", result
    assert len(port.accepts) == 1
    evidence = port.accepts[0]["evidence"]["transcripts"]
    assert verify_pinned_entries("p", evidence) == evidence
    assert port.accepts[0]["result"]["canonical_document"]["source_mapping"]["pinned_transcripts"] == evidence
    assert [r[0] for r in reads] == ["document", "object"]
    assert port.accepts[0]["publication"]["parent_composition"]["clips"][0]["app"]["transcript"]["binding"] == call["args"]["next"]


def test_unselected_accepted_history_does_not_expand_source_allowlist(base, source):
    body = request()
    port, reads = resolver(body, base, source, accepted_history=[source[2]])
    selection = TranscriptSourceSelection.from_reference("p", source[2])
    with pytest.raises(ValueError, match="allowlist"):
        port.resolve_transcript_source(body, selection)
    assert reads == []


def runtime_adapter(body, base, source, history=()):
    from astrid.sdk.timeline.source_hydration import _runtime_transcript_resolver
    compiled = compile_authoring_candidate(base).publication
    parent = dict(project_id=body["project_id"], timeline_id=body["timeline_id"],
                  revision_id=body["base_revision_id"], payload=compiled["parent_composition"],
                  content_digest=_digest(compiled["parent_composition"]))
    # These adapter tests exercise parent references. Child closure/reload is
    # exercised against Runtime in test_transcript_commit.py.
    parent["payload"]["occurrences"] = []
    parent["content_digest"] = _digest(parent["payload"])
    shots, internals = [], []
    reads = []
    def document(docid):
        reads.append("document")
        return dict(project_id="p", document_id=docid, version=1, kind="media.transcript/v1", content=source[0])
    def obj(oid):
        reads.append("object")
        return dict(status=200, data=source[1])
    port = _runtime_transcript_resolver(body,
        dict(parent_revision=parent, shot_revisions=shots, internal_timeline_revisions=internals),
        history, document_reader=document, object_reader=obj)
    return port, reads


def test_runtime_adapter_uses_sole_capture_codec_and_exact_closure(base, source):
    body = request(reference(source))
    port, reads = runtime_adapter(body, base, source)
    capture = port.resolve_transcript_source(body, TranscriptSourceSelection.from_reference("p", source[2]))
    assert isinstance(capture, FrozenTranscriptSource) and capture.snapshot_bytes == source[1]
    assert capture.request_digest == _digest(body) and reads == ["document", "object"]


def test_runtime_adapter_reconstructs_accepted_reference_without_document(base, source):
    accepted, _ = hydrated(base, source, reference(source))
    accepted, _, _ = RuntimeCommitService._apply(accepted, [reference(source)])
    body = request()
    port, reads = runtime_adapter(body, accepted, source)
    capture = port.resolve_transcript_source(body, TranscriptSourceSelection.from_reference("p", source[2]))
    assert capture.snapshot_bytes == source[1] and reads == ["object"]


def test_runtime_adapter_rejects_changed_history_bytes(base, source):
    detached, _ = hydrated(base, source, reference(source))
    entries = copy.deepcopy(detached["source_mapping"]["pinned_transcripts"])
    next(iter(entries.values()))["canonical_record_json"] = "{}"
    with pytest.raises(ValueError, match="immutable transcript object"):
        runtime_adapter(request(reference(source)), base, source, [entries])
