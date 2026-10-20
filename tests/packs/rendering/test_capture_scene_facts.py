"""Fresh capture handoff over public scene rows; no browser or pixel proof."""
import copy
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from PIL import Image

from astrid.core.timeline import scene_answers
from astrid.core.timeline.scene_answers import occlusions_from_frames
from astrid.core.timeline.shot_composition_projection import project_shot_composition
from astrid.packs.rendering.actions.timeline_visualize import composed_frame, filmstrip_cards
from astrid.packs.rendering.actions.timeline_visualize.layers import builtin_checks
from astrid.packs.rendering.actions.timeline_visualize.layers.base import CheckContext
from astrid.packs.rendering.actions.timeline_visualize.layers.builtin import render_lint
from astrid.packs.rendering.actions.timeline_visualize.motion import lint, model, sheet
from astrid.packs.rendering.actions.timeline_visualize.overlays import labels
from tests.packs.rendering.test_scene_query_occlusion import admitted_public_evaluation
from tests.packs.rendering.test_scene_query_occlusion import installed as _public_occlusion

public_occlusion = _public_occlusion

ROOT = Path(__file__).resolve().parents[3]
CANVAS = {"width": 200, "height": 100, "fps": 30}


@pytest.fixture(scope="module")
def public_rows():
    # An explicit export alias lets an admitted release be tested read-only,
    # without changing installed packages or tracked consumer pins.
    evaluation = admitted_public_evaluation()
    node = os.environ.get("ASTRID_NODE_EXECUTABLE") or shutil.which("node")
    script = """
import {prepareScene, querySceneFrame} from EVALUATION;
const clips = [
  {id: 'compiled-first', clipType: 'test-card', track: 'plate', at: 0, hold: 1},
  {id: 'totally-different', clipType: 'test-card', track: 'plate', at: 2, hold: 1},
];
const components = Object.fromEntries(clips.map(clip => [clip.id, {
  identity: clip.id, frame: contentFrame => ({presence: 'present', opaqueSupport: 'rect',
    bounds: {status: 'known', rect: {x: 20, y: 10, width: 60, height: 40}},
    diagnostics: {motion: {contentFrame}}}),
}]));
const scene = prepareScene([{track: {id: 'plate', kind: 'visual'}, clips, transitions: [null]}],
  {assets: {}}, 30, 200, 100, {elements: new Set(['test-card']), capabilities: {components},
    roles: Object.fromEntries(clips.map(clip => [clip.id, 'picture']))});
console.log(JSON.stringify({clips, answers: [0, 1, 12, 15, 60, 90].map(frame => querySceneFrame(scene, frame))}));
""".replace("EVALUATION", json.dumps(evaluation.as_uri()))
    result = subprocess.run([node, "--input-type=module", "-e", script], check=True,
                            capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)


@pytest.fixture
def captured(public_rows, tmp_path, monkeypatch):
    props = {"timeline": {"tracks": [{"id": "plate", "kind": "visual"}],
                          "clips": copy.deepcopy(public_rows["clips"])},
             "assets": {"assets": {}}, "theme": {"id": "actual-theme", "visual": {"canvas": dict(CANVAS)}},
             "compiledTransitions": {"identity": "actual-serialized-carrier"}, "generation": 17}
    for clip, occurrence in zip(props["timeline"]["clips"], ("one", "two")):
        clip["shot_occurrence_id"] = occurrence
        clip["app"] = {"cut": "c01", "layer": "card", "astrid_shot_composition": {
            "source_clip_id": "reused:card", "occurrence_id": occurrence,
            "shot_revision_id": "child-r1"}}
    snapshot = {"config": props["timeline"], "registry": props["assets"], "fps_rational": [30, 1],
                "metadata": {"canonical_timeline": {"parent_revision_id": "r1"}},
                "timeline_id": "timeline", "render_run_id": "capture", "duration_frames": 120,
                "project_slug": "demo", "video_digest": "sha256:" + "a" * 64,
                "clips": props["timeline"]["clips"], "scripts": []}
    calls, occlusion_calls = [], []

    def query(actual, basis, frames):
        calls.append((copy.deepcopy(actual), copy.deepcopy(basis), list(frames)))
        assert actual is props
        return [copy.deepcopy(next(row for row in public_rows["answers"] if row["frame"] == frame))
                for frame in frames]

    def occlude(answers, targets):
        occlusion_calls.append((copy.deepcopy(answers), copy.deepcopy(targets)))
        # Peer API stub: this test covers carrying the public result unchanged.
        return [{"status": "unknown", "reason": f"peer fixture threshold {t['min_fraction']}"}
                for t in targets]

    monkeypatch.setattr(scene_answers, "host_frames_at", query)
    monkeypatch.setattr(scene_answers, "occlusions_from_frames", occlude, raising=False)
    monkeypatch.setattr(composed_frame, "renderer_environment_identity", lambda: "test-closure")
    provider = None

    def render(frames, output, _resolution):
        provider._scene_labels(props, frames)
        result = {}
        for frame in frames:
            path = output / f"{frame}.png"
            Image.new("RGB", (200, 100), (frame % 256, 0, 0)).save(path)
            result[frame] = path
        return result

    provider = composed_frame.RemotionFrameProvider(
        snapshot, timeline_path=tmp_path / "timeline.json", assets_path=tmp_path / "assets.json",
        project_dir=tmp_path, cache=composed_frame.FrameCaptureCache(tmp_path / "cache"), renderer=render)
    return provider, props, calls, occlusion_calls


