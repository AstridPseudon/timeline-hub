#!/usr/bin/env python3
"""Consume the existing request-test/test-run binding without creating one.

The controller remains the producer of the receipt, request, service row and
brief.  This file only verifies their exact paths, bytes and source bindings;
it is deliberately not an admission authority or a second request route.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shlex
import sys


FLOOR = 4_714_564_096
SUITE = "agent-core-full"
EXPECTED = {
    "integrated": {
        "agent": ("ecdc242ed9b673f641759ecf029f95e89a2c6f92", "d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735"),
        "runtime": ("95d98f038320d5d46bd679ac000ab3e15825c935", "78df31d62c5b9ba4c84dee4ea346e43a767718c1"),
        "app": ("4de54db14bdc9ddc2ce2e5887258b03acbffd30d", "84c3fb7f73f08c22220f8e808962fe3f24aaa0aa"),
        "composition": ("635f4de06fda22a85fc2e4cfc764d0153a4c9f40", "5ab5191a296980a0a6bcd1178ab6902d6478a148"),
    },
    "pristine": {
        "agent": ("64197afa297f86f1e738238d5e80aff6d33e303a", "6c0488b3efdfa47479b0ad1b7bd20608383be26e"),
        "runtime": ("fa9cd5464a8b37b02f971de375e56be846cd69e2", "124e10dbcd54fb90219e783ec11aa34f8c91590c"),
    },
}


def fail(message: str) -> None:
    raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular(path: str, label: str) -> Path:
    value = Path(path)
    if not value.is_absolute() or value.resolve(strict=True) != value:
        fail(f"{label} path is not an exact absolute path: {path}")
    if not value.is_file():
        fail(f"{label} is not a regular file: {path}")
    return value


def hashed(entry: dict, label: str) -> Path:
    path = regular(entry["path"], label)
    if sha(path) != entry["sha256"]:
        fail(f"{label} hash mismatch")
    return path


def source_tuple(binding: dict, source_manifest: Path) -> None:
    source = json.loads(source_manifest.read_text(encoding="utf-8"))
    actual = source["integrated"]
    for label, (commit, tree) in EXPECTED["integrated"].items():
        row = actual[label]
        if (row["sha"], row["tree"]) != (commit, tree):
            fail(f"integrated {label} tuple mismatch")
    if source["pristine"]["agent"]["sha"] != EXPECTED["pristine"]["agent"][0]:
        fail("pristine Agent tuple mismatch")
    if source["pristine"]["runtime"]["sha"] != EXPECTED["pristine"]["runtime"][0]:
        fail("pristine Runtime tuple mismatch")


def expected_row(binding: dict, mode: str, command: Path, manifest: Path, source_manifest: Path) -> str:
    row = binding["rows"][mode]
    expected = ["agent", SUITE, "/bin/bash", str(command), str(binding["receipt"]["path"]), str(binding["brief"]["path"])]
    if shlex.split(row) != expected:
        fail(f"{mode} service row does not bind command, receipt and brief")
    if row != binding["rows"][mode]:
        fail(f"{mode} service row changed during validation")
    command_binding = binding["commands"][mode]
    if str(command) != command_binding["command"] or sha(command) != command_binding["command_sha256"]:
        fail(f"{mode} command path/hash mismatch")
    if str(manifest) != command_binding["manifest"] or sha(manifest) != command_binding["manifest_sha256"]:
        fail(f"{mode} command manifest path mismatch")
    if (str(source_manifest) != command_binding["source_manifest"]
            or sha(source_manifest) != command_binding["source_manifest_sha256"]):
        fail(f"{mode} source-manifest path mismatch")
    service = hashed(binding["service"][mode], f"{mode} service row")
    if service.read_text(encoding="utf-8").strip() != row:
        fail(f"{mode} service row bytes do not match the bound row")
    return row


def validate(binding_path: str, mode: str, command: str, manifest: str, source_manifest: str,
             *, allow_fixture: bool = False) -> dict:
    binding_file = regular(binding_path, "controller binding")
    binding = json.loads(binding_file.read_text(encoding="utf-8"))
    if binding.get("fixture") and not allow_fixture:
        fail("isolated fixture cannot be used as actual admission")
    if binding.get("suite") != SUITE:
        fail("wrong request-test suite")
    command_path = regular(command, "command")
    manifest_path = regular(manifest, "command manifest")
    source_path = regular(source_manifest, "source manifest")
    source_tuple(binding, source_path)
    request = hashed(binding["request"], "request")
    if binding["request_id"] not in request.read_text(encoding="utf-8"):
        fail("request ID is not present in the bound request")
    receipt = hashed(binding["receipt"], "controller receipt")
    brief = hashed(binding["brief"], "controller brief")
    expected_row(binding, mode, command_path, manifest_path, source_path)
    if binding["service"][mode].get("service_id") != binding["service_id"]:
        fail(f"{mode} service ID binding mismatch")
    record = json.loads(receipt.read_text(encoding="utf-8"))
    witness = record.get("manager_dispatch_witness", {})
    actual = record.get("actual_controller_admission", {})
    if record.get("service_id") != binding["service_id"]:
        fail("service ID differs between receipt and binding")
    if not record.get("controller") or not witness.get("utc"):
        fail("controller receipt lacks dispatch witness")
    if witness.get("comparison") != "PASS" or witness.get("free_bytes", 0) < FLOOR:
        fail("controller dispatch witness is below the D89d floor")
    if witness.get("required_bytes") != FLOOR:
        fail("controller dispatch witness uses the wrong floor")
    if actual.get("comparison") != "PASS" or actual.get("terminal_exit") != 0:
        fail("controller admission did not pass")
    if binding["request"]["path"] != str(request):
        fail("request/service path was retargeted")
    return {
        "mode": mode,
        "suite": SUITE,
        "request_id": binding["request_id"],
        "service_id": binding["service_id"],
        "controller": record["controller"],
        "dispatch_utc": witness["utc"],
        "admitted_bytes": witness["free_bytes"],
        "floor_bytes": FLOOR,
        "request_sha256": binding["request"]["sha256"],
        "service_sha256": binding["service"][mode]["sha256"],
        "receipt_sha256": binding["receipt"]["sha256"],
        "brief_sha256": binding["brief"]["sha256"],
    }


def main() -> None:
    action, *args = sys.argv[1:]
    if action == "consume" and len(args) == 5:
        print(json.dumps(validate(*args), sort_keys=True))
    elif action == "fixture" and len(args) == 5:
        print(json.dumps(validate(*args, allow_fixture=True), sort_keys=True))
    else:
        fail("usage: consume|fixture binding.json cut|pristine command manifest source-manifest")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        sys.exit(78)
