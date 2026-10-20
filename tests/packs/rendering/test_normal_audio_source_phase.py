"""Slicing an audio clip must preserve its original fade phase.

The slicer rewrites at/from/to, so two different originals can slice to the
same clip; the host therefore records the original phase on the slice.  The
PCM requirements need the trusted prepared-source producer, which this tree
does not have yet (docs/design/audio-compile-contract.md, join plan).
"""

import copy

import pytest

from astrid.core.rendering.contracts import FrameWindow
from astrid.core.rendering.service import RenderService

WINDOW = FrameWindow(start_frame=15, end_frame=45, fps_rational=(30, 1))


def _timeline():
    return {
        "tracks": [{"id": "A1", "kind": "audio"}],
        "clips": [{"id": "sound", "track": "A1", "asset": "sound", "at": 0,
                   "from": 0, "to": 2,
                   "params": {"fadeIn": 0.5, "fadeOut": 0.5}}],
    }


def test_slice_records_original_phase_that_the_cut_clip_cannot_recover():
    first = _timeline()
    second = copy.deepcopy(first)
    second["clips"][0].update(at=0.5, **{"from": 0.5})
    before = copy.deepcopy(first)
    a = RenderService._window_timeline(first, WINDOW)["clips"][0]
    b = RenderService._window_timeline(second, WINDOW)["clips"][0]
    # Same cut clip; original gain at source .5 is 1 in first, 0 in second.
    assert {k: v for k, v in a.items() if k != "app"} == {k: v for k, v in b.items() if k != "app"}
    assert a["app"]["astrid_slice_origin"] == {"id": "sound", "at": 0, "from": 0, "to": 2}
    assert b["app"]["astrid_slice_origin"] == {"id": "sound", "at": 0.5, "from": 0.5, "to": 2}
    assert a["at"] == 0 and a["from"] == 0.5
    assert first == before


def test_slice_origin_is_host_owned_and_only_for_fading_clips():
    timeline = _timeline()
    timeline["clips"][0]["app"] = {"astrid_slice_origin": {"at": 9}, "keep": 1}
    timeline["clips"].append({"id": "plain", "track": "A1", "asset": "x", "at": 0,
                              "from": 0, "to": 2,
                              "app": {"astrid_slice_origin": {"at": 9}}})
    fading, plain = RenderService._window_timeline(timeline, WINDOW, tracks=["A1"])["clips"]
    assert fading["app"] == {"keep": 1, "astrid_slice_origin": {"id": "sound", "at": 0, "from": 0, "to": 2}}
    assert plain["app"] == {}


@pytest.mark.parametrize("asset", ["sound", "other"])
@pytest.mark.parametrize("tracks", [None, ("A1", "A2")], ids=["window", "layer"])
@pytest.mark.xfail(
    strict=True,
    raises=ImportError,
    reason="Agent source owner: trusted prepared-source producer "
    "(normal_audio) must translate the recorded origin so the 0..2s clip "
    "sliced at .5s with fadeIn .5 keeps (.25, -.125) at source .5",
)
def test_half_second_slice_pcm_equals_original_on_host_served_wav(tracks, asset):
    from astrid.packs.rendering.rendering.renderers.remotion.normal_audio import (  # noqa: F401
        prepare_normal_audio_sources,
    )
