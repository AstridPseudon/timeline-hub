"""Disposable exact-take consumer evidence; no provider or real project data."""
import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_timeline_commit import CoreService, Port, request
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands, narration
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


def take(text="Hello world!", *, voice="fixture", rate="+0%", duration=1.25, tag=""):
    audio = hashlib.sha256((text + voice + rate + tag).encode()).hexdigest()
    words = [{"word": word, "start_s": i * duration / len(text.split()),
              "end_s": (i + .8) * duration / len(text.split())} for i, word in enumerate(text.split())]
    manifest = dict(schema_version=1, text=text, text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                    settings={**narration.DEFAULT_SETTINGS, "voice": voice, "rate": rate},
                    audio_sha256=audio, duration_seconds=duration)
    word_doc = dict(schema_version=1, audio_sha256=audio, duration_seconds=duration, words=words)
    refs = {"speech": dict(association_id="speech-" + audio, object_id="sha256:" + audio)}
    for port, doc in (("speech_words", word_doc), ("speech_manifest", manifest)):
        refs[port] = dict(association_id=port + "-" + audio, object_id="sha256:" + narration.digest(doc))
    return dict(refs=refs, speech=dict(object_id=refs["speech"]["object_id"], size=27,
                                     media_type="audio/wav", duration_seconds=duration), manifest=manifest, words=word_doc)


def line(oid, cid, selected, *, segment="same", gap=None):
    value = dict(occurrence_id=oid, clip_id=cid, segment=segment,
                 text=selected["manifest"]["text"], take=copy.deepcopy(selected["refs"]))
    if gap is not None:
        value["gap_after_s"] = gap
    return value


def op(*lines, remove=()):
    return dict(op="timeline.apply-script", select=None,
                args=dict(spec=dict(version=1, lines=list(lines), remove=list(remove))))


def pinned(bundle, rid="rev-0"):
    pub = compile_authoring_candidate(bundle).publication
    return open_authoring_bundle(dict(project_id="p", timeline_id="t", revision_id=rid,
                                     payload=pub["parent_composition"], content_digest=_digest(pub["parent_composition"])),
        shot_revisions=[dict(r, project_id="p") for r in pub["shot_revisions"]],
        internal_timeline_revisions=[dict(r, project_id="p") for r in pub["internal_timeline_revisions"]])


def sample(*, same_clip_ids=False):
    bundle = Checkout(json.loads((Path(__file__).parents[1] / "fixtures/timeline_editing/tiny_publishable.json").read_text())).document()
    takes = [take(), take("Second line.", tag="B")]
    for sid, selected in zip(("A", "B"), takes):
        internal = bundle["shots"][sid]["internal_timeline"]
        internal["clips"] = [c for c in internal["clips"] if not c["id"].endswith(("rocket", "music", "type"))]
        voice = next(c for c in internal["clips"] if intent.line(c))
        if same_clip_ids:
            voice["id"] = "vo"
        asset = "speech-" + selected["refs"]["speech"]["object_id"][7:]
        internal["registry"]["assets"][asset] = dict(object_id=selected["speech"]["object_id"], type="audio", duration=1.25)
        voice.update(asset=asset, **{"from": 0, "to": 1.25})
        intent.set_line(voice, "same", [[w["start_s"], w["end_s"], w["word"], f"{sid}-word-{i}"]
                                         for i, w in enumerate(selected["words"]["words"])])
        intent.set_line_text(voice, selected["manifest"]["text"])
        intent.set_line_take(voice, selected["refs"])
        voice["opaque"] = {"owner": sid, "unicode": "é"}
        bundle["shots"][sid]["payload"]["text_bindings"] = []
    return pinned(bundle), {narration.take_key(t["refs"]): t for t in takes}


class NarrationPort(Port):
    def __init__(self, body, bundle, takes):
        super().__init__(body, {"rev-0": bundle})
        self.takes, self.take_reads = copy.deepcopy(takes), []

    def narration_take(self, refs):
        self.take_reads.append(copy.deepcopy(refs))
        return copy.deepcopy(self.takes[narration.take_key(refs)])


def execute(bundle, takes, *ops, head=None):
    body = request(*ops)
    port = NarrationPort(body, bundle, takes)
    if head is not None:
        port.current = "head-1"
        port.bundles["head-1"] = head
    return CoreService().commit(body, port), port


