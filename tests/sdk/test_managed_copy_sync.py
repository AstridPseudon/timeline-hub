"""COPY-SYNC through the existing exact managed-take command/compiler route."""
import copy

import pytest
from test_timeline_narration_reflow import line, op, sample
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


def copy_film():
    bundle, takes = sample()
    document = bundle["shots"]["A"]["internal_timeline"]
    document["clips"].append(dict(id="quote", clipType="am-type", track="overlay", at=.1,
        hold=.8, params=dict(text="Hello world!"), app=dict(foreign=dict(opaque=[1, "é"]))))
    document["tracks"].append(dict(id="overlay", kind="visual"))
    return bundle, takes


def test_managed_reflow_exposes_pinned_copy_source_without_legacy_binding():
    bundle, takes = copy_film()
    tl = Checkout(copy.deepcopy(bundle))
    tl._narration_takes = takes
    selected = next(iter(takes.values()))
    commands.run(tl, op(line("occ-A", "a-vo", selected, gap=.7)))
    assert tl.bundle["shots"]["A"]["payload"]["text_bindings"] == []
    row = next(r for r in tl.copy_inventory()["rows"] if r["layer"] == "occurrence:occ-A/clip:quote")
    assert row["status"] == "unique", row
    source = row["matches"][0]["source"]
    assert source["take"] == selected["refs"]
    assert source["words"] == [{"id": "A-word-0", "text": "Hello"}, {"id": "A-word-1", "text": "world!"}]


def declaration(tl, cid="quote", *, text_range=None, candidate=0):
    from astrid.core.timeline import copy_sync as core
    from astrid.sdk.timeline import copy_sync as api
    row = next(r for r in tl.copy_inventory()["rows"] if r["layer"].endswith("/clip:" + cid))
    display = dict(path=row["path"], text=row["text"])
    if text_range is not None:
        display["range"] = text_range
        source_line = next(s for s in api.source_context(tl.bundle)["lines"] if s["clip"] == "occurrence:occ-A/clip:a-vo")
        source = api._source_at(source_line, core.runs(core.selected_display(display), source_line)[candidate])
    else:
        source = row["matches"][candidate]["source"]
    return dict(version=1, normalization=core.NORMALIZATION, display=display, source=source)


def declared_film():
    from astrid.sdk import timeline_intent as intent
    bundle, takes = copy_film()
    document = bundle["shots"]["A"]["internal_timeline"]
    for cid, text, at in [("second-quote", "Hello world!", 3), ("clean-quote", "Second line.", 2), ("heading", "PART 02", .1)]:
        target = bundle["shots"]["B"]["internal_timeline"] if cid == "clean-quote" else document
        if cid == "clean-quote":
            target["tracks"].append(dict(id="overlay", kind="visual"))
        target["clips"].append(dict(id=cid, clipType="am-type", track="overlay", at=at,
            hold=.8, params=dict(text=text), app=dict(foreign=dict(opaque=[cid, "é"]))))
    tl = Checkout(bundle)
    tl._narration_takes = takes
    quotes = {}
    for cid in ("quote", "second-quote", "clean-quote"):
        q = declaration(tl, cid)
        quotes[cid] = [q]
        if cid == "quote":
            quotes[cid].append(declaration(tl, text_range=[0, 5]))
        tl.clip(cid).declare_quotes(quotes[cid])
    assert intent.copy_quotes(tl.clip("quote").data) == quotes["quote"]
    return tl, takes, quotes


def test_managed_script_reports_every_affected_layer_and_preserves_quote_provenance():
    from test_timeline_narration_reflow import take

    from astrid.sdk import timeline_intent as intent
    tl, takes, quotes = declared_film()
    original = tl.document()
    fresh = take("Goodbye world!")
    from astrid.sdk.timeline import narration
    takes[narration.take_key(fresh["refs"])] = fresh
    commands.run(tl, op(line("occ-A", "a-vo", fresh)))
    affected = [f["layer"] for f in tl.copy_lint() if any(r["code"] == "COPY_STALE" for r in f["reasons"])]
    assert affected == ["occurrence:occ-A/clip:quote", "occurrence:occ-A/clip:second-quote"]
    for cid, expected in quotes.items():
        assert intent.copy_quotes(tl.clip(cid).data) == expected
    for cid in ("clean-quote", "heading"):
        prior = next(c for shot in original["shots"].values() for c in shot["internal_timeline"]["clips"] if c["id"] == cid)
        assert tl.clip(cid).data == prior
    for cid in ("quote", "second-quote"):
        assert sum(s.startswith("occurrence:occ-A/clip:" + cid + ":") for s in tl.report) == 1
        expected = {"opaque": [1, "é"]} if cid == "quote" else {"opaque": [cid, "é"]}
        assert tl.clip(cid).data["app"]["foreign"] == expected


