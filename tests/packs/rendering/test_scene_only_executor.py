"""Private Scene-only visualization reuses the managed filmstrip artifact."""

import json
import zipfile
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

from astrid.core.timeline import scene_answers
from astrid.sdk import timeline_filmstrip
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
    capture_identity = "sha256:" + "a" * 64
    return {
        "mode": "scene_only",
        "capture_identity": capture_identity,
        "capture_snapshot": {
            "project_slug": "demo",
            "timeline_id": "timeline",
            "render_run_id": "capture:timeline:revision",
            "duration_frames": 4,
            "config": {"tracks": [], "clips": [{"id": "compiled:clip"}]},
            "registry": {"assets": {}},
            "metadata": {
                "capture_identity": capture_identity,
                "capture_authority": {"parent_revision_id": "revision"},
                "scene_clips": {"compiled:clip": {"address": "c01.layer"}},
            },
        },
    }


class _Source:
    def __init__(self, snapshot):
        self.snapshot = snapshot

    def validate_snapshot(self, snapshot):
        assert snapshot == self.snapshot

    def read(self):
        return {"snapshot": self.snapshot}


def test_scene_only_writes_no_png_and_binds_receipt_to_capture(tmp_path, monkeypatch):
    args = _args(tmp_path)
    authority = _authority()
    source = _Source(authority["capture_snapshot"])
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: source,
    )
    monkeypatch.setattr(
        filmstrip_execution,
        "snapshot_label",
        lambda snapshot, *, source: {
            "status": "committed", "label": "committed revision revision",
            "actual_revision_id": "revision", "base_revision_id": None,
        },
    )
    monkeypatch.setattr(
        scene_answers,
        "_prepared_host_frames_at",
        lambda timeline, assets, frames, **kwargs: [
            {
                "frame": frame,
                "width": 1920,
                "height": 1080,
                "coverage": "COVERED",
                "content": "CONTENT",
                "layers": [{"clipId": "compiled:clip"}],
                "findings": [],
            }
            for frame in frames
        ],
    )

    result = filmstrip_execution.execute_filmstrip(args, authority=authority)

    payload = json.loads(Path(result["outputs"]["scene_answers"]).read_text(encoding="utf-8"))
    assert [answer["frame"] for answer in payload["answers"]] == [0, 1, 2, 3]
    assert payload["scene_clips"] == {"compiled:clip": {"address": "c01.layer"}}
    assert not list((args.out / "filmstrip-view").glob("*.png"))
    host_manifest = json.loads((args.out / "manifest.json").read_text(encoding="utf-8"))
    bundle = next(row for row in host_manifest["outputs"] if row["name"] == "filmstrip_bundle")
    assert bundle["provenance"] == {
        "video_digest": "sha256:" + "a" * 64, "timeline_id": "timeline",
    }
    with zipfile.ZipFile(result["outputs"]["filmstrip_bundle"]) as archive:
        assert archive.namelist() == ["manifest.json", "scene-answers.json"]
    bundle_bytes = Path(result["outputs"]["filmstrip_bundle"]).read_bytes()
    sdk_context = {
        **authority,
        "mode": "composed_capture",
        "scene_only": True,
        "video_digest": "sha256:" + "b" * 64,
        "video_object_id": "sha256:" + "b" * 64,
        "managed_object_reference": "sha256:" + "b" * 64,
    }
    sdk_result = {
        "ok": True,
        "outputs": {
            "managed_outputs": [{
                "output_port": "filmstrip_bundle",
                "role": "result",
                "digest": bundle["content_hash"],
                "size": len(bundle_bytes),
                "provenance": bundle["provenance"],
            }],
        },
    }
    assert timeline_filmstrip._scene_only_authority(sdk_context) is not None
    bundle_source = timeline_filmstrip._scene_only_bundle_payload(
        sdk_result,
        client=SimpleNamespace(media=SimpleNamespace(read_bytes=lambda _: bundle_bytes)),
    )
    assert bundle_source is not None
    assert bundle_source[0]["snapshot_label"] == timeline_filmstrip._scene_only_authority(sdk_context)["snapshot_label"]
    spans = timeline_filmstrip._scene_only_spans(
        sdk_result,
        sdk_context,
        client=SimpleNamespace(media=SimpleNamespace(read_bytes=lambda _: bundle_bytes)),
    )
    assert [(item.start_frame, item.end_frame, item.cls, item.clips) for item in spans] == [
        (0, 4, "COVERED", ("c01.layer",)),
    ], spans[0].findings


def test_scene_only_failure_is_advisory_and_has_no_partial_answers(tmp_path, monkeypatch):
    args = _args(tmp_path)
    monkeypatch.setattr(
        "astrid.core.rendering.verified_source.inherited_source",
        lambda timeline, assets: None,
    )

    result = filmstrip_execution.execute_filmstrip(args, authority=_authority())

    payload = json.loads(Path(result["outputs"]["scene_answers"]).read_text(encoding="utf-8"))
    assert result["returncode"] == 0
    assert payload["answers"] == []
    assert payload["scene_clips"] == {}
    assert payload["snapshot_label"]["status"] == "unavailable"
