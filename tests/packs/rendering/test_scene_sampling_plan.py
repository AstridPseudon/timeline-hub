"""Exact check samples are metadata reservations, independent of pixel cards."""
import json
import os
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest
from PIL import Image

from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.timeline import scene_answers
from astrid.core.timeline.shot_composition_projection import project_shot_composition
from astrid.packs.rendering.actions.timeline_visualize import composed_frame, filmstrip_cards
from astrid.packs.rendering.actions.timeline_visualize.layers.builtin import render_lint
from astrid.packs.rendering.actions.timeline_visualize.motion import lint, model, sheet
from tests.packs.rendering.test_scene_query_occlusion import installed as _public_occlusion

public_occlusion = _public_occlusion

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.parametrize("fps", [30.0, float(Fraction(30000, 1001)), float(Fraction(24000, 1001))])
def test_plan_matches_actual_check_frames_for_cut_window_and_half_open_elements(fps, monkeypatch):
    cut = {"index": 2, "start": 1, "end": 3}
    elements = [
        model.Element("prior", "am-type", "text", 0, 1, {"punchAt": [fps]}, {}),
        model.Element("inside", "am-type", "text", 1, 3, {"keyframes": [{"frame": 7}]}, {}),
        model.Element("later", "am-type", "text", 3, 5, {"punchAt": [1]}, {}),
        model.Element("voice", "media", "vo", 1, 3, {}, {}, audio=True),
    ]
    times = lint._sample_times(cut, model.in_window(elements, 1, 3), fps)
    expected = list(dict.fromkeys(round(t * fps) for t in times))
    pixels = expected[:1]
    planned = sheet.plan_scene_frames([cut], elements, fps, pixel_frames=pixels)
    assert planned == expected[1:]
    assert round(2 * fps) in expected  # the midpoint is independent of entrances/keys
    assert round((1 + 7 / fps + lint.SETTLE_S) * fps) in expected
    assert all(1 <= t <= 3 - 1 / fps for t in times)
    requested = []
    original = lint._scene_boxes

    def observe(elements, t, rate, shared):
        requested.append(round(t * rate))
        return original(elements, t, rate, shared)

    monkeypatch.setattr(lint, "_scene_boxes", observe)
    lint.composition(cut, model.in_window(elements, 1, 3), fps, shared={"scene_frames": {}})
    assert requested == expected


def test_cap_is_stable_deduplicated_and_counts_only_extra_metadata():
    cuts = [{"index": n + 1, "start": n * 2, "end": n * 2 + 1} for n in range(80)]
    # Repeated cuts do not spend the cap; pixel samples do not spend it either.
    pixels = [15, 75, 135]
    planned = sheet.plan_scene_frames([cuts[0], cuts[0], *cuts[1:]], [], 30, pixel_frames=pixels)
    assert planned == [15 + n * 60 for n in range(3, 63)]
    assert len(planned) == sheet.SCENE_FRAME_BUDGET == 60
    assert sheet.plan_scene_frames([cuts[0]], [], 30, pixel_frames=[15]) == []
    assert sheet.plan_scene_frames([{"start": 0, "end": .01}], [], 30) == []


@pytest.mark.parametrize("fps", [0, -1, True, float("nan"), float("inf")])
def test_invalid_fps_is_rejected(fps):
    with pytest.raises(ValueError, match="fps"):
        sheet.plan_scene_frames([], [], fps)


@pytest.mark.parametrize("frame", [-1, True, 1.5, "2", 2**53])
def test_invalid_pixel_frames_are_rejected(frame):
    with pytest.raises(ValueError, match="safe integers"):
        sheet.plan_scene_frames([], [], 30, pixel_frames=[frame])


@pytest.mark.parametrize("start,end", [(-1, 1), (1, 1), (2, 1), (0, float("nan")), (0, float("inf"))])
def test_invalid_cut_windows_are_rejected(start, end):
    with pytest.raises(ValueError, match="cut window"):
        sheet.plan_scene_frames([{"start": start, "end": end}], [], 30)


