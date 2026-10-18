from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution.capability_ledger import capability_execution_admission
from astrid.core.execution.executor.actions import (
    action_executor_definition,
    action_is_local_orchestrator,
    action_orchestrator_definition,
)
from astrid.core.execution.executor.schema import ExecutorValidationError
from astrid.core.execution.generic_host import GenericPackHost, HostError, _preflight_unavailable_reason
from astrid.core.pack.canonical import validate_canonical_pack


def test_beta_matrix_covers_every_discovered_capability_and_declaration():
    host = GenericPackHost(pack_roots=[Path("astrid/packs")])
    records = host.discover()
    discovered = {record.id: record for record in records}
    assert len(discovered) == len(records), "discovered action identities must be unique"
    external_contracts = {
        "hivemind.contribute", "hivemind.get_item", "hivemind.ingest_article",
        "hivemind.ingest_workflow", "hivemind.ingest_youtube",
        "hivemind.refresh_media", "hivemind.search",
    }
    assert {key for key in host.matrix if key.startswith("hivemind.")} == external_contracts
    assert set(host.matrix) - set(discovered) == external_contracts | {"h3_av.transform"}
    assert host.stale_matrix_entries == ("h3_av.transform",)

    # The sole matrix-only local parent is not a Host executor. Verify its
    # owning projection and exact children before excluding it from equality.
    entry = validate_canonical_pack(Path("astrid/packs/h3_av"))
    pack = SimpleNamespace(id=entry.id, root=entry.root, version=entry.definition.version)
    action = entry.definition.actions["transform"]
    assert action_is_local_orchestrator(action) is True
    with pytest.raises(ExecutorValidationError, match="not a host executor"):
        action_executor_definition(pack, "transform", action)
    parent = action_orchestrator_definition(pack, "transform", action)
    assert parent.id == "h3_av.transform"
    assert parent.child_executors == (
        "h3_av.prepare", "h3_av.compile", "vibecomfy.validate", "vibecomfy.run",
        "h3_av.compose", "h3_av.verify", "h3_av.publication_finalizer",
    )
    with pytest.raises(HostError, match="capability not discovered: h3_av.transform"):
        host.admit("executor", parent.id)

    # Discovery keeps unapproved actions visible; it does not authorize them.
    assert set(discovered) - set(host.matrix) == {"pixel.strip"}
    approved = {key: record for key, record in discovered.items() if not record.approval_reason}
    assert set(approved) == set(host.matrix) - external_contracts - {parent.id}
    assert set(parent.child_executors) <= set(approved)
    assert {record.matrix["disposition"] for record in approved.values()} <= {
        "required", "optional", "unsupported", "retired",
    }
    for record in approved.values():
        assert record.matrix == host.matrix[record.id]
        admission = capability_execution_admission(host.ledger, record.id)
        assert admission["executable"] is True
        assert admission["requires_runtime_readiness"] is True
        assert record.matrix["evidence_reason"]
        assert record.matrix["adapter_family"] == record.adapter.family
        assert isinstance(record.resource_keys, tuple) and record.resource_keys
        assert record.capability_digest and record.source_digest
        assert isinstance(record.manifest()["inputs"], list)
        assert isinstance(record.manifest()["outputs"], list)

    publication = approved["media.transcript_publish"]
    assert publication.definition.metadata["requires_caller_document_adapter"] is True
    assert publication.ready is False  # declaration/discovery is not readiness

    pixel = discovered["pixel.strip"]
    assert pixel.matrix == {}
    assert "no approved capability-matrix row" in pixel.approval_reason
    denied = capability_execution_admission(host.ledger, pixel.id)
    assert denied["executable"] is False
    assert denied["reason"] == "capability is not declared in the canonical matrix"
    [pixel] = host.preflight(pixel.id)
    assert pixel.ready is False
    assert pixel.preflight["approval"] == {"ok": False, "reason": pixel.approval_reason}
    assert "no approved capability-matrix row" in _preflight_unavailable_reason(pixel)
    manifest = pixel.manifest()  # the owning registration metadata projection
    assert manifest["disposition"] == "unclassified"
    assert manifest["ready"] is False
    assert manifest["preflight"]["approval"]["ok"] is False
    with pytest.raises(HostError, match="no approved capability-matrix row"):
        host.admit("executor", pixel.id)


