"""Inactive exact-fold IPC against the registered presenter and frozen releases."""

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter

import pytest

from astrid.core.rendering.remotion_runtime import RemotionRuntimeStatus
from astrid.core.theme import builtin_theme
from astrid.core.timeline import scene_answers
from tests.packs.rendering.test_presenter_scene_capability import (
    PRESENTER,
    ROOT,
)
from tests.packs.rendering.test_presenter_scene_capability import (
    presenter_query as _presenter_query,
)
from tests.packs.rendering.test_scene_sampling_plan import composed_snapshot

presenter_query = _presenter_query
BASIS = {"fps": 30000 / 1001, "width": 1920, "height": 1080}


@pytest.fixture
def motion_host(presenter_query, monkeypatch):
    project = presenter_query.project
    shutil.copyfile(ROOT / "remotion/scene-query.mjs", project / "scene-query.mjs")
    for key in ("NODE_OPTIONS", "NODE_PATH", "PYTHONPYCACHEPREFIX"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("ASTRID_PACKS_PATH", presenter_query.env["ASTRID_PACKS_PATH"])
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        RemotionRuntimeStatus(True, project, node_executable=presenter_query.node))
    sources = [*ROOT.joinpath(PRESENTER).glob("*.ts*"),
               ROOT / "remotion/src/host-scene.ts", ROOT / "remotion/src/host-registries.ts"]
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    yield presenter_query
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources} == before


def inputs():
    # Keep the projector's distinct compiled occurrence IDs for a repeated source.
    repeated = [copy.deepcopy(c) for c in composed_snapshot()["config"]["clips"]
                if c["app"]["astrid_shot_composition"]["source_clip_id"] == "lower"]
    fps = BASIS["fps"]
    for i, clip in enumerate(repeated):
        clip.update(track=clip["id"], at=0, from_=7, hold=(301 if i == 0 else 150.5) / fps,
                    speed=1 if i == 0 else .5, clipType="am-presenter",
                    elementRef={"kind": "effect", "id": "am-presenter", "packId": "astrid_motion"},
                    params={"words": [[180 / fps, 183 / fps]], "seed": 7,
                            "chrome": "none", "blinkEvery": 0})
        clip["from"] = clip.pop("from_")
    # Same short authored pulse, absent outside its own half-open lifetime.
    short = {**copy.deepcopy(repeated[0]), "id": "short", "track": "short",
             "at": 100 / fps, "hold": 12 / fps,
             "params": {"words": [[0, 6 / fps]], "seed": 7, "chrome": "none", "blinkEvery": 0}}
    clips = [*repeated, short]
    props = {"timeline": {"tracks": [{"id": c["track"], "kind": "visual"} for c in clips],
                           "clips": clips}, "assets": {"assets": {}}, "theme": builtin_theme()}
    request = {"ranges": [[0, 301]], "clip_ids": [c["id"] for c in clips],
               "keys": ["mouth", "not-published"], "max_frames": 301}
    return props, request


