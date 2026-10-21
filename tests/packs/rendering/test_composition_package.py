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
SHA256 = "21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e"
INTEGRITY = "sha512-Bgf9lHdk3CJCTsA3Jbd5WW9UYCHEZQTF3VFM1YO6dimZ+q8bQ8cX6CZ4FCfClBNgg10DQ1bozGMqFCpkGNXvvw=="
REQUIRED_EXPORTS = (".", "./evaluation", "./theme-api", "./registries", "./effects.generated",
                    "./animations.generated", "./transitions.generated", "./registry.generated")


def _stage_locked_package(project: Path) -> tuple[Path, dict]:
    cli = project / remotion_runtime.REMOTION_CLI_RELATIVE_PATH
    cli.parent.mkdir(parents=True)
    cli.write_text("// CLI")
    package = project / "node_modules/@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(REMOTION / "artifacts/banodoco-timeline-composition-0.0.14.tgz") as archive:
        archive.extractall(project)
    (project / "package").rename(package)
    return package, json.loads((package / "package.json").read_text())


def test_locked_release_is_built_and_requires_no_separate_schema_or_theme(tmp_path):
    artifact = REMOTION / "artifacts/banodoco-timeline-composition-0.0.14.tgz"
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == SHA256
    lock = json.loads((REMOTION / "package-lock.json").read_text())
    package = lock["packages"]["node_modules/@banodoco/timeline-composition"]
    assert package["version"] == "0.0.14"
    assert package["resolved"] == "file:artifacts/banodoco-timeline-composition-0.0.14.tgz"
    assert package["integrity"] == INTEGRITY
    with tarfile.open(artifact) as archive:
        manifest_file = archive.extractfile("package/package.json")
        assert manifest_file is not None
        manifest = json.load(manifest_file)
        members = archive.getmembers()
        files = {member.name for member in members}
    assert len(members) == 80
    assert all(member.isfile() for member in members)
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


def test_public13_evaluation_admits_valid_source_and_rejects_four_forged_sources(tmp_path):
    project = tmp_path / "api"
    _stage_locked_package(project)
    script = r'''
import assert from 'node:assert/strict';
import {AudioEnvelopeError, encodedEnvelopeSource} from '@banodoco/timeline-composition/evaluation';

const envelope = {keyframes: [{at: 0, value: 1}, {at: 1, value: 1}]};
const prepared = {
  file: 'https://example.test/prepared.wav',
  envelope_key: '{"keyframes":[{"at":0,"value":1},{"at":1,"value":1}]}',
  source_from: 2 / 30,
  playback_rate: 1.5,
};
assert.equal(encodedEnvelopeSource(prepared, envelope, 2 / 30, 1.5), prepared.file);
assert.equal('useAudioEnvelopeSource' in await import('@banodoco/timeline-composition/evaluation'), false);

for (const [name, change] of Object.entries({
  envelope: {envelope_key: '{}'},
  sourceFrom: {source_from: 0.05},
  playbackRate: {playback_rate: 1},
  url: {file: 'blob:prepared'},
})) {
  const forged = {...prepared, ...change};
  const before = JSON.stringify(forged);
  assert.throws(() => encodedEnvelopeSource(forged, envelope, 2 / 30, 1.5),
    (error) => error instanceof AudioEnvelopeError && error.code === 'ENVELOPE_UNRENDERED', name);
  assert.equal(JSON.stringify(forged), before, name);
}
''';
    subprocess.run([os.environ.get("ASTRID_NODE_EXECUTABLE", "node"), "--input-type=module", "-e", script],
                   cwd=project, check=True, capture_output=True, text=True, timeout=30)


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
