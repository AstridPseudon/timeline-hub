"""Strict shared-schema behavior for clip-level modifier descriptors."""

from __future__ import annotations

from copy import deepcopy
from unittest.mock import patch

import jsonschema
import pytest

from astrid.core.timeline import load_timeline, save_timeline
from astrid.core.timeline.validators import timeline as timeline_validator


MODIFIERS = [
    {
        "id": "fresh_vignette_029",
        "element": "timeline.component/fresh_vignette_029.vignette",
        "params": {"strength": 0.6},
    }
]


def _minimal_timeline() -> dict:
    return {
        "tracks": [{"id": "visual", "kind": "visual", "label": "Visual"}],
        "clips": [
            {
                "id": "clip-1",
                "at": 0,
                "track": "visual",
                "modifiers": deepcopy(MODIFIERS),
            }
        ],
    }


def test_valid_clip_modifiers_validate_and_round_trip(tmp_path) -> None:
    timeline = _minimal_timeline()
    timeline_validator.validate_timeline(timeline)

    path = tmp_path / "timeline.json"
    save_timeline(timeline, path)
    loaded = load_timeline(path)

    assert loaded["clips"][0]["modifiers"] == MODIFIERS


def test_modifier_descriptor_extra_property_is_rejected_by_shared_schema() -> None:
    timeline = _minimal_timeline()
    timeline["clips"][0]["modifiers"][0]["unexpected"] = True

    with pytest.raises(jsonschema.ValidationError):
        timeline_validator.validate_timeline(timeline)


def test_unknown_clip_property_is_still_rejected_by_astrid_guard() -> None:
    timeline = _minimal_timeline()
    timeline["clips"][0]["unexpected"] = True

    # The canonical schema also refuses this key. Bypass only that first layer
    # here so this regression exercises Astrid's own clip allowlist guard.
    with patch.object(timeline_validator, "_validate_shared_timeline"):
        with pytest.raises(ValueError, match=r"clips\[0\] has unknown key 'unexpected'"):
            timeline_validator.validate_timeline(timeline)
