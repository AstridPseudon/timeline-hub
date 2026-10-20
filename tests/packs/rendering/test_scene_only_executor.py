"""Private scene-only visualization reuses the managed filmstrip artifact."""

import json
import zipfile
from argparse import Namespace
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.timeline import scene_answers
from astrid.packs.rendering.actions.timeline_visualize import filmstrip_execution


def _args(tmp_path: Path) -> Namespace:
    timeline = tmp_path / "timeline.json"
    assets = tmp_path / "assets.json"
    timeline.write_text("{}", encoding="utf-8")
    assets.write_text('{"assets": {}}', encoding="utf-8")
    return Namespace(
        filmstrip_authority=None,
        project_slug="demo",
        out=tmp_path / "output",
        timeline=timeline,
        assets_registry=assets,
        materialized_root=None,
        materialized_objects=None,
        theme_path=None,
    )


def _authority(*, scene_clips=None, clips=None) -> dict:
    capture_identity = "sha256:" + "a" * 64
    return {
        "mode": "scene_only",
        "capture_snapshot": {
            "project_slug": "demo",
            "timeline_id": "timeline",
            "render_run_id": "capture:timeline:revision",
            "video_digest": capture_identity,
            "duration_frames": 4,
            "config": {"tracks": [], "clips": clips if clips is not None else [{"id": "compiled:clip"}]},
            "registry": {"assets": {}},
            "metadata": {
                "capture_authority": {"parent_revision_id": "revision"},
                "capture_identity": capture_identity,
                "scene_clips": (scene_clips if scene_clips is not None else
                                {"compiled:clip": {"address": "c01.layer"}}),
            },
        },
    }


class _Source:
    def __init__(self, *, stale: bool = False, bound_snapshot=None):
        self.stale = stale
        self.bound_snapshot = bound_snapshot or _authority()["capture_snapshot"]
        self.validations = []

    def validate_snapshot(self, snapshot):
        self.validations.append("snapshot")
        if self.stale:
            raise ValueError("capture source differs")

    def read(self):
        return {"snapshot": self.bound_snapshot}


@pytest.mark.parametrize("binding", ["saved", "candidate"])
def test_scene_only_queries_full_extent_and_uses_existing_bundle(tmp_path, monkeypatch, binding):
    args = _args(tmp_path)
    authority = _authority(scene_clips={"forged": {"address": "wrong.layer"}})
    bound_snapshot = _authority()["capture_snapshot"]
    if binding == "candidate":
        bound_snapshot["metadata"]["working_copy"] = {
            "base_parent": {"revision_id": "base-revision"},
        }
    source = _Source(bound_snapshot=bound_snapshot)
    calls = []
    label_sources = []
    expected_label = {
        "status": "candidate" if binding == "candidate" else "committed",
        "label": "candidate" if binding == "candidate" else "committed",
        "actual_revision_id": None if binding == "candidate" else "source-revision",
        "base_revision_id": "base-revision" if binding == "candidate" else None,
    }

    def unexpected_render(*args, **kwargs):
        pytest.fail("scene-only execution must not invoke filmstrip rendering")

    monkeypatch.setattr(filmstrip_execution, "_render_input_projection_png", unexpected_render)
    monkeypatch.setattr(filmstrip_execution, "_render_paired_rows", unexpected_render)
    monkeypatch.setattr(filmstrip_execution, "_render_time_anchored_output", unexpected_render)
    monkeypatch.setattr(
        filmstrip_execution,
        "snapshot_label",
        lambda snapshot, *, source=None: label_sources.append(source) or expected_label,
    )

    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: source,
    )

    def query(timeline, assets, frames, **kwargs):
        calls.append((timeline, assets, tuple(frames), kwargs))
        assert kwargs["frame_output_dir"].is_dir()
        return [{"frame": frame, "width": 1920, "height": 1080, "layers": []} for frame in frames]

    monkeypatch.setattr(scene_answers, "_prepared_host_frames_at", query)
    result = filmstrip_execution.execute_filmstrip(args, authority=authority)

    assert result["returncode"] == 0
    assert calls[0][2] == (0, 1, 2, 3)
    scene_path = Path(result["outputs"]["scene_answers"])
    payload = json.loads(scene_path.read_text(encoding="utf-8"))
    assert [answer["frame"] for answer in payload["answers"]] == [0, 1, 2, 3]
    assert payload["scene_clips"] == {"compiled:clip": {"address": "c01.layer"}}
    assert payload["snapshot_label"] == expected_label
    assert label_sources == [source]
    assert not list(scene_path.parent.glob("*.png"))
    assert not (args.out / ".scene-only-unused.mp4").exists()

    with zipfile.ZipFile(result["outputs"]["filmstrip_bundle"]) as bundle:
        assert "scene-answers.json" in bundle.namelist()
        assert not any(name.endswith(".png") for name in bundle.namelist())
    host_manifest = json.loads((args.out / "manifest.json").read_text(encoding="utf-8"))
    assert {row["name"] for row in host_manifest["outputs"]} == {
        "filmstrip_manifest", "filmstrip_bundle",
    }
    bundle_receipt = next(row for row in host_manifest["outputs"] if row["name"] == "filmstrip_bundle")
    assert bundle_receipt["provenance"] == {
        "video_digest": "sha256:" + "a" * 64,
        "timeline_id": "timeline",
    }


