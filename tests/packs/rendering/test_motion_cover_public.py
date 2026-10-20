"""COVER policy over real public scene/occlusion answers, plus unavailable inputs."""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.timeline.cuts import occurrences_from_snapshot
from astrid.core.timeline.shot_composition_projection import project_shot_composition
from astrid.packs.rendering.actions.timeline_visualize.motion import lint, model

ROOT = Path(__file__).resolve().parents[3]
CUT = {"index": 1, "start": 0, "end": 1}


def clip(clip_id, track, kind="am-type", *, x=300, y=300, width=100, height=100, **extra):
    return {"id": clip_id, "track": track, "clipType": kind, "at": 0, "hold": 1,
            "params": {"text": clip_id, "rect": {"x": x, "y": y, "width": width, "height": height}}, **extra}


def timeline(clips):
    return {"tracks": [{"id": track, "kind": "visual", "label": track}
                       for track in dict.fromkeys(c["track"] for c in reversed(clips))], "clips": clips}


def elements(config):
    return model.elements_from_occurrences(occurrences_from_snapshot(config))


def cover(findings):
    return [f.message for f in findings if f.code == "COVER"]


def test_missing_shared_context_is_advisory_and_keeps_other_checks():
    element = model.Element("card", "am-callout", "fx", 0, 1,
                            {"title": "Offscreen", "body": "small body", "x": 1900, "y": 100, "width": 400}, {})
    legacy = lint.composition(CUT, [element], 30)
    canonical = lint.composition(CUT, [element], 30, shared={"scene_unavailable": "historical PNG has no scene facts"})
    assert [f for f in canonical if f.code != "SCENE"] == legacy
    assert {f.code for f in canonical} >= {"SCENE", "FRAME", "SMALL", "SAFE"}
    assert all(f.severity == "info" and "historical PNG" in f.message for f in canonical if f.code == "SCENE")


def test_tracked_faces_stay_labelled_and_timing_stays_data_only():
    from types import SimpleNamespace

    element = model.Element("card", "am-callout", "fx", 0, 1,
                            {"title": "Tracked", "x": 300, "y": 300, "width": 400}, {})
    tracks = [SimpleNamespace(name="face", kind="boxes", clip_id="footage",
                              boxes_at=lambda t: [(300, 300, 700, 700)])]
    found = lint.composition(CUT, [element], 30, tracks=tracks, shared={})
    assert any(f.code == "FACE" and "tracked face" in f.message for f in found)
    assert lint.timing({"index": 1, "start": 0, "end": .4}, [element], [], 30)[0].code == "SHORT"


@pytest.fixture(scope="module")
def public_query(tmp_path_factory):
    # The public-package integration lane requires an actual release artifact
    # and locked peers. A private draft can be selected without changing pins.
    artifact = Path(os.environ.get("ASTRID_COMPOSITION_TEST_ARTIFACT", str(
        ROOT / "remotion/artifacts/banodoco-timeline-composition-0.0.9.tgz")))
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == (
        "fa94f9c6438278764fad1285fa3d76063020ea7b20f4018de6bec4ffff0c9f61")
    peers = Path(os.environ.get("ASTRID_COMPOSITION_TEST_NODE_MODULES", str(ROOT / "remotion/node_modules")))
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok, node.problem
    assert artifact.is_file(), "public occlusion tests require the Composition release with querySceneOcclusion"
    assert peers.is_dir(), "requires the locked Remotion peer graph"
    project = tmp_path_factory.mktemp("motion-cover-public")
    modules = project / "node_modules"
    package = modules / "@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(artifact) as archive:
        archive.extractall(project, filter="data")
    (project / "package").rename(package)
    for peer in peers.iterdir():
        if peer.name != "@banodoco":
            (modules / peer.name).symlink_to(peer, target_is_directory=peer.is_dir())
    shutil.copyfile(Path(__file__).with_name("motion_cover_public.mjs"), project / "query.mjs")

    def hashes():
        return {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in package.rglob("*") if p.is_file()}

    before = hashes()
    assert len(before) == 77
    env = {k: v for k, v in os.environ.items() if k not in ("NODE_OPTIONS", "NODE_PATH")}

    def query(config, frames=(12, 15)):
        return json.loads(subprocess.check_output(
            [str(node.path), "query.mjs"], cwd=project, env=env, text=True,
            input=json.dumps({"timeline": config, "frames": frames}), timeout=30))

    try:
        yield query
        assert hashes() == before
    finally:
        shutil.rmtree(project)


