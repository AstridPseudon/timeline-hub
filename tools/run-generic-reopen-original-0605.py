"""Custody runner for the one generic-host harvest/reopen qualification.

The default mode is a fail-closed preflight.  ``run-original`` is deliberately
explicit and requires an independently reviewed harness digest; it is the only
mode that starts the unchanged pytest body.  Production imports are resolved
by the managed child interpreter, with no ``PYTHONPATH`` or installed-tree
overlay.
"""

from __future__ import annotations

import argparse
import ast
import base64
import csv
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree as ET

SOURCE_COMMIT = "bb50a43c915ec00c05c5ee34569a040bab8e817c"
RUNTIME_COMMIT = "f3208b26b53c4d7053e5464eaa7c5e15b1505812"
TEST_RELATIVE = Path("tests/test_generic_host.py")
TEST_FUNCTION = "test_structure_pack_members_survive_harvest_cleanup_and_reopen"
PREFIXES = ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client")
EXPECTED_PROFILE = Path("/home/user/work/runtimes/agent-remotion-v3-819acf-1110")
EXPECTED_NODE = Path("/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node")
EXPECTED_NODE_VERSION = "v20.19.4"
EXPECTED_ARCHIVE_SHA256 = "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"
EXPECTED_PROFILE_FILES = {
    "package-lock.json": "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d",
    ".astrid-registry.lock": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ".astrid-registry-state.json": "d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96",
}
EXPECTED_TEST_IDENTITY = {
    "file_sha256": "b4b99d0bd4336f26d65c7763d87d28f0ca98fc5f92b02a70ba41a43c17453709",
    "function_source_sha256": "c5e09e12bf2a898571b9c6888604ac658f2884a5f2cb33532a24aee4d226f211",
    "function_ast_sha256": "549a1b07affc5d59365da430a8a31887074544b50a2a3b14575d30e1a275bb6b",
    "assertion_count": 12,
    "assertion_ast_sha256": [
        "589e2c1ea0e9c3c4f93b8b3b3a785884aa12cc484e3addf21bc977dd68807ec8",
        "ad50885719d8833eba7e8105ebbc20554541fc2263b2c2cca0d2fbb8400286a5",
        "e643f450fb4532b784d5fad2f3df8c641b043ff1dfbf35cc90f5e914e2cc4a41",
        "a494599e2450c152cbdfb815fb21a1fbdd626f5aacf8b41abef01fa83cddc12c",
        "72d2c7016083f09def50d83741d11050e66dcd48b04c1a119f76b49fcd162dc5",
        "1de374522d2309e4da5b40ceaa852c7b780a1eabc2a9c417291b4485cc435c7f",
        "6bfd1867fff52b71f7f671b1dbb0ea69663bfc2f3686e7b0707e239b291f6012",
        "815adbb0a394022f82c45d23de7682f396e10bc7448a6cc57994986994b7b480",
        "81bdc7f6948097c132454be5ab0758f6c4a623c150cc51340a6e1306d5dd1022",
        "22260ca4efefb72fd34c59be3578c363aa9cb8a0d6613e6d695514623158abf4",
        "edadff1d8207c852d74217d8b8fe5b42bc49b96115a0ea19b132971fcbb29195",
        "e961a9537c2f82344a3e220fad4beea000d79c4e4231d8586057b9a6c2f3d3ed",
    ],
    "body_bytes": 4870,
}
SCRIPT = Path(__file__).resolve()