def test_persist_reload_inverse_redo_and_same_request_replay_keep_accepted_provenance(tmp_path, monkeypatch):
    import json

    from test_timeline_commit import CoreService, request
    from test_timeline_narration_reflow import NarrationPort, take

    from astrid.sdk import timeline_intent as intent
    from astrid.sdk.timeline import narration
    from astrid.sdk.timeline.commit import RuntimeCommitService
    from astrid.sdk.timeline.inverse import inverse_command

    tl, takes, quotes = declared_film()
    tl.save(tmp_path / "draft.json", quiet=True)
    before = tl.document()
    fresh = take("Goodbye world!")
    takes[narration.take_key(fresh["refs"])] = fresh
    operation = op(line("occ-A", "a-vo", fresh))
    commands.run(tl, operation)
    tl.save(quiet=True)
    loaded = Checkout.load(tl.path)
    assert loaded.copy_lint() == tl.copy_lint()
    for cid, expected in quotes.items():
        assert intent.copy_quotes(loaded.clip(cid).data) == expected
        assert intent.copy_quote_tracking(loaded.clip(cid).data) == intent.copy_quote_tracking(tl.clip(cid).data)
    accepted = tl.document()
    loaded.undo()
    assert loaded.document()["shots"] == before["shots"]
    loaded.redo()
    assert loaded.document()["shots"] == accepted["shots"]

    body = request(operation)
    port = NarrationPort(body, before, takes)
    service = CoreService()
    result = service.commit(body, port)
    assert result["status"] == "accepted", result.get("error", result)
    canonical = json.loads(json.dumps(result["canonical_document"]))
    assert Checkout(canonical).copy_lint() == loaded.copy_lint()
    inverse = inverse_command(result["change"]["commands"], before, canonical, "publication-fixture",
                              consequences=result["change"]["consequences"])
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("inverse regenerated speech"))
    undone, _, _ = RuntimeCommitService._apply(canonical, [inverse], narration_takes=takes)
    assert undone["shots"] == before["shots"]
    redone, _, _ = RuntimeCommitService._apply(undone, [operation], narration_takes=takes)
    assert redone["shots"] == canonical["shots"]
    port.narration_take = lambda *_: pytest.fail("take read before stored replay")
    port.revision = lambda *_: pytest.fail("base read before stored replay")
    assert service.commit(body, port) == result
    assert len(port.accepts) == 1


@pytest.mark.parametrize("text", ["Hello world! Hello world!", "Hello Hello world!"])
def test_ambiguous_managed_correspondence_refuses_document_revision_and_history_atomically(text):
    from test_timeline_narration_reflow import execute, take

    from astrid.sdk.timeline import narration
    from astrid.sdk.timeline._common import TimelineEditError

    tl, takes, _ = declared_film()
    original = tl.document(), copy.deepcopy(tl._journal), copy.deepcopy(tl._pending_calls)
    fresh = take(text)
    takes[narration.take_key(fresh["refs"])] = fresh
    operation = op(line("occ-A", "a-vo", fresh))
    with pytest.raises(TimelineEditError, match="ambiguous source correspondence"):
        commands.run(tl, operation)
    assert (tl.document(), tl._journal, tl._pending_calls) == original
    result, port = execute(tl.document(), takes, operation)
    assert result["status"] == "refused", result
    assert port.current == "rev-0" and port.saved is None and port.accepts == []


@pytest.mark.parametrize("text,expected", [("Today Hello world!", set()), ("HELLO WORLD!", {"COPY_RAW_CHANGE"}),
    ("Hello", {"COPY_STALE", "COPY_SYNC"}), ("Hello strange world!", {"COPY_STALE", "COPY_SYNC"})])
