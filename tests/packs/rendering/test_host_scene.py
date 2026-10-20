"""Native host preparation with the locked install, real maps and renderer aliases.

Status is replaced here; this is not live launch-admission or pixel evidence.
"""
import copy
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from astrid.core.element.registry import ElementRegistry
from astrid.core.element.schema import ElementDefinition
from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.rendering.remotion_runtime import RemotionRuntimeStatus
from astrid.core.theme import builtin_theme
from astrid.core.timeline import scene_answers
from astrid.packs.rendering.actions.timeline_visualize.overlays import labels
from scripts import gen_effect_registry

ROOT = Path(__file__).resolve().parents[3]
REMOTION = ROOT / "remotion"

# Test elements fill exactly the rectangle they declare. This is component
# support, not evidence about media alpha or undeclared AM pack internals.
LABEL_COMPONENT = """
import {createElement} from 'react';
import {useVideoConfig} from 'remotion';

const layout = (clip, width, height) => clip.clipType === 'test-field'
  ? {x: 0, y: 0, width, height}
  : {x: clip.x, y: clip.y, width: clip.width, height: clip.height};
const unknownBounds = 'Test component does not declare evaluated bounds';

export default Object.assign(({clip}) => {
  const {width, height} = useVideoConfig();
  const rect = layout(clip, width, height);
  return createElement('div', {style: {position: 'absolute', left: rect.x,
    top: rect.y, width: rect.width, height: rect.height, background: '#123456'}});
}, {
  prepareSceneCapability: ({clip, width, height}) => {
    const rect = layout(clip, width, height);
    if (clip.clipType === 'test-unknown-bounds') {
      return {identity: JSON.stringify(rect), frame: () => ({presence: 'present',
        opaqueSupport: 'none', bounds: {status: 'unknown', reason: unknownBounds}})};
    }
    return {identity: JSON.stringify(rect), frame: () => ({presence: 'present',
      opaqueSupport: 'rect', bounds: {status: 'known', rect}})};
  },
});
"""


@pytest.fixture(scope="module")
def host_project(tmp_path_factory):
    project_root = tmp_path_factory.mktemp("native-host")
    project = project_root / "remotion"
    (project / "src").mkdir(parents=True)
    (project_root / "astrid").symlink_to(ROOT / "astrid", target_is_directory=True)
    assert (REMOTION / "node_modules/esbuild").is_dir(), "requires this worktree's locked npm ci"
    (project / "node_modules").symlink_to(REMOTION / "node_modules", target_is_directory=True)
    for name in ("scene-query.mjs", "native-scene.mjs", "webpack-alias.mjs", "package.json"):
        shutil.copyfile(REMOTION / name, project / name)
    for name in ("host-scene.ts", "host-registries.ts"):
        shutil.copyfile(REMOTION / "src" / name, project / "src" / name)
    pack = project_root / "probe"
    elements = list(gen_effect_registry._element_registry().list())
    rendering = {}
    for kind, element_id in (("effects", "custom"), ("effects", "test-card"), ("effects", "test-field"),
                             ("effects", "test-unknown-bounds"),
                             ("animations", "fade-up"), ("transitions", "fade")):
        element = pack / kind / element_id
        element.mkdir(parents=True)
        source = LABEL_COMPONENT if element_id.startswith("test-") else (REMOTION / "tests" / f"custom-{kind}.tsx").read_text()
        if element_id == "custom":
            source = "import {probeWidth} from 'probe-dependency';\n" + source.replace("width: 1920", "width: probeWidth")
        (element / "component.tsx").write_text(source)
        (element / "element.yaml").write_text(f"id: {element_id}\nkind: {kind[:-1]}\n")
        rendering[f"{kind}/{element_id}"] = {"type": "element", "path": f"{kind}/{element_id}/element.yaml"}
        elements.append(ElementDefinition(
            id=element_id, kind=kind, root=element, source="pack:probe", editable=True,
            priority=100, component=element / "component.tsx", schema={}, defaults={"durationFrames": 8},
            metadata={"pack_id": "probe", "kind": "wrapper", "phase": ["entrance", "exit"],
                      **({"clipTypeAliases": ["custom-alias"]} if element_id == "custom" else {})}))
    (pack / "pack.json").write_text(json.dumps({"id": "probe", "rendering": rendering}))
    dependency = pack / "node_modules/probe-dependency"
    dependency.mkdir(parents=True)
    (dependency / "package.json").write_text('{"type":"module","exports":"./index.js"}')
    (dependency / "index.js").write_text('export const probeWidth = 1920;')
    registry = ElementRegistry(elements)
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(gen_effect_registry, "_element_registry", lambda: registry)
        for kind in ("effects", "animations", "transitions"):
            (project / "src" / f"{kind}.generated.ts").write_text(gen_effect_registry.generate_element_registry(kind))
    package = REMOTION / "node_modules/@banodoco/timeline-composition"
    assert json.loads((package / "package.json").read_text())["version"] == "0.0.8"
    assert hashlib.sha256((REMOTION / "artifacts/banodoco-timeline-composition-0.0.8.tgz").read_bytes()).hexdigest() == (
        "93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa")
    def hashes():
        return {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in package.rglob("*") if p.is_file()}
    before = hashes()
    assert len(before) == 77
    yield project, pack
    assert hashes() == before