class PreflightFailure(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    return sha256(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def require_file(path: Path, label: str) -> Path:
    if not path.is_file() or path.is_symlink():
        raise PreflightFailure(f"{label} is missing or is a symlink: {path}")
    return path


def real_child(path: Path) -> Path:
    if not path.is_dir() or path.is_symlink():
        raise PreflightFailure(f"managed child root is missing or is a symlink: {path}")
    resolved = path.resolve()
    if not (resolved / "bin/python").is_file():
        raise PreflightFailure(f"managed child has no bin/python: {resolved}")
    return resolved


def source_identity(root: Path) -> dict[str, Any]:
    test_path = require_file(root / TEST_RELATIVE, "target test source")
    data = test_path.read_bytes()
    text = data.decode("utf-8")
    tree = ast.parse(text, filename=str(test_path))
    function = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == TEST_FUNCTION
        ),
        None,
    )
    if function is None:
        raise PreflightFailure(f"target function not found: {TEST_FUNCTION}")
    lines = text.splitlines()
    body = "\n".join(lines[function.lineno - 1 : function.end_lineno])
    assertions = [node for node in ast.walk(function) if isinstance(node, ast.Assert)]
    identity = {
        "path": str(test_path),
        "file_sha256": sha256(data),
        "function_source_sha256": sha256(body.encode("utf-8")),
        "function_ast_sha256": sha256(ast.dump(function, include_attributes=True).encode()),
        "assertion_count": len(assertions),
        "assertion_ast_sha256": [
            sha256(ast.dump(node, include_attributes=True).encode()) for node in assertions
        ],
        "body_bytes": len(body.encode("utf-8")),
    }
    expected = {"path": str(test_path), **EXPECTED_TEST_IDENTITY}
    if identity != expected:
        raise PreflightFailure(
            "target test source does not match the independently reviewed body/function/assertion hashes"
        )
    return identity


def git_identity(root: Path) -> dict[str, Any]:
    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.STDOUT
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreflightFailure(f"cannot read source git identity: {exc}") from exc
    changed = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        text=True,
    ).strip()
    if head != SOURCE_COMMIT:
        raise PreflightFailure(f"source HEAD is {head}, expected reviewed bb50 source {SOURCE_COMMIT}")
    if changed:
        raise PreflightFailure(f"source tree is modified: {changed}")
    return {"head": head, "source_tree_status": "clean"}


def parse_kv_receipt(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="strict").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return values


def verify_record(site: Path, dist: Path, stem: str) -> dict[str, Any]:
    record = require_file(dist / "RECORD", f"{stem} RECORD")
    record_relative = record.relative_to(site).as_posix()
    rows: dict[str, Any] = {}
    try:
        with record.open(encoding="utf-8", newline="") as record_file:
            parsed_rows = csv.reader(record_file, strict=True)
            record_rows = list(parsed_rows)
        for row in record_rows:
            if len(row) != 3:
                raise PreflightFailure(f"malformed {stem} RECORD row")
            relative, encoded_digest, encoded_size = row
            pure = PurePosixPath(relative)
            if (
                not relative
                or pure.is_absolute()
                or "\\" in relative
                or str(pure) != relative
                or relative in rows
            ):
                raise PreflightFailure(f"unsafe or duplicate {stem} RECORD path: {relative!r}")
            installed = site / relative
            resolved = installed.resolve()
            if not installed.is_file() or installed.is_symlink() or not resolved.is_relative_to(site.resolve()):
                raise PreflightFailure(f"missing or escaping {stem} RECORD file: {relative}")
            content = installed.read_bytes()
            if not encoded_digest and not encoded_size:
                if relative != record_relative:
                    raise PreflightFailure(f"unhashed non-RECORD {stem} row: {relative}")
            else:
                if not encoded_digest.startswith("sha256=") or not encoded_size.isdigit():
                    raise PreflightFailure(f"malformed {stem} RECORD digest/size: {relative}")
                digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
                if encoded_digest != f"sha256={digest}" or int(encoded_size) != len(content):
                    raise PreflightFailure(f"{stem} RECORD bytes mismatch: {relative}")
            rows[relative] = {
                "sha256": sha256(content),
                "record_digest": encoded_digest,
                "bytes": len(content),
            }
    except UnicodeDecodeError as exc:
        raise PreflightFailure(f"{stem} RECORD is not UTF-8") from exc
    if not rows:
        raise PreflightFailure(f"{stem} RECORD is empty")
    return rows


