"""D72's local JSON contract does not supply D67's installed Python models."""

import hashlib
import json
from pathlib import Path

import jsonschema
import pytest

from astrid.core.rendering import node_pin, remotion_runtime
from astrid.core.timeline import banodoco_schema
from astrid.installer.backend import Backend
from astrid.sdk import host_bootstrap

ROOT = Path(__file__).parents[1]
SCHEMA = Path("astrid/core/timeline/schema/timeline-config.schema.json")


def test_staged_canonical_schema_is_not_an_installed_model_package(tmp_path, monkeypatch):
    # Acquisition, installation and native tools are outside this finite test.
    # Keep stage, source-host provisioning and the schema readers real.
    backend = Backend(tmp_path / "program", tmp_path / "log", tmp_path / "uv")

    def source(name, _sha, destination, **_kwargs):
        destination.mkdir(parents=True)
        if name == "agent":
            for relative in (SCHEMA, Path("runtime.lock.json"),
                             Path("remotion/package.json"), Path("remotion/package-lock.json")):
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
        return destination

    monkeypatch.setattr("astrid.installer.backend.source", source)
    monkeypatch.setattr("astrid.installer.backend.install_tools", lambda *_args: {
        "PATH": "/tools", "ASTRID_NODE_EXECUTABLE": "/tools/node",
        "ASTRID_BUN_EXECUTABLE": "/tools/bun",
    })
    monkeypatch.setattr("astrid.installer.backend.binary", lambda *_args: Path("/tools/npm-cli.js"))
    monkeypatch.setattr(backend, "existing", lambda _data: None)
    monkeypatch.setattr(backend, "_declare_services", lambda **kw: kw["folder"] / "services.json")

    def run(argv, *, cwd=None, **_kwargs):
        if len(argv) > 2 and argv[1:3] == [Path("/tools/npm-cli.js"), "ci"]:
            (cwd / "node_modules").mkdir()
        return "uv 1.0.0"

    monkeypatch.setattr(backend, "run", run)
    version = backend.stage({
        "agent": {"sha": "a" * 40}, "runtime": {"sha": "b" * 40},
        "tools": {"uv": {"version": "1.0.0"}, "python": {"version": "3.11.9"}},
    }, backend.root, tmp_path / "data")
    agent = version.root / "a"
    assert hashlib.sha256((agent / SCHEMA).read_bytes()).hexdigest() == (
        "4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd"
    )

    # Use the existing local reader on the staged contract, including role.
    monkeypatch.setattr(banodoco_schema, "_VENDORED_SCHEMA", agent / SCHEMA)
    banodoco_schema.load_vendored_timeline_schema.cache_clear()
    try:
        contract = banodoco_schema.load_vendored_timeline_schema()
        jsonschema.validate({"tracks": [{"id": "source", "kind": "visual",
                                        "label": "Source", "role": "source"}], "clips": []}, contract)
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate({"tracks": [], "clips": "invalid"}, contract)
    finally:
        banodoco_schema.load_vendored_timeline_schema.cache_clear()

    # This source-profile caller reaches the actual provisioner. It does not
    # stand in for D67's isolated installed-origin probe or qualify a host.
    monkeypatch.setenv("ASTRID_HOST_EXECUTION_PROFILE", "source")
    for name in ("ASTRID_NODE_EXECUTABLE", "ASTRID_REMOTION_PROJECT_DIR",
                 "ASTRID_TIMELINE_SCHEMA_PYTHONPATH"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(host_bootstrap, "_dependency_pythonpath", lambda: ())
    monkeypatch.setattr(node_pin, "resolve_pinned_node", lambda *_args, **_kwargs:
                        node_pin.NodeResolution(Path("/tools/node"), "v20.19.4", "v20.19.4", "test"))
    environment = host_bootstrap._host_render_environment(agent)
    assert environment["ASTRID_REMOTION_PROJECT_DIR"] == str(agent / "remotion")
    assert "ASTRID_TIMELINE_SCHEMA_PYTHONPATH" not in environment
    assert not (agent / "remotion/node_modules/@banodoco/timeline-schema").exists()

    # Isolate the schema preflight from the separately qualified JS bundle.
    # Never manufacture Python modules or report runtime readiness here.
    monkeypatch.setattr(remotion_runtime, "remotion_install_problem", lambda _project: None)
    monkeypatch.setattr(remotion_runtime, "resolve_remotion_runtime_tools", lambda *_args:
                        pytest.fail("missing schema must refuse before native tools"))
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", environment["ASTRID_REMOTION_PROJECT_DIR"])
    status = remotion_runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available
    assert status.reason == "ASTRID_TIMELINE_SCHEMA_PYTHONPATH must point to the installed timeline schema"

    # Binding the JSON directory as a Python package cannot satisfy the reader.
    monkeypatch.setenv("ASTRID_TIMELINE_SCHEMA_PYTHONPATH", str((agent / SCHEMA).parent))
    status = remotion_runtime.remotion_runtime_status(require_explicit_project=True)
    assert not status.available
    assert status.reason.startswith("installed timeline schema is incomplete under ")

    profile = json.loads(version.profile.read_text())
    assert profile["source_checkout"] == str(agent)
    assert profile["runtime_checkout"] == str(version.root / "r")