def cards(*frames):
    return [{"frame": frame, "image": f"frames/{frame}.png"} for frame in frames]


@pytest.mark.integration
def test_actual_public_rows_and_labels_share_one_whole_props_query(captured, public_rows, tmp_path):
    provider, props, calls, occlusion_calls = captured
    original = copy.deepcopy(props)
    info = provider.capture(cards(60, 0, 0), tmp_path / "pack")
    assert info["fresh_frames"] == 3
    assert len(calls) == 1 and calls[0] == (props, CANVAS, [0, 60])
    assert calls[0][0]["compiledTransitions"] == original["compiledTransitions"]
    assert props == original
    assert provider.scene_unavailable is None
    assert provider.scene_frames == {str(row["frame"]): row for row in public_rows["answers"] if row["frame"] in (0, 60)}
    assert provider.label_batches == labels.labels_from_frames(props["timeline"], list(provider.scene_frames.values()))
    assert [provider.label_batches[f][0].address for f in (0, 60)] == ["c01.card", "c01.card"]
    assert provider.label_batches[0][0].bounds == (20, 10, 80, 50)
    assert provider.scene_frames["0"]["layers"][0]["diagnostics"]["motion"] == {"contentFrame": 0}
    assert provider.scene_clip_identities == {
        "compiled-first": {"clip_id": "reused:card", "occurrence_id": "one"},
        "totally-different": {"clip_id": "reused:card", "occurrence_id": "two"}}
    answers, targets = occlusion_calls[0]
    assert answers == list(provider.scene_frames.values())
    assert targets == [{"frame": f, "clip_id": clip, "min_fraction": fraction}
                       for fraction in (0.9, 0.98) for f, clip in ((0, "compiled-first"), (60, "totally-different"))]
    assert provider.scene_occlusions["0.9"]["0"]["compiled-first"] == {
        "status": "unknown", "reason": "peer fixture threshold 0.9"}
    assert provider.scene_occlusions["0.98"]["0"]["compiled-first"]["reason"].endswith("0.98")


@pytest.mark.integration
def test_cache_mixed_batches_and_new_revision_do_not_reuse_scene_facts(captured, tmp_path):
    provider, props, calls, _ = captured
    provider.capture(cards(0), tmp_path / "pack")
    old_frames = provider.scene_frames
    cached = provider.capture(cards(0), tmp_path / "pack")
    assert cached["cached_frames"] == 1 and len(calls) == 1
    assert provider.scene_frames == provider.scene_occlusions == provider.scene_clip_identities == {}
    assert provider.label_batches == {} and "cached" in provider.scene_unavailable
    assert old_frames["0"]["frame"] == 0  # a prior context stays an independent value
    mixed = provider.capture(cards(0, 1), tmp_path / "pack")
    assert mixed["evidence_source"] == "mixed" and set(provider.scene_frames) == {"1"}
    assert "cached" in provider.scene_unavailable and calls[-1][2] == [1]
    provider.snapshot["metadata"]["canonical_timeline"]["parent_revision_id"] = "r2"
    props["generation"] = 18
    props["theme"]["id"] = "r2-theme"
    provider.capture(cards(60), tmp_path / "pack")
    assert set(provider.scene_frames) == {"60"} and provider.scene_unavailable is None
    assert calls[-1][0]["generation"] == 18 and calls[-1][0]["theme"]["id"] == "r2-theme"


