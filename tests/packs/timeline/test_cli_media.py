from __future__ import annotations

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
    monkeypatch.setattr(tl, "save", lambda **_kwargs: Path("draft.json"))
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
