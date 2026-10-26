#!/usr/bin/env python3
"""Authenticate the native request-test/test-run artifacts.

The test-service request is the six-field shell record emitted by
request-test. It is not the Runtime commit-v2 payload, so this consumer does
not invent a second v2 validator or trust flag.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shlex
import sys


FLOOR = 4_714_564_096
SUITE = "agent-core-full"
EXPECTED_INTEGRATED = {
    "agent": ("ecdc242ed9b673f641759ecf029f95e89a2c6f92", "d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735"),
    "runtime": ("95d98f038320d5d46bd679ac000ab3e15825c935", "78df31d62c5b9ba4c84dee4ea346e43a767718c1"),
    "app": ("82e9e13ddf1d7ec6c736521b2eb091dca9877598", "6a6e49eb4461b5ca1a7fa1247653bc794f26d710"),
    "composition": ("635f4de06fda22a85fc2e4cfc764d0153a4c9f40", "5ab5191a296980a0a6bcd1178ab6902d6478a148"),
}
EXPECTED_PRISTINE = {
    "agent": "64197afa297f86f1e738238d5e80aff6d33e303a",
    "runtime": "fa9cd5464a8b37b02f971de375e56be846cd69e2",
}


def fail(message: str) -> None:
    raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or path.resolve(strict=True) != path:
        fail(f"{label} path is not exact absolute: {value}")
    if not path.is_file():
        fail(f"{label} is not a regular file: {value}")
    return path


def hashed(entry: dict, label: str) -> Path:
    path = regular(entry["path"], label)
    if sha(path) != entry["sha256"]:
        fail(f"{label} hash mismatch")
    return path


def request_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        key, sep, encoded = line.partition("=")
        if not sep or key in fields:
            fail("request has malformed or duplicate fields")
        values = shlex.split(encoded)
        if len(values) != 1:
            fail(f"request field is not one shell value: {key}")
        fields[key] = values[0]
    if set(fields) != {"target", "repo", "suite", "files", "nocache", "requested"}:
        fail("request fields differ from request-test")
    if fields["target"] != "integration:agent" or fields["repo"] != "agent":
        fail("request target/repo is not the actual Agent integration target")
    if fields["suite"] != SUITE or fields["files"] != "" or fields["nocache"] != "1":
        fail("request suite/files/nocache differ from the dispatched request")
    if not re.fullmatch(r"20\d\d-\d\d-\d\dT[^ ]+Z", fields["requested"]):
        fail("request timestamp is not request-test output")
    return fields


def source_tuple(source_manifest: Path) -> None:
    data = json.loads(source_manifest.read_text(encoding="utf-8"))
    for label, expected in EXPECTED_INTEGRATED.items():
        row = data["integrated"][label]
        if (row["sha"], row["tree"]) != expected:
            fail(f"integrated {label} tuple mismatch")
    for label, expected in EXPECTED_PRISTINE.items():
        if data["pristine"][label]["sha"] != expected:
            fail(f"pristine {label} tuple mismatch")


def native_row(receipt: dict, mode: str, command: Path, manifest: Path,
               source_manifest: Path, *, live_registry: bool = True) -> tuple[str, Path]:
    row_entry = receipt["registered_row"]
    row_file = hashed(row_entry, f"{mode} registered row")
    row = row_file.read_text(encoding="utf-8")
    expected = f"agent {SUITE} /bin/bash {command} {receipt['path']} {receipt['brief']['path']}\n"
    if row != expected:
        fail(f"{mode} registered row bytes differ from command/receipt/brief")
    registry = regular(row_entry["registry_path"], f"{mode} suite registry")
    registry_text = registry.read_text(encoding="utf-8")
    if live_registry and registry_text.count(row) != 1:
        fail(f"{mode} native suite row is absent or duplicated")
    if live_registry and sha(registry) != row_entry["registry_sha256"]:
        fail(f"{mode} suite registry changed after native row capture")
    command_entry = receipt["command"]
    if command_entry["path"] != str(command) or command_entry["sha256"] != sha(command):
        fail(f"{mode} command path/hash mismatch")
    if command_entry["manifest"] != str(manifest) or command_entry["manifest_sha256"] != sha(manifest):
        fail(f"{mode} command manifest path/hash mismatch")
    if command_entry["source_manifest"] != str(source_manifest) or command_entry["source_manifest_sha256"] != sha(source_manifest):
        fail(f"{mode} source manifest path/hash mismatch")
    return row, registry


def validate_admission(receipt_path: str, brief_path: str, mode: str,
                      command: str, manifest: str, source_manifest: str,
                      *, live_registry: bool = True) -> dict:
    receipt_file = regular(receipt_path, "controller receipt")
    brief_file = regular(brief_path, "owner brief")
    command_file = regular(command, "command")
    manifest_file = regular(manifest, "command manifest")
    source_file = regular(source_manifest, "source manifest")
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
    source_tuple(source_file)
    if receipt["mode"] != mode or receipt["suite"] != SUITE:
        fail("receipt mode/suite mismatch")
    if receipt["admission"]["comparison"] != "PASS" or receipt["admission"]["required_bytes"] != FLOOR:
        fail("dispatch admission witness is not the recorded heavy floor")
    if receipt["admission"]["free_bytes"] < FLOOR:
        fail("dispatch admission is below the recorded heavy floor")
    if receipt["brief"]["path"] != str(brief_file) or receipt["brief"]["sha256"] != sha(brief_file):
        fail("owner brief is not bound to this receipt")
    request_file = hashed(receipt["request"], "request bytes")
    fields = request_fields(request_file)
    service_id = receipt["service_id"]
    if service_id != request_file.parent.name or not re.fullmatch(r"agent-agent-core-full-\d+-\d+", service_id):
        fail("service ID is not the actual request-test result directory")
    if receipt["request_id"] != service_id:
        fail("request ID is not the returned service ID")
    row, registry = native_row(receipt, mode, command_file, manifest_file, source_file,
                                live_registry=live_registry)
    if receipt["registered_row"]["path"] != str(receipt_file.parent / "registered-row.txt"):
        fail("registered row was retargeted")
    brief_text = brief_file.read_text(encoding="utf-8")
    marker = f"service_id={service_id} request_sha256={sha(request_file)} row_sha256={sha(Path(receipt['registered_row']['path']))}"
    if marker not in brief_text:
        fail("immutable brief does not bind service, request and row")
    if receipt["terminal"]["path"] != str(receipt_file.parent / "terminal.json"):
        fail("terminal result was retargeted")
    return {
        "mode": mode,
        "suite": SUITE,
        "request_id": service_id,
        "service_id": service_id,
        "request_sha256": sha(request_file),
        "registered_row_sha256": sha(Path(receipt["registered_row"]["path"])),
        "registry_sha256": sha(registry),
        "receipt_sha256": sha(receipt_file),
        "brief_sha256": sha(brief_file),
        "dispatch_utc": receipt["admission"]["utc"],
        "admitted_bytes": receipt["admission"]["free_bytes"],
        "floor_bytes": FLOOR,
    }


def validate_binding(binding_path: str, mode: str, command: str,
                     manifest: str, source_manifest: str) -> dict:
    binding_file = regular(binding_path, "controller binding")
    binding = json.loads(binding_file.read_text(encoding="utf-8"))
    if binding["mode"] != mode:
        fail("binding mode mismatch")
    hashed(binding["receipt"], "binding receipt")
    hashed(binding["brief"], "binding brief")
    hashed(binding["terminal"], "binding terminal")
    result = validate_admission(
        binding["receipt"]["path"], binding["brief"]["path"], mode,
        command, manifest, source_manifest, live_registry=False,
    )
    terminal = hashed(binding["terminal"], "terminal result")
    terminal_data = json.loads(terminal.read_text(encoding="utf-8"))
    if terminal_data["service_id"] != result["service_id"] or terminal_data["request_id"] != result["request_id"]:
        fail("terminal result is not for the returned service ID")
    if terminal_data["status"] != "pass" or terminal_data["exit"] != 0:
        fail("normal wait-test terminal result did not pass")
    if binding["service_id"] != result["service_id"] or binding["request_id"] != result["request_id"]:
        fail("binding identity differs from authenticated artifacts")
    return {**result, "terminal_sha256": sha(terminal)}


def main() -> None:
    action, *args = sys.argv[1:]
    if action == "admission" and len(args) == 6:
        print(json.dumps(validate_admission(*args), sort_keys=True))
    elif action == "consume" and len(args) == 5:
        print(json.dumps(validate_binding(*args), sort_keys=True))
    else:
        fail("usage: admission receipt brief mode command manifest source-manifest | consume binding mode command manifest source-manifest")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        sys.exit(78)