@pytest.mark.integration
class TestPublicOcclusion:
    def test_cover_messages_and_order_equal_legacy(self, public_query, monkeypatch):
        config = timeline([clip("lower-a", "back"), clip("lower-b", "back", x=700),
                           clip("upper-b", "front", "am-callout", x=690, y=290, width=120, height=120),
                           clip("upper-a", "front", "am-callout", x=290, y=290, width=120, height=120)])
        source = elements(config)

        def boxes(element, t, fps):
            r = element.params["rect"]
            return [model.Box(element, "card" if element.type == "am-callout" else "text",
                              (r["x"], r["y"], r["x"] + r["width"], r["y"] + r["height"]), element.label)]

        monkeypatch.setattr(model, "boxes_at", boxes)
        legacy = cover(lint.composition(CUT, source, 30, track_order=["front", "back"]))
        shared = public_query(config)
        monkeypatch.setattr(model, "boxes_at", lambda *args: [])

        def private_math(*args):
            raise AssertionError("canonical COVER must not use private geometry/order")

        monkeypatch.setattr(lint, "_z", private_math)
        monkeypatch.setattr(model, "intersection", private_math)
        monkeypatch.setattr(model, "area", private_math)
        canonical = lint.composition(CUT, source, 30, track_order=["back", "front"], shared=shared)
        assert cover(canonical) == legacy == [
            'am-callout "upper-a" fully covers am-type "lower-a"',
            'am-callout "upper-b" fully covers am-type "lower-b"']
        assert not any(f.code == "SCENE" for f in canonical)

    @pytest.mark.parametrize("width,opacity,support,kind,expected", [
        (97, 1, "rect", "am-callout", False),
        (98, 1, "rect", "am-callout", True),
        (100, .5, "rect", "am-callout", False),
        (100, 0, "rect", "am-callout", False),
        (100, 1, "none", "am-callout", False),
        (100, 1, "rect", "test-unknown", False),
    ])
    def test_threshold_translucency_glyph_holes_and_unknown(self, public_query, width, opacity, support, kind, expected):
        top = clip("upper", "front", kind, width=width, opacity=opacity)
        top["params"]["support"] = support
        config = timeline([clip("lower", "back"), top])
        shared = public_query(config)
        findings = lint.composition(CUT, elements(config), 30, shared=shared)
        assert bool(cover(findings)) == expected
        assert any(f.code == "SCENE" for f in findings) == (kind == "test-unknown" or support == "none")
        if width == 97:
            assert shared["scene_occlusions"]["0.9"]["12"]["lower"]["occluderId"] == "upper"
            assert not cover(findings)  # the .9 answer cannot satisfy the .98 policy
        if opacity == .5:
            assert "opacity:0.5" in shared["html"]["12"]

    def test_same_track_painter_order_and_half_open_boundaries(self, public_query, monkeypatch):
        config = timeline([clip("lower", "one"), clip("upper", "one", "am-callout", hold=.5)])
        shared = public_query(config, [0, 14, 15, 29, 30])
        source = elements(config)
        for frame in [0, 14, 15, 29, 30]:
            monkeypatch.setattr(lint, "_sample_times", lambda *args: [frame / 30])
            findings = lint.composition(CUT, source, 30, shared=shared)
            assert bool(cover(findings)) == (frame < 15)
            assert not any(f.code == "SCENE" for f in findings)
        assert shared["scene_frames"]["30"]["layers"] == []

    def test_canvas_clipping_offscreen_and_unknown_target(self, public_query):
        config = timeline([clip("lower", "back", x=-50), clip("upper", "front", "am-callout", x=0, width=50)])
        shared = public_query(config)
        # Public policy measures the target's on-canvas support. Python does
        # not intersect the original 100px rectangle with the frame again.
        assert shared["scene_occlusions"]["0.98"]["12"]["lower"]["fraction"] == 1
        assert len(cover(lint.composition(CUT, elements(config), 30, shared=shared))) == 1
        config["clips"][0]["params"]["rect"]["x"] = -200
        shared = public_query(config)
        assert not cover(lint.composition(CUT, elements(config), 30, shared=shared))
        config["clips"][0]["clipType"] = "test-unknown"
        shared = public_query(config)
        findings = lint.composition(CUT, elements(config), 30, shared=shared)
        assert not cover(findings)
        assert any(f.code == "SCENE" and "Target output bounds are unknown" in f.message for f in findings)

    @pytest.mark.parametrize("missing", ["frame", "threshold", "target", "occluder", "unknown"])
    def test_exact_facts_are_required_without_private_fallback(self, public_query, missing):
        config = timeline([clip("lower", "back"), clip("upper", "front", "am-callout")])
        shared = public_query(config)
        for frame in ["12", "15"]:
            if missing == "frame":
                del shared["scene_frames"][frame]
            elif missing == "threshold":
                shared["scene_occlusions"]["0.98"][frame] = {}
            elif missing in ("target", "occluder"):
                shared["scene_frames"][frame]["layers"] = [layer for layer in shared["scene_frames"][frame]["layers"]
                    if layer["clipId"] != ("lower" if missing == "target" else "upper")]
            else:
                shared["scene_occlusions"]["0.98"][frame]["lower"] = {"status": "unknown", "reason": "unadmitted bounds"}
        findings = lint.composition(CUT, elements(config), 30, shared=shared)
        assert not cover(findings)
        assert any(f.code == "SCENE" and "unavailable" in f.message for f in findings)

    def test_repeated_source_ids_use_projected_occurrence_identity(self, public_query):
        graph = json.loads((ROOT / "tests/fixtures/timeline/shot_composition.json").read_text())
        graph["occurrences"] = graph["occurrences"][:2]  # the same immutable shot twice
        revision = next(r for r in graph["shot_revisions"] if r["shot_id"] == "shot-alpha" and r["revision_id"] == "rev-a")
        revision["internal_timeline_revision"]["timeline"] = timeline([
            clip("lower", "back", hold=2), clip("upper", "front", "am-callout", hold=2)])
        projected = project_shot_composition(graph)
        config = projected.config
        # Only the second occurrence's upper layer is translucent.
        second_upper = next(c for c in config["clips"] if c["shot_occurrence_id"] == "occ-2"
                            and c["app"]["astrid_shot_composition"]["source_clip_id"] == "upper")
        second_upper["opacity"] = .5
        shared = public_query(config, [12, 30, 132, 150])
        source = elements(config)
        first = lint.composition({**CUT, "end": 2}, source, 30, shared=shared)
        second = lint.composition({**CUT, "start": 4, "end": 6}, source, 30, shared=shared)
        assert len(cover(first)) == 1
        assert not cover(second)
        assert not any(f.code == "SCENE" for f in first + second)
        assert shared["scene_occlusions"]["0.98"]["12"]["occ-1:lower"]["occluderId"] == "occ-1:upper"
        assert shared["scene_occlusions"]["0.98"]["132"]["occ-2:lower"]["occluderId"] is None
        # Raw IDs/same display labels cannot replace the projector's exact join.
        raw = copy.deepcopy(source)
        for element in raw:
            element.id = element.clip["app"]["astrid_shot_composition"]["source_clip_id"]
            element.clip = {"id": element.id}
        assert cover(lint.composition({**CUT, "end": 2}, raw, 30, shared=shared)) == cover(first)
        assert not cover(lint.composition({**CUT, "start": 4, "end": 6}, raw, 30, shared=shared))
        ambiguous = raw + [copy.deepcopy(raw[0])]
        refused = lint.composition({**CUT, "end": 2}, ambiguous, 30, shared=shared)
        assert not cover(refused)
        assert any(f.code == "SCENE" and "identity" in f.message for f in refused)
        shared["scene_clip_identities"] = {}
        refused = lint.composition({**CUT, "end": 2}, raw, 30, shared=shared)
        assert not cover(refused)
        assert any(f.code == "SCENE" and "identity" in f.message for f in refused)


@pytest.mark.parametrize("shared", [
    {"scene_frames": None},
    {"scene_frames": {"12": None}},
    {"scene_frames": {"12": {"frame": 12, "layers": None}}},
    {"scene_frames": {"12": {"frame": 12, "layers": [None]}}},
    {"scene_frames": {"12": {"frame": 12, "layers": [{"clipId": "a"}]}}, "scene_occlusions": []},
    {"scene_frames": {"12": {"frame": 12, "layers": [{"clipId": "a"}]}},
     "scene_occlusions": {"0.98": {"12": {"a": {"status": "known", "occluderId": []}}}}},
])
def test_malformed_shared_facts_are_advisory(shared, monkeypatch):
    monkeypatch.setattr(lint, "_sample_times", lambda *args: [.4])
    found = lint.composition(CUT, elements(timeline([clip("a", "back")])), 30, shared=shared)
    assert not cover(found)
    assert any(f.code == "SCENE" and f.severity == "info" for f in found)
