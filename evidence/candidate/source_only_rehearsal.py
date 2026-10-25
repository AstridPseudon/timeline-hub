"""Apply the frozen D108 source delta on the approved fresh upstream tips.

This is the source-only half of the reviewed D68 route.  It imports the retained
D68 staging callable, gives it private object-only views of the existing clones,
and deliberately stops before any delivery builder, render, package, or live
service work.  The source clones and all integration checkouts are inspected
before and after and are never changed by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REPOS = ("agent", "runtime", "app", "composition")
SOURCE_CLONES = {
    "agent": Path("/home/user/peteromallet/astrid-agent"),
    "runtime": Path("/home/user/banodoco/banodoco-workspace-runtime"),
    "app": Path("/home/user/banodoco/reigh-app"),
    "composition": Path("/home/user/peteromallet/timeline-composition"),
}
INTEGRATION_ROOTS = {
    "agent": Path("/home/user/work/agent"),
    "runtime": Path("/home/user/work/runtime"),
    "app": Path("/home/user/work/app"),
    "composition": Path("/home/user/work/composition"),
}
CAPTURED = {
    "agent": "d6294843286c18e57af3c1874cf1996be42212d2",
    "runtime": "1daca2a33f6d7b10053e07c539a54843e3984e19",
    "app": "0b6cee269f32079c5446036bbca8a484176799bc",
    "composition": "635f4de06fda22a85fc2e4cfc764d0153a4c9f40",
}
UPSTREAM_BASE = {
    "agent": "92443771676ef2bbb547d0a103d708fa8bec4c63",
    "runtime": "d4f496ec4fbcae7a1f3a51d47ed5147c561117ad",
    "app": "3881e9440688f774878e18806da2dc5c993a9b00",
    "composition": "67b8aa3d0d6831d3e3504a340ff583c3da253707",
}
FRESH_UPSTREAM = {
    "agent": "08e6b905114a3ee2b05c3e7980421f26b4abf15c",
    "runtime": "d4f496ec4fbcae7a1f3a51d47ed5147c561117ad",
    "app": "d11417a59b5edbb617e0311212b79069620538a7",
    "composition": "67b8aa3d0d6831d3e3504a340ff583c3da253707",
}
D68_WRAPPER = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
    "/workers/rt-F-final-D68-review-1554/evidence/delivery_gate_build.py"
)
D68_WRAPPER_SHA256 = "bae840fad6ea496457a3d6138609ce9d89b0b10825827c94f855257bce6c6779"
SHA256 = re.compile(r"^[0-9a-f]{40}$")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(root: Path, *args: str, input_data: bytes | None = None) -> str:
    env = os.environ.copy()
    env.update(
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_CONFIG_SYSTEM="/dev/null",
        GIT_CONFIG_NOSYSTEM="1",
        GIT_OPTIONAL_LOCKS="0",
        GIT_TERMINAL_PROMPT="0",
    )
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            input=input_data,
            capture_output=True,
            check=True,
            env=env,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        output = b""
        if isinstance(exc, subprocess.CalledProcessError):
            output = exc.stderr or exc.stdout or b""
        detail = output.decode(errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args[:4])} failed in {root}: {detail}") from exc
    return result.stdout.decode().strip()


def checked_commit(root: Path, object_id: str, label: str) -> dict[str, str]:
    if not SHA256.fullmatch(object_id):
        raise ValueError(f"{label} is not a Git object id")
    if run_git(root, "cat-file", "-e", f"{object_id}^{{commit}}") != "":
        raise ValueError(f"{label} is not a commit: {object_id}")
    return {
        "commit": run_git(root, "rev-parse", f"{object_id}^{{commit}}"),
        "tree": run_git(root, "rev-parse", f"{object_id}^{{tree}}"),
        "parents": run_git(root, "show", "-s", "--format=%P", object_id),
    }


def clone_snapshot(root: Path, label: str) -> dict[str, Any]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"{label} is not an approved real clone: {root}")
    status = run_git(root, "status", "--porcelain")
    if status:
        raise ValueError(f"{label} clone is dirty: {status}")
    return {
        "root": str(root),
        "head": run_git(root, "rev-parse", "HEAD"),
        "head_tree": run_git(root, "rev-parse", "HEAD^{tree}"),
        "origin_main": run_git(root, "rev-parse", "origin/main"),
        "origin_main_tree": run_git(root, "rev-parse", "origin/main^{tree}"),
        "integration": run_git(root, "rev-parse", "tl/integration"),
        "integration_tree": run_git(root, "rev-parse", "tl/integration^{tree}"),
        "status": status,
        "shallow": run_git(root, "rev-parse", "--is-shallow-repository"),
    }


def load_wrapper() -> Any:
    raw = D68_WRAPPER.read_bytes()
    actual = digest(raw)
    if actual != D68_WRAPPER_SHA256:
        raise ValueError(f"D68 wrapper hash mismatch: {actual} != {D68_WRAPPER_SHA256}")
    spec = importlib.util.spec_from_file_location("retained_d68_source_stager", D68_WRAPPER)
    if spec is None or spec.loader is None:
        raise ValueError("unable to load retained D68 wrapper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def alternate_view(source: Path, parent: Path, name: str) -> Path:
    """Expose an existing clone's complete object store without cloning it.

    App is shallow, but its approved existing clone contains the captured
    objects.  A private bare view has no shallow boundary and only points at
    that clone's object directory; no source .git file is changed.
    """

    view = parent / f"source-view-{name}"
    run_git(parent, "init", "--bare", "-q", str(view))
    objects = run_git(source, "rev-parse", "--path-format=absolute", "--git-path", "objects")
    (view / "objects" / "info").mkdir(parents=True, exist_ok=True)
    (view / "objects" / "info" / "alternates").write_text(objects + "\n")
    for ref, object_id in (
        ("refs/remotes/origin/main", FRESH_UPSTREAM[name]),
        ("refs/heads/tl/integration", CAPTURED[name]),
    ):
        run_git(view, "update-ref", ref, object_id)
    checked_commit(view, CAPTURED[name], f"{name} source-view capture")
    return view


def diff_blobs(root: Path, base: str, tip: str) -> list[dict[str, Any]]:
    raw = run_git(root, "diff", "--raw", "--no-renames", "--abbrev=40", base, tip)
    entries: list[dict[str, Any]] = []
    for line in raw.splitlines():
        header, path = line.split("\t", 1)
        fields = header.split()
        if len(fields) != 5 or not fields[0].startswith(":"):
            raise ValueError(f"unexpected raw diff line: {line}")
        old_blob, new_blob, status = fields[2], fields[3], fields[4]
        entries.append(
            {
                "path": path,
                "status": status,
                "upstream_blob": None if old_blob == "0" * 40 else old_blob,
                "source_blob": None if new_blob == "0" * 40 else new_blob,
            }
        )
    return entries


def write_patch(path: Path, patch: bytes) -> str:
    if len(patch) > 50 * 1024 * 1024:
        raise ValueError(f"patch exceeds the 50 MiB evidence limit: {path}")
    path.write_bytes(patch)
    return digest(patch)


def stage_one(
    wrapper: Any,
    name: str,
    source: Path,
    stage_root: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    base = UPSTREAM_BASE[name]
    capture = CAPTURED[name]
    fresh = FRESH_UPSTREAM[name]
    if run_git(SOURCE_CLONES[name], "rev-parse", "origin/main") != fresh:
        raise ValueError(f"{name} approved fresh upstream ref drifted before staging")
    source_identity = checked_commit(source, capture, f"{name} capture")
    base_identity = checked_commit(source, base, f"{name} gating upstream base")
    fresh_identity = checked_commit(source, fresh, f"{name} approved fresh upstream")
    patch = subprocess.check_output(
        ["git", "-C", str(source), "diff", "--no-ext-diff", "--binary", "--full-index", base, capture],
        env=wrapper.GIT_ENV,
    )
    patch_path = evidence_dir / f"{name}.base-to-capture.patch"
    patch_sha = write_patch(patch_path, patch)
    stage = stage_root / name
    before = {
        "base": base,
        "base_tree": base_identity["tree"],
        "upstream_tip": fresh,
        "upstream_tip_tree": fresh_identity["tree"],
        "gated_tip": capture,
        "gated_tree": source_identity["tree"],
    }
    result = wrapper.stage_repo(
        name,
        {
            "root": str(source),
            "upstream_base": base,
            "upstream_base_tree": base_identity["tree"],
            "gated_tip": capture,
            "gated_tree": source_identity["tree"],
        },
        before,
        stage,
    )
    stage_diff = subprocess.check_output(
        ["git", "-C", str(stage), "diff", "--no-ext-diff", "--binary", "--full-index", fresh, "HEAD"],
        env=wrapper.GIT_ENV,
    )
    # The applied worktree is the acceptance surface here.  Checking the
    # clean worktree (rather than re-linting the historical source delta)
    # avoids turning pre-existing upstream whitespace into a source-only
    # mutation while still proving the staged tree has no local residue.
    check = subprocess.run(
        ["git", "-C", str(stage), "diff", "--check"],
        check=False,
        env=wrapper.GIT_ENV,
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        raise RuntimeError(f"git diff --check failed for {name}: {check.stdout}{check.stderr}")
    result.update(
        {
            "source_clone": str(SOURCE_CLONES[name]),
            "source_view": str(source),
            "gating_upstream_base": base_identity,
            "captured_integration": source_identity,
            "fresh_upstream": fresh_identity,
            "patch_path": str(patch_path),
            "patch_sha256": patch_sha,
            "patch_bytes": len(patch),
            "source_upstream_blobs": diff_blobs(source, base, capture),
            "applied_diff_sha256": digest(stage_diff),
            "applied_diff_bytes": len(stage_diff),
            "staged_status": run_git(stage, "status", "--porcelain"),
            "staged_gate_ref": run_git(stage, "rev-parse", "tl/integration"),
            "staged_gate_tree": run_git(stage, "rev-parse", "tl/integration^{tree}"),
            "staged_upstream_ref": run_git(stage, "rev-parse", "origin/main"),
            "staged_upstream_tree": run_git(stage, "rev-parse", "origin/main^{tree}"),
            "diff_check": "PASS",
        }
    )
    if result["staged_status"]:
        raise RuntimeError(f"staged {name} tree is dirty: {result['staged_status']}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--staging", type=Path, required=True)
    args = parser.parse_args()
    evidence = args.evidence.absolute()
    staging = args.staging.absolute()
    evidence.mkdir(parents=True, exist_ok=True)
    staging.mkdir(parents=True, exist_ok=True)
    wrapper = load_wrapper()
    before = {
        name: clone_snapshot(SOURCE_CLONES[name], f"{name} source clone") for name in REPOS
    }
    integration_before = {
        name: clone_snapshot(INTEGRATION_ROOTS[name], f"{name} integration checkout")
        for name in REPOS
    }
    records: dict[str, Any] = {}
    views: dict[str, str] = {}
    source_view_root = staging / "source-views"
    source_view_root.mkdir()
    stage_root = staging / "applied"
    stage_root.mkdir()
    for name in REPOS:
        view = alternate_view(SOURCE_CLONES[name], source_view_root, name)
        views[name] = str(view)
        records[name] = stage_one(wrapper, name, view, stage_root, evidence)
    after = {
        name: clone_snapshot(SOURCE_CLONES[name], f"{name} source clone") for name in REPOS
    }
    integration_after = {
        name: clone_snapshot(INTEGRATION_ROOTS[name], f"{name} integration checkout")
        for name in REPOS
    }
    if before != after or integration_before != integration_after:
        raise RuntimeError("source or integration checkout changed during source-only staging")
    manifest = {
        "version": 1,
        "phase": "SOURCEONLY",
        "status": "PASS",
        "tuple": CAPTURED,
        "gating_upstream": UPSTREAM_BASE,
        "approved_fresh_upstream": FRESH_UPSTREAM,
        "d68_wrapper": {"path": str(D68_WRAPPER), "sha256": D68_WRAPPER_SHA256},
        "source_clones_before": before,
        "source_clones_after": after,
        "integration_checkouts_before": integration_before,
        "integration_checkouts_after": integration_after,
        "source_views": views,
        "staging_root": str(staging),
        "repositories": records,
        "build_render_zip": "PENDING",
        "notes": {
            "D65": "authentic manifest release order preserved",
            "D67": "postinstall environment known gap preserved",
            "D72": "CLI notes preserved",
            "D62": "submit gap preserved",
        },
    }
    manifest_path = evidence / "d108-source-rehearsal-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    (evidence / "d108-source-rehearsal-manifest.sha256").write_text(
        f"{digest(manifest_path.read_bytes())}  {manifest_path.name}\n"
    )
    (evidence / "d108-source-rehearsal-status").write_text("PASS\n")
    print(json.dumps({"status": "PASS", "manifest": str(manifest_path), "staging": str(staging)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"source-only rehearsal refused: {exc}", file=sys.stderr)
        raise SystemExit(2)