def test_beta_reference_family_preflight_is_truthful_on_this_machine():
    host = GenericPackHost(pack_roots=[Path("astrid/packs")])
    host.discover()
    host.preflight()

    cpu = host.capabilities["editorial.arrange"]
    assert cpu.adapter.family == "cpu"
    assert cpu.ready

    provider = host.capabilities["generation.generate_image_openai"]
    assert provider.adapter.family == "provider"
    if not provider.ready:
        assert provider.preflight["credentials"]["missing"]

    render = host.capabilities["rendering.render"]
    assert render.adapter.family == "render"
    assert render.adapter.requires_remotion is True
    assert "remotion" in render.preflight
    if not render.ready:
        assert not render.preflight["remotion"]["ok"] or render.preflight["binaries"]["missing"]

    # These helpers are offline pack executors.  They share the rendering
    # namespace but do not inherit the final compositor's Remotion dependency.
    for capability_id in (
        "rendering.html_canvas_effect",
        "rendering.sprite_sheet",
        "rendering.timeline_storyboard",
        "rendering.timeline_visualize",
    ):
        helper = host.capabilities[capability_id]
        assert helper.adapter.family == "render"
        assert helper.adapter.requires_remotion is False
        assert "remotion" not in helper.preflight
        if capability_id == "rendering.sprite_sheet" and not helper.ready:
            assert helper.preflight["binaries"]["missing"] == ["ffmpeg"]
            pytest.skip(
                "OPTIONAL_FFMPEG: rendering.sprite_sheet requires ffmpeg "
                "on this host"
            )
        assert helper.ready

    local = host.capabilities["vibecomfy.run"]
    assert local.adapter.family == "local_generation"
    if not local.ready:
        assert local.preflight["packages"]["missing"]


def test_bounded_typed_media_is_optional_until_gpu_output_proof():
    host = GenericPackHost(pack_roots=[Path("astrid/packs")])
    host.discover()
    host.preflight()

    for capability_id in ("vibecomfy.video_enhance", "vibecomfy.character_animation"):
        record = host.capabilities[capability_id]
        assert record.matrix["disposition"] == "optional"
        assert "GPU" in record.matrix["evidence_reason"]
        assert record.adapter.family == "local_generation"


def test_provider_ledger_rows_are_networked_and_credential_dispositions_match():
    """B9.4: provider declarations cannot silently become offline executors."""
    host = GenericPackHost(pack_roots=[Path("astrid/packs")])
    records = host.discover()
    provider_rows = [record for record in records if record.adapter.family == "provider"]
    assert provider_rows

    by_credential = {
        str(row["credential"]): set(row["capabilities"])
        for row in host.ledger["sources"]["providers"]
    }
    for record in provider_rows:
        assert record.definition.isolation.network is True
        required_env = record.matrix.get("required_env") or ()
        for credential in required_env:
            assert record.id in by_credential[str(credential)]
        # A source manifest's provider metadata and the frozen matrix must
        # agree on the family; this catches a provider accidentally advertised
        # as a CPU/local capability after a manifest edit.
        assert record.matrix["adapter_family"] == "provider"


def test_manifest_secrets_reconcile_to_provider_readiness(monkeypatch):
    for key in ("GIPHY_API_KEY", "FAL_KEY"):
        monkeypatch.delenv(key, raising=False)
    host = GenericPackHost(pack_roots=[Path("astrid/packs")])
    host.discover()
    host.preflight()
    assert host.capabilities["media.gif_search"].preflight["credentials"]["missing"] == ["GIPHY_API_KEY"]
    assert host.capabilities["media.gif_search"].ready is False
    for capability_id in ("media.speech_repair_lavasr", "fal.h3_video"):
        record = host.capabilities[capability_id]
        assert record.preflight["credentials"]["missing"] == ["FAL_KEY"]
        assert record.ready is False
