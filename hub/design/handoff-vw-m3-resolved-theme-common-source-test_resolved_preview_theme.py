"""UNAPPLIED tests intended for tests/packs/rendering/test_resolved_preview_theme.py.

Policy: PLAN 2026-10-20 06:07; final export theme is the single authority.
These CPU tests do not qualify a host-to-browser read or custom theme pins.
"""
import copy
import json

import pytest

from astrid.core.theme import builtin_theme
from astrid.packs.rendering.shared.rendering_backend import _resolved_theme_for_render


@pytest.mark.parametrize("theme_id", [None, "banodoco-default", "uninstalled-example"])
def test_unpinned_preview_source_is_exact_final_export_theme(tmp_path, theme_id):
    config = {"tracks": [], "clips": []}
    if theme_id is not None:
        config["theme"] = theme_id
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps(config))
    before = path.read_bytes()
    resolved = _resolved_theme_for_render(path, None)
    assert resolved == builtin_theme()
    assert path.read_bytes() == before
    resolved["visual"]["color"]["bg"] = "authored mutation probe"
    assert _resolved_theme_for_render(path, None) == builtin_theme()


def test_authored_color_overrides_preserve_complete_final_export_remainder(tmp_path):
    config = {"tracks": [], "clips": [],
              "theme_overrides": {"visual": {"color": {"bg": "#123456"}}}}
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps(config))
    expected = builtin_theme()
    expected["visual"]["color"]["bg"] = "#123456"
    assert _resolved_theme_for_render(path, None) == expected
    assert json.loads(path.read_text()) == config


def test_complete_authored_visual_survives_source_preparation(tmp_path):
    visual = builtin_theme()["visual"]
    visual["color"]["accent"] = "#654321"
    visual["type"]["families"]["heading"] = "Authored example face"
    config = {"tracks": [], "clips": [], "theme_overrides": {"visual": visual}}
    before = copy.deepcopy(config)
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps(config))
    resolved = _resolved_theme_for_render(path, None)
    assert resolved["visual"] == visual
    assert config == before == json.loads(path.read_text())
