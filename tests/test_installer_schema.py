"""Installer staging must consume the schema artifact pinned by Remotion."""

import json
import tarfile
from pathlib import Path

from astrid.installer.backend import Backend

ROOT = Path(__file__).parents[1]


def test_staging_installs_the_npm_locked_schema_before_declaring_services(tmp_path, monkeypatch):
    import astrid.installer.backend as backend_module

    calls = []
    backend = Backend(tmp_path / "program", tmp_path / "install.log", tmp_path / "uv")
    monkeypatch.setattr(backend, "existing", lambda _data: None)

    def source(_name, _sha, destination, **_kwargs):
        destination.mkdir(parents=True)
        if destination.name == "a":
            (destination / "remotion").mkdir()
            (destination / "remotion/package-lock.json").write_text("{}\n")
        else:
            (destination / "packages" / "python").mkdir(parents=True)
        return destination

    monkeypatch.setattr(backend_module, "source", source)
    monkeypatch.setattr(backend_module, "install_tools", lambda *_args: {
        "PATH": "/tools",
        "ASTRID_NODE_EXECUTABLE": "/tools/node",
        "ASTRID_BUN_EXECUTABLE": "/tools/bun",
    })
    monkeypatch.setattr(backend_module, "binary", lambda *_args: Path("/tools/npm-cli.js"))

    def run(argv, **_kwargs):
        call = [str(value) for value in argv]
        calls.append(call)
        if call[0].endswith("uv") and call[1:] == ["--version"]:
            return "uv 1.0.0"
        if call[1:3] == ["/tools/npm-cli.js", "ci"]:
            package = tmp_path / "program" / "versions"
            agent_root = next(package.iterdir()) / "a"
            schema = agent_root / "remotion" / "node_modules" / "@banodoco" / "timeline-schema" / "python"
            (schema / "banodoco_timeline_schema").mkdir(parents=True)
            (schema / "pyproject.toml").write_text("[project]\nname='banodoco-timeline-schema'\n", encoding="utf-8")
        if "source_checkout_digest" in " ".join(call):
            return "digest"
        return ""

    monkeypatch.setattr(backend, "run", run)

    declarations = []

    def declare(*, folder, agent, **_kwargs):
        schema = agent / "remotion" / "node_modules" / "@banodoco" / "timeline-schema" / "python"
        assert (schema / "pyproject.toml").is_file()
        calls.append(["declare-services"])
        declarations.append(schema)
        destination = folder / "services.json"
        destination.write_text('{"version":1,"services":[]}', encoding="utf-8")
        return destination

    monkeypatch.setattr(backend, "_declare_services", declare)
    manifest = {
        "agent": {"sha": "a" * 40},
        "runtime": {"sha": "b" * 40},
        "tools": {"uv": {"version": "1.0.0"}, "python": {"version": "3.11.9"}},
    }

    version = backend.stage(manifest, tmp_path / "program", tmp_path / "workspace")

    npm_index = next(i for i, call in enumerate(calls) if call[1:3] == ["/tools/npm-cli.js", "ci"])
    schema_path = str(declarations[0])
    schema_install_index = next(
        i for i, call in enumerate(calls)
        if call[1:3] == ["pip", "install"] and schema_path in call
    )
    assert npm_index < schema_install_index < calls.index(["declare-services"])
    assert schema_path.endswith("/a/remotion/node_modules/@banodoco/timeline-schema/python")
    initial_install = next(call for call in calls if any(value.endswith("packages/python") for value in call))
    assert not any("timeline-schema" in value for value in initial_install)
    python_installs = [call for call in calls if call[1:3] == ["pip", "install"]]
    assert python_installs[0] == [
        str(backend.uv), "pip", "install", "--python", str(version.python),
        "--require-hashes", "-r", str(version.root / "a/requirements/runtime.lock"),
    ]
    assert python_installs[1] == [
        str(backend.uv), "pip", "install", "--python", str(version.python), "--no-deps",
        str(version.root / "r"), str(version.root / "r/packages/python"), str(version.root / "a"),
        str(version.root / "v"),
    ]
    assert python_installs[2] == [
        str(backend.uv), "pip", "install", "--python", str(version.python), "--no-deps", schema_path,
    ]
    assert version.profile.is_file()


def test_remotion_lock_pins_the_immutable_composition_public_entry():
    package = json.loads((ROOT / "remotion/package.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "remotion/package-lock.json").read_text(encoding="utf-8"))
    composition = lock["packages"]["node_modules/@banodoco/timeline-composition"]
    artifact = ROOT / "remotion/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
    public_exports = (".", "./evaluation", "./theme-api", "./registries",
                      "./effects.generated", "./animations.generated",
                      "./transitions.generated", "./registry.generated")

    assert package["dependencies"]["@banodoco/timeline-composition"] == (
        "file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
    )
    assert composition["version"] == "0.0.14"
    assert composition["resolved"] == (
        "file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
    )
    assert composition["integrity"] == (
        "sha512-Ajl7lyCbJqbbOpHKEr2xlhFw85hWyirlTU1Dq63BNNUdHYfqgzLXljmudP359uKH6yBxSBMPTDoHLxgiDt65oQ=="
    )
    assert "node_modules/@banodoco/timeline-schema" not in lock["packages"]
    assert "node_modules/@banodoco/timeline-theme-2rp" not in lock["packages"]

    with tarfile.open(artifact) as archive:
        manifest = json.load(archive.extractfile("package/package.json"))
        files = {member.name for member in archive.getmembers()}
    assert manifest["name"] == "@banodoco/timeline-composition"
    assert manifest["version"] == "0.0.14"
    for export in public_exports:
        for target in manifest["exports"][export].values():
            assert target.startswith("./dist/")
            assert "package/" + target.removeprefix("./") in files

