from __future__ import annotations

import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline_checkout import Checkout

TINY = Path(__file__).resolve().parents[1] / "fixtures" / "timeline_editing" / "tiny.json"


def tiny():
    data = json.loads(TINY.read_text(encoding="utf-8"))
    data["shots"]["A"]["internal_timeline"]["registry"]["assets"]["Q"]["duration"] = 10.0
    return Checkout(data)


def test_add_audio_has_no_cut_and_uses_the_source_duration():
    tl = tiny()
    clip = tl.add("media", asset="Q", track="music", at=1, cut=None, clip_id="bed")
    assert clip.cut_id is None
    assert clip.start == pytest.approx(1)
    assert clip.duration == pytest.approx(10)
    assert clip.data["from"] == 0
    assert clip.data["to"] == 10


def test_trim_keeps_film_start_and_slip_keeps_film_span():
    tl = tiny()
    clip = tl.clip("a-music")
    clip.trim(in_s=1, out_s=3)
    assert clip.start == pytest.approx(0)
    assert clip.duration == pytest.approx(2)
    clip.slip(2)
    assert clip.start == pytest.approx(0)
    assert clip.duration == pytest.approx(2)
    assert clip.data["from"] == 3
    assert clip.data["to"] == 5


@pytest.mark.parametrize("method", [lambda clip: clip.trim(in_s=-1), lambda clip: clip.trim(out_s=11), lambda clip: clip.slip(-1), lambda clip: clip.slip(7)])
def test_source_bounds_name_the_clip_and_file_limit(method):
    tl = tiny()
    with pytest.raises(TimelineEditError, match=r"a-music:.*(0–10|0–10\.0)"):
        method(tl.clip("a-music"))
