"""The scene-only artifact is the managed filmstrip result, not a caller payload."""

from __future__ import annotations

import copy
import json
import os
import shutil
import zipfile
from argparse import Namespace
from pathlib import Path

from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.rendering.verified_source import mint_prepared_source
from astrid.core.timeline import Timeline, scene_answers
from astrid.core.timeline.authoring_bundle import (
    _digest,
    open_authoring_bundle,
    preview_authoring_candidate,
)
from astrid.packs.rendering.actions.render import managed_timeline
from astrid.packs.rendering.actions.timeline_visualize import filmstrip_execution
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion_run
from astrid.sdk.timeline_filmstrip import prepare_filmstrip
from tests.packs.rendering.test_scene_answers import ROOT as AGENT_ROOT
from tests.packs.rendering.test_scene_answers import _real_runtime_tools
from tests.packs.rendering.test_scene_source_carry import Revisions

pytest_plugins = ("tests.packs.rendering.test_scene_host",)


class _TinyRevisions(Revisions):
    """Use the real closure/projector with a six-frame source, not a large blob."""

    def get_project_parent_composition_revision(self, project, timeline, revision):
        value = super().get_project_parent_composition_revision(project, timeline, revision)
        for index, occurrence in enumerate(value["payload"]["occurrences"]):
            occurrence["at_ms"] = index * 125
            occurrence["duration_ms"] = 125
        value["content_digest"] = _digest(value["payload"])
        return value


def _candidate_preview(client: _TinyRevisions) -> dict:
    parent = client.get_project_parent_composition_revision("p", "tl", "parent:old")
    shot = client.get_project_shot_revision("p", "s", "shot:old")
    shot["project_id"] = "p"
    internal = copy.deepcopy(client.internal)
    internal["payload"]["clips"] = internal["payload"]["clips"][:1]
    for row in (parent, shot, internal):
        row["content_digest"] = _digest(row["payload"])
    bundle = open_authoring_bundle(
        parent, shot_revisions=[shot], internal_timeline_revisions=[internal],
    )
    for value in bundle["shots"].values():
        value["internal_timeline"]["clips"][0]["params"]["content"] = "Unpublished title"
    return preview_authoring_candidate(bundle)


def _source_for(snapshot, timeline: Path, assets: Path, attempt: Path):
    # The fixture's admission seam supplies the project identity that the
    # Runtime normally carries beside the existing capture authority.
    authority = {"project_id": "p", **snapshot["metadata"]["capture_authority"]}
    working = snapshot["metadata"].get("working_copy")
    if isinstance(working, dict):
        base = working["base_parent"]
        ref = {
            "source_kind": "working_copy",
            "project_id": "p",
            "timeline_id": "tl",
            "revision_id": working["candidate_parent_revision_id"],
            "revision_digest": working["candidate_digest"],
            "working_copy": {
                "candidate_digest": working["candidate_digest"],
                "publication_digest": working["publication_digest"],
                "base_revision_id": base["revision_id"],
                "base_revision_digest": base["content_digest"],
            },
        }
    else:
        ref = {
            "source_kind": "revision",
            "project_id": "p",
            "timeline_id": "tl",
            "revision_id": authority["parent_revision_id"],
            "revision_digest": authority["parent_content_digest"],
        }
    return mint_prepared_source(
        ref=ref,
        authority=authority,
        snapshot=snapshot,
        timeline_path=timeline,
        assets_path=assets,
        attempt=attempt,
    )


def _args(tmp_path, timeline: Path, assets: Path) -> Namespace:
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


def _save_example(root: Path | None, name: str, result: dict, payload: dict) -> None:
    """Optionally retain only the bounded artifact/result, never its snapshot inputs."""
    if root is None:
        return
    root.mkdir(parents=True, exist_ok=True)
    (root / f"{name}-scene-answers.json").write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")), encoding="utf-8",
    )
    shutil.copyfile(result["outputs"]["filmstrip_bundle"], root / f"{name}-filmstrip-bundle.zip")
    output_root = Path(result["run_root"])
    for suffix, path in (
        ("managed-manifest.json", output_root / "manifest.json"),
        ("nested-manifest.json", output_root / "filmstrip-view" / "manifest.json"),
    ):
        shutil.copyfile(path, root / f"{name}-{suffix}")


