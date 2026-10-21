"""Prove the current Agent candidate is usable from an installed Runtime."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig
import tarfile
import zipfile

import pytest


AGENT_COMMIT = "68dc081cb563e99cf38d7926dd6f3ed840514682"
AGENT_TREE = "c04a3d3a52af275988026959f370c53cb212f44d"
RUNTIME_COMMIT = "8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a"
RUNTIME_TREE = "3ea37d662116b6231605d7d2b83f66560a6130c3"
RUNTIME_REPOSITORY = Path("/home/user/banodoco/banodoco-workspace-runtime")
CONTRACT_VERSION = "0.2.14"
SCHEMA_DIGEST = "sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816"


def _git(repository: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), *args], text=True
    ).strip()


def _archive(repository: Path, revision: str, destination: Path, *paths: str) -> None:
    destination.mkdir(parents=True)
    process = subprocess.Popen(
        ["git", "-C", str(repository), "archive", revision, *paths],
        stdout=subprocess.PIPE,
    )
    assert process.stdout is not None
    with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
        if sys.version_info >= (3, 12):
            archive.extractall(destination, filter="data")
        else:
            archive.extractall(destination)
    assert process.wait() == 0


def _build_wheel(source: Path, wheelhouse: Path, builder: str) -> Path:
    wheelhouse.mkdir(parents=True)
    build_env = os.environ.copy()
    if builder != sys.executable:
        build_env["SETUPTOOLS_USE_DISTUTILS"] = "stdlib"
    else:
        build_env.pop("SETUPTOOLS_USE_DISTUTILS", None)
    subprocess.run(
        [
            builder,
            "-m",
            "pip",
            "wheel",
            "--no-cache-dir",
            "--no-index",
            "--no-build-isolation",
            "--no-deps",
            "--wheel-dir",
            str(wheelhouse),
            str(source),
        ],
        cwd=source,
        check=True,
        env=build_env,
    )
    wheels = sorted(wheelhouse.glob("*.whl"))
    assert len(wheels) == 1
    return wheels[0]


def _builder() -> str:
    for candidate in (sys.executable, "python3.11", "python3.12", "python3.13", "python3"):
        try:
            result = subprocess.run(
                [candidate, "-c", "import setuptools.build_meta"],
                capture_output=True,
                check=False,
            )
        except OSError:
            continue
        if result.returncode == 0:
            return candidate
    raise RuntimeError("WC10 installed compatibility needs a setuptools build interpreter")


def _link_dependencies(environment: Path) -> None:
    fixture_site = Path(
        subprocess.check_output(
            [
                str(environment / "bin" / "python"),
                "-c",
                "import sysconfig; print(sysconfig.get_paths()['purelib'])",
            ],
            text=True,
        ).strip()
    )
    shared_site = Path(sysconfig.get_paths()["purelib"])
    for pattern in (
        "attr",
        "attrs",
        "attrs-*.dist-info",
        "jsonschema",
        "jsonschema-*.dist-info",
        "jsonschema_specifications",
        "jsonschema_specifications-*.dist-info",
        "referencing",
        "referencing-*.dist-info",
        "rpds",
        "rpds_py-*.dist-info",
        "typing_extensions.py",
        "typing_extensions-*.dist-info",
        "yaml",
        "pyyaml-*.dist-info",
    ):
        matches = sorted(shared_site.glob(pattern))
        assert matches, f"shared dependency is unavailable: {pattern}"
        for source in matches:
            target = fixture_site / source.name
            if not target.exists() and not target.is_symlink():
                target.symlink_to(source, target_is_directory=source.is_dir())


@pytest.mark.integration
def test_wc10_current_agent_provider_is_installed_compatible(tmp_path: Path) -> None:
    """Build both reviewed sources and validate the installed provider ABI."""
    agent_repository = Path(__file__).resolve().parents[2]
    assert _git(agent_repository, "rev-parse", f"{AGENT_COMMIT}^{{tree}}") == AGENT_TREE
    assert _git(RUNTIME_REPOSITORY, "rev-parse", f"{RUNTIME_COMMIT}^{{tree}}") == RUNTIME_TREE

    agent_source = tmp_path / "agent-source"
    _archive(
        agent_repository,
        AGENT_COMMIT,
        agent_source,
        "LICENSE",
        "pyproject.toml",
        "astrid",
        "astrid_runtime_client",
    )
    runtime_source = tmp_path / "runtime-source"
    _archive(
        RUNTIME_REPOSITORY,
        RUNTIME_COMMIT,
        runtime_source,
        "LICENSE",
        "pyproject.toml",
        "setup.py",
        "astrid_runtime",
        "runtime_protocol",
        "packages/python/pyproject.toml",
        "packages/python/astrid_runtime_client",
    )
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    builder = _builder()
    agent_wheel = _build_wheel(agent_source, wheelhouse / "agent", builder)
    client_wheel = _build_wheel(
        runtime_source / "packages/python", wheelhouse / "client", builder
    )
    runtime_wheel = _build_wheel(runtime_source, wheelhouse / "runtime", builder)

    environment = tmp_path / "environment"
    subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
    pip = environment / "bin" / "pip"
    subprocess.run(
        [
            str(pip),
            "install",
            "--no-index",
            "--no-deps",
            "--force-reinstall",
            str(agent_wheel),
            str(client_wheel),
            str(runtime_wheel),
        ],
        check=True,
    )
    _link_dependencies(environment)

    probe = f"""
import inspect
import json
from pathlib import Path
import sys

import astrid
import astrid_runtime_client
import runtime_protocol
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

site = Path(sys.prefix).resolve()
locations = [
    Path(astrid.__file__).resolve(),
    Path(astrid_runtime_client.__file__).resolve(),
    Path(runtime_protocol.__file__).resolve(),
]
assert all(path.is_relative_to(site) for path in locations), locations
assert astrid_runtime_client.contract_metadata.CONTRACT_VERSION == {CONTRACT_VERSION!r}
assert astrid_runtime_client.contract_metadata.SCHEMA_DIGEST == {SCHEMA_DIGEST!r}
provider = load_timeline_commit_provider("astrid")
assert provider.provider_id == "astrid-v1"
assert provider.contract_digest == runtime_protocol.contract_metadata.SCHEMA_DIGEST
assert len(inspect.signature(provider.commit).parameters) == 2
print(json.dumps({{"locations": [str(path) for path in locations],
                  "provider": provider.provider_id}}))
"""
    result = subprocess.run(
        [str(environment / "bin" / "python"), "-I", "-B", "-c", probe],
        cwd=tmp_path,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["provider"] == "astrid-v1"

    with zipfile.ZipFile(agent_wheel) as wheel:
        assert "astrid/sdk/timeline/commit.py" in wheel.namelist()
        assert "astrid_runtime_client/contract_metadata.py" in wheel.namelist()

