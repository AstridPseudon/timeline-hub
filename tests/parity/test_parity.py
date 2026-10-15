from __future__ import annotations

import importlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from tools.parity.inventory import build_inventory


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "tests/parity/inventory.json"
LEDGER = ROOT / "tests/parity/removed.yaml"
APPROVED = re.compile(r"^user \d{4}-\d{2}-\d{2}$")


def _feature_map(inventory: dict[str, Any]) -> dict[str, Any]:
    features: dict[str, Any] = {}
    for path, command in inventory["commands"].items():
        if path != "timelines":
            features[f"command:{path}"] = {"registered": True}
        for action in command["flags"]:
            for option in action["options"]:
                features[f"flag:{path}:{option}"] = action
        for argument in command["positionals"]:
            features[f"argument:{path}:{argument['dest']}"] = argument
    for class_name, item in inventory["sdk"].items():
        features[f"sdk:{class_name}"] = {"signature": item["signature"]}
        for name, member in item["members"].items():
            features[f"sdk:{class_name}.{name}"] = member
    for category, codes in inventory["finding_codes"].items():
        for code in codes:
            features[f"finding:{category}:{code}"] = {"registered": True}
    for category in ("presets", "views", "layer_views", "layers"):
        for name in inventory["visualize"][category]:
            features[f"visualize:{category}:{name}"] = {"registered": True}
    return features


def _ledger_rows() -> list[dict[str, Any]]:
    value = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or []
    assert isinstance(value, list), "removed.yaml must contain a list of removal records"
    assert all(isinstance(row, dict) for row in value), "each removed.yaml record must be a mapping"
    return value


def _option_strings(inventory: dict[str, Any]) -> set[str]:
    return {
        option
        for command in inventory["commands"].values()
        for action in command["flags"]
        for option in action["options"]
    }


def _alias_is_parseable(alias: Any, inventory: dict[str, Any], *, feature: str | None = None) -> bool:
    if not isinstance(alias, str) or not alias.strip():
        return False
    alias = alias.strip()
    if alias.startswith("-"):
        if feature and feature.startswith("flag:"):
            command_path = feature.removeprefix("flag:").rsplit(":", 1)[0]
            return any(
                alias in action["options"]
                for action in inventory["commands"].get(command_path, {}).get("flags", [])
            )
        return alias in _option_strings(inventory)
    if alias.startswith("command:") or alias.startswith("sdk:") or alias.startswith("finding:") or alias.startswith("visualize:"):
        return alias in _feature_map(inventory)
    if alias.startswith("timelines."):
        return alias in inventory["commands"] or f"command:{alias}" in _feature_map(inventory)
    if "." in alias:
        module_name, attribute = alias.rsplit(".", 1)
        try:
            return callable(getattr(importlib.import_module(module_name), attribute))
        except (ImportError, AttributeError, ValueError):
            return False
    return False


def _validate_removal_row(feature: str, row: dict[str, Any] | None, inventory: dict[str, Any]) -> None:
    assert row is not None, f"removed inventory feature {feature!r} needs a matching removed.yaml entry"
    for field in ("feature", "card", "reason", "alias"):
        assert field in row, f"removed.yaml entry for {feature!r} is missing {field!r}"
    assert row["feature"] == feature, f"removed.yaml feature must exactly match {feature!r}"
    assert isinstance(row["card"], str) and row["card"].strip(), f"removed.yaml entry for {feature!r} needs a card"
    assert isinstance(row["reason"], str) and row["reason"].strip(), f"removed.yaml entry for {feature!r} needs a reason"
    alias = row["alias"]
    if alias:
        assert _alias_is_parseable(alias, inventory, feature=feature), (
            f"removed.yaml alias {alias!r} for {feature!r} does not parse or resolve"
        )
    else:
        assert isinstance(row.get("approved"), str) and APPROVED.fullmatch(row["approved"]), (
            f"removed feature {feature!r} without an alias needs 'approved: user YYYY-MM-DD'"
        )


