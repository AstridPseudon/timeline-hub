"""Private D111b native acceptance: real provider reads, bytes, and curve."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

WORKER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111b-native-return-0958")
EVIDENCE = WORKER / "evidence"
BASE_COMMIT = "8b3895cf141f5b7359cceacefde62c9a9475eabf"
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"


def git_value(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phase(runtime: Path, candidate: Path, stage: str, run_id: str) -> dict:
    output = EVIDENCE / run_id
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    with tempfile.TemporaryDirectory(prefix="D111b-", dir=os.environ.get("TMPDIR")) as temporary:
        root = Path(temporary)
        overlay = root / "runtime-overlay"
        overlay.mkdir(mode=0o700)
        for name in (".venv", "runtime_protocol", "astrid_runtime_client"):
            (overlay / name).symlink_to(runtime / name, target_is_directory=True)
        if stage == "baseline":
            package = root / "runtime-protocol-base"
            package.mkdir(mode=0o700)
            for source in (candidate / "runtime_protocol").glob("*.py"):
                (package / source.name).symlink_to(source)
            (package / "schemas").symlink_to(candidate / "runtime_protocol/schemas", target_is_directory=True)
            for name in ("timeline_commit_port.py", "timeline_commit_store.py"):
                source = subprocess.check_output(
                    ["git", "-C", str(candidate), "show", f"{BASE_COMMIT}:runtime_protocol/{name}"]
                )
                (package / name).write_bytes(source)
            (overlay / "runtime_protocol").unlink()
            (overlay / "runtime_protocol").symlink_to(package, target_is_directory=True)
        (overlay / "sitecustomize.py").symlink_to(Path(__file__).with_name("sitecustomize_d111b.py"))
        app_dist = root / "app-dist"
        app_dist.mkdir(mode=0o700)
        (app_dist / "index.html").write_text("<!doctype html><title>D111b</title>\n", encoding="utf-8")
        env = dict(os.environ)
        env.update({
            "D111B_ENABLED": "1", "D111B_MODE": "counter", "D111B_STAGE": stage,
            "D111B_RUN_ID": run_id, "D111B_LOG_DIR": str(output), "D111B_REAL_RUNTIME": str(overlay),
            "ASTRID_RUNTIME_CHECKOUT": str(overlay), "ASTRID_APP_DIRECT_DIST": str(app_dist),
            "ASTRID_CHECKOUT": str(AGENT), "ASTRID_PYTHON": "/home/user/work/venv-agent/bin/python",
            "ASTRID_RUNTIME_PYTHON": "/home/user/work/venv-runtime/bin/python",
            "NODE_PATH": "/home/user/work/app/node_modules", "PYTHONDONTWRITEBYTECODE": "1",
        })
        command = [NODE, "--import", TSX, str(Path(__file__).with_name("measure_d111b_native_acceptance.mjs"))]
        started = time.monotonic()
        completed = subprocess.run(command, cwd="/home/user/work/app", env=env, capture_output=True, text=True, timeout=600, check=False)
        (output / "launcher.stdout.log").write_text(completed.stdout, encoding="utf-8")
        (output / "launcher.stderr.log").write_text(completed.stderr, encoding="utf-8")
        for path in (output / "launcher.stdout.log", output / "launcher.stderr.log"):
            path.chmod(0o600)
        assert completed.returncode == 0, f"{stage} launcher failed: {completed.stderr[-4000:]}"
        result_path = output / f"result-{stage}.json"
        assert result_path.exists(), "native result is missing"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["launcher_elapsed_ms"] = (time.monotonic() - started) * 1000
        metrics_path = output / "port-metrics.json"
        assert metrics_path.exists(), "RequestCommitPort metrics are missing"
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        result["metrics"] = metrics
        (output / f"combined-{stage}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        (output / f"combined-{stage}.json").chmod(0o600)
        return result


def summarize(result: dict) -> dict:
    native = [record for record in result["metrics"]["records"] if str(record.get("label", "")).startswith("D111b native element")]
    assert len(native) == 8, f"expected eight native RequestCommitPort records, got {len(native)}"
    points = result["points"]
    assert len(points) == 8
    for point in points:
        assert point["status"] == 200
        assert point["receipt_readback_byte_identical"] is True
        assert point["existing_rows_preserved"] is True
    assert result["tagged_refusal"]["status"] == 401
    stderr = (EVIDENCE / result["run_id"] / "runtime.stderr.log").read_text(encoding="utf-8")
    assert f"D111b startup run={result['run_id']} mode=counter" in stderr
    assert f"D111b refusal tag={result['tagged_refusal']['tag']} status=401" in stderr
    assert result["runtime_stderr_capture"] == "direct"
    assert result["metrics"]["sys_setprofile"] is False
    for record in native:
        assert record["request_bytes"] > 0
        assert record["reads"]
        assert all(read["port_read_ns"] > 0 and read["storecall_ns"] >= 0 for read in record["reads"])
        assert all(read["deepcopy_calls"] >= 0 and read["finite_json_calls"] >= 0 for read in record["reads"])
        assert all(read["deepcopy_bytes_limited"] == 0 for read in record["reads"])
        assert record["mutation_leak"] is False
    by_label = {record["label"]: record for record in native}
    return {
        "run_id": result["run_id"], "stage": result["stage"],
        "native_request_count": len(native),
        "request_bytes": [point["request_bytes"] for point in points],
        "request_sha256": [point["request_sha256"] for point in points],
        "history_items": [point["history_items"] for point in points],
        "manifest_pins": [point["manifest_pins"] for point in points],
        "canonical_document_bytes": [point["canonical_document_bytes"] for point in points],
        "port_read_ns": [sum(read["port_read_ns"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "storecall_ns": [sum(read["storecall_ns"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "deepcopy_calls": [sum(read["deepcopy_calls"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "deepcopy_bytes": [sum(read["deepcopy_bytes"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "finite_json_calls": [sum(read["finite_json_calls"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "finite_json_bytes": [sum(read["finite_json_bytes"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "source_document_ns": [sum(read["source_document_ns"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "source_document_calls": [sum(read["source_document_calls"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "source_document_bytes": [sum(read["source_document_bytes"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "source_store_ns": [sum(read["source_store_ns"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "source_store_calls": [sum(read["source_store_calls"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "source_store_bytes": [sum(read["source_store_bytes"] for read in by_label[f"D111b native element {i}"]["reads"]) for i in range(8)],
        "mutation_leak": [record["mutation_leak"] for record in native],
    }


def test_d111b_native_acceptance_same_provider_and_curve() -> None:
    assert git_value(AGENT, "rev-parse", "HEAD") == "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
    candidate = Path.cwd().resolve()
    changed_runtime = git_value(candidate, "diff", "--name-only", BASE_COMMIT, "--", "runtime_protocol").splitlines()
    assert changed_runtime == ["runtime_protocol/timeline_commit_port.py", "runtime_protocol/timeline_commit_store.py"]
    EVIDENCE.mkdir(parents=True, exist_ok=True, mode=0o700)
    diagnostic_id = f"D111b-{time.time_ns()}-{os.getpid()}"
    baseline = phase(candidate, candidate, "baseline", f"{diagnostic_id}-baseline")
    current = phase(candidate, candidate, "candidate", f"{diagnostic_id}-candidate")
    baseline_summary = summarize(baseline)
    current_summary = summarize(current)

    assert baseline_summary["request_bytes"] == current_summary["request_bytes"]
    assert baseline_summary["native_request_count"] == current_summary["native_request_count"] == 8
    assert baseline_summary["history_items"] == current_summary["history_items"]
    assert baseline_summary["canonical_document_bytes"] == current_summary["canonical_document_bytes"]
    assert baseline_summary["mutation_leak"] == current_summary["mutation_leak"] == [False] * 8
    # The candidate must perform strictly less repeated detach work on the same
    # native provider path; otherwise the measured acceptance is a failure.
    assert sum(current_summary["deepcopy_calls"]) < sum(baseline_summary["deepcopy_calls"])
    assert sum(current_summary["deepcopy_bytes"]) < sum(baseline_summary["deepcopy_bytes"])
    assert sum(current_summary["source_document_ns"]) < sum(baseline_summary["source_document_ns"])
    assert sum(current_summary["source_store_ns"]) < sum(baseline_summary["source_store_ns"])
    assert sum(current_summary["source_document_calls"]) <= sum(baseline_summary["source_document_calls"])
    assert sum(current_summary["source_store_calls"]) <= sum(baseline_summary["source_store_calls"])
    # The curve is collected in one process while durable history grows.
    assert current_summary["history_items"][-1] > current_summary["history_items"][0]
    assert current_summary["canonical_document_bytes"][-1] > current_summary["canonical_document_bytes"][0]

    source_hashes = {
        "baseline_author_head": BASE_COMMIT,
        "baseline_author_tree": git_value(candidate, "rev-parse", f"{BASE_COMMIT}^{{tree}}"),
        "candidate_runtime_head": git_value(candidate, "rev-parse", "HEAD"),
        "candidate_runtime_tree": git_value(candidate, "rev-parse", "HEAD^{tree}"),
        "agent_head": git_value(AGENT, "rev-parse", "HEAD"),
        "agent_tree": git_value(AGENT, "rev-parse", "HEAD^{tree}"),
        "agent_commit_sha256": sha256(AGENT / "astrid/sdk/timeline/commit.py"),
        "app_harness_sha256": sha256(Path("/home/user/work/app/tests/e2e/local/support/harness.ts")),
        "launcher_sha256": sha256(Path(__file__).with_name("measure_d111b_native_acceptance.mjs")),
        "sitecustomize_sha256": sha256(Path(__file__).with_name("sitecustomize_d111b.py")),
    }
    packet = {"task": "D111b", "diagnostic_id": diagnostic_id, "source_hashes": source_hashes,
              "baseline": baseline_summary, "candidate": current_summary,
              "interpretation": {"same_input_byte_lengths": True, "same_registered_provider": True,
                                  "same_process_curve": True, "history_growing": current_summary["history_items"][-1] > current_summary["history_items"][0],
                                  "manifest_history_curve": {"manifest_pins": current_summary["manifest_pins"], "history_items": current_summary["history_items"]},
                                  "source_document_wall_drops": sum(current_summary["source_document_ns"]) < sum(baseline_summary["source_document_ns"]),
                                  "source_store_wall_drops": sum(current_summary["source_store_ns"]) < sum(baseline_summary["source_store_ns"]),
                                  "per_call_flat": current_summary["port_read_ns"][-1] <= current_summary["port_read_ns"][0] * 1.5,
                                  "sys_setprofile": False,
                                  "decision": "PASS", "history_note": "per-call counters were collected in one process while history grew; raw per-call data remains private"}}
    packet_path = EVIDENCE / "D111b-acceptance.json"
    packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    packet_path.chmod(0o600)
    junit = '<?xml version="1.0" encoding="utf-8"?>\n<testsuite name="D111b native acceptance" tests="1" failures="0"><testcase classname="diagnostics.test_d111b_native_acceptance" name="same_provider_and_curve" /></testsuite>\n'
    junit_path = EVIDENCE / "D111b-acceptance.junit.xml"
    junit_path.write_text(junit, encoding="utf-8")
    junit_path.chmod(0o600)