def managed_custody(root: Path, child: Path, receipt: Path) -> dict[str, Any]:
    owner_path = require_file(child / ".bench-owner.json", "managed child owner record")
    owner = json.loads(owner_path.read_text(encoding="utf-8"))
    identity = owner.get("identity")
    if owner.get("component") != "child" or not isinstance(identity, dict):
        raise PreflightFailure("managed child owner record is not a child identity")
    if identity.get("agent_sha") != SOURCE_COMMIT:
        raise PreflightFailure("managed child owner agent SHA does not bind bb50 source")
    if identity.get("backend_sha") != RUNTIME_COMMIT:
        raise PreflightFailure("managed child owner runtime SHA does not bind f320 backend")

    marker_values: dict[str, str] = {}
    for name, expected in (
        (".astrid-source-commit", SOURCE_COMMIT),
        (".astrid-runtime-source-commit", RUNTIME_COMMIT),
    ):
        path = require_file(child / name, name)
        value = path.read_text(encoding="utf-8").strip()
        if value != expected:
            raise PreflightFailure(f"{name} is {value!r}, expected {expected}")
        marker_values[name] = value

    origin_marker = require_file(child / ".astrid-import-origins", "installed origin marker")
    distribution_marker = require_file(child / ".astrid-distribution-metadata", "distribution marker")
    metadata = parse_kv_receipt(distribution_marker)
    if metadata.get("astrid_name") != "astrid" or metadata.get("astrid_version") != "0.1.0":
        raise PreflightFailure("distribution marker has the wrong Agent identity")
    if metadata.get("astrid-runtime_name") != "astrid-runtime" or metadata.get("astrid-runtime_version") != "0.1.0":
        raise PreflightFailure("distribution marker has the wrong Runtime identity")
    if metadata.get("astrid_provenance") != "directory" or metadata.get("astrid-runtime_provenance") != "directory":
        raise PreflightFailure("distribution marker does not require directory provenance")

    receipt = require_file(receipt, "managed child provision receipt")
    receipt_text = receipt.read_text(encoding="utf-8", errors="strict")
    expected_receipt_parts = {
        "status=passed",
        f"agent_sha={SOURCE_COMMIT}",
        f"runtime_sha={RUNTIME_COMMIT}",
        f"{child}",
    }
    missing_receipt_parts = sorted(part for part in expected_receipt_parts if part not in receipt_text)
    if missing_receipt_parts:
        raise PreflightFailure(
            "managed provision receipt does not bind this source/runtime/child: "
            + ", ".join(missing_receipt_parts)
        )

    site = child / "lib" / "python3.13" / "site-packages"
    if not site.is_dir() or site.is_symlink():
        raise PreflightFailure(f"managed child site-packages is missing or symlinked: {site}")
    distributions: dict[str, Any] = {}
    source_roots = sorted(child.glob(".child-venv-source-*/"))
    if len(source_roots) != 1 or any(path.is_symlink() for path in source_roots):
        raise PreflightFailure("managed child must have exactly one non-symlink source snapshot")
    source_root = source_roots[0]
    expected_sources = {"astrid": source_root / "agent", "astrid_runtime": source_root / "runtime"}
    for name, source in expected_sources.items():
        if not source.is_dir() or source.is_symlink() or not source.resolve().is_relative_to(source_root.resolve()):
            raise PreflightFailure(f"{name} canonical source root is missing or escapes child custody")
    expected_direct_urls = {name: source.resolve().as_uri() for name, source in expected_sources.items()}
    for stem in ("astrid", "astrid_runtime"):
        dist_infos = sorted(site.glob(stem + "-*.dist-info"))
        if len(dist_infos) != 1:
            raise PreflightFailure(f"expected one {stem} dist-info directory, found {len(dist_infos)}")
        dist = dist_infos[0]
        record = require_file(dist / "RECORD", f"{stem} RECORD")
        direct = require_file(dist / "direct_url.json", f"{stem} direct_url")
        direct_value = json.loads(direct.read_text(encoding="utf-8"))
        if direct_value.get("url") != expected_direct_urls[stem]:
            raise PreflightFailure(f"{stem} direct URL is not its canonical child source root")
        if direct_value.get("dir_info", {}).get("editable") is not False:
            raise PreflightFailure(f"{stem} direct URL is editable or lacks non-editable provenance")
        if "archive_info" in direct_value:
            raise PreflightFailure(f"{stem} direct URL uses archive provenance")
        if metadata.get(f"{stem.replace('_', '-')}_direct_url") != direct_value["url"]:
            raise PreflightFailure(f"{stem} distribution marker does not match direct_url.json")
        record_rows = verify_record(site, dist, stem)
        distributions[stem] = {
            "dist_info": str(dist),
            "record": {
                "path": str(record),
                "sha256": file_digest(record),
                "rows": record_rows,
            },
            "direct_url": {
                "path": str(direct),
                "sha256": file_digest(direct),
                "value": direct_value,
            },
        }

    return {
        "child": str(child),
        "owner": owner,
        "markers": marker_values,
        "origin_marker": {"path": str(origin_marker), "sha256": file_digest(origin_marker)},
        "distribution_marker": {
            "path": str(distribution_marker),
            "sha256": file_digest(distribution_marker),
            "value": metadata,
        },
        "receipt": {"path": str(receipt), "sha256": file_digest(receipt), "kv": parse_kv_receipt(receipt)},
        "site_packages": str(site),
        "source_roots": {name: str(path.resolve()) for name, path in expected_sources.items()},
        "distributions": distributions,
        "authority": "managed child owner + source/runtime markers + provision receipt + canonical direct URLs + complete RECORDs",
    }