@pytest.mark.parametrize("text,words", [("Hello world!", ["Hello", "world!"]),
    ("Hello\tworld!", ["Hello", "world!"]), ("Café 12.", ["Café", "12."])])
def test_boundary_accepts_only_explicit_whitespace_formatting(text, words):
    narration.validate_speech_boundary(text, [{"word": w} for w in words])


@pytest.mark.parametrize("text,words", [("Hello world!", ["Hello", "world"]),
    ("Hello world!", ["hello", "world!"]), ("Hello world!", ["world!", "Hello"]),
    ("Hello world!", ["Hello"]), ("12", ["twelve"]), ("Café", ["Cafe\u0301"]),
    ("Hello world!", ["Hello world!"])])
def test_exact_missing_reordered_numeric_and_format_mismatch_refused(text, words):
    with pytest.raises(TimelineEditError):
        narration.validate_speech_boundary(text, [{"word": w} for w in words])


@pytest.mark.parametrize("mutation", [lambda t: t["words"]["words"][1].update(start_s=.1),
    lambda t: t["words"]["words"][1].update(end_s=1.3),
    lambda t: t["words"]["words"][0].update(start_s=True),
    lambda t: t["words"]["words"][0].update(end_s=float("nan")),
    lambda t: t["manifest"].update(duration_seconds=1.25000001),
    lambda t: t["manifest"].update(text_sha256="0" * 64),
    lambda t: t["manifest"].update(settings={})])
def test_structural_range_and_exact_identity_vectors(mutation):
    selected = take()
    mutation(selected)
    with pytest.raises(TimelineEditError):
        narration.validate_take("Hello world!", selected)


def test_same_segment_and_clip_ids_in_distinct_occurrences_are_independent():
    bundle, takes = sample(same_clip_ids=True)
    a, b = list(takes.values())
    result, port = execute(bundle, takes, op(line("occ-A", "vo", a, gap=.7), line("occ-B", "vo", b)))
    assert result["status"] == "accepted", result
    tl = Checkout(result["canonical_document"])
    assert len(tl.lines()) == 2
    assert [v.text for v in tl.lines()] == ["Hello world!", "Second line."]
    assert [w.id for w in tl.lines()[1].words] == ["B-word-0", "B-word-1"]
    projection = port.accepts[0]["narration"]
    assert [(r["occurrence_id"], r["clip_id"]) for r in projection["lines"]] == [("occ-A", "vo"), ("occ-B", "vo")]
    for row in projection["lines"]:
        clip = narration.line_clips(tl)[f"occurrence:{row['occurrence_id']}/clip:vo"]
        assert row["line_digest"] == "sha256:" + narration.digest(clip.data)
        assert clip.data["opaque"]["unicode"] == "é"


@pytest.mark.parametrize("managed,source_in,speed,visible", [
    (True, .5, 2, [("world!", "source-word-1", .0625, .3125)]),
    (True, 0, 1, [("Hello", "source-word-0", 0, .5), ("world!", "source-word-1", .625, 1.125)]),
    (False, .5, 2, [("Hello", "source-word-0", 0, .5), ("world!", "source-word-1", .625, 1.125)]),
], ids=["managed-trim-speed", "managed-unit-speed", "unmanaged-clip-relative"])
def test_source_word_clock_projects_exact_take_per_occurrence(managed, source_in, speed, visible):
    bundle, takes = sample(same_clip_ids=True)
    selected = next(iter(takes.values()))
    rows = [[w["start_s"], w["end_s"], w["word"], f"source-word-{i}"]
            for i, w in enumerate(selected["words"]["words"])]
    for sid in ("A", "B"):
        internal = bundle["shots"][sid]["internal_timeline"]
        voice = next(c for c in internal["clips"] if c["id"] == "vo")
        asset = "shared-exact-take"
        internal["registry"]["assets"][asset] = dict(object_id=selected["speech"]["object_id"],
                                                     type="audio", duration=1.25)
        voice.update(asset=asset, at=0, speed=speed, **{"from": source_in, "to": 1.25})
        intent.set_line(voice, "same", rows)
        intent.set_line_text(voice, selected["manifest"]["text"])
        intent.set_line_take(voice, selected["refs"] if managed else None)
    original, original_takes = copy.deepcopy(bundle), copy.deepcopy(takes)
    tl = Checkout(copy.deepcopy(bundle))
    tl.resolve()
    for sid, placement in (("A", 0), ("B", 4)):
        words = [w for w in tl.words() if w.shot_id == sid]
        assert [(w.text, w.id, w.clip_id) for w in words] == [(text, wid, "vo") for text, wid, _, _ in visible]
        assert [(w.start, w.end) for w in words] == pytest.approx(
            [(placement + start, placement + end) for _, _, start, end in visible])
        voice = narration.line_clips(tl)[f"occurrence:occ-{sid}/clip:vo"]
        assert intent.words(voice.data) == rows
        assert intent.line_take(voice.data) == (selected["refs"] if managed else None)
    # Ordinary word moments consume the same projected timestamps and floor to frames.
    onset = next(start for text, _, start, _ in visible if text == "world!")
    assert tl.time('"world!" #1') == pytest.approx(int(onset * tl.fps) / tl.fps, abs=1e-6)
    assert tl.time('"world!" #2') == pytest.approx(int((4 + onset) * tl.fps) / tl.fps, abs=1e-6)
    assert bundle == original and takes == original_takes