def composed_snapshot():
    graph = json.loads((ROOT / "tests/fixtures/timeline/shot_composition.json").read_text())
    graph["occurrences"] = graph["occurrences"][:2]
    revision = next(r for r in graph["shot_revisions"] if r["shot_id"] == "shot-alpha" and r["revision_id"] == "rev-a")
    clips = [{"id": cid, "track": track, "clipType": kind, "at": 0, "hold": 2,
              "params": {"text": cid, "rect": {"x": x, "y": 100, "width": width, "height": 100}}}
             for cid, track, kind, x, width in [
                 ("plate", "plate", "am-snap-plate", 0, 1920),
                 ("lower", "text", "am-type", 1900, 100),
                 ("upper", "front", "am-callout", 1890, 120)]]
    revision["internal_timeline_revision"]["timeline"] = {
        "tracks": [{"id": t, "kind": "visual"} for t in ("front", "text", "plate")], "clips": clips}
    projected = project_shot_composition(graph)
    return {"config": projected.config, "registry": projected.registry, "clips": projected.config["clips"],
            "fps_rational": [30, 1], "duration_frames": 180, "timeline_id": "timeline", "render_run_id": "capture",
            "project_slug": "demo", "video_digest": "sha256:" + "a" * 64, "scripts": []}


class MetadataProvider:
    def __init__(self, query=None):
        self.query = query
        self.reserved = None
        self.pixels = None
        self.scene_frames = {}
        self.scene_occlusions = {}
        self.scene_clip_identities = {}

    def reserve_scene_frames(self, frames):
        assert self.pixels is None, "reservation must precede pixel capture"
        self.reserved = list(frames)

    def capture(self, cards, out_root, resolution):
        self.pixels = [card["frame"] for card in cards]
        if self.query:
            shared = self.query(list(dict.fromkeys(self.pixels + (self.reserved or []))))
            for key, value in shared.items():
                setattr(self, key, value)
        for card in cards:
            path = out_root / card["image"]
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (40, 24)).save(path)
        return {"requested_frames": self.pixels}


def run_pack(tmp_path, monkeypatch, provider, *, layers=("lint",), rules=None, **options):
    snapshot = composed_snapshot()
    options = {"view": "motion", "cut": "1", "preset": "scan", "explicit_interval": True,
               "every_frames": 23, "layers": list(layers), "rules": rules or {}, **options}
    expected = filmstrip_cards.plan_filmstrip(snapshot, options)["cards"]
    contexts = []

    def compose(ctx, _layers, _root, **kwargs):
        contexts.append(ctx)
        result = render_lint(ctx)
        return {"png": [], "findings": result.findings, "layers": list(layers)}

    monkeypatch.setattr(sheet, "compose_motion_sheet", compose)
    monkeypatch.setattr(filmstrip_cards, "_audio_envelope", lambda *args: None)
    result = filmstrip_cards.build_filmstrip_pack(
        out_root=tmp_path / "pack", snapshot=snapshot, options=options, frame_provider=provider)
    assert provider.pixels == [card["frame"] for card in expected]
    assert result["frame_index"]["cards"] == expected
    assert list(contexts[0].frames) == provider.pixels
    return contexts[0]


@pytest.mark.parametrize("layers,rules", [(("strip",), {}), (("lint",), {"disable": ["composition"]})])
def test_no_reservations_when_composition_check_will_not_run(tmp_path, monkeypatch, layers, rules):
    provider = MetadataProvider()
    run_pack(tmp_path, monkeypatch, provider, layers=layers, rules=rules)
    assert provider.reserved is None


def test_selected_cut_does_not_sample_other_cuts_and_keeps_explicit_pixels(tmp_path, monkeypatch):
    provider = MetadataProvider()
    ctx = run_pack(tmp_path, monkeypatch, provider)
    assert provider.reserved == [12, 30]
    assert all(frame < 60 for frame in provider.reserved)  # repeated occurrence starts at frame 120
    assert ctx.cut["start"] == 0 and ctx.cut["end"] == 2


def test_window_reserves_its_exact_samples_instead_of_the_host_cut(tmp_path, monkeypatch):
    provider = MetadataProvider()
    ctx = run_pack(tmp_path, monkeypatch, provider, cut=None, range=(.8, 1.4))
    assert ctx.cut["window"] is True
    assert provider.reserved == [33, 36]
    assert 12 not in provider.reserved and 30 not in provider.reserved


def test_explicit_single_pixel_request_is_unchanged(tmp_path, monkeypatch):
    provider = MetadataProvider()
    run_pack(tmp_path, monkeypatch, provider, cut=None, frame=21, preset="frame")
    assert provider.pixels == [21]
    assert provider.reserved == []  # the check policy has no sample in this one-frame window


