"""Registered checks must retain clips drawn outside their authored window."""

import pytest

from astrid.packs.rendering.actions.timeline_visualize.motion.conditions import run_checks
from tests.packs.rendering.test_motion_cover_public import (
    clip,
    cover,
    elements,
    timeline,
)
from tests.packs.rendering.test_motion_cover_public import (
    public_query as _public_query,
)

public_query = _public_query


@pytest.mark.integration
def test_registered_composition_check_keeps_public_incoming_preroll(public_query):
    config = timeline([
        clip("a", "back", x=700),
        clip("b", "back", at=1, transition={"type": "fade", "duration": .4}),
        clip("upper", "front", "am-callout", hold=2),
    ])
    shared = public_query(config, [24])
    assert 'data-clip="b"' in shared["html"]["24"]
    assert shared["scene_occlusions"]["0.98"]["24"]["b"]["occluderId"] == "upper"

    # The midpoint is frame 24. The canonical clip starts at 1s, after
    # this selected window, but the public draw window includes it.
    per_cut, _ = run_checks(
        [{"index": 1, "start": .7, "end": .9}], elements(config), 30,
        only=["composition"], shared=shared,
    )
    assert cover(per_cut[0][1]) == ['am-callout "upper" fully covers am-type "b"']
