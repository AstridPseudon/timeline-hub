"""Preparation helpers for the named D13 native qualification.

This module contains only the existing test opt-in and resource checks.  It
does not start Runtime, create credentials, claim work, or execute the native
proof.  The later proof imports ``installed_profile`` and obtains Runtime
credentials from its normal ephemeral bootstrap.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import tarfile
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from astrid.core.execution.generic_host import source_checkout_digest

_PROFILE_KEYS = frozenset(
    {"profile", "runtime_checkout", "source_checkout", "runtime_environment"}
)
_BINDING_KEYS = frozenset(
    {
        "agent_commit",
        "agent_tree",
        "agent_wheel",
        "agent_wheel_sha256",
        "source_checkout",
        "source_digest",
        "runtime_environment",
    }
)
_REQUIRED_ORIGINS = (
    "host",
    "child",
    "action",
    "client",
    "sdk",
    "runtime_protocol",
    "runtime_protocol.platform",
    "astrid_runtime",
)
_FORBIDDEN_ENV_PREFIXES = ("LD_",)
_FORBIDDEN_ENV = frozenset(
    {"NODE_OPTIONS", "NODE_PATH", "PYTHONHOME", "PYTHONPATH", "ASTRID_RUNTIME_CHECKOUT"}
)
_NATIVE_TEST = (
    "tests/packs/video_editing/test_runtime_publication_chain.py::"
    "test_daemon_backed_host_executes_authoring_and_final_render"
)
_MAX_SOCKET_PATH = 100


@dataclass(frozen=True)
class D13Inputs:
    """Existing D13 bindings plus manager-selected, non-profile resources."""

    profile: Path
    bindings: Path
    source: Path
    environment: Path
    agent_commit: str
    agent_tree: str
    agent_wheel: Path
    agent_wheel_sha256: str
    source_digest: str
    node: Path
    node_sha256: str
    remotion: Path
    remotion_lock_sha256: str
    browser: Path
    browser_sha256: str
    ffmpeg: Path
    ffmpeg_sha256: str
    ffprobe: Path
    ffprobe_sha256: str
    node_modules: Path


def _required(name: str, failures: list[str]) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        failures.append(f"missing required D13 test input: {name}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _record_digest(data: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")


def _record_rows(text: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for row in csv.reader(text.splitlines()):
        if len(row) != 3 or not row[0] or row[0] in rows:
            raise ValueError("malformed or duplicate RECORD row")
        rows[row[0]] = (row[1], row[2])
    return rows


def load_inputs() -> tuple[D13Inputs | None, list[str]]:
    """Load the existing profile and seven-key bindings carrier.

    The JSON carriers remain deliberately path/hash based.  Runtime identity,
    project scope, task scope, and credentials are not represented here.
    """
    failures: list[str] = []
    profile = Path(_required("ASTRID_D13_SOURCE_PROFILE", failures))
    bindings = Path(_required("ASTRID_D13_EXPECTED_BINDINGS", failures))
    values: dict[str, str] = {}
    if not bindings.is_file() or bindings.is_symlink():
        failures.append(f"D13 bindings JSON is not a regular file: {bindings}")
    else:
        try:
            raw = json.loads(bindings.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            failures.append(f"D13 bindings JSON is unreadable: {exc}")
        else:
            if (
                not isinstance(raw, dict)
                or set(raw) != _BINDING_KEYS
                or any(not isinstance(value, str) or not value.strip() for value in raw.values())
            ):
                failures.append("D13 bindings JSON must contain exactly the existing seven non-empty string keys")
            else:
                values = {key: value.strip() for key, value in raw.items()}

    if any(not values.get(key) for key in _BINDING_KEYS):
        failures.extend(f"D13 bindings JSON missing {key}" for key in sorted(_BINDING_KEYS - values.keys()))

    def value(key: str) -> str:
        return values.get(key, "")

    try:
        inputs = D13Inputs(
            profile=profile,
            bindings=bindings,
            source=Path(value("source_checkout")),
            environment=Path(value("runtime_environment")),
            agent_commit=value("agent_commit"),
            agent_tree=value("agent_tree"),
            agent_wheel=Path(value("agent_wheel")),
            agent_wheel_sha256=value("agent_wheel_sha256"),
            source_digest=value("source_digest"),
            node=Path(_required("ASTRID_NODE_EXECUTABLE", failures)),
            node_sha256=_required("ASTRID_D13_NODE_SHA256", failures),
            remotion=Path(_required("ASTRID_REMOTION_PROJECT_DIR", failures)),
            remotion_lock_sha256=_required("ASTRID_D13_REMOTION_LOCK_SHA256", failures),
            browser=Path(_required("ASTRID_REMOTION_BROWSER_EXECUTABLE", failures)),
            browser_sha256=_required("ASTRID_D13_BROWSER_SHA256", failures),
            ffmpeg=Path(_required("ASTRID_FFMPEG_EXECUTABLE", failures)),
            ffmpeg_sha256=_required("ASTRID_D13_FFMPEG_SHA256", failures),
            ffprobe=Path(_required("ASTRID_FFPROBE_EXECUTABLE", failures)),
            ffprobe_sha256=_required("ASTRID_D13_FFPROBE_SHA256", failures),
            node_modules=Path(_required("ASTRID_TEST_NODE_MODULES", failures)),
        )
    except (TypeError, ValueError):
        return None, failures
    return inputs, failures


def _safe_path(path: Path, label: str, failures: list[str]) -> None:
    if not path.is_absolute() or path.is_symlink() or not path.exists():
        failures.append(f"{label} is unavailable, non-absolute, or symlinked: {path}")
    if any(parent.is_symlink() for parent in (path, *path.parents)):
        failures.append(f"{label} traverses a symlink: {path}")


def _profile_failures(inputs: D13Inputs, profile: Mapping[str, object]) -> list[str]:
    failures: list[str] = []
    if set(profile) != _PROFILE_KEYS:
        failures.append(f"profile must retain exactly four existing keys: {sorted(profile)}")
        return failures
    if profile.get("profile") != "astrid":
        failures.append("profile id is not astrid")
    selected_source = Path(str(profile["source_checkout"]))
    selected_runtime = Path(str(profile["runtime_checkout"]))
    selected_environment = Path(str(profile["runtime_environment"]))
    if selected_source.resolve() != inputs.source.resolve():
        failures.append(f"profile source differs from bindings: {selected_source} != {inputs.source}")
    if selected_runtime.resolve() != inputs.source.resolve():
        failures.append(f"profile runtime differs from bindings: {selected_runtime} != {inputs.source}")
    if selected_environment.resolve() != inputs.environment.resolve():
        failures.append(
            f"profile environment differs from bindings: {selected_environment} != {inputs.environment}"
        )
    for label, path in (
        ("profile source", selected_source),
        ("profile runtime", selected_runtime),
        ("profile environment", selected_environment),
    ):
        _safe_path(path, label, failures)
    interpreter = selected_environment / "bin" / "python"
    _safe_path(interpreter, "selected interpreter", failures)
    if interpreter.is_file() and Path(os.sys.executable).resolve() != interpreter.resolve():
        failures.append(f"pytest interpreter differs from selected interpreter: {os.sys.executable} != {interpreter}")
    try:
        from astrid.sdk.host_bootstrap import _installed_execution_origins

        origins = _installed_execution_origins(selected_source, str(interpreter))
    except (AttributeError, ImportError, KeyError, OSError, TypeError, ValueError) as exc:
        failures.append(f"installed origin probe failed: {exc}")
    else:
        for name in _REQUIRED_ORIGINS:
            origin = origins.get(name)
            if not origin:
                failures.append(f"installed origin missing: {name}")
            elif not Path(origin).resolve().is_relative_to(selected_source.resolve()):
                failures.append(f"installed origin escaped selected tree: {name}={origin}")
    return failures


def _wheel_failures(inputs: D13Inputs) -> list[str]:
    failures: list[str] = []
    wheel = inputs.agent_wheel
    if not wheel.is_file() or wheel.is_symlink():
        return [f"Agent wheel is unavailable or symlinked: {wheel}"]
    if _sha256(wheel) != inputs.agent_wheel_sha256:
        failures.append("Agent wheel hash differs from bindings")
    try:
        with zipfile.ZipFile(wheel) as archive:
            record_names = [name for name in archive.namelist() if name.endswith(".dist-info/RECORD")]
            if len(record_names) != 1:
                return failures + [f"Agent wheel must contain exactly one RECORD, found {len(record_names)}"]
            record_name = record_names[0]
            rows = _record_rows(archive.read(record_name).decode("utf-8"))
            members = {name for name in archive.namelist() if not name.endswith("/")}
            if set(rows) != members:
                failures.append("Agent wheel RECORD does not enumerate exactly its members")
            wheel_bytes = {name: archive.read(name) for name in members if name != record_name}
    except (OSError, UnicodeDecodeError, ValueError, zipfile.BadZipFile) as exc:
        return failures + [f"Agent wheel RECORD is unreadable: {exc}"]

    record_path = Path(record_name)
    if record_path.is_absolute() or ".." in record_path.parts or "" in record_name.split("/"):
        return failures + [f"Agent wheel RECORD contains an unsafe path: {record_name}"]
    installed_record = inputs.source / record_path
    if not installed_record.is_file() or installed_record.is_symlink():
        return failures + [f"installed Agent RECORD is missing or symlinked: {installed_record}"]
    try:
        installed_rows = _record_rows(installed_record.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return failures + [f"installed Agent RECORD is unreadable: {exc}"]
    for name, (expected_hash, expected_size) in rows.items():
        if name == record_name:
            if expected_hash or expected_size:
                failures.append("Agent RECORD must leave its own row unhashed")
            continue
        target = inputs.source / Path(name)
        if not target.is_file() or target.is_symlink():
            failures.append(f"installed Agent RECORD member is missing: {name}")
            continue
        data = target.read_bytes()
        if str(len(data)) != expected_size or _record_digest(data) != expected_hash.removeprefix("sha256="):
            failures.append(f"installed Agent RECORD hash/size differs: {name}")
        if name in wheel_bytes and data != wheel_bytes[name]:
            failures.append(f"installed Agent package bytes differ from wheel: {name}")
        if installed_rows.get(name) != (expected_hash, expected_size):
            failures.append(f"installed Agent RECORD row differs from wheel: {name}")
    return failures


def _resource_failures(inputs: D13Inputs) -> list[str]:
    failures: list[str] = []
    for label, path, digest in (
        ("node", inputs.node, inputs.node_sha256),
        ("Remotion package lock", inputs.remotion / "package-lock.json", inputs.remotion_lock_sha256),
        ("browser", inputs.browser, inputs.browser_sha256),
        ("ffmpeg", inputs.ffmpeg, inputs.ffmpeg_sha256),
        ("ffprobe", inputs.ffprobe, inputs.ffprobe_sha256),
    ):
        _safe_path(path, label, failures)
        if path.is_file() and not path.is_symlink() and _sha256(path) != digest:
            failures.append(f"{label} hash differs from bindings: {path}")
    _safe_path(inputs.remotion, "Remotion project", failures)
    _safe_path(inputs.node_modules, "Remotion node_modules", failures)
    fonts = inputs.remotion / "public" / "fonts"
    if not (fonts / "FONT_PROVENANCE.md").is_file():
        failures.append("Remotion font provenance is unavailable")
    if not tuple(fonts.glob("*.woff2")) or any(not font.is_file() or font.stat().st_size == 0 for font in fonts.glob("*.woff2")):
        failures.append("Remotion font closure is empty or invalid")
    return failures


def installed_profile(tmp_path: Path) -> tuple[D13Inputs, dict[str, object], dict[str, str]]:
    """Validate the selected profile and return it without starting anything."""
    inputs, failures = load_inputs()
    if inputs is None:
        raise AssertionError("; ".join(failures))
    if not inputs.profile.is_file() or inputs.profile.is_symlink():
        failures.append(f"profile is not a regular file: {inputs.profile}")
        profile: dict[str, object] = {}
    else:
        try:
            profile = json.loads(inputs.profile.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            failures.append(f"profile is unreadable: {exc}")
            profile = {}
    if not isinstance(profile, dict):
        failures.append("profile is not a JSON object")
        profile = {}
    failures.extend(_profile_failures(inputs, profile))
    failures.extend(_wheel_failures(inputs))
    failures.extend(_resource_failures(inputs))
    if shutil.disk_usage(tmp_path).free < 5 * 1024**3:
        failures.append("free disk is below the existing 5 GiB test guard")
    attempt = tmp_path / "d13-preflight-attempt"
    attempt.mkdir()
    probe = attempt / "writable-probe"
    probe.write_text("d13", encoding="utf-8")
    if probe.read_text(encoding="utf-8") != "d13" or probe.is_symlink():
        failures.append("private D13 attempt root is not writable and isolated")
    if failures:
        raise AssertionError("; ".join(failures))
    return inputs, profile, {
        "source": str(inputs.source.resolve()),
        "source_digest": source_checkout_digest(inputs.source),
        "node": _sha256(inputs.node),
        "remotion_package_lock": _sha256(inputs.remotion / "package-lock.json"),
        "browser": _sha256(inputs.browser),
        "ffmpeg": _sha256(inputs.ffmpeg),
        "ffprobe": _sha256(inputs.ffprobe),
    }


def isolated_environment(inputs: D13Inputs, *, home: Path, tmpdir: Path) -> dict[str, str]:
    """Build the existing env -i child environment for later named tests."""
    if not tmpdir.is_absolute() or len(str(tmpdir)) >= _MAX_SOCKET_PATH:
        raise ValueError("D13 per-run temp root must be an absolute short path")
    env = {
        "HOME": str(home),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": f"{inputs.node.parent}:{inputs.environment / 'bin'}:/usr/bin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
        "TMPDIR": str(tmpdir),
        "XDG_RUNTIME_DIR": str(tmpdir),
        "ASTRID_D13_SOURCE_PROFILE": str(inputs.profile),
        "ASTRID_D13_EXPECTED_BINDINGS": str(inputs.bindings),
        "ASTRID_D13_NODE_SHA256": inputs.node_sha256,
        "ASTRID_D13_REMOTION_LOCK_SHA256": inputs.remotion_lock_sha256,
        "ASTRID_D13_BROWSER_SHA256": inputs.browser_sha256,
        "ASTRID_D13_FFMPEG_SHA256": inputs.ffmpeg_sha256,
        "ASTRID_D13_FFPROBE_SHA256": inputs.ffprobe_sha256,
        "ASTRID_HOST_EXECUTION_PROFILE": "installed",
        "ASTRID_PACK_HOST_PYTHON": str(inputs.environment / "bin" / "python"),
        "ASTRID_PACKS_PATH": str(inputs.source / "astrid" / "packs" / "rendering"),
        "ASTRID_REMOTION_PROJECT_DIR": str(inputs.remotion),
        "ASTRID_REMOTION_BROWSER_EXECUTABLE": str(inputs.browser),
        "ASTRID_NODE_EXECUTABLE": str(inputs.node),
        "ASTRID_TEST_NODE_MODULES": str(inputs.node_modules),
        "ASTRID_FFMPEG_EXECUTABLE": str(inputs.ffmpeg),
        "ASTRID_FFPROBE_EXECUTABLE": str(inputs.ffprobe),
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": str(inputs.source),
        "ASTRID_RUNTIME_SOURCE_MANIFEST": str(inputs.profile),
    }
    assert not any(name in _FORBIDDEN_ENV or any(name.startswith(prefix) for prefix in _FORBIDDEN_ENV_PREFIXES) for name in env)
    return env


def named_collection_command(
    inputs: D13Inputs,
    source_root: Path,
    *,
    runtime_checkout: Path,
    run_root: Path,
) -> tuple[list[str], dict[str, str]]:
    """Return, but do not execute, the existing named C13 collection command.

    The command is run from ``source_root`` by its caller.  Its test selector
    is relative so a recycled worker worktree cannot enter the exported argv;
    Runtime's checkout selector is explicit and remains separate from the
    installed Agent source selected by the profile.
    """
    if not source_root.is_absolute() or not source_root.is_dir():
        raise ValueError("D13 source root must be an existing absolute directory")
    if not runtime_checkout.is_absolute() or not runtime_checkout.is_dir() or runtime_checkout.is_symlink():
        raise ValueError("D13 Runtime checkout must be an existing regular directory")
    if not run_root.is_absolute() or len(str(run_root)) >= _MAX_SOCKET_PATH:
        raise ValueError("D13 per-run root must be an absolute short path")
    env = isolated_environment(inputs, home=run_root / "home", tmpdir=run_root / "tmp")
    env.update({"ASTRID_RUNTIME_CHECKOUT": str(runtime_checkout)})
    command = [
        str(inputs.environment / "bin" / "python"),
        "-B",
        "-m",
        "pytest",
        "-o",
        "addopts=",
        "-p",
        "no:cacheprovider",
        _NATIVE_TEST,
        "--collect-only",
        "-q",
    ]
    return command, env


def source_archive_matches_checkout(inputs: D13Inputs, checkout: Path) -> list[str]:
    """Check the f4ed source archive against the selected wheel without imports."""
    failures: list[str] = []
    commit = inputs.agent_commit.lower()

    def git(*args: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", "-C", str(checkout), *args], check=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    if git("rev-parse", "--verify", f"{commit}^{{commit}}").returncode != 0:
        return [f"Agent commit is unavailable in exact checkout: {commit}"]
    tree = git("rev-parse", "--verify", f"{commit}^{{tree}}").stdout.decode().strip()
    if tree != inputs.agent_tree.lower():
        failures.append(f"Agent tree differs from binding: {tree} != {inputs.agent_tree}")
    try:
        with tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", commit, "--", "astrid").stdout), mode="r:") as archive:
            source = {
                item.name.removeprefix("./"): archive.extractfile(item).read()
                for item in archive.getmembers()
                if item.isfile() and item.name.removeprefix("./").startswith("astrid/")
            }
        with zipfile.ZipFile(inputs.agent_wheel) as wheel:
            for name in wheel.namelist():
                if name.startswith("astrid/") and not name.endswith("/") and wheel.read(name) != source.get(name):
                    failures.append(f"Agent wheel differs from exact f4ed checkout: {name}")
    except (OSError, KeyError, tarfile.TarError, zipfile.BadZipFile) as exc:
        failures.append(f"Agent source/wheel parity could not be checked: {exc}")
    return failures
