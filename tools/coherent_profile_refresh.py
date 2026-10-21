#!/usr/bin/env python3
"""Preflight and print the later private coherent-profile refresh command.

This is an operator-side preparation aid, not an installer or a product
profile authority.  It is deliberately stdlib-only: the cheap preflight must
not import Astrid, Runtime, the client, or any checkout.  The refresh command
is emitted only after the manager supplies the exact current Agent identity and
all approval/resource records.  This worker never executes that command.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import os
import shlex
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

LOCK_SHA256 = "478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761"
LOCK_ENTRIES = 164
MIN_FREE_BYTES = 5 * 1024**3
PROFILE_KEYS = {"profile", "runtime_checkout", "source_checkout", "runtime_environment"}
REQUIRED_ORIGINS = {
    "host",
    "child",
    "action",
    "client",
    "sdk",
    "runtime_protocol",
    "runtime_protocol.platform",
    "astrid_runtime",
}
EXPECTED_WHEELS = {
    "astrid-0.1.0-py3-none-any.whl": "fa2f824d1068f6233dc852960726d597f21a243d768ff0cafe258b7afe391346",
    "astrid_runtime-0.1.0-py3-none-any.whl": "12df54644e1acac46b9c396135ef345808a98515965f1f12f479f32adf3c9b0a",
    "astrid_runtime_client-0.2.14-py3-none-any.whl": "567605b13254f88ddeddad7b570553a2c50b5092908e6c4153553f9867e37254",
}
EXPECTED_DISTS = {
    "astrid": "0.1.0",
    "astrid-runtime": "0.1.0",
    "astrid-runtime-client": "0.2.14",
}
SHARED_ROOTS = tuple(
    Path(item)
    for item in (
        "/home/user/work/app/node_modules",
        "/home/user/work/venv-agent",
        "/home/user/work/venv-runtime",
        "/home/user/work/runtimes",
    )
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _real(path: Path) -> Path:
    return path.expanduser().absolute()


def _under(path: Path, root: Path) -> bool:
    try:
        return _real(path).is_relative_to(_real(root))
    except ValueError:
        return False


def _no_symlink_components(path: Path) -> bool:
    current = _real(path)
    for parent in (current, *current.parents):
        if parent.is_symlink():
            return False
    return True


def _all_symlinks(root: Path) -> list[Path]:
    found: list[Path] = []
    if not root.exists():
        return found
    for directory, dirs, files in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in (*dirs, *files):
            candidate = directory_path / name
            if candidate.is_symlink():
                found.append(candidate)
    return found


def _git(repo: Path, *args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def _read_json(path: Path, label: str, blockers: list[str]) -> dict[str, object] | None:
    if not path.is_file() or path.is_symlink():
        blockers.append(f"{label} is not a regular file: {path}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        blockers.append(f"{label} is unreadable JSON: {exc}")
        return None
    if not isinstance(value, dict):
        blockers.append(f"{label} must contain a JSON object")
        return None
    return value


def _required(value: str | None, name: str, blockers: list[str]) -> str:
    if not value or not value.strip():
        blockers.append(f"missing manager-supplied prerequisite: {name}")
        return ""
    return value.strip()


def _validate_evidence(
    path_text: str,
    label: str,
    agent_commit: str,
    agent_tree: str,
    blockers: list[str],
) -> None:
    if not path_text:
        return
    record = _read_json(_real(Path(path_text)), label, blockers)
    if record is None:
        return
    verdict = str(record.get("verdict", record.get("approval", ""))).upper()
    if verdict != "APPROVE":
        blockers.append(f"{label} is not APPROVE (got {verdict or 'missing'})")
    if record.get("merged") is not True:
        blockers.append(f"{label} does not prove the approved change is merged")
    if label.startswith("document") and str(record.get("http_result", "")).upper() not in {
        "PASS",
        "PASSED",
    }:
        blockers.append(f"{label} does not contain a passing HTTP result")
    if agent_commit and record.get("source_commit") != agent_commit:
        blockers.append(f"{label} source commit does not equal the selected Agent commit")
    if agent_tree and record.get("source_tree") != agent_tree:
        blockers.append(f"{label} source tree does not equal the selected Agent tree")
    if label.startswith("installed-origin"):
        origins = set(record.get("origins", []))
        missing = sorted(REQUIRED_ORIGINS - origins)
        if missing:
            blockers.append(f"{label} omits required installed origins: {', '.join(missing)}")


def _lock_requirements(lock: Path, blockers: list[str]) -> dict[str, str | None]:
    if not lock.is_file() or lock.is_symlink():
        blockers.append(f"164-pin lock is not a regular file: {lock}")
        return {}
    try:
        lines = [
            line.strip() for line in lock.read_text(encoding="utf-8").splitlines() if line.strip()
        ]
    except (OSError, UnicodeDecodeError) as exc:
        blockers.append(f"164-pin lock is unreadable: {exc}")
        return {}
    if len(lines) != LOCK_ENTRIES:
        blockers.append(f"expected {LOCK_ENTRIES} lock entries, found {len(lines)}")
    if _sha256(lock) != LOCK_SHA256:
        blockers.append("164-pin lock SHA-256 differs from the immutable coherent6f closure")
    requirements: dict[str, str | None] = {}
    for line in lines:
        if "==" in line:
            left, version = line.split("==", 1)
        else:
            left, version = line.split(" @ ", 1)[0], None
        requirements[left.strip().lower().replace("_", "-")] = version
    return requirements


def _check_records(site: Path, environment: Path, blockers: list[str]) -> int:
    records = sorted(site.glob("*.dist-info/RECORD")) if site.is_dir() else []
    rows_checked = 0
    for record in records:
        try:
            rows = list(csv.reader(record.read_text(encoding="utf-8").splitlines()))
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            blockers.append(f"unreadable RECORD: {record} ({exc})")
            continue
        for row in rows:
            if len(row) != 3 or not row[0]:
                blockers.append(f"malformed RECORD row: {record}")
                continue
            relative, expected_hash, expected_size = row
            if relative.startswith("/") or ".." in Path(relative).parts:
                target = (site / relative).resolve()
            else:
                target = site / relative
            if not _real(target).is_relative_to(_real(environment)):
                blockers.append(
                    f"RECORD path escapes the private environment: {record}: {relative}"
                )
                continue
            if target.is_symlink():
                blockers.append(f"RECORD path is symlinked: {record}: {relative}")
                continue
            if not target.is_file():
                # RECORD permits an empty hash/size row for generated files
                # such as optional __pycache__ entries.
                if expected_hash or expected_size:
                    blockers.append(f"hashed RECORD member is missing: {record}: {relative}")
                continue
            rows_checked += 1
            if expected_hash:
                if not expected_hash.startswith("sha256="):
                    blockers.append(f"RECORD uses a non-sha256 digest: {record}: {relative}")
                else:
                    digest = (
                        base64.urlsafe_b64encode(bytes.fromhex(_sha256(target)))
                        .decode()
                        .rstrip("=")
                    )
                    if digest != expected_hash.removeprefix("sha256="):
                        blockers.append(f"RECORD hash mismatch: {record}: {relative}")
            if expected_size and int(expected_size) != target.stat().st_size:
                blockers.append(f"RECORD size mismatch: {record}: {relative}")
    if not records:
        blockers.append(f"no installed RECORD files under private site-packages: {site}")
    return rows_checked


def _check_origins(python: Path, site: Path, blockers: list[str]) -> None:
    probe = subprocess.run(
        [
            str(python),
            "-I",
            "-B",
            "-c",
            "import importlib.util, json; "
            "names = ['astrid', 'astrid_runtime_client', 'runtime_protocol', 'runtime_protocol.platform', "
            "'astrid_runtime', 'banodoco_timeline_schema', 'numpy', 'PIL', 'cv2', 'yaml']; "
            "print(json.dumps({name: (importlib.util.find_spec(name).origin if importlib.util.find_spec(name) else None) for name in names}))",
        ],
        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C.UTF-8"},
        cwd="/tmp",
        check=False,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        blockers.append(f"installed origin probe failed: {probe.stderr.strip()}")
        return
    try:
        origins = json.loads(probe.stdout)
    except ValueError:
        blockers.append("installed origin probe was not JSON")
        return
    for name, origin in origins.items():
        if not origin:
            blockers.append(f"installed origin missing: {name}")
        elif not _real(Path(origin)).is_relative_to(_real(site)):
            blockers.append(f"installed origin escaped private site-packages: {name}={origin}")


def _check_stage(stage: Path, blockers: list[str]) -> dict[str, str]:
    facts: dict[str, str] = {}
    if not stage.is_dir() or stage.is_symlink():
        blockers.append(f"leased coherent stage is not a regular directory: {stage}")
        return facts
    if any(_under(stage, root) or _under(root, stage) for root in SHARED_ROOTS):
        blockers.append(f"leased stage overlaps a shared dependency root: {stage}")
    symlinks = _all_symlinks(stage)
    if symlinks:
        blockers.append(f"leased coherent stage contains {len(symlinks)} symlink(s)")
    lock = stage / "metadata" / "venv-agent-child-s2.txt"
    requirements = _lock_requirements(lock, blockers)
    facts["lock_entries"] = str(len(requirements))
    wheels = stage / "wheelhouse"
    actual_names = {path.name for path in wheels.iterdir()} if wheels.is_dir() else set()
    if actual_names != set(EXPECTED_WHEELS):
        blockers.append(
            "coherent wheelhouse does not contain exactly Runtime/client/Agent wheels: "
            + ", ".join(sorted(actual_names))
        )
    for name, expected in EXPECTED_WHEELS.items():
        wheel = wheels / name
        if not wheel.is_file() or wheel.is_symlink():
            blockers.append(f"coherent wheel is missing or symlinked: {wheel}")
        elif _sha256(wheel) != expected:
            blockers.append(f"coherent wheel hash differs: {name}")
    profile_path = stage / "profile" / "astrid.json"
    profile = _read_json(profile_path, "existing SourceProfile", blockers)
    if profile is not None:
        if set(profile) != PROFILE_KEYS:
            blockers.append(f"SourceProfile fields changed: {sorted(profile)}")
        if profile.get("profile") != "astrid":
            blockers.append("SourceProfile profile is not astrid")
        environment = _real(Path(str(profile.get("runtime_environment", ""))))
        site = _real(Path(str(profile.get("source_checkout", ""))))
        if profile.get("runtime_checkout") != profile.get("source_checkout"):
            blockers.append("SourceProfile runtime/source checkout roots differ")
        if not _no_symlink_components(environment) or not _no_symlink_components(site):
            blockers.append("SourceProfile path contains a symlink component")
        if site != _real(environment / "lib" / "python3.13" / "site-packages"):
            blockers.append(
                "SourceProfile does not select the existing private Python 3.13 site-packages"
            )
        python = environment / "bin" / "python"
        if not python.is_file() or python.is_symlink():
            blockers.append(f"selected installed interpreter is unavailable: {python}")
        else:
            probe = subprocess.run(
                [
                    str(python),
                    "-I",
                    "-B",
                    "-c",
                    "import importlib.metadata as m, json, sys; "
                    "d = {x.metadata['Name'].lower().replace('_', '-'): x.version for x in m.distributions() if x.metadata.get('Name')}; "
                    "print(json.dumps({'python': sys.version_info[:2], 'dists': len(d), 'versions': d}))",
                ],
                env={"PATH": "/usr/bin:/bin", "LC_ALL": "C.UTF-8"},
                cwd="/tmp",
                check=False,
                capture_output=True,
                text=True,
            )
            if probe.returncode != 0:
                blockers.append(f"installed package inventory failed: {probe.stderr.strip()}")
            else:
                try:
                    inventory = json.loads(probe.stdout)
                except ValueError:
                    inventory = {}
                    blockers.append("installed package inventory was not JSON")
                if inventory.get("python") != [3, 13]:
                    blockers.append(
                        f"selected interpreter is not Python 3.13: {inventory.get('python')}"
                    )
                versions = inventory.get("versions", {})
                for name, expected in EXPECTED_DISTS.items():
                    if versions.get(name) != expected:
                        blockers.append(
                            f"installed {name} is {versions.get(name)!r}, expected {expected!r}"
                        )
                for name, expected in requirements.items():
                    if name not in versions:
                        blockers.append(f"164-pin distribution is not installed: {name}")
                    elif expected is not None and versions[name] != expected:
                        blockers.append(
                            f"164-pin version differs for {name}: {versions[name]} != {expected}"
                        )
                if not isinstance(inventory.get("dists"), int) or len(requirements) != LOCK_ENTRIES:
                    blockers.append(
                        "installed distribution inventory is smaller than the 164-pin closure"
                    )
            facts["record_rows"] = str(_check_records(site, environment, blockers))
            _check_origins(python, site, blockers)
    facts["stage_free_bytes"] = str(shutil.disk_usage(stage).free)
    return facts


def _check_source(
    source: Path,
    commit: str,
    tree: str,
    ancestry_path: Path | None,
    blockers: list[str],
) -> None:
    if not source.is_dir() or source.is_symlink():
        blockers.append(f"selected Agent source is not a regular directory: {source}")
        return
    code, status, stderr = _git(source, "status", "--porcelain")
    if code != 0:
        blockers.append(f"selected Agent source status failed: {stderr or status}")
    elif status:
        blockers.append("selected Agent source is dirty; archive only a clean exact commit")
    code, actual_commit, stderr = _git(source, "rev-parse", "HEAD")
    if code != 0:
        blockers.append(f"selected Agent source HEAD could not be read: {stderr}")
    elif commit and actual_commit != commit:
        blockers.append(
            f"selected Agent source HEAD differs from manager commit: {actual_commit} != {commit}"
        )
    code, actual_tree, stderr = _git(source, "rev-parse", "HEAD^{tree}")
    if code != 0:
        blockers.append(f"selected Agent source tree could not be read: {stderr}")
    elif tree and actual_tree != tree:
        blockers.append(
            f"selected Agent source tree differs from manager tree: {actual_tree} != {tree}"
        )
    if ancestry_path is None:
        return
    ancestry = _read_json(ancestry_path, "Agent ancestry/blob record", blockers)
    if ancestry is None:
        return
    if ancestry.get("agent_commit") != commit or ancestry.get("agent_tree") != tree:
        blockers.append("Agent ancestry/blob record does not bind to the selected commit/tree")
    for parent in ancestry.get("reachable_commits", []):
        code, _, stderr = _git(source, "merge-base", "--is-ancestor", str(parent), commit)
        if code != 0:
            blockers.append(f"declared Agent ancestry commit is not reachable: {parent} ({stderr})")
    blobs = ancestry.get("preserved_blobs", {})
    if not isinstance(blobs, dict) or not blobs:
        blockers.append("Agent ancestry/blob record has no preserved blobs")
    else:
        for path, expected in blobs.items():
            code, actual, stderr = _git(source, "rev-parse", f"{commit}:{path}")
            if code != 0 or actual != expected:
                blockers.append(f"preserved Agent blob differs at {path}: {actual or stderr}")


def _check_tools(args: argparse.Namespace, blockers: list[str], facts: dict[str, str]) -> None:
    for name in ("node", "remotion", "browser", "ffmpeg", "ffprobe"):
        value = getattr(args, name)
        if not value:
            blockers.append(f"missing manager-supplied tool path: {name}")
            continue
        path = _real(Path(value))
        expected_kind = "dir" if name == "remotion" else "file"
        if (expected_kind == "dir" and (not path.is_dir() or path.is_symlink())) or (
            expected_kind == "file" and (not path.is_file() or path.is_symlink())
        ):
            blockers.append(f"tool path is unavailable or symlinked: {name}={path}")
        else:
            facts[f"{name}_sha256"] = _sha256(path) if path.is_file() else "directory"


def _check_ambient(blockers: list[str]) -> None:
    for name in ("PYTHONPATH", "NODE_OPTIONS", "NODE_PATH"):
        if os.environ.get(name):
            blockers.append(f"ambient {name} must be unset for the pack-host command")
    if any("site-packages" in entry and str(Path.cwd()) in entry for entry in sys.path):
        blockers.append(
            "current preflight interpreter exposes a checkout/product site-packages path"
        )


def _check_destination(
    destination: Path, stage: Path, blockers: list[str], facts: dict[str, str]
) -> None:
    if destination.exists():
        blockers.append(
            f"refresh destination already exists; choose a new private root: {destination}"
        )
    if any(_under(destination, root) or _under(root, destination) for root in SHARED_ROOTS):
        blockers.append(f"refresh destination overlaps a shared dependency root: {destination}")
    if not _no_symlink_components(destination.parent):
        blockers.append(
            f"refresh destination parent contains a symlink component: {destination.parent}"
        )
    free = shutil.disk_usage(destination.parent).free
    facts["destination_free_bytes"] = str(free)
    if free < MIN_FREE_BYTES:
        blockers.append(f"free disk below 5 GiB at refresh destination: {free} bytes")
    if _under(destination, stage) or _under(stage, destination):
        blockers.append("refresh destination must not overlap the leased immutable stage")


def _check_args(args: argparse.Namespace) -> tuple[list[str], dict[str, str]]:
    blockers: list[str] = []
    facts: dict[str, str] = {}
    stage_text = _required(args.stage, "--stage", blockers)
    commit = _required(args.agent_commit, "--agent-commit", blockers)
    tree = _required(args.agent_tree, "--agent-tree", blockers)
    source_text = _required(args.agent_source, "--agent-source", blockers)
    destination_text = _required(args.destination, "--destination", blockers)
    document = _required(args.document_evidence, "--document-evidence", blockers)
    origins = _required(args.origin_evidence, "--origin-evidence", blockers)
    ancestry = _required(args.ancestry, "--ancestry", blockers)
    stage = _real(Path(stage_text)) if stage_text else Path("/")
    source = _real(Path(source_text)) if source_text else Path("/")
    destination = _real(Path(destination_text)) if destination_text else Path("/nonexistent")
    facts.update(_check_stage(stage, blockers))
    if source_text and commit and tree:
        _check_source(source, commit, tree, _real(Path(ancestry)) if ancestry else None, blockers)
    _validate_evidence(document, "document adapter evidence", commit, tree, blockers)
    _validate_evidence(origins, "installed-origin evidence", commit, tree, blockers)
    _check_tools(args, blockers, facts)
    _check_ambient(blockers)
    if destination_text:
        _check_destination(destination, stage, blockers, facts)
    for label, value in (("--full-argv", args.full_argv), ("--d13-argv", args.d13_argv)):
        if not value:
            blockers.append(f"missing manager-supplied later test argv: {label}")
        elif any(token in value for token in ("PYTHONPATH", "NODE_OPTIONS", "NODE_PATH")):
            blockers.append(
                f"later test argv contains a forbidden ambient path/tool variable: {label}"
            )
    return blockers, facts


def _refresh_command(args: argparse.Namespace) -> str:
    env = {
        "HOME": "/tmp/coherent-profile-home",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": f"{_real(Path(args.node)).parent}:{_real(Path(args.destination)) / 'venv' / 'bin'}:/usr/bin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    command = [
        "env",
        "-i",
        *[item for pair in env.items() for item in (pair[0], pair[1])],
        str(_real(Path(args.stage)) / "venv" / "bin" / "python"),
        "-I",
        "-B",
        str(Path(__file__).resolve()),
        "--refresh",
        "--stage",
        str(_real(Path(args.stage))),
        "--agent-source",
        str(_real(Path(args.agent_source))),
        "--agent-commit",
        args.agent_commit,
        "--agent-tree",
        args.agent_tree,
        "--ancestry",
        str(_real(Path(args.ancestry))),
        "--document-evidence",
        str(_real(Path(args.document_evidence))),
        "--origin-evidence",
        str(_real(Path(args.origin_evidence))),
        "--destination",
        str(_real(Path(args.destination))),
        "--node",
        str(_real(Path(args.node))),
        "--remotion",
        str(_real(Path(args.remotion))),
        "--browser",
        str(_real(Path(args.browser))),
        "--ffmpeg",
        str(_real(Path(args.ffmpeg))),
        "--ffprobe",
        str(_real(Path(args.ffprobe))),
        "--full-argv",
        args.full_argv,
        "--d13-argv",
        args.d13_argv,
    ]
    return shlex.join(command)


def _extract_agent(source: Path, commit: str, destination: Path) -> None:
    result = subprocess.run(
        ["git", "-C", str(source), "archive", "--format=tar", commit, "--", "astrid"],
        check=True,
        capture_output=True,
    )
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
        members = archive.getmembers()
        if any(member.issym() or member.islnk() for member in members):
            raise RuntimeError("selected Agent archive contains a symlink")
        archive.extractall(destination, filter="data")


def _rewrite_launchers_and_records(destination: Path, old_stage: Path) -> None:
    environment = destination / "venv"
    for path in (environment / "bin").iterdir():
        if not path.is_file() or path.is_symlink():
            continue
        data = path.read_bytes()
        replacement = data.replace(str(old_stage).encode(), str(destination).encode())
        replacement = replacement.replace(
            str(destination / "venv").encode(), str(environment).encode()
        )
        if replacement != data:
            path.write_bytes(replacement)
    site = environment / "lib" / "python3.13" / "site-packages"
    for record in site.glob("*.dist-info/RECORD"):
        rows = list(csv.reader(record.read_text(encoding="utf-8").splitlines()))
        updated: list[list[str]] = []
        for row in rows:
            if len(row) != 3 or not row[0] or row[0].endswith(".dist-info/RECORD"):
                updated.append(row)
                continue
            target = (site / row[0]).resolve()
            if target.is_file() and target.is_relative_to(environment):
                row[1] = "sha256=" + base64.urlsafe_b64encode(
                    bytes.fromhex(_sha256(target))
                ).decode().rstrip("=")
                row[2] = str(target.stat().st_size)
            updated.append(row)
        output = io.StringIO(newline="")
        csv.writer(output, lineterminator="\n").writerows(updated)
        record.write_text(output.getvalue(), encoding="utf-8")


def _execute_refresh(args: argparse.Namespace) -> int:
    blockers, _ = _check_args(args)
    if blockers:
        print("coherent profile refresh: BLOCKED")
        for blocker in blockers:
            print(f"- {blocker}")
        return 2
    stage = _real(Path(args.stage))
    source = _real(Path(args.agent_source))
    destination = _real(Path(args.destination))
    destination.mkdir(parents=True)
    shutil.copytree(
        stage, destination, symlinks=False, copy_function=shutil.copy2, dirs_exist_ok=True
    )
    old_source = destination / "source" / "agent-6f"
    if old_source.exists():
        shutil.rmtree(old_source)
    old_wheel = destination / "wheelhouse" / "astrid-0.1.0-py3-none-any.whl"
    if old_wheel.exists():
        old_wheel.unlink()
    current_source = destination / "source" / "agent-current"
    current_source.mkdir(parents=True)
    _extract_agent(source, args.agent_commit, destination / "source")
    extracted = destination / "source" / "astrid"
    extracted.rename(current_source)
    python = destination / "venv" / "bin" / "python"
    wheelhouse = destination / "wheelhouse"
    (destination / "home").mkdir()
    environment = {"PATH": "/usr/bin:/bin", "HOME": str(destination / "home"), "LC_ALL": "C.UTF-8"}
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "wheel",
            "--no-index",
            "--no-build-isolation",
            "--no-deps",
            "--wheel-dir",
            str(wheelhouse),
            str(current_source),
        ],
        cwd="/tmp",
        env=environment,
        check=True,
    )
    wheels = sorted(wheelhouse.glob("astrid-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"expected one newly built Agent wheel, found {wheels}")
    wheel = wheels[0]
    subprocess.run(
        [
            str(destination / "venv" / "bin" / "pip"),
            "install",
            "--no-index",
            "--no-deps",
            "--force-reinstall",
            str(wheel),
        ],
        cwd="/tmp",
        env=environment,
        check=True,
    )
    _rewrite_launchers_and_records(destination, stage)
    wheel_rows = [
        f"{_sha256(wheel)}  {wheel.name}",
        f"{EXPECTED_WHEELS['astrid_runtime-0.1.0-py3-none-any.whl']}  astrid_runtime-0.1.0-py3-none-any.whl",
        f"{EXPECTED_WHEELS['astrid_runtime_client-0.2.14-py3-none-any.whl']}  astrid_runtime_client-0.2.14-py3-none-any.whl",
    ]
    (destination / "metadata" / "wheels.sha256").write_text(
        "\n".join(wheel_rows) + "\n", encoding="utf-8"
    )
    provenance = destination / "metadata" / "provenance.txt"
    with provenance.open("a", encoding="utf-8") as stream:
        stream.write(
            "\nCurrent public refresh\n"
            f"  Agent source commit: {args.agent_commit}\n"
            f"  Agent source tree: {args.agent_tree}\n"
            f"  Agent wheel: {wheel.name}\n"
            f"  Agent wheel SHA-256: {_sha256(wheel)}\n"
            "  Runtime/client and 164-pin closure: inherited byte-for-byte\n"
        )
    profile = destination / "profile" / "astrid.json"
    site = destination / "venv" / "lib" / "python3.13" / "site-packages"
    profile.write_text(
        json.dumps(
            {
                "profile": "astrid",
                "runtime_checkout": str(site),
                "source_checkout": str(site),
                "runtime_environment": str(destination / "venv"),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"coherent profile refresh: created private root {destination}")
    print(f"agent_wheel={wheel}")
    print(f"agent_wheel_sha256={_sha256(wheel)}")
    print(
        "Next: run the existing wheel/RECORD/origin harness, then the one manager-authorized full and D13 commands."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="execute the later private refresh after a passing preflight",
    )
    parser.add_argument(
        "--emit-refresh",
        action="store_true",
        help="print the exact later command after a passing preflight",
    )
    parser.add_argument("--stage")
    parser.add_argument("--agent-source")
    parser.add_argument("--agent-commit")
    parser.add_argument("--agent-tree")
    parser.add_argument("--ancestry")
    parser.add_argument("--document-evidence")
    parser.add_argument("--origin-evidence")
    parser.add_argument("--destination")
    parser.add_argument("--node")
    parser.add_argument("--remotion")
    parser.add_argument("--browser")
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    parser.add_argument("--full-argv")
    parser.add_argument("--d13-argv")
    args = parser.parse_args(argv)
    if args.refresh:
        return _execute_refresh(args)
    blockers, facts = _check_args(args)
    if blockers:
        print("coherent profile preflight: BLOCKED")
        for key, value in sorted(facts.items()):
            print(f"{key}={value}")
        for blocker in blockers:
            print(f"- {blocker}")
        return 2
    print("coherent profile preflight: READY (no build/install/native/full work performed)")
    for key, value in sorted(facts.items()):
        print(f"{key}={value}")
    if args.emit_refresh:
        print("refresh_command=" + _refresh_command(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
