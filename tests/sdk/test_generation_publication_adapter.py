from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest

from astrid.core.execution.generic_host import GenericPackHost
from astrid.sdk.exceptions import CapabilityValidationError
from astrid.sdk.generation_publication import (
    CAPABILITY_ID,
    compose_image_publication_request,
)
from astrid.sdk.invocation import get_capability


def _actual_capability():
    capability = get_capability(CAPABILITY_ID, kind="executor", include_elements=False)
    assert isinstance(capability.definition, Mapping)
    assert any(output.name == "generated_images" for output in capability.outputs)
    return capability


def _actual_host_record():
    host = GenericPackHost(
        pack_roots=[Path(__file__).resolve().parents[2] / "astrid/packs/generation"]
    )
    host.discover()
    return host.capabilities[CAPABILITY_ID]


def _request(capability, *, count: int = 3) -> dict[str, object]:
    return {
        "project": "project-ordinary-image",
        "capability_digest": _actual_host_record().capability_digest,
        "params": {
            "model": "z-image",
            "mode": "t2i",
            "execution": "cloud",
            "prompt": "a blue ceramic vase on a wooden table",
            "count": count,
            "size": "1024x1024",
            "seed": 42,
            "negative_prompt": "blurry",
            "guidance_scale": 7.5,
            "steps": 28,
        },
    }


def test_compose_is_deterministic_and_uses_real_capability_outputs() -> None:
    capability = _actual_capability()
    host_record = _actual_host_record()
    request = _request(capability)

    first = compose_image_publication_request(request)
    second = compose_image_publication_request(request)

    assert first == second
    assert first["project"] == request["project"]
    assert first["capability_id"] == CAPABILITY_ID
    assert first["capability_digest"] == request["capability_digest"]
    assert first["capability_digest"] == host_record.capability_digest
    assert first["input_object_ids"] == []
    assert first["storage_estimate"] == {
        "scratch_bytes": 69_206_016,
        "output_bytes": 269_484_032,
    }
    intent = first["generation_intent"]
    assert intent == {
        "version": 1,
        "modality": "image",
        "partial_success_policy": "reject",
        "groups": [
            {
                "group_key": "main",
                "selectors": [
                    {"selector": "main-0", "ordinal": 0, "variant_key": "original"},
                    {"selector": "main-1", "ordinal": 1, "variant_key": "variant-1"},
                    {"selector": "main-2", "ordinal": 2, "variant_key": "variant-2"},
                ],
            }
        ],
    }
    effect = first["settlement_effect"]
    assert effect["effect_type"] == "generation.publish_v1"
    assert effect["target_id"] == request["project"]
    assert effect["payload"]["groups"][0]["selectors"] == [
        {
            "selector": "main-0",
            "ordinal": 0,
            "variant_key": "original",
            "output_port": "generated_images",
        },
        {
            "selector": "main-1",
            "ordinal": 1,
            "variant_key": "variant-1",
            "output_port": "generated_images",
        },
        {
            "selector": "main-2",
            "ordinal": 2,
            "variant_key": "variant-2",
            "output_port": "generated_images",
        },
    ]
    assert "image_manifest" not in json.dumps(effect)


def test_compose_digest_matches_generic_pack_host_registration() -> None:
    capability = _actual_capability()
    host_record = _actual_host_record()
    composed = compose_image_publication_request(_request(capability, count=1))

    assert composed["capability_digest"] == host_record.capability_digest


@pytest.mark.parametrize(
    "mutator, match",
    [
        (lambda request: request.update({"settlement_effect": {}}), "unsupported field"),
        (
            lambda request: request["params"].update({"generation_intent": {}}),
            "unsupported parameter",
        ),
        (
            lambda request: request["params"].update({"output_selector": "main-0"}),
            "unsupported parameter",
        ),
        (
            lambda request: request["params"].update({"count": 5}),
            "count must be between",
        ),
        (
            lambda request: request["params"].update({"size": "4096x4096"}),
            "dimensions must be at most",
        ),
    ],
)
def test_compose_rejects_effect_or_unbounded_route_fields(mutator, match) -> None:
    capability = _actual_capability()
    request = _request(capability, count=1)
    mutator(request)
    with pytest.raises(CapabilityValidationError, match=match):
        compose_image_publication_request(request)