def test_managed_correspondence_insert_delete_normalization_and_broken_contiguity(text, expected):
    from test_timeline_narration_reflow import take

    from astrid.sdk import timeline_intent as intent
    from astrid.sdk.timeline import narration

    tl, takes, quotes = declared_film()
    fresh = take(text)
    takes[narration.take_key(fresh["refs"])] = fresh
    commands.run(tl, op(line("occ-A", "a-vo", fresh)))
    reasons = {r["code"] for f in tl.copy_lint() for r in f["reasons"] if f["layer"] == "occurrence:occ-A/clip:quote"}
    assert reasons == expected
    assert intent.copy_quotes(tl.clip("quote").data) == quotes["quote"]
    if text.startswith("Today"):
        state = next(iter(intent.copy_quote_tracking(tl.clip("quote").data).values()))
        assert state["source"]["take"] == fresh["refs"]
        assert state["source"]["words"] == quotes["quote"][0]["source"]["words"]


def test_managed_deleted_quote_never_resurrects_after_save_reload(tmp_path):
    from test_timeline_narration_reflow import take

    from astrid.sdk import timeline_intent as intent
    from astrid.sdk.timeline import narration

    tl, takes, quotes = declared_film()
    fresh = take("Gone.")
    takes[narration.take_key(fresh["refs"])] = fresh
    commands.run(tl, op(line("occ-A", "a-vo", fresh)))
    tl.save(tmp_path / "deleted.json", quiet=True)
    loaded = Checkout.load(tl.path)
    loaded._narration_takes = takes
    original = next(iter(takes.values()))
    commands.run(loaded, op(line("occ-A", "a-vo", original)))
    assert "COPY_STALE" in {r["code"] for f in loaded.copy_lint() for r in f["reasons"]}
    assert intent.copy_quotes(loaded.clip("quote").data) == quotes["quote"]


def test_managed_inventory_uses_f_word_identity_and_trim_speed_clock():
    from astrid.sdk import timeline_intent as intent
    from astrid.sdk.timeline import copy_sync as api

    bundle, _ = copy_film()
    voice = next(c for c in bundle["shots"]["A"]["internal_timeline"]["clips"] if intent.line(c))
    voice.update(at=0, speed=2, **{"from": .5, "to": 1.25})
    tl = Checkout(bundle)
    source = next(s for s in api.source_context(bundle)["lines"] if s["clip"] == "occurrence:occ-A/clip:a-vo")
    assert [(w["id"], w["text"], w["start"], w["end"]) for w in source["words"]] == [("A-word-1", "world!", .0625, .3125)]
    word = next(w for w in tl.words() if w.shot_id == "A")
    assert (word.id, word.start, word.end) == ("A-word-1", .0625, .3125)
    assert source["interval"] == [.0625, .3125]


def test_timing_only_noop_and_readonly_inventory_do_not_refresh_provenance():
    from astrid.sdk.timeline import narration
    tl, takes, _ = declared_film()
    original = tl.document(), copy.deepcopy(tl._journal)
    inventory = tl.copy_inventory()
    assert any(r["text"] == "PART 02" and r["status"] == "unmatched" for r in inventory["rows"])
    assert not any(r["code"] == "COPY_STALE" for f in tl.copy_lint() for r in f["reasons"])
    assert not any(f["layer"].endswith("heading") for f in tl.copy_lint())
    assert (tl.document(), tl._journal) == original
    selected = next(iter(takes.values()))
    plan = commands.run(tl, op(line("occ-A", "a-vo", selected)))
    assert not plan.changed
    assert tl.document()["shots"] == original[0]["shots"]
    assert "COPY_STALE" not in " ".join(tl.report)
    # Different immutable timing artifact, exact same spoken tokens.
    from test_timeline_narration_reflow import take
    fresh = take(duration=1.5)
    takes[narration.take_key(fresh["refs"])] = fresh
    commands.run(tl, op(line("occ-A", "a-vo", fresh)))
    assert not any(r["code"] == "COPY_STALE" for f in tl.copy_lint() for r in f["reasons"])


