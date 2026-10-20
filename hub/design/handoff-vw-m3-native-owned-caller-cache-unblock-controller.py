"""Manager-reviewed offline source gate for the owned native caller.

This controller deliberately does not launch a browser or renderer.  Its
future capture mode refuses until the Agent-owned host carries the already
approved explicit browser selector; it supplies no alias, fallback, fake
validation, or new cache mechanism.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


WORKER = "vw-m3-native-owned-caller-cache-unblock"
PREFIX = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design") / f"handoff-{WORKER}"
SOURCES = (
    "astrid/packs/rendering/rendering/renderers/remotion/run.py",
    "astrid/core/execution/remotion_host_session.py",
    "tests/core/execution/test_remotion_host_session.py",
    "tests/packs/rendering/test_scene_source_carry.py",
    "remotion/shared-browser.mjs",
    "remotion/src/astrid-frame-worker.mjs",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(root: Path) -> dict[str, object]:
    files = {name: sha(root / name) for name in SOURCES}
    caller = (root / SOURCES[0]).read_text(encoding="utf-8")
    host = (root / SOURCES[1]).read_text(encoding="utf-8")
    browser = (root / "remotion/shared-browser.mjs").read_text(encoding="utf-8")
    worker = (root / "remotion/src/astrid-frame-worker.mjs").read_text(encoding="utf-8")
    if "if not (frame_mode and frame_session is not None):" not in caller:
        raise RuntimeError("owned caller conditional is missing")
    if '"ASTRID_REMOTION_PROJECT_DIR"' not in host or '"ASTRID_REMOTION_BROWSER_EXECUTABLE"' in host:
        raise RuntimeError("unexpected core host source shape")
    if "ASTRID_REMOTION_BROWSER_EXECUTABLE" not in browser or "sharedBrowserExecutable" not in worker:
        raise RuntimeError("approved shared-browser selector seam is missing")
    return {"kind": "owned-caller-source-review", "source": files}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preflight", "capture"))
    parser.add_argument("--source", type=Path, default=Path.cwd())
    parser.add_argument("--reviewed-sha256")
    args = parser.parse_args()
    data = fingerprint(args.source.resolve())
    digest = hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if args.mode == "preflight":
        print(json.dumps({**data, "fingerprint_sha256": digest}, indent=2, sort_keys=True))
        return 0
    if args.reviewed_sha256 != digest:
        raise SystemExit("manager-reviewed new source fingerprint is required")
    raise SystemExit(
        "physical capture refused: HostRemotionSession._start drops "
        "ASTRID_REMOTION_BROWSER_EXECUTABLE; wait for the Agent core fix and refresh this fingerprint"
    )


if __name__ == "__main__":
    raise SystemExit(main())