def _comparison_inventory() -> dict[str, Any]:
    """Compare working edits to HEAD, or a clean commit to its parent snapshot."""
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    ref = "HEAD" if status.strip() else "HEAD^"
    result = subprocess.run(
        ["git", "show", f"{ref}:tests/parity/inventory.json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def _damaged_art_measurement() -> float | None:
    path = ROOT / "tests/parity/.damaged-art-probe.png"
    try:
        from PIL import Image

        from astrid.sdk.timeline.checkout import Checkout

        # A one-pixel opaque black sprite on transparency has a measurable outline.
        image = Image.new("RGBA", (3, 3), (0, 0, 0, 0))
        image.putpixel((1, 1), (0, 0, 0, 255))
        image.save(path)
        checkout = Checkout.__new__(Checkout)
        value = checkout._native_outline_integrity({"local_path": str(path)})
        return float(value) if value is not None else None
    except Exception:  # an unavailable optional path must be reported by this parity guard
        return None
    finally:
        path.unlink(missing_ok=True)


def test_inventory_is_generated_from_current_code() -> None:
    current = build_inventory(ROOT)
    checked_in = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    assert current == checked_in


def test_inventory_generation_is_byte_stable() -> None:
    first = json.dumps(build_inventory(ROOT), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    second = json.dumps(build_inventory(ROOT), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    assert first.encode("utf-8") == second.encode("utf-8")


def test_disappearing_inventory_features_need_a_valid_disposition() -> None:
    previous = _feature_map(_comparison_inventory())
    current_inventory = build_inventory(ROOT)
    current = _feature_map(current_inventory)
    rows = _ledger_rows()
    by_feature = {row.get("feature"): row for row in rows}
    assert len(by_feature) == len(rows), "removed.yaml must not repeat a feature"
    for feature, previous_value in previous.items():
        if feature not in current or current[feature] != previous_value:
            _validate_removal_row(feature, by_feature.get(feature), current_inventory)


def test_hold_option_and_its_choices_remain_in_the_parser_inventory() -> None:
    inventory = build_inventory(ROOT)
    current = _feature_map(inventory).get("flag:timelines.edit:--hold")
    previous = _feature_map(_comparison_inventory()).get("flag:timelines.edit:--hold")
    if current != previous:
        rows = {row.get("feature"): row for row in _ledger_rows()}
        _validate_removal_row("flag:timelines.edit:--hold", rows.get("flag:timelines.edit:--hold"), inventory)
    else:
        assert current is not None, "timelines edit lost --hold"
        assert current["choices"] == ["deliberate", "off"]


def test_damaged_art_native_measurement_import_resolves() -> None:
    inventory = build_inventory(ROOT)
    value = _damaged_art_measurement()
    if value is None:
        rows = {row.get("feature"): row for row in _ledger_rows()}
        _validate_removal_row("finding:check:DAMAGED-ART", rows.get("finding:check:DAMAGED-ART"), inventory)
    else:
        assert value > 0.0, "DAMAGED-ART measurement did not inspect the native sprite outline"


def test_non_parsing_alias_is_rejected_for_a_removed_flag() -> None:
    inventory = build_inventory(ROOT)
    row = {
        "feature": "flag:timelines.edit:--former-option",
        "card": "TEST-CARD",
        "reason": "The old option has a documented replacement.",
        "alias": "--this-option-does-not-exist",
    }
    with pytest.raises(AssertionError, match="does not parse or resolve"):
        _validate_removal_row(row["feature"], row, inventory)


def test_matching_removed_flag_entry_with_a_parseable_alias_is_accepted() -> None:
    inventory = build_inventory(ROOT)
    row = {
        "feature": "flag:timelines.edit:--former-option",
        "card": "TEST-CARD",
        "reason": "The old spelling has a supported replacement.",
        "alias": "--why",
    }
    _validate_removal_row(row["feature"], row, inventory)


def test_matching_damaged_art_entry_can_point_to_a_resolved_replacement() -> None:
    inventory = build_inventory(ROOT)
    row = {
        "feature": "finding:check:DAMAGED-ART",
        "card": "TEST-CARD",
        "reason": "A replacement native outline measurement is recorded.",
        "alias": "astrid.packs.pixel.actions._common.outline_integrity",
    }
    _validate_removal_row(row["feature"], row, inventory)


def test_unaliased_removal_requires_explicit_user_approval() -> None:
    inventory = build_inventory(ROOT)
    row = {
        "feature": "finding:check:OLD-CODE",
        "card": "TEST-CARD",
        "reason": "No supported equivalent remains.",
        "alias": None,
    }
    with pytest.raises(AssertionError, match="approved: user YYYY-MM-DD"):
        _validate_removal_row(row["feature"], row, inventory)
    row["approved"] = "user 2026-10-15"
    _validate_removal_row(row["feature"], row, inventory)


def test_deliberate_removal_ledger_starts_with_r4_changes() -> None:
    rows = {row["feature"]: row for row in _ledger_rows()}
    expected = {
        "deliberate: timelines.edit --set KEY=null": "UX-CLEAR",
        "deliberate: --remove on a picture clip": "M4",
        "deliberate: two 0.5-opacity layers count as covered": "SCENE-PLAN",
        "deliberate: core/timeline/inverses.py": "M2",
        "deliberate: stale draft expiry": "TL-LIFECYCLE",
    }
    assert {feature: rows.get(feature, {}).get("card") for feature in expected} == expected
    assert all(rows[feature].get("reason") and rows[feature].get("alias") for feature in expected)
