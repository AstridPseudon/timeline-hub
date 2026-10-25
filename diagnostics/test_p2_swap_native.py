"""Private P2 SWAP replay diagnostic; product sources remain untouched."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

EVIDENCE = Path(os.environ.get("D66_OUTPUT_DIR", "/tmp/p2-swap-native-evidence"))
APP = Path("/home/user/banodoco/reigh-app")
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
COMPOSITION = Path("/home/user/peteromallet/timeline-composition")
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"
APP_COMMIT = "96d4754b4eef0591a208d6b51b60c30fc44b6915"
AGENT_COMMIT = "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
COMPOSITION_COMMIT = "635f4de06fda22a85fc2e4cfc764d0153a4c9f40"
APP_SOURCE_HASHES = {
    "tests/e2e/local/three-products.mounted-readiness.spec.ts": "2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593",
    "tests/e2e/local/three-products.p2-elements-assets.spec.ts": "7cca78274f96c9466d82bea3108f6f8a447462c9cd722c078ab958bc3578d637",
    "tests/e2e/local/three-products.p2-popup.spec.ts": "09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9",
    "tests/e2e/local/three-products.p2-tour.spec.ts": "54ea18f3f3fa8fef2eb31cc0a05809ede76099f9f3bee9bf0511824e652a85f7",
}


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def source_hash(path: Path, commit: str, relative: str) -> str:
    data = subprocess.check_output(["git", "-C", str(path), "show", f"{commit}:{relative}"])
    return hashlib.sha256(data).hexdigest()


def preflight() -> dict:
    assert git(APP, "cat-file", "-t", APP_COMMIT) == "commit"
    assert git(AGENT, "rev-parse", "HEAD") == AGENT_COMMIT
    assert git(COMPOSITION, "rev-parse", COMPOSITION_COMMIT) == COMPOSITION_COMMIT
    assert git(APP, "status", "--porcelain") == ""
    assert git(AGENT, "status", "--porcelain") == ""
    assert git(COMPOSITION, "status", "--porcelain") == ""
    actual_hashes = {name: source_hash(APP, APP_COMMIT, name) for name in APP_SOURCE_HASHES}
    assert actual_hashes == APP_SOURCE_HASHES
    return {
        "runtime_commit": git(Path.cwd(), "rev-parse", "HEAD"),
        "runtime_tree": git(Path.cwd(), "rev-parse", "HEAD^{tree}"),
        "app_commit": APP_COMMIT,
        "app_tree": git(APP, "rev-parse", f"{APP_COMMIT}^{{tree}}"),
        "agent_commit": AGENT_COMMIT,
        "agent_tree": git(AGENT, "rev-parse", "HEAD^{tree}"),
        "composition_commit": COMPOSITION_COMMIT,
        "composition_tree": git(COMPOSITION, "rev-parse", "HEAD^{tree}"),
        "app_source_hashes": actual_hashes,
        "recorded_runtime": {
            "commit": "d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e",
            "tree": "6283b5fbb128447f1b333e0e6af334d35637cf69",
        },
        "recorded_app_tuple": {
            "app": "96d4754b4eef0591a208d6b51b60c30fc44b6915",
            "agent": "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2",
            "runtime": "d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e",
            "composition": "635f4de06fda22a85fc2e4cfc764d0153a4c9f40",
        },
    }


def test_p2_swap_native_replay_and_d112_control() -> None:
    source_identity = preflight()
    EVIDENCE.mkdir(parents=True, exist_ok=True, mode=0o700)
    started = time.monotonic()
    env = dict(os.environ)
    env.update({
        "P2_SWAP_EVIDENCE": str(EVIDENCE),
        "P2_SWAP_RUNTIME": str(Path.cwd().resolve()),
        "P2_SWAP_AGENT": str(AGENT),
        "P2_SWAP_SOURCE_IDENTITY": json.dumps(source_identity, separators=(",", ":")),
        "ASTRID_RUNTIME_CHECKOUT": str(Path.cwd().resolve()),
        "ASTRID_CHECKOUT": str(AGENT),
        "ASTRID_PYTHON": "/home/user/work/venv-agent/bin/python",
        "ASTRID_RUNTIME_PYTHON": "/home/user/work/venv-runtime/bin/python",
        "ASTRID_APP_DIRECT_DIST": "/home/user/work/app/dist",
        "ASTRID_APP_DIRECT_DOOR_PORT": str(20000 + (os.getpid() % 1000)),
        "PYTHONDONTWRITEBYTECODE": "1",
        "NODE_PATH": "/home/user/work/app/node_modules",
    })
    launcher = Path(__file__).with_name("measure_p2_swap_native.mjs").resolve()
    completed = subprocess.run(
        [NODE, "--import", TSX, str(launcher)],
        cwd="/home/user/work/app",
        env=env,
        capture_output=True,
        text=True,
        timeout=1_800,
        check=False,
    )
    for name, value in (("launcher.stdout.log", completed.stdout), ("launcher.stderr.log", completed.stderr)):
        target = EVIDENCE / name
        target.write_text(value, encoding="utf-8")
        target.chmod(0o600)
    assert completed.returncode == 0, f"stdout={completed.stdout[-4000:]} stderr={completed.stderr[-4000:]}"
    result_path = EVIDENCE / "result-p2-swap-native.json"
    assert result_path.exists()
    result = json.loads(result_path.read_text(encoding="utf-8"))
    result["source_identity"] = source_identity
    result["wall_seconds"] = round(time.monotonic() - started, 3)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    result_path.chmod(0o600)
    assert result["preflight"] == "PASS"
    assert result["d112_positive"]["swap"]["status"] == 200
    assert result["d112_positive"]["undo"]["status"] == 200
    assert result["app_replay"]["fork"]["generated"] is True
    assert result["app_replay"]["request"]["status"] == 409
    assert result["app_replay"]["swap"]["status"] == 409
    assert result["app_replay"]["swap"]["reason"] == "dependency_changed"
    assert result["comparison"]["recorded_app_reason"] == "history_unavailable"
    assert result["comparison"]["observed_replay_reason"] == "dependency_changed"
    assert result["app_replay"]["swap"]["diagnostic_reason"] is None
    assert result["app_replay"]["stderr_bytes"] == 0
    assert result["app_replay"]["stderr_bytes"] >= 0
    assert result["comparison"]["difference"]
