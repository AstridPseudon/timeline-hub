"""Executable design spike; product registry and default compiler stay untouched."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline import commands
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.compiler import TimingCompileError, TimingInputs, compile_timing
from tests.editing_conformance import test_timing_retained_inputs as retained_inputs
from tests.editing_conformance.word_binding_recipe import OP, binding, fold, install

pytestmark = pytest.mark.integration
retained = retained_inputs.retained
TARGET = retained_inputs.TARGET
REF = "parent/clip:card"
KEY = (REF, "on")


@pytest.fixture
def recipe(retained, monkeypatch):
    install(monkeypatch)
    retained.submit(retained.create("recipe-initial"), "recipe-initial")
    return retained


def bundle(case):
    result = bundle_from_document(case.documents[case.head()["revision_id"]])
    # This is the same authorized capture observed from the real provider,
    # handed to the frontend picker, not an inline command/source authority.
    result["source_mapping"]["pinned_documents"] = copy.deepcopy(
        case.hydrated[-1]["source_mapping"]["pinned_documents"])
    return result


def pick(case, index=0, *, text='"again"', source="voice", count=1):
    original = bundle(case)
    words = original["source_mapping"]["pinned_documents"][0]["document"]["content"]["segments"][0]["words"]
    call = {"schema_version": 1, "op": OP, "version": "1", "select": REF,
            "args": {"field": "on", "declaration": text, "choice": {
                "source": "occurrence:occ/clip:" + source, "document": case.pin,
                "word_ids": [word["id"] for word in words[index:index + count]]}},
            "intent": {"anchor": "follow"}}
    return commands.execute(original, [call]).commands[0]


def history(case):
    # Runtime verifies accepted receipt/record correspondence and scopes each
    # entry; fold also checks complete publication adjacency, including ABA.
    page = case.service.list_timeline_commits(case.project, "film", limit=200, authorize=lambda: None)
    assert page["next_cursor"] is None
    assert page["head"] == case.head()
    return json.loads(json.dumps(page["items"]))


def projected(case, entries=None):
    current = bundle(case)
    state = fold(history(case) if entries is None else entries)
    bindings = [binding(current, target, args) for (target, _), args in state.items() if args is not None]
    return compile_timing(TimingInputs(current,
        sources=current["source_mapping"]["pinned_documents"], bindings=bindings))


def undo(case, accepted, key):
    return case.submit(case.request([{"schema_version": 1, "op": "timeline.inverse", "version": "1",
        "select": None, "args": {"publications": [accepted["receipt"]["receipt_id"]]}}]), key)


def restore(case, accepted, key):
    parent = accepted["data"]["canonical_document"]["parent_revision"]
    return case.submit(case.request([{"schema_version": 1, "op": "timeline.restore", "version": "1",
        "select": None, "args": {name: parent[name] for name in ("revision_id", "content_digest")}}]), key)


@pytest.mark.parametrize("same_text", [False, True])
@pytest.mark.parametrize("retained", [True], indirect=True)
def test_undo_recovers_before_binding_even_when_text_writes_are_equal(recipe, same_text):
    case = recipe
    a = pick(case)
    accepted_a = case.submit(case.request([a]), "anchor-a")
    expected = projected(case).timings[TARGET]
    b = pick(case, 1, text='"again"' if same_text else '"again" +1f')
    accepted_b = case.submit(case.request([b]), "anchor-b")
    assert projected(case).timings[TARGET] != expected
    record_b = history(case)[-1]["records"]["commands"][0]
    if same_text:
        write = record_b["writes"][-1]
        assert write["before"] == write["after"]
        assert accepted_a["data"]["canonical_document"] == accepted_b["data"]["canonical_document"]
    # This publication changes derived timing and source order, without writing
    # the target's declaration. Undo B must recover A's choice at the new time.
    moved = capture_move(bundle(case), "occurrence:occ/clip:voice", 8)
    case.submit(case.request([moved]), "move-source-before-undo")
    inverse_b = undo(case, accepted_b, "undo-b")
    case.restart()
    assert fold(history(case))[KEY] == a["args"]
    assert projected(case).timings[TARGET]["start"] > expected["start"]
    undo(case, inverse_b, "redo-b")
    assert fold(history(case))[KEY] == b["args"]


@pytest.mark.parametrize("retained", [True], indirect=True)
def test_follow_rebases_original_choice_after_source_move_and_reorder(recipe):
    case = recipe
    captured = pick(case, 1, text='"again" in line #2 +1f')
    base = case.head()
    original = bundle(case)
    assert retained_inputs.first_selection(original).source[-1] == "voice"
    moved = capture_move(original, "occurrence:occ/clip:voice", 8)
    case.submit(case.request([moved]), "move-source")
    # Ordinal reselection now points at the other raw clip of the SAME CAS and
    # exact stable word. The command must retain the originally clicked clip.
    assert retained_inputs.first_selection(bundle(case)).source[-1] == "other"
    accepted = case.submit(case.request([captured], base), "stale-anchor")
    assert accepted["data"]["status"] == "rebased"
    assert fold(history(case))[KEY] == captured["args"]
    expected = projected(case).timings[TARGET]
    assert expected["start"] > 8
    case.restart()
    assert projected(case).timings[TARGET] == expected
    # A subsequent accepted source move also follows without a direct timing
    # read guard on the declaration's source start/window/order.
    moved = capture_move(bundle(case), "occurrence:occ/clip:voice", 5)
    case.submit(case.request([moved]), "move-again")
    assert projected(case).timings[TARGET]["start"] < expected["start"]
    record = next(row for row in history(case) if row["publication_id"] == accepted["receipt"]["receipt_id"])
    reads = record["records"]["commands"][0]["reads"]
    assert not any(read["ref"].endswith("/clip:voice") and read["path"] == ["at"] for read in reads)


def test_phrase_records_all_consecutive_main_word_ids(recipe):
    case = recipe
    command = pick(case, text='"again again"', count=2)
    case.submit(case.request([command]), "phrase")
    assert len(fold(history(case))[KEY]["choice"]["word_ids"]) == 2
    assert projected(case).timings[TARGET]["start_frame"] == 89
    invalid = copy.deepcopy(command)
    invalid["args"]["choice"]["word_ids"].reverse()
    with pytest.raises(TimingCompileError, match="consecutive"):
        commands.execute(bundle(case), [{key: invalid[key] for key in
            ("schema_version", "op", "version", "select", "args", "intent")}])


@pytest.mark.parametrize("retained", [True], indirect=True)
def test_same_word_in_reused_cas_clips_retains_raw_source_through_undo(recipe):
    case = recipe
    a = pick(case, 1)
    case.submit(case.request([a]), "voice-word")
    b = pick(case, 1, source="other")
    assert a["args"]["choice"]["document"] == b["args"]["choice"]["document"]
    assert a["args"]["choice"]["word_ids"] == b["args"]["choice"]["word_ids"]
    accepted_b = case.submit(case.request([b]), "other-word")
    assert fold(history(case))[KEY]["choice"]["source"] == "occurrence:occ/clip:other"
    undo(case, accepted_b, "undo-other")
    case.restart()
    assert fold(history(case))[KEY] == a["args"]


def test_last_write_clear_undo_restore_and_restore_inverse(recipe):
    case = recipe
    a = pick(case)
    accepted_a = case.submit(case.request([a]), "a")
    b = pick(case, 1, text='"again" +1f')
    case.submit(case.request([b]), "b")
    assert fold(history(case))[KEY] == b["args"]
    clear = {"schema_version": 1, "op": OP, "version": "1", "select": REF,
             "args": {"field": "on", "declaration": None, "choice": None}}
    cleared = case.submit(case.request([clear]), "clear")
    assert fold(history(case))[KEY] is None
    assert projected(case).bundle["parent"]["clips"][0]["app"]["astrid"].get("on") is None
    undo(case, cleared, "undo-clear")
    assert fold(history(case))[KEY] == b["args"]
    restored = restore(case, accepted_a, "restore-a")
    assert fold(history(case))[KEY] == a["args"]
    case.restart()
    undo(case, restored, "undo-restore")
    assert fold(history(case))[KEY] == b["args"]


def test_equal_text_revision_only_restore_is_an_executable_counterexample(recipe):
    case = recipe
    a = case.submit(case.request([pick(case)]), "a")
    b = case.submit(case.request([pick(case, 1)]), "b")
    assert a["data"]["canonical_document"] == b["data"]["canonical_document"]
    assert a["receipt"]["receipt_id"] != b["receipt"]["receipt_id"]
    restore(case, a, "restore-a")
    # Both A and B have this revision/digest. Current RestoreArgs cannot say
    # which binding provenance the user selected; guessing would retarget.
    with pytest.raises(CommandError, match="ambiguous binding provenance"):
        fold(history(case))


@pytest.mark.xfail(strict=True, reason="Restore needs reviewed exact publication provenance in existing general reads")
def test_equal_text_restore_recovers_the_selected_publications_binding(recipe):
    case = recipe
    command_a = pick(case)
    a = case.submit(case.request([command_a]), "a")
    case.submit(case.request([pick(case, 1)]), "b")
    restore(case, a, "restore-a")
    assert fold(history(case))[KEY] == command_a["args"]


@pytest.mark.parametrize("damage", ["missing", "foreign", "revoked", "invented", "missing-word"])
def test_invalid_inputs_fail_closed_before_acceptance(recipe, damage):
    case = recipe
    call = pick(case)
    current = case.head()
    if damage in ("invented", "missing-word"):
        if damage == "invented":
            call["bindings"]["anchor.source"] = "occurrence:occ/clip:other"
        else:
            call["args"]["choice"]["word_ids"] = ["word:" + "0" * 64]
        from runtime_protocol.errors import RuntimeErrorBase
        with pytest.raises((RuntimeErrorBase, TimingCompileError)):
            case.submit(case.request([call]), damage)
    else:
        candidate = bundle(case)
        sources = candidate["source_mapping"]["pinned_documents"]
        if damage in ("missing", "revoked"):
            sources.clear()
        else:
            sources[0]["document"]["project_id"] = "foreign-project"
        # Source authority is enforced by the real Runtime port in the retained
        # input neighbor tests. The pure recipe receives only allowed captures.
        with pytest.raises(TimingCompileError, match="missing or revoked|scoped pin"):
            commands.execute(candidate, [call])
    assert case.head() == current


def test_incomplete_history_and_changed_capture_refuse(recipe):
    case = recipe
    case.submit(case.request([pick(case)]), "a")
    entries = history(case)
    with pytest.raises(CommandError, match="ancestry"):
        fold(entries[1:])
    entries[-1]["records"]["commands"][0]["dependencies"] = []
    with pytest.raises(CommandError, match="incomplete accepted binding"):
        fold(entries)
