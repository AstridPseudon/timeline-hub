"""Disposable producer proof; the transport below is not Runtime acceptance."""
from __future__ import annotations

import hashlib
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid import sdk
from astrid.core._shared.result_manifest import harvest_staged_outputs
from astrid.core.execution.generic_host import GenericPackHost, HostError
from astrid.core.media import MediaProbe, MediaProbeError
from astrid.packs.rendering.actions.render import run
from astrid.sdk.invocation import (
    _automatic_generation_intent,
    _generation_capability_modality,
    _generation_publish_effect,
    _kernel_invoke,
    get_capability,
)
from astrid.sdk.remote import RemoteTasks
from astrid.sdk.workspace_client import WorkspaceClientError


@pytest.fixture(scope="module")
def producer():
    registries = sdk._load_registries(include_elements=False)
    cap = get_capability("rendering.render", kind="executor", include_elements=False,
                         _registries=registries)
    definition = registries[0].get(cap.id)
    record = SimpleNamespace(id=cap.id, definition=definition)
    intent = _automatic_generation_intent(cap, {}, modality=_generation_capability_modality(cap))
    return cap, record, intent, registries


@pytest.fixture
def rendered(tmp_path, monkeypatch):
    """Use the real facade with deterministic render/probe backend seams."""
    timeline = tmp_path / "timeline.json"
    assets = tmp_path / "assets.json"
    timeline.write_text('{"tracks": [], "clips": []}')
    assets.write_text('{"assets": {}}')
    out = tmp_path / "outputs" / "final.mp4"
    out.parent.mkdir()
    def render(*args, **kwargs):
        assert kwargs["out_path"] == out
        out.write_bytes(b"deterministic-final-video")
        Path(f"{out}.provenance.json").write_text('{}')
        return out
    def probe(path):
        assert path == out
        assert path.read_bytes() == b"deterministic-final-video"
        return MediaProbe(duration_seconds=2.5, video_stream_present=True)
    monkeypatch.setattr(run, "_default_service", lambda: SimpleNamespace(render=render))
    monkeypatch.setattr(run, "ffprobe_metadata_strict", probe)
    assert run.render(timeline, assets, out) == out
    return out


def _harvest(record, out):
    return harvest_staged_outputs(out.parent, definition=record.definition, require=True)


def test_actual_render_admission_and_settlement_exclude_siblings(producer, rendered, tmp_path):
    cap, record, intent, registries = producer
    assert cap.definition["metadata"]["generation_publication"] == {
        "version": 1, "modality": "video", "output_port": "video"}
    calls = []
    client = SimpleNamespace(tasks=SimpleNamespace(create=lambda **kw: (
        calls.append(kw) or SimpleNamespace(ok=True, data={"run_id": "r", "task_id": "t"}))))
    _kernel_invoke(cap, kind="executor", project="P", inputs={}, outputs={},
                   generation_intent=intent, _client=client)
    effect = calls[0]["settlement_effect"]
    assert effect["effect_type"] == "generation.publish_v1"
    assert effect["payload"]["groups"][0]["selectors"] == [{
        "selector": "main-0", "ordinal": 0, "variant_key": "original",
        "required": True, "output_port": "video"}]
    host = object.__new__(GenericPackHost)
    host.client = SimpleNamespace(INLINE_SETTLEMENT_OUTPUTS=True, upload_object=lambda *a, **kw: None)
    # The provenance appears first: position is never publication identity.
    typed = host._typed_outputs(record, list(reversed(_harvest(record, rendered))),
                                tmp_path, generation_intent=intent)
    settled = host._upload_outputs(typed, project_id="P")
    video = next(row for row in settled if row["name"] == "video")
    assert video["digest"] == "sha256:" + hashlib.sha256(rendered.read_bytes()).hexdigest()
    assert video["ordinal"] == 0
    assert video["selector"] == {"group_key": "main", "variant_key": "original"}
    assert video["metadata"] == {"duration_seconds": 2.5}
    assert all("selector" not in row and "metadata" not in row
               for row in settled if row["name"] != "video")
    import yaml
    actions = yaml.safe_load((Path(__file__).resolve().parents[3] /
        "astrid/packs/rendering/pack.yaml").read_text())["actions"]
    for name in ("timeline_visualize", "timeline_storyboard"):
        sibling = SimpleNamespace(id=f"rendering.{name}", definition=actions[name],
                                  capability_type="executor")
        assert _generation_capability_modality(sibling) is None
        assert _automatic_generation_intent(sibling, {}, modality=None) is None
    from astrid.packs.rendering.actions.render.task_adapter import FAMILY
    assert FAMILY == "render_export"
    assert _generation_capability_modality(SimpleNamespace(id=FAMILY, definition={})) is None


@pytest.mark.parametrize("duration", [None, 0, -1, float("nan"), float("inf"),
                                      -float("inf"), True, "2.5", {}])
def test_invalid_intrinsic_duration_refuses_before_manifest(tmp_path, monkeypatch, duration):
    out = tmp_path / "final.mp4"
    out.write_bytes(b"fixture")
    monkeypatch.setattr(run, "ffprobe_metadata_strict", lambda path: MediaProbe(
        duration_seconds=duration, video_stream_present=True))
    with pytest.raises(ValueError, match="intrinsic duration_seconds"):
        run._write_render_manifest(out, timeline_path=tmp_path / "timeline.json", selector="fixture")
    assert not (tmp_path / "manifest.json").exists()


