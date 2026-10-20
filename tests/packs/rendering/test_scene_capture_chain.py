"""Composed sampling and public host facts; pixel production is an injected seam."""
import json
from copy import deepcopy

import pytest
from PIL import Image

from astrid.core.element.registry import ElementRegistry
from astrid.core.element.schema import ElementDefinition
from astrid.core.rendering.remotion_runtime import RemotionRuntimeStatus
from astrid.core.theme import builtin_theme
from astrid.core.timeline import scene_answers
from astrid.packs.rendering.actions.timeline_visualize import composed_frame, filmstrip_cards
from astrid.packs.rendering.actions.timeline_visualize.layers.builtin import render_lint
from astrid.packs.rendering.actions.timeline_visualize.motion import model, sheet
from astrid.packs.rendering.rendering.renderers.remotion import run as renderer
from astrid.packs.rendering.rendering.renderers.remotion.canonical_transitions import (
    compile_canonical_root_props,
)
from tests.packs.rendering.test_canonical_root_compiler import compiler_host as _compiler_host
from tests.packs.rendering.test_host_scene import host_project as _host_project

compiler_host = _compiler_host
host_project = _host_project


@pytest.mark.parametrize("canonical_incoming", [False, True])
def test_selected_samples_reach_public_host_labels_occlusion_and_checks(
    compiler_host, tmp_path, monkeypatch, canonical_incoming,
):
    project, tools = compiler_host
    pack_element = project.parent / "probe/effects/test-card"
    component = pack_element / "component.tsx"
    component.write_text(component.read_text().replace(
        "opaqueSupport: 'rect', bounds: {status: 'known', rect}})",
        "opaqueSupport: 'rect', bounds: {status: 'known', rect}, diagnostics: {"
        "text: {bounds: {status: 'known', rect}, minPx: 20},"
        "face: {status: 'known', rect: {x: 0, y: 0, width: 0, height: 0}}}})"))
    entries = list(renderer.load_default_registry(project_root=renderer.REPO_ROOT).list())
    entries.append(ElementDefinition(
        id="test-card", kind="effects", root=pack_element, source="pack:probe", editable=True,
        priority=100, component=pack_element / "component.tsx", schema={}, defaults={},
        metadata={"pack_id": "probe"}))
    registry_entries = ElementRegistry(entries)
    monkeypatch.setattr(renderer, "load_default_registry", lambda **kwargs: registry_entries)
    canvas = {"width": 1920, "height": 1080, "fps": 30}
    config = {"theme": "historical-unused-slug", "theme_overrides": {"visual": {"canvas": canvas}},
              "tracks": [{"id": "front", "kind": "visual", "label": "Front"},
                         {"id": "plate", "kind": "visual", "label": "Picture"}],
              "clips": []}
    for cid, track, start, hold in [("upper", "front", 0, 2), ("a", "plate", 0, 1),
                                   ("b", "plate", 1, 1)]:
        config["clips"].append({
            "id": cid, "track": track, "clipType": "test-card", "at": start, "hold": hold,
            "x": 1900, "y": 100, "width": 100, "height": 100,
            "params": {"text": cid},
            "elementRef": {"kind": "effect", "id": "test-card", "packId": "probe"},
            "app": {"cut": "c01", "layer": cid},
        })
    if canonical_incoming:
        config["clips"][-1]["transition"] = {"type": "fade", "duration": .4}
    registry = {"assets": {}}
    theme = builtin_theme()
    theme["visual"]["canvas"] = canvas
    snapshot = {"config": config, "registry": registry, "clips": config["clips"],
                "fps_rational": [30, 1], "duration_frames": 60, "scripts": [],
                "project_slug": "demo", "timeline_id": "timeline", "render_run_id": "capture",
                "video_digest": "sha256:" + "a" * 64}
    original = deepcopy(snapshot)
    timeline, assets, theme_path = [tmp_path / name for name in ("timeline.json", "assets.json", "theme.json")]
    for path, value in ((timeline, config), (assets, registry), (theme_path, theme)):
        path.write_text(json.dumps(value))
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        RemotionRuntimeStatus(True, project, node_executable=tools.node_executable))
    monkeypatch.setattr(renderer, "_validate_project_dir", lambda project: tools)
    monkeypatch.setattr(renderer, "_regenerate_element_registries", lambda *args: None)
    monkeypatch.setattr(renderer, "_validate_renderer_effect_registry", lambda *args: None)
    monkeypatch.setattr(renderer, "_effective_registry_state", lambda *args: {"hash": "test-registry"})
    monkeypatch.setattr(renderer, "_available_remotion_port", lambda: 32101)
    monkeypatch.setattr(composed_frame, "_SHARED_REMOTION_OWNER", None)
    monkeypatch.setattr(composed_frame, "renderer_environment_identity", lambda: "composed-test")
    monkeypatch.setattr(model, "boxes_at", lambda *args: pytest.fail("private layout must not run"))
    queries, rendered, observed, reserved, contexts = [], [], [], [], []
    real_query = scene_answers.host_frames_at

    def query(props, basis, frames):
        queries.append(list(frames))
        assert props == observed[-1]
        return real_query(props, basis, frames)

    monkeypatch.setattr(scene_answers, "host_frames_at", query)

    class Prepared(Exception):
        pass

    def capture(timeline, assets, output, frames, **kwargs):
        rendered.append(list(frames))

        def observe(props, actual_frames):
            assert props == json.loads((tmp_path / ".remotion-props.json").read_text())
            assert "compiledTransitions" not in props  # production compiler remains inactive
            if canonical_incoming:
                # Explicit test-only prepared input, separate from native production
                # admission. The same public compiler is covered against registered SSR.
                props = compile_canonical_root_props(props, project_dir=project, runtime_tools=tools)
            observed.append(deepcopy(props))
            kwargs["on_scene_props"](props, actual_frames)
            raise Prepared()

        with pytest.raises(Prepared):
            renderer._execute_remotion_locked(
                timeline, assets, tmp_path / "unused.mp4", provenance_out_path=tmp_path / "unused.mp4",
                project_dir=project, composition_id="TimelineComposition", theme_path=theme_path,
                min_free_gb=None, frame_numbers=frames, frame_output_dir=output, on_scene_props=observe)
        result = {}
        for frame in frames:
            path = output / f"{frame}.png"
            Image.new("RGB", (40, 24)).save(path)
            result[frame] = path
        return result

    monkeypatch.setattr(renderer, "capture_remotion_frames", capture)
    provider = composed_frame.RemotionFrameProvider(
        snapshot, timeline_path=timeline, assets_path=assets, project_dir=project,
        cache=composed_frame.FrameCaptureCache(tmp_path / "cache"), scene_labels=True)
    reserve = provider.reserve_scene_frames

    def record_reservation(frames):
        reserved.append(list(frames))
        reserve(frames)

    def compose(ctx, layers, root, **kwargs):
        contexts.append(ctx)
        findings = render_lint(ctx).findings
        return {"png": [], "findings": findings, "layers": ["lint"]}

    monkeypatch.setattr(provider, "reserve_scene_frames", record_reservation)
    monkeypatch.setattr(sheet, "compose_motion_sheet", compose)
    monkeypatch.setattr(filmstrip_cards, "_audio_envelope", lambda *args: None)
    options = {"view": "motion", "range": (.4, 1.2), "explicit_interval": True,
               "every_frames": 23, "layers": ["lint"]}
    cards = filmstrip_cards.plan_filmstrip(snapshot, options)["cards"]
    pixels = [card["frame"] for card in cards]
    try:
        result = filmstrip_cards.build_filmstrip_pack(
            out_root=tmp_path / "pack", snapshot=snapshot, options=options, frame_provider=provider)
        assert reserved == [[24]] and 24 not in pixels
        assert rendered == [sorted(pixels)]
        assert queries == [list(dict.fromkeys(sorted(pixels) + [24]))]
        assert set(provider.scene_frames) == {str(frame) for frame in queries[0]}
        assert set(provider.label_batches) == set(queries[0])
        assert all(label.status == "known" for labels in provider.label_batches.values() for label in labels)
        assert result["frame_index"]["cards"] == cards and snapshot == original
        assert provider.scene_unavailable is None
        assert not (tmp_path / ".remotion-props.json").exists()
        shared = contexts[0].shared
        assert shared["scene_frames"] == provider.scene_frames
        assert shared["scene_occlusions"] == provider.scene_occlusions
        assert shared["scene_clip_identities"] == provider.scene_clip_identities
        found = shared["check_findings"]
        assert {f["code"] for f in found} >= {"FRAME", "SAFE", "SMALL", "COVER"}
        assert not any(f["code"] in ("SCENE", "REGION") for f in found)
        lower = "b" if canonical_incoming else "a"
        assert provider.scene_occlusions["0.98"]["24"][lower]["occluderId"] == "upper"
        assert any(f["code"] == "COVER" and f["message"] ==
                   f'test-card "upper" fully covers test-card "{lower}"' for f in found)
        if canonical_incoming:
            layer = next(layer for layer in provider.scene_frames["24"]["layers"] if layer["clipId"] == "b")
            assert layer["contentFrame"] == 6 and layer["transitionOpacity"] == .5
            assert config["clips"][-1]["at"] == 1 > 24 / 30
        cached = filmstrip_cards.build_filmstrip_pack(
            out_root=tmp_path / "cached", snapshot=snapshot, options=options, frame_provider=provider)
        assert len(queries) == len(rendered) == 1
        assert "cached" in cached["frame_index"]["frame_capture"]["scene_unavailable"]
        assert provider.scene_frames == provider.scene_occlusions == provider.label_batches == {}
        assert provider._reserved_scene_frames == provider._active_reserved_scene_frames == ()
        assert any(f["code"] == "SCENE" for f in contexts[-1].shared["check_findings"])
    finally:
        provider.close()