@pytest.mark.integration
def test_observer_failure_does_not_change_capture_or_cache(captured, tmp_path, monkeypatch):
    provider, _props, _calls, _ = captured

    def fail(*_args):
        raise scene_answers.SceneQueryUnavailable("observer unavailable")

    monkeypatch.setattr(scene_answers, "host_frames_at", fail)
    info = provider.capture(cards(0), tmp_path / "pack")
    assert info["fresh_frames"] == 1 and info["scene_unavailable"] == "observer unavailable"
    assert provider.scene_frames == {} and provider.label_batches == {}
    assert (tmp_path / "pack/frames/0.png").is_file()
    cached = provider.capture(cards(0), tmp_path / "pack")
    assert cached["cached_frames"] == 1


@pytest.mark.integration
def test_missing_occlusion_api_keeps_native_rows_and_labels(captured, tmp_path, monkeypatch):
    provider, _, _, _ = captured
    monkeypatch.delattr(scene_answers, "occlusions_from_frames")
    info = provider.capture(cards(0), tmp_path / "pack")
    assert info["fresh_frames"] == 1 and info["scene_unavailable"]
    assert provider.scene_frames["0"]["layers"][0]["clipId"] == "compiled-first"
    assert provider.label_batches[0][0].status == "known"
    assert provider.scene_occlusions == {}


@pytest.mark.integration
def test_native_empty_scene_is_distinct_from_no_captured_facts(captured, tmp_path):
    provider, _, _, occlusion_calls = captured
    provider.capture(cards(90), tmp_path / "pack")
    assert provider.scene_frames["90"]["coverage"] == "GAP"
    assert provider.scene_unavailable is None and provider.label_batches[90] == []
    assert not occlusion_calls


@pytest.mark.integration
def test_missing_canvas_basis_never_falls_back_to_current_theme(captured, tmp_path):
    provider, props, calls, _ = captured
    del props["theme"]["visual"]["canvas"]["fps"]
    provider.capture(cards(0), tmp_path / "pack")
    assert not calls and "basis" in provider.scene_unavailable
    assert provider.scene_frames == {}


@pytest.mark.integration
def test_filmstrip_passes_scene_facts_through_context_to_builtin_check(captured, tmp_path, monkeypatch):
    provider, props, calls, _ = captured
    provider.snapshot["theme"] = copy.deepcopy(props["theme"])
    delivered = []

    def check(cut, elements, fps, **kwargs):
        delivered.append(kwargs["shared"])
        return []

    def compose(ctx, _layers, _root, **_kwargs):
        render_lint(ctx)
        return {"png": [], "findings": [], "layers": []}

    monkeypatch.setattr(builtin_checks.rules, "composition", check)
    monkeypatch.setattr(sheet, "compose_motion_sheet", compose)
    monkeypatch.setattr(filmstrip_cards, "_audio_envelope", lambda *_args: None)
    result = filmstrip_cards.build_filmstrip_pack(
        out_root=tmp_path / "pack", snapshot=provider.snapshot,
        options={"view": "motion", "at": 0, "frame": 0, "layers": ["lint"]}, frame_provider=provider)
    shared = delivered[0]
    assert shared["scene_frames"] == provider.scene_frames
    assert shared["scene_occlusions"] == provider.scene_occlusions
    assert shared["scene_clip_identities"] == provider.scene_clip_identities
    assert not shared.get("scene_unavailable")
    assert result["frame_index"]["frame_capture"]["fresh_frames"] == 1
    cached = filmstrip_cards.build_filmstrip_pack(
        out_root=tmp_path / "pack", snapshot=provider.snapshot,
        options={"view": "motion", "at": 0, "frame": 0, "layers": ["lint"]}, frame_provider=provider)
    assert len(calls) == 1  # even a retained snapshot theme cannot restore cached scene facts
    assert delivered[1]["scene_frames"] == {} and "cached" in delivered[1]["scene_unavailable"]
    receipt = json.loads(Path(cached["paths"]["json"]).read_text())
    assert receipt["cards"][0]["scene_status"] == "unavailable"


def test_historical_context_missing_facts_reports_unavailable_without_query(monkeypatch):
    def fail(*_args):
        raise AssertionError("must not query a current runtime for historical scene facts")

    monkeypatch.setattr(scene_answers, "host_frames_at", fail)
    snapshot = {"clips": [], "config": {}, "fps_rational": [30, 1]}
    cut = {"index": 1, "start": 0, "end": 1, "duration": 1}
    ctx = sheet.build_context(snapshot, cut, {}, fps=30, frame_size=(200, 100))
    assert ctx.shared["scene_frames"] == {} and ctx.shared["scene_unavailable"]