def test_changed_new_and_deleted_lines_are_one_prepared_candidate(monkeypatch):
    bundle, takes = sample()
    fresh = take("Changed exact text.")
    inserted = take("First inserted.")
    takes.update({narration.take_key(t["refs"]): t for t in [fresh, inserted]})
    result, port = execute(bundle, takes, op(line("occ-A", "first", inserted, segment="new", gap=.3),
        line("occ-A", "a-vo", fresh), remove=["occurrence:occ-B/clip:b-vo"]))
    assert result["status"] == "accepted", result
    lines = narration.line_clips(Checkout(result["canonical_document"]))
    assert set(lines) == {"occurrence:occ-A/clip:first", "occurrence:occ-A/clip:a-vo"}
    assert intent.line_take(lines["occurrence:occ-A/clip:a-vo"].data) == fresh["refs"]
    assert lines["occurrence:occ-A/clip:a-vo"].data["opaque"] == {"owner": "A", "unicode": "é"}
    assert len(port.accepts) == 1


def test_partial_validation_failure_never_accepts_or_mutates_base():
    bundle, takes = sample()
    original = copy.deepcopy(bundle)
    a, b = list(takes.values())
    bad = take("Bad mismatch")
    bad["words"]["words"][0]["word"] = "bad"
    takes[narration.take_key(bad["refs"])] = bad
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", a, gap=.8), line("occ-B", "b-vo", bad)))
    assert result["status"] == "refused"
    assert port.accepts == [] and port.saved is None and bundle == original


def test_timing_only_and_rebase_preserve_exact_take_words_and_opaque_fields():
    bundle, takes = sample()
    a = next(iter(takes.values()))
    head = copy.deepcopy(bundle)
    head["shots"]["B"]["internal_timeline"]["clips"][0]["opaque"] = {"head": True}
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", a, gap=.5)), head=head)
    assert result["status"] == "accepted", result
    before = narration.line_clips(Checkout(copy.deepcopy(bundle)))["occurrence:occ-A/clip:a-vo"].data
    after = narration.line_clips(Checkout(result["canonical_document"]))["occurrence:occ-A/clip:a-vo"].data
    assert result["rebased_onto"] == "head-1"
    for key in ("words", "take", "text", "segment"):
        assert before["app"]["astrid"][key] == after["app"]["astrid"][key]
    assert after["opaque"] == before["opaque"]
    assert result["canonical_document"]["shots"]["B"]["internal_timeline"]["clips"][0]["opaque"] == {"head": True}


def test_concurrent_edit_of_line_text_refuses_without_overwrite():
    bundle, takes = sample()
    a = next(iter(takes.values()))
    head = copy.deepcopy(bundle)
    clip = narration.line_clips(Checkout(head))["occurrence:occ-A/clip:a-vo"]
    intent.set_gap_after(clip.data, .9)
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", a, gap=.5)), head=head)
    assert result["status"] == "conflict" and not port.accepts


