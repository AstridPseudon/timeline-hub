"""Private D112 return controls; no product or protected test source is edited."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

EVIDENCE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D112-acceptance-return-0850/evidence")
BASELINE = Path("/home/user/work/wt/rt-pin-1daca2a3")
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
SOURCE = Path(__file__).parents[1] / "tests" / "test_timeline_history_state.py"
PYTHON = "/home/user/work/venv-runtime/bin/python"
WRAPPER = Path(__file__).with_name("d112_runtime_wrapper.sh").resolve()
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"

CASES = [
    "test_replaced_sqlite_file_reopens_and_fully_verifies_current_state",
    "test_replacing_connection_rebinds_and_fully_verifies",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_controls(runtime: Path, label: str, expected_returncode: int) -> dict:
    out = EVIDENCE / "identity-controls" / label
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    xml = out / "pytest.xml"
    command = [PYTHON, "-m", "pytest", "--import-mode=importlib", "-q", f"--junitxml={xml}"]
    command.extend(f"{SOURCE}::{case}" for case in CASES)
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join((str(runtime), str(runtime / "tests"), str(SOURCE.parent), env.get("PYTHONPATH", "")))
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=runtime, env=env, capture_output=True, text=True, check=False)
    elapsed = time.perf_counter() - started
    for name, value in (("stdout.log", completed.stdout), ("stderr.log", completed.stderr)):
        path = out / name
        path.write_text(value, encoding="utf-8")
        path.chmod(0o600)
    assert completed.returncode == expected_returncode, f"{label} returned {completed.returncode}: {completed.stderr[-2000:]}"
    suite = ET.parse(xml).getroot().find(".//testsuite")
    assert suite is not None
    return {
        "runtime_commit": subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD"], text=True).strip(),
        "runtime_tree": subprocess.check_output(["git", "-C", str(runtime), "write-tree"], text=True).strip(),
        "test_source_sha256": sha256(SOURCE), "returncode": completed.returncode,
        "expected_returncode": expected_returncode, "tests": int(suite.attrib["tests"]),
        "failures": int(suite.attrib.get("failures", "0")), "errors": int(suite.attrib.get("errors", "0")),
        "elapsed_seconds": elapsed,
    }


def test_d112_old_red_new_green_identity_controls() -> None:
    assert SOURCE.read_text(encoding="utf-8")
    baseline = run_controls(BASELINE, "baseline-old-red", expected_returncode=1)
    candidate = run_controls(Path.cwd().resolve(), "candidate-new-green", expected_returncode=0)
    summary = {"control_source_sha256": sha256(SOURCE), "cases": CASES, "baseline": baseline, "candidate": candidate,
               "agent_commit": subprocess.check_output(["git", "-C", str(AGENT), "rev-parse", "HEAD"], text=True).strip()}
    path = EVIDENCE / "identity-controls" / "summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)


def test_d112_curve_source_is_bound_to_frozen_pair() -> None:
    assert subprocess.check_output(["git", "-C", str(AGENT), "rev-parse", "HEAD"], text=True).strip() == "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
    assert subprocess.run(["git", "-C", str(Path.cwd()), "diff", "--quiet", "be828d92cba9200a6ae0ded3a2e968dc3f6ac383", "--", "runtime_protocol/timeline_commit_store.py", "tests/test_timeline_history_state.py"], check=False).returncode == 0


def test_d112_current_candidate_native_curve() -> None:
    out = EVIDENCE / "finite-curve" / f"run-{os.getpid()}-{time.time_ns()}"
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    child_out = Path(os.environ.get("TMPDIR", "/tmp")) / f"d112-curve-{os.getpid()}-{time.time_ns()}"
    child_out.mkdir(parents=True, exist_ok=True, mode=0o700)
    metric = child_out / "metrics.json"
    env = dict(os.environ)
    candidate = Path.cwd().resolve()
    env.update({
        "ASTRID_RUNTIME_CHECKOUT": str(candidate), "ASTRID_CHECKOUT": str(AGENT),
        "ASTRID_PYTHON": str(WRAPPER), "ASTRID_RUNTIME_PYTHON": str(WRAPPER),
        "ASTRID_APP_DIRECT_DIST": "/home/user/work/app/dist", "NODE_PATH": "/home/user/work/app/node_modules",
        "D112_REAL_RUNTIME": str(candidate), "D112_STAGE": "candidate-curve", "D112_CURVE": "1",
        "D112_METRIC_PATH": str(metric), "D112_LOG_DIR": str(child_out),
        "ASTRID_APP_DIRECT_DOOR_PORT": str(21000 + (os.getpid() % 1000)), "PYTHONDONTWRITEBYTECODE": "1",
    })
    launcher = Path(__file__).with_name("measure_d112_native_acceptance.mjs").resolve()
    completed = subprocess.run(
        [NODE, "--import", TSX, str(launcher)], cwd="/home/user/work/app", env=env,
        capture_output=True, text=True, timeout=900, check=False,
    )
    for name, value in (("launcher.stdout.log", completed.stdout), ("launcher.stderr.log", completed.stderr)):
        path = out / name
        path.write_text(value, encoding="utf-8")
        path.chmod(0o600)
    assert completed.returncode == 0, completed.stderr[-4000:]
    for source in child_out.iterdir():
        destination = out / source.name
        if source.is_file():
            shutil.copyfile(source, destination)
            destination.chmod(0o600)
    result_path = child_out / "result-candidate-curve.json"
    assert result_path.exists(), f"curve result missing; stdout={completed.stdout[-2000:]} stderr={completed.stderr[-2000:]}"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert result["phases"][-1] == "current-candidate-finite-curve"
    assert result["curve"]["same_process"] is True
    assert result["curve"]["cache_resets"] == 0
    assert result["curve"]["external_state_changes"] == 3
    assert len(result["curve"]["rows"]) == 3
    assert all(row["status"] == 200 and row["receipt"] for row in result["curve"]["rows"])
    assert all(row["external_revalidation_reads"]["verification_calls"] > 0 for row in result["curve"]["rows"])