def profile_inputs(profile: Path, node: Path) -> dict[str, Any]:
    if profile != EXPECTED_PROFILE:
        raise PreflightFailure(f"profile root is not the approved 819acf profile: {profile}")
    if node != EXPECTED_NODE:
        raise PreflightFailure(f"Node executable is not the approved Node20 path: {node}")
    if not profile.is_dir() or profile.is_symlink():
        raise PreflightFailure(f"profile root is missing or symlinked: {profile}")
    if not node.is_file() or node.is_symlink():
        raise PreflightFailure(f"profile Node executable is missing or symlinked: {node}")
    locks = []
    for name, expected in EXPECTED_PROFILE_FILES.items():
        path = require_file(profile / name, "profile lock/input")
        actual = file_digest(path)
        if actual != expected:
            raise PreflightFailure(f"approved profile {name} is {actual}, expected {expected}")
        locks.append({"path": str(path), "sha256": actual, "bytes": path.stat().st_size})
    package = json.loads(require_file(profile / "package.json", "profile package manifest").read_text(encoding="utf-8"))
    dependency_spec = {
        **package.get("dependencies", {}),
        **package.get("devDependencies", {}),
    }
    package_lock = json.loads((profile / "package-lock.json").read_text(encoding="utf-8"))
    lock_packages = package_lock.get("packages", {})
    node_modules = profile / "node_modules"
    if not node_modules.is_dir() or node_modules.is_symlink():
        raise PreflightFailure(f"profile node_modules is missing or symlinked: {node_modules}")
    installed: dict[str, Any] = {}
    for dependency in sorted(dependency_spec):
        package_path = node_modules.joinpath(*dependency.split("/"))
        lock_key = f"node_modules/{dependency}"
        if lock_key not in lock_packages:
            raise PreflightFailure(f"profile lock lacks direct dependency {dependency}")
        if not package_path.is_dir() or package_path.is_symlink():
            raise PreflightFailure(f"required profile dependency is missing or symlinked: {dependency}")
        manifest = require_file(package_path / "package.json", f"{dependency} package manifest")
        value = json.loads(manifest.read_text(encoding="utf-8"))
        if value.get("name") != dependency:
            raise PreflightFailure(f"profile dependency manifest name mismatch: {dependency}")
        expected_version = lock_packages[lock_key].get("version")
        if expected_version is not None and value.get("version") != expected_version:
            raise PreflightFailure(f"profile dependency version mismatch: {dependency}")
        installed[dependency] = {"path": str(package_path), "version": value.get("version")}
    composition = dependency_spec.get("@banodoco/timeline-composition")
    if composition != "file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz":
        raise PreflightFailure("profile composition dependency is not the approved archive")
    archive = profile / composition.removeprefix("file:")
    require_file(archive, "Composition archive")
    archive_sha256 = file_digest(archive)
    if archive_sha256 != EXPECTED_ARCHIVE_SHA256:
        raise PreflightFailure(f"Composition archive is {archive_sha256}, expected {EXPECTED_ARCHIVE_SHA256}")
    composition_manifest = json.loads(
        require_file(node_modules / "@banodoco" / "timeline-composition" / "package.json", "Composition package manifest").read_text(
            encoding="utf-8"
        )
    )
    if composition_manifest.get("version") != "0.0.14":
        raise PreflightFailure("installed Composition package is not version 0.0.14")
    version = subprocess.check_output([str(node), "--version"], text=True, stderr=subprocess.STDOUT).strip()
    if version != EXPECTED_NODE_VERSION:
        raise PreflightFailure(f"profile Node is {version}, expected {EXPECTED_NODE_VERSION}")
    return {
        "root": str(profile),
        "node": str(node),
        "node_version": version,
        "locks": locks,
        "composition_archive": {"path": str(archive), "sha256": archive_sha256},
        "node_modules": {"path": str(node_modules), "required": installed},
    }


