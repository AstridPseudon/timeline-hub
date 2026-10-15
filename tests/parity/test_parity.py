from __future__ import annotations

import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
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


def test_inventory_import_resolves_to_this_checkout() -> None:
    module = importlib.import_module("tools.parity.inventory")
    assert Path(module.__file__).resolve() == (ROOT / "tools/parity/inventory.py").resolve()


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


def _fixture_source_root(parent: Path, marker: str) -> Path:
    root = parent / marker
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(
        ROOT / "astrid", root / "astrid", ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
    )
    shutil.copy2(ROOT / "pyproject.toml", root / "pyproject.toml")

    cli_path = root / "astrid/packs/timeline/cli.py"
    cli_path.write_text(
        cli_path.read_text(encoding="utf-8")
        + f"\n\n_original_build_parser = build_parser\n"
        + "def build_parser(client):\n"
        + "    parser = _original_build_parser(client)\n"
        + f"    parser.add_argument('--fixture-{marker}', action='store_true')\n"
        + "    return parser\n",
        encoding="utf-8",
    )
    window_path = root / "astrid/packs/rendering/actions/timeline_visualize/motion/window.py"
    window_path.write_text(
        window_path.read_text(encoding="utf-8").replace(
            'ALL_PRESETS = ("overview", *WINDOW_PRESETS, "compare")',
            f'ALL_PRESETS = ("overview", *WINDOW_PRESETS, "compare", "{marker}-preset")',
        ),
        encoding="utf-8",
    )
    assert f"--fixture-{marker}" in cli_path.read_text(encoding="utf-8")
    assert f'"{marker}-preset"' in window_path.read_text(encoding="utf-8")
    return root


def _generate_fixture_inventory(
    root: Path, output: Path, origins_output: Path
) -> subprocess.CompletedProcess[str]:
    generator = ROOT / "tools/parity/inventory.py"
    runner = textwrap.dedent(
        """
        import importlib
        import json
        import runpy
        import sys
        from pathlib import Path

        generator, source_root, output_path, origins_path = sys.argv[1:]
        sys.argv = [generator, "--root", source_root, "--output", output_path]
        try:
            runpy.run_path(generator, run_name="__main__")
        except SystemExit as exc:
            if exc.code not in (None, 0):
                raise
        names = (
            "astrid.packs.timeline.cli",
            "astrid.packs.rendering.actions.timeline_visualize.layers.base",
            "astrid.packs.rendering.actions.timeline_visualize.motion.window",
            "astrid.sdk.timeline.checkout",
            "astrid.sdk.timeline.look",
            "astrid.sdk.timeline.model",
        )
        origins = {
            name: importlib.import_module(name).__spec__.origin
            for name in names
        }
        Path(origins_path).write_text(json.dumps(origins, sort_keys=True) + "\\n", encoding="utf-8")
        """
    )
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, "-c", runner, str(generator), str(root), str(output), str(origins_output)],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


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


def test_two_source_inventory_comparison_isolated_and_deterministic(tmp_path: Path) -> None:
    fixture_parent = Path(os.environ.get("ASTRID_PARITY_FIXTURE_DIR", tmp_path / "source-trees"))
    fixture_parent.mkdir(parents=True, exist_ok=True)
    root_a = _fixture_source_root(fixture_parent, "alpha")
    root_b = _fixture_source_root(fixture_parent, "beta")
    output_root = Path(os.environ.get("ASTRID_PARITY_OUTPUT_DIR", tmp_path / "outputs"))
    output_root.mkdir(parents=True, exist_ok=True)

    output_a = output_root / "alpha-inventory.json"
    origins_a = output_root / "alpha-import-origins.json"
    output_b = output_root / "beta-inventory.json"
    origins_b = output_root / "beta-import-origins.json"
    output_a_repeat = output_root / "alpha-inventory-repeat.json"
    origins_a_repeat = output_root / "alpha-import-origins-repeat.json"
    _generate_fixture_inventory(root_a, output_a, origins_a)
    _generate_fixture_inventory(root_b, output_b, origins_b)
    _generate_fixture_inventory(root_a, output_a_repeat, origins_a_repeat)
    inventory_a = json.loads(output_a.read_text(encoding="utf-8"))
    inventory_b = json.loads(output_b.read_text(encoding="utf-8"))

    alpha_flag = "flag:timelines:--fixture-alpha"
    beta_flag = "flag:timelines:--fixture-beta"
    alpha_preset = "visualize:presets:alpha-preset"
    beta_preset = "visualize:presets:beta-preset"
    features_a = _feature_map(inventory_a)
    features_b = _feature_map(inventory_b)
    assert alpha_flag in features_a and alpha_preset in features_a
    assert beta_flag in features_b and beta_preset in features_b
    assert alpha_flag not in features_b and alpha_preset not in features_b
    assert beta_flag not in features_a and beta_preset not in features_a
    with pytest.raises(AssertionError, match="needs a matching removed.yaml entry"):
        _validate_removal_row(alpha_preset, None, inventory_b)

    origins = {
        "alpha": json.loads(origins_a.read_text(encoding="utf-8")),
        "beta": json.loads(origins_b.read_text(encoding="utf-8")),
    }
    for label, root in (("alpha", root_a), ("beta", root_b)):
        assert all(
            Path(origin).resolve().is_relative_to(root.resolve())
            for origin in origins[label].values()
        ), f"{label} inventory imported Astrid modules outside its source root: {origins[label]}"
    assert output_a.read_bytes() == output_a_repeat.read_bytes()

    guard = textwrap.dedent(
        """
        import sys
        from pathlib import Path
        sys.path.insert(0, sys.argv[1])
        from tools.parity.inventory import build_inventory
        first, second = map(Path, sys.argv[2:4])
        build_inventory(first)
        try:
            second_inventory = build_inventory(second)
        except RuntimeError as exc:
            if "fresh Python process" not in str(exc):
                raise
            print(str(exc))
        else:
            options = {
                option
                for command in second_inventory["commands"].values()
                for action in command["flags"]
                for option in action["options"]
            }
            if "--fixture-alpha" in options or "--fixture-beta" not in options:
                raise AssertionError(
                    "cross-root inventory mixed the first source's cached parser into the second inventory"
                )
            raise AssertionError("cross-root inventory reused cached Astrid modules without rejection")
        """
    )
    guard_result = subprocess.run(
        [sys.executable, "-c", guard, str(ROOT), str(root_a), str(root_b)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert guard_result.returncode == 0, guard_result.stderr
    assert "fresh Python process" in guard_result.stdout


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
