"""Bounded offline probes of the commit path; never open a Runtime or Store.

Run with the checkout on PYTHONPATH. The retained capture is used unchanged.
Element-shaped documents use synthetic identities/media and are NOT accepted
history, provider execution, or a speed ratio against a mounted request.
"""

from __future__ import annotations

import argparse
import copy
import cProfile
import hashlib
import json
import statistics
import time
from collections import Counter
from pathlib import Path
from types import CodeType

from runtime_protocol import timeline_commit_auth as auth
from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.util import canonical_json

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "tests/fixtures/timeline_sequential_capture.json"


def element_document(scale: int = 1) -> dict:
    """Match the P2 seed's 2 parent/3 child clips, 1 shot and 1 occurrence.

    Shape source: App tests/e2e/local/support/harness.ts:commitNativeSeed,
    seedThreeProducts(..., 'native-none'), as used by the mounted element test.
    Scaling multiplies clip/asset rows, not roots or purported accepted history.
    """
    if scale not in (1, 4, 16):
        raise ValueError("scale must be 1, 4 or 16")
    media = "sha256:" + "a" * 64

    def config(parent):
        clips, assets = [], {}
        names = ("app", "video") if parent else ("plate", "placeholder", "clear")
        for index in range(scale):
            for ordinal, name in enumerate(names):
                asset = f"offline-{name}-{index}"
                row = {"id": asset, "at": index * 20 + ordinal * 3,
                       "track": "V1" if parent else "V2", "clipType": "media",
                       "asset": asset, "hold": 3}
                if parent:
                    row["transition"] = {"type": "crossfade", "duration": 0.5,
                                         "params": {"nullable": None,
                                                    "ordered": [False, 0, "", []]}}
                clips.append(row)
                assets[asset] = {"file": asset + ".png", "type": "image/png",
                                 "media_id": media, "content_sha256": media,
                                 "generationId": asset, "variantId": asset}
        return {"clips": clips, "tracks": [
            {"id": "V1" if parent else "V2", "kind": "visual"},
            {"id": "S1" if parent else "plate", "kind": "visual"}],
            "registry": {"assets": assets}, "effects": [], "audio": [],
            "layout": {}, "assets": [],
            "output": {"resolution": "1280x720", "fps": 30, "file": "out.mp4"}}

    parent_config, child_config = config(True), config(False)
    parent = {"slug": "offline", "name": "Offline synthetic shape",
              "config": parent_config, "clips": copy.deepcopy(parent_config["clips"]),
              "registry": copy.deepcopy(parent_config["registry"]),
              "occurrences": [{"occurrence_id": "offline-occ", "shot_id": "offline-shot",
                               "shot_revision_id": "offline-shot-rev",
                               "placement": {"start_ms": 0}, "duration_ms": 12000,
                               "track": "S1"}]}
    shot = {"name": "Offline shot", "internal_timeline_revision_id": "offline-internal",
            "metadata": {}, "items": [], "pools": [], "selected_variants": {},
            "provenance": {}, "generation_inputs": {}, "audio_bindings": [],
            "text_bindings": []}
    shot_image = {"shot_id": "offline-shot", "revision_id": "offline-shot-rev",
                  "internal_timeline_revision_id": "offline-internal",
                  "content_digest": validation.digest(shot), "payload": shot}
    internal_image = {"timeline_id": "offline-timeline", "revision_id": "offline-internal",
                      "content_digest": validation.digest(child_config),
                      "payload": child_config}
    return {"schema_version": 1, "project_id": "offline-project",
            "timeline_id": "offline-timeline",
            "parent_revision": {"revision_id": "offline-parent",
                                "content_digest": validation.digest(parent), "payload": parent},
            "shot_revisions": [shot_image], "internal_timeline_revisions": [internal_image],
            "dependency_manifest": {"shots": [
                {key: value for key, value in shot_image.items() if key != "payload"}],
                "internal_timelines": [
                    {key: value for key, value in internal_image.items() if key != "payload"}],
                "media": [], "documents": []}}