@pytest.fixture
def native_host(host_project, monkeypatch):
    project, pack = host_project
    toolchain = resolve_pinned_node(REMOTION, override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert toolchain.ok and toolchain.version == "v20.19.4"
    for key in ("NODE_OPTIONS", "NODE_PATH", "PYTHONPYCACHEPREFIX"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("ASTRID_PACKS_PATH", str(pack))
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        RemotionRuntimeStatus(True, project, node_executable=toolchain.path))
    return project


@pytest.fixture(name="native_label_inputs")
def capture_label_inputs(native_host):
    def capture(config, frames, fps, canvas):
        config = copy.deepcopy(config)
        for clip in config["clips"]:
            clip["elementRef"] = {"kind": "effect", "id": clip["clipType"], "packId": "probe"}
        theme = builtin_theme()
        theme["visual"]["canvas"] = {**canvas, "fps": fps}
        config["theme"] = theme["id"]
        snapshot = {"config": config, "registry": {"assets": {}}, "theme": theme,
                    "fps_rational": float(fps).as_integer_ratio(), "clips": [], "occurrences": [], "metadata": {}}
        original = copy.deepcopy(snapshot)
        batches = labels.snapshot_labels(snapshot, frames)
        assert all(item.status == "known" for layers in batches.values() for item in layers)
        assert snapshot == original
        return snapshot, batches
    return capture


def props(clips=None, *, theme=None, assets=None):
    return {"timeline": {"theme": "stale-config-slug", "tracks": [{"id": "plate", "kind": "visual"}],
                         "clips": clips or []},
            "assets": assets if assets is not None else {"assets": {}},
            "theme": theme if theme is not None else builtin_theme()}


BASIS = {"width": 1920, "height": 1080, "fps": 30}


def test_native_host_default_custom_alias_capability_and_immutable_props(native_host):
    p = props([{"id": "first", "track": "plate", "clipType": "custom-alias", "at": 0, "hold": 1,
                "params": {"nested": [1, None, "preserve"]}}])
    original = copy.deepcopy(p)
    first, end = scene_answers.host_frames_at(p, BASIS, [0, 30])
    assert first["coverage"] == "COVERED"
    assert first["layers"][0]["bounds"] == {"status": "known", "rect": {"x": 0, "y": 0, "width": 1920, "height": 1080}}
    assert first["layers"][0]["opacity"] == 1
    assert end["coverage"] == "GAP" and end["layers"] == []
    assert p == original
    p["timeline"]["clips"][0]["elementRef"] = {"kind": "effect", "id": "custom", "packId": "probe"}
    assert scene_answers.host_frames_at(p, BASIS, [0])[0]["coverage"] == "COVERED"
    p["timeline"]["clips"][0]["elementRef"]["packId"] = "missing"
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="Unknown effect owner"):
        scene_answers.host_frames_at(p, BASIS, [0])


