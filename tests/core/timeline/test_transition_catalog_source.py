"""Exercise the lazy transition boundary with the authentic pack catalog."""

from __future__ import annotations

import pytest

from astrid.core.element import catalog
from astrid.core.timeline.validators.timeline import _validate_clip_transitions


@pytest.fixture
def catalog_loads(monkeypatch):
    catalog._clear_registry_cache()
    calls = []
    load = catalog.load_default_registry

    def counted_load(**kwargs):
        calls.append(kwargs)
        return load(**kwargs)

    monkeypatch.setattr(catalog, "load_default_registry", counted_load)
    yield calls
    catalog._clear_registry_cache()


def _clip(clip_id, at, **fields):
    return {"id": clip_id, "track": "v1", "at": at, "hold": 2, **fields}


@pytest.mark.parametrize("clips", [[], [_clip("a", 0)]], ids=["empty", "media"])
def test_no_transition_does_not_reach_registry(clips, catalog_loads):
    _validate_clip_transitions(clips, 30)

    assert catalog_loads == []


def test_authentic_transitions_share_one_catalog_load(catalog_loads):
    _validate_clip_transitions(
        [
            _clip("a", 0, transition={"id": "cross-fade", "durationFrames": 8}),
            _clip("b", 2, transition={"id": "fade", "duration": 0.5}),
            _clip("c", 4),
        ],
        30,
    )

    assert len(catalog_loads) == 1


def test_unknown_transition_reaches_authentic_catalog_and_is_refused(catalog_loads):
    with pytest.raises(ValueError, match="not present in the transitions catalog"):
        _validate_clip_transitions([_clip("a", 0, transition="missing-transition")], 30)

    assert len(catalog_loads) == 1


def test_modified_reference_is_checked_after_successful_validation(catalog_loads):
    clips = [_clip("a", 0)]
    _validate_clip_transitions(clips, 30)
    assert catalog_loads == []

    clips[0]["transition"] = "cross-fade"
    _validate_clip_transitions(clips, 30)
    assert len(catalog_loads) == 1

    clips[0]["transition"] = "missing-transition"
    with pytest.raises(ValueError, match="not present in the transitions catalog"):
        _validate_clip_transitions(clips, 30)