@pytest.mark.parametrize("stale", [True, False])
def test_scene_only_unavailable_is_advisory_and_has_no_partial_answers(tmp_path, monkeypatch, stale):
    args = _args(tmp_path)
    source = _Source(stale=stale)
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: source,
    )
    if not stale:
        def unavailable(*args, **kwargs):
            raise scene_answers.SceneQueryUnavailable("public host unavailable")

        monkeypatch.setattr(scene_answers, "_prepared_host_frames_at", unavailable)

    result = filmstrip_execution.execute_filmstrip(args, authority=_authority())
    payload = json.loads(Path(result["outputs"]["scene_answers"]).read_text(encoding="utf-8"))
    assert result["returncode"] == 0
    assert payload["answers"] == []
    assert payload["snapshot_label"] == {
        "status": "unavailable",
        "label": "revision unavailable",
        "actual_revision_id": None,
        "base_revision_id": None,
    }
    host_manifest = json.loads((args.out / "manifest.json").read_text(encoding="utf-8"))
    bundle_receipt = next(row for row in host_manifest["outputs"] if row["name"] == "filmstrip_bundle")
    assert "provenance" not in bundle_receipt


@pytest.mark.parametrize("identity_field", ["capture_identity", "video_digest"])
def test_scene_only_missing_prepared_capture_identity_is_unavailable(
    tmp_path, monkeypatch, identity_field,
):
    args = _args(tmp_path)
    authority = _authority()
    bound_snapshot = authority["capture_snapshot"]
    if identity_field == "capture_identity":
        del bound_snapshot["metadata"][identity_field]
    else:
        del bound_snapshot[identity_field]
    source = _Source(bound_snapshot=bound_snapshot)
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: source,
    )
    monkeypatch.setattr(
        scene_answers,
        "_prepared_host_frames_at",
        lambda *args, **kwargs: pytest.fail("missing capture identity must fail before query"),
    )

    result = filmstrip_execution.execute_filmstrip(args, authority=authority)
    payload = json.loads(Path(result["outputs"]["scene_answers"]).read_text(encoding="utf-8"))
    assert result["returncode"] == 0
    assert payload["answers"] == [] and payload["scene_clips"] == {}
    assert payload["snapshot_label"]["status"] == "unavailable"


@pytest.mark.parametrize("clips", [None, [{"id": ""}], [{"id": "a"}, {"id": "a"}], ["not-a-clip"]])
def test_scene_only_malformed_compiled_clips_are_unavailable(tmp_path, monkeypatch, clips):
    args = _args(tmp_path)
    authority = _authority(clips=clips) if clips is not None else _authority()
    if clips is None:
        del authority["capture_snapshot"]["config"]["clips"]
    source = _Source(bound_snapshot=authority["capture_snapshot"])
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: source,
    )
    monkeypatch.setattr(scene_answers, "_prepared_host_frames_at", lambda *args, **kwargs: pytest.fail("query"))

    result = filmstrip_execution.execute_filmstrip(args, authority=authority)
    payload = json.loads(Path(result["outputs"]["scene_answers"]).read_text(encoding="utf-8"))
    assert result["returncode"] == 0
    assert payload["snapshot_label"]["status"] == "unavailable"
    assert payload["answers"] == [] and payload["scene_clips"] == {}