@pytest.mark.integration
def test_registered_presenter_actual_ipc_exact_counts(motion_host, monkeypatch):
    from fractions import Fraction

    from astrid.packs.rendering.actions.timeline_visualize.motion import sheet

    props, request = inputs()
    before = copy.deepcopy(props)
    calls = []
    run = scene_answers.subprocess.run

    def capture(*args, **kwargs):
        calls.append((json.loads(kwargs["input"]), kwargs["timeout"]))
        return run(*args, **kwargs)

    monkeypatch.setattr(scene_answers.subprocess, "run", capture)
    result = scene_answers.host_motion_counts(props, BASIS, **request)
    assert len(calls) == 1 and calls[0][1] == 30
    assert calls[0][0] == {"query": "motion", "props": props, "basis": BASIS, "motion": {
        "ranges": [[0, 301]], "clipIds": request["clip_ids"], "keys": request["keys"], "maxFrames": 301}}
    monkeypatch.setattr(scene_answers.subprocess, "run", run)
    frames = scene_answers.host_frames_at(props, BASIS, range(301))
    for row in result["counts"]:
        values, unknown, absent = Counter(), 0, 0
        for frame in frames:
            layer = next((layer for layer in frame["layers"] if layer["clipId"] == row["clipId"]), None)
            if layer is None:
                absent += 1
            elif row["key"] not in layer.get("diagnostics", {}).get("motion", {}):
                unknown += 1
            else:
                values[layer["diagnostics"]["motion"][row["key"]]] += 1
        assert row == {"clipId": row["clipId"], "key": row["key"], "totalFrames": 301,
                       "unknownFrames": unknown, "absentFrames": absent,
                       "values": [{"value": v, "count": n} for v, n in sorted(values.items())]}
    first, missing, second, _, short, short_missing = result["counts"]
    assert sorted(v["count"] for v in first["values"]) == [1, 1, 299]
    assert second["values"] == [{"value": first["values"][0]["value"], "count": 301}]
    assert missing["unknownFrames"] == 301
    assert short["absentFrames"] == 289
    assert short_missing["unknownFrames"] == 12 and short_missing["absentFrames"] == 289
    fps = Fraction(30000, 1001)
    samples = sheet.curve_sample_frames((0, Fraction(301) / fps), fps)
    assert len(samples) == sheet.SCENE_FRAME_BUDGET == 60
    assert not set(samples).intersection((180, 181, 182))
    sampled = [next(layer for layer in frames[f]["layers"] if layer["clipId"] == first["clipId"])
               ["diagnostics"]["motion"]["mouth"] for f in samples]
    assert len(set(sampled)) == 1 and len(first["values"]) == 3
    assert props == before


@pytest.mark.integration
def test_one_host_preparation_and_one_public_query_per_selected_frame(motion_host):
    # Instrument only the temporary transport copy; all evaluator/package/source
    # files remain untouched. The wrapper delegates every real preparation/query.
    helper = motion_host.project / "scene-query.mjs"
    original = helper.read_text()
    instrumented = original.replace("const prepared = prepare(props, basis, hostRoles ?? {});", """
    let preparations = 0;
    const once = (...args) => { preparations++; return prepare(...args); };
    const prepared = once(props, basis, hostRoles ?? {});
    const observed = [];
    const query = (scene, frame) => {
      if (scene !== prepared) throw new Error('different prepared scene');
      observed.push(frame);
      return querySceneFrame(scene, frame);
    };
""").replace("foldSceneMotion(prepared, querySceneFrame, input.motion)", """
foldSceneMotion(prepared, query, input.motion);
    if (preparations !== 1 || JSON.stringify(observed) !== JSON.stringify([180, 181, 182, 300]))
      throw new Error('preparation/query count mismatch')
""")
    assert instrumented != original
    helper.write_text(instrumented)
    try:
        props, request = inputs()
        request.update(ranges=[[180, 183], [300, 301]], max_frames=4)
        assert scene_answers.host_motion_counts(props, BASIS, **request)["totalFrames"] == 4
    finally:
        helper.write_text(original)


@pytest.mark.integration
@pytest.mark.parametrize("change", ["stale", "duplicate", "source-id", "malformed"])
def test_actual_ipc_refuses_clip_identity_or_bad_host(motion_host, change):
    props, request = inputs()
    if change in ("stale", "source-id"):
        request["clip_ids"] = ["stale" if change == "stale" else "lower"]
    elif change == "duplicate":
        props["timeline"]["clips"].append(copy.deepcopy(props["timeline"]["clips"][0]))
    else:
        props.pop("theme")
    with pytest.raises(scene_answers.SceneQueryUnavailable):
        scene_answers.host_motion_counts(props, BASIS, **request)


