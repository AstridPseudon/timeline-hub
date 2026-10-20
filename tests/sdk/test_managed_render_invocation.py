from __future__ import annotations

from types import SimpleNamespace

import pytest

from astrid.sdk import invocation
from astrid.sdk import timeline_filmstrip
import astrid.core.rendering.storage as storage_module


VIDEO_DIGEST = "sha256:" + "d" * 64


def _filmstrip_invoke_fixtures(monkeypatch, authority):
    capability = SimpleNamespace(
        id="rendering.timeline_visualize",
        capability_type="executor",
        native_kind="built_in",
        inputs=(),
        definition={"id": "rendering.timeline_visualize", "metadata": {}},
    )
    executor_definition = SimpleNamespace(to_dict=lambda: {"id": capability.id})
    fake_sdk = SimpleNamespace(
        _load_registries=lambda **_: ({capability.id: executor_definition}, None, None),
        get_capability=lambda *_, **__: capability,
    )
    monkeypatch.setattr(invocation, "_sdk_module", lambda: fake_sdk)
    monkeypatch.setattr(invocation, "_validate_timeline_visualize_inputs", lambda *_, **__: authority)
    return capability


def test_scene_only_private_preflight_repreparation_keeps_carrier_without_video(monkeypatch):
    seen = {"inputs": None}

    def prepare(values, *, project, client):
        seen["prepared_include_media"] = values["include_media"]
        return {
            "capture_snapshot": {
                "project_slug": project,
                "config": {"clips": []},
                "video_digest": VIDEO_DIGEST,
                "metadata": {
                    "capture_identity": VIDEO_DIGEST,
                    "capture_authority": {"parent_revision_id": "r1"},
                    "scene_clips": {"clip": {"address": "c1.picture"}},
                },
            },
            "capture_identity": VIDEO_DIGEST,
            "video_digest": VIDEO_DIGEST,
            "video_object_id": VIDEO_DIGEST,
            "managed_object_reference": VIDEO_DIGEST,
            "timeline_id": "main",
        }

    def invoke(capability_id, **kwargs):
        seen["inputs"] = kwargs["inputs"]
        return SimpleNamespace(ok=False)

    monkeypatch.setattr(timeline_filmstrip, "prepare_filmstrip", prepare)
    monkeypatch.setattr(invocation, "_invoke_internal_result", invoke)
    spans, _ = timeline_filmstrip._invoke_scene_only(
        {"timeline_ref": "main"}, project="project-1", client=SimpleNamespace()
    )

    assert spans[0].cls == "UNAVAILABLE"
    assert seen["prepared_include_media"] is False
    assert seen["inputs"]["mode"] == "scene_only"
    assert "rendered_video" not in seen["inputs"]


def test_private_filmstrip_backend_preflight_enrichment_reaches_kernel(monkeypatch):
    authority = {
        "mode": "filmstrip",
        "video_object_id": VIDEO_DIGEST,
        "video_digest": VIDEO_DIGEST,
        "filmstrip_snapshot": {"project_slug": "project-1"},
    }
    _filmstrip_invoke_fixtures(monkeypatch, authority)
    captured = {}

    def fake_kernel(capability, **kwargs):
        captured.update(kwargs)
        return "run-1", "task-1", "attempt-1", None, {"ok": True}, True, None

    monkeypatch.setattr(invocation, "_kernel_invoke", fake_kernel)
    result = invocation._invoke_internal_result(
        "rendering.timeline_visualize",
        kind="executor",
        project="project-1",
        inputs={"view": "filmstrip"},
        client=SimpleNamespace(),
    )

    assert result.ok
    assert captured["inputs"]["rendered_video"] == {
        "digest": VIDEO_DIGEST,
        "object_id": VIDEO_DIGEST,
    }
    assert "filmstrip_authority" in captured["inputs"]
    assert captured["idempotency_context"]["video_object_id"] == VIDEO_DIGEST


