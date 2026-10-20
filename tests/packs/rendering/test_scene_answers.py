"""The Python adapter queries the immutable release, without renderer peers."""

import copy
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering import remotion_runtime
from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.timeline import Timeline, scene_answers

pytest_plugins = ("tests.packs.rendering.test_scene_host",)

ROOT = Path(__file__).resolve().parents[3]
SHA256 = "0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3"
_COMPOSITION_PACKAGE = "@banodoco/timeline-composition"


def _composition_archive() -> Path:
    package = json.loads((ROOT / "remotion/package.json").read_text(encoding="utf-8"))
    dependency = package["dependencies"][_COMPOSITION_PACKAGE]
    assert isinstance(dependency, str) and dependency.startswith("file:"), dependency
    archive = (ROOT / "remotion" / dependency.removeprefix("file:")).resolve()
    try:
        archive.relative_to((ROOT / "remotion").resolve())
    except ValueError as error:
        raise AssertionError(f"composition archive escapes Remotion root: {archive}") from error
    assert archive.is_file(), archive
    return archive


@pytest.fixture
def installed(tmp_path, monkeypatch):
    # Harness loader overrides are inadmissible; use the clean host environment.
    for key in ("PYTHONPYCACHEPREFIX", "NODE_OPTIONS", "NODE_PATH"):
        monkeypatch.delenv(key, raising=False)
    toolchain = resolve_pinned_node(
        ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert toolchain.ok, toolchain.problem
    node = str(toolchain.path)
    assert toolchain.version == "v20.19.4"
    artifact = _composition_archive()
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == SHA256
    package = tmp_path / "node_modules/@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(artifact) as archive:
        archive.extractall(tmp_path, filter="data")
    (tmp_path / "package").rename(package)
    (tmp_path / "package.json").write_text('{"type":"module"}')
    shutil.copyfile(ROOT / "remotion/scene-query.mjs", tmp_path / "scene-query.mjs")

    def hashes():
        return {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in package.rglob("*") if p.is_file()}

    before = hashes()
    assert len(before) == 77
    # Admission is tested separately. Only the status seam is replaced here;
    # subprocess/import/preparation/query all execute the real installed artifact.
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        remotion_runtime.RemotionRuntimeStatus(
                            True, tmp_path, node_executable=Path(node), node_version="v20.19.4"))
    yield tmp_path, node, package
    assert hashes() == before


def scene(clips=None, transitions=None):
    clips = clips if clips is not None else [
        {"id": "exact:first", "at": 0, "hold": 1, "track": "plate", "clipType": "custom"},
        {"id": "exact:second", "at": 1, "hold": 1, "track": "plate", "clipType": "custom"},
    ]
    return {"tracks": [{"track": {"id": "plate", "kind": "visual"}, "clips": clips,
                        "transitions": transitions if transitions is not None else [None]}],
            "assets": {"assets": {}}, "fps": 30, "width": 641, "height": 359}


def canonical(project, node, payload, frames):
    script = """
import {prepareScene, querySceneFrame} from '@banodoco/timeline-composition/evaluation';
import {readFileSync} from 'node:fs';
const {scene: s, frames} = JSON.parse(readFileSync(0, 'utf8'));
const prepared = prepareScene(s.tracks, s.assets, s.fps, s.width, s.height,
  {roles: s.roles, elements: new Set(s.elements ?? [])});
console.log(JSON.stringify(frames.map(frame => querySceneFrame(prepared, frame))));
"""
    return json.loads(subprocess.check_output(
        [node, "--input-type=module", "-e", script], cwd=project, text=True,
        input=json.dumps({"scene": payload, "frames": frames})))


@pytest.mark.parametrize("kind", ["dip", "dissolve"])
@pytest.mark.parametrize("align", ["start", "center", "end"])
def test_transition_frames_equal_canonical_public_query(installed, kind, align):
    project, node, _ = installed
    payload = scene(transitions=[{"T": 8, "kind": kind, "align": align}])
    original = copy.deepcopy(payload)
    frames = [0, 21, 22, 25, 26, 29, 30, 31, 33, 34, 37, 38, 59, 60, 30]
    answers = scene_answers.frames_at(payload, iter(frames))
    assert answers == canonical(project, node, payload, frames)
    assert payload == original
    assert answers[-2]["layers"] == []  # half-open final boundary
    if align == "end":
        incoming = answers[2]["layers"][1]
        assert (incoming["clipId"], incoming["drawLocalFrame"], incoming["ownFrame"]) == (
            "exact:second", 0, 0)
        assert answers[5]["layers"][1]["ownFrame"] == 0
    if align == "start":
        outgoing = answers[6]["layers"][0]
        assert (outgoing["drawLocalFrame"], outgoing["ownFrame"]) == (30, 29)