def test_durable_commit_lost_response_and_identical_replay_precede_take_reads(monkeypatch):
    bundle, takes = sample()
    a = next(iter(takes.values()))
    body = request(op(line("occ-A", "a-vo", a, gap=.5)))
    port = NarrationPort(body, bundle, takes)
    service = CoreService()
    accept = port.accept
    def lose(prepared):
        accept(prepared)
        raise TimeoutError("accepted; response lost")
    port.accept = lose
    with pytest.raises(TimeoutError):
        service.commit(body, port)
    saved = copy.deepcopy(port.saved["result"])
    port.narration_take = lambda *_: pytest.fail("take read before stored replay")
    port.revision = lambda *_: pytest.fail("base read before stored replay")
    assert service.commit(body, port) == saved
    changed = copy.deepcopy(body)
    changed["label"] = "conflicting request"
    assert service.commit(changed, port)["error"]["code"] == "request_id_conflict"


def test_delete_all_emits_explicit_empty_projection():
    bundle, takes = sample()
    result, port = execute(bundle, takes, op(remove=["occurrence:occ-A/clip:a-vo", "occurrence:occ-B/clip:b-vo"]))
    assert result["status"] == "accepted", result
    assert port.accepts[0]["narration"] == {"version": 1, "lines": []}


def test_concurrent_take_replacement_conflicts_even_for_gap_only_intent():
    bundle, takes = sample()
    a = next(iter(takes.values()))
    head = copy.deepcopy(bundle)
    clip = narration.line_clips(Checkout(head))["occurrence:occ-A/clip:a-vo"]
    intent.set_line_take(clip.data, take("Concurrent line.")["refs"])
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", a, gap=.5)), head=head)
    assert result["status"] == "conflict" and not port.accepts
    assert any("take" in c["path"] for c in result["conflicts"])


def test_multi_line_change_fits_music_once(monkeypatch):
    from astrid.sdk.timeline._timing_evaluators import _TimingEvaluators
    bundle, takes = sample()
    a, b = list(takes.values())
    calls = []
    original = _TimingEvaluators._apply_bed_cuts
    def observe(self, records):
        calls.append(copy.deepcopy(records))
        return original(self, records)
    monkeypatch.setattr(_TimingEvaluators, "_apply_bed_cuts", observe)
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", a, gap=.5), line("occ-B", "b-vo", b, gap=.8)))
    assert result["status"] == "accepted", result
    assert len(calls) == 1


def test_undo_and_save_reload_preserve_exact_prior_take_and_words(tmp_path, monkeypatch):
    bundle, takes = sample()
    tl = Checkout(copy.deepcopy(bundle), path=tmp_path / "draft.json")
    tl._narration_takes = takes
    tl.save(quiet=True)
    before = tl.document()
    a = next(iter(takes.values()))
    commands.run(tl, op(line("occ-A", "a-vo", a, gap=.7)))
    # Real serialization/reload, no provider or local managed-output resolver.
    from astrid.sdk.timeline.doc import _serialize
    saved = tmp_path / "disposable.json"
    saved.write_text(_serialize(tl._annotated()))
    loaded = Checkout(json.loads(saved.read_text()))
    old_line = narration.line_clips(Checkout(before))["occurrence:occ-A/clip:a-vo"]
    new_line = narration.line_clips(loaded)["occurrence:occ-A/clip:a-vo"]
    assert intent.words(old_line.data) == intent.words(new_line.data)
    assert intent.line_take(old_line.data) == intent.line_take(new_line.data)
    assert [w.id for w in tl.words()] == [w.id for w in loaded.words()]
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("undo regenerated speech"))
    tl.undo()
    # Existing IDENTITY intentionally retains its high-water reservation on
    # undo. Every prior authored clip/take/text/timing must still be exact.
    restored = tl.document()
    assert restored["shots"] == before["shots"]
    assert restored["placements"] == before["placements"]
    assert restored["parent"]["clips"] == before["parent"]["clips"]


def test_acceptance_failure_preserves_original_head_and_bindings():
    bundle, takes = sample()
    before = copy.deepcopy(bundle)
    a = next(iter(takes.values()))
    body = request(op(line("occ-A", "a-vo", a, gap=.7)))
    port = NarrationPort(body, bundle, takes)
    def refuse(_port, _prepared):
        raise TimelineEditError("injected dependency validation failure")
    port.on_accept = refuse
    result = CoreService().commit(body, port)
    assert result["status"] == "refused"
    assert port.current == "rev-0" and port.saved is None and bundle == before


