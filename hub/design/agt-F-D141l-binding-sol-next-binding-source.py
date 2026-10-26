#!/usr/bin/env python3
"""Observe native request-test/test-run artifacts without granting admission.

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


# test-run does not hold install_p4_launcher.py's registry lock while it
# resolves BASE_CMD or snapshots, and emits no receipt spanning those events.
# Neither an observation nor a controller-written JSON can supply that custody.
NATIVE_CUSTODY_BLOCKER = (
    "U2-003: bin/request-test queues immediately; bin/test-run resolves the live "
    "row before its optional bench lease and emits snap without resolved row/command "
    "or admission witness; tools/install_p4_launcher.py locks only installers. "
    "No existing native producer binds request, row, admission, snapshot and terminal "
    "under one custody span. Controller-authored JSON is not that producer."
)


def require_native_custody() -> None:
    fail(NATIVE_CUSTODY_BLOCKER)


def shell_fields(path: Path) -> dict[str, str]:
    fields = {}
    for line in path.read_text().splitlines():
        key, sep, raw = line.partition("=")
        values = shlex.split(raw)
        if not sep or key in fields or len(values) != 1:
            fail("malformed native shell fields")
        fields[key] = values[0]
    return fields


def native_identity(d66: str, tests: str, source_manifest: str) -> dict:
    # D66_OUTPUT_DIR is already exported by test-run's snapshot child. It is
    # an identity locator, not an authentication token or an admission receipt.
    path = Path(d66)
    root = Path(tests)
    result = path.parent
    if not path.is_absolute() or path.name != "d66" or result.parent != root:
        fail("D66_OUTPUT_DIR does not locate a native result directory")
    if result.resolve(strict=True) != result:
        fail("native result directory alias")
    service = result.name
    if not re.fullmatch(r"agent-agent-core-full-\d+-\d+", service):
        fail("not a returned agent-core-full service ID")
    request = regular(str(result / "request"), "native request")
    request_fields(request)
    snap = regular(str(result / "snap"), "native snapshot")
    fields = shell_fields(snap)
    source = json.loads(regular(source_manifest, "source manifest").read_text())
    agent = source["integrated"]["agent"]
    if set(fields) != {"tree", "key", "worktree"}:
        fail("native snapshot fields differ")
    if fields["tree"] != agent["tree"] or fields["worktree"] != agent["path"]:
        fail("native snapshot is not the receiving Agent source")
    if not re.fullmatch(r"[0-9a-f]{32}", fields["key"]):
        fail("native snapshot key malformed")
    return {"service_id": service, "result_dir": str(result),
            "request_sha256": sha(request), "snap_sha256": sha(snap),
            "custody_status": "UNPROVEN_NATIVE_ATOMIC_SPAN"}


def inspect_result(result_dir: str, mode: str, command: str, manifest: str,
                   source_manifest: str, run_root: str) -> dict:
    # This is deliberately a terminal readback, never a receipt producer.
    result = Path(result_dir)
    identity = native_identity(str(result / "d66"), str(result.parent), source_manifest)
    service = identity["service_id"]
    status = regular(str(result / "status"), "native status").read_text().strip()
    exit_code = int(regular(str(result / "exit"), "native exit").read_text())
    if status not in {"pass", "fail", "timeout"}:
        fail("native service did not reach a measurement terminal")
    if (status == "pass") != (exit_code == 0) or not 0 <= exit_code <= 255:
        fail("native status/exit disagreement")
    if (status == "timeout") != (exit_code in {124, 137}):
        fail("native timeout/exit disagreement")
    command_file = regular(command, "command")
    source = regular(source_manifest, "source manifest")
    source_tuple(source)
    manifest_file = regular(manifest, "command manifest")
    if manifest_file == source or sha(manifest_file) == sha(source):
        fail("command/source manifests alias")
    expected_cmd = f"/bin/bash {command_file}"
    summary = regular(str(result / "summary"), "native summary").read_text()
    if summary.splitlines()[1:2] != ["cmd: " + expected_cmd]:
        fail("native terminal resolved a different command")
    regular(str(result / "log.txt"), "native log")
    run = Path(run_root)
    fields = shell_fields(regular(str(run / "status.txt"), "command terminal"))
    for name in ("monitor_exit", "source_before_exit", "source_after_exit", "cleanup_exit", "evidence_exit"):
        if fields[name] != "0":
            fail("command custody failed: " + name)
    if fields["body_started"] != "1" or int(fields["runner_exit"]) != exit_code or int(fields["exit"]) != exit_code:
        fail("command/native body result disagreement")
    if fields["state"] != ("PASS" if exit_code == 0 else "FAIL"):
        fail("command state disagrees with measurement")
    # Reuse the original hash/inode/owner/mode seal verifier, not existence tests.
    import importlib.util
    spec = importlib.util.spec_from_file_location("owned_checker", Path(__file__).with_name("check-source.py"))
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    checker.verify_seal(run)
    if mode == "cut":
        launch = run / "launcher-evidence"
        if regular(str(launch / (service + ".request-id")), "launcher ID").read_text() != service + "\n":
            fail("launcher ID differs from returned service ID")
        if regular(str(launch / (service + ".manifest")), "launcher manifest").read_bytes() != manifest_file.read_bytes():
            fail("launcher manifest differs")
        # D73 manifests contain unquoted values; use its native key=value split.
        pins = dict(line.split("=", 1) for line in manifest_file.read_text().splitlines()
                    if line and not line.startswith("#"))
        keys = ("agent_sha", "runtime_sha", "app_sha", "composition_sha",
                "original_p4_test_hash", "service_versions", "junit_paths")
        expected = "".join(key + "=" + pins[key] + "\n" for key in keys)
        if regular(str(launch / (service + ".runmanifest")), "launcher runmanifest").read_text() != expected:
            fail("launcher runmanifest differs from pinned input")
        for suffix, expected_exit in (("preflight.exit", 0), ("body.exit", exit_code)):
            if int(regular(str(launch / (service + "." + suffix)), "launcher exit").read_text()) != expected_exit:
                fail("launcher/native terminal disagreement")
    elif mode != "pristine":
        fail("unknown mode")
    return {**identity, "mode": mode, "test_status": status, "test_exit": exit_code,
            "artifact_checks": "PASS", "admitted": False,
            "command_sha256": sha(command_file), "manifest_sha256": sha(manifest_file),
            "source_manifest_sha256": sha(source)}


def main() -> None:
    action, *args = sys.argv[1:]
    if action in {"admission", "consume", "dispatch-readiness"}:
        require_native_custody()
    elif action == "identity" and len(args) == 3:
        print(native_identity(*args)["service_id"])
    elif action == "inspect-result" and len(args) == 6:
        print(json.dumps(inspect_result(*args), sort_keys=True))
    else:
        fail("usage: dispatch-readiness | identity d66 tests source | inspect-result result mode command manifest source run-root")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        sys.exit(78)
