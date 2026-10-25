"""Private D112 native acceptance diagnostic; product and protected tests are untouched."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

EVIDENCE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D112-native-acceptance-0827/evidence")
BASELINE = Path("/home/user/work/wt/rt-pin-1daca2a3")
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def run_stage(runtime: Path, stage: str) -> dict:
    out = EVIDENCE / stage
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    env = dict(os.environ)
    env.update({
        "ASTRID_RUNTIME_CHECKOUT": str(runtime), "ASTRID_CHECKOUT": str(AGENT),
        "ASTRID_PYTHON": "/home/user/work/venv-agent/bin/python",
        "ASTRID_RUNTIME_PYTHON": "/home/user/work/venv-runtime/bin/python",
        "ASTRID_APP_DIRECT_DIST": "/home/user/work/app/dist", "NODE_PATH": "/home/user/work/app/node_modules",
        "D112_REAL_RUNTIME": str(runtime), "D112_STAGE": stage, "D112_LOG_DIR": str(out),
        "ASTRID_APP_DIRECT_DOOR_PORT": str(20000 + (os.getpid() % 1000)),
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    launcher = Path(__file__).with_name("measure_d112_native_acceptance.mjs").resolve()
    completed = subprocess.run([NODE, "--import", TSX, str(launcher)],
        cwd="/home/user/work/app", env=env, capture_output=True, text=True, timeout=480)
    (out / "launcher.stdout.log").write_text(completed.stdout, encoding="utf-8")
    (out / "launcher.stderr.log").write_text(completed.stderr, encoding="utf-8")
    for path in (out / "launcher.stdout.log", out / "launcher.stderr.log"):
        path.chmod(0o600)
    assert completed.returncode == 0, f"{stage} launcher failed: {completed.stderr[-4000:]}"
    result_path = out / f"result-{stage}.json"
    assert result_path.exists(), f"{stage} result missing"
    return json.loads(result_path.read_text(encoding="utf-8"))


def test_d112_native_acceptance_baseline_and_candidate() -> None:
    assert git(BASELINE, "rev-parse", "HEAD") == "1daca2a33f6d7b10053e07c539a54843e3984e19"
    assert git(AGENT, "rev-parse", "HEAD") == "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
    candidate = Path.cwd().resolve()
    source_check = subprocess.run(
        ["git", "-C", str(candidate), "diff", "--quiet", "be828d92cba9200a6ae0ded3a2e968dc3f6ac383", "--",
         "runtime_protocol/timeline_commit_store.py", "tests/test_timeline_history_state.py"],
        check=False,
    )
    assert source_check.returncode == 0, "candidate product files differ from frozen be828d source"
    baseline = run_stage(BASELINE, "baseline")
    current = run_stage(candidate, "candidate")
    for result in (baseline, current):
        assert result["tagged_refusal"]["status"] == 401
        assert result["phases"] == ["startup-witness", "tagged-refusal-control", "genuine-registered-provider-seed",
            "native-add-accepted", "native-swap-accepted", "native-undo-accepted"]
        assert result["add_reply"]["receipt_present"] is True
        assert result["swap_reply"]["receipt_present"] is True
        assert result["undo_reply"]["receipt_present"] is True
        assert result["final_controls"]["history_items"] is not None
