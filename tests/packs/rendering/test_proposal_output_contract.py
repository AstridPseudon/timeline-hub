"""Declared-file serialization only; no Runtime custody or acceptance claim."""
from __future__ import annotations

import hashlib
import json
from types import SimpleNamespace

import pytest

from astrid.core._shared.result_manifest import harvest_staged_outputs, write_manifest
from astrid.core.execution.executor.registry import load_default_registry
from astrid.core.execution.generic_host import GenericPackHost
from tests.editing_conformance.test_settled_proposal_contract import FIXTURES, golden
from tests.packs.rendering.test_assemble_timeline import _payload, main


@pytest.mark.parametrize("settled_fixture", [False, True])
def test_registered_authoring_file_preserves_bytes_and_attempt_upload_binding(tmp_path, settled_fixture):
    definition = load_default_registry().get("rendering.assemble_timeline")
    port = next(output for output in definition.outputs if output.name == "authoring_proposal")
    assert (port.type, port.artifact_type, port.path_template) == (
        "file", "timeline/authoring-proposal", "{out}/authoring-proposal.json")
    output_root = tmp_path / "outputs"
    source = tmp_path / "children.json"
    source.write_text(json.dumps(_payload()), encoding="utf-8")
    assert main(["--resolved-children", str(source), "--out", str(output_root)]) == 0
    path = output_root / "authoring-proposal.json"
    if settled_fixture:
        # Exercise the existing file port with frozen canonical JSON bytes.
        # The actual assembler still emits the legacy whole-timeline proposal.
        path.write_bytes((FIXTURES / golden()["artifact"]["fixture"]).read_bytes())
        manifest_path = output_root / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        for output in manifest["outputs"]:
            output.pop("content_hash", None)
            output.pop("bytes", None)
        write_manifest(manifest_path, manifest)
    raw = path.read_bytes()
    harvested = harvest_staged_outputs(
        output_root, definition=definition, declared_outputs=definition.outputs,
        values={"out": str(output_root)}, require=True)
    host = GenericPackHost.__new__(GenericPackHost)
    typed = host._typed_outputs(SimpleNamespace(definition=definition), harvested, tmp_path)
    descriptor = next(item for item in typed if item["name"] == port.name)
    digest = "sha256:" + hashlib.sha256(raw).hexdigest()
    assert descriptor["digest"] == digest and descriptor["size"] == len(raw)
    calls = []

    def upload_object(upload_path, **binding):
        calls.append((upload_path.read_bytes(), binding))
        return SimpleNamespace(digest=digest, size=len(raw))

    host.client = SimpleNamespace(upload_object=upload_object)
    rows = host._upload_outputs(
        [descriptor], project_id="project", run_id="run", task_id="task",
        attempt_id="attempt", lease_id="lease", fence=2, runtime_epoch=3)
    assert calls == [(raw, {
        "project_id": "project", "run_id": "run", "task_id": "task",
        "attempt_id": "attempt", "lease_id": "lease", "fence": 2, "runtime_epoch": 3,
        "media_type": "application/json", "filename": "authoring-proposal.json",
        "output_key": "authoring_proposal", "output_port": "authoring_proposal"})]
    assert {key: rows[0][key] for key in ("name", "kind", "digest", "size", "media_type")} == {
        "name": "authoring_proposal", "kind": "object", "digest": digest,
        "size": len(raw), "media_type": "application/json"}
    assert "path" not in rows[0] and "data_base64" not in rows[0]
