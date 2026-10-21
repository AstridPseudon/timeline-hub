"""One installed-host proof for the normal Astrid launcher profile."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig

import pytest


AGENT_COMMIT = "6efc81500a0e0688c2bb41e736503f0fc3e04abb"
AGENT_TREE = "2ed2b8a12b5b3391ca221ba6ff05390f71a73556"
AGENT_SOURCE = Path("/home/user/work/wt/agt-pin-6efc8150")


def _python(environment: Path) -> Path:
    return environment / "bin" / "python"


def _run(argv: list[str | Path], *, env: dict[str, str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(part) for part in argv], env=env, text=True, **kwargs)


def _git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def _build_agent_wheel(tmp_path: Path, environment: Path) -> None:
    """Build the exact Agent source from a private, non-editable copy."""
    source = tmp_path / "agent-wheel-source"
    source.mkdir()
    for filename in ("pyproject.toml",):
        shutil.copy2(AGENT_SOURCE / filename, source / filename)
    shutil.copytree(
        AGENT_SOURCE / "astrid",
        source / "astrid",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copytree(
        AGENT_SOURCE / "astrid_runtime_client",
        source / "astrid_runtime_client",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    wheelhouse = tmp_path / "agent-wheelhouse"
    wheelhouse.mkdir()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-index",
            "--no-build-isolation",
            "--no-deps",
            "--wheel-dir",
            str(wheelhouse),
            str(source),
        ],
        check=True,
    )
    wheels = sorted(wheelhouse.glob("astrid-*.whl"))
    assert len(wheels) == 1
    pip = environment / "bin" / "pip"
    subprocess.run(
        [str(pip), "install", "--no-index", "--no-deps", "--force-reinstall", str(wheels[0])],
        check=True,
    )


def _installed_identity(environment: Path) -> dict[str, str]:
    probe = """
import json
from pathlib import Path
import astrid
import astrid_runtime_client
import runtime_protocol
print(json.dumps({
    "astrid": str(Path(astrid.__file__).resolve()),
    "client": str(Path(astrid_runtime_client.__file__).resolve()),
    "runtime": str(Path(runtime_protocol.__file__).resolve()),
    "contract": astrid_runtime_client.contract_metadata.CONTRACT_VERSION,
    "schema": astrid_runtime_client.contract_metadata.SCHEMA_DIGEST,
}))
"""
    result = subprocess.run(
        [_python(environment), "-B", "-c", probe],
        check=True,
        capture_output=True,
        text=True,
        cwd=environment.parent,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
    )
    return json.loads(result.stdout)


def _link_runtime_dependencies(environment: Path) -> None:
    """Expose only shared dependency bytes through private fixture symlinks."""
    fixture_site = Path(
        subprocess.check_output(
            [_python(environment), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"],
            text=True,
        ).strip()
    )
    shared_site = Path(sysconfig.get_paths()["purelib"])
    names = (
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
    )
    for pattern in names:
        matches = sorted(shared_site.glob(pattern))
        assert matches, f"shared dependency is unavailable: {pattern}"
        for source in matches:
            target = fixture_site / source.name
            if not target.exists() and not target.is_symlink():
                target.symlink_to(source, target_is_directory=source.is_dir())


@pytest.mark.integration
def test_wc10_installed_normal_launcher_provider_bootstrap(tmp_path, stage1_runtime_environment):
    """Launch the installed Runtime and create/read one provider-backed empty timeline."""
    assert _git(AGENT_SOURCE, "rev-parse", "HEAD") == AGENT_COMMIT
    assert _git(AGENT_SOURCE, "rev-parse", "HEAD^{tree}") == AGENT_TREE
    assert not _git(AGENT_SOURCE, "status", "--porcelain")

    environment = stage1_runtime_environment
    _build_agent_wheel(tmp_path, environment)
    _link_runtime_dependencies(environment)
    identity = _installed_identity(environment)
    site_packages = Path(identity["runtime"]).parent.parent
    assert site_packages == Path(identity["client"]).parent.parent
    assert site_packages == Path(identity["astrid"]).parent.parent
    assert identity["contract"] == "0.2.14"
    assert identity["schema"] == "sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816"

    support = tmp_path / "support"
    manifest = tmp_path / "astrid-profile.json"
    manifest.write_text(
        json.dumps(
            {
                "profile": "astrid",
                "runtime_checkout": str(site_packages),
                "source_checkout": str(site_packages),
                "runtime_environment": str(environment),
            }
        ),
        encoding="utf-8",
    )
    child_env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        environment / "bin" / "astrid-runtime",
        "--profile",
        "astrid",
        "--data-root",
        support,
        "--source-manifest",
        manifest,
        "--hosted-origin",
        "https://hosted.test",
        "--json",
    ]
    created = _run(
        [*command[:1], "workspace", "create", "--realm-root", support / "runtime" / "realms" / "wc10",
         "--realm-id", "wc10", *command[1:]],
        env=child_env,
        capture_output=True,
        cwd=tmp_path,
    )
    assert created.returncode == 0, created.stderr + created.stdout
    started = None
    try:
        started = _run([*command[:1], "up", "--wait", "--door-port", "0", *command[1:]],
                       env=child_env, capture_output=True, cwd=tmp_path, timeout=90)
        assert started.returncode == 0, started.stderr + started.stdout
        ready = json.loads(started.stdout)
        assert ready["realm_id"] == "wc10"
        assert ready["door_endpoint"].startswith("http://127.0.0.1:")

        status = _run(
            [*command[:1], "status", "--data-root", support, "--json"],
            env=child_env,
            capture_output=True,
            cwd=tmp_path,
        )
        assert status.returncode == 0, status.stderr + status.stdout
        status_json = json.loads(status.stdout)
        assert status_json["support"]["healthy"] is True
        assert status_json["health"]["status"] == "ok"

        operation = """