def test_cut_fractional_fps_and_empty_scene_are_answers(installed):
    project, node, _ = installed
    payload = scene()
    payload["fps"] = 30000 / 1001
    frames = [29, 30, 59, 60]
    answers = scene_answers.frames_at(payload, frames)
    assert answers == canonical(project, node, payload, frames)
    assert [[layer["clipId"] for layer in answer["layers"]] for answer in answers] == [
        ["exact:first"], ["exact:second"], ["exact:second"], []]
    payload["tracks"] = []
    assert scene_answers.frames_at(payload, [0]) == [
        {"frame": 0, "width": 641, "height": 359, "layers": [],
         "coverage": "GAP", "content": None, "findings": []}]


def test_resolved_painter_order_and_compiled_payload_are_preserved(installed, monkeypatch):
    project, node, _ = installed
    payload = scene()
    payload["tracks"][0]["clips"][0]["compiledExtension"] = {"opaque": [1, None, "keep"]}
    payload["tracks"].append({"track": {"id": "front", "kind": "visual"}, "clips": [
        {"id": "front:exact-id", "at": 0, "hold": 1, "clipType": "custom"}],
        "transitions": []})
    payload["roles"] = {"front:exact-id": "content"}
    requests = []
    run = subprocess.run

    def capture(*args, **kwargs):
        requests.append(json.loads(kwargs["input"]))
        return run(*args, **kwargs)

    monkeypatch.setattr(scene_answers.subprocess, "run", capture)
    answers = scene_answers.frames_at(payload, [1, 0, 1])
    assert requests == [{"scene": payload, "frames": [1, 0, 1]}]
    monkeypatch.setattr(scene_answers.subprocess, "run", run)
    assert answers == canonical(project, node, payload, [1, 0, 1])
    assert [layer["clipId"] for layer in answers[0]["layers"]] == ["exact:first", "front:exact-id"]


@pytest.mark.parametrize("clip_id", ["__proto__", "constructor", "toString"])
@pytest.mark.parametrize("role", [None, "background"])
def test_reserved_clip_ids_use_only_authored_role_overrides(installed, clip_id, role):
    payload = scene(clips=[
        {"id": clip_id, "track": "plate", "clipType": "custom", "at": 0, "hold": 1},
    ], transitions=[])
    if role is not None:
        payload["roles"] = {clip_id: role}
    answer = scene_answers.frames_at(payload, [0])[0]
    assert answer["layers"][0]["clipId"] == clip_id
    assert answer["layers"][0]["role"] == (role or "picture")
    assert answer["coverage"] == "UNKNOWN"


def test_unknown_custom_modifier_and_unresolved_media_stay_unknown(installed):
    payload = scene(clips=[
        {"id": "custom", "at": 0, "hold": 1, "clipType": "my-component",
         "params": {"width": 641, "opaque": True}},
        {"id": "missing", "at": 0, "hold": 1, "asset": "missing-media"},
        {"id": "modifier", "at": 0, "hold": 1, "asset": "image",
         "modifiers": [{"id": "m", "element": "custom-modifier", "params": {}}]},
    ], transitions=[None, None])
    payload["assets"]["assets"]["image"] = {
        "file": "unverified.png", "type": "image", "resolution": "641x359", "opaque": True}
    answer = scene_answers.frames_at(payload, [0])[0]
    assert answer["coverage"] == "UNKNOWN"
    assert all(layer["visible"] == "unknown" for layer in answer["layers"])
    assert all(layer["opaqueSupport"] == "unknown" for layer in answer["layers"])
    assert {finding["code"] for finding in answer["findings"]} >= {
        "unknown-component-internals", "unknown-media-alpha", "modifier-admission-refused"}