def test_native_host_uses_exact_assets_and_runtime_theme(native_host):
    clip = {"id": "media", "track": "plate", "clipType": "image", "asset": "P", "at": 0, "hold": 1}
    basis = {"width": 200, "height": 100, "fps": 30000 / 1001}
    p = props([clip], assets={"assets": {"P": {"file": "p.png", "type": "image", "resolution": "100x200"}}})
    answer = scene_answers.host_frames_at(p, basis, [0])[0]
    assert answer["layers"][0]["bounds"]["rect"] == {"x": 75, "y": 0, "width": 50, "height": 100}
    assert answer["coverage"] == "UNKNOWN" and answer["layers"][0]["opacity"] is None
    p["assets"] = {"assets": {}}
    assert scene_answers.host_frames_at(p, basis, [0])[0]["layers"][0]["bounds"]["status"] == "unknown"
    p = props([{**clip, "clipType": "art-card"}])
    answer = scene_answers.host_frames_at(p, basis, [0])[0]
    assert answer["coverage"] == "UNKNOWN"
    # Admission is distinct from alpha: art-card intentionally has no declared
    # bounds capability. Inspect the prepared host set, never invent geometry.
    script = """
import {loadHostScene} from './native-scene.mjs';
import {DEFAULT_THEME} from '@banodoco/timeline-composition';
const prepare = await loadHostScene(process.cwd());
console.log(JSON.stringify(['banodoco-default', '2rp'].map(id =>
  prepare({timeline: {theme: 'stale', clips: [], tracks: []}, assets: {assets: {}},
    theme: {...DEFAULT_THEME, id}}, {width: 200, height: 100, fps: 30}, {}).elements.has('art-card'))));
"""
    result = subprocess.run([str(scene_answers.remotion_runtime_status().node_executable), "--input-type=module", "-e", script],
                            cwd=native_host, check=True, text=True, capture_output=True, timeout=30)
    assert json.loads(result.stdout) == [False, True]



@pytest.mark.parametrize("align", ["start", "center", "end"])
def test_native_host_resolves_custom_transition_defaults_and_boundaries(native_host, align):
    clips = [{"id": "first", "track": "plate", "clipType": "custom", "at": 0, "hold": 1,
              "transition": {"id": "fade", "align": align}},
             {"id": "next", "track": "plate", "clipType": "custom", "at": 1, "hold": 1}]
    answers = scene_answers.host_frames_at(props(clips), BASIS, [21, 22, 26, 29, 30, 33, 34, 37, 38, 59, 60])
    assert answers[-1]["layers"] == []
    incoming_start = {"end": 22, "center": 26, "start": 30}[align]
    active = [a["frame"] for a in answers if any(layer["clipId"] == "next" for layer in a["layers"])]
    assert min(active) == incoming_start
    if align == "end":
        incoming = next(layer for layer in answers[1]["layers"] if layer["clipId"] == "next")
        assert incoming["drawLocalFrame"] == incoming["ownFrame"] == 0
    clips[0]["transition"] = "not-admitted"
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="Unknown transition"):
        scene_answers.host_frames_at(props(clips), BASIS, [0])


def test_native_labels_known_unknown_unavailable_and_single_batch(native_host, monkeypatch):
    p = props([{"id": "native:card", "clipType": "custom", "track": "plate", "at": 0, "hold": 1}])
    calls = []
    run = scene_answers.subprocess.run
    def capture(*args, **kwargs):
        calls.append(json.loads(kwargs["input"])["frames"])
        return run(*args, **kwargs)
    monkeypatch.setattr(scene_answers.subprocess, "run", capture)
    batch = labels.labels_batch(p["timeline"], [0, 1, 30, 0], 30, BASIS,
                                assets=p["assets"], theme=p["theme"])
    assert calls == [[0, 1, 30]]
    assert batch[0][0].status == "known" and batch[0][0].opacity == 1
    assert batch[30] == []
    p["timeline"]["clips"][0]["clipType"] = "browser-only-unknown"
    unknown = labels.labels_for(p["timeline"], 0, 30, BASIS, assets=p["assets"], theme=p["theme"])[0]
    assert unknown.status == "unknown" and unknown.opacity is None and unknown.bounds is None
    unavailable = labels.labels_for(p["timeline"], 0, 30, BASIS)[0]
    assert unavailable.status == "unavailable" and "resolved runtime theme" in unavailable.message
    from PIL import Image
    image = labels.draw_labels(Image.new("RGB", (200, 100)), [unknown, unavailable], canvas=BASIS, tile_size=(200, 100))
    assert image.getbbox() is not None


