"""Composition region policy over actual prepared public scene answers."""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.timeline.cuts import occurrences_from_snapshot
from astrid.core.timeline.shot_composition_projection import project_shot_composition
from astrid.packs.rendering.actions.timeline_visualize.motion import lint, model
from tests.packs.rendering.test_scene_query_occlusion import admitted_public_artifact

ROOT = Path(__file__).resolve().parents[3]
CUT = {"index": 1, "start": 0, "end": 1}


def rect(x=300, y=300, width=100, height=100):
    return {"x": x, "y": y, "width": width, "height": height}


def clip(clip_id, kind="am-type", *, bounds=None, **params):
    return {"id": clip_id, "track": clip_id, "clipType": kind, "at": 0, "hold": 1,
            "params": {"text": clip_id, "rect": bounds or rect(), **params}}


def timeline(clips):
    return {"tracks": [{"id": c["track"], "kind": "visual"} for c in reversed(clips)], "clips": clips}


def elements(config):
    return model.elements_from_occurrences(occurrences_from_snapshot(config))


def messages(found, code):
    return [f.message for f in found if f.code == code]


@pytest.fixture(scope="module")
def public_diagnostics(tmp_path_factory):
    artifact, _version = admitted_public_artifact("ASTRID_COMPOSITION_TEST_ARTIFACT")
    peers = Path(os.environ.get("ASTRID_COMPOSITION_TEST_NODE_MODULES", str(ROOT / "remotion/node_modules"))).resolve()
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok, node.problem
    assert artifact.is_file(), "requires an admitted Composition artifact with component diagnostics"
    assert peers.is_dir(), "requires the qualified locked peer graph"
    project = tmp_path_factory.mktemp("motion-diagnostics-public")
    modules = project / "node_modules"
    package = modules / "@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(artifact) as archive:
        archive.extractall(project, filter="data")
    (project / "package").rename(package)
    for peer in peers.iterdir():
        if peer.name != "@banodoco":
            (modules / peer.name).symlink_to(peer, target_is_directory=peer.is_dir())
    shutil.copyfile(Path(__file__).with_name("motion_diagnostics_public.mjs"), project / "query.mjs")
    env = {k: v for k, v in os.environ.items() if k not in ("NODE_OPTIONS", "NODE_PATH")}
    before = {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in package.rglob("*") if p.is_file()}
    assert len(before) == 77
    # Verify actual resolution from the fresh consumer, without using App peers.
    preflight = """
      import {createRequire} from 'node:module';
      import {realpathSync} from 'node:fs';
      import {fileURLToPath} from 'node:url';
      const require = createRequire(import.meta.url);
      console.log(JSON.stringify(Object.fromEntries(['react', 'react-dom', 'remotion',
        '@remotion/media', '@remotion/renderer', '@remotion/layout-utils'].map(name =>
          [name, {path: realpathSync(fileURLToPath(import.meta.resolve(name))), version: require(`${name}/package.json`).version}]))));
    """
    resolved = json.loads(subprocess.check_output([str(node.path), "--input-type=module", "-e", preflight],
                                                cwd=project, env=env, text=True, timeout=30))
    for name, peer in resolved.items():
        assert Path(peer["path"]).is_relative_to(peers)
        assert peer["version"] == ("18.3.1" if name in ("react", "react-dom") else "4.0.509")

    def query(config, frames=(12, 15), *, width=1920, height=1080):
        return json.loads(subprocess.check_output([str(node.path), "query.mjs"], cwd=project, env=env,
            text=True, input=json.dumps({"timeline": config, "frames": frames, "width": width, "height": height}), timeout=30))

    try:
        yield query
        assert {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in package.rglob("*") if p.is_file()} == before
    finally:
        shutil.rmtree(project)


@pytest.fixture
def no_private_boxes(monkeypatch):
    def forbidden(*args):
        raise AssertionError("public composition diagnostics must not evaluate private boxes/layout")

    monkeypatch.setattr(model, "boxes_at", forbidden)
    monkeypatch.setattr(model, "face_box", forbidden)
    monkeypatch.setattr(model, "declared_face", forbidden)
    monkeypatch.setattr(model, "_wrap_lines", forbidden)
    monkeypatch.setattr(model, "props_at", forbidden)