@pytest.mark.parametrize("broken", ["missing", "broken"])
def test_public_package_failure_is_unavailable(installed, broken):
    _, _, package = installed
    # Use a separate copy so the immutable fixture itself remains unchanged.
    project = package.parents[2] / broken
    target = project / "node_modules/@banodoco/timeline-composition"
    target.parent.mkdir(parents=True)
    shutil.copytree(package, target)
    shutil.copyfile(ROOT / "remotion/scene-query.mjs", project / "scene-query.mjs")
    evaluation = target / "dist/evaluation.js"
    if broken == "missing":
        evaluation.unlink()
    else:
        evaluation.write_text("throw new Error('broken evaluation');")
    status = scene_answers.remotion_runtime_status()
    from unittest.mock import patch

    with patch.object(scene_answers, "remotion_runtime_status", return_value=
                      remotion_runtime.RemotionRuntimeStatus(
                          True, project, node_executable=status.node_executable)):
        with pytest.raises(scene_answers.SceneQueryUnavailable, match="unavailable"):
            scene_answers.frames_at(scene(), [0])


def test_invalid_runtime_context_never_becomes_empty_answer(tmp_path, monkeypatch):
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(tmp_path / "missing"))
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="project directory not found"):
        scene_answers.frames_at({"tracks": []}, [0])


def test_invalid_launch_validation_is_unavailable(installed, monkeypatch):
    project, node, _ = installed
    cli = project / remotion_runtime.REMOTION_CLI_RELATIVE_PATH
    cli.parent.mkdir(parents=True)
    cli.write_text("// not executed")
    monkeypatch.setenv("ASTRID_NODE_EXECUTABLE", node)
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(project))
    for key in list(os.environ):
        if key.startswith("GIT_"):
            monkeypatch.delenv(key)
    for key in remotion_runtime._REF_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        remotion_runtime.RemotionRuntimeStatus(
                            False, project, remotion_runtime.resolve_remotion_runtime_tools(project)[1]))
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="missing or invalid launch validation"):
        scene_answers.frames_at(scene(), [0])


def test_unsupported_loader_override_is_unavailable(installed, monkeypatch):
    monkeypatch.setenv("NODE_OPTIONS", "--inspect")
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="unsupported loader"):
        scene_answers.frames_at(scene(), [0])


@pytest.mark.parametrize("escape", [False, True])
def test_missing_or_escaped_admitted_helper_is_unavailable(installed, tmp_path_factory, escape):
    project, _, _ = installed
    helper = project / "scene-query.mjs"
    helper.unlink()
    if escape:
        outside = tmp_path_factory.mktemp("scene-helper") / "scene-query.mjs"
        outside.write_text("throw new Error('must not execute');")
        helper.symlink_to(outside)
    with pytest.raises(scene_answers.SceneQueryUnavailable):
        scene_answers.frames_at(scene(), [0])


@pytest.mark.parametrize("response", [[], [{"frame": 1}], [{"frame": False}], [None], {}])
def test_invalid_response_cardinality_or_frame_is_unavailable(installed, monkeypatch, response):
    monkeypatch.setattr(scene_answers.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(returncode=0, stdout=json.dumps(response)))
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="invalid scene query response"):
        scene_answers.frames_at(scene(), [0])


@pytest.mark.parametrize("change", ["unsorted", "unresolved", "frame"])
def test_invalid_resolved_inputs_are_unavailable(installed, change):
    payload = scene()
    frames = [0]
    if change == "unsorted":
        payload["tracks"][0]["clips"].reverse()
    elif change == "unresolved":
        payload["tracks"][0]["transitions"] = [{"id": "fade"}]
    else:
        frames = [-1]
    with pytest.raises(scene_answers.SceneQueryUnavailable):
        scene_answers.frames_at(payload, frames)


