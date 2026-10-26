"""D141jj source-only acceptance controls.

This check exercises the real candidate caller and D68 successor against the
four read-only integration worktrees with a private stub builder.  Refusal
cases use only tiny private Git fixtures.  It never installs, builds, or
mutates a product worktree or the Runtime registry.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "candidate"
CALLER_PATH = CANDIDATE / "run-final-delivery.py"
INSTALLER_PATH = CANDIDATE / "install-final-services.py"
WRAPPER_PATH = CANDIDATE / "delivery_gate_build.py"
REGISTRY = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
    "/scratchpad/orch/tests/suites.conf"
)
APP_BASE = "fc24f84994dc36cfae9349112782ab4d91dbc73b"
APP_BASE_TREE = "faf477adef3ec24c9cc359486ac16866500ab219"
APP_SUCCESSOR = "eac97ea5"
REPOS = {
    "agent": Path("/home/user/work/agent"),
    "runtime": Path("/home/user/work/runtime"),
    "app": Path("/home/user/work/app"),
    "composition": Path("/home/user/work/composition"),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def git_run(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, stdout=subprocess.DEVNULL)


def load_caller():
    sys.path.insert(0, str(CANDIDATE))
    spec = importlib.util.spec_from_file_location("d141jj_caller", CALLER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("candidate caller could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_snapshot() -> dict[str, tuple[str, str, str, str]]:
    return {
        name: (
            git(root, "status", "--porcelain"),
            git(root, "rev-parse", "HEAD"),
            git(root, "rev-parse", "origin/main"),
            git(root, "rev-parse", "tl/integration"),
        )
        for name, root in REPOS.items()
    }


def actual_tuples() -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    source: dict[str, Any] = {}
    gate: dict[str, Any] = {"version": 1, "repos": {}}
    upstream: dict[str, str] = {}
    for name, root in REPOS.items():
        head = git(root, "rev-parse", "HEAD")
        gate_tip = git(root, "rev-parse", "tl/integration")
        gate_tree = git(root, "rev-parse", "tl/integration^{tree}")
        source[name] = {"root": str(root), "sha": head, "tree": gate_tree}
        if name == "app":
            base = APP_BASE
            base_tree = APP_BASE_TREE
        else:
            base = git(root, "rev-parse", "origin/main")
            base_tree = git(root, "rev-parse", "origin/main^{tree}")
        upstream[name] = git(root, "rev-parse", "origin/main")
        gate["repos"][name] = {
            "root": str(root),
            "base_ref": "origin/main",
            "gate_ref": "tl/integration",
            "upstream_base": base,
            "upstream_base_tree": base_tree,
            "gated_tip": gate_tip,
            "gated_tree": gate_tree,
        }
    return source, gate, upstream


def write_json(path: Path, value: Any) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.write_bytes(raw)
    return digest(raw)


def invoke(caller: Any, args: list[str]) -> BaseException | None:
    try:
        caller.main(args)
    except BaseException as exc:  # refusal is the expected result for negatives
        return exc
    return None


def fixture_repo(root: Path, name: str) -> tuple[str, str]:
    repo = root / name
    repo.mkdir()
    git_run(repo, "init", "-q", "--initial-branch=main")
    git_run(repo, "config", "user.name", "D141jj fixture")
    git_run(repo, "config", "user.email", "d141jj@example.invalid")
    (repo / "fixture.txt").write_text(name + "\n")
    git_run(repo, "add", "fixture.txt")
    git_run(repo, "commit", "-q", "-m", "fixture")
    base = git(repo, "rev-parse", "HEAD")
    git_run(repo, "branch", "origin/main")
    git_run(repo, "branch", "tl/integration")
    return str(repo), base


def main() -> None:
    caller = load_caller()
    before = source_snapshot()
    source, gate, upstream = actual_tuples()
    work = Path(tempfile.mkdtemp(prefix="d141jj-check-", dir=os.environ.get("TMPDIR", "/tmp")))
    source_path = work / "source.json"
    gate_path = work / "gate.json"
    source_sha = write_json(source_path, source)
    gate_sha = write_json(gate_path, gate)

    builder = work / "stub-builder.py"
    builder.write_text(
        "import os\n"
        "from pathlib import Path\n"
        "def main_with_args(args):\n"
        "    Path(os.environ['D141JJ_BUILDER_MARK']).write_text('called\\n')\n"
        "    return 0\n"
    )
    builder_sha = digest(builder.read_bytes())
    caller.REVIEWED_BUILDER_SHA256 = builder_sha
    mark = work / "builder-called"
    os.environ["D141JJ_BUILDER_MARK"] = str(mark)
    service_tmp = work / "service-tmp"
    service_tmp.mkdir()
    os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = str(service_tmp)
    receipt = work / "positive-receipt.json"
    args = [
        "--source-tuple", str(source_path), "--tuple-sha", source_sha,
        "--gate-tuple", str(gate_path), "--gate-tuple-sha", gate_sha,
        "--wrapper", str(WRAPPER_PATH), "--wrapper-sha", digest(WRAPPER_PATH.read_bytes()),
        "--builder", str(builder), "--builder-sha", builder_sha,
        "--receipt", str(receipt), "--", "--private-stub",
    ]
    assert caller.main(args) == 0
    value = json.loads(receipt.read_text())
    assert mark.is_file() and value["status"] == "PASS"
    wrapper = value["wrapper"]["receipt"]
    assert wrapper["status"] == "PASS"
    app = wrapper["repos"]["app"]
    assert app["checkout_base"] == APP_BASE
    assert app["applied_tree"] == gate["repos"]["app"]["gated_tree"]
    assert app["fresh_upstream"] == upstream["app"]
    assert app["fresh_upstream"] != APP_BASE
    assert git(Path(app["staged_root"]), "rev-parse", "HEAD^{tree}") == app["applied_tree"]
    for name in ("agent", "runtime", "composition"):
        item = wrapper["repos"][name]
        assert item["checkout_base"] == upstream[name]
        assert item["fresh_upstream"] == upstream[name]
        assert item["applied_tree"] == gate["repos"][name]["gated_tree"]
    assert not (CANDIDATE / "final-source-tuple.json").exists()
    assert not (CANDIDATE / "final-gate-tuple.json").exists()
    assert APP_SUCCESSOR.encode() not in CALLER_PATH.read_bytes()
    assert source_snapshot() == before
    print("PASS actual caller/D68/stub construction: frozen App fc24/faf477ad applied; later App origin not applied; other3 current tips applied; source refs clean")

    registry_before = REGISTRY.read_bytes()
    installer = subprocess.run(
        [sys.executable, str(INSTALLER_PATH), "--registry", str(REGISTRY),
         "--candidate", str(CANDIDATE / "runtime-final-service-rows.txt"),
         "--builder", "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build"],
        cwd="/", capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert installer.returncode == 0, installer.stderr
    assert "no installation requested" in installer.stdout
    assert REGISTRY.read_bytes() == registry_before
    receiving = subprocess.run(
        [sys.executable, str(CANDIDATE / "receiving_controls.py")],
        cwd="/", capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert receiving.returncode == 0, receiving.stdout + receiving.stderr
    print("PASS no-install/preimage/outside-four-row/poisoned-caller scoped-CAS controls")

    def refusal(label: str, changed_gate: dict[str, Any], changed_source: dict[str, Any] | None = None) -> None:
        gpath = work / f"{label}-gate.json"
        spath = work / f"{label}-source.json"
        gsha = write_json(gpath, changed_gate)
        ssha = write_json(spath, changed_source if changed_source is not None else source)
        target = work / f"{label}-receipt.json"
        failure = invoke(caller, [
            "--source-tuple", str(spath), "--tuple-sha", ssha,
            "--gate-tuple", str(gpath), "--gate-tuple-sha", gsha,
            "--wrapper", str(WRAPPER_PATH), "--wrapper-sha", digest(WRAPPER_PATH.read_bytes()),
            "--builder", str(builder), "--builder-sha", builder_sha,
            "--receipt", str(target), "--", "--private-stub",
        ])
        assert failure is not None, label
        assert not target.exists(), (label, target)
        print(f"PASS refusal before candidate writes: {label}")

    wrong_base = json.loads(json.dumps(gate))
    wrong_base["repos"]["app"]["upstream_base"] = upstream["app"]
    wrong_base["repos"]["app"]["upstream_base_tree"] = git(REPOS["app"], "rev-parse", "origin/main^{tree}")
    refusal("wrong-app-base", wrong_base)

    wrong_tree = json.loads(json.dumps(gate))
    wrong_tree["repos"]["app"]["upstream_base_tree"] = "0" * 40
    refusal("wrong-app-tree", wrong_tree)

    dirty_root, dirty_head = fixture_repo(work, "dirty")
    (Path(dirty_root) / "dirty.txt").write_text("uncommitted\n")
    dirty_source = json.loads(json.dumps(source))
    dirty_source["agent"] = {"root": dirty_root, "sha": dirty_head, "tree": git(Path(dirty_root), "rev-parse", "tl/integration^{tree}")}
    refusal("dirty-source", gate, dirty_source)

    symlink_target, symlink_head = fixture_repo(work, "symlink-target")
    symlink = work / "symlink-root"
    symlink.symlink_to(symlink_target, target_is_directory=True)
    symlink_source = json.loads(json.dumps(source))
    symlink_source["agent"] = {"root": str(symlink), "sha": symlink_head, "tree": git(Path(symlink_target), "rev-parse", "tl/integration^{tree}")}
    refusal("symlink-source", gate, symlink_source)

    drift_root, drift_head = fixture_repo(work, "ref-drift")
    drift_repo = Path(drift_root)
    drift_gate = json.loads(json.dumps(gate))
    drift_gate["repos"]["agent"] = {
        "root": drift_root,
        "base_ref": "origin/main",
        "gate_ref": "tl/integration",
        "upstream_base": drift_head,
        "upstream_base_tree": git(drift_repo, "rev-parse", f"{drift_head}^{{tree}}"),
        "gated_tip": drift_head,
        "gated_tree": git(drift_repo, "rev-parse", f"{drift_head}^{{tree}}"),
    }
    (drift_repo / "drift.txt").write_text("ref drift\n")
    git_run(drift_repo, "add", "drift.txt")
    git_run(drift_repo, "commit", "-q", "-m", "drift")
    drift_actual = git(drift_repo, "rev-parse", "HEAD")
    git_run(drift_repo, "update-ref", "refs/heads/tl/integration", drift_actual)
    refusal("source-ref-drift", drift_gate)
    assert source_snapshot() == before
    print("PASS dirty/symlink/source-ref drift refusals leave all four real worktrees unchanged")


if __name__ == "__main__":
    main()