@pytest.mark.parametrize("mutation", ["missing-take", "wrong-media", "pending-text", "malformed-take"])
def test_missing_or_mismatched_managed_source_is_unavailable_and_reads_do_not_mutate(mutation):
    import json

    from astrid.sdk import timeline_intent as intent
    tl, _, _ = declared_film()
    voice = tl.clip("a-vo")
    if mutation == "missing-take":
        intent.set_line_take(voice.data, None)
    elif mutation == "pending-text":
        intent.set_line_text(voice.data, "unprepared words")
    elif mutation == "malformed-take":
        intent.set_line_take(voice.data, {"speech": {}})
    else:
        tl._registry("A")[voice.data["asset"]]["object_id"] = "sha256:" + "0" * 64
    before = json.dumps(tl.document(), sort_keys=True)
    row = next(r for r in tl.copy_inventory()["rows"] if r["layer"].endswith("/clip:quote"))
    assert row["status"] == "unavailable"
    findings = tl.copy_lint()
    assert any(r["code"] == "COPY_SOURCE_UNAVAILABLE" for f in findings for r in f["reasons"])
    assert json.dumps(tl.document(), sort_keys=True) == before


def test_repeated_managed_placements_keep_all_scoped_candidates_visible():
    tl = Checkout(copy_film()[0])
    other = copy.deepcopy(tl.bundle["placements"][0])
    other.update(occurrence_id="occ-A-again", placement=dict(start_ms=8000))
    tl.bundle["placements"].append(other)
    row = next(r for r in tl.copy_inventory()["rows"] if r["layer"] == "occurrence:occ-A/clip:quote")
    assert row["status"] == "ambiguous"
    assert [m["source"]["occurrence_id"] for m in row["matches"]] == ["occ-A", "occ-A-again"]
    assert [m["source"]["words"][0]["id"] for m in row["matches"]] == ["A-word-0", "A-word-0"]


def test_cli_managed_script_preserves_quotes_and_reports_affected_layers(tmp_path, monkeypatch, capsys):
    import json

    from test_timeline_narration_reflow import take

    from astrid.packs.timeline import cli
    from astrid.sdk import timeline_intent as intent
    from astrid.sdk.timeline import narration
    tl, takes, quotes = declared_film()
    tl.save(tmp_path / "cli-draft.json", quiet=True)
    original = tl.document()
    fresh = take("Goodbye world!")
    takes[narration.take_key(fresh["refs"])] = fresh
    script = dict(version=1, lines=[line("occ-A", "a-vo", fresh)], remove=[])
    source = tmp_path / "script.json"
    source.write_text(json.dumps(script))
    monkeypatch.setattr(narration, "read_managed_take", lambda _c, _p, refs: copy.deepcopy(takes[narration.take_key(refs)]))
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("prepared take regenerated"))
    # The supported --file path saves this task-owned document and avoids a
    # live draft selection or any mounted Runtime/scene assertion.
    parsed = cli.build_parser(object()).parse_args(["edit", "main", "--project", "p", "--file", str(tl.path), "--from-script", str(source)])
    assert parsed.handler(parsed) == 0
    output = capsys.readouterr().out
    assert "occurrence:occ-A/clip:quote: COPY_STALE" in output
    assert "occurrence:occ-A/clip:second-quote: COPY_STALE" in output
    loaded = Checkout.load(tl.path)
    assert intent.copy_quotes(loaded.clip("quote").data) == quotes["quote"]
    assert tl.document() == original  # --file edits its own loaded checkout
    assert {f["layer"] for f in loaded.copy_lint() if any(r["code"] == "COPY_STALE" for r in f["reasons"])} == {
        "occurrence:occ-A/clip:quote", "occurrence:occ-A/clip:second-quote"}
    assert not any(f["layer"].endswith("clean-quote") for f in loaded.copy_lint())


def test_untracked_take_swap_cannot_inherit_identity_from_equal_words():
    from test_timeline_narration_reflow import take

    from astrid.sdk import timeline_intent as intent
    tl, _, _ = declared_film()
    # An out-of-band snapshot is readable, but lacks the command's old/new
    # correspondence evidence. Equal text/IDs alone do not identify a retake.
    fresh = take(voice="another-voice")
    for shot in tl.bundle["shots"].values():
        shot.pop("base_internal_timeline", None)
    clip = tl.clip("a-vo")
    asset = "speech-" + fresh["speech"]["object_id"][7:]
    tl._registry("A")[asset] = dict(object_id=fresh["speech"]["object_id"], type="audio", duration=1.25)
    clip.data["asset"] = asset
    intent.set_line_take(clip.data, fresh["refs"])
    assert any(r["code"] == "COPY_STALE" and "correspondence chain" in r["reason"]
               for f in tl.copy_lint() for r in f["reasons"])