@pytest.mark.parametrize("change", [{}, {"voice": "another-voice"}, {"rate": "+10%"}, {"text": "Changed words."}])
def test_preparation_selects_new_take_only_for_text_or_resolved_settings(monkeypatch, change):
    bundle, takes = sample()
    tl = Checkout(bundle)
    original = copy.deepcopy(bundle)
    a = next(iter(takes.values()))
    prepared = line("occ-A", "a-vo", a, gap=.9)
    prepared.pop("take")
    prepared.update(change)
    syntheses = []
    def invoke(capability, **kwargs):
        assert capability == "generation.generate_speech"
        assert kwargs["wait"] and kwargs["read_managed_outputs"]
        syntheses.append(kwargs)
        settings = kwargs["inputs"]
        selected = take(settings["text"], voice=settings["voice"], rate=settings["rate"])
        takes[narration.take_key(selected["refs"])] = selected
        return SimpleNamespace(ok=True, outputs={"managed_outputs": [dict(ref, output_port=p) for p, ref in selected["refs"].items()]})
    monkeypatch.setattr("astrid.sdk.invocation.invoke", invoke)
    monkeypatch.setattr(narration, "read_managed_take", lambda _c, _p, refs: copy.deepcopy(takes[narration.take_key(refs)]))
    command, verified = narration.prepare_script(tl, dict(version=1, lines=[prepared], remove=[]), client=object(), preparation_id="exact-request")
    assert len(syntheses) == bool(change)
    assert tl.bundle == original and tl._journal == []
    selected = command["args"]["spec"]["lines"][0]["take"]
    assert (selected != a["refs"]) == bool(change)
    if syntheses:
        assert syntheses[0]["idempotency_context"]["base_revision_id"] == "rev-0"
    assert all(k not in command["args"]["spec"]["lines"][0] for k in narration.DEFAULT_SETTINGS)


def test_partial_preparation_failure_leaves_authored_document_and_journal_unchanged(monkeypatch):
    bundle, takes = sample()
    tl = Checkout(bundle)
    before = tl.document()
    a, b = list(takes.values())
    rows = [line("occ-A", "a-vo", a), line("occ-B", "b-vo", b)]
    for row in rows:
        row.pop("take")
        row["text"] += " Changed."
    settled = []
    def invoke(_capability, **kwargs):
        if settled:
            return SimpleNamespace(ok=False, error={"message": "injected second-line failure"})
        selected = take(kwargs["inputs"]["text"])
        settled.append(selected)
        takes[narration.take_key(selected["refs"])] = selected
        return SimpleNamespace(ok=True, outputs={"managed_outputs": [dict(ref, output_port=p) for p, ref in selected["refs"].items()]})
    monkeypatch.setattr("astrid.sdk.invocation.invoke", invoke)
    monkeypatch.setattr(narration, "read_managed_take", lambda _c, _p, refs: copy.deepcopy(takes[narration.take_key(refs)]))
    with pytest.raises(TimelineEditError, match="second-line failure"):
        narration.apply_managed_script(tl, dict(version=1, lines=rows, remove=[]), client=object(), preparation_id="failure")
    assert tl.document() == before and tl._journal == [] and len(settled) == 1


def test_one_semantic_publication_inverse_restores_prior_takes_text_and_timing(monkeypatch):
    from astrid.sdk.timeline.inverse import inverse_command
    bundle, takes = sample()
    fresh = take("A replacement line.", duration=1.5)
    takes[narration.take_key(fresh["refs"])] = fresh
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", fresh, gap=.6)))
    assert result["status"] == "accepted", result
    after = result["canonical_document"]
    inverse = inverse_command(result["change"]["commands"], bundle, after, "publication-fixture",
                              consequences=result["change"]["consequences"])
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("inverse regenerated speech"))
    undone, plan, direct = RuntimeCommitService._apply(after, [inverse], narration_takes=takes)
    old, restored = narration.line_clips(Checkout(copy.deepcopy(bundle))), narration.line_clips(Checkout(undone))
    for sid in old:
        assert old[sid].data == restored[sid].data


