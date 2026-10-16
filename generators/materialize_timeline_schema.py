"""Materialize the pinned canonical TimelineConfig schema for Runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent.parent / "banodoco-workspace" / "packages" / "timeline-schema"
PIN = "242f9c4306bf3b501222cb041a9eb246ef47bc85"
SCHEMA_RELATIVE = Path("python/banodoco_timeline_schema/timeline.schema.json")
OUTPUT = ROOT / "contract/schemas/timeline-config.schema.json"
PROVENANCE = ROOT / "contract/schemas/timeline-config.schema.provenance.json"
EXPECTED_SHA256 = "f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1"
# Already-admitted track-role slice on this assigned base, preserved by D022.
ROLE_EXTENSION = {
    "property": "TimelineConfig.tracks[].role", "values": ["output", "source"],
    "source_receipt": "receiving/coordination/evidence/C/reigh-main-role-slice-20261009/integration-receipt.json",
    "source_commit": "3bd1d019715de79cd54aa208cf26de10427c29d5",
    "source_artifact": "vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json",
    "source_artifact_sha256": EXPECTED_SHA256,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--source", type=Path, default=Path(os.environ.get("BANODOCO_TIMELINE_SCHEMA_ROOT", DEFAULT_SOURCE)))
    args = parser.parse_args()
    source = args.source.resolve()
    schema_source = source / SCHEMA_RELATIVE
    manifest = {
        "owner": "@banodoco/timeline-schema#TimelineConfig",
        "package": "@banodoco/timeline-schema",
        "version": "0.0.2",
        "source_commit": PIN,
        "source_tree": "75a5a697f630affee40632e500b3f5b704a9b834",
        "source_artifact": str(SCHEMA_RELATIVE),
        "sha256": EXPECTED_SHA256,
        "role_extension": ROLE_EXTENSION,
    }
    if not schema_source.is_file() or sha256(schema_source) != EXPECTED_SHA256:
        raise SystemExit(f"canonical schema artifact missing or differs from pinned {PIN}: {schema_source}")
    group_source = ROOT / "contract/schemas/shot-group.schema.json"
    group = json.loads(group_source.read_text())
    extended = json.loads(schema_source.read_text())
    extended["properties"]["pinnedShotGroups"]["items"] = {k: v for k, v in group.items() if k not in {"$id", "$schema"}}
    expected = (json.dumps(extended, indent=2) + "\n").encode()
    manifest["runtime_group_extension"] = {"source": "schemas/shot-group.schema.json", "sha256": sha256(group_source)}
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != expected:
            raise SystemExit("Runtime TimelineConfig materialization is stale; rerun this generator")
        if not PROVENANCE.is_file() or json.loads(PROVENANCE.read_text()) != manifest:
            raise SystemExit("Runtime TimelineConfig provenance is stale; rerun this generator")
        print(f"canonical TimelineConfig materialization clean: {PIN} sha256:{EXPECTED_SHA256}")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(expected)
    PROVENANCE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"materialized {OUTPUT.relative_to(ROOT)} from {PIN} sha256:{EXPECTED_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