def test_parent_managed_source_declares_through_the_existing_command():
    from astrid.sdk import timeline_intent as intent
    tl = Checkout(copy_film()[0])
    _, takes = copy_film()
    tl._narration_takes = takes
    selected = next(iter(takes.values()))
    commands.run(tl, op(line(None, "parent-voice", selected, segment="parent-line")))
    tl.bundle["parent"].setdefault("tracks", []).append(dict(id="parent-copy", kind="visual"))
    tl.bundle["parent"].setdefault("clips", []).append(dict(id="parent-quote", clipType="am-type",
        track="parent-copy", at=.1, hold=.8, params=dict(text="Hello world!")))
    row = next(r for r in tl.copy_inventory()["rows"] if r["layer"] == "parent/clip:parent-quote")
    candidate = next(m for m in row["matches"] if m["source"]["clip"] == "parent/clip:parent-voice")
    q = dict(version=1, normalization="copy-token-v1", display=dict(path=row["path"], text=row["text"]), source=candidate["source"])
    assert q["source"]["occurrence_id"] is None
    tl.clip("parent-quote").declare_quotes([q])
    assert intent.copy_quotes(tl.clip("parent-quote").data) == [q]


def test_colliding_word_ids_from_managed_insert_refuse_atomically():
    from test_timeline_narration_reflow import take

    from astrid.sdk import timeline_intent as intent
    from astrid.sdk.timeline import narration
    from astrid.sdk.timeline._common import TimelineEditError
    bundle, takes = copy_film()
    voice = next(c for c in bundle["shots"]["A"]["internal_timeline"]["clips"] if intent.line(c))
    rows = intent.words(voice)
    for i, word in enumerate(rows):
        word[3] = f"same:{i}"
    intent.set_line(voice, "same", rows)
    tl = Checkout(bundle)
    tl._narration_takes = takes
    tl.clip("quote").declare_quotes([declaration(tl)])
    fresh = take("Today Hello world!")
    takes[narration.take_key(fresh["refs"])] = fresh
    original = tl.document(), copy.deepcopy(tl._journal)
    # Existing narration retains explicit equal-run IDs; its unlabelled inserted
    # row's fallback may collide. Never silently identify either occurrence.
    with pytest.raises(TimelineEditError, match="ambiguous source correspondence"):
        commands.run(tl, op(line("occ-A", "a-vo", fresh)))
    assert (tl.document(), tl._journal) == original


def test_saved_quote_publish_lost_response_reload_replays_exact_normal_envelope(tmp_path, monkeypatch):
    import json

    from test_timeline_narration_reflow import take
    from test_timeline_saved_publish import RuntimeFixture

    from astrid.sdk import timeline_intent as intent
    from astrid.sdk.timeline import narration, saved_publish, store
    from astrid.sdk.workspace_client import WorkspaceClientError

    tl, takes, quotes = declared_film()
    bundle = tl.document()
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
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("speech regenerated"))
    draft = Checkout.draft("p", "t")
    draft._narration_takes = takes
    fresh = take("Goodbye world!")
    takes[narration.take_key(fresh["refs"])] = fresh
    commands.run(draft, op(line("occ-A", "a-vo", fresh)))
    draft = Checkout.load(draft.path)
    runtime.lose = True
    with pytest.raises(WorkspaceClientError) as caught:
        draft.publish(client=client, idempotency_key="quote-lost-response")
    assert caught.value.code == "transport_timeout" and len(runtime.publications) == 1
    monkeypatch.setattr(narration, "read_managed_take", lambda *_a: pytest.fail("take read before pending replay"))
    result = Checkout.load(draft.path).publish(client=client)
    assert result["status"] == "accepted", result
    assert len(runtime.publications) == 1 and len(runtime.commits) == 2
    assert runtime.commits[0][0] == runtime.commits[1][0]
    assert [json.loads(c[0])["dry_run"] for c in runtime.calls] == [True, False, False]
    loaded = Checkout.load(draft.path)
    for cid, q in quotes.items():
        assert intent.copy_quotes(loaded.clip(cid).data) == q
    assert {f["layer"] for f in loaded.copy_lint() if any(r["code"] == "COPY_STALE" for r in f["reasons"])} == {
        "occurrence:occ-A/clip:quote", "occurrence:occ-A/clip:second-quote"}
