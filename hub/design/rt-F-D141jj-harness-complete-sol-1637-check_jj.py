"""D141jj source-only acceptance controls.

This check exercises the real candidate caller and D68 successor against the
four read-only integration worktrees with a private stub builder.  Refusal
cases use only tiny private Git fixtures.  It never installs, builds, or
mutates a product worktree or the Runtime registry.
"""

from __future__ import annotations

import hashlib
import contextlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from unittest.mock import patch
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


def fixture_repo(root: Path, name: str) -> tuple[str, str]:
    repo = root / name
    repo.mkdir(mode=0o700)
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
        assert digest(candidate.read_bytes()) == entry["sha256"], f"candidate hash mismatch: {entry['name']}"


def manifest_refusal(work: Path) -> None:
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    manifest["candidates"][0]["sha256"] = "0" * 64
    poisoned = work / "poisoned-source-manifest.json"
    write_json(poisoned, manifest)
    try:
        validate_manifest(poisoned)
    except AssertionError as exc:
        assert str(exc) == "candidate hash mismatch: " + manifest["candidates"][0]["name"]
        print("PASS refusal before candidate writes: stale-source-manifest; phase=validate_manifest; reason=" + str(exc))
    else:
        raise AssertionError("stale source manifest was accepted")


def protected_snapshot() -> dict[str, tuple[str, int]]:
    paths = [CANDIDATE / item["name"] for item in json.loads((HERE / "source-manifest.json").read_text())["candidates"]]
    paths += [CANDIDATE.parent / "source-manifest.json", REGISTRY]
    return {str(path): (digest(path.read_bytes()), path.stat().st_mode & 0o777) for path in paths}


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
    observations = []
    baseline = protected_snapshot()
    mark = Path(os.environ["D141JJ_BUILDER_MARK"])
    mark_before = (mark.read_bytes(), mark.stat().st_mtime_ns, mark.stat().st_ino)

    def refusal(
        label: str,
        changed_gate: dict[str, Any],
        changed_source: dict[str, Any],
        reason: str,
        phase: str,
        *,
        returned: bool = False,
        service_root: Path | None = None,
    ) -> None:
        invocation = Path(tempfile.mkdtemp(prefix=f"{label}-", dir=work))
        service_root = service_root or invocation / "service"
        if not service_root.exists():
            service_root.mkdir(mode=0o700)
        assert not (service_root / "timeline-delivery-KEEP" / "disk-trace.tsv").exists()
        gpath, spath = invocation / "gate.json", invocation / "source.json"
        gsha, ssha = write_json(gpath, changed_gate), write_json(spath, changed_source)
        target = invocation / "receipt.json"
        args = [
            "--source-tuple", str(spath), "--tuple-sha", ssha,
            "--gate-tuple", str(gpath), "--gate-tuple-sha", gsha,
            "--wrapper", str(WRAPPER_PATH), "--wrapper-sha", digest(WRAPPER_PATH.read_bytes()),
            "--builder", str(builder), "--builder-sha", builder_sha,
            "--receipt", str(target), "--", "--private-stub",
        ]
        phases = []

        def observe(name: str, original: Any) -> Any:
            def observed(*args: Any, **kwargs: Any) -> Any:
                event = {"phase": name, "outcome": "entered"}
                phases.append(event)
                try:
                    value = original(*args, **kwargs)
                except ValueError as exc:
                    event.update(outcome="refused", reason=str(exc))
                    raise
                event["outcome"] = "returned"
                return value
            return observed

        code = None
        failure = None
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.dict(os.environ, {name: str(service_root) for name in ("TMPDIR", "TMP", "TEMP")}))
            for name in ("source_identity", "gate_identity", "require_root_binding", "require_app_base", "overlap_identity", "run_wrapper"):
                stack.enter_context(patch.object(caller, name, observe(name, getattr(caller, name))))
            try:
                code = caller.main(args)
            except ValueError as exc:
                failure = str(exc)
        assert phases[-1]["phase"] == phase, (label, phases)
        if returned:
            assert failure is None and code == 2, (label, code, failure)
            assert phases[-1]["outcome"] == "returned", phases
            value = json.loads(target.read_text())
            assert value["status"] == "FAIL" and value["exit"] == code
            d68 = value["wrapper"]["receipt"]
            assert d68["status"] == "FAIL" and d68["error"] == reason, d68
            assert d68["repos"] == {} and "builder_exit" not in d68
            assert list(Path(d68["stage_root"]).iterdir()) == []
            assert "delivery gate refused: " + reason in value["output"]
            lifecycle = json.loads((service_root / "timeline-delivery-KEEP" / "lifecycle.json").read_text())
            assert lifecycle["status"] == "failed" and lifecycle["exit"] == code, lifecycle
            assert lifecycle["trace_status"] == "PASS", lifecycle
            assert all(event["outcome"] == "returned" for event in phases)
        else:
            assert code is None and failure == reason, (label, code, failure, reason)
            assert phases[-1]["outcome"] == "refused", phases
            assert not target.exists(), (label, target)
        assert not list(service_root.rglob("delivery-output")), label
        assert (mark.read_bytes(), mark.stat().st_mtime_ns, mark.stat().st_ino) == mark_before
        assert protected_snapshot() == baseline
        assert not (CANDIDATE / "final-source-tuple.json").exists()
        assert not (CANDIDATE / "final-gate-tuple.json").exists()
        record = {"label": label, "phase": phase, "reason": reason, "returncode": code,
                  "diagnostic_receipt": str(target) if target.exists() else None,
                  "service_root": str(service_root), "phases": phases,
                  "builder_unchanged": True, "protected_sources_unchanged": True}
        observations.append(record)
        write_json(work / "negative-observations.json", observations)
        print(f"PASS refusal before success delivery/candidate/activation writes: {label}; phase={phase}; reason={reason}")

    def direct_stage_refusal(label: str, fixture: Path, detail: str) -> None:
        # Real source validation succeeds before testing the D68-only stage entrypoint.
        invocation = Path(tempfile.mkdtemp(prefix=f"{label}-direct-", dir=work))
        parent = invocation / "stage"
        parent.mkdir(mode=fixture.stat().st_mode & 0o777)
        os.chown(parent, fixture.stat().st_uid, -1)
        reason = f"stage parent {detail}: {parent}"
        spath, gpath = invocation / "source.json", invocation / "gate.json"
        ssha, gsha = write_json(spath, source), write_json(gpath, gate)
        assert caller.source_identity(spath, ssha) == source
        receipt = invocation / "wrapper-receipt.json"
        try:
            wrapper.main([
                "--gate-tuple", str(gpath), "--gate-tuple-sha", gsha,
                "--builder", str(builder), "--builder-sha", builder_sha,
                "--stage-parent", str(parent), "--receipt", str(receipt),
                "--app-upstream-base", APP_BASE, "--app-upstream-tree", APP_BASE_TREE,
                "--", "--private-stub",
            ])
        except wrapper.CandidateError as exc:
            assert str(exc) == reason, (label, str(exc), reason)
        else:
            raise AssertionError(f"{label} direct D68 stage guard accepted")
        assert not receipt.exists() and list(parent.iterdir()) == []
        observations.append({"label": label, "phase": "D68.main/require_directory(stage parent)",
                             "reason": reason, "source_identity_passed": True})
        print(f"PASS direct guard: {label}; phase=D68.main/require_directory(stage parent); reason={reason}")

    mismatch_root, mismatch_head = fixture_repo(work, "gate-root-mismatch")
    _, mismatch_gate = fixture_source_gate(source, gate, "agent", mismatch_root, mismatch_head)
    refusal("gate-source-root-mismatch", mismatch_gate, source,
            "source and gate tuple roots differ for agent", "require_root_binding")

    stale_root, stale_base = fixture_repo(work, "stale-upstream")
    stale_repo = Path(stale_root)
    (stale_repo / "current.txt").write_text("current origin main\n")
    git_run(stale_repo, "add", "current.txt")
    git_run(stale_repo, "commit", "-q", "-m", "current origin main")
    stale_head = git(stale_repo, "rev-parse", "HEAD")
    git_run(stale_repo, "update-ref", "refs/heads/origin/main", stale_head)
    stale_source, stale_gate = fixture_source_gate(
        source, gate, "agent", stale_root, stale_head, stale_base, stale_base
    )
    recorded = stale_gate["repos"]["agent"]["upstream_base"]
    current = git(stale_repo, "rev-parse", "origin/main")
    assert recorded == stale_base and current == stale_head and recorded != current
    assert stale_source["agent"]["sha"] == stale_head
    print(f"STALE fixture before invocation: recorded={recorded} current_origin_main={current} source_sha={stale_source['agent']['sha']}")
    write_json(work / "stale-before-invocation.json", {"recorded": recorded, "current_origin_main": current, "source": stale_source["agent"]})
    refusal("stale-nonapp-upstream", stale_gate, stale_source,
            "agent recorded upstream base is not current origin/main", "run_wrapper", returned=True)

    wrong_owner_root, wrong_owner_head = fixture_repo(work, "wrong-source-owner")
    owner_source, owner_gate = fixture_source_gate(source, gate, "agent", wrong_owner_root, wrong_owner_head)
    assert os.geteuid() == 0, "real private owner fixtures require root; no geteuid patch allowed"
    os.chown(wrong_owner_root, 65534, -1)
    refusal("wrong-source-owner", owner_gate, owner_source,
            f"source tuple root agent owner is not the effective user: {wrong_owner_root}", "source_identity")

    wrong_mode_root, wrong_mode_head = fixture_repo(work, "wrong-source-mode")
    os.chmod(wrong_mode_root, 0o775)
    mode_source, mode_gate = fixture_source_gate(source, gate, "agent", wrong_mode_root, wrong_mode_head)
    refusal("wrong-source-mode", mode_gate, mode_source,
            f"source tuple root agent is writable by another user: {wrong_mode_root}", "source_identity")

    for kind in ("mode", "owner"):
        parent = work / f"wrong-stage-{kind}"
        parent.mkdir(mode=0o700)
        if kind == "mode":
            parent.chmod(0o775)
            detail = "is writable by another user"
        else:
            os.chown(parent, 65534, -1)
            detail = "owner is not the effective user"
        direct_stage_refusal(f"wrong-stage-{kind}", parent, detail)
        refusal(f"wrong-stage-{kind}", gate, source, f"service TMPDIR {detail}: {parent}",
                "run_wrapper", service_root=parent)

    wrong_base = json.loads(json.dumps(gate))
    wrong_base["repos"]["app"]["upstream_base"] = git(REPOS["app"], "rev-parse", "origin/main")
    wrong_base["repos"]["app"]["upstream_base_tree"] = git(REPOS["app"], "rev-parse", "origin/main^{tree}")
    refusal("wrong-app-base", wrong_base, source,
            "App upstream base is not the authorized fc24f849 source", "require_app_base")

    wrong_tree = json.loads(json.dumps(gate))
    wrong_tree["repos"]["app"]["upstream_base_tree"] = "0" * 40
    # The caller's object-tree validation precedes its authorized-tree guard.
    try:
        caller.require_app_base(wrong_tree["repos"])
    except ValueError as exc:
        assert str(exc) == "App upstream base tree is not the authorized faf477ad source"
    else:
        raise AssertionError("wrong authorized App tree accepted")
    observations.append({"label": "wrong-app-tree", "phase": "require_app_base/direct",
                         "reason": "App upstream base tree is not the authorized faf477ad source"})
    refusal("wrong-app-tree", wrong_tree, source,
            "frozen upstream base tree drift for app", "gate_identity")

    dirty_root, dirty_head = fixture_repo(work, "dirty")
    dirty_source, dirty_gate = fixture_source_gate(source, gate, "agent", dirty_root, dirty_head)
    (Path(dirty_root) / "dirty.txt").write_text("uncommitted\n")
    refusal("dirty-source", dirty_gate, dirty_source,
            f"source tuple source is dirty: {dirty_root}", "source_identity")

    symlink_target, symlink_head = fixture_repo(work, "symlink-target")
    symlink_source, symlink_gate = fixture_source_gate(source, gate, "agent", symlink_target, symlink_head)
    symlink = work / "symlink-root"
    symlink.symlink_to(symlink_target, target_is_directory=True)
    symlink_source["agent"]["root"] = str(symlink)
    refusal("symlink-source", symlink_gate, symlink_source,
            "invalid final source tuple identity for agent", "source_identity")

    drift_root, drift_head = fixture_repo(work, "ref-drift")
    drift_repo = Path(drift_root)
    drift_source, drift_gate = fixture_source_gate(source, gate, "agent", drift_root, drift_head)
    (drift_repo / "drift.txt").write_text("ref drift\n")
    git_run(drift_repo, "add", "drift.txt")
    git_run(drift_repo, "commit", "-q", "-m", "drift")
    drift_actual = git(drift_repo, "rev-parse", "HEAD")
    git_run(drift_repo, "update-ref", "refs/heads/tl/integration", drift_actual)
    drift_source["agent"].update(sha=drift_actual, tree=git(drift_repo, "rev-parse", "tl/integration^{tree}"))
    refusal("source-ref-drift", drift_gate, drift_source,
            "frozen gate ref drift for agent", "gate_identity")
    write_json(work / "negative-observations.json", observations)
    assert len([item for item in observations if "returncode" in item]) == 11