def test_prepared_host_query_uses_final_root_inside_lock(monkeypatch, tmp_path):
    props = {
        "timeline": {"tracks": [], "clips": []},
        "assets": {"assets": {}},
        "theme": {"visual": {}},
    }
    events = []
    calls = []

    @contextmanager
    def lock():
        events.append("lock-enter")
        yield
        events.append("lock-exit")

    @contextmanager
    def prepare(*args, **kwargs):
        calls.append((args, kwargs))
        events.append("prepare-enter")
        yield (props, tmp_path / ".props.json")
        events.append("prepare-exit")

    from astrid.core.rendering import profile, verified_source
    from astrid.packs.rendering.rendering.renderers.remotion import lock as remotion_lock
    from astrid.packs.rendering.rendering.renderers.remotion import root_preparation

    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        SimpleNamespace(available=True, project_dir=tmp_path / "remotion"))
    monkeypatch.setattr(verified_source, "inherited_source",
                        lambda *args, **kwargs: SimpleNamespace(
                            validate=lambda *args, **kwargs: None))
    monkeypatch.setattr(remotion_lock, "remotion_render_lock", lock)
    monkeypatch.setattr(root_preparation, "_prepared_remotion_root", prepare)
    monkeypatch.setattr(profile, "resolve_render_profile", lambda *args, **kwargs:
                        SimpleNamespace(width=641, height=359, fps_rational=(30000, 1001)))

    def query(received_props, basis, frames):
        assert received_props is props
        assert basis == {"width": 641, "height": 359, "fps": 30000 / 1001}
        assert tuple(frames) == (7, 0, 7)
        assert events == ["lock-enter", "prepare-enter"]
        return [{"frame": frame, "width": 641, "height": 359} for frame in frames]

    monkeypatch.setattr(scene_answers, "host_frames_at", query)
    result = scene_answers._prepared_host_frames_at(
        tmp_path / "timeline.json", tmp_path / "assets.json", (7, 0, 7),
        staged_video=tmp_path / "unused.mp4", provenance_out_path=tmp_path / "provenance.json",
        project_dir=tmp_path / "remotion", composition_id="TimelineComposition",
        theme_path=None, min_free_gb=None, frame_output_dir=tmp_path / "frames",
    )

    assert result == [
        {"frame": 7, "width": 641, "height": 359},
        {"frame": 0, "width": 641, "height": 359},
        {"frame": 7, "width": 641, "height": 359},
    ]
    assert calls[0][1]["frame_numbers"] == (7, 0, 7)
    assert calls[0][1]["frame_output_dir"] == tmp_path / "frames"
    assert events == ["lock-enter", "prepare-enter", "prepare-exit", "lock-exit"]


def test_prepared_host_query_reports_unavailable_without_fallback(monkeypatch, tmp_path):
    @contextmanager
    def prepare(*args, **kwargs):
        raise RuntimeError("source admission failed")
        yield  # pragma: no cover

    from astrid.packs.rendering.rendering.renderers.remotion import root_preparation

    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        SimpleNamespace(available=True, project_dir=tmp_path / "remotion"))
    from astrid.core.rendering import verified_source
    monkeypatch.setattr(verified_source, "inherited_source",
                        lambda *args, **kwargs: SimpleNamespace(
                            validate=lambda *args, **kwargs: None))
    monkeypatch.setattr(root_preparation, "_prepared_remotion_root", prepare)
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="source admission failed"):
        scene_answers._prepared_host_frames_at(
            tmp_path / "timeline.json", tmp_path / "assets.json", [0],
            staged_video=tmp_path / "unused.mp4", provenance_out_path=tmp_path / "provenance.json",
            project_dir=tmp_path / "remotion", composition_id="TimelineComposition",
            theme_path=None, min_free_gb=None, frame_output_dir=tmp_path / "frames",
        )


def _write_registered_scene_pair(tmp_path):
    timeline = tmp_path / "timeline.json"
    Timeline.from_config({
        "theme": "banodoco-default",
        "tracks": [{"id": "picture", "kind": "visual", "label": "Picture"}],
        "clips": [{"id": "prepared:plate", "track": "picture",
                   "clipType": "am-snap-plate", "at": 0, "hold": 1,
                   "params": {"fill": "#F7F4ED"}}],
    }).dump(timeline)
    assets = tmp_path / "assets.json"
    assets.write_text(json.dumps({"assets": {}}), encoding="utf-8")
    return timeline, assets


def _prepared_query_kwargs(tmp_path):
    return {
        "staged_video": tmp_path / "staged.mp4",
        "provenance_out_path": tmp_path / "provenance.json",
        "composition_id": "TimelineComposition",
        "theme_path": None,
        "min_free_gb": None,
        "frame_output_dir": tmp_path / "frames",
        "staging_parent": tmp_path / "staging",
    }


class _PreparedPairSource:
    def validate(self, timeline_path, assets_path):
        if not Path(timeline_path).is_file() or not Path(assets_path).is_file():
            raise ValueError("prepared source pair is unavailable")


def _real_runtime_tools(project, node):
    peers = Path(os.environ.get("ASTRID_TEST_NODE_MODULES", ROOT / "remotion/node_modules"))
    cli = project / "node_modules/@remotion/cli"
    if not cli.exists():
        cli.symlink_to((peers / "@remotion/cli").resolve(), target_is_directory=True)
    executable = cli / "remotion-cli.js"
    assert executable.is_file()
    return SimpleNamespace(node_executable=node.path, remotion_cli=executable)


