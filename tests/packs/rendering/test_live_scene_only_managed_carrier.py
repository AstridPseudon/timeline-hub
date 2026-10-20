"""One live managed-carrier proof for the private Scene-only visualization seam."""
from __future__ import annotations

import hashlib
import json
import zipfile
from copy import deepcopy
from pathlib import Path

import pytest

from astrid.sdk import invocation, timeline_filmstrip
from astrid.sdk.remote import RemoteAstridClient
from astrid.sdk.timeline_filmstrip import _invoke_scene_only
from astrid.sdk.workspace_client import WorkspaceClient
from tests.packs.rendering.real_pack_host import start_real_pack_host
from tests.sdk.test_capture_source_runtime import CaptureRuntime
from tests.timeline.test_authoring_bundle import AUDIO, OLD, _closure, _replace_values

pytestmark = pytest.mark.integration


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def _seed(daemon):
    service = daemon.service
    project = service.create_project({"slug": "scene-only-live", "name": "Scene-only live"})["id"]
    service.create_timeline(project, "main", idempotency_key="scene-only-live-timeline")
    replacements = {}
    for old, data in ((OLD, b"scene source"), (AUDIO, b"scene audio")):
        replacements[old] = service.ingest(
            project, data, idempotency_key="scene-only-live-" + old.split(":")[1],
        )["data"]["object_id"]
    parent, shots, internals = (_replace_values(part, replacements) for part in _closure(shared=False))
    for row in (parent, *shots, *internals):
        row["project_id"] = project
    # The live host requires labels on every track; keep this repair local to
    # the private Scene proof fixture rather than changing the shared fixture.
    internal = internals[0]["payload"]
    internal["tracks"][0]["label"] = "Picture"
    internal["tracks"][1]["label"] = "Voice"
    internal["tracks"][0].pop("opaque_track", None)
    for clip in internal["clips"]:
        clip.pop("opaque_clip", None)
        clip.pop("rect", None)
    parent["payload"]["config"]["tracks"][0]["label"] = "Picture"
    shots[0]["payload"]["text_bindings"] = []
    for row in (parent, *shots, *internals):
        row["content_digest"] = _digest(row["payload"])
    published = service.publish_parent_composition(
        project, "main", {
            "project_id": project, "timeline_id": "main", "expected_head": None,
            "parent_revision_id": "scene-parent-1", "parent_composition": parent["payload"],
            "shot_revisions": [{key: row[key] for key in (
                "shot_id", "revision_id", "payload", "content_digest", "internal_timeline_revision_id")}
                for row in shots],
            "internal_timeline_revisions": [{key: row[key] for key in (
                "timeline_id", "revision_id", "payload", "content_digest")}
                for row in internals],
        }, idempotency_key="scene-only-live-publish",
    )
    assert published
    from astrid.sdk.timeline.commit import create_runtime_commit_service
    service.register_timeline_commit_provider(create_runtime_commit_service())
    runtime = CaptureRuntime(service, project)
    runtime.document = {
        "parent_revision": {"revision_id": "scene-parent-1"},
        "shot_revisions": shots, "internal_timeline_revisions": internals,
    }
    runtime.r1 = "scene-parent-1"
    return runtime


class _ManagedCarrier:
    def __init__(self, runtime, daemon, host):
        self.runtime = runtime
        self.service = daemon.service
        self.host = host
        self.project_id = runtime.project_id
        self._remote = RemoteAstridClient(WorkspaceClient(daemon.endpoint, daemon.token))
        self.tasks = self._remote.tasks
        self.media = self._remote.media

    def __getattr__(self, name):
        return getattr(self.runtime, name)

    def _read_bytes(self, object_id):
        return self.service.object(str(object_id).removeprefix("sha256:"))[1]

    def get_run(self, run_id):
        return self.service.run(run_id)

    def get_task(self, task_id):
        return self.service.task(task_id)

    def list_project_runs(self, project_id, **kwargs):
        return self.service.list_project_runs(project_id, **kwargs)


