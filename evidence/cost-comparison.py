"""Finite parent/candidate comparison of the existing retained-capture control."""
from __future__ import annotations

import cProfile
import hashlib
import importlib.util
import json
import os
import pstats
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = "44917baf5976d6a655d582fafc63fde7b6cb242d"
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]

from test_timeline_commit_sequential_verifier import _verify_packet
from test_timeline_validation_cost import FIXTURE, _packet

from runtime_protocol import timeline_commit_validation as validation

parent_source = subprocess.check_output([
    "git", "show", PARENT + ":runtime_protocol/timeline_commit_validation.py"
])
parent_path = Path(os.environ["TMPDIR"]) / "cost-parent-validation.py"
parent_path.write_bytes(parent_source)
spec = importlib.util.spec_from_file_location("runtime_protocol._cost_parent", parent_path)
assert spec is not None and spec.loader is not None
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)
candidate = validation._validator
factories = {"parent": parent._validator, "candidate": candidate}
packet = _packet()
before = json.dumps(packet, sort_keys=True)
samples = {name: [] for name in factories}
profiles = {}

try:
    for name, factory in factories.items():
        validation._validator = factory
        _verify_packet(packet)
    for round_number in range(10):
        order = ("parent", "candidate") if round_number % 2 == 0 else ("candidate", "parent")
        for name in order:
            validation._validator = factories[name]
            cpu, wall = time.process_time(), time.perf_counter()
            for _ in range(3):
                _verify_packet(packet)
            samples[name].append({"cpu": time.process_time() - cpu,
                                  "wall": time.perf_counter() - wall})
    for name, factory in factories.items():
        validation._validator = factory
        profile = cProfile.Profile()
        profile.runcall(_verify_packet, packet)
        stats = pstats.Stats(profile)
        profiles[name] = stats.stats
        profile.dump_stats(str(Path(os.environ["TMPDIR"]) / f"cost-{name}.prof"))
finally:
    validation._validator = candidate

assert json.dumps(packet, sort_keys=True) == before


def checks(stats):
    return {f"{Path(file).name}:{line}:{name}": (primitive, total)
            for (file, line, name), (primitive, total, *_rest) in stats.items()
            if file.endswith(("jsonschema/_keywords.py", "jsonschema/_types.py"))
            or name in {"validate_commit_value", "finite_json", "validate_sequential_capture",
                        "_capture_document_images", "validate_claims"}}


assert checks(profiles["parent"]) == checks(profiles["candidate"])
medians = {name: {clock: statistics.median(s[clock] for s in values)
                  for clock in ("cpu", "wall")} for name, values in samples.items()}
result = {
    "parent_commit": PARENT,
    "parent_source_sha256": hashlib.sha256(parent_source).hexdigest(),
    "candidate_source_sha256": hashlib.sha256(
        (ROOT / "runtime_protocol/timeline_commit_validation.py").read_bytes()).hexdigest(),
    "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
    "schema_bundle_sha256": hashlib.sha256(
        (ROOT / "runtime_protocol/schemas/timeline-commit-bundle.json").read_bytes()).hexdigest(),
    "samples_seconds_per_three_verifications": samples,
    "medians": medians,
    "cpu_reduction_fraction": 1 - medians["candidate"]["cpu"] / medians["parent"]["cpu"],
    "identical_checks_per_verification": checks(profiles["parent"]),
    "validator_constructions": {
        label: sum(total for (_file, _line, name), (_primitive, total, *_rest)
                   in stats.items() if name == "__attrs_post_init__")
        for label, stats in profiles.items()
    },
    "limits": "Existing two-command capture control; no original/service latency or 45s proof.",
}
(ROOT / "evidence/cost-comparison.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in (
    "medians", "cpu_reduction_fraction", "validator_constructions")}, indent=2))