def test_native_labels_preserve_unknown_bounds_and_public_finding(native_host):
    p = props([{"id": "native:unknown-bounds", "clipType": "test-unknown-bounds",
                "track": "plate", "at": 0, "hold": 1}])
    answer = scene_answers.host_frames_at(p, BASIS, [0])[0]
    layer = answer["layers"][0]
    assert layer["visible"] is True
    assert layer["opaqueSupport"] == "none"
    assert layer["bounds"]["status"] == "unknown"
    assert layer["coverage"] == "unknown"
    assert layer["findings"] == [{
        "code": "unknown-component-bounds",
        "clipId": "native:unknown-bounds",
        "reason": "Test component does not declare evaluated bounds",
    }]

    projected = labels.labels_for(p["timeline"], 0, 30, BASIS, assets=p["assets"], theme=p["theme"])[0]
    assert projected.status == "unknown"
    assert projected.message == "Test component does not declare evaluated bounds"

    from astrid.packs.rendering.actions.timeline_visualize.filmstrip_cards import (
        attach_frame_addresses,
    )

    receipt = {"cards": [{}]}
    attach_frame_addresses(receipt, {"config": p["timeline"], "registry": p["assets"],
                                    "theme": p["theme"], "fps_rational": [30, 1]}, [{"frame": 0}])
    assert receipt["cards"] == [{
        "addresses": ["unknown-bounds"],
        "scene_status": "unknown",
        "scene_findings": ["Test component does not declare evaluated bounds"],
    }]


def test_check_scene_is_advisory_and_missing_basis_is_explicit(native_host, monkeypatch):
    from astrid.sdk.timeline_checkout import Checkout
    fixture = ROOT / "tests/fixtures/timeline_editing/tiny_publishable.json"
    candidate = json.loads(fixture.read_text())
    checkout = Checkout(candidate)
    plain = checkout.check()
    assert plain.valid and any("UNAVAILABLE" in line for line in plain.problems)
    empty = checkout.check(render_props=props(), frame_basis={**BASIS, "fps": checkout.fps})
    assert empty.valid and not any("picture" in line for line in empty.blocking)
    assert any("GAP" in line for line in empty.problems)
    unknown = checkout.check(render_props=props([{"id": "c", "track": "plate", "clipType": "browser-only", "at": 0, "hold": 1}]),
                             frame_basis={**BASIS, "fps": checkout.fps})
    assert unknown.valid and any("UNKNOWN" in line for line in unknown.problems)
    # Role declarations are test metadata only; support/coverage still come
    # from the registered native capability and the real public query.
    from astrid.core.timeline import scene_roles

    with monkeypatch.context() as patch:
        patch.setattr(scene_roles, "element_coverage", lambda ids: {"custom": {"coverage": "background"}})
        background = checkout.check(render_props=props([
            {"id": "background", "track": "plate", "clipType": "custom", "at": 0, "hold": 1}]),
            frame_basis={**BASIS, "fps": checkout.fps})
    assert background.valid and any("EMPTY" in line for line in background.problems)
    assert not any("EMPTY" in line for line in background.blocking)
    dipping = checkout.check(render_props=props([
        {"id": "out", "track": "plate", "clipType": "custom", "at": 0, "hold": 1, "transition": "fade"},
        {"id": "in", "track": "plate", "clipType": "custom", "at": 1, "hold": 1}]),
        frame_basis={**BASIS, "fps": checkout.fps})
    assert dipping.valid and any("DIP" in line for line in dipping.problems)
    broken = copy.deepcopy(candidate)
    broken["shots"]["A"]["internal_timeline"]["clips"][1]["params"]["scale"] = "not-a-number"
    assert not Checkout(broken).check().valid


