"""Coverage per frame at check time (TRUTH.md §2): a cut left with only its background plate is EMPTY, an inset
or a translucent plate does not cover the canvas, and a declared fade is a DIP, not a GAP.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline_checkout import Checkout

FPS = 30
# A complete, publishable candidate (schema 1, pinned base, source mapping). check() refuses an incomplete
# candidate outright (valid False), so the skeleton is the repo fixture; only the shots and tracks are ours.
PUBLISHABLE = Path(__file__).resolve().parents[1] / "fixtures" / "timeline_editing" / "tiny_publishable.json"
TRACKS = [
    {"id": "fx", "kind": "visual"}, {"id": "type", "kind": "visual"},
    {"id": "sprite", "kind": "visual"}, {"id": "plate", "kind": "visual"},
]


def _shot(fixture_shot, clips):
    """The fixture's shot (its shot_id and base_* fields), with our clips on the four visual tracks."""
    shot = copy.deepcopy(fixture_shot)
    shot["payload"] = {"name": "SHOT"}
    shot["internal_timeline"] = {"tracks": TRACKS, "clips": clips, "registry": {
        "assets": {"P": {"media_id": "sha256:c57bc0c5ceafe2c7fff32d0d16a3a4b0b4bb7885238ac376c70dbf53bd669f44"}}}}
    return shot


def bundle(a, b):
    """Shot A (0–4 s) is cut c01, a picture. Shot B (4–8 s) is cut c02, the span under test."""
    doc = copy.deepcopy(json.loads(PUBLISHABLE.read_text()))
    fixture = doc["shots"]
    a_clips = [{"id": "a-plate", "clipType": "am-snap-plate", "track": "plate", "asset": "P", "at": 0.0, "hold": 4.0,
                "params": {}, "app": {"cut": "c01", "layer": "field"}}] + a
    doc["shots"] = {"A": _shot(fixture["A"], a_clips), "B": _shot(fixture["B"], b)}
    return doc


def _empty_cut_bundle(**plate_fields):
    """c02 with ONLY its background plate: no asset, no params.src (the element.yaml 'flat background-only plate')."""
    plate = {"id": "b-plate", "clipType": "am-snap-plate", "track": "plate", "at": 0.0, "hold": 4.0,
             "params": {"fill": "#F7F4ED"}, "app": {"cut": "c02", "layer": "field"}}
    plate.update(plate_fields)
    return bundle([], [plate])


def _blocking(report, *words):
    return [line for line in report.blocking if all(w in line for w in words)]


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 EMPTY diagnostics require exact immutable Root props and declared am-snap-plate support.')
def test_a_cut_left_with_only_a_background_plate_is_advisory():
    report = Checkout(_empty_cut_bundle()).check()
    assert report.valid is True
    assert any("EMPTY" in line and "c02" in line and "4.000" in line for line in report.problems)
    assert not _blocking(report, "EMPTY")


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 EMPTY diagnostics require exact immutable Root props and declared am-snap-plate support.')
def test_a_deliberate_hold_waives_an_empty_cut():
    b = _empty_cut_bundle()
    # Without the hold: EMPTY is advisory under PLAN5.
    report = Checkout(b).check()
    assert report.valid is True
    assert any("EMPTY" in line and "c02" in line for line in report.problems)
    assert not _blocking(report, "EMPTY")
    # A deliberate hold remains valid and retains the EMPTY explanation.
    held = Checkout(b)
    held.set_cut_note("c02", hold="deliberate")
    report = held.check()
    assert report.valid is True, report.blocking
    assert not any("EMPTY" in line for line in report.blocking)
    assert any("EMPTY" in line and "c02" in line for line in report.problems), report.problems


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 GAP diagnostics require exact immutable Root props and declared am-footage bounds.')
def test_an_inset_footage_does_not_cover_the_canvas():
    inset = {"id": "b-inset", "clipType": "am-footage", "track": "fx", "asset": "P", "at": 0.0, "hold": 4.0,
             "params": {"x": 1200, "y": 600, "scale": 0.3}, "app": {"cut": "c02", "layer": "inset"}}
    report = Checkout(bundle([], [inset])).check()
    assert report.valid is True
    assert any("GAP" in line or "nothing covers the canvas" in line for line in report.problems)
    assert not _blocking(report, "GAP")


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 GAP diagnostics require exact immutable Root props and declared am-snap-plate alpha.')
def test_a_translucent_plate_does_not_cover_the_canvas():
    report = Checkout(_empty_cut_bundle(asset="P", params={}, opacity=0.4)).check()
    assert report.valid is True
    assert any("GAP" in line or "nothing covers the canvas" in line for line in report.problems)
    assert not _blocking(report, "GAP")


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 check diagnostics require exact compiled Root assets/theme and declared plate/fade capabilities.')
def test_a_declared_fade_in_is_a_dip_not_a_gap():
    report = Checkout(_empty_cut_bundle(asset="P", params={}, effects={"fade_in": 0.5})).check()
    assert report.valid is True, report.blocking
    assert not _blocking(report, "GAP")
    assert any("DIP" in line and "c02" in line and "0.50" in line for line in report.problems), report.problems



def test_deliberate_hold_preserves_empty_finding_and_waiver_classification():
    from astrid.core.timeline.scene_answers import Span

    checkout = Checkout(_empty_cut_bundle())
    spans = [Span(120, 240, "COVERED", "EMPTY", ("b-plate",))]
    sustained, incidental = checkout.empty_cuts(spans)
    assert any("EMPTY" in line and "c02" in line for line in sustained)
    assert incidental == []
    checkout.set_cut_note("c02", hold="deliberate")
    sustained, incidental = checkout.empty_cuts(spans)
    assert sustained == []
    assert any("EMPTY" in line and "c02" in line for line in incidental)
    assert checkout.check().valid
