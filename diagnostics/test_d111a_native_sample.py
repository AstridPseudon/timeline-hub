"""One bounded, private D111a whole-request native element sample."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

WORKER_EVIDENCE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111a-element-sample-0811/evidence")
RUNTIME = Path("/home/user/work/wt/rt-pin-1daca2a3")
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_value(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def test_d111a_whole_request_native_element_sample() -> None:
    assert git_value(RUNTIME, "rev-parse", "HEAD") == "1daca2a33f6d7b10053e07c539a54843e3984e19"
    assert git_value(AGENT, "rev-parse", "HEAD") == "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
    WORKER_EVIDENCE.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="d111a-", dir=os.environ.get("TMPDIR")) as temp:
        temp_root = Path(temp)
        overlay = temp_root / "runtime-overlay"
        overlay.mkdir(mode=0o700)
        (overlay / ".venv").symlink_to(RUNTIME / ".venv", target_is_directory=True)
        (overlay / "runtime_protocol").symlink_to(RUNTIME / "runtime_protocol", target_is_directory=True)
        (overlay / "astrid_runtime_client").symlink_to(RUNTIME / "astrid_runtime_client", target_is_directory=True)
        (overlay / "sitecustomize.py").symlink_to(Path(__file__).with_name("sitecustomize_d111a.py"))
        output = WORKER_EVIDENCE
        output.mkdir(mode=0o700, exist_ok=True)
        app_dist = temp_root / "app-dist"
        app_dist.mkdir(mode=0o700)
        (app_dist / "index.html").write_text("<!doctype html><title>D111a direct harness</title>\n", encoding="utf-8")
        marker = output / "d111a-request.marker"
        (overlay / "d111a-config.json").write_text(json.dumps({
            "enabled": True, "root": str(output), "marker": str(marker),
            "runtime": str(overlay), "agent": str(AGENT),
        }) + "\n", encoding="utf-8")
        env = dict(os.environ)
        env.update({
            "D111_REAL_RUNTIME": str(overlay),
            "D111_PROFILE": "d111a-native-element",
            "D111_LOG_DIR": str(output),
            "D111A_PROFILE_ROOT": str(output),
            "D111A_REQUEST_MARKER": str(marker),
            "D111A_PROFILE_ENABLED": "1",
            "D111A_SAMPLING_INTERVAL": "0.02",
            "ASTRID_RUNTIME_CHECKOUT": str(overlay),
            "ASTRID_APP_DIRECT_DIST": str(app_dist),
            "ASTRID_CHECKOUT": str(AGENT),
            "ASTRID_PYTHON": "/home/user/work/venv-agent/bin/python",
            "ASTRID_RUNTIME_PYTHON": "/home/user/work/venv-runtime/bin/python",
            "NODE_PATH": "/home/user/work/app/node_modules",
            "PYTHONDONTWRITEBYTECODE": "1",
        })
        command = [NODE, "--import", TSX, str(Path(__file__).with_name("measure_d111a_native_element.mjs"))]
        started = time.monotonic()
        completed = subprocess.run(command, cwd="/home/user/work/app", env=env, capture_output=True, text=True, timeout=480)
        wall_ms = (time.monotonic() - started) * 1000
        (WORKER_EVIDENCE / "d111a-launcher.stdout.log").write_text(completed.stdout, encoding="utf-8")
        (WORKER_EVIDENCE / "d111a-launcher.stderr.log").write_text(completed.stderr, encoding="utf-8")
        for path in (WORKER_EVIDENCE / "d111a-launcher.stdout.log", WORKER_EVIDENCE / "d111a-launcher.stderr.log"):
            os.chmod(path, 0o600)
        result_path = output / "result-d111a-native-element.json"
        assert completed.returncode == 0, f"launcher failed; see {WORKER_EVIDENCE / 'd111a-launcher.stderr.log'}"
        assert result_path.exists(), "native launcher did not produce a result"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        assert result["positive_control"]["status"] == 401
        assert result["reply"]["status"] == 200
        assert result["reply"]["receipt_present"] is True
        assert result["request"]["pid"] == result["runtime_pid"]
        assert result["request"]["elapsed_ms"] > 0
        assert result["profiles"], "runtime profiler did not write a profile"
        assert all(item["sampler_errors"] == [] for item in result["profiles"])
        sampled_profile = next((item for item in result["profiles"] if item["sample_total"] > 0), None)
        assert sampled_profile is not None
        assert sampled_profile["top_inclusive_frames"]
        assert sampled_profile["lost_samples"] >= 0
        checksums = {
            "runtime_head": git_value(RUNTIME, "rev-parse", "HEAD"),
            "runtime_tree": git_value(RUNTIME, "rev-parse", "HEAD^{tree}"),
            "agent_head": git_value(AGENT, "rev-parse", "HEAD"),
            "agent_tree": git_value(AGENT, "rev-parse", "HEAD^{tree}"),
            "runtime_protocol_init_sha256": digest(RUNTIME / "runtime_protocol/__init__.py"),
            "agent_commit_sha256": digest(AGENT / "astrid/sdk/timeline/commit.py"),
            "app_harness_sha256": digest(Path("/home/user/work/app/tests/e2e/local/support/harness.ts")),
            "app_oracle_sha256": digest(Path("/home/user/work/app/tests/e2e/local/support/p2-semantic-oracle.ts")),
            "launcher_sha256": digest(Path(__file__).with_name("measure_d111a_native_element.mjs")),
            "profiler_sha256": digest(Path(__file__).with_name("sitecustomize_d111a.py")),
            "launcher_wall_ms": wall_ms,
        }
        (WORKER_EVIDENCE / "d111a-source-hashes.json").write_text(json.dumps(checksums, indent=2) + "\n", encoding="utf-8")
        os.chmod(WORKER_EVIDENCE / "d111a-source-hashes.json", 0o600)
        junit = f'''<?xml version="1.0" encoding="utf-8"?>\n<testsuite name="D111a native element" tests="1" failures="0" time="{wall_ms / 1000:.6f}"><testcase classname="diagnostics.test_d111a_native_sample" name="whole_request_native_element" time="{wall_ms / 1000:.6f}" /></testsuite>\n'''
        (WORKER_EVIDENCE / "d111a-native-sample.junit.xml").write_text(junit, encoding="utf-8")
        os.chmod(WORKER_EVIDENCE / "d111a-native-sample.junit.xml", 0o600)
