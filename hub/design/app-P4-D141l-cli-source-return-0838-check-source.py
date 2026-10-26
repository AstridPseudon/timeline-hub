#!/usr/bin/env python3
"""Author/reviewer-owned source and tiny-launcher checks for D141l P4."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shlex
import stat
import subprocess
import sys


ROOT = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P4-D141l-cli-source-return-0838/evidence")
WORK = ROOT.parent
ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
AGENT = Path("/home/user/work/wt/agt-pin-ecdc242e")
RUNTIME = Path("/home/user/work/wt/rt-pin-95d98f03")
APP = Path("/home/user/work/wt/app-pin-82e9e13d")
COMPOSITION = Path("/home/user/work/wt/vw-pin-635f4de0")
PYTHON = Path("/home/user/work/venv-agent/bin/python")
PROFILE = Path("/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830")
NODE = PROFILE / ".toolchain/node-v20.19.4-linux-x64/bin/node"
SCHEMA = Path("/home/user/work/venv-agent/lib/python3.13/site-packages")
TARGET = AGENT / "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py"
TESTS = [
    TARGET,
    AGENT / "tests/editing_conformance/test_p4_ten_note_v2_runtime.py",
    AGENT / "tests/editing_conformance/test_p4_note_rerun_v2_runtime.py",
]
LAUNCHER = AGENT / "tools/p4-d73-pinned-launch.sh"
INSTALLER = AGENT / "tools/install_p4_launcher.py"
PRODUCTION_MANIFEST = WORK / "operational inputs/p4-d141l-cli-selector.manifest"
PRODUCTION_EVIDENCE = WORK / "operational inputs/body-evidence"
CONTROL_MANIFEST = WORK / "operational inputs/control-positive.manifest"
POISON_MANIFEST = WORK / "operational inputs/control-poison-agent-sha.manifest"
STUB = WORK / "operational inputs/positive-stub.sh"
COUNT = WORK / "control-logs/stub.count"
POSITIVE_LOG = WORK / "control-logs/positive"
POISON_LOG = WORK / "control-logs/poison"
SOURCE_MANIFEST = ROOT / "source-manifest.json"
CANDIDATE_ROW = ROOT / "candidate-row.txt"
CONTROLS = ROOT / "controls.json"

EXPECTED = {
    "agent": ("ecdc242ed9b673f641759ecf029f95e89a2c6f92", "d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735"),
    "runtime": ("95d98f038320d5d46bd679ac000ab3e15825c935", "78df31d62c5b9ba4c84dee4ea346e43a767718c1"),
    "app": ("82e9e13ddf1d7ec6c736521b2eb091dca9877598", "6a6e49eb4461b5ca1a7fa1247653bc794f26d710"),
    "composition": ("635f4de06fda22a85fc2e4cfc764d0153a4c9f40", "5ab5191a296980a0a6bcd1178ab6902d6478a148"),
}
PARENTS = {
    "agent": "ecdc242ed9b673f641759ecf029f95e89a2c6f92 432f9dcbc66fb80b539d9ef709a63ef8065dbc92 00ec0f2f841401b69dad26fb1b23d31cce11efab",
    "runtime": "95d98f038320d5d46bd679ac000ab3e15825c935 857e4c3bce8fd7fc862d7e6e5831e63f24e8cce5 012889c1b0bbfe5f290f757cb6d31dd7d995ccc7",
    "app": "82e9e13ddf1d7ec6c736521b2eb091dca9877598 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 4937203f545a77fa3ca7597493e009c84eebeffa",
    "composition": "635f4de06fda22a85fc2e4cfc764d0153a4c9f40 7a95a40b07ea0d273e17afb69dbc3456b603f2bc c05fdb171fe37c1d5817a060ecb716a329ee821a",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(path: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "--no-optional-locks", "-C", str(path), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def archive_for(profile: Path) -> Path:
    package = json.loads((profile / "package.json").read_text())
    return (profile / package["dependencies"]["@banodoco/timeline-composition"].removeprefix("file:")).resolve()


def base_values(profile: Path) -> dict[str, str]:
    archive = archive_for(profile)
    client_code = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "from astrid_runtime_client.contract_metadata import CONTRACT_VERSION, SCHEMA_DIGEST; "
        "print(CONTRACT_VERSION); print(SCHEMA_DIGEST)"
    )
    client = subprocess.run([str(PYTHON), "-P", "-c", client_code, str(AGENT)], check=True, capture_output=True, text=True).stdout.splitlines()
    composition_version = json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())["version"]
    original_hash = digest_bytes(subprocess.run(["sha256sum", *(str(p) for p in TESTS)], check=True, capture_output=True).stdout)
    values = {
        "format": "p4-d73-v1",
        "agent_sha": EXPECTED["agent"][0],
        "agent_tree": EXPECTED["agent"][1],
        "agent_parents": PARENTS["agent"],
        "agent_path": str(AGENT),
        "runtime_sha": EXPECTED["runtime"][0],
        "runtime_tree": EXPECTED["runtime"][1],
        "runtime_parents": PARENTS["runtime"],
        "runtime_path": str(RUNTIME),
        "app_sha": EXPECTED["app"][0],
        "app_tree": EXPECTED["app"][1],
        "app_parents": PARENTS["app"],
        "app_path": str(APP),
        "composition_sha": EXPECTED["composition"][0],
        "composition_tree": EXPECTED["composition"][1],
        "composition_parents": PARENTS["composition"],
        "composition_path": str(COMPOSITION),
        "python": str(PYTHON),
        "node": str(NODE),
        "profile": str(profile),
        "schema": str(SCHEMA),
        "node_version": subprocess.run([str(NODE), "--version"], check=True, capture_output=True, text=True).stdout.strip(),
        "profile_lock_sha": digest(profile / "package-lock.json"),
        "profile_archive_sha": digest(archive),
        "profile_registry_sha": digest(profile / ".astrid-registry-state.json") if (profile / ".astrid-registry-state.json").exists() else "MISSING:/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.astrid-registry-state.json",
        "composition_version": composition_version,
        "client_version": client[0],
        "schema_digest": client[1],
        "runtime_lock_files": str(len(json.loads((AGENT / "runtime.lock.json").read_text())["files"])),
        "original_p4_test_hash": original_hash,
        "service_versions": f"agent:{EXPECTED['agent'][0]},runtime:{EXPECTED['runtime'][0]},node:{subprocess.run([str(NODE), '--version'], check=True, capture_output=True, text=True).stdout.strip()},composition:{composition_version},client:{client[0]},schema:{client[1]}",
        "junit_paths": str(PRODUCTION_EVIDENCE / "p4-d141l-cli-selector.xml"),
    }
    return values


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_manifest(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(f"{key}={value}\n" for key, value in values.items()), encoding="utf-8")
    os.chmod(path, 0o600)


def source_state() -> dict[str, dict[str, object]]:
    paths = {"agent": AGENT, "runtime": RUNTIME, "app": APP, "composition": COMPOSITION}
    result = {}
    for name, path in paths.items():
        result[name] = {
            "path": str(path),
            "branch": git(path, "branch", "--show-current"),
            "commit": git(path, "rev-parse", "HEAD"),
            "tree": git(path, "rev-parse", "HEAD^{tree}"),
            "parents": git(path, "rev-list", "--parents", "-n", "1", "HEAD"),
            "clean": git(path, "status", "--porcelain", "--untracked-files=all") == "",
        }
    return result


def prepare() -> None:
    state = source_state()
    for name, expected in EXPECTED.items():
        require((state[name]["commit"], state[name]["tree"]) == expected, f"{name} source moved")
        require(state[name]["parents"] == PARENTS[name], f"{name} parents changed")
        require(state[name]["clean"] is True, f"{name} source dirty")
    require(all(state[name]["branch"] == "" for name in EXPECTED), "source worktrees are not detached")
    require(git(AGENT, "diff", "--quiet", "HEAD", "--", str(TARGET.relative_to(AGENT))) == "", "target test changed")
    profile_missing = str(PROFILE / ".astrid-registry-state.json") if not (PROFILE / ".astrid-registry-state.json").exists() else None
    production = base_values(PROFILE)
    control_profile = WORK / "control-logs/control-profile"
    control = base_values(control_profile)
    control["profile"] = str(control_profile)
    control["profile_lock_sha"] = digest(control_profile / "package-lock.json")
    control["profile_archive_sha"] = digest(archive_for(control_profile))
    control["profile_registry_sha"] = digest(control_profile / ".astrid-registry-state.json")
    control["junit_paths"] = str(POSITIVE_LOG / "control.xml")
    write_manifest(PRODUCTION_MANIFEST, production)
    write_manifest(CONTROL_MANIFEST, control)
    poison = dict(control)
    poison["agent_sha"] = "0" * 40
    write_manifest(POISON_MANIFEST, poison)
    SOURCE_MANIFEST.write_text(json.dumps({
        "schema": "timeline.p4.d141l.cli-selector.source-only.v1",
        "status": "SOURCE_READY_PRODUCTION_PROFILE_MISSING",
        "source_only": True,
        "task": "P4 D141l current CLI selector preparation",
        "target": str(TARGET.relative_to(AGENT)) + "::test_cli_sheet_v2_runtime_preserves_document_and_reads_back",
        "actual_source": state,
        "expected_tuple": {name: {"commit": value[0], "tree": value[1], "parents": PARENTS[name]} for name, value in EXPECTED.items()},
        "protected_source": {
            "target_test_sha256": digest(TARGET),
            "target_test_unchanged": True,
            "launcher_sha256": digest(LAUNCHER),
            "installer_sha256": digest(INSTALLER),
            "original_p4_test_hash": production["original_p4_test_hash"],
            "contract": str(ORCH / "design/commit-v2.md"),
        },
        "production_input": {
            "manifest": str(PRODUCTION_MANIFEST),
            "evidence_root": str(PRODUCTION_EVIDENCE),
            "profile": str(PROFILE),
            "supported_input_missing": profile_missing,
            "historical_profile_also_missing": "/home/user/work/runtimes/agent-remotion-v3-819acf-1110",
            "junit_path": production["junit_paths"],
            "manifest_ready_for_controller": profile_missing is None,
        },
        "historical_metadata": {
            "app_expected_pointer": "8585ed9c0404d0187b2ce70242d25114a32747c2",
            "app_expected_pointer_role": "D141v metadata pointer only; not a producer wait and not retargeted",
            "historical_10086": str(ORCH / "design/agt-P4-D141-receipt-return-0159-correction.json"),
            "historical_0114": str(ORCH / "design/agt-P4-D141-result-review-0114-review.json"),
            "historical_0202": str(ORCH / "design/agt-P4-D141-receipt-check-0202-review.json"),
        },
        "receipts": {
            "agent_home": {"path": str(ORCH / "design/agent-U4a-D141-postREG-home-0622.json"), "sha256": digest(ORCH / "design/agent-U4a-D141-postREG-home-0622.json")},
            "app_final_home": {"path": str(ORCH / "design/app-D141w-final-catchup-source-home-0734.json"), "sha256": digest(ORCH / "design/app-D141w-final-catchup-source-home-0734.json")},
            "runtime_applicability": {"path": str(ORCH / "design/rt-P5-D141-ecdc-applicability-0637-source-manifest.json"), "sha256": digest(ORCH / "design/rt-P5-D141-ecdc-applicability-0637-source-manifest.json")},
        },
        "controls": {"manifest": str(CONTROL_MANIFEST), "poison_manifest": str(POISON_MANIFEST), "stub": str(STUB)},
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CANDIDATE_ROW.write_text(
        f"agent p4-current-becfe-http-3legs env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 P4_D73_MANIFEST={shlex.quote(str(PRODUCTION_MANIFEST))} P4_D73_EVIDENCE={shlex.quote(str(PRODUCTION_EVIDENCE))} P4_D73_REQUEST_ID=p4-d141l-cli-selector /bin/bash --noprofile --norc -c 'set -eu; exec {shlex.quote(str(LAUNCHER))} \"$P4_D73_MANIFEST\" run -- -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration --junitxml=\"$P4_D73_EVIDENCE/p4-d141l-cli-selector.xml\" tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back'\n",
        encoding="utf-8",
    )


def run_control(manifest: Path, evidence: Path, request: str, poison: bool) -> tuple[int, int, str]:
    evidence.mkdir(parents=True, exist_ok=True)
    COUNT.write_text("", encoding="utf-8")
    env = os.environ.copy()
    env.update({"P4_D73_EVIDENCE": str(evidence), "P4_D73_REQUEST_ID": request, "P4_STUB_COUNT": str(COUNT)})
    code = f'import os; os.execv("/bin/sh", ["sh", {str(STUB)!r}])'
    result = subprocess.run([str(LAUNCHER), str(manifest), "run", "--", "-c", code], cwd=AGENT, env=env, capture_output=True, text=True)
    count = len(COUNT.read_text(encoding="utf-8").splitlines())
    return result.returncode, count, result.stdout + result.stderr


def check() -> None:
    require(SOURCE_MANIFEST.is_file() and CANDIDATE_ROW.is_file(), "prepared source inputs missing")
    source = json.loads(SOURCE_MANIFEST.read_text())
    state = source_state()
    require(source["actual_source"] == state, "current source differs from prepared readback")
    for name, expected in EXPECTED.items():
        require((state[name]["commit"], state[name]["tree"]) == expected, f"{name} tuple changed")
        require(state[name]["parents"] == PARENTS[name] and state[name]["clean"] is True, f"{name} source not clean")
    require(git(AGENT, "diff", "--quiet", "HEAD", "--", str(TARGET.relative_to(AGENT))) == "", "target test changed")
    require(digest(LAUNCHER) == source["protected_source"]["launcher_sha256"], "launcher changed")
    require(digest(INSTALLER) == source["protected_source"]["installer_sha256"], "installer changed")
    require(digest(TARGET) == source["protected_source"]["target_test_sha256"], "target test hash changed")
    for receipt in source["receipts"].values():
        receipt_path = Path(receipt["path"])
        require(receipt_path.is_file() and digest(receipt_path) == receipt["sha256"], f"source receipt changed: {receipt_path}")
    agent_receipt = json.loads(Path(source["receipts"]["agent_home"]["path"]).read_text())
    require(agent_receipt["head"] == EXPECTED["agent"][0] and agent_receipt["tree"] == EXPECTED["agent"][1], "Agent source receipt tuple")
    require(agent_receipt["parents"] == PARENTS["agent"].split()[1:] and agent_receipt["clean"] is True, "Agent source receipt cleanliness")
    app_receipt = json.loads(Path(source["receipts"]["app_final_home"]["path"]).read_text())
    require(app_receipt["head"] == EXPECTED["app"][0] and app_receipt["tree"] == EXPECTED["app"][1] and app_receipt["clean"] is True, "App source receipt tuple")
    runtime_receipt = json.loads(Path(source["receipts"]["runtime_applicability"]["path"]).read_text())
    runtime_tuple = runtime_receipt["source_tuple"]["runtime"]
    require(runtime_tuple["head"] == EXPECTED["runtime"][0] and runtime_tuple["tree"] == EXPECTED["runtime"][1] and runtime_tuple["clean"] is True, "Runtime source receipt tuple")
    require(PRODUCTION_MANIFEST.resolve() != SOURCE_MANIFEST.resolve(), "input/source manifest alias")
    require(PRODUCTION_EVIDENCE.resolve() != PRODUCTION_MANIFEST.resolve(), "input/evidence alias")
    require(PRODUCTION_MANIFEST.is_file(), "production manifest missing")
    values = dict(line.split("=", 1) for line in PRODUCTION_MANIFEST.read_text().splitlines() if line and not line.startswith("#"))
    require(values["agent_sha"] == EXPECTED["agent"][0] and values["runtime_sha"] == EXPECTED["runtime"][0], "manifest pins are not generated current pins")
    require(values["junit_paths"] == str(PRODUCTION_EVIDENCE / "p4-d141l-cli-selector.xml"), "manifest JUnit path mismatch")
    row = CANDIDATE_ROW.read_text()
    require(row.count("tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back") == 1, "selector not singular")
    require("run -- -m pytest" in row and "-m integration" in row and "--timeout=45" in row and "-p no:cacheprovider" in row, "required pytest argv changed")
    require(f'--junitxml="$P4_D73_EVIDENCE/p4-d141l-cli-selector.xml"' in row, "actual JUnit argv path mismatch")
    require(str(PRODUCTION_MANIFEST) in row and str(PRODUCTION_EVIDENCE) in row, "row paths not durable")
    require(digest(STUB) == "38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0", "positive stub changed")
    subprocess.run(["bash", "-n", str(STUB)], check=True)
    require(CONTROL_MANIFEST.resolve() != POISON_MANIFEST.resolve(), "poison aliases positive")
    require((ROOT / "disk-trace.txt").is_file(), "disk trace missing")
    positive_rc, positive_count, positive_output = run_control(CONTROL_MANIFEST, POSITIVE_LOG, "p4-d141l-control-positive", False)
    require(positive_rc == 17 and positive_count == 1, f"positive control failed rc={positive_rc} calls={positive_count}: {positive_output}")
    poison_rc, poison_count, poison_output = run_control(POISON_MANIFEST, POISON_LOG, "p4-d141l-control-poison", True)
    require(poison_rc != 0 and poison_count == 0 and "agent SHA mismatch" in poison_output, f"poison control failed rc={poison_rc} calls={poison_count}: {poison_output}")
    require((POSITIVE_LOG / "p4-d141l-control-positive.runmanifest").is_file(), "positive runmanifest missing")
    runmanifest = (POSITIVE_LOG / "p4-d141l-control-positive.runmanifest").read_text()
    require(f"junit_paths={POSITIVE_LOG}/control.xml" in runmanifest, "control runmanifest JUnit path mismatch")
    CONTROLS.write_text(json.dumps({
        "schema": "timeline.p4.d141l.cli-selector.controls.v1",
        "status": "PASS_TINY_RUN_MODE_CONTROLS_PRODUCTION_INPUT_MISSING",
        "launcher": {"path": str(LAUNCHER), "sha256": digest(LAUNCHER), "mode": "run"},
        "positive": {"request_id": "p4-d141l-control-positive", "exit_code": positive_rc, "stub_calls": positive_count, "stub_sha256": digest(STUB), "manifest": str(CONTROL_MANIFEST), "runmanifest": str(POSITIVE_LOG / "p4-d141l-control-positive.runmanifest"), "argv_junit": str(POSITIVE_LOG / "control.xml")},
        "poison": {"request_id": "p4-d141l-control-poison", "exit_code": poison_rc, "stub_calls": poison_count, "manifest": str(POISON_MANIFEST), "observed": "D73 launcher: agent SHA mismatch"},
        "boundary": {"pytest": False, "collection": False, "service_request": False, "row_install": False, "production_profile_ready": False},
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("source_status=PASS_CURRENT_TUPLE_CLEAN_TARGET_UNCHANGED")
    print("control_status=PASS_POSITIVE_17_CALL1_POISON_NONZERO_CALL0")
    print("production_status=BLOCKED_PROFILE_REGISTRY_STATE_MISSING")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"prepare", "check"}:
        raise SystemExit("usage: check-source.py prepare|check")
    (prepare if sys.argv[1] == "prepare" else check)()
