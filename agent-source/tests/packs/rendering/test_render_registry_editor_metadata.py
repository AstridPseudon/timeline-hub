"""Editor metadata on registry entries never reaches the renderer's strict schema."""
import pytest

from astrid.core import timeline
from astrid.packs.rendering.actions.render.managed_timeline import _render_compatible_projection

DIGEST = "a" * 64


def _entry(**extra):
    return {"media_id": "sha256:" + DIGEST, "content_sha256": DIGEST, "type": "image/png", **extra}


def test_swap_asset_metadata_is_projected_out_and_the_source_is_unchanged():
    registry = {"assets": {"BUGNET": _entry(handle="run:r/sprites#0", filename="sprite-00.png",
                                           source="run:r/sprites#0", pixel_provenance={"drawn_block": 13.0})}}
    with pytest.raises(ValueError, match="unknown key"):
        timeline.validate_registry(registry)
    _config, projected = _render_compatible_projection({"clips": []}, registry)
    timeline.validate_registry(projected)
    assert set(projected["assets"]["BUGNET"]) == {"media_id", "content_sha256", "type"}
    assert "pixel_provenance" in registry["assets"]["BUGNET"]  # the published document keeps it


def test_retired_locators_and_unknown_keys_still_fail():
    for extra in ({"path": "/tmp/x.png"}, {"mystery": 1}):
        _config, projected = _render_compatible_projection({"clips": []}, {"assets": {"A": _entry(**extra)}})
        with pytest.raises(ValueError, match="unknown key"):
            timeline.validate_registry(projected)