def controlled_env(child: Path, profile: dict[str, Any], scratch: Path) -> dict[str, str]:
    node = Path(profile["node"])
    remotion = Path(profile["root"])
    return {
        "HOME": os.environ.get("HOME", "/root"),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": f"{node.parent}:/usr/bin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "TMPDIR": str(scratch),
        "ASTRID_HOST_EXECUTION_PROFILE": "installed",
        "ASTRID_NODE_EXECUTABLE": str(node),
        "ASTRID_REMOTION_PROJECT_DIR": str(remotion),
        "ASTRID_TEST_NODE_MODULES": str(remotion / "node_modules"),
    }


def child_probe(child: Path, root: Path, env: dict[str, str]) -> dict[str, Any]:
    probe = (
        "import importlib, json, sys; "
        f"names={PREFIXES!r}; "
        "mods={}; "
        "for_name=None; "
        "[mods.__setitem__(name, (m:=importlib.import_module(name)).__file__) for name in names]; "
        "print(json.dumps({'executable':sys.executable,'prefix':sys.prefix,'path':sys.path,'modules':mods}, sort_keys=True))"
    )
    result = subprocess.run(
        [str(child / "bin/python"), "-P", "-c", probe],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise PreflightFailure(f"installed child import probe failed ({result.returncode}): {result.stderr.strip()}")
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PreflightFailure(f"installed child import probe was not JSON: {result.stdout!r}") from exc
    site = (child / "lib" / "python3.13" / "site-packages").resolve()
    origins = {}
    for name, filename in value.get("modules", {}).items():
        if not isinstance(filename, str):
            raise PreflightFailure(f"module has no file origin: {name}")
        resolved = Path(filename).resolve()
        if not resolved.is_relative_to(site):
            raise PreflightFailure(f"production module escaped managed site-packages: {name} -> {resolved}")
        origins[name] = {"file": filename, "realpath": str(resolved), "sha256": file_digest(resolved)}
    if set(origins) != set(PREFIXES):
        raise PreflightFailure(f"installed origin probe omitted modules: {set(PREFIXES) - set(origins)}")
    return {
        "probe_argv": [str(child / "bin/python"), "-P", "-c", probe],
        "result": value,
        "origins": origins,
        "observation_scope": "fresh child -P import probe; not an in-body observer",
    }


def source_after_check(root: Path, before: dict[str, Any]) -> dict[str, Any]:
    after = source_identity(root)
    if after != before:
        raise PreflightFailure("target source/function identity changed during run")
    return after


def preflight(args: argparse.Namespace, evidence: Path) -> dict[str, Any]:
    root = args.source_root.resolve()
    child = real_child(args.child_root)
    source = source_identity(root)
    git = git_identity(root)
    profile = profile_inputs(args.profile_root.resolve(), args.node.resolve())
    receipt = args.provision_receipt.resolve()
    custody = managed_custody(root, child, receipt)
    scratch = Path(args.tmpdir).resolve() if args.tmpdir else Path(os.environ.get("TMPDIR", "/tmp")).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    env = controlled_env(child, profile, scratch)
    forbidden = sorted(set(env) & {"PYTHONPATH", "PYTHONHOME", "PYTHONUSERBASE", "VIRTUAL_ENV", "LD_PRELOAD", "LD_LIBRARY_PATH", "NODE_PATH"})
    if forbidden:
        raise PreflightFailure(f"forbidden overlay environment keys: {forbidden}")
    origins = child_probe(child, root, env)
    record = {
        "status": "PASS",
        "body_runs": 0,
        "source": {"root": str(root), "git": git, "identity": source},
        "child": custody,
        "profile": profile,
        "production_origin_map": origins,
        "environment_keys": sorted(env),
        "environment_overlay_keys": forbidden,
        "checks": [
            "source HEAD and unchanged target test bind bb50",
            "owner, source/runtime markers and provision receipt bind the managed child",
            "astrid and astrid_runtime RECORD/direct_url are present and non-editable",
            "runtime_protocol and production modules import from managed site-packages under child -P",
            "Node20/profile lock inputs are present and hashed",
            "no PYTHONPATH or installed overlay is used",
        ],
    }
    write_json(evidence / "preflight.json", record)
    write_json(evidence / "source-before.json", {"git": git, "identity": source})
    write_json(evidence / "production-origins-before.json", origins)
    write_json(evidence / "profile-inputs-before.json", profile)
    write_json(evidence / "invocation-preflight.json", {"argv": sys.orig_argv, "cwd": str(Path.cwd())})
    return {"root": root, "child": child, "profile": profile, "env": env, "source": source}


def suite_row(junit: Path, nodeid: str, exit_code: int) -> dict[str, Any]:
    result: dict[str, Any] = {"nodeid": nodeid, "exit_code": exit_code, "junit": str(junit)}
    if not junit.is_file():
        result["outcome"] = "no-junit"
        return result
    root = ET.parse(junit).getroot()
    testcases = list(root.iter("testcase"))
    if len(testcases) != 1:
        result["outcome"] = "unexpected-testcase-count"
        result["testcase_count"] = len(testcases)
        return result
    case = testcases[0]
    result.update({"name": case.attrib.get("name"), "classname": case.attrib.get("classname")})
    result["outcome"] = "failed" if case.find("failure") is not None else "error" if case.find("error") is not None else "skipped" if case.find("skipped") is not None else "passed"
    return result


def run_original(args: argparse.Namespace, evidence: Path) -> int:
    script_digest = file_digest(SCRIPT)
    if args.reviewed_script_sha256 != script_digest:
        raise PreflightFailure("run-original requires the independently reviewed harness SHA")
    prepared = preflight(args, evidence)
    root = prepared["root"]
    child = prepared["child"]
    env = prepared["env"]
    target = f"{TEST_RELATIVE.as_posix()}::{TEST_FUNCTION}"
    junit = evidence / "junit.xml"
    command = [
        str(child / "bin/python"),
        "-P",
        "-m",
        "pytest",
        "--import-mode=importlib",
        "-q",
        "-oaddopts=",
        "-p",
        "no:cacheprovider",
        target,
        f"--junitxml={junit}",
    ]
    write_json(evidence / "invocation.json", {"argv": command, "cwd": str(root), "environment_keys": sorted(env)})
    write_bytes(
        evidence / "command.sh",
        ("env -i " + shlex.join([f"{k}={env[k]}" for k in sorted(env)] + command) + "\n").encode(),
    )
    write_json(evidence / "source-before.json", {"identity": prepared["source"], "script_sha256": script_digest})
    start = time.time()
    stdout: bytes = b""
    stderr: bytes = b""
    exit_code = 125
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=env,
            text=False,
            capture_output=True,
            timeout=args.timeout,
            check=False,
        )
        stdout, stderr, exit_code = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        exit_code = 124
        write_json(evidence / "timeout.json", {"timeout_seconds": args.timeout})
    except OSError as exc:
        write_json(evidence / "launch-error.json", {"error_type": type(exc).__name__, "error": str(exc)})
    finally:
        write_json(evidence / "timing.json", {"elapsed_seconds": time.time() - start})
    write_bytes(evidence / "stdout.txt", stdout)
    write_bytes(evidence / "stderr.txt", stderr)
    write_json(evidence / "exit.json", {"returncode": exit_code})
    try:
        after = source_after_check(root, prepared["source"])
        source_error = None
    except PreflightFailure as exc:
        try:
            after = source_identity(root)
        except PreflightFailure as after_exc:
            after = {"error": str(after_exc)}
        source_error = str(exc)
    write_json(evidence / "source-after.json", {"identity": after, "error": source_error})
    try:
        origins_after = child_probe(child, root, env)
    except PreflightFailure as exc:
        origins_after = {"error": str(exc)}
    write_json(evidence / "production-origins-after.json", origins_after)
    try:
        profile_after = profile_inputs(Path(prepared["profile"]["root"]), Path(prepared["profile"]["node"]))
    except PreflightFailure as exc:
        profile_after = {"error": str(exc)}
    write_json(evidence / "profile-inputs-after.json", profile_after)
    row = suite_row(junit, target, exit_code)
    write_json(evidence / "suite-row.json", row)
    if source_error:
        return 2
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "run-original"), nargs="?", default="preflight")
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--child-root", type=Path, required=True)
    parser.add_argument("--provision-receipt", type=Path, required=True)
    parser.add_argument("--profile-root", type=Path, default=Path("/home/user/work/runtimes/agent-remotion-v3-819acf-1110"))
    parser.add_argument("--node", type=Path, default=Path("/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"))
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--tmpdir", type=Path)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--reviewed-script-sha256")
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    write_json(evidence / "harness.json", {"path": str(SCRIPT), "sha256": file_digest(SCRIPT), "mode": args.mode})
    try:
        if args.mode == "preflight":
            preflight(args, evidence)
            print(json.dumps({"status": "PASS", "body_runs": 0, "evidence": str(evidence)}, indent=2))
            return 0
        if not args.reviewed_script_sha256:
            raise PreflightFailure("--reviewed-script-sha256 is required for run-original")
        status = run_original(args, evidence)
        print(json.dumps({"status": "BODY-RAN", "exit_code": status, "evidence": str(evidence)}, indent=2))
        return status
    except Exception as exc:  # noqa: BLE001 - durable failure evidence is contractual.
        failure = {
            "status": "PREFLIGHT-FAILED" if isinstance(exc, PreflightFailure) else "HARNESS-FAILED",
            "body_runs": 0,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "argv": sys.orig_argv,
            "cwd": str(Path.cwd()),
            "script_sha256": file_digest(SCRIPT),
            "source_root": str(args.source_root.resolve()),
            "child_root": str(args.child_root.resolve()),
        }
        try:
            failure["source_identity"] = source_identity(args.source_root.resolve())
        except Exception as source_exc:  # noqa: BLE001 - retain the primary failure.
            failure["source_identity_error"] = f"{type(source_exc).__name__}: {source_exc}"
        write_json(evidence / "failure.json", failure)
        write_json(
            evidence / "suite-row.json",
            {
                "nodeid": f"{TEST_RELATIVE.as_posix()}::{TEST_FUNCTION}",
                "outcome": "preflight-refused",
                "exit_code": 2,
                "body_runs": 0,
            },
        )
        print(json.dumps(failure, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
