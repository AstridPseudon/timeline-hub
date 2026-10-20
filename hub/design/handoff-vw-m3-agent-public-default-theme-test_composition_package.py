"""Exercise the built release through the host's ordinary generated element maps."""
import hashlib
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from astrid.core.element.registry import ElementRegistry
from astrid.core.element.schema import ElementDefinition
from astrid.core.rendering import remotion_runtime
from scripts import gen_effect_registry

ROOT = Path(__file__).resolve().parents[3]
REMOTION = ROOT / "remotion"
SHA256 = "cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7"
INTEGRITY = "sha512-SmJAoem9f+86D+eO+PvBAz3JydlefpUUwcOOkG7SU9k2ZPKpjXLWKHm/N4424TO5HNQtCHMt5T6Jy2Y5zA6Ycg=="
REQUIRED_EXPORTS = (".", "./evaluation", "./theme-api", "./registries", "./effects.generated",
                    "./animations.generated", "./transitions.generated", "./registry.generated")


def _stage_locked_package(project: Path) -> tuple[Path, dict]:
    cli = project / remotion_runtime.REMOTION_CLI_RELATIVE_PATH
    cli.parent.mkdir(parents=True)
    cli.write_text("// CLI")
    package = project / "node_modules/@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(REMOTION / "artifacts/banodoco-timeline-composition-0.0.10.tgz") as archive:
        archive.extractall(project)
    (project / "package").rename(package)
    return package, json.loads((package / "package.json").read_text())


def test_locked_release_is_built_and_requires_no_separate_schema_or_theme(tmp_path):
    artifact = REMOTION / "artifacts/banodoco-timeline-composition-0.0.10.tgz"
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == SHA256
    lock = json.loads((REMOTION / "package-lock.json").read_text())
    package = lock["packages"]["node_modules/@banodoco/timeline-composition"]
    assert package["version"] == "0.0.10"
    assert package["resolved"] == "file:artifacts/banodoco-timeline-composition-0.0.10.tgz"
    assert package["integrity"] == INTEGRITY
    with tarfile.open(artifact) as archive:
        manifest_file = archive.extractfile("package/package.json")
        assert manifest_file is not None
        manifest = json.load(manifest_file)
        files = set(archive.getnames())
    assert not any(name.startswith("package/typescript/") for name in files)
    for export in REQUIRED_EXPORTS:
        for target in manifest["exports"][export].values():
            assert target.startswith("./dist/")
            assert "package/" + target.removeprefix("./") in files
    assert not any(name in lock["packages"] for name in (
        "node_modules/@banodoco/timeline-schema", "node_modules/@banodoco/timeline-theme-2rp"))
    cli = tmp_path / remotion_runtime.REMOTION_CLI_RELATIVE_PATH
    cli.parent.mkdir(parents=True)
    cli.write_text("// CLI")
    package_json = tmp_path / "node_modules/@banodoco/timeline-composition/package.json"
    package_json.parent.mkdir(parents=True)
    package_json.write_text(json.dumps(manifest))
    problem = remotion_runtime.remotion_install_problem(tmp_path)
    assert problem is not None
    assert "dist directory is missing" in problem

    package, staged_manifest = _stage_locked_package(tmp_path / "valid")
    assert staged_manifest == manifest
    assert remotion_runtime.remotion_install_problem(package.parents[2]) is None


@pytest.mark.parametrize("mutation, expected", [
    ("delete", "evaluation"),
    ("missing", "missing"),
    ("outside", "escapes the package"),
])
def test_installed_package_refuses_incomplete_or_unsafe_built_exports(tmp_path, mutation, expected):
    project = tmp_path / mutation
    package, manifest = _stage_locked_package(project)
    if mutation == "delete":
        (package / "dist/evaluation.js").unlink()
    else:
        target = manifest["exports"]["./evaluation"]
        if mutation == "missing":
            target["import"] = "./dist/missing-evaluation.js"
        else:
            target["import"] = "../evaluation.js"
        (package / "package.json").write_text(json.dumps(manifest))
    problem = remotion_runtime.remotion_install_problem(project)
    assert problem is not None
    assert expected in problem


