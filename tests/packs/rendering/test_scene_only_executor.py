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


def _authority() -> dict:
    return {
        "mode": "scene_only",
        "capture_snapshot": {
            "project_slug": "demo",
            "timeline_id": "timeline",
            "render_run_id": "capture:timeline:revision",
            "duration_frames": 4,
            "config": {"tracks": [], "clips": [{"id": "compiled:clip"}]},
            "registry": {"assets": {}},
            "metadata": {
                "capture_authority": {"parent_revision_id": "revision"},
                "scene_clips": {"compiled:clip": {"address": "c01.layer"}},
            },
        },
    }


class _Source:
    def __init__(self, *, stale: bool = False):
        self.stale = stale
        self.validations = []

    def validate_snapshot(self, snapshot):
        self.validations.append("snapshot")
        if self.stale:
            raise ValueError("capture source differs")

    def read(self):
        return {"snapshot": _authority()["capture_snapshot"]}


def test_scene_only_queries_full_extent_and_uses_existing_bundle(tmp_path, monkeypatch):
    args = _args(tmp_path)
    source = _Source()
    calls = []
    label_sources = []

    def unexpected_render(*args, **kwargs):
        pytest.fail("scene-only execution must not invoke filmstrip rendering")

    monkeypatch.setattr(filmstrip_execution, "_render_input_projection_png", unexpected_render)
    monkeypatch.setattr(filmstrip_execution, "_render_paired_rows", unexpected_render)
    monkeypatch.setattr(filmstrip_execution, "_render_time_anchored_output", unexpected_render)
    monkeypatch.setattr(
        filmstrip_execution,
        "snapshot_label",
        lambda snapshot, *, source=None: label_sources.append(source) or {
            "status": "uncertified",
            "label": "uncertified",
            "actual_revision_id": None,
            "base_revision_id": None,
        },
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
    result = filmstrip_execution.execute_filmstrip(args, authority=_authority())

    assert result["returncode"] == 0
    assert calls[0][2] == (0, 1, 2, 3)
    scene_path = Path(result["outputs"]["scene_answers"])
    payload = json.loads(scene_path.read_text(encoding="utf-8"))
    assert [answer["frame"] for answer in payload["answers"]] == [0, 1, 2, 3]
    assert payload["scene_clips"] == {"compiled:clip": {"address": "c01.layer"}}
    assert payload["snapshot_label"]["status"] == "uncertified"
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