def test_compose_rejects_digest_mismatch_before_building_admission_document() -> None:
    capability = _actual_capability()
    request = _request(capability, count=1)
    request["capability_digest"] = "sha256:" + "0" * 64
    with pytest.raises(CapabilityValidationError, match="capability_digest"):
        compose_image_publication_request(request)


def test_fixed_host_adapter_serializes_one_complete_request() -> None:
    capability = _actual_capability()
    request = _request(capability, count=2)
    result = subprocess.run(
        [sys.executable, "-m", "astrid.sdk.generation_publication", "--json"],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    response = json.loads(result.stdout)
    assert response["ok"] is True
    serialized = response["request"]
    assert serialized["capability_id"] == CAPABILITY_ID
    assert serialized["spec"]["family"] == CAPABILITY_ID
    assert serialized["spec"]["params"]["count"] == 2
    assert serialized["settlement_effect"]["payload"]["groups"][0]["selectors"][1][
        "output_port"
    ] == "generated_images"
    assert result.stderr == ""


# These fixtures change only host-configured discovery, retaining the canonical
# loader, SDK projection, host registration, byte digest and execution fence.
@pytest.fixture
def native_source(tmp_path, monkeypatch):
    import shutil

    from astrid.core.execution.executor import registry as executor_registry
    from astrid.core.pack import discovery as pack_discovery
    from astrid.core.pack.loader import load_pack_manifest

    root = tmp_path / "generation"
    shutil.copytree(Path(__file__).resolve().parents[2] / "astrid/packs/generation", root)

    def scan(*_args, **_kwargs):
        return (load_pack_manifest(root / "pack.yaml"),)

    monkeypatch.setattr(executor_registry, "discover_packs", scan)
    monkeypatch.setattr(pack_discovery, "discover_packs", scan)
    return root


def _source_record(root):
    host = GenericPackHost(pack_roots=[root])
    host.discover()
    return host, host.capabilities[CAPABILITY_ID]


def _source_capability(record):
    from astrid.core.execution.executor.registry import ExecutorRegistry
    from astrid.sdk.discovery import _capability_from_definition

    registry = ExecutorRegistry([record.definition])
    return _capability_from_definition(
        record.definition, registry, capability_type="executor"
    )


def _source_request(record):
    return {
        "project": "project-ordinary-image",
        "capability_digest": record.capability_digest,
        "params": {
            "model": "z-image", "mode": "t2i", "execution": "cloud",
            "prompt": "a blue ceramic vase", "count": 1, "size": "1024x1024",
        },
    }


def _forbid_composition_effects(monkeypatch):
    from astrid.sdk import generation_publication as adapter

    def forbidden(*_args, **_kwargs):
        pytest.fail("identity refusal must precede registry/effect construction")

    monkeypatch.setattr(adapter, "_load_model_registry", forbidden)
    monkeypatch.setattr(adapter, "_generation_publish_effect", forbidden)


def test_native_source_matches_real_host_and_sdk_projection(native_source):
    from astrid.sdk.generation_publication import _capability_digest

    _, record = _source_record(native_source)
    capability = _source_capability(record)
    assert capability.definition == record.definition.to_dict()
    assert _capability_digest(capability) == record.capability_digest


@pytest.mark.parametrize("substitution", [
    "capability_id", "definition_id", "source_pack", "missing_markers",
    "missing_declaration", "missing_invocation", "malformed_declaration",
    "malformed_invocation", "empty_invocation", "unavailable_root",
    "unconfigured_identical_root", "escaping_runtime", "substituted_runtime",
    "substituted_invocation",
])
def test_native_identity_substitutions_refuse_before_effects(
    native_source, tmp_path, monkeypatch, substitution,
):
    import copy
    import shutil
    from dataclasses import replace

    from astrid.sdk import generation_publication as adapter

    _, record = _source_record(native_source)
    capability = _source_capability(record)
    definition = copy.deepcopy(dict(capability.definition))
    metadata = definition["metadata"]
    capability_id = CAPABILITY_ID
    if substitution == "capability_id":
        capability_id = "generation.other"
    elif substitution == "definition_id":
        definition["id"] = "generation.other"
    elif substitution == "source_pack":
        metadata["source_pack"] = "other"
    elif substitution == "missing_markers":
        metadata.pop("action_declaration")
        metadata.pop("action_invocation")
    elif substitution.startswith("missing_"):
        metadata.pop("action_" + substitution.removeprefix("missing_"))
    elif substitution.startswith("malformed_"):
        metadata["action_" + substitution.removeprefix("malformed_")] = "command"
    elif substitution == "empty_invocation":
        metadata["action_invocation"] = {}
    elif substitution == "unavailable_root":
        metadata["pack_root"] = str(tmp_path / "unavailable")
    elif substitution == "unconfigured_identical_root":
        other = tmp_path / "unconfigured" / "generation"
        shutil.copytree(native_source, other)
        metadata["pack_root"] = str(other)
    elif substitution == "escaping_runtime":
        (tmp_path / "outside.py").write_text("raise AssertionError('never run')\n")
        metadata["runtime_file"] = "../outside.py"
    elif substitution == "substituted_runtime":
        metadata["runtime_file"] = "actions/generate_audio/run.py"
    elif substitution == "substituted_invocation":
        metadata["action_invocation"]["command"]["argv"] = ["false"]
    capability = replace(capability, id=capability_id, definition=definition)
    monkeypatch.setattr(adapter, "get_capability", lambda *_args, **_kwargs: capability)
    request = _source_request(record)
    _forbid_composition_effects(monkeypatch)
    with pytest.raises(CapabilityValidationError):
        compose_image_publication_request(request)


def test_byte_identical_relocation_keeps_portable_digest_with_configured_authority(
    native_source, tmp_path, monkeypatch,
):
    import shutil

    from astrid.core.execution.executor import registry as executor_registry
    from astrid.core.pack import discovery as pack_discovery
    from astrid.core.pack.loader import load_pack_manifest
    from astrid.sdk.generation_publication import _capability_digest

    _, before = _source_record(native_source)
    moved = tmp_path / "relocated" / "generation"
    shutil.copytree(native_source, moved)

    def scan(*_args, **_kwargs):
        return (load_pack_manifest(moved / "pack.yaml"),)

    monkeypatch.setattr(executor_registry, "discover_packs", scan)
    monkeypatch.setattr(pack_discovery, "discover_packs", scan)
    _, after = _source_record(moved)
    assert after.capability_digest == before.capability_digest
    assert after.source_digest != before.source_digest
    assert _capability_digest(_source_capability(after)) == before.capability_digest
    with pytest.raises(CapabilityValidationError):
        _capability_digest(_source_capability(before))


def test_legacy_folder_executor_retains_loader_and_host_digest(tmp_path, monkeypatch):
    import copy

    from astrid.core.execution.executor import folder
    from astrid.sdk.generation_publication import _capability_digest

    definition = copy.deepcopy(dict(_actual_capability().definition))
    metadata = definition["metadata"]
    for key in ("action_declaration", "action_invocation", "source", "source_pack",
                "pack_root", "priority"):
        metadata.pop(key, None)
    metadata["runtime_file"] = "run.py"
    pack_root = tmp_path / "generation"
    root = pack_root / "executors" / "generate_image"
    root.mkdir(parents=True)
    (pack_root / "pack.yaml").write_text(json.dumps({
        "schema_version": 3, "id": "generation", "name": "Legacy fixture",
        "version": "1.0.0",
    }))
    (root / "run.py").write_text("raise AssertionError('compose only')\n")
    (root / "executor.yaml").write_text(json.dumps(definition))
    _, record = _source_record(root)
    capability = _source_capability(record)
    calls = []
    loader = folder.load_folder_executor

    def load(path):
        calls.append(path)
        return loader(path)

    monkeypatch.setattr(folder, "load_folder_executor", load)
    assert _capability_digest(capability) == record.capability_digest
    assert calls == [root.resolve()]
    assert capability.definition["metadata"]["executor_root"] == str(root.resolve())
    assert capability.definition["metadata"]["source_pack"] == "generation"
    assert capability.definition["metadata"]["pack_root"] == str(pack_root.resolve())


@pytest.mark.parametrize("malformation", [
    "missing_invocation", "unknown_invocation", "escaping_python", "missing_python",
])
def test_malformed_native_source_is_rejected_by_canonical_discovery(
    native_source, malformation,
):
    import yaml

    from astrid.core.pack import PackValidationError
    from astrid.core.pack.discovery import discover_pack_metadata
    from astrid.core.pack.loader import load_pack_manifest

    path = native_source / "pack.yaml"
    payload = yaml.safe_load(path.read_text())
    action = payload["actions"]["generate_image"]
    if malformation == "missing_invocation":
        action.pop("invocation")
    elif malformation == "unknown_invocation":
        action["invocation"]["kind"] = "unrecognized"
    else:
        action["invocation"] = {
            "kind": "python", "function": "run",
            "path": "../outside.py" if malformation == "escaping_python"
                    else "actions/does-not-exist.py",
        }
    path.write_text(yaml.safe_dump(payload))
    with pytest.raises(PackValidationError):
        load_pack_manifest(path)
    with pytest.raises(PackValidationError):
        discover_pack_metadata()


@pytest.mark.parametrize("escape_kind", ["relative", "absolute"])
def test_configured_native_runtime_must_stay_in_admitted_pack(
    native_source, escape_kind,
):
    import yaml

    from astrid.sdk.generation_publication import _capability_digest

    path = native_source / "pack.yaml"
    payload = yaml.safe_load(path.read_text())
    outside = native_source.parent / "outside.py"
    outside.write_text("raise AssertionError('never run')\n")
    runtime_file = "../outside.py" if escape_kind == "relative" else str(outside)
    payload["actions"]["generate_image"]["metadata"]["runtime_file"] = runtime_file
    path.write_text(yaml.safe_dump(payload))
    _, record = _source_record(native_source)
    with pytest.raises(CapabilityValidationError):
        _capability_digest(_source_capability(record))


def _mutate_bytes_preserving_stat(path):
    import os

    before = path.stat()
    data = path.read_bytes()
    assert b"from" in data
    changed = data.replace(b"from", b"frOm", 1)
    assert len(changed) == len(data) and changed != data
    path.write_bytes(changed)
    os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert path.stat().st_size == before.st_size
    assert path.stat().st_mtime_ns == before.st_mtime_ns


def test_native_command_byte_mutation_refuses_old_digest_before_effects(
    native_source, monkeypatch,
):
    from astrid.sdk import generation_publication as adapter

    _, old = _source_record(native_source)
    capability = _source_capability(old)
    request = _source_request(old)
    monkeypatch.setattr(adapter, "get_capability", lambda *_args, **_kwargs: capability)
    _mutate_bytes_preserving_stat(native_source / "actions/generate_image/run.py")
    _, fresh = _source_record(native_source)
    assert fresh.definition.to_dict() == old.definition.to_dict()
    assert fresh.capability_digest != old.capability_digest
    assert fresh.source_digest != old.source_digest
    _forbid_composition_effects(monkeypatch)
    with pytest.raises(CapabilityValidationError, match="capability_digest"):
        compose_image_publication_request(request)


def test_native_command_source_fence_refuses_before_child_or_provider(
    native_source, tmp_path, monkeypatch,
):
    from astrid.core.execution import generic_host
    from astrid.core.execution.generic_host import HostError

    host, record = _source_record(native_source)
    definition, admission = host.admit("executor", CAPABILITY_ID)
    assert definition == record.definition.to_dict()
    assert admission["capability_digest"] == record.capability_digest
    _mutate_bytes_preserving_stat(native_source / "actions/generate_image/run.py")
    launched = []

    def forbidden(*args, **kwargs):
        launched.append((args, kwargs))
        pytest.fail("source mutation reached child/provider boundary")

    monkeypatch.setattr(generic_host, "popen_owned_group", forbidden)
    monkeypatch.setattr(host, "_child_environment", forbidden)
    attempt = tmp_path / "attempt"
    with pytest.raises(HostError, match="source digest changed"):
        host._run_command_definition(
            record, {}, attempt / "outputs", attempt, admission=admission,
        )
    assert not launched
    assert not attempt.exists()
