"""UNAPPLIED, offline source preparation demonstration; no runtime/public API.

Run with PYTHONPATH pointing to the reviewed Agent tree. All themes are outputs
of the existing export resolver, never a reimplementation or literal default.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import inspect
import json
import subprocess
import tempfile
from pathlib import Path

from astrid.core.theme import builtin_theme
from astrid.packs.rendering.shared import rendering_backend as backend


def prepare(config: dict, directory: Path, runtime_theme_path: Path | None = None) -> dict:
    """Proposed local result member; browser delivery is absent in product code."""
    path = directory / "timeline.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return {
        "config": copy.deepcopy(config),
        "theme": backend._resolved_theme_for_render(path, runtime_theme_path),
    }


def examples() -> dict:
    minimal = {"tracks": [], "clips": []}
    visual = builtin_theme()["visual"]
    # Authored example inputs, never implicit defaults.
    visual["color"]["bg"] = "#273849"
    visual["type"]["families"]["heading"] = "Example authored face"
    cases = {
        "implicit": minimal,
        "explicit_default": {**minimal, "theme": builtin_theme()["id"]},
        "color_override": {**minimal, "theme_overrides": {"visual": {"color": {"bg": "#123456"}}}},
        "full_visual_override": {**minimal, "theme_overrides": {"visual": visual}},
    }
    with tempfile.TemporaryDirectory(prefix="theme-source-") as raw:
        root = Path(raw)
        return {name: prepare(config, root) for name, config in cases.items()}


def source_binding() -> dict:
    # Review metadata only, not a product receipt or new theme authority.
    import astrid.core.theme._schema as schema
    root = Path(inspect.getfile(backend)).resolve().parents[5]
    paths = [Path(inspect.getfile(backend)).resolve(), Path(inspect.getfile(schema)).resolve()]
    return {
        "agent_commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
        "files": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
        "resolver": "astrid.packs.rendering.shared.rendering_backend._resolved_theme_for_render",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--default-only", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    values = examples()
    payload = values["implicit"]["theme"] if args.default_only else {
        "qualification": "offline resolver outputs only; no host/browser delivery",
        "source": source_binding(), "cases": values,
    }
    expected = json.dumps(payload, indent=2) + "\n"
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != expected:
            raise SystemExit("Stale generated theme: regenerate from the selected Agent source")
        print("Generated output matches the actual selected Agent resolver")
    else:
        args.output.write_text(expected, encoding="utf-8")
        print(args.output)
