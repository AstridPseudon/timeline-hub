"""Check or regenerate the portable parent track.create golden from Agent."""
import json
import sys
from pathlib import Path

from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute

AGENT_SOURCE = "027bd16d96010544331c953c0e1014e161786e71"
SCHEMA_SHA256 = "472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9"
FIXTURES = Path(__file__).parent
SOURCE = FIXTURES / "recipe_m1_move.json"
TARGET = FIXTURES / "recipe_m2_app_track_create.json"
ROW = {
    "id": "A1",
    "kind": "audio",
    "label": "A1",
    "scale": 1,
    "fit": "contain",
    "opacity": 1,
    "blendMode": "normal",
    "muted": None,
    "opaque": {"keep": [None, False, {"nested": "opaque"}]},
    "unknown": [None, False, {"preserve": True}],
}


def main() -> None:
    if sys.argv[1:] not in ([], ["--update"]):
        raise SystemExit("usage: track_create_parity.py [--update]")
    source = json.loads(SOURCE.read_text())
    bundle = source["bundle"]
    command = capture_track_create(bundle, "parent", ROW)
    plan = execute(bundle, [command])
    expected = {
        "agent_source": AGENT_SOURCE,
        "schema_sha256": SCHEMA_SHA256,
        "source_fixture": SOURCE.name,
        "input": {"select": "parent", "row": ROW},
        "bundle": bundle,
        "command": command,
        "record": plan.records[0],
        "after_bundle": plan.bundle,
    }
    encoded = json.dumps(expected, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n"
    if sys.argv[1:] == ["--update"]:
        TARGET.write_text(encoded)
    else:
        assert TARGET.read_text() == encoded, "native track.create golden changed; review before regenerating"
    print("Agent 027bd16d exact parent track.create command, record and result verified")


if __name__ == "__main__":
    main()