def test_nonmotion_capture_does_not_reserve_metadata(tmp_path, monkeypatch):
    provider = MetadataProvider()
    monkeypatch.setattr(filmstrip_cards, "_static", lambda *args, **kwargs: {"png": []})
    filmstrip_cards.build_filmstrip_pack(out_root=tmp_path / "pack", snapshot=composed_snapshot(),
                                       options={"frame": 17}, frame_provider=provider)
    assert provider.pixels == [17] and provider.reserved is None


def test_samples_beyond_cap_remain_unavailable_without_nearest_substitution():
    cut = {"index": 1, "start": 0, "end": 5}
    element = model.Element("keys", "am-type", "text", 0, 5, {"punchAt": list(range(1, 110))}, {})
    frames = sheet.plan_scene_frames([cut], [element], 30)
    requested = {round(t * 30) for t in lint._sample_times(cut, [element], 30)}
    assert len(frames) == 60 and requested - set(frames)
    rows = {str(f): {"frame": f, "width": 1920, "height": 1080, "layers": []} for f in frames}
    found = lint.composition(cut, [element], 30, shared={"scene_frames": rows})
    for frame in requested - set(frames):
        assert any(f.code == "REGION" and f"frame {frame}:" in f.message and "missing" in f.message for f in found)


def test_provider_without_reservation_method_still_reports_missing_facts(tmp_path, monkeypatch):
    provider = MetadataProvider()
    provider.reserve_scene_frames = None
    ctx = run_pack(tmp_path, monkeypatch, provider)
    assert provider.reserved is None
    assert {f["code"] for f in ctx.shared["check_findings"]} >= {"SCENE", "REGION"}


@pytest.fixture(scope="module")
def public_scene_query():
    evaluation = Path(os.environ.get("ASTRID_TEST_SCENE_EVALUATION", str(
        ROOT / "remotion/node_modules/@banodoco/timeline-composition/dist/evaluation.js")))
    assert json.loads((evaluation.parent.parent / "package.json").read_text())["version"] == "0.0.10"
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok, node.problem
    script = """
import {readFileSync} from 'node:fs';
import {prepareScene, querySceneFrame, querySceneOcclusion} from EVALUATION;
const {timeline, frames} = JSON.parse(readFileSync(0, 'utf8'));
const components = Object.fromEntries(timeline.clips.map(clip => [clip.id, {
  identity: clip.id, frame: () => ({presence: 'present', opaqueSupport: 'rect',
    bounds: {status: 'known', rect: clip.params.rect},
    diagnostics: {face: {status: 'known', rect: clip.params.rect},
      text: {bounds: {status: 'known', rect: clip.params.rect}, minPx: 20}}}),
}]));
const tracks = [...timeline.tracks].reverse().map(track => {
  const clips = timeline.clips.filter(clip => clip.track === track.id);
  return {track, clips, transitions: Array(Math.max(0, clips.length - 1)).fill(null)};
});
const scene = prepareScene(tracks, {assets: {}}, 30, 1920, 1080,
  {elements: new Set(timeline.clips.map(clip => clip.clipType)), capabilities: {components},
   roles: Object.fromEntries(timeline.clips.map(clip => [clip.id, 'picture']))});
const rows = frames.map(frame => querySceneFrame(scene, frame));
console.log(JSON.stringify({scene_frames: Object.fromEntries(rows.map(row => [row.frame, row])),
  scene_occlusions: {'0.98': Object.fromEntries(rows.map(row => [row.frame,
    Object.fromEntries(row.layers.map(layer => [layer.clipId, querySceneOcclusion(row, layer.clipId, .98)]))]))},
  scene_clip_identities: Object.fromEntries(timeline.clips.map(clip => [clip.id, {
    clip_id: clip.app.astrid_shot_composition.source_clip_id,
    occurrence_id: clip.app.astrid_shot_composition.occurrence_id}]))}));
""".replace("EVALUATION", json.dumps(evaluation.as_uri()))

    def query(config, frames):
        result = subprocess.run([str(node.path), "--input-type=module", "-e", script], check=True,
                                input=json.dumps({"timeline": config, "frames": frames}),
                                capture_output=True, text=True, timeout=30,
                                env={k: v for k, v in os.environ.items() if k not in ("NODE_OPTIONS", "NODE_PATH")})
        return json.loads(result.stdout)

    return query


