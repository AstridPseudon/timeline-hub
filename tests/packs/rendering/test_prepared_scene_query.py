"""Read-only public queries retain the normal Root inputs until Node returns."""
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.timeline import scene_answers
from astrid.packs.rendering.rendering.renderers.remotion import root_preparation, run
from tests.packs.rendering import test_scene_host as host_fixture
from tests.packs.rendering.test_verified_source import materialize

host_project = host_fixture.host_project
native_host = host_fixture.native_host


@pytest.fixture
def retained(tmp_path, monkeypatch, native_host):
    config = {"tracks": [{"id": "v", "kind": "visual", "label": "Visual"}], "clips": [
        {"id": "opaque:original", "clipType": "text-card", "track": "v", "at": 0, "hold": 1,
         "params": {"content": "Retained title"}},
    ]}
    _, _, _, _, values = materialize(tmp_path, monkeypatch, capture=True, config=config)
    # Environment admission and the unused renderer port are separate boundaries.
    monkeypatch.setattr(run, "_validate_project_dir", lambda project: SimpleNamespace())
    monkeypatch.setattr(run, "_regenerate_element_registries", lambda *args: None)
    monkeypatch.setattr(run, "_available_remotion_port", lambda: 32101)

    def no_audio(*args, **kwargs):
        pytest.fail("a read-only frame query prepared PCM audio")

    monkeypatch.setattr(run, "prepare_normal_audio_sources", no_audio)
    return values, {
        "staged_video": tmp_path / "unused.mp4", "provenance_out_path": tmp_path / "unused.json",
        "project_dir": native_host, "composition_id": run.DEFAULT_COMPOSITION_ID,
        "theme_path": None, "min_free_gb": None, "frame_output_dir": tmp_path / "frames",
    }


def query(retained):
    values, kwargs = retained
    return scene_answers._prepared_host_frames_at(
        Path(values["timeline"]), Path(values["assets_registry"]), (7, 0, 7), **kwargs,
    )


def test_registered_public_query_uses_final_root_and_releases_resources(retained, monkeypatch):
    prepare = root_preparation._prepared_remotion_root
    transport = scene_answers.host_frames_at
    active = []

    @contextmanager
    def observe_root(*args, **kwargs):
        with prepare(*args, **kwargs) as prepared:
            active.append(prepared)
            yield prepared
            active.pop()
        assert not prepared[1].exists()
        assert not prepared[9].exists()

    def observe_query(props, basis, frames):
        assert props is active[0][0] and active[0][1].is_file()
        assert basis == {"width": 1920, "height": 1080, "fps": 30}
        return transport(props, basis, frames)

    monkeypatch.setattr(root_preparation, "_prepared_remotion_root", observe_root)
    monkeypatch.setattr(scene_answers, "host_frames_at", observe_query)
    answers = query(retained)
    assert [answer["frame"] for answer in answers] == [7, 0, 7]
    assert answers[0]["layers"][0]["clipId"] == "opaque:original"
    assert answers[0]["layers"][0]["role"] == "content"
    assert answers[0]["coverage"] == "UNKNOWN"


@pytest.mark.parametrize("damage", ["timeline", "registry", "host", "during-query", "query-error", "basis"])
def test_stale_source_and_query_failures_are_unavailable(retained, monkeypatch, damage):
    values, kwargs = retained
    if damage in {"timeline", "registry"}:
        Path(values["timeline" if damage == "timeline" else "assets_registry"]).write_text("{}")
    elif damage == "host":
        kwargs["project_dir"] = kwargs["project_dir"].parent
    else:
        transport = scene_answers.host_frames_at

        def changed(props, basis, frames):
            answers = transport(props, basis, frames)
            if damage == "during-query":
                Path(values["timeline"]).write_text("{}")
            elif damage == "query-error":
                raise scene_answers.SceneQueryUnavailable("host query failed")
            else:
                answers[0]["width"] += 1
            return answers

        monkeypatch.setattr(scene_answers, "host_frames_at", changed)
    with pytest.raises(scene_answers.SceneQueryUnavailable):
        query(retained)
    assert not kwargs["provenance_out_path"].with_name(".remotion-props.json").exists()