def test_frozen_label_callers_retain_assets_theme_and_batch(native_host, tmp_path, monkeypatch):
    from PIL import Image

    from astrid.packs.rendering.actions.timeline_visualize.fast_lane import _labelled_tiles
    from astrid.packs.rendering.actions.timeline_visualize.filmstrip_cards import (
        _contact_overlay_for_layers,
        attach_frame_addresses,
    )
    from astrid.packs.rendering.actions.timeline_visualize.motion.sheet import build_context

    p = props([{"id": "native:card", "track": "plate", "clipType": "custom-alias", "at": 0, "hold": 1}])
    snapshot = {"config": p["timeline"], "registry": p["assets"], "theme": p["theme"], "fps_rational": [30, 1],
                "clips": [], "occurrences": [], "metadata": {"parent_revision_id": "frozen-rev"}}
    original = copy.deepcopy(snapshot)
    requests = []
    run = scene_answers.subprocess.run
    def capture(*args, **kwargs):
        requests.append(json.loads(kwargs["input"]))
        return run(*args, **kwargs)
    monkeypatch.setattr(scene_answers.subprocess, "run", capture)
    receipt = {"cards": [{}, {}]}
    attach_frame_addresses(receipt, snapshot, [{"frame": 0}, {"frame": 30}])
    assert receipt["cards"] == [
        {"addresses": ["card"], "scene_status": "known", "scene_findings": []},
        {"addresses": [], "scene_status": "known", "scene_findings": []}]
    overlay = _contact_overlay_for_layers(snapshot, ["labels"], 30, frames=[0, 1])
    source = Image.new("RGB", (200, 100))
    overlay(source, 0)
    overlay(source, 1 / 30)
    source_path = tmp_path / "source.png"
    source.save(source_path)
    source_bytes = source_path.read_bytes()
    ctx = build_context(snapshot, {"index": 1, "start": 0, "end": 1, "duration": 1, "clip_id": "card"},
                        {0: source_path, 1: source_path}, fps=30, frame_size=(200, 100), layer_names=["labels"])
    _labelled_tiles({"working": snapshot}, 0, 30, {"working": source_path}, tmp_path, 0,
                    label_batches={"working": ctx.shared["label_batches"]})
    assert [request["frames"] for request in requests] == [[0, 30], [0, 1], [0, 1]]
    assert all(request["props"] == p for request in requests)
    assert source_path.read_bytes() == source_bytes
    assert snapshot == original
    # This existing snapshot contract has no resolved theme; no fetch or Node.
    legacy = {key: value for key, value in snapshot.items() if key != "theme"}
    attach_frame_addresses(receipt, legacy, [{"frame": 0}, {"frame": 30}])
    assert len(requests) == 3
    assert all(row["scene_status"] == "unavailable" for row in receipt["cards"])
    assert all("resolved runtime theme" in row["scene_findings"][0] for row in receipt["cards"])


@pytest.mark.parametrize("entry", ["native-scene.mjs", "src/host-scene.ts"])
def test_native_host_entry_cannot_escape_selected_project(native_host, tmp_path, entry):
    target = native_host / entry
    original = target.read_bytes()
    outside = tmp_path / target.name
    outside.write_bytes(original)
    target.unlink()
    try:
        target.symlink_to(outside)
        with pytest.raises(scene_answers.SceneQueryUnavailable):
            scene_answers.host_frames_at(props(), BASIS, [0])
    finally:
        target.unlink()
        target.write_bytes(original)


def test_root_render_tail_stays_explicitly_unsupported(native_host):
    p = props()
    p["timeline"]["app"] = {"astrid_render_clock": {"tail": {"source_asset": "tail"}}}
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="RenderClockTail"):
        scene_answers.host_frames_at(p, BASIS, [0])



def test_large_native_batch_is_not_truncated(native_host):
    p = props([{"id": "first", "track": "plate", "clipType": "custom-alias", "at": 0, "hold": 10}])
    frames = list(range(300))
    answers = scene_answers.host_frames_at(p, BASIS, frames)
    assert [answer["frame"] for answer in answers] == frames
    assert all(answer["coverage"] == "COVERED" for answer in answers)
    spans = scene_answers.spans_from_frames(answers)
    assert [(s.start_frame, s.end_frame, s.cls) for s in spans] == [(0, 300, "COVERED")]