def test_bundle_only_builtin_check_retains_legacy_caller_path(monkeypatch):
    delivered = []
    monkeypatch.setattr(builtin_checks.rules, "composition", lambda *args, **kwargs:
                        delivered.append(kwargs.get("shared")) or [])
    ctx = CheckContext(cut={"index": 1}, cuts=[], fps=30, elements=[], all_elements=[],
                       words=[], beats={}, sfx=[], tracks=[], params={})
    builtin_checks._composition(ctx)
    assert delivered == [None]


def test_occurrence_identities_come_from_actual_projector_provenance(tmp_path, monkeypatch):
    graph = json.loads((ROOT / "tests/fixtures/timeline/shot_composition.json").read_text())
    graph["occurrences"] = graph["occurrences"][:2]
    projected = project_shot_composition(graph)
    by_source = {}
    for clip in projected.config["clips"]:
        source = clip["app"]["astrid_shot_composition"]["source_clip_id"]
        by_source.setdefault(source, []).append(clip)
    repeated = next(clips for clips in by_source.values() if len(clips) == 2)
    answers = [{"frame": int(clip["at"] * 30), "layers": [{"clipId": clip["id"], "role": "picture"}]}
               for clip in repeated]
    # This test isolates the identity join. Geometry and labels are exercised
    # above with complete rows from the public evaluator.
    monkeypatch.setattr(scene_answers, "host_frames_at", lambda *_args: answers)
    monkeypatch.setattr(labels, "labels_from_frames", lambda *_args: {})
    monkeypatch.setattr(scene_answers, "occlusions_from_frames", lambda _answers, targets:
                        [{"status": "unknown", "reason": "identity-only fixture"} for _ in targets], raising=False)
    provider = composed_frame.RemotionFrameProvider(
        {"fps_rational": [30, 1]}, timeline_path=tmp_path / "timeline.json", assets_path=tmp_path / "assets.json",
        project_dir=tmp_path, cache=composed_frame.FrameCaptureCache(tmp_path / "cache"), renderer=lambda *_args: {})
    provider._scene_labels({"timeline": projected.config, "assets": projected.registry,
                            "theme": {"visual": {"canvas": CANVAS}}}, [row["frame"] for row in answers])
    assert provider.scene_unavailable is None
    assert provider.scene_clip_identities == {clip["id"]: {
        "clip_id": clip["app"]["astrid_shot_composition"]["source_clip_id"],
        "occurrence_id": clip["app"]["astrid_shot_composition"]["occurrence_id"]} for clip in repeated}
    assert len({identity["occurrence_id"] for identity in provider.scene_clip_identities.values()}) == 2


@pytest.mark.integration
def test_captured_public_rows_reach_real_occlusion_bridge_and_shared_consumer(
    captured, public_occlusion, tmp_path, monkeypatch,
):
    provider, _, _, _ = captured
    monkeypatch.setattr(scene_answers, "occlusions_from_frames", occlusions_from_frames)
    provider.capture(cards(12, 15), tmp_path / "pack")
    assert provider.scene_unavailable is None
    for threshold in ("0.9", "0.98"):
        for frame in ("12", "15"):
            assert provider.scene_occlusions[threshold][frame]["compiled-first"] == {
                "status": "known", "occluderId": None, "fraction": 0}
    # This source ID intentionally differs from the compiled Root ID. Only the
    # captured source+occurrence provenance can join it to the public answer.
    element = model.Element("source-card", "am-type", "plate", 0, 1, {"text": "Card"},
                            {"id": "reused:card"}, occurrence_id="one")
    shared = {"scene_frames": provider.scene_frames, "scene_occlusions": provider.scene_occlusions,
              "scene_clip_identities": provider.scene_clip_identities}

    def forbidden(*_args):
        raise AssertionError("captured scene facts must not evaluate private layout")

    monkeypatch.setattr(model, "boxes_at", forbidden)
    cut = {"index": 1, "start": 0, "end": 1}
    found = lint.composition(cut, [element], 30, shared=shared)
    assert not any(f.code in ("SCENE", "COVER") for f in found)
    shared["scene_occlusions"]["0.98"]["12"]["compiled-first"] = {
        "status": "unknown", "reason": "planted public unknown"}
    assert any(f.code == "SCENE" and "planted public unknown" in f.message
               for f in lint.composition(cut, [element], 30, shared=shared))