@pytest.mark.integration
def test_missing_public_query_is_honestly_unavailable(motion_host, tmp_path, monkeypatch):
    # Separate broken package; never patch the frozen public10 extraction.
    project = tmp_path / "missing-export"
    package = project / "node_modules/@banodoco/timeline-composition"
    package.mkdir(parents=True)
    (project / "src").mkdir()
    (project / "src/host-scene.ts").write_text("// must not prepare")
    (project / "native-scene.mjs").write_text("throw Error('must not prepare');")
    (project / "package.json").write_text('{"type":"module"}')
    (package / "package.json").write_text('{"type":"module","exports":{"./evaluation":"./evaluation.js"}}')
    (package / "evaluation.js").write_text("export const prepareScene = () => {};\n")
    shutil.copyfile(ROOT / "remotion/scene-query.mjs", project / "scene-query.mjs")
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        RemotionRuntimeStatus(True, project, node_executable=motion_host.node))
    props, request = inputs()
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="scene_motion_export_missing"):
        scene_answers.host_motion_counts(props, BASIS, **request)


@pytest.mark.parametrize("change", [
    {"ranges": []}, {"ranges": [[1, 1]]}, {"ranges": [[2, 4], [3, 5]]},
    {"ranges": [[True, 2]]}, {"ranges": [[0, 3601]]}, {"ranges": [[2**53, 2**53 + 1]]},
    {"ranges": [[i, i + 1] for i in range(65)]},
    {"clip_ids": ["x", "x"]}, {"keys": []}, {"keys": ["x", "x"]},
    {"keys": [str(i) for i in range(65)]}, {"max_frames": True}, {"max_frames": 3601},
])
def test_invalid_selection_refuses_before_ipc(monkeypatch, change):
    monkeypatch.setattr(scene_answers, "_run_query", lambda *a, **k: pytest.fail("unexpected IPC"))
    props, request = inputs()
    with pytest.raises(scene_answers.SceneQueryUnavailable):
        scene_answers.host_motion_counts(props, BASIS, **{**request, **change})


@pytest.mark.parametrize("change", ["range", "total", "pair", "duplicate", "missing", "bool", "nan",
                                   "duplicate-value", "negative", "nonconserving", "error"])
def test_malformed_or_stale_fold_response_is_unavailable(monkeypatch, change):
    props, request = inputs()
    request.update(clip_ids=["exact"], keys=["arbitrary"])
    row = {"clipId": "exact", "key": "arbitrary", "totalFrames": 301, "unknownFrames": 0,
           "absentFrames": 0, "values": [{"value": -.125, "count": 301}]}
    answer = {"ranges": [[0, 301]], "totalFrames": 301, "counts": [row]}
    if change == "range":
        answer["ranges"] = [[1, 302]]
    elif change == "total":
        answer["totalFrames"] = 300
    elif change == "pair":
        row["clipId"] = "stale"
    elif change == "duplicate":
        answer["counts"].append(copy.deepcopy(row))
    elif change == "missing":
        row.pop("unknownFrames")
    elif change == "bool":
        row["unknownFrames"] = False
    elif change == "nan":
        row["values"][0]["value"] = float("nan")
    elif change == "duplicate-value":
        row["values"] = [{"value": 1, "count": 300}, {"value": 1, "count": 1}]
    elif change == "negative":
        row["values"][0]["count"] = -1
    elif change == "nonconserving":
        row["unknownFrames"] = 1
    else:
        answer = {"error": "public query failed"}
    monkeypatch.setattr(scene_answers, "_run_query", lambda *a, **k: [answer])
    with pytest.raises(scene_answers.SceneQueryUnavailable):
        scene_answers.host_motion_counts(props, BASIS, **request)


def test_internal_motion_transport_has_no_default_sdk_import_or_caller():
    script = """
import sys
import astrid.sdk
assert 'astrid.core.timeline.scene_answers' not in sys.modules
assert not any(n.startswith('astrid.core.rendering') for n in sys.modules)
"""
    subprocess.run([sys.executable, "-c", script], cwd=ROOT, check=True, timeout=30)
    # The only production occurrence is its definition; activation stays held.
    callers = [p for p in (ROOT / "astrid").rglob("*.py") if "host_motion_counts(" in p.read_text()]
    assert callers == [ROOT / "astrid/core/timeline/scene_answers.py"]