def test_label_canvas_comes_from_actual_runtime_theme(native_host):
    from PIL import Image

    from astrid.packs.rendering.actions.timeline_visualize.filmstrip_cards import (
        _contact_overlay_for_layers,
    )

    p = props([{"id": "media", "track": "plate", "clipType": "image", "asset": "P", "at": 0, "hold": 1}],
              assets={"assets": {"P": {"file": "p.png", "type": "image", "resolution": "100x200"}}})
    p["timeline"]["tracks"][0]["fit"] = "contain"
    p["theme"]["visual"]["canvas"] = {"width": 200, "height": 100, "fps": 30}
    snapshot = {"config": p["timeline"], "registry": p["assets"], "theme": p["theme"], "fps_rational": [30, 1]}
    overlay = _contact_overlay_for_layers(snapshot, ["labels"], 30, frames=[0])
    result = overlay(Image.new("RGB", (200, 100)), 0)
    assert result.getpixel((75, 50)) == (56, 189, 248)
    assert result.getpixel((20, 50)) == (0, 0, 0)



def test_native_host_rational_frame_clock_is_half_open(native_host):
    fps = 30000 / 1001
    clip = {"id": "immutable:clip", "track": "plate", "clipType": "custom-alias", "at": 1001 / 30000,
            "hold": 2002 / 30000, "opaqueExtension": {"preserved": [None, 2]}}
    p = props([clip])
    before = copy.deepcopy(p)
    answers = scene_answers.host_frames_at(p, {**BASIS, "fps": fps}, [0, 1, 2, 3, 1])
    assert [[layer["clipId"] for layer in answer["layers"]] for answer in answers] == [
        [], ["immutable:clip"], ["immutable:clip"], [], ["immutable:clip"]]
    assert p == before


def test_capture_context_carries_exact_props_to_native_labels(native_host, tmp_path, monkeypatch):
    from PIL import Image

    from astrid.packs.rendering.actions.timeline_visualize import composed_frame
    from astrid.packs.rendering.actions.timeline_visualize.filmstrip_cards import (
        attach_frame_addresses,
    )
    from astrid.packs.rendering.rendering.renderers.remotion import run as renderer

    p = props([{"id": "frozen:card", "clipType": "custom-alias", "track": "plate", "at": 0, "hold": 1,
                "app": {"cut": "frozen-cut", "layer": "card"}}])
    snapshot = {"config": p["timeline"], "registry": p["assets"], "fps_rational": [30, 1],
                "metadata": {"canonical_timeline": {"parent_revision_id": "frozen-revision"}}}
    original = copy.deepcopy(snapshot)
    # The browser/capture boundary is a unit seam; the supplied props run
    # through the real native host preparation and query, without a socket.
    def capture(timeline, assets, output, frames, **kwargs):
        kwargs["on_scene_props"](p, frames)
        result = {}
        for frame in frames:
            path = Path(output) / f"frame-{frame:06d}.png"
            Image.new("RGB", (200, 100)).save(path)
            result[frame] = path
        return result

    monkeypatch.setattr(renderer, "capture_remotion_frames", capture)
    monkeypatch.setattr(composed_frame, "_SHARED_REMOTION_OWNER", None)
    monkeypatch.setattr(composed_frame, "renderer_environment_identity", lambda: "test-renderer-closure")
    provider = composed_frame.RemotionFrameProvider(
        snapshot, timeline_path=tmp_path / "timeline.json", assets_path=tmp_path / "assets.json", project_dir=native_host,
        cache=composed_frame.FrameCaptureCache(tmp_path / "cache"), scene_labels=True)
    cards = [{"frame": 0, "image": "frame-0.png"}, {"frame": 1, "image": "frame-1.png"}]
    try:
        info = provider.capture(cards, tmp_path / "pack")
        assert info["fresh_frames"] == 2
        assert all(provider.label_batches[frame][0].status == "known" for frame in (0, 1))
        receipt = {"cards": [{}, {}]}
        attach_frame_addresses(receipt, snapshot, cards, label_batches=provider.label_batches)
        assert all(row["addresses"] == ["frozen-cut.card"] and row["scene_status"] == "known" for row in receipt["cards"])
        assert snapshot == original and "theme" not in snapshot
        # Cached pixels do not establish the resolved props of the original
        # render; do not retain a previous call's answers as current evidence.
        cached = provider.capture(cards, tmp_path / "pack")
        assert cached["cached_frames"] == 2 and provider.label_batches == {}
        attach_frame_addresses(receipt, snapshot, cards, label_batches=provider.label_batches)
        assert all(row["scene_status"] == "unavailable" for row in receipt["cards"])
    finally:
        provider.close()