import json, sys
from pathlib import Path
from astrid.sdk.workspace_client import WorkspaceClient

credential = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
client = WorkspaceClient(sys.argv[1], credential["token"])
health = client.health()
assert health["status"] == "ok"
project = client.create_project("WC10", slug="wc10", idempotency_key="wc10-project")["project_id"]
timeline = client.create_timeline(project, "empty", idempotency_key="wc10-empty")
assert timeline["head_revision_id"] and timeline["head_publication_id"]
history = client.list_timeline_commits(project, "empty", limit=10)
assert history["head"] == {
    "revision_id": timeline["head_revision_id"],
    "publication_id": timeline["head_publication_id"],
}
assert len(history["items"]) == 1
assert history["items"][0]["intent"] == "bootstrap"
assert history["items"][0]["records"] is None
assert "publish_parent_composition" not in json.dumps(history, sort_keys=True)
inspection = client.inspect_timeline(project, "empty")
assert inspection["project_id"] == project
assert inspection["timeline_id"] == "empty"
print(json.dumps({"project": project, "timeline": timeline, "inspection": inspection}, sort_keys=True))
"""
        credential = json.loads((support / "runtime" / "discovery.json").read_text(encoding="utf-8"))["credential_file"]
        measured = _run(
            [_python(environment), "-B", "-c", operation, ready["endpoint"], credential],
            env=child_env,
            capture_output=True,
            cwd=tmp_path,
            timeout=60,
        )
        assert measured.returncode == 0, measured.stderr + measured.stdout
        assert json.loads(measured.stdout)["timeline"]["timeline_id"] == "empty"
    finally:
        if started is not None and (support / "runtime" / "discovery.json").is_file():
            stopped = _run(
                [*command[:1], "down", *command[1:]],
                env=child_env,
                capture_output=True,
                cwd=tmp_path,
                timeout=60,
            )
            assert stopped.returncode == 0, stopped.stderr + stopped.stdout
