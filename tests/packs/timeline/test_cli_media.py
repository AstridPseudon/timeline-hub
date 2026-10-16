from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.packs.timeline import cli as timeline_cli
from astrid.packs.timeline import cli_sweep
from astrid.sdk.timeline_checkout import Checkout

TINY = Path(__file__).resolve().parents[2] / "fixtures" / "timeline_editing" / "tiny.json"


def _tiny() -> Checkout:
    data = json.loads(TINY.read_text(encoding="utf-8"))
    data["shots"]["A"]["internal_timeline"]["registry"]["assets"]["Q"]["duration"] = 10.0
    return Checkout(data)


def _run(monkeypatch, tl, *argv) -> int:
    monkeypatch.setattr(tl, "save", lambda *_args, **_kwargs: Path("draft.json"))
    monkeypatch.setattr(timeline_cli, "_edit_checkout", lambda _parsed: tl)
    monkeypatch.setattr(cli_sweep, "touched_cuts", lambda *_args: set())
    monkeypatch.setattr(cli_sweep, "auto_sweep_after_edit", lambda *_args, **_kwargs: 0)
    parsed = timeline_cli.build_parser(object()).parse_args(["edit", "--project", "p1", "main", *argv])
    return parsed.handler(parsed)


def test_add_media_adds_a_cut_free_audio_clip_of_the_whole_source(monkeypatch) -> None:
    tl = _tiny()
    assert _run(monkeypatch, tl, "--add-media", "Q", "--track", "music", "--on", "1", "--id", "bed") == 0
    clip = tl.clip("bed")
    assert clip.cut_id is None
    assert clip.start == pytest.approx(1)
    assert (clip.data["from"], clip.data["to"]) == (0, 10)


def test_trim_and_slip_keep_the_film_span(monkeypatch) -> None:
    tl = _tiny()
    assert _run(monkeypatch, tl, "--clip", "a-music", "--trim-in", "1", "--trim-out", "3") == 0
    assert _run(monkeypatch, tl, "--clip", "a-music", "--slip", "2") == 0
    clip = tl.clip("a-music")
    assert clip.start == pytest.approx(0)
    assert clip.duration == pytest.approx(2)
    assert (clip.data["from"], clip.data["to"]) == (3, 5)


def test_audio_fade_accepts_a_registered_curve_and_persists_it(monkeypatch) -> None:
    tl = _tiny()
    assert _run(monkeypatch, tl, "--clip", "a-music", "--fade-in", "3s", "curve=equal-power") == 0
    clip = tl.clip("a-music")
    assert clip.params["fadeIn"] == 3
    assert clip.params["fadeInCurve"] == "equal-power"
    from astrid.core.timeline import clip_fields as cf

    assert "curve=equal-power" in cf.describe(clip.data, fps=tl.fps)["fade_in"]
    assert _run(monkeypatch, tl, "--clip", "a-music", "--fade-in", "3s") == 0  # no curve token: back to linear
    assert "fadeInCurve" not in tl.clip("a-music").params


def test_unknown_audio_curve_is_refused_and_stored_bad_curves_fail_check() -> None:
    from astrid.sdk.timeline._common import TimelineEditError

    tl = _tiny()
    with pytest.raises(TimelineEditError, match="unknown audio curve"):
        tl.clip("a-music").set_look(fade_in="3s curve=wat")
    clip = tl.clip("a-music")
    clip.params["fadeInCurve"] = "wat"
    assert any("fadeInCurve is invalid" in problem for problem in tl._type_mismatches())


def test_crossfade_moves_b_and_writes_both_fades(monkeypatch, capsys) -> None:
    import copy

    tl = _tiny()
    a = tl.clip("a-music")
    b_data = copy.deepcopy(a.data)
    b_data.update(id="b-music", at=5.0)
    tl._internal(a.shot_id)["clips"].append(b_data)
    assert _run(monkeypatch, tl, "--crossfade", "a-music", "b-music", "curve=equal-power", "--over", "1") == 0
    b = tl.clip("b-music")
    assert b.start == pytest.approx(3.0)  # A stays 0..4; B moved to overlap it by one second
    assert a.params["fadeOut"] == b.params["fadeIn"] == 1
    assert a.params["fadeOutCurve"] == b.params["fadeInCurve"] == "equal-power"
    assert "moved b-music start" in capsys.readouterr().out