def test_launch_input_binding_reuses_built_package_readiness(tmp_path):
    project = tmp_path / "runtime"
    _stage_locked_package(project)
    (project / "package.json").write_text("{}")
    (project / "package-lock.json").write_text("{}")
    schema = tmp_path / "schema" / "banodoco_timeline_schema"
    schema.mkdir(parents=True)
    for name in remotion_runtime._REQUIRED_SCHEMA_FILES:
        (schema / name).write_text("{}")
    node = tmp_path / "node"
    node.write_text("#!/bin/sh\n")
    node.chmod(0o755)
    environment = {
        remotion_runtime.NODE_EXECUTABLE_ENV: str(node),
        remotion_runtime.TIMELINE_SCHEMA_PYTHONPATH_ENV: str(schema.parent),
    }
    assert remotion_runtime._runtime_inputs(project, environment, sys.executable, {})
    (project / "node_modules/@banodoco/timeline-composition/dist/evaluation.js").unlink()
    with pytest.raises(remotion_runtime.RemotionValidationError, match="evaluation"):
        remotion_runtime._runtime_inputs(project, environment, sys.executable, {})


@pytest.mark.integration
def test_generated_custom_elements_reach_shared_render_and_scene_unchanged(tmp_path, monkeypatch):
    # This lane requires the host's locked npm install; pure artifact checks run above.
    elements = []
    for kind, element_id in (("effects", "custom"), ("animations", "fade-up"), ("transitions", "fade")):
        root = tmp_path / kind / element_id
        root.mkdir(parents=True)
        (root / "component.tsx").write_text((REMOTION / "tests" / f"custom-{kind}.tsx").read_text())
        elements.append(ElementDefinition(
            id=element_id, kind=kind, root=root, source="pack:probe", editable=True,
            priority=0, component=root / "component.tsx", schema={}, defaults={"durationFrames": 8},
            metadata={"pack_id": "probe", "kind": "wrapper", "phase": ["entrance", "exit"],
                      "clipTypeAliases": ["custom-alias"]} if kind == "effects" else
                     {"pack_id": "probe", "kind": "wrapper", "phase": ["entrance", "exit"]},
        ))
    registry = ElementRegistry(elements)
    monkeypatch.setattr(gen_effect_registry, "_element_registry", lambda: registry)
    for kind in ("effects", "animations", "transitions"):
        (tmp_path / f"{kind}.generated.ts").write_text(gen_effect_registry.generate_element_registry(kind))
    (tmp_path / "host-registries.ts").write_text((REMOTION / "src/host-registries.ts").read_text())
    package = REMOTION / "node_modules/@banodoco/timeline-composition"
    before = {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in package.rglob("*") if p.is_file()}
    subprocess.run([os.environ.get("ASTRID_NODE_EXECUTABLE", "node"),
                    str(REMOTION / "tests/composition-package.mjs"), str(tmp_path)],
                   cwd=REMOTION, check=True, capture_output=True, text=True, timeout=60)
    after = {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in package.rglob("*") if p.is_file()}
    assert before == after


@pytest.mark.integration
def test_builtin_theme_matches_locked_public_export(tmp_path):
    # Uses the provisioned host peers, never installs or loads package source.
    from astrid.core.theme import builtin_theme

    artifact = REMOTION / "artifacts/banodoco-timeline-composition-0.0.10.tgz"
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == SHA256
    with tarfile.open(artifact) as archive:
        assert len(archive.getnames()) == 77
    package, _ = _stage_locked_package(tmp_path)
    for name in ("react", "react-dom", "remotion", "@remotion/media", "@remotion/layout-utils"):
        peer = (REMOTION / "node_modules" / name).resolve(strict=True)
        link = tmp_path / "node_modules" / name
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(peer, target_is_directory=True)
    script = package / "default-theme-parity.mjs"
    script.write_text("""
import assert from 'node:assert/strict';
import {DEFAULT_THEME as rootDefault} from '@banodoco/timeline-composition';
import {DEFAULT_THEME} from '@banodoco/timeline-composition/theme-api';
assert.equal(process.version, 'v20.19.4');
assert.strictEqual(rootDefault, DEFAULT_THEME);
process.stdout.write(JSON.stringify(DEFAULT_THEME));
""")
    result = subprocess.run(
        [os.environ.get("ASTRID_NODE_EXECUTABLE", "node"), str(script)],
        check=True, capture_output=True, text=True, timeout=30,
    )
    public_default = json.loads(result.stdout)
    reference = json.loads((ROOT / "tests/fixtures/themes/public-composition-default.json").read_text())
    assert public_default == reference
    assert builtin_theme() == public_default
