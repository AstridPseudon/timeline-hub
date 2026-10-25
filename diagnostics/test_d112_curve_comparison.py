"""One baseline stage for the retained D112 finite native protocol."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
EVIDENCE = ORCH / "workers/rt-D112-curve-return-sol-0907/evidence"
RETAINED = ORCH / "workers/rt-D112-acceptance-return-0850/evidence/finite-curve/run-9233-1792918986781364164/result-candidate-curve.json"
BASELINE = Path("/home/user/work/wt/rt-pin-1daca2a3")
AGENT = Path("/home/user/work/wt/agt-pin-070dfc5e")
APP = Path("/home/user/work/app")
NODE = "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"
TSX = "/home/user/work/app/node_modules/tsx/dist/loader.mjs"
PYTHON = "/home/user/work/venv-runtime/bin/python"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def private_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)


def test_d112_single_baseline_native_curve() -> None:
    if os.environ.get("D112_BASELINE_BODY") != "1":
        attempt = EVIDENCE / f"pytest-{time.time_ns()}"
        attempt.mkdir(parents=True, mode=0o700)
        env = dict(os.environ, D112_BASELINE_BODY="1", PYTHONDONTWRITEBYTECODE="1",
                   TMPDIR=os.environ.get("TMPDIR", "/tmp/w-33ab92340e"))
        xml = attempt / "baseline-pytest.xml"
        completed = subprocess.run(
            [PYTHON, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={xml}", str(Path(__file__).resolve())],
            env=env, capture_output=True, text=True, timeout=950, check=False,
        )
        for name, value in (("pytest.stdout.log", completed.stdout), ("pytest.stderr.log", completed.stderr)):
            destination = attempt / name
            destination.write_text(value, encoding="utf-8")
            destination.chmod(0o600)
        if xml.exists():
            xml.chmod(0o600)
        assert completed.returncode == 0, completed.stdout[-4000:] + completed.stderr[-4000:]
        return
    diagnostics = Path(__file__).resolve().parent
    candidate = diagnostics.parent
    assert git(BASELINE, "rev-parse", "HEAD") == "1daca2a33f6d7b10053e07c539a54843e3984e19"
    assert git(AGENT, "rev-parse", "HEAD") == "070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2"
    assert not git(BASELINE, "status", "--porcelain")
    assert not git(AGENT, "status", "--porcelain")
    assert not git(candidate, "diff", "be828d92cba9200a6ae0ded3a2e968dc3f6ac383", "--",
                   "runtime_protocol/timeline_commit_store.py", "tests/test_timeline_history_state.py")
    for name in ("measure_d112_native_acceptance.mjs", "sitecustomize.py"):
        retained_source = subprocess.check_output(["git", "show", f"b40f8f36b:diagnostics/{name}"])
        assert (diagnostics / name).read_bytes() == retained_source

    # The preceding native body must finish before this one starts.
    predecessor = ORCH / "tests/rt-D111b-native-0905-targeted-1025090933-461/status"
    assert predecessor.read_text().strip() not in {"queued", "running"}
    out = EVIDENCE / f"baseline-{time.time_ns()}"
    out.mkdir(parents=True, mode=0o700)
    child_out = Path(os.environ["TMPDIR"]) / f"d112-baseline-{time.time_ns()}"
    child_out.mkdir(mode=0o700)
    wrapper = diagnostics / "d112_curve_runtime_wrapper.sh"
    env = dict(os.environ)
    env.update({
        "ASTRID_RUNTIME_CHECKOUT": str(BASELINE), "ASTRID_CHECKOUT": str(AGENT),
        "ASTRID_PYTHON": str(wrapper), "ASTRID_RUNTIME_PYTHON": str(wrapper),
        "ASTRID_APP_DIRECT_DIST": str(APP / "dist"), "NODE_PATH": str(APP / "node_modules"),
        "D112_REAL_RUNTIME": str(BASELINE), "D112_STAGE": "baseline-curve", "D112_CURVE": "1",
        "D112_METRIC_PATH": str(child_out / "metrics.json"), "D112_LOG_DIR": str(child_out),
        "ASTRID_APP_DIRECT_DOOR_PORT": str(22000 + os.getpid() % 1000), "PYTHONDONTWRITEBYTECODE": "1",
    })
    import_source = (
        "import hashlib,json,pathlib; import runtime_protocol.timeline_commit_store as s; "
        "import astrid.sdk.timeline.commit as c; "
        "print(json.dumps({m.__name__:{'path':m.__file__,'sha256':hashlib.sha256("
        "pathlib.Path(m.__file__).read_bytes()).hexdigest()} for m in (s,c)}))"
    )
    import_env = dict(env, PYTHONPATH=os.pathsep.join((str(BASELINE), str(AGENT))))
    imports = json.loads(subprocess.check_output([PYTHON, "-c", import_source], cwd=child_out,
                                                env=import_env, text=True))
    assert imports["runtime_protocol.timeline_commit_store"]["path"] == str(BASELINE / "runtime_protocol/timeline_commit_store.py")
    assert imports["astrid.sdk.timeline.commit"]["path"] == str(AGENT / "astrid/sdk/timeline/commit.py")
    composition = AGENT / "remotion/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
    provenance = {
        "baseline": {"commit": git(BASELINE, "rev-parse", "HEAD"), "tree": git(BASELINE, "rev-parse", "HEAD^{tree}")},
        "agent": {"commit": git(AGENT, "rev-parse", "HEAD"), "tree": git(AGENT, "rev-parse", "HEAD^{tree}")},
        "app": {"commit": git(APP, "rev-parse", "HEAD"), "tree": git(APP, "rev-parse", "HEAD^{tree}"),
                "harness_sha256": sha256(APP / "tests/e2e/local/support/harness.ts")},
        "composition": {"commit": "635f4de06fda22a85fc2e4cfc764d0153a4c9f40", "artifact_sha256": sha256(composition)},
        "imports_preflight": imports, "candidate_result_sha256": sha256(RETAINED),
        "launcher_sha256": sha256(diagnostics / "measure_d112_native_acceptance.mjs"),
        "hook_sha256": sha256(diagnostics / "sitecustomize.py"),
        "predecessor_status": predecessor.read_text().strip(),
    }
    private_json(out / "provenance.json", provenance)
    completed = subprocess.run([NODE, "--import", TSX, str(diagnostics / "measure_d112_native_acceptance.mjs")],
                               cwd=APP, env=env, capture_output=True, text=True, timeout=900, check=False)
    for name, value in (("launcher.stdout.log", completed.stdout), ("launcher.stderr.log", completed.stderr)):
        destination = out / name
        destination.write_text(value, encoding="utf-8")
        destination.chmod(0o600)
    for source in child_out.iterdir():
        if source.is_file():
            destination = out / source.name
            shutil.copyfile(source, destination)
            destination.chmod(0o600)
    assert completed.returncode == 0, completed.stderr[-4000:]
    baseline = json.loads((out / "result-baseline-curve.json").read_text())
    retained = json.loads(RETAINED.read_text())
    for result in (baseline, retained):
        assert "error" not in result
        assert result["tagged_refusal"]["status"] == 401
        assert result["curve"]["seed"]["initial_history_items"] == 3
        assert result["curve"]["same_process"] is True
        assert result["curve"]["cache_resets"] == 0
        assert result["curve"]["external_state_changes"] == 3
        assert [row["N"] for row in result["curve"]["rows"]] == [4, 5, 6]
        assert all(row["status"] == 200 and row["receipt"] for row in result["curve"]["rows"])
    private_json(out / "comparison.json", {
        "baseline": baseline["curve"], "retained_candidate": retained["curve"],
        "acceptance": "Existing false flatness flags remain failures; this comparison does not waive them.",
        "measurement_limits": [
            "Fresh native ADD then two SWAP writes, growing history, external SQLite update after each write.",
            "verification_reads later rows span the prior post snapshot through the next sampled snapshot.",
            "external_revalidation_reads also include preceding history and canonical reads.",
            "Signal freshness compares against a caller watermark, which can lag the file's existing snapshot.",
            "Counters therefore cannot isolate per-call verification or prove unexpected identity reopens.",
            "Single instrumented run per source, random identities, growing response bytes, no uninstrumented control.",
        ],
    })