@pytest.mark.integration
class TestPublicDiagnostics:
    def test_frame_safe_small_and_edge_positive_equivalents(self, public_diagnostics, no_private_boxes):
        config = timeline([
            clip("card", "am-callout", bounds=rect(1260, 100, 720, 200),
                 textRect=rect(1280, 120, 680, 160), fontPx=24),
            clip("type", bounds=rect(1760, 500, 200, 60), textRect=rect(1760, 500, 200, 60), fontPx=20),
            clip("sprite", "am-sprite", bounds=rect(-12, 500)),
        ])
        shared = public_diagnostics(config)
        found = lint.composition(CUT, elements(config), 30, shared=shared)
        assert any('am-callout "card" is cut off: 60 px' in m for m in messages(found, "FRAME"))
        assert any('am-type "type" is cut off: 40 px' in m for m in messages(found, "FRAME"))
        assert any('am-type "type" is 136 px outside title-safe (right)' in m for m in messages(found, "SAFE"))
        assert any('body text 24 px < 32 px at 1080p' in m for m in messages(found, "SMALL"))
        assert any('text 20 px < 32 px at 1080p' in m for m in messages(found, "SMALL"))
        assert any('runs 12 px past the left edge' in m for m in messages(found, "EDGE"))
        assert all(f.fix is None for f in found)

    def test_face_and_declared_footage_face_equivalents(self, public_diagnostics, no_private_boxes):
        for kind in ("am-presenter", "am-footage"):
            config = timeline([clip("presenter", kind, bounds=rect(0, 0, 1920, 1080),
                                    face=rect(700, 110, 500, 610), mouth=rect(800, 500, 100, 50)),
                               clip("claw", "am-sprite", bounds=rect(780, 240, 522, 840)),
                               clip("side", "am-callout", bounds=rect(1300, 160, 400, 200))])
            shared = public_diagnostics(config)
            found = lint.composition(CUT, elements(config), 30, shared=shared)
            face = messages(found, "FACE")
            assert len(face) == 1 and 'am-sprite "claw" covers 66% of the presenter face' in face[0]
            layer = next(layer for layer in shared["scene_frames"]["12"]["layers"] if layer["clipId"] == "presenter")
            assert layer["diagnostics"]["mouth"]["rect"] == rect(800, 500, 100, 50)
            assert layer["diagnostics"]["motion"] == {"position": 12}

    def test_tracked_face_observation_provenance(self, public_diagnostics, no_private_boxes):
        config = timeline([clip("presenter", "am-presenter", bounds=rect(0, 0, 1920, 1080), face=rect(100, 100)),
                           clip("card", "am-callout", bounds=rect(300, 300, 400, 100))])
        tracks = [SimpleNamespace(name="face", kind="boxes", clip_id="footage",
                                  boxes_at=lambda t: [(300, 300, 700, 700)])]
        found = lint.composition(CUT, elements(config), 30, shared=public_diagnostics(config), tracks=tracks)
        assert len(messages(found, "FACE")) == 1
        assert "25% of the tracked face" in messages(found, "FACE")[0]

    def test_actual_canvas_and_1080p_text_policy(self, public_diagnostics, no_private_boxes):
        config = timeline([clip("type", bounds=rect(950, 100, 30, 40),
                                textRect=rect(950, 100, 30, 40), fontPx=20),
                           clip("sprite", "am-sprite", bounds=rect(950, 300, 30, 40))])
        shared = public_diagnostics(config, width=960, height=540)
        found = lint.composition(CUT, elements(config), 30, shared=shared)
        assert any("20 px past the frame edge" in m for m in messages(found, "FRAME"))
        assert any("68 px outside title-safe (right)" in m for m in messages(found, "SAFE"))
        assert any("20 px past the right edge" in m for m in messages(found, "EDGE"))
        assert not messages(found, "SMALL")  # 20 canvas px = 40 px at 1080p
        assert messages(lint.composition(CUT, elements(config), 30, shared=shared, min_text_px=41), "SMALL")

    def test_face_uses_output_while_safe_uses_declared_text_region(self, public_diagnostics, no_private_boxes):
        config = timeline([
            clip("presenter", "am-presenter", bounds=rect(0, 0, 1920, 1080), face=rect(100, 100)),
            clip("panel", "test-panel", bounds=rect(100, 100, 500, 100),
                 textRect=rect(400, 100), fontPx=40),
        ])
        found = lint.composition(CUT, elements(config), 30, shared=public_diagnostics(config))
        assert any('test-panel "panel" covers 100% of the presenter face' in m for m in messages(found, "FACE"))
        assert not messages(found, "FRAME")
        assert not messages(found, "SAFE")

    def test_half_open_and_component_content_clock(self, public_diagnostics, no_private_boxes, monkeypatch):
        moving = clip("moving", bounds=rect(1760, 100, 100, 100),
                      textRect=rect(1760, 100, 100, 100), fontPx=40, dx=5)
        moving.update(at=.5, hold=.5)
        config = timeline([moving])
        shared = public_diagnostics(config, [14, 15, 29, 30])
        for frame in (14, 15, 29, 30):
            monkeypatch.setattr(lint, "_sample_times", lambda *args: [frame / 30])
            found = lint.composition(CUT, elements(config), 30, shared=shared)
            assert bool(messages(found, "FRAME")) == (frame == 29)
            if frame in (14, 30):
                assert not messages(found, "REGION")
        assert shared["scene_frames"]["15"]["layers"][0]["diagnostics"]["motion"] == {"position": 0}
        assert shared["scene_frames"]["29"]["layers"][0]["diagnostics"]["motion"] == {"position": 14}
        assert shared["scene_frames"]["30"]["layers"] == []

    @pytest.mark.parametrize("change", ["absent", "opacity", "offscreen"])
    def test_known_invisible_is_not_a_finding(self, public_diagnostics, no_private_boxes, change):
        item = clip("type", bounds=rect(1900, 100, 200, 100),
                    textRect=rect(1900, 100, 200, 100), fontPx=10)
        if change == "absent":
            item["params"]["absent"] = True
        elif change == "opacity":
            item["opacity"] = 0
        else:
            item["params"]["rect"]["x"] = 2000
            item["params"]["textRect"]["x"] = 2000
        config = timeline([item])
        shared = public_diagnostics(config)
        assert shared["scene_frames"]["12"]["layers"][0]["visible"] is False
        assert not lint.composition(CUT, elements(config), 30, shared=shared)

    @pytest.mark.parametrize("change", ["unknown", "omitDiagnostics"])
    def test_unknown_and_missing_regions_are_advisory(self, public_diagnostics, no_private_boxes, change):
        config = timeline([clip("type", **{change: True})])
        found = lint.composition(CUT, elements(config), 30, shared=public_diagnostics(config))
        assert messages(found, "REGION")
        assert all(f.severity == "info" for f in found)

    def test_repeated_source_ids_require_unique_occurrence_mapping(self, public_diagnostics, no_private_boxes):
        graph = json.loads((ROOT / "tests/fixtures/timeline/shot_composition.json").read_text())
        graph["occurrences"] = graph["occurrences"][:2]
        revision = next(r for r in graph["shot_revisions"] if r["shot_id"] == "shot-alpha" and r["revision_id"] == "rev-a")
        item = clip("type", bounds=rect(1900, 100), textRect=rect(1900, 100), fontPx=20)
        item["hold"] = 2
        revision["internal_timeline_revision"]["timeline"] = timeline([item])
        config = project_shot_composition(graph).config
        second = next(c for c in config["clips"] if c["shot_occurrence_id"] == "occ-2")
        second["params"].update(rect=rect(), textRect=rect(), fontPx=40)
        shared = public_diagnostics(config, [12, 30, 132, 150])
        source = elements(config)
        for element in source:
            element.id = element.clip["app"]["astrid_shot_composition"]["source_clip_id"]
            element.clip = {"id": element.id}
        first_cut, second_cut = {**CUT, "end": 2}, {**CUT, "start": 4, "end": 6}
        assert messages(lint.composition(first_cut, source, 30, shared=shared), "FRAME")
        assert not messages(lint.composition(second_cut, source, 30, shared=shared), "FRAME")
        ambiguous = source + [copy.deepcopy(source[0])]
        found = lint.composition(first_cut, ambiguous, 30, shared=shared)
        assert not messages(found, "FRAME")
        assert any("identity" in m for m in messages(found, "REGION"))
        shared["scene_clip_identities"] = {}
        assert any("identity" in m for m in messages(lint.composition(first_cut, source, 30, shared=shared), "REGION"))

    @pytest.mark.parametrize("change", ["frame", "canvas", "layers", "identity", "duplicate", "visible", "bounds", "face", "text", "minPx"])
    def test_malformed_or_missing_facts_do_not_trigger_private_math(self, public_diagnostics, no_private_boxes, change):
        config = timeline([clip("type", textRect=rect(), fontPx=40, face=rect())])
        shared = public_diagnostics(config)
        for frame, row in shared["scene_frames"].items():
            layer = row["layers"][0]
            if change == "frame":
                row["frame"] = 900
            elif change == "canvas":
                row["height"] = 0
            elif change == "layers":
                row["layers"] = [None]
            elif change == "identity":
                layer["clipId"] = "no-suffix-guess:type"
            elif change == "duplicate":
                row["layers"].append(copy.deepcopy(layer))
            elif change == "visible":
                layer["visible"] = "unknown"
            elif change == "bounds":
                layer["bounds"] = {"status": "known", "rect": {**rect(), "width": "100"}}
            elif change == "face":
                layer["diagnostics"]["face"] = {"status": "known", "rect": {**rect(), "x": True}}
            elif change == "text":
                layer["diagnostics"]["text"]["bounds"] = {"status": "unknown", "reason": "no glyph/layout proof"}
            else:
                layer["diagnostics"]["text"]["minPx"] = "40"
        found = lint.composition(CUT, elements(config), 30, shared=shared)
        assert messages(found, "REGION")
        assert all(f.severity == "info" for f in found)
