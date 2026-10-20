"""The implicit default follows Composition; explicit film styling stays authored."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.core.theme import ThemeValidationError, builtin_theme, validate_theme_document
from astrid.packs.rendering.shared.rendering_backend import _resolved_theme_for_render

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEFAULT = json.loads(
    (ROOT / "tests/fixtures/themes/public-composition-default.json").read_text()
)


def _timeline(tmp_path: Path, **updates: object) -> Path:
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps({"tracks": [], "clips": [], **updates}))
    return path


def _explicit_theme() -> dict:
    # Keep the historical export style as a fully explicit film, not a default.
    return json.loads((ROOT / "tests/golden/hype/merged_render_props.json").read_text())["theme"]


def test_builtin_matches_complete_public_default_and_schema() -> None:
    assert validate_theme_document(PUBLIC_DEFAULT) == PUBLIC_DEFAULT
    assert builtin_theme() == PUBLIC_DEFAULT


def test_builtin_returns_an_independent_copy() -> None:
    theme = builtin_theme()
    theme["visual"]["type"]["families"]["heading"] = "changed"
    assert builtin_theme() == PUBLIC_DEFAULT


@pytest.mark.parametrize("slug", [None, "banodoco-default", "2rp", "unknown-theme"])
def test_unpinned_theme_uses_public_default_without_slug_lookup(tmp_path: Path, slug) -> None:
    path = _timeline(tmp_path, **({"theme": slug} if slug is not None else {}))
    before = path.read_bytes()
    assert _resolved_theme_for_render(path, None) == PUBLIC_DEFAULT
    assert path.read_bytes() == before


def test_runtime_pin_preserves_full_explicit_theme(tmp_path: Path) -> None:
    theme = _explicit_theme()
    theme["id"] = "owner-film"
    pin = tmp_path / "theme.json"
    pin.write_text(json.dumps(theme))
    before = pin.read_bytes()
    assert _resolved_theme_for_render(_timeline(tmp_path, theme="2rp"), pin) == theme
    assert pin.read_bytes() == before


def test_complete_authored_visual_theme_is_preserved(tmp_path: Path) -> None:
    theme = _explicit_theme()
    path = _timeline(tmp_path, theme=theme["id"], theme_overrides={"visual": theme["visual"]})
    before = path.read_bytes()
    assert _resolved_theme_for_render(path, None) == theme
    assert path.read_bytes() == before


@pytest.mark.parametrize("pinned", [False, True])
def test_partial_override_keeps_resolved_remainder(tmp_path: Path, pinned: bool) -> None:
    base = _explicit_theme() if pinned else PUBLIC_DEFAULT
    pin = tmp_path / "theme.json" if pinned else None
    if pin is not None:
        pin.write_text(json.dumps(base))
    path = _timeline(tmp_path, theme_overrides={"visual": {"color": {"accent": "#abcdef"}}})
    expected = copy.deepcopy(base)
    expected["visual"]["color"]["accent"] = "#abcdef"
    assert _resolved_theme_for_render(path, pin) == expected
    assert builtin_theme() == PUBLIC_DEFAULT


def test_nested_override_keeps_existing_shallow_merge_semantics(tmp_path: Path) -> None:
    path = _timeline(tmp_path, theme_overrides={"visual": {"type": {"families": {"heading": "Owner"}}}})
    expected = copy.deepcopy(PUBLIC_DEFAULT)
    expected["visual"]["type"]["families"] = {"heading": "Owner"}
    assert _resolved_theme_for_render(path, None) == expected


def test_unknown_theme_fields_still_fail_validation() -> None:
    theme = copy.deepcopy(PUBLIC_DEFAULT)
    theme["visual"]["unknown"] = True
    with pytest.raises(ThemeValidationError, match="Additional properties are not allowed"):
        validate_theme_document(theme)


def test_explicit_missing_runtime_pin_never_uses_default(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="theme file not found or invalid"):
        _resolved_theme_for_render(_timeline(tmp_path), tmp_path / "theme.json")
