"""One bounded private D111asamples diagnostic, with separate observer phases."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

WORKER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111a-sample-custody-sol-0853")
WORKER_EVIDENCE = WORKER / "evidence"
RUNTIME = Path("/home/user/work/wt/rt-pin-1daca2a3")
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_value(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def phase(temp_root, mode, diagnostic_id):
    run_id = f"{diagnostic_id}-{mode}"
    output = WORKER_EVIDENCE / run_id
    output.mkdir(mode=0o700)
    overlay = temp_root / f"runtime-overlay-{mode}"
    overlay.mkdir(mode=0o700)
    for name in (".venv", "runtime_protocol", "astrid_runtime_client"):
        (overlay / name).symlink_to(RUNTIME / name, target_is_directory=True)
    (overlay / "sitecustomize.py").symlink_to(Path(__file__).with_name("sitecustomize_d111a.py"))
    app_dist = temp_root / f"app-dist-{mode}"
    app_dist.mkdir(mode=0o700)
    (app_dist / "index.html").write_text("<!doctype html><title>D111a direct harness</title>\n")
    marker = output / "d111a-request.marker"
    config = {"enabled": True, "root": str(output), "marker": str(marker), "run_id": run_id,
              "runtime": str(overlay), "agent": str(AGENT), "mode": mode}
    (overlay / "d111a-config.json").write_text(json.dumps(config))
    env = dict(os.environ)
    env.update({
        "D111_REAL_RUNTIME": str(overlay), "D111_PROFILE": "D111asamples",
        "D111_LOG_DIR": str(output), "D111A_PROFILE_ROOT": str(output),
        "D111A_REQUEST_MARKER": str(marker), "D111A_RUN_ID": run_id, "D111A_MODE": mode,
        "D111A_SOURCE": "tl/rt-D111a-scope-return-0827",
        "ASTRID_RUNTIME_CHECKOUT": str(overlay), "ASTRID_APP_DIRECT_DIST": str(app_dist),
        "ASTRID_CHECKOUT": str(AGENT), "ASTRID_PYTHON": "/home/user/work/venv-agent/bin/python",
        "ASTRID_RUNTIME_PYTHON": "/home/user/work/venv-runtime/bin/python",
        "NODE_PATH": "/home/user/work/app/node_modules", "PYTHONDONTWRITEBYTECODE": "1",
    })
    command = [NODE, "--import", TSX, str(Path(__file__).with_name("measure_d111a_native_element.mjs"))]
    started = time.monotonic()
    completed = subprocess.run(command, cwd="/home/user/work/app", env=env, capture_output=True, text=True, timeout=480, check=False)
    for name, value in (("stdout", completed.stdout), ("stderr", completed.stderr)):
        path = output / f"d111a-launcher.{name}.log"
        path.write_text(value)
        path.chmod(0o600)
    assert completed.returncode == 0, "launcher failed; private evidence retained"
    result = json.loads((output / "result-D111asamples.json").read_text())
    assert result["run_id"] == run_id
    assert result["positive_control"]["status"] == 401
    assert result["positive_control"]["tag"] == f"d111a-refusal-{run_id}"
    assert result["runtime_stderr_capture"] == "direct"
    stderr = (output / "runtime.stderr.log").read_text()
    assert f"D111asamples startup {mode}" in stderr
    assert f"D111asamples refusal d111a-refusal-{run_id} status=401" in stderr
    assert result["sizes"]["history_items"] >= 1
    assert result["sizes"]["canonical_document_bytes"] > 0
    assert result["reply"]["status"] == 200 and result["reply"]["receipt_present"]
    assert result["request"]["pid"] == result["runtime_pid"]
    assert all(result["correctness"][key] for key in (
        "receipt_result_exact", "canonical_readback_exact", "head_exact", "existing_rows_preserved"))
    assert result["profiles"]
    assert len(result["profiles"]) == 1
    profile = result["profiles"][0]
    assert profile["sampler_errors"] == [] and profile["sys_setprofile"] is False
    assert profile["request_count"] == 1
    measured = profile["requests"][0]
    assert measured["boundary"] == "server._dispatch"
    assert profile["pid"] == result["runtime_pid"]
    assert profile["process_identity"]["birth_ticks"] > 0
    assert measured["end_ns"] > measured["start_ns"]
    assert measured["missing_thread_samples"] == 0
    reply = json.loads((output / "reply.json").read_text())
    canonical = reply["data"]["canonical_document"]
    def canonical_digest(value):
        return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    assert canonical_digest(canonical) == reply["data"]["document_digest"]
    for image in [canonical["parent_revision"], *canonical["shot_revisions"], *canonical["internal_timeline_revisions"]]:
        assert canonical_digest(image["payload"]) == image["content_digest"]
    assert digest(output / "reply.json") == result["correctness"]["reply_sha256"]
    assert (output / "reply.json").stat().st_size == result["correctness"]["reply_bytes"]
    raw = next(output.glob("raw-samples-*.json"))
    assert raw.stat().st_mode & 0o777 == 0o600
    raw_request = json.loads(raw.read_text())[0]
    for sample in raw_request["samples"]:
        assert len(sample["frames"]) == len(set(sample["frames"]))
        assert sample["thread_id"] == measured["thread_id"]
    if mode == "sample":
        assert measured["sample_total"] > 0
        assert 0 <= measured["deepcopy_finite_json_union_frequency"] <= 1
        assert all(row["sample_count"] <= measured["sample_total"] for row in measured["top_inclusive_frames"])
        assert measured["calls"] == {} and measured["accounting_cpu_ns"] == 0
    else:
        assert measured["sample_total"] == 0
        assert set(measured["calls"]) == {"deepcopy", "finite_json", "port_read"}
        assert all(value > 0 for value in measured["outer_calls"].values())
        assert measured["accounting_cpu_ns"] > 0
        for operation, count in measured["outer_calls"].items():
            assert measured["value_summary"][operation]["values_captured"] == count
    hashes = {"runtime_head": git_value(RUNTIME, "rev-parse", "HEAD"),
              "runtime_tree": git_value(RUNTIME, "rev-parse", "HEAD^{tree}"),
              "agent_head": git_value(AGENT, "rev-parse", "HEAD"),
              "agent_tree": git_value(AGENT, "rev-parse", "HEAD^{tree}"),
              "launcher_wall_ms": (time.monotonic() - started) * 1000, "run_id": run_id}
    for root, files in ((RUNTIME, ("runtime_protocol/__init__.py", "runtime_protocol/server.py", "runtime_protocol/timeline_commit_port.py", "runtime_protocol/timeline_commit_validation.py")),
                        (AGENT, ("astrid/sdk/timeline/commit.py",)),
                        (Path("/home/user/work/app"), ("tests/e2e/local/support/harness.ts",)),
                        (Path(__file__).parent, ("sitecustomize_d111a.py", "measure_d111a_native_element.mjs", "test_d111a_native_sample.py"))):
        for file in files:
            hashes[file] = digest(root / file)
    path = output / "D111asamples-source-hashes.json"
    path.write_text(json.dumps(hashes, indent=2) + "\n")
    path.chmod(0o600)
    # Actual immutable artifacts remain private; the summary contains hashes/counts only.
    summary = {"run_id": run_id, "mode": mode, "request": measured,
               "lifecycle": result["lifecycle"], "sizes": result["sizes"], "element_shape": {k: result["element"][k] for k in ("read_count", "command_op", "intent")}, "correctness": result["correctness"],
               "process_identity": profile["process_identity"], "source_hashes": hashes,
               "request_sha256": result["request"]["request_sha256"], "actual_client_request_ms": result["request"]["elapsed_ms"]}
    path = output / "D111asamples-summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n")
    path.chmod(0o600)
    return summary


def test_d111a_whole_request_native_element_sample() -> None:
    assert git_value(RUNTIME, "rev-parse", "HEAD") == "1daca2a33f6d7b10053e07c539a54843e3984e19"
    assert git_value(AGENT, "rev-parse", "HEAD") == "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
    orch = WORKER.parent.parent
    assert (orch / "workers/rt-D112-acceptance-return-0850/ended").exists(), "D112 has not ended"
    assert shutil.disk_usage("/home/user").free > 5_200_000_000, "disk floor"
    for worker in (orch / "workers").iterdir():
        if (worker / "running").exists() and (worker / "meta").exists():
            assert "heavy=1" not in (worker / "meta").read_text(), "Main heavy worker active"
    for suite in (orch / "tests").iterdir():
        if (suite / "heavy").exists() and (suite / "status").exists():
            assert (suite / "status").read_text().strip() not in ("running", "queued"), "Main heavy suite active"
    WORKER_EVIDENCE.mkdir(parents=True, exist_ok=True)
    diagnostic_id = f"D111asamples-{time.time_ns()}-{os.getpid()}"
    with tempfile.TemporaryDirectory(prefix="D111asamples-", dir=os.environ.get("TMPDIR")) as temp:
        sampled = phase(Path(temp), "sample", diagnostic_id)
        counted = phase(Path(temp), "counter", diagnostic_id)
    assert sampled["run_id"] != counted["run_id"]
    assert sampled["element_shape"] == counted["element_shape"]
    for key in ("history_items", "parent_clip_count", "shot_revision_count", "internal_timeline_revision_count"):
        assert sampled["sizes"][key] == counted["sizes"][key]
    wall = sampled["request"]
    summary = {"diagnostic_id": diagnostic_id, "sample_phase": sampled, "counter_phase": counted,
               "sample_union_majority": "YES" if wall["deepcopy_finite_json_union_frequency"] > 0.5 else "NO",
               "production_wall_causal_majority": "UNKNOWN",
               "limits": "Independent freshly seeded lifecycles, same provider/shape/operation count; IDs differ. No cache resets, no replay of an accepted key. Counter phase never used as production wall. Sampling estimates occupancy, not causal savings; no optimization applied."}
    path = WORKER_EVIDENCE / "D111asamples.json"
    path.write_text(json.dumps(summary, indent=2) + "\n")
    path.chmod(0o600)
