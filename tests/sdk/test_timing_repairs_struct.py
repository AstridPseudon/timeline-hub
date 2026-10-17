"""REPAIRS-STRUCT: disposable current-source scenarios, not named-film proof."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline.compiler import TimingCycleError, TimingInputs, compile_timing
from astrid.sdk.timeline_checkout import Checkout, TimelineEditError

TINY = Path(__file__).resolve().parents[1] / "fixtures/timeline_editing/tiny.json"


def tiny():
    return Checkout(json.loads(TINY.read_text()))


def beat_film():
    tl = tiny()
    bed = tl.clip("a-music")
    bed.data["to"] = 8.0
    intent.set_beats(bed.data, {"beats": [i * .5 for i in range(20)]})
    return tl


def ambiguous():
    tl = tiny()
    voice = tl.clip("a-vo")
    intent._app_w(voice.data)["words"] = [
        [.1, .4, "It"], [.5, .8, "went"], [1.3, 1.9, "viral"], [2.1, 2.4, "viral"]
    ]
    return tl


def assert_refused_unchanged(tl, action):
    before = copy.deepcopy(tl.__dict__)
    bundle, clip_data = tl.bundle, [c.data for c in tl.clips()]
    with pytest.raises(TimelineEditError) as error:
        action()
    assert error.value.code == "AMBIGUOUS_REFERENCE"
    text = str(error.value)
    assert '"viral"' in text and "Say which" in text and "#n" in text
    assert "s1" in text and "1.80" in text and "2.60" in text
    assert tl.__dict__ == before and tl.bundle is bundle
    assert all(a is b.data for a, b in zip(clip_data, tl.clips()))
    return text


def test_music_film_feedback_reports_complete_path_without_adoption():
    tl = beat_film()
    intent.set_until(tl.clip("a-music").data, "end of c2")
    intent.set_until(tl.cut_picture("c2").data, 'beat 2 after "now"')
    before = copy.deepcopy(tl.__dict__)
    with pytest.raises(TimingCycleError) as error:
        tl.resolve()
    assert error.value.path == ("a-music.end", "c2.end", "film.pictureEnd",
                                "c2.plate.end", "a-music.end")
    assert str(error.value) == "CYCLE: " + " -> ".join(error.value.path)
    assert tl.__dict__ == before


@pytest.mark.parametrize("on", ["end", "end of c2", "c2.end"])
def test_terminal_start_self_feedback_is_refused(on):
    tl = tiny()
    intent.set_on(tl.cut_picture("c2").data, on)
    before = copy.deepcopy(tl.bundle)
    with pytest.raises(TimingCycleError) as error:
        compile_timing(tl.bundle)
    assert "c2.start" not in error.value.path  # own end closes through picture start
    assert {"c2.plate.start", "c2.end", "film.pictureEnd"} <= set(error.value.path)
    assert error.value.path[0] == error.value.path[-1]
    assert tl.bundle == before


@pytest.mark.parametrize("until", ["end", "end of c2", "c2.end"])
def test_imported_terminal_until_preserves_compatibility_basis_and_idempotence(until):
    tl = tiny()
    intent.set_until(tl.cut_picture("c2").data, until)
    before = copy.deepcopy(tl.bundle)
    result = compile_timing(tl.bundle)
    assert result.bundle == before
    assert compile_timing(result.bundle).bundle == before


def test_terminal_sequence_end_land_and_member_metadata_are_preserved():
    tl = tiny()
    head = tl.cut_picture("c2")
    head.data["hold"] = 2.0
    intent.set_sequence(head.data, "ending", 0)
    intent.set_until(head.data, "end")
    tail = copy.deepcopy(head.data)
    tail.update(id="authored-tail", at=2.0, hold=2.0, params={"custom": "kept"})
    intent.set_sequence(tail, "ending", 1)
    intent.set_until(tail, None)
    tl.bundle["shots"]["B"]["internal_timeline"]["clips"].append(tail)
    intent.set_sequence_fit(head.data, {"land": "end"})
    tl.resolve()
    steps = tl.sequence("ending").steps
    assert steps[-1].end == 8.0 and steps[-1].id == "authored-tail"
    assert steps[-1].params["custom"] == "kept"
    before = copy.deepcopy(tl.bundle)
    tl.resolve()
    assert tl.bundle == before


@pytest.mark.parametrize("field", ["on", "until", "beat", "formula", "timing_formula", "word_formula", "land", "legacy_land", "later_member"])
def test_stored_ambiguity_refuses_every_reference_consumer_before_reflow(field):
    tl = ambiguous()
    clip = tl.clip("a-rocket")
    intent.set_on(clip.data, None)
    if field in ("on", "beat"):
        intent.set_on(clip.data, '"viral"' if field == "on" else 'beat 1 after "viral"')
    elif field == "until":
        intent.set_until(clip.data, 'after "viral"')
    elif field in ("formula", "timing_formula"):
        intent.set_formula(clip.data, "params.delay" if field == "formula" else "hold",
                           {"moment": '"viral"', "as": "timeline_seconds"})
    elif field == "word_formula":
        intent.set_formula(clip.data, "params.delay", {"word": "missing", "text": "viral", "as": "timeline_seconds"})
    else:
        head = tl.cut_picture("c1")
        intent.set_sequence(head.data, "opening", 0)
        if field == "later_member":
            tail = copy.deepcopy(head.data)
            tail.update(id="tail", at=2.0, hold=2.0)
            intent.set_sequence(tail, "opening", 1)
            intent.set_on(tail, '"viral"')
            tl.bundle["shots"]["A"]["internal_timeline"]["clips"].append(tail)
        else:
            land = '"viral"' if field == "land" else {"word": "gone", "text": "viral"}
            intent.set_sequence_fit(head.data, {"land": land, "cycle": ["P"], "race": [2]})
    text = assert_refused_unchanged(tl, lambda: tl.reflow(gaps={"a-vo": 1.0}))
    assert ("c1.rocket" in text) if field in ("on", "until", "beat", "formula", "timing_formula", "word_formula") else ("c1.plate" in text or "tail" in text)


def test_reported_line_scoped_occurrence_choices_resolve_to_the_named_words():
    tl = ambiguous()
    intent._app_w(tl.clip("b-vo").data)["words"] = [[.1, .4, "viral"], [.6, .9, "viral"]]
    with pytest.raises(TimelineEditError) as error:
        tl.resolve()
    assert '"viral" in s2 #1 at ' in str(error.value)
    assert '"viral" in s2 #2 at ' in str(error.value)
    assert '"viral" in s2 #3' not in str(error.value)
    assert tl._moment_time('"viral" in s2 #1') == tl.word("viral", n=3).start
    assert tl._moment_time('"viral" in s2 #2') == tl.word("viral", n=4).start


def test_ambiguity_refusal_keeps_compiler_inputs_and_commands_immutable():
    tl = ambiguous()
    state = {"notes": ["keep"], "_music": "plays_on"}
    calls = [("reflow", (), {"gaps": {"a-vo": 1.0}})]
    before = copy.deepcopy((tl.bundle, state, calls))
    with pytest.raises(TimelineEditError) as error:
        compile_timing(TimingInputs(tl.bundle, state), calls)
    assert error.value.code == "AMBIGUOUS_REFERENCE"
    assert (tl.bundle, state, calls) == before


def test_ambiguity_in_a_later_compiled_command_refuses_partial_adoption(monkeypatch):
    tl = tiny()
    before = copy.deepcopy(tl.__dict__)

    def broken(workspace):
        intent._app_w(workspace.clip("a-vo").data)["words"].append([2.1, 2.4, "viral"])
        workspace.clip("a-rocket").data["at"] = 0.0
        raise RuntimeError("error after an ambiguous partial write")

    monkeypatch.setattr(Checkout, "retime", broken)
    with pytest.raises(TimelineEditError) as error:
        tl.resolve()
    assert error.value.code == "AMBIGUOUS_REFERENCE"
    assert tl.__dict__ == before


def test_explicit_occurrence_and_frozen_orphan_formula_keep_existing_behavior():
    tl = ambiguous()
    clip = tl.clip("a-rocket")
    intent.set_on(clip.data, '"viral" in s1 #2')
    intent.set_formula(clip.data, "params.delay", {"moment": '"viral"', "orphan": "ORPHAN: keep cache"})
    clip.params["delay"] = 9.0
    tl.resolve()
    assert clip.start == pytest.approx(2.6)
    assert clip.params["delay"] == 9.0
    assert intent.on(clip.data) == '"viral" in s1 #2'


def test_keep_end_film_command_refuses_its_actual_music_feedback():
    tl = beat_film()
    before = copy.deepcopy(tl.__dict__)
    with pytest.raises(TimingCycleError) as error:
        tl.film_end('beat 2 after "now"')
    assert "a-music.end" in error.value.path and "c2.plate.end" in error.value.path
    assert tl.__dict__ == before


def test_plays_on_film_command_retains_acyclic_beats_and_policy():
    tl = beat_film()
    tl.film_end('beat 2 after "now"', music="plays_on")
    assert tl.duration == 7.0 and tl.music == "keep_end"
    assert tl.clip("a-music").end == 8.0


def test_plays_on_override_preserves_an_existing_numeric_ripple_basis():
    from astrid.sdk.timeline.music_beds import sources
    tl = beat_film()
    tl.insert_time(2.0, 1.0)
    before = {owner: copy.deepcopy(entry["ripple_basis"]) for owner, entry in sources(tl).items()}
    assert before and all(before.values())
    target = tl._moment_time('beat 1 after "it" +7s')
    tl.film_end('beat 1 after "it" +7s', music="plays_on")
    assert tl.duration == target and tl.music == "keep_end"
    assert {owner: entry["ripple_basis"] for owner, entry in sources(tl).items()} == before
    snapshot = copy.deepcopy(tl.bundle)
    tl.resolve()
    assert tl.bundle == snapshot


def test_ambiguity_rolls_back_an_earlier_timing_command_in_the_same_edit():
    tl = tiny()
    before = copy.deepcopy(tl.__dict__)
    bundle = tl.bundle
    with pytest.raises(TimelineEditError) as error:
        with tl.edit("timing before ambiguity", check=False, quiet=True):
            tl.insert_time(2.0, .5)
            intent._app_w(tl.clip("a-vo").data)["words"].append([2.1, 2.4, "viral"])
            tl.resolve()
    assert error.value.code == "AMBIGUOUS_REFERENCE"
    assert tl.__dict__ == before and tl.bundle is bundle


def test_deliberate_repairs_are_listed_in_existing_release_recipe():
    text = (Path(__file__).resolve().parents[2] / "docs/setup/release-recipe.md").read_text()
    assert "REPAIRS-STRUCT" in text and "AMBIGUOUS_REFERENCE" in text and "terminal" in text
