"""Prepare Runtime-owned source custody for an external orchestrator test."""

from __future__ import annotations

import hashlib
import json
import pickle
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any

RUNTIME_F320 = "f3208b26b53c4d7053e5464eaa7c5e15b1505812"


def _runtime_fixture(name: str) -> Any:
    from tests.core.execution.test_runtime_source_custody_d40 import (
        _runtime_fixture as load_fixture,
    )

    return load_fixture(name)


def _orchestrator_digest(pack_root: Path) -> str:
    """Project the same captured manifest metadata used by Runtime admission."""
    import yaml

    from astrid.core.execution import generic_host as host_module
    from astrid.core.execution.orchestrator.schema import load_orchestrator_manifest

    manifest = pack_root / "orchestrators" / "demo" / "orchestrator.yaml"
    definition = load_orchestrator_manifest(manifest)
    metadata = dict(definition.metadata)
    metadata.update(
        source="folder",
        orchestrator_root=str(manifest.parent),
        folder_id=manifest.parent.name,
        manifest_file=str(manifest),
    )
    pack = yaml.safe_load((pack_root / "pack.yaml").read_text(encoding="utf-8"))
    metadata.setdefault("source_pack", str(pack.get("id") or pack_root.name))
    metadata.setdefault("pack_root", str(pack_root))
    return host_module._capability_digest(replace(definition, metadata=metadata).to_dict())


def admit_external_orchestrator_source(
    *, tmp_path: Path, monkeypatch: Any, pack_root: Path
) -> SimpleNamespace:
    """Install one genuine owner-captured source handle before host discovery."""
    from tests.helpers.runtime import use_runtime

    use_runtime(RUNTIME_F320)
    from runtime_protocol import external_pack_sources as producer
    from runtime_protocol import verified_host_launch as gate
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    from astrid.core.execution import generic_host as host_module

    owner_fixture = _runtime_fixture("test_external_pack_sources")
    authority_fixture = _runtime_fixture("test_verified_host_launch")
    from tests.core.execution.test_runtime_source_custody_d40 import _repository

    monkeypatch.setattr(host_module, "_runtime_external_sources", None)
    revision, tree = _repository(pack_root)
    definition_digest = _orchestrator_digest(pack_root)
    files = {
        path.relative_to(pack_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in pack_root.rglob("*")
        if path.is_file()
    }
    grant = {
        "repository": "https://example.test/owner/tool.git",
        "checkout": str(pack_root.parent),
        "revision": revision,
        "subpath": pack_root.name,
        "tree": tree,
        "root": str(pack_root),
        "files": files,
        "definitions": [{
            "path": "orchestrators/demo/orchestrator.yaml",
            "capability_kind": "orchestrator",
            "capability_id": "external_pack.demo",
            "definition_digest": definition_digest,
        }],
    }

    authority = authority_fixture.fixture_authority(tmp_path / "authority")
    realm = tmp_path / "realm"
    RealmStore.initialize(realm).close()
    service = RuntimeService(realm, support_root=tmp_path / "support")
    try:
        preparation = authority.args["preparation"]
        authority.args["config"]["support_root"] = str(service.support_root)
        preparation["profile"].update(
            workspace_uuid=service.realm["id"],
            support_root=str(service.support_root),
            host_launch={"additional_pack_roots": [{"path": str(pack_root), "files": files}]},
        )
        authority.record["selected_profile_digest"] = gate.raw_digest(preparation["profile"])
        authority.record["import_binding"]["mode"] = gate.TRUSTED_LOCAL_MODE
        producer._write_owner_grants(service, [grant], identity=owner_fixture.OWNER)

        capture = producer.OwnerSourceCapture(
            preparation=preparation,
            config=authority.args["config"],
        )
        verifier = gate.TrustedLocalHostLaunchVerifier(
            installed_release=authority.record,
            external_sources=capture,
        )
        proof = verifier.verify(**authority.args)
        _argv, payload = verifier.claim(proof, **authority.args, binding_fd=31)
        selected = gate._RuntimeExternalSources(
            gate.canonical(json.loads(payload)["external_pack_sources"])
        )
        try:
            pickle.dumps(selected)
        except TypeError:
            pass
        else:
            raise AssertionError("Runtime source handle unexpectedly became serializable")
        host_module._consume_runtime_external_sources(sources=selected)
        custody = host_module._runtime_external_sources
        custody.bind(preparation)
    finally:
        service.close()
    return SimpleNamespace(
        capture=capture,
        custody=custody,
        grant=grant,
        preparation=preparation,
        selected=selected,
    )