def test_check_scene_source_identity_is_separate_from_candidate(native_host):
    from astrid.sdk.timeline_checkout import Checkout

    candidate = json.loads((ROOT / "tests/fixtures/timeline_editing/tiny_publishable.json").read_text())
    p = props()
    p["timeline"]["metadata"] = {"parent_revision_id": "actual-frozen-source"}
    report = Checkout(candidate).check(render_props=p, frame_basis=BASIS)
    assert any("revision actual-frozen-source" in line for line in report.problems)
    assert not any("revision rev-0" in line for line in report.problems)


def test_actual_renderer_props_observer_matches_serialized_root_props(native_host, tmp_path, monkeypatch):
    from astrid.core.rendering.remotion_runtime import RemotionRuntimeTools
    from astrid.packs.rendering.rendering.renderers.remotion import run as renderer

    timeline = tmp_path / "timeline.json"
    assets = tmp_path / "assets.json"
    runtime_theme = tmp_path / "theme.json"
    config = {"theme": "historical-unused-slug", "tracks": [{"id": "plate", "kind": "visual", "label": "Picture"}], "clips": [],
              "theme_overrides": {"visual": {"canvas": {"width": 200, "height": 100, "fps": 30000 / 1001}}}}
    timeline.write_text(json.dumps(config))
    assets.write_text('{"assets":{}}')
    theme = builtin_theme()
    theme["id"] = "actual-runtime-theme"
    runtime_theme.write_text(json.dumps(theme))
    node = scene_answers.remotion_runtime_status().node_executable
    tools = RemotionRuntimeTools(node, "v20.19.4", native_host / "node_modules/@remotion/cli/remotion-cli.js")
    # Admission is a separate gate. Keep real serialization, materialization,
    # theme resolution and effect staging; stop before native/browser allocation.
    monkeypatch.setattr(renderer, "_validate_project_dir", lambda project: tools)
    monkeypatch.setattr(renderer, "_regenerate_element_registries", lambda *args: None)
    monkeypatch.setattr(renderer, "_validate_renderer_effect_registry", lambda *args: None)
    monkeypatch.setattr(renderer, "_effective_registry_state", lambda *args: {"hash": "test-registry"})
    monkeypatch.setattr(renderer, "_available_remotion_port", lambda: 32101)
    observed = []
    class Prepared(Exception):
        pass
    def observe(props, frames):
        assert props == json.loads((tmp_path / ".remotion-props.json").read_text())
        assert props["theme"]["id"] == "actual-runtime-theme"
        assert props["timeline"]["theme"] == "historical-unused-slug"
        assert props["theme"]["visual"]["canvas"] == config["theme_overrides"]["visual"]["canvas"]
        observed.extend(scene_answers.host_frames_at(props, {"width": 200, "height": 100, "fps": 30000 / 1001}, frames))
        raise Prepared()
    with pytest.raises(Prepared):
        renderer._execute_remotion_locked(timeline, assets, tmp_path / "unused.mp4", provenance_out_path=tmp_path / "unused.mp4",
                                          project_dir=native_host, composition_id="TimelineComposition", theme_path=runtime_theme,
                                          min_free_gb=None, frame_numbers=[29, 30], frame_output_dir=tmp_path / "frames",
                                          on_scene_props=observe)
    assert [answer["frame"] for answer in observed] == [29, 30]
    assert all(answer["coverage"] == "GAP" for answer in observed)
    assert not (tmp_path / ".remotion-props.json").exists()