def test_scene_only_query_must_cover_exact_extent_and_projected_ids(tmp_path, monkeypatch):
    args = _args(tmp_path)
    source = _Source()
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: source,
    )
    monkeypatch.setattr(
        filmstrip_execution,
        "snapshot_label",
        lambda snapshot, *, source: {"status": "committed", "label": "source", "actual_revision_id": "R1", "base_revision_id": None},
    )
    monkeypatch.setattr(
        scene_answers,
        "_prepared_host_frames_at",
        lambda *args, **kwargs: [
            {"frame": frame, "layers": [{"clipId": "not-in-source"}] if frame == 0 else []}
            for frame in range(4)
        ],
    )

    result = filmstrip_execution.execute_filmstrip(args, authority=_authority())
    payload = json.loads(Path(result["outputs"]["scene_answers"]).read_text(encoding="utf-8"))
    assert payload["snapshot_label"]["status"] == "unavailable"
    assert payload["answers"] == [] and payload["scene_clips"] == {}


def test_scene_only_missing_source_is_explicitly_unavailable(tmp_path, monkeypatch):
    args = _args(tmp_path)
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: None,
    )
    result = filmstrip_execution.execute_filmstrip(args, authority=_authority())
    payload = json.loads(Path(result["outputs"]["scene_answers"]).read_text(encoding="utf-8"))
    assert result["returncode"] == 0
    assert payload["snapshot_label"]["status"] == "unavailable"
    assert payload["answers"] == [] and payload["scene_clips"] == {}


def test_prepared_scene_query_keeps_root_alive_and_validates_source(monkeypatch, tmp_path):
    props = {
        "timeline": {"tracks": [], "clips": []},
        "assets": {"assets": {}},
        "theme": {"visual": {}},
    }
    source = SimpleNamespace(validate=lambda *args: None)
    events = []

    @contextmanager
    def lock():
        events.append("lock-enter")
        yield
        events.append("lock-exit")

    @contextmanager
    def prepare(*args, **kwargs):
        events.append("prepare-enter")
        yield (props, tmp_path / ".props.json")
        events.append("prepare-exit")

    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs: SimpleNamespace(
        available=True, project_dir=tmp_path / "remotion", node_executable=tmp_path / "node",
    ))
    monkeypatch.setattr(
        "astrid.packs.rendering.rendering.renderers.remotion.lock.remotion_render_lock", lock,
    )
    monkeypatch.setattr(
        "astrid.packs.rendering.rendering.renderers.remotion.root_preparation._prepared_remotion_root",
        prepare,
    )
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: source,
    )
    monkeypatch.setattr(
        "astrid.core.rendering.profile.resolve_render_profile",
        lambda *args, **kwargs: SimpleNamespace(width=641, height=359, fps_rational=(30, 1)),
    )

    def query(received, basis, frames):
        assert received is props
        assert basis == {"width": 641, "height": 359, "fps": 30.0}
        assert events == ["lock-enter", "prepare-enter"]
        return [{"frame": frame, "width": 641, "height": 359} for frame in frames]

    monkeypatch.setattr(scene_answers, "host_frames_at", query)
    result = scene_answers._prepared_host_frames_at(
        tmp_path / "timeline.json",
        tmp_path / "assets.json",
        (3, 0, 3),
        staged_video=tmp_path / "unused.mp4",
        provenance_out_path=tmp_path / "provenance.json",
        project_dir=tmp_path / "remotion",
        composition_id="TimelineComposition",
        theme_path=None,
        min_free_gb=None,
        frame_output_dir=tmp_path / "frames",
    )
    assert [row["frame"] for row in result] == [3, 0, 3]
    assert events == ["lock-enter", "prepare-enter", "prepare-exit", "lock-exit"]