@pytest.mark.parametrize("curve", [None, "linear", "s-curve"])
def test_crossfade_records_curves_for_exact_replay_and_one_undo_step(tmp_path, monkeypatch, curve):
    from astrid.sdk import timeline_checkout as tc
    from astrid.sdk.timeline import commands, journal, store

    bundle = _tiny().bundle
    clips = bundle["shots"]["A"]["internal_timeline"]["clips"]
    a = next(clip for clip in clips if clip["id"] == "a-music")
    a["params"] = {"fadeOut": 0.2, "fadeOutCurve": "equal-power"}
    b = copy.deepcopy(a)
    b.update(id="next-bed", at=3.5, params={"fadeIn": 0.2, "fadeInCurve": "equal-power"})
    clips.append(b)
    bundle["parent"]["config"].setdefault("app", {}).setdefault("astrid", {})["cut_id_high_water"] = {
        "number": 2, "suffixes": {}}
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.setattr(tc, "resolve_ids", lambda *a, **k: ("p", "t", "rev-0"))
    monkeypatch.setattr(tc, "fetch_bundle", lambda *a, **k: copy.deepcopy(bundle))
    tl = Checkout.draft("p", "t")
    before = tl.document()
    argv = ["edit", "t", "--project", "p", "--crossfade", "a-music", "next-bed"]
    if curve is not None:
        argv.append(f"curve={curve}")
    parsed = timeline_cli.build_parser(None).parse_args([*argv, "--over", "0.5", "--no-sweep"])
    assert parsed.handler(parsed) == 0

    tl = Checkout.draft("p", "t")
    after = tl.document()
    assert tl.bundle["base_parent"] == before["base_parent"] == {"revision_id": "rev-0"}
    assert tl.clip("a-music").start == 0 and tl.clip("next-bed").start == 3.5
    assert tl.clip("a-music").duration == tl.clip("next-bed").duration == 4
    assert tl.clip("a-music").params["fadeOut"] == tl.clip("next-bed").params["fadeIn"] == 0.5
    expected_curve = curve or "equal-power"
    for clip, key in ((tl.clip("a-music"), "fadeOutCurve"), (tl.clip("next-bed"), "fadeInCurve")):
        if expected_curve == "linear":
            assert key not in clip.params
        else:
            assert clip.params[key] == expected_curve
    records = journal.read(journal.journal_path("p", "t"))
    calls = records[-1].calls
    assert [call["op"] for call in calls] == ["clip.enter-at", "clip.set-look", "clip.set-look"]
    for call, field in zip(calls[1:], ("fade_out", "fade_in")):
        assert call["args"][field] == (0.5 if expected_curve == "linear" else f"0.5s curve={expected_curve}")
    for call, side in zip(calls[1:], ("Out", "In")):
        for key, value in ((f"params.fade{side}", 0.2), (f"params.fade{side}Curve", "equal-power")):
            assert call["expect"][key] == {"state": "present", "value": value}
            assert call["authorship"][key] == "direct"
    batch = {"op": "timeline.batch", "select": None, "args": {"commands": list(calls)}}
    replay = Checkout(copy.deepcopy(before))
    commands.run(replay, batch)
    assert replay.document() == after
    for key, value in (("fadeOut", 0.3), ("fadeOutCurve", "exponential")):
        stale = Checkout(copy.deepcopy(before))
        stale.clip("a-music").params[key] = value
        stale_before = stale.document()
        with pytest.raises(commands.SemanticConflict, match="same-property"):
            commands.run(stale, batch)
        assert stale.document() == stale_before and not stale._journal
    assert len(list(store._history_dir(Path(tl.path)).glob("*.json"))) == 1
    assert tl.undo(1) and tl.document() == before
    assert tl.redo(1) and tl.document() == after
    assert journal.verify(journal.journal_path("p", "t")) == []