def test_scene_only_bundle_is_real_node_artifact_for_saved_candidate_and_unavailable(
    native_host, host_project, tmp_path, monkeypatch,
):
    """Exercise producer -> Root source -> public Node rows -> bundle entrypoint.

    ``native_host`` supplies the pinned public12 evaluator and Node. Runtime
    admission is the existing fixture seam, so this is UNIT-REAL-NODE evidence,
    not live Runtime or ordinary SDK qualification.
    """
    monkeypatch.setattr(managed_timeline, "_runtime_snapshot_registry", lambda registry, **kwargs: registry)
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(native_host))
    monkeypatch.setattr(remotion_run, "_available_remotion_port", lambda: 32101)
    node = resolve_pinned_node(AGENT_ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok and node.version == "v20.19.4"
    monkeypatch.setattr(remotion_run, "_validate_project_dir", lambda _: _real_runtime_tools(native_host, node))
    examples = os.environ.get("ASTRID_SCENE_ARTIFACT_EXAMPLES")
    example_root = Path(examples).resolve() if examples else None

    client = _TinyRevisions()
    candidate = _candidate_preview(client)
    cases = [
        (
            "saved",
            prepare_filmstrip(
                {"composed_capture": True, "timeline_ref": "tl", "revision_id": "parent:old"},
                project="demo", client=client,
            )["capture_snapshot"],
        ),
        (
            "candidate",
            prepare_filmstrip(
                {"composed_capture": True, "timeline_ref": "tl", "authoring_preview": candidate},
                project="demo", client=client,
            )["capture_snapshot"],
        ),
    ]

    for label, snapshot in cases:
        assert 3 <= snapshot["duration_frames"] <= 6
        attempt = tmp_path / label / "attempt"
        attempt.mkdir(parents=True)
        (attempt / "inputs").mkdir()
        timeline = attempt / "timeline.json"
        assets = attempt / "assets.json"
        Timeline.from_config(snapshot["config"]).dump(timeline)
        assets.write_text(json.dumps(snapshot["registry"]), encoding="utf-8")
        source = _source_for(snapshot, timeline, assets, attempt)
        monkeypatch.setenv("ASTRID_VERIFIED_TIMELINE_SOURCE", source._anchor)

        result = filmstrip_execution.execute_filmstrip(
            _args(tmp_path / label, timeline, assets),
            authority={"mode": "scene_only", "capture_snapshot": snapshot},
        )
        assert result["returncode"] == 0
        scene_path = Path(result["outputs"]["scene_answers"])
        payload = json.loads(scene_path.read_text(encoding="utf-8"))
        assert payload["snapshot_label"]["status"] == ("candidate" if label == "candidate" else "committed")
        assert [row["frame"] for row in payload["answers"]] == list(range(snapshot["duration_frames"]))
        assert set(payload["scene_clips"]) == {clip["id"] for clip in snapshot["config"]["clips"]}
        assert payload["snapshot_label"]["label"]
        assert all(
            layer["clipId"] in payload["scene_clips"]
            for answer in payload["answers"]
            for layer in answer["layers"]
        )
        assert not any("synthetic" in json.dumps(row).lower() for row in payload["answers"])

        with zipfile.ZipFile(result["outputs"]["filmstrip_bundle"]) as bundle:
            assert bundle.namelist() == ["manifest.json", "scene-answers.json"]
            nested = json.loads(bundle.read("manifest.json"))
            assert nested["entrypoints"]["scene"] == "scene-answers.json"
            assert json.loads(bundle.read(nested["entrypoints"]["scene"])) == payload
        host_manifest = json.loads((Path(result["run_root"]) / "manifest.json").read_text())
        bundle_entry = next(row for row in host_manifest["outputs"] if row["name"] == "filmstrip_bundle")
        assert bundle_entry["path"] == "filmstrip-bundle.zip"
        assert host_manifest["entrypoints"]["bundle"] == bundle_entry["path"]
        _save_example(example_root, label, result, payload)

    stale_snapshot = copy.deepcopy(cases[0][1])
    stale_snapshot["metadata"]["capture_authority"]["parent_revision_id"] = "stale"
    stale_attempt = tmp_path / "stale" / "attempt"
    stale_attempt.mkdir(parents=True)
    (stale_attempt / "inputs").mkdir()
    timeline = stale_attempt / "timeline.json"
    assets = stale_attempt / "assets.json"
    Timeline.from_config(stale_snapshot["config"]).dump(timeline)
    assets.write_text(json.dumps(stale_snapshot["registry"]), encoding="utf-8")
    stale_source = _source_for(cases[0][1], timeline, assets, stale_attempt)
    monkeypatch.setenv("ASTRID_VERIFIED_TIMELINE_SOURCE", stale_source._anchor)
    stale_result = filmstrip_execution.execute_filmstrip(
        _args(tmp_path / "stale", timeline, assets),
        authority={"mode": "scene_only", "capture_snapshot": stale_snapshot},
    )
    stale_payload = json.loads(Path(stale_result["outputs"]["scene_answers"]).read_text())
    assert stale_payload == {
        "answers": [],
        "scene_clips": {},
        "snapshot_label": {
            "status": "unavailable", "label": "revision unavailable",
            "actual_revision_id": None, "base_revision_id": None,
        },
    }
    _save_example(example_root, "stale", stale_result, stale_payload)

    monkeypatch.setattr(scene_answers, "_prepared_host_frames_at", lambda *args, **kwargs: (_ for _ in ()).throw(
        scene_answers.SceneQueryUnavailable("Node unavailable"),
    ))
    unavailable_result = filmstrip_execution.execute_filmstrip(
        _args(tmp_path / "unavailable", timeline, assets),
        authority={"mode": "scene_only", "capture_snapshot": cases[0][1]},
    )
    unavailable_payload = json.loads(
        Path(unavailable_result["outputs"]["scene_answers"]).read_text(),
    )
    assert unavailable_payload["snapshot_label"]["status"] == "unavailable"
    assert unavailable_payload["answers"] == [] and unavailable_payload["scene_clips"] == {}
    _save_example(example_root, "unavailable", unavailable_result, unavailable_payload)
    if example_root is not None:
        (example_root / "manifest.json").write_text(
            json.dumps(
                {
                    "artifact": "filmstrip_bundle",
                    "entrypoint": "filmstrip-view/scene-answers.json",
                    "examples": {
                        name: {
                            "scene_answers": f"{name}-scene-answers.json",
                            "bundle": f"{name}-filmstrip-bundle.zip",
                            "status": status,
                        }
                        for name, status in (
                            ("saved", "committed"),
                            ("candidate", "candidate"),
                            ("stale", "unavailable"),
                            ("unavailable", "unavailable"),
                        )
                    },
                },
                sort_keys=True,
                indent=2,
            ),
            encoding="utf-8",
        )