def test_prepared_host_query_runs_registered_public_node_inside_real_root(
    native_host, host_project, tmp_path, monkeypatch,
):
    project, _ = host_project
    timeline, assets = _write_registered_scene_pair(tmp_path)
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok and node.version == "v20.19.4"

    from astrid.core.rendering import verified_source
    from astrid.packs.rendering.rendering.renderers.remotion import run
    monkeypatch.setattr(verified_source, "inherited_source",
                        lambda *args, **kwargs: _PreparedPairSource())
    monkeypatch.setattr(run, "_available_remotion_port", lambda: 32101)
    monkeypatch.setattr(run, "_validate_project_dir", lambda _: _real_runtime_tools(project, node))
    frames = list(range(31))
    rows = scene_answers._prepared_host_frames_at(
        timeline, assets, frames, project_dir=project,
        **_prepared_query_kwargs(tmp_path),
    )

    assert [row["frame"] for row in rows] == frames
    assert all((row["coverage"], row["content"]) == ("COVERED", "EMPTY")
               for row in rows[:-1])
    assert (rows[-1]["coverage"], rows[-1]["content"]) == ("GAP", None)
    assert rows[0]["layers"][0]["clipId"] == "prepared:plate"
    assert rows[0]["layers"][0]["bounds"] == {
        "status": "known", "rect": {"x": 0, "y": 0, "width": 1920, "height": 1080},
    }
    assert not (tmp_path / ".remotion-props.json").exists()
    assert not list((tmp_path / "staging").glob(".remotion-runtime-*"))
    assert not list((project / "public" / "astrid-effects").glob("*"))


@pytest.mark.parametrize("source", ["missing", "stale"])
def test_prepared_host_query_refuses_missing_or_stale_source_pair_and_cleans(
    native_host, host_project, tmp_path, monkeypatch, source,
):
    project, _ = host_project
    timeline, assets = _write_registered_scene_pair(tmp_path)
    if source == "missing":
        timeline.unlink()
    else:
        assets.write_text(json.dumps({"assets": {
            "gone": {"object_id": "missing-object", "type": "image",
                      "digest": "sha256:" + "0" * 64},
        }}), encoding="utf-8")

    from astrid.packs.rendering.rendering.renderers.remotion import run

    monkeypatch.setattr(run, "_available_remotion_port", lambda: 32101)
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok and node.version == "v20.19.4"
    monkeypatch.setattr(run, "_validate_project_dir", lambda _: _real_runtime_tools(project, node))
    with pytest.raises(scene_answers.SceneQueryUnavailable):
        scene_answers._prepared_host_frames_at(
            timeline, assets, [0], project_dir=project,
            **_prepared_query_kwargs(tmp_path),
        )

    assert not (tmp_path / ".remotion-props.json").exists()
    assert not list((tmp_path / "staging").glob(".remotion-runtime-*"))
    assert not list((project / "public" / "astrid-effects").glob("*"))


def test_prepared_host_query_cleans_after_real_public_query_exception(
    native_host, host_project, tmp_path, monkeypatch,
):
    project, _ = host_project
    timeline, assets = _write_registered_scene_pair(tmp_path)
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok and node.version == "v20.19.4"

    from astrid.core.rendering import verified_source
    from astrid.packs.rendering.rendering.renderers.remotion import run
    monkeypatch.setattr(verified_source, "inherited_source",
                        lambda *args, **kwargs: _PreparedPairSource())
    monkeypatch.setattr(run, "_available_remotion_port", lambda: 32101)
    monkeypatch.setattr(run, "_validate_project_dir", lambda _: _real_runtime_tools(project, node))
    real_query = scene_answers.host_frames_at
    seen = []

    def query_then_fail(props, basis, frames):
        rows = real_query(props, basis, frames)
        seen.extend(rows)
        raise RuntimeError("consumer failed after real public answer")

    monkeypatch.setattr(scene_answers, "host_frames_at", query_then_fail)
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="consumer failed"):
        scene_answers._prepared_host_frames_at(
            timeline, assets, [0], project_dir=project,
            **_prepared_query_kwargs(tmp_path),
        )

    assert seen and seen[0]["layers"][0]["clipId"] == "prepared:plate"
    assert not (tmp_path / ".remotion-props.json").exists()
    assert not list((tmp_path / "staging").glob(".remotion-runtime-*"))
    assert not list((project / "public" / "astrid-effects").glob("*"))
