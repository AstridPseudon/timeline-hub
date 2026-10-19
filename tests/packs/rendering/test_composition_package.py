"""Exercise the built release through the host's ordinary generated element maps."""
import hashlib
import json
import os
import subprocess
import tarfile
from pathlib import Path

import pytest

from astrid.core.element.registry import ElementRegistry
from astrid.core.element.schema import ElementDefinition
from astrid.core.rendering import remotion_runtime
from scripts import gen_effect_registry

ROOT = Path(__file__).resolve().parents[3]
REMOTION = ROOT / "remotion"
SHA256 = "93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa"
INTEGRITY = "sha512-dzRWuIgeSjKt6ko64AJ7F8aaiSBBxtEzwS0WBFkVi7XB+z2wHLKArlA9fWle/KlwZlXjFDzq2oBi9QJLy1HHUw=="


def test_locked_release_is_built_and_requires_no_separate_schema_or_theme(tmp_path):
    artifact = REMOTION / "artifacts/banodoco-timeline-composition-0.0.8.tgz"
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == SHA256
    lock = json.loads((REMOTION / "package-lock.json").read_text())
    package = lock["packages"]["node_modules/@banodoco/timeline-composition"]
    assert package["version"] == "0.0.8"
    assert package["resolved"] == "file:artifacts/banodoco-timeline-composition-0.0.8.tgz"
    assert package["integrity"] == INTEGRITY
    with tarfile.open(artifact) as archive:
        manifest_file = archive.extractfile("package/package.json")
        assert manifest_file is not None
        manifest = json.load(manifest_file)
        files = set(archive.getnames())
    assert not any(name.startswith("package/typescript/") for name in files)
    for export in (".", "./evaluation", "./theme-api", "./registries", "./effects.generated",
                   "./animations.generated", "./transitions.generated", "./registry.generated"):
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
    assert remotion_runtime.remotion_install_problem(tmp_path) is None


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