def test_parent_line_projection_has_null_child_pins_and_exact_word_ids():
    bundle, takes = sample()
    a = next(iter(takes.values()))
    result, port = execute(bundle, takes, op(line(None, "parent-voice", a, segment="parent-segment")))
    assert result["status"] == "accepted", result
    first = port.accepts[0]["narration"]["lines"][0]
    assert first["clip_id"] == "parent-voice"
    assert all(first[k] is None for k in ("occurrence_id", "shot_id", "shot_revision_id", "internal_timeline_id", "internal_revision_id"))


def test_no_change_emits_projection_and_preserves_identical_payload():
    bundle, takes = sample()
    a = next(iter(takes.values()))
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", a)))
    assert result["status"] == "no_change", result
    assert port.accepts[0]["publication"] is None
    assert len(port.accepts[0]["narration"]["lines"]) == 2


def test_saved_managed_edit_reload_publish_and_lost_response_retry_use_original_envelope(tmp_path, monkeypatch):
    from test_timeline_saved_publish import RuntimeFixture

    from astrid.sdk.timeline import saved_publish, store
    bundle, takes = sample()
    for shot in bundle["shots"].values():
        shot["internal_timeline"]["fixture_seed"] = True
    runtime = RuntimeFixture(bundle)
    original_port = runtime.port
    def with_narration(body):
        port = original_port(body)
        port.narration_take = lambda refs: copy.deepcopy(takes[narration.take_key(refs)])
        return port
    runtime.port = with_narration
    client = runtime.client()
    base = saved_publish._exact(client, dict(project_id="p", timeline_id="t"), "rev-0")
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.setattr(store, "resolve_ids", lambda *_a, **_k: ("p", "t", "rev-0"))
    monkeypatch.setattr(store, "fetch_bundle", lambda *_a, **_k: copy.deepcopy(base))
    monkeypatch.setattr(narration, "read_managed_take", lambda _c, _p, refs: copy.deepcopy(takes[narration.take_key(refs)]))
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("unexpected regeneration"))
    draft = Checkout.draft("p", "t")
    draft._narration_takes = takes
    a = next(iter(takes.values()))
    commands.run(draft, op(line("occ-A", "a-vo", a, gap=.5)))
    draft = Checkout.load(draft.path)
    runtime.lose = True
    from astrid.sdk.workspace_client import WorkspaceClientError
    with pytest.raises(WorkspaceClientError) as caught:
        draft.publish(client=client, idempotency_key="managed-lost-response")
    assert caught.value.code == "transport_timeout"
    assert len(runtime.publications) == 1
    monkeypatch.setattr(narration, "read_managed_take", lambda *_a: pytest.fail("catalog/managed read before pending replay"))
    result = Checkout.load(draft.path).publish(client=client)
    assert result["status"] == "accepted"
    assert len(runtime.publications) == 1
    assert runtime.calls[0][0] == runtime.calls[1][0]
    loaded = Checkout.load(draft.path)
    assert intent.line_take(narration.line_clips(loaded)["occurrence:occ-A/clip:a-vo"].data) == a["refs"]


def test_established_segments_adapter_preserves_scope_and_makes_deletions_explicit():
    bundle, takes = sample()
    tl = Checkout(bundle)
    with pytest.raises(TimelineEditError, match="requires occurrence_id"):
        narration.script_intents(tl, {"segments": [{"id": "same", "text": "ambiguous"}]})
    spec = narration.script_intents(tl, {"voice": "selected", "segments": [
        {"id": "new", "text": "First inserted.", "occurrence_id": "occ-A"},
        {"id": "same", "text": "Hello world!", "occurrence_id": "occ-A"}]})
    assert spec["remove"] == ["occurrence:occ-B/clip:b-vo"]
    assert spec["lines"][0]["clip_id"] == "voice-new" and spec["voice"] == "selected"