def test_private_backend_input_only_preflight_forwards_snapshot_without_video(monkeypatch):
    authority = {
        "mode": "input_only",
        "input_snapshot": {"project_slug": "project-1"},
    }
    _filmstrip_invoke_fixtures(monkeypatch, authority)
    captured = {}

    def fake_kernel(capability, **kwargs):
        captured.update(kwargs)
        return "run-1", "task-1", "attempt-1", None, {"ok": True}, True, None

    monkeypatch.setattr(invocation, "_kernel_invoke", fake_kernel)
    result = invocation._invoke_internal_result(
        "rendering.timeline_visualize",
        kind="executor",
        project="project-1",
        inputs={"view": "filmstrip", "hide": ["output"]},
        client=SimpleNamespace(),
    )

    assert result.ok
    assert captured["inputs"]["project_slug"] == "project-1"
    assert "rendered_video" not in captured["inputs"]
    assert "filmstrip_authority" in captured["inputs"]


def test_private_filmstrip_backend_keeps_strict_video_identity_rejection(monkeypatch):
    authority = {
        "mode": "filmstrip",
        "video_object_id": VIDEO_DIGEST,
        "video_digest": "sha256:" + "e" * 64,
        "filmstrip_snapshot": {"project_slug": "project-1"},
    }
    _filmstrip_invoke_fixtures(monkeypatch, authority)

    result = invocation._invoke_internal_result(
        "rendering.timeline_visualize",
        kind="executor",
        project="project-1",
        inputs={"view": "filmstrip"},
        client=SimpleNamespace(),
    )

    assert not result.ok
    assert result.error["type"] == "CapabilityValidationError"
    assert "identity mismatch" in result.error["message"]


def test_managed_render_snapshot_is_forwarded_to_runtime_task(monkeypatch) -> None:
    """The post-preflight snapshot must reach Runtime admission."""

    capability = SimpleNamespace(
        id="rendering.render",
        capability_type="executor",
        native_kind="built_in",
        inputs=(),
        definition={"id": "rendering.render", "metadata": {}},
    )
    executor_definition = SimpleNamespace(to_dict=lambda: {"id": "rendering.render"})
    fake_sdk = SimpleNamespace(
        _load_registries=lambda **_: ({"rendering.render": executor_definition}, None, None),
        get_capability=lambda *_, **__: capability,
    )
    monkeypatch.setattr(invocation, "_sdk_module", lambda: fake_sdk)

    snapshot = {
        "timeline_id": "timeline-1",
        "project_id": "project-1",
        "config_version": 2,
        "config": {"clips": []},
        "registry": {"assets": {}},
    }
    prepared = {
        "timeline_ref": "timeline-1",
        "timeline_snapshot": snapshot,
        "timeline_authority": {"timeline_id": "timeline-1", "config_version": 2},
    }
    monkeypatch.setattr(
        invocation,
        "_prepare_managed_render_inputs",
        lambda inputs, **_: (prepared, {"timeline_id": "timeline-1"}),
    )

    monkeypatch.setattr(storage_module, "managed_object_sizes", lambda *_: {})
    monkeypatch.setattr(storage_module, "used_effect_asset_sizes", lambda *_: {})
    monkeypatch.setattr(
        storage_module,
        "estimate_managed_render_storage",
        lambda **_: {"estimated_scratch_bytes": 0, "estimated_output_bytes": 0},
    )

    captured: dict[str, object] = {}

    def fake_kernel(capability, **kwargs):
        captured.update(kwargs)
        return "run-1", "task-1", "attempt-1", None, {"ok": True}, True, None

    monkeypatch.setattr(invocation, "_kernel_invoke", fake_kernel)

    client = SimpleNamespace(
        media=SimpleNamespace(list=lambda *_args, **_kwargs: [[{"digest": "sha256:" + "a" * 64, "size": 1}], None])
    )
    result = invocation.invoke(
        "rendering.render",
        kind="executor",
        project="project-1",
        inputs={"timeline_ref": "timeline-1"},
        client=client,
    )

    assert result.ok
    assert captured["inputs"] == prepared