@pytest.mark.parametrize("fault", ["no-video", "probe-failure"])
def test_final_file_requires_a_strict_video_probe(tmp_path, monkeypatch, fault):
    out = tmp_path / "final.mp4"
    out.write_bytes(b"fixture")
    def probe(path):
        assert path == out
        if fault == "probe-failure":
            raise MediaProbeError("invalid file")
        return MediaProbe(duration_seconds=2.5, video_stream_present=False)
    monkeypatch.setattr(run, "ffprobe_metadata_strict", probe)
    with pytest.raises((ValueError, MediaProbeError)):
        run._write_render_manifest(out, timeline_path=tmp_path / "timeline.json", selector="fixture")
    assert not (tmp_path / "manifest.json").exists()


@pytest.mark.parametrize("fault", ["missing", "duplicate", "implicit", "wrong-ordinal",
    "wrong-port", "wrong-selector", "ambiguous", "auxiliary", "wrong-hash",
    "missing-duration", "nan-duration", "neighbor-duration"])
def test_host_refuses_bad_exact_identity_or_duration(producer, rendered, tmp_path, fault):
    _, record, original_intent, _ = producer
    intent = deepcopy(original_intent)
    rows = _harvest(record, rendered)
    video = rows[0]
    if fault == "missing":
        rows.pop(0)
    elif fault == "duplicate":
        rows.append(dict(video))
    elif fault == "implicit":
        video["ordinal_explicit"] = False
    elif fault == "wrong-ordinal":
        video["ordinal"] = 2
    elif fault == "wrong-port":
        video["output_port"] = "provenance"
    elif fault == "wrong-selector":
        video["selector"] = {"group_key": "other", "variant_key": "original"}
    elif fault == "ambiguous":
        intent["groups"].append({"group_key": "other", "selectors": [
            {"selector": "other-0", "ordinal": 0, "variant_key": "original"}]})
    elif fault == "auxiliary":
        video["role"] = "auxiliary"
    elif fault == "wrong-hash":
        video["content_hash"] = "sha256:" + "0" * 64
    elif fault == "missing-duration":
        video.pop("duration_seconds")
    elif fault == "nan-duration":
        video["duration_seconds"] = float("nan")
    elif fault == "neighbor-duration":
        video.pop("duration_seconds")
        rows[1]["duration_seconds"] = 99
    host = object.__new__(GenericPackHost)
    with pytest.raises(HostError):
        host._typed_outputs(record, rows, tmp_path, generation_intent=intent)


@pytest.mark.parametrize("inline", [True, False])
def test_final_video_duration_survives_both_upload_paths(producer, rendered, tmp_path, inline):
    _, record, intent, _ = producer
    host = object.__new__(GenericPackHost)
    host.client = SimpleNamespace(INLINE_SETTLEMENT_OUTPUTS=inline, upload_object=lambda path, **kw:
        SimpleNamespace(digest="sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(), size=path.stat().st_size))
    typed = host._typed_outputs(record, _harvest(record, rendered), tmp_path, generation_intent=intent)
    assert host._upload_outputs(typed, project_id="P")[0]["metadata"] == {"duration_seconds": 2.5}


def test_lost_admission_response_preserves_body_effect_and_output(producer, rendered, tmp_path):
    cap, record, intent, _ = producer
    effect = _generation_publish_effect(cap, project="P", generation_intent=intent)
    class Transport:
        def __init__(self):
            self.requests, self.accepted = [], {}
        def list_capabilities(self, **kw):
            return [[{"capability_id": cap.id, "definition_digest": "sha256:" + "a" * 64}], None]
        def get_project(self, project):
            return {"project_id": project}
        def admit_task(self, **body):
            self.requests.append(deepcopy(body))
            key = body["idempotency_key"]
            if key in self.accepted and self.accepted[key][0] != body:
                raise WorkspaceClientError(409, "idempotency_conflict", "changed body")
            receipt = {"run_id": "r", "task_id": "t", "attempt_id": "a"}
            self.accepted.setdefault(key, (deepcopy(body), receipt))
            if len(self.requests) == 1:
                raise WorkspaceClientError(503, "response_lost", "lost after acceptance")
            return self.accepted[key][1]
    transport = Transport()
    tasks = RemoteTasks(transport)
    arguments = dict(project_id="P", capability=cap.id, spec={"inputs": {"timeline": "sha256:fixture"}},
        generation_intent=intent, settlement_effect=effect, deterministic_idempotency=True)
    first = tasks.create(**arguments)
    assert not first.ok
    retry = tasks.create(**deepcopy(arguments))
    assert retry.ok and len(transport.accepted) == 1
    assert first.idempotency_key == retry.idempotency_key
    assert transport.requests[0] == transport.requests[1]
    assert tasks.create(**deepcopy(arguments)).data == retry.data
    changed = deepcopy(arguments)
    changed["spec"]["inputs"]["timeline"] = "sha256:changed"
    refused = tasks.create(**changed, idempotency_key=retry.idempotency_key)
    assert not refused.ok and len(transport.accepted) == 1
    host = object.__new__(GenericPackHost)
    host.client = SimpleNamespace(INLINE_SETTLEMENT_OUTPUTS=True, upload_object=lambda *a, **kw: None)
    def settle():
        return host._upload_outputs(host._typed_outputs(record, _harvest(record, rendered),
            tmp_path, generation_intent=intent), project_id="P")
    assert settle() == settle()
#