def test_cli_prepare_failure_precedes_saved_edit_audit(tmp_path, monkeypatch):
    from astrid.packs.timeline import cli
    from astrid.sdk.timeline import journal
    bundle, takes = sample()
    tl = Checkout(bundle, path=tmp_path / "draft.json")
    tl.save(quiet=True)
    a = next(iter(takes.values()))
    item = line("occ-A", "a-vo", a)
    item.pop("take")
    item["text"] = "Changed words."
    source = tmp_path / "script.json"
    source.write_text(json.dumps(dict(version=1, lines=[item], remove=[])))
    log = journal.journal_path("p", "t")
    before = tl.path.read_bytes(), log.read_bytes() if log.exists() else None, tl.document()
    monkeypatch.setattr(cli, "_edit_checkout", lambda _parsed: tl)
    monkeypatch.setattr(narration, "read_managed_take", lambda _c, _p, refs: copy.deepcopy(takes[narration.take_key(refs)]))
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: SimpleNamespace(ok=False, error="injected prepare failure"))
    parsed = cli.build_parser(object()).parse_args(["edit", "main", "--project", "p", "--from-script", str(source)])
    assert parsed.handler(parsed) == 2
    assert before == (tl.path.read_bytes(), log.read_bytes() if log.exists() else None, tl.document())


def test_preview_does_not_generate_changed_speech(monkeypatch):
    bundle, takes = sample()
    a = next(iter(takes.values()))
    item = line("occ-A", "a-vo", a)
    item.pop("take")
    item["text"] = "Changed words."
    monkeypatch.setattr(narration, "read_managed_take", lambda _c, _p, refs: copy.deepcopy(takes[narration.take_key(refs)]))
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("preview synthesized speech"))
    with pytest.raises(TimelineEditError, match="before previewing"):
        narration.prepare_script(Checkout(bundle), dict(version=1, lines=[item], remove=[]), client=object(),
                                 preparation_id="preview", allow_generation=False)


def test_managed_multi_line_edit_materializes_the_existing_music_bed_once(monkeypatch):
    from test_timeline_reflow_golden import film

    from astrid.sdk.timeline._timing_evaluators import _TimingEvaluators
    tl = Checkout(film())
    prepared, takes = [], {}
    for voice in tl.lines():
        selected = take(voice.text, duration=2)
        takes[narration.take_key(selected["refs"])] = selected
        prepared.append(line("occ-F", voice.clips[0].id, selected, segment=voice.segment, gap=.5))
    tl._narration_takes = takes
    materializations = []
    original = _TimingEvaluators._apply_bed_cuts
    def observe(self, records):
        materializations.append(len(records))
        return original(self, records)
    monkeypatch.setattr(_TimingEvaluators, "_apply_bed_cuts", observe)
    plan = commands.run(tl, op(*prepared))
    assert plan.changed and len(plan.calls) == 1 and len(materializations) == 1
    assert materializations[0] > 0
    music = [c for c in tl.clips() if c.track == "music"]
    assert music and max(c.end for c in music) == pytest.approx(tl.duration, abs=1 / tl.fps)


def test_voice_change_preserves_ids_of_exactly_matching_words():
    bundle, takes = sample()
    fresh = take(voice="new-voice", duration=2)
    takes[narration.take_key(fresh["refs"])] = fresh
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", fresh)))
    assert result["status"] == "accepted", result
    clip = narration.line_clips(Checkout(result["canonical_document"]))["occurrence:occ-A/clip:a-vo"]
    assert intent.line_take(clip.data) == fresh["refs"]
    assert [r[3] for r in intent.words(clip.data)] == ["A-word-0", "A-word-1"]


def test_legacy_narration_descriptor_retires_in_same_candidate_and_other_kinds_survive(monkeypatch):
    bundle, takes = sample()
    pins = [dict(kind="voiceover_script", content_hash="sha256:" + "1" * 64, head=1, text="old"),
            dict(kind="notes", content_hash="sha256:" + "2" * 64, head=2, text="keep")]
    bundle["shots"]["A"]["payload"]["text_bindings"] = copy.deepcopy(pins)
    before = copy.deepcopy(bundle)
    monkeypatch.setattr(Checkout, "pin_narration", lambda *_a, **_k: pytest.fail("separate binding mutation"))
    a = next(iter(takes.values()))
    result, port = execute(bundle, takes, op(line("occ-A", "a-vo", a, gap=.8)))
    assert result["status"] == "accepted", result
    assert result["canonical_document"]["shots"]["A"]["payload"]["text_bindings"] == pins[1:]
    assert bundle == before