def _candidate_preview(runtime):
    from astrid.core.timeline.authoring_bundle import (
        open_authoring_bundle,
        preview_authoring_candidate,
    )

    service = runtime.service
    parent = runtime.get_project_parent_composition_revision(runtime.project_id, "main", "scene-parent-1")
    shots = [service.get_project_shot_revision(runtime.project_id, row["shot_id"], row["revision_id"])
             for row in runtime.document["shot_revisions"]]
    internals = [service.get_project_timeline_revision(runtime.project_id, "main", row["revision_id"])
                 for row in runtime.document["internal_timeline_revisions"]]
    bundle = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    for clips in (bundle["parent"]["clips"], bundle["parent"]["config"]["clips"]):
        clips[0]["opacity"] = 0.5
    return preview_authoring_candidate(bundle)


def _assert_result(carrier, inputs, *, label, monkeypatch):
    spans, prepared = _invoke_scene_only(inputs, project=carrier.project_id, client=carrier)
    result = carrier._last_result
    artifact_path = __import__("os").environ.get("ASTRID_SCENE_PROOF_ARTIFACT")
    destination = Path(artifact_path) if artifact_path else None
    if destination is not None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.with_name(label + "-receipt.json").write_text(json.dumps({
            "ok": result.ok, "error": result.error, "outputs": result.outputs,
            "raw_result": result.raw_result, "context": prepared,
            "spans": [vars(span) for span in spans],
        }, sort_keys=True, default=str))
        for row in result.outputs.get("managed_outputs", []):
            if row.get("output_port", row.get("name")) == "filmstrip_bundle":
                destination.with_name(label + "-bundle.zip").write_bytes(carrier._read_bytes(row["object_id"]))
    assert spans and spans[0].cls != "UNAVAILABLE", prepared
    assert result.ok, result.error
    rows = result.outputs["managed_outputs"]
    bundle = next(row for row in rows if row.get("output_port", row.get("name")) == "filmstrip_bundle")
    bundle_bytes = carrier._read_bytes(bundle["object_id"])
    with zipfile.ZipFile(__import__("io").BytesIO(bundle_bytes)) as archive:
        assert "scene-answers.json" in archive.namelist()
        assert not any(name.endswith(".png") for name in archive.namelist())
        answers = json.loads(archive.read("scene-answers.json"))
    assert answers["answers"]
    assert bundle["provenance"]["video_digest"] == prepared["capture_identity"]
    assert bundle["provenance"]["timeline_id"] == prepared["timeline_id"]
    if destination is not None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(bundle_bytes)
        destination.with_suffix(".json").write_text(json.dumps({
            "label": label, "video_digest": bundle["provenance"]["video_digest"],
            "timeline_id": bundle["provenance"]["timeline_id"],
            "bundle_digest": bundle["digest"], "answers": len(answers["answers"]),
        }, sort_keys=True) + "\n")
    return spans, prepared, result


@pytest.mark.timeout(180)
def test_live_managed_scene_only_saved_candidate_and_stale(real_runtime, tmp_path, monkeypatch):
    daemon = real_runtime()
    daemon.support_root.chmod(0o700)
    source = Path(__file__).resolve().parents[3]
    discovery = daemon.support_root / "discovery.json"
    value = json.loads(discovery.read_text(encoding="utf-8"))
    with start_real_pack_host(
        realm_dir=daemon.root, support_dir=daemon.support_root, discovery_file=discovery,
        source_checkout=source, runtime_instance_id=value["runtime_instance_id"],
    ) as host:
        runtime = _seed(daemon)
        carrier = _ManagedCarrier(runtime, daemon, host)
        saved_inputs = {"timeline_ref": "main", "revision_id": "scene-parent-1"}
        carrier._last_result = None
        original_invoke = invocation._invoke_internal_result
        def invoke(*args, **kwargs):
            result = original_invoke(*args, **kwargs)
            carrier._last_result = result
            return result
        monkeypatch.setattr(invocation, "_invoke_internal_result", invoke)
        spans, prepared, result = _assert_result(carrier, saved_inputs, label="saved", monkeypatch=monkeypatch)

        candidate_preview = _candidate_preview(runtime)
        candidate_inputs = {"timeline_ref": "main", "authoring_preview": candidate_preview}
        _assert_result(carrier, candidate_inputs, label="candidate", monkeypatch=monkeypatch)

        stale = deepcopy(prepared)
        stale["timeline_id"] = "stale-timeline"
        stale["capture_snapshot"]["timeline_id"] = "stale-timeline"
        stale_spans = timeline_filmstrip._scene_only_spans(result, stale, client=carrier)
        assert stale_spans[0].cls == "UNAVAILABLE"
        assert "stale scene source" in stale_spans[0].findings
