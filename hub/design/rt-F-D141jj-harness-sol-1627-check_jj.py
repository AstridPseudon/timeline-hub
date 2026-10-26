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
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CANDIDATE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/candidate")
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
    except (OSError, ValueError) as exc:  # refusal is the expected result for negatives
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


def fixture_source_gate(
    source: dict[str, Any],
    gate: dict[str, Any],
    name: str,
    root: str,
    head: str,
    base: str | None = None,
    gated_tip: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    repo = Path(root)
    base = head if base is None else base
    gated_tip = head if gated_tip is None else gated_tip
    base_tree = git(repo, "rev-parse", f"{base}^{{tree}}")
    gated_tree = git(repo, "rev-parse", f"{gated_tip}^{{tree}}")
    source_value = json.loads(json.dumps(source))
    source_value[name] = {
        "root": root,
        "sha": head,
        "tree": git(repo, "rev-parse", "tl/integration^{tree}"),
    }
    gate_value = json.loads(json.dumps(gate))
    gate_value["repos"][name] = {
        "root": root,
        "base_ref": "origin/main",
        "gate_ref": "tl/integration",
        "upstream_base": base,
        "upstream_base_tree": base_tree,
        "gated_tip": gated_tip,
        "gated_tree": gated_tree,
    }
    return source_value, gate_value


def validate_manifest(path: Path) -> None:
    value = json.loads(path.read_text())
    assert value["candidate_root"] == str(CANDIDATE)
    for entry in value["candidates"]:
        candidate = CANDIDATE / entry["name"]
        assert candidate.stat().st_mode & 0o777 == int(entry["mode"], 8)
        assert digest(candidate.read_bytes()) == entry["sha256"]


def manifest_refusal(work: Path) -> None:
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    manifest["candidates"][0]["sha256"] = "0" * 64
    poisoned = work / "poisoned-source-manifest.json"
    write_json(poisoned, manifest)
    try:
        validate_manifest(poisoned)
    except (AssertionError, KeyError, OSError, ValueError, json.JSONDecodeError):
        print("PASS refusal before candidate writes: stale-source-manifest")
    else:
        raise AssertionError("stale source manifest was accepted")


def finding_refusals(
    caller: Any,
    source: dict[str, Any],
    gate: dict[str, Any],
    builder: Path,
    builder_sha: str,
    work: Path,
) -> None:
    wrapper_spec = importlib.util.spec_from_file_location("d141jj_wrapper", WRAPPER_PATH)
    assert wrapper_spec is not None and wrapper_spec.loader is not None
    wrapper = importlib.util.module_from_spec(wrapper_spec)
    wrapper_spec.loader.exec_module(wrapper)

    def direct_refusal(label: str, operation: Any) -> None:
        try:
            operation()
        except (OSError, ValueError, RuntimeError):
            print(f"PASS refusal before candidate writes: {label}")
        else:
            raise AssertionError(f"{label} was accepted")

    def refusal(
        label: str,
        changed_gate: dict[str, Any],
        changed_source: dict[str, Any] | None = None,
        service_root: Path | None = None,
    ) -> None:
        gpath = work / f"{label}-gate.json"
        spath = work / f"{label}-source.json"
        gsha = write_json(gpath, changed_gate)
        ssha = write_json(spath, changed_source if changed_source is not None else source)
        target = work / f"{label}-receipt.json"
        old_tmp = os.environ.get("TMPDIR")
        if service_root is None:
            service_root = Path(tempfile.mkdtemp(prefix=f"{label}-service-", dir=work))
        os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = str(service_root)
        try:
            failure = invoke(caller, [
                "--source-tuple", str(spath), "--tuple-sha", ssha,
                "--gate-tuple", str(gpath), "--gate-tuple-sha", gsha,
                "--wrapper", str(WRAPPER_PATH), "--wrapper-sha", digest(WRAPPER_PATH.read_bytes()),
                "--builder", str(builder), "--builder-sha", builder_sha,
                "--receipt", str(target), "--", "--private-stub",
            ])
        finally:
            if old_tmp is None:
                os.environ.pop("TMPDIR", None)
                os.environ.pop("TMP", None)
                os.environ.pop("TEMP", None)
            else:
                os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = old_tmp
        assert failure is not None, label
        assert not target.exists(), (label, target)
        print(f"PASS refusal before candidate writes: {label}")

    mismatch_root, mismatch_head = fixture_repo(work, "gate-root-mismatch-low")
    _, mismatch_gate = fixture_source_gate(source, gate, "agent", mismatch_root, mismatch_head)
    refusal("gate-source-root-mismatch-low", mismatch_gate)

    stale_root, stale_base = fixture_repo(work, "stale-upstream-low")
    stale_repo = Path(stale_root)
    (stale_repo / "current.txt").write_text("current origin main\n")
    git_run(stale_repo, "add", "current.txt")
    git_run(stale_repo, "commit", "-q", "-m", "current origin main")
    stale_head = git(stale_repo, "rev-parse", "HEAD")
    git_run(stale_repo, "update-ref", "refs/heads/origin/main", stale_head)
    stale_source, stale_gate = fixture_source_gate(
        source, gate, "agent", stale_root, stale_head, stale_base, stale_base
    )
    direct_refusal(
        "stale-nonapp-upstream-low",
        lambda: wrapper.source_snapshot("agent", stale_gate["repos"]["agent"]),
    )

    wrong_owner_root, wrong_owner_head = fixture_repo(work, "wrong-source-owner-low")
    owner_source, owner_gate = fixture_source_gate(
        source, gate, "agent", wrong_owner_root, wrong_owner_head
    )
    real_euid = caller.os.geteuid
    caller.os.geteuid = lambda: 65534
    try:
        refusal("wrong-source-owner-low", owner_gate, owner_source)
    finally:
        caller.os.geteuid = real_euid

    wrong_mode_root, wrong_mode_head = fixture_repo(work, "wrong-source-mode-low")
    os.chmod(wrong_mode_root, 0o775)
    mode_source, mode_gate = fixture_source_gate(
        source, gate, "agent", wrong_mode_root, wrong_mode_head
    )
    refusal("wrong-source-mode-low", mode_gate, mode_source)

    bad_stage_mode = work / "wrong-stage-mode-low"
    bad_stage_mode.mkdir(mode=0o700)
    os.chmod(bad_stage_mode, 0o775)
    refusal("wrong-stage-mode-low", gate, source, bad_stage_mode)

    bad_stage_owner = work / "wrong-stage-owner-low"
    bad_stage_owner.mkdir(mode=0o700)
    real_euid = caller.os.geteuid
    caller.os.geteuid = lambda: 65534
    try:
        refusal("wrong-stage-owner-low", gate, source, bad_stage_owner)
    finally:
        caller.os.geteuid = real_euid


def main() -> None:
    caller = load_caller()
    before = source_snapshot()
    source, gate, upstream = actual_tuples()
    private_tmp = HERE / "tmp"
    private_tmp.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="d141jj-check-", dir=private_tmp))
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
    service_tmp.mkdir(mode=0o700)
    os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = str(service_tmp)
    receipt = work / "positive-receipt.json"
    if shutil.disk_usage(service_tmp).free < 4_960_000_000:
        validate_manifest(HERE / "source-manifest.json")
        manifest_refusal(work)
        finding_refusals(caller, source, gate, builder, builder_sha, work)
        print(
            "NOT_READY heavy admission: available bytes below enforced "
            "4,960,000,000-byte pre-stage floor; positive staging and inherited "
            "lifecycle controls not executed"
        )
        return
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
    staging = wrapper["staging"]
    assert staging["method"] == "alternates-backed private Git no-checkout worktree"
    assert staging["max_bytes"] == 100_000_000
    assert staging["full_history_copied"] is False
    assert staging["admission_free_bytes"] >= 4_860_000_000 + 100_000_000
    assert staging["measured_bytes"] <= staging["max_bytes"]
    assert staging["free_bytes"] >= 4_860_000_000
    app = wrapper["repos"]["app"]
    assert app["checkout_base"] == APP_BASE
    assert app["applied_tree"] == gate["repos"]["app"]["gated_tree"]
    assert app["fresh_upstream"] == upstream["app"]
    assert app["fresh_upstream"] != APP_BASE
    assert git(Path(app["staged_root"]), "rev-parse", "HEAD^{tree}") == app["applied_tree"]
    for name in REPOS:
        item = wrapper["repos"][name]
        staged = Path(item["staged_root"])
        assert staged.is_dir() and not staged.is_symlink()
        assert staged.resolve().is_relative_to(service_tmp.resolve())
        assert item["staging_method"] == staging["method"]
        assert item["staging_bytes"] <= staging["max_bytes"]
        assert item["free_bytes_after_stage"] >= staging["min_free_after_bytes"]
        alternates = staged / ".git" / "objects" / "info" / "alternates"
        assert alternates.is_file() and not alternates.is_symlink()
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

    validate_manifest(HERE / "source-manifest.json")
    manifest_refusal(work)

    registry_before = REGISTRY.read_bytes()
    installer = subprocess.run(
        [sys.executable, str(INSTALLER_PATH), "--registry", str(REGISTRY),
         "--candidate", str(CANDIDATE / "runtime-final-service-rows.txt"),
         "--builder", "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build"],
        cwd="/", capture_output=True, text=True, check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert installer.returncode == 0, installer.stderr
    assert "no installation requested" in installer.stdout
    assert REGISTRY.read_bytes() == registry_before
    receiving = subprocess.run(
        [sys.executable, str(CANDIDATE / "receiving_controls.py")],
        cwd="/", capture_output=True, text=True, check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert receiving.returncode == 0, receiving.stdout + receiving.stderr
    print("PASS no-install/preimage/outside-four-row/poisoned-caller scoped-CAS controls")

    def refusal(
        label: str,
        changed_gate: dict[str, Any],
        changed_source: dict[str, Any] | None = None,
        service_root: Path | None = None,
    ) -> None:
        gpath = work / f"{label}-gate.json"
        spath = work / f"{label}-source.json"
        gsha = write_json(gpath, changed_gate)
        ssha = write_json(spath, changed_source if changed_source is not None else source)
        target = work / f"{label}-receipt.json"
        old_tmp = os.environ.get("TMPDIR")
        if service_root is None:
            service_root = Path(tempfile.mkdtemp(prefix=f"{label}-service-", dir=work))
        os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = str(service_root)
        try:
            failure = invoke(caller, [
                "--source-tuple", str(spath), "--tuple-sha", ssha,
                "--gate-tuple", str(gpath), "--gate-tuple-sha", gsha,
                "--wrapper", str(WRAPPER_PATH), "--wrapper-sha", digest(WRAPPER_PATH.read_bytes()),
                "--builder", str(builder), "--builder-sha", builder_sha,
                "--receipt", str(target), "--", "--private-stub",
            ])
        finally:
            if old_tmp is None:
                os.environ.pop("TMPDIR", None)
                os.environ.pop("TMP", None)
                os.environ.pop("TEMP", None)
            else:
                os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = old_tmp
        assert failure is not None, label
        assert not target.exists(), (label, target)
        print(f"PASS refusal before candidate writes: {label}")

    mismatch_root, mismatch_head = fixture_repo(work, "gate-root-mismatch")
    _, mismatch_gate = fixture_source_gate(source, gate, "agent", mismatch_root, mismatch_head)
    refusal("gate-source-root-mismatch", mismatch_gate)

    stale_root, stale_base = fixture_repo(work, "stale-upstream")
    stale_repo = Path(stale_root)
    (stale_repo / "current.txt").write_text("current origin main\n")
    git_run(stale_repo, "add", "current.txt")
    git_run(stale_repo, "commit", "-q", "-m", "current origin main")
    stale_head = git(stale_repo, "rev-parse", "HEAD")
    stale_source, stale_gate = fixture_source_gate(
        source, gate, "agent", stale_root, stale_head, stale_base, stale_base
    )
    refusal("stale-nonapp-upstream", stale_gate, stale_source)

    wrong_owner_root, wrong_owner_head = fixture_repo(work, "wrong-source-owner")
    owner_source, owner_gate = fixture_source_gate(
        source, gate, "agent", wrong_owner_root, wrong_owner_head
    )
    real_euid = caller.os.geteuid
    caller.os.geteuid = lambda: 65534
    try:
        refusal("wrong-source-owner", owner_gate, owner_source)
    finally:
        caller.os.geteuid = real_euid

    wrong_mode_root, wrong_mode_head = fixture_repo(work, "wrong-source-mode")
    os.chmod(wrong_mode_root, 0o775)
    mode_source, mode_gate = fixture_source_gate(
        source, gate, "agent", wrong_mode_root, wrong_mode_head
    )
    refusal("wrong-source-mode", mode_gate, mode_source)

    bad_stage_mode = work / "wrong-stage-mode"
    bad_stage_mode.mkdir(mode=0o700)
    os.chmod(bad_stage_mode, 0o775)
    refusal("wrong-stage-mode", gate, source, bad_stage_mode)

    bad_stage_owner = work / "wrong-stage-owner"
    bad_stage_owner.mkdir(mode=0o700)
    real_euid = caller.os.geteuid
    caller.os.geteuid = lambda: 65534
    try:
        refusal("wrong-stage-owner", gate, source, bad_stage_owner)
    finally:
        caller.os.geteuid = real_euid

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
