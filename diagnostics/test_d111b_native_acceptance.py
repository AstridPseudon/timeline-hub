"""Private D111b native acceptance: real provider reads, bytes, and curve."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

WORKER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111b-joined-native-1057")
EVIDENCE = WORKER / "evidence"
BASE_COMMIT = "d23a8e0d2"
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"


def git_value(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phase(runtime: Path, candidate: Path, stage: str, run_id: str, mode: str = "plain") -> dict:
    output = EVIDENCE / run_id
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    production_hashes = {name: sha256(candidate / "runtime_protocol" / name) for name in ("timeline_commit_port.py", "timeline_commit_store.py")}
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
                (package / name).unlink()
                (package / name).write_bytes(source)
            (overlay / "runtime_protocol").unlink()
            (overlay / "runtime_protocol").symlink_to(package, target_is_directory=True)
        (overlay / "sitecustomize.py").symlink_to(Path(__file__).with_name("sitecustomize_d111b.py"))
        app_dist = root / "app-dist"
        app_dist.mkdir(mode=0o700)
        (app_dist / "index.html").write_text("<!doctype html><title>D111b</title>\n", encoding="utf-8")
        env = dict(os.environ)
        env.update({
            "D111B_POINTS": "1" if run_id.startswith("classifier-") else "8",
            "D111B_ENABLED": "1", "D111B_MODE": mode, "D111B_STAGE": stage,
            "D111B_RUN_ID": run_id, "D111B_LOG_DIR": str(output), "D111B_REAL_RUNTIME": str(overlay),
            "ASTRID_RUNTIME_CHECKOUT": str(overlay), "ASTRID_APP_DIRECT_DIST": str(app_dist),
            "ASTRID_CHECKOUT": str(AGENT), "ASTRID_PYTHON": "/home/user/work/venv-agent/bin/python",
            "ASTRID_RUNTIME_PYTHON": "/home/user/work/venv-runtime/bin/python",
            "NODE_PATH": "/home/user/work/app/node_modules", "PYTHONDONTWRITEBYTECODE": "1",
        })
        command = [NODE, "--import", TSX, str(Path(__file__).with_name("measure_d111b_native_acceptance.mjs"))]
        started = time.monotonic()
        completed = subprocess.run(command, cwd="/home/user/work/app", env=env, capture_output=True, text=True, timeout=180, check=False)
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
        assert production_hashes == {name: sha256(candidate / "runtime_protocol" / name) for name in production_hashes}
        result["candidate_source_hashes"] = production_hashes
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
    assert result["metrics"]["sys_setprofile"] is False
    assert result["runtime_stderr_capture"] == "direct"
    stderr = (EVIDENCE / result["run_id"] / "runtime.stderr.log").read_text()
    assert f"D111b startup run={result['run_id']} mode={result['metrics']['mode']}" in stderr
    assert f"D111b refusal tag={result['tagged_refusal']['tag']} status=401" in stderr
    return {
        "run_id": result["run_id"], "mode": result["metrics"]["mode"],
        "request_bytes": [point["request_bytes"] for point in points],
        "canonical_document_bytes": [point["canonical_document_bytes"] for point in points],
        "history_items": [point["history_items"] for point in points],
        "port_read_ns": [sum(read["port_read_ns"] for read in record["reads"]) for record in native],
        "counters": [{key: sum(read.get(key, 0) for read in record["reads"]) for key in
                      ("deepcopy_calls", "deepcopy_bytes", "finite_json_calls", "finite_json_bytes",
                       "detached_calls", "detached_bytes", "store_calls", "store_ns", "source_store_calls", "source_document_calls")}
                     for record in native],
        "entry_calls": [sum(operation["name"] in {"history_entry", "_history_entry_view"}
                            for read in record["reads"] for operation in read["operations"]) for record in native],
        "unique_entries": [len({operation["publication_id"] for read in record["reads"] for operation in read["operations"]
                                if "publication_id" in operation}) for record in native],
    }


def test_plain_inherited_curve() -> None:
    candidate = Path.cwd().resolve()
    result = phase(candidate, candidate, "candidate", f"inherited-{time.time_ns()}")
    packet = summarize(result)
    (EVIDENCE / "inherited-plain.json").write_text(json.dumps(packet, indent=2) + "\n")
    assert packet["port_read_ns"][-1] <= packet["port_read_ns"][0] * 1.5


def test_actual_read_classifier() -> None:
    candidate = Path.cwd().resolve()
    result = phase(candidate, candidate, "baseline", f"classifier-{time.time_ns()}")
    assert len(result["points"]) == 1
    (EVIDENCE / "classifier.json").write_text(json.dumps(result["metrics"], indent=2) + "\n")


def test_d111b_native_acceptance_same_provider_and_curve() -> None:
    candidate = Path.cwd().resolve()
    assert git_value(AGENT, "rev-parse", "HEAD") == "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
    run_id = f"D111b-{time.time_ns()}"
    baseline = phase(candidate, candidate, "baseline", run_id + "-baseline")
    current = phase(candidate, candidate, "candidate", run_id + "-candidate")
    before, after = summarize(baseline), summarize(current)
    packet = {"baseline": before, "candidate": after, "parent": git_value(candidate, "rev-parse", "HEAD"), "candidate_source_hashes": current["candidate_source_hashes"], "baseline_modules": baseline["metrics"]["modules"], "candidate_modules": current["metrics"]["modules"]}
    (EVIDENCE / "growth.json").write_text(json.dumps(packet, indent=2) + "\n")
    assert before["request_bytes"] == after["request_bytes"]
    assert before["canonical_document_bytes"] == after["canonical_document_bytes"]
    assert before["history_items"] == after["history_items"]
    detail = phase(candidate, candidate, "candidate", run_id + "-detail", "detail")
    accounting = phase(candidate, candidate, "candidate", run_id + "-accounting", "accounting")
    packet["detail"] = summarize(detail)
    packet["accounting"] = summarize(accounting)
    packet["overhead_note"] = "Only plain intervals decide acceptance. Detail and accounting use separate, otherwise identical lifecycles; times are not subtracted."
    (EVIDENCE / "growth.json").write_text(json.dumps(packet, indent=2) + "\n")
    assert sum(row["source_store_calls"] for row in packet["detail"]["counters"]) == 0
    assert sum(row["source_document_calls"] for row in packet["detail"]["counters"]) == 0
    assert sum(after["port_read_ns"]) < sum(before["port_read_ns"])
    assert after["port_read_ns"][-1] <= after["port_read_ns"][0] * 1.5
