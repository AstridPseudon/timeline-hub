from __future__ import annotations

import shutil
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tests.process_groups import ProcessGroups


@pytest.fixture
def owned_process_groups():
    """Own process groups explicitly launched by this test."""
    owner = ProcessGroups()
    try:
        yield owner
    finally:
        owner.terminate_all()


def pytest_sessionfinish(session, exitstatus):
    """Catch a CLI daemon that outlived its pytest child fixture."""
    _ = exitstatus
    try:
        basetemp = Path(session.config._tmp_path_factory.getbasetemp()).resolve()
        listing = subprocess.run(
            ["ps", "-axo", "pid=,pgid=,command="], capture_output=True, text=True, check=True
        ).stdout
    except (AttributeError, OSError, subprocess.CalledProcessError) as exc:
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter is not None:
            reporter.write_line(f"WARNING: daemon/host session guard could not inspect processes: {exc}")
        return
    leaked: list[tuple[int, int, str]] = []
    for line in listing.splitlines():
        fields = line.strip().split(None, 2)
        if len(fields) != 3:
            continue
        try:
            pid, pgid = int(fields[0]), int(fields[1])
        except ValueError:
            continue
        command = fields[2]
        is_runtime = "runtime_protocol" in command and "start" in command and "--root" in command
        is_host = "generic_host" in command and "--support-root" in command
        if not (is_runtime or is_host):
            continue
        roots = []
        tokens = command.split()
        for option in ("--root", "--support-root"):
            if option in tokens and tokens.index(option) + 1 < len(tokens):
                roots.append(tokens[tokens.index(option) + 1].strip("'\""))
            roots.extend(token.split("=", 1)[1].strip("'\"") for token in tokens if token.startswith(option + "="))
        if any(_under(root, basetemp) for root in roots):
            leaked.append((pid, pgid, command))
    if not leaked:
        return
    groups = {pgid for _, pgid, _ in leaked if pgid != os.getpgrp()}
    for pgid in groups:
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline and any(_group_exists(pgid) for pgid in groups):
        time.sleep(0.02)
    for pgid in groups:
        if _group_exists(pgid):
            try:
                os.killpg(pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is not None:
        reporter.write_line(f"ERROR: killed daemon/host processes left under pytest basetemp: {leaked!r}")
    session.exitstatus = pytest.ExitCode.TESTS_FAILED


def _under(candidate: str, parent: Path) -> bool:
    try:
        return Path(candidate).resolve().is_relative_to(parent)
    except (OSError, ValueError):
        return False


def _group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


@pytest.fixture(scope="session")
def stage1_runtime_environment(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One offline venv containing both installed runtime packages.

    The test runner may be a development Python without setuptools (notably
    the system 3.14 build on this host).  Build local wheels with whichever
    available interpreter has the build backend, then install those wheels
    into the clean target venv without consulting a package index.
    """
    root = Path(__file__).resolve().parents[1]
    environment = tmp_path_factory.mktemp("stage1-runtime") / "venv"
    wheelhouse = environment.parent / "wheelhouse"
    generated = (
        root / "build",
        root / "banodoco_workspace_runtime.egg-info",
        root / "banodoco_workspace_client.egg-info",
        root / "packages" / "python" / "build",
        root / "packages" / "python" / "banodoco_workspace_client.egg-info",
    )
    existed = {path: path.exists() for path in generated}
    try:
        builders = [sys.executable, "python3.11", "python3.12", "python3.13", "python3", "python"]
        builder = None
        for candidate in builders:
            try:
                probe = subprocess.run(
                    [candidate, "-c", "import setuptools.build_meta"],
                    capture_output=True,
                    check=False,
                )
            except OSError:
                continue
            if probe.returncode == 0:
                builder = candidate
                break
        if builder is None:
            raise RuntimeError("Stage 1 tests require an available Python with setuptools.build_meta")
        subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
        wheelhouse.mkdir()
        subprocess.run(
            [builder, "-m", "pip", "wheel", "--no-index", "--no-build-isolation", "--no-deps", "--wheel-dir", str(wheelhouse), str(root), str(root / "packages" / "python")],
            cwd=str(root),
            check=True,
        )
        pip = environment / "bin" / "pip"
        wheels = sorted(wheelhouse.glob("*.whl"))
        if len(wheels) != 2:
            raise RuntimeError(f"expected two local Stage 1 wheels, found {len(wheels)}")
        # The prepared interpreter may carry an editable checkout of this
        # project.  Force-install the exact wheels into the fresh child venv so
        # pip cannot mistake that outer editable metadata for an installed
        # package and silently omit one of the two runtime components.
        subprocess.run(
            [str(pip), "install", "--no-index", "--no-deps", "--force-reinstall", *(str(wheel) for wheel in wheels)],
            check=True,
        )
        yield environment
    finally:
        for path, was_present in existed.items():
            if not was_present and path.is_dir():
                shutil.rmtree(path)