def main() -> None:
    caller = load_caller()
    before = source_snapshot()
    source, gate, upstream = actual_tuples()
    private_tmp = HERE / "tmp"
    private_tmp.mkdir(exist_ok=True)
    run_id = uuid.uuid4().hex
    work = Path(tempfile.mkdtemp(prefix=f"d141jj-check-{run_id}-", dir=private_tmp))
    print(f"RUN_ID={run_id} private_work={work}", flush=True)
    protected_before = protected_snapshot()
    source_path = work / "source.json"
    gate_path = work / "gate.json"
    source_sha = write_json(source_path, source)
    gate_sha = write_json(gate_path, gate)

    builder = work / "stub-builder.py"
    builder.write_text(
        "import os\n"
        "from pathlib import Path\n"
        "def main_with_args(args):\n"
        "    with Path(os.environ['D141JJ_BUILDER_MARK']).open('x') as f: f.write('called\\n')\n"
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
    assert shutil.disk_usage(service_tmp).free >= 4_960_000_000, "NOT_READY: pre-stage floor below 4,960,000,000"
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

    finding_refusals(caller, source, gate, builder, builder_sha, work)
    assert protected_snapshot() == protected_before
    validate_manifest(HERE / "source-manifest.json")
    assert source_snapshot() == before
    print("PASS dirty/symlink/source-ref drift refusals leave all four real worktrees unchanged")


if __name__ == "__main__":
    main()
