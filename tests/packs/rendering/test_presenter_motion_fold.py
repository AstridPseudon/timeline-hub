"""Exact selected-cut counts from the registered presenter, without private math."""

import json
from fractions import Fraction

import pytest

from astrid.packs.rendering.actions.timeline_visualize.motion import sheet
from tests.packs.rendering.test_presenter_scene_capability import (
    presenter_query as _presenter_query,
)
from tests.packs.rendering.test_scene_sampling_plan import composed_snapshot

presenter_query = _presenter_query


@pytest.mark.integration
def test_registered_presenter_exact_cut_counts_by_compiled_occurrence(presenter_query):
    snapshot = composed_snapshot()
    repeated = [c for c in snapshot["config"]["clips"]
                if c["app"]["astrid_shot_composition"]["source_clip_id"] == "lower"]
    fps = Fraction(30000, 1001)
    # Exercise the existing panel sampler, not a new approximation of its clock.
    samples = sheet.curve_sample_frames((0, Fraction(301) / fps), fps)
    assert len(samples) == sheet.SCENE_FRAME_BUDGET == 60
    assert not set(samples).intersection((180, 181, 182))
    assert presenter_query("exact-fold", json.dumps({"repeated": repeated, "samples": samples}))["ok"]