@pytest.mark.integration
@pytest.mark.parametrize("missing", [False, True])
def test_reserved_midpoint_reaches_public_cover_and_regions(tmp_path, monkeypatch, public_scene_query, missing):
    config = composed_snapshot()["config"]

    def query(frames):
        assert 30 in frames  # actual midpoint requested before capture
        shared = public_scene_query(config, frames)
        if missing:
            shared["scene_frames"].pop("30")
        return shared

    def private(*args, **kwargs):
        raise AssertionError("captured checks must use public rows")

    monkeypatch.setattr(model, "boxes_at", private)
    provider = MetadataProvider(query)
    ctx = run_pack(tmp_path, monkeypatch, provider)
    assert 30 in provider.reserved and 30 not in provider.pixels
    found = ctx.shared["check_findings"]
    assert {f["code"] for f in found} >= {"COVER", "FRAME", "SMALL", "SAFE"}
    if missing:
        assert {f["code"] for f in found if f["t"] == 1} >= {"SCENE", "REGION"}
        assert all(f["severity"] == "info" for f in found if f["code"] in ("SCENE", "REGION"))
    else:
        assert not any(f["code"] in ("SCENE", "REGION") for f in found)
        assert ctx.shared["scene_frames"] == provider.scene_frames
        assert ctx.shared["scene_clip_identities"] == provider.scene_clip_identities
        assert len({value["occurrence_id"] for value in provider.scene_clip_identities.values()}) == 2


@pytest.mark.integration
def test_real_provider_consumes_reserved_midpoint_and_cached_pixels_stay_unavailable(
    tmp_path, monkeypatch, public_scene_query, public_occlusion,
):
    snapshot = composed_snapshot()
    props = {"timeline": snapshot["config"], "assets": snapshot["registry"],
             "theme": {"visual": {"canvas": {"width": 1920, "height": 1080, "fps": 30}}}}
    queries, renders = [], []

    def query(actual, basis, frames):
        assert actual is props
        queries.append(list(frames))
        return list(public_scene_query(actual["timeline"], frames)["scene_frames"].values())

    def render(frames, output, resolution):
        renders.append(list(frames))
        provider._scene_labels(props, frames)
        result = {}
        for frame in frames:
            path = output / f"{frame}.png"
            Image.new("RGB", (40, 24)).save(path)
            result[frame] = path
        return result

    monkeypatch.setattr(scene_answers, "host_frames_at", query)
    monkeypatch.setattr(composed_frame, "renderer_environment_identity", lambda: "sampling-test")
    provider = composed_frame.RemotionFrameProvider(
        snapshot, timeline_path=tmp_path / "timeline.json", assets_path=tmp_path / "assets.json",
        project_dir=tmp_path, cache=composed_frame.FrameCaptureCache(tmp_path / "cache"), renderer=render)
    reserve, capture = provider.reserve_scene_frames, provider.capture

    def record_reservation(frames):
        provider.reserved = list(frames)
        reserve(frames)

    def record_capture(cards, out_root, resolution):
        provider.pixels = [card["frame"] for card in cards]
        return capture(cards, out_root, resolution)

    monkeypatch.setattr(provider, "reserve_scene_frames", record_reservation)
    monkeypatch.setattr(provider, "capture", record_capture)
    monkeypatch.setattr(model, "boxes_at", lambda *args: pytest.fail("private layout must not run"))
    try:
        ctx = run_pack(tmp_path, monkeypatch, provider)
        assert provider.reserved == [12, 30] and 30 not in provider.pixels
        assert renders == [sorted(provider.pixels)]
        assert queries == [list(dict.fromkeys(sorted(provider.pixels) + [12, 30]))]
        assert set(provider.scene_frames) == {str(frame) for frame in queries[0]}
        assert set(provider.label_batches) == set(queries[0])
        found = ctx.shared["check_findings"]
        assert {f["code"] for f in found} >= {"COVER", "FRAME", "SMALL", "SAFE"}
        assert not any(f["code"] in ("SCENE", "REGION") for f in found)
        cached = run_pack(tmp_path, monkeypatch, provider)
        assert len(queries) == len(renders) == 1
        assert provider.scene_frames == {} and "cached" in provider.scene_unavailable
        assert {f["code"] for f in cached.shared["check_findings"]} >= {"SCENE", "REGION"}
    finally:
        provider.close()