def verify_retained(packet):
    """Use the existing verifier test's authentic, unchanged packet and ancestry."""
    continuations = {}
    entries = {entry["publication_id"]: entry for entry in packet["history"]["items"]}
    cursor = packet["history"]["head"]
    while cursor["publication_id"] != packet["request"]["base_publication_id"]:
        entry = entries[cursor["publication_id"]]
        for record in (entry["records"] or {}).get("commands", []):
            for binding in record["bindings"]:
                if binding.get("key") == "commit.materialization":
                    continuations.setdefault(binding["physical_ref"], set()).add(binding["successor"])
        cursor = entry["previous"]
    proof = auth.validate_sequential_capture(
        packet["request"], packet["prepared"], packet["capture"],
        packet["head_document"], packet["source"], continuations)
    auth.validate(packet["request"], packet["prepared"], packet["head_document"],
                  packet["source"], continuations, sequential=proof)


def profile(call):
    profiler = cProfile.Profile()
    profiler.runcall(call)
    rows = [{"file": Path(entry.code.co_filename).name if isinstance(entry.code, CodeType) else "<builtin>",
             "line": entry.code.co_firstlineno if isinstance(entry.code, CodeType) else 0,
             "function": entry.code.co_name if isinstance(entry.code, CodeType) else entry.code,
             "primitive_calls": entry.callcount - entry.reccallcount, "calls": entry.callcount,
             "self_seconds": entry.inlinetime, "cumulative_seconds": entry.totaltime}
            for entry in profiler.getstats()]
    return {"total_seconds": sum(row["self_seconds"] for row in rows),
            "top_self": sorted(rows, key=lambda row: row["self_seconds"], reverse=True)[:20],
            "top_cumulative": sorted(rows, key=lambda row: row["cumulative_seconds"], reverse=True)[:20]}


def measure(call, repeats):
    start = time.perf_counter()
    call()
    first = time.perf_counter() - start
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        call()
        samples.append(time.perf_counter() - start)
    return {"first_seconds": first, "warm_seconds": samples,
            "warm_median_seconds": statistics.median(samples)}


def run(repeats=3):
    if not 1 <= repeats <= 5:
        raise ValueError("repeats must be between 1 and 5")
    packet = json.loads(CAPTURE.read_text(encoding="utf-8"))
    before = canonical_json(packet)
    validation._validator.cache_clear()
    validation._schema_resources.cache_clear()
    retained = measure(lambda: verify_retained(packet), repeats)
    retained["profile"] = profile(lambda: verify_retained(packet))
    counts = Counter()
    original = validation._validator

    def counted(definition):
        counts[definition] += 1
        return original(definition)

    validation._validator = counted
    try:
        verify_retained(packet)
    finally:
        validation._validator = original
    assert canonical_json(packet) == before
    rows = []
    for scale in (1, 4, 16):
        document = element_document(scale)
        encoded = canonical_json(document)
        for boundaries in (1, 8, 54):
            def checks():
                for _ in range(boundaries):
                    auth._capture_document_images(document)
            def copies():
                for _ in range(boundaries):
                    validation.detached(document)
            rows.append({"scale": scale, "synthetic_boundaries": boundaries,
                         "canonical_bytes": len(encoded.encode()),
                         "parent_clips": 2 * scale, "child_clips": 3 * scale,
                         "validation_and_digests": measure(checks, repeats),
                         "detached": measure(copies, repeats)})
        assert canonical_json(document) == encoded
    return {"status": "UNAPPLIED", "production_changed": False,
            "limits": ["No mounted/provider/Store execution or accepted-history growth replay",
                       "Synthetic shapes/repetition counts are not measured element lifecycle sizes",
                       "First retained call includes cold imports/setup; synthetic calls are warmed",
                       "cProfile overhead is excluded from unprofiled timings",
                       "No before/after product speedup or live dominant-cost claim"],
            "capture_sha256": hashlib.sha256(CAPTURE.read_bytes()).hexdigest(),
            "retained_fixture_file_bytes": CAPTURE.stat().st_size,
            "retained_canonical_bytes": len(before.encode()),
            "retained_commands": len(packet["request"]["commands"]),
            "retained_validation_calls": dict(counts), "retained": retained,
            "synthetic": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=3, choices=range(1, 6))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(args.repeats), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
