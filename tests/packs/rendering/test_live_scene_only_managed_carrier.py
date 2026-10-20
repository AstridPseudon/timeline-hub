"""One live managed-carrier proof for the private Scene-only visualization seam."""
from __future__ import annotations

import hashlib
import json
import time
import zipfile
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.sdk import timeline_filmstrip
from astrid.sdk.timeline_filmstrip import _invoke_scene_only, prepare_filmstrip
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
        self.media = SimpleNamespace(list=runtime.media_list, read_bytes=self._read_bytes)
        self._remote = SimpleNamespace(_transport=self)

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

    def invoke_result(self, capability_id, *, kind, project, inputs, wait=True,
                      read_managed_outputs=True, **_kwargs):
        assert capability_id == "rendering.timeline_visualize" and kind == "executor"
        assert inputs["mode"] == "scene_only"
        assert inputs["view"] == "filmstrip"
        assert inputs["formats"] == ["md"]
        authority = dict(inputs)
        authority["mode"] = "scene_only"
        prepared = self._prepared
        snapshot = deepcopy(prepared["capture_snapshot"])
        snapshot["project_slug"] = self.service.get_project(project)["slug"]
        context = {
            "mode": "scene_only", "project_id": project,
            "project_slug": self.service.get_project(project)["slug"],
            "timeline_id": prepared["timeline_id"],
            "capture_identity": prepared["capture_identity"],
            "video_digest": prepared["capture_identity"],
            "video_object_id": prepared["capture_identity"],
            "managed_object_reference": prepared["capture_identity"],
            "capture_snapshot": snapshot,
        }
        body = {
            "project": project, "capability_id": capability_id,
            "capability_digest": self._capability_digest(capability_id),
            "input_object_ids": [row["object_id"] for row in self.runtime.media_list(project)[0]],
            "idempotency_key": "scene-only-live-" + str(time.time_ns()),
            "spec": {"inputs": {"filmstrip_authority": json.dumps(context)},
                     "authority_context": context},
        }
        created = self.service.create_task(body, enforce_readiness=True)
        task = created.get("task", created)
        task_id = str(task.get("id") or task.get("task_id"))
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            observed = self.service.task(task_id)
            state = str(observed.get("state") or observed.get("status") or "")
            if state in {"completed", "succeeded", "failed", "cancelled"}:
                rows = self.service.managed_outputs(task_id)
                return {"ok": state in {"completed", "succeeded"},
                        "outputs": {"managed_outputs": rows}, "task": observed}
            time.sleep(0.1)
        raise AssertionError(f"managed scene task did not settle: {task_id}")

    def _capability_digest(self, capability_id):
        rows = self.service.list_capabilities()
        for row in rows.get("items", rows.get("rows", [])):
            if row["capability_id"] == capability_id:
                return row["definition_digest"]
        row = self.service.store.conn.execute(
            "SELECT definition_digest FROM capabilities WHERE id=?", (capability_id,)
        ).fetchone()
        if row:
            return str(row["definition_digest"])
        raise AssertionError(f"host did not register {capability_id}")


def _candidate_preview(runtime):
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle, preview_authoring_candidate

    service = runtime.service
    parent = runtime.get_project_parent_composition_revision(runtime.project_id, "main", "scene-parent-1")
    shots = [service.get_project_shot_revision(runtime.project_id, row["shot_id"], row["revision_id"])
             for row in runtime.document["shot_revisions"]]
    internals = [service.get_project_timeline_revision(runtime.project_id, "main", row["revision_id"])
                 for row in runtime.document["internal_timeline_revisions"]]
    bundle = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    bundle["parent"]["config"]["output"]["file"] = "scene-candidate.mp4"
    return preview_authoring_candidate(bundle)


def _assert_result(carrier, context, *, label, monkeypatch):
    carrier._prepared = context
    monkeypatch.setattr(timeline_filmstrip, "prepare_filmstrip", lambda *_a, **_k: context)
    spans, prepared = _invoke_scene_only({"timeline_ref": "main"}, project=carrier.project_id, client=carrier)
    assert spans and spans[0].cls != "UNAVAILABLE", prepared
    result = carrier._last_result
    rows = result["outputs"]["managed_outputs"]
    bundle = next(row for row in rows if row.get("output_port", row.get("name")) == "filmstrip_bundle")
    bundle_bytes = carrier._read_bytes(bundle["object_id"])
    with zipfile.ZipFile(__import__("io").BytesIO(bundle_bytes)) as archive:
        assert "scene-answers.json" in archive.namelist()
        assert not any(name.endswith(".png") for name in archive.namelist())
        answers = json.loads(archive.read("scene-answers.json"))
    assert answers["answers"]
    assert bundle["provenance"]["video_digest"] == prepared["capture_identity"]
    assert bundle["provenance"]["timeline_id"] == prepared["timeline_id"]
    destination = Path(__import__("os").environ.get("ASTRID_SCENE_PROOF_ARTIFACT", ""))
    if destination:
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
        saved_inputs = {"timeline_ref": "main"}
        saved_request = prepare_filmstrip({**saved_inputs, "composed_capture": True},
                                          project=runtime.project_id, client=runtime)
        saved_request.update({
            "video_digest": saved_request["capture_identity"],
            "video_object_id": saved_request["capture_identity"],
            "managed_object_reference": saved_request["capture_identity"],
            "timeline_id": saved_request["timeline_id"],
        })
        carrier._last_result = None
        original_invoke = carrier.invoke_result
        def invoke(*args, **kwargs):
            result = original_invoke(*args, **kwargs)
            carrier._last_result = result
            return result
        carrier.invoke_result = invoke
        spans, prepared, result = _assert_result(carrier, saved_request, label="saved", monkeypatch=monkeypatch)

        candidate_preview = _candidate_preview(runtime)
        candidate_request = prepare_filmstrip(
            {"timeline_ref": "main", "authoring_preview": candidate_preview,
             "composed_capture": True}, project=runtime.project_id, client=runtime,
        )
        candidate_request.update({
            "video_digest": candidate_request["capture_identity"],
            "video_object_id": candidate_request["capture_identity"],
            "managed_object_reference": candidate_request["capture_identity"],
            "timeline_id": candidate_request["timeline_id"],
        })
        _assert_result(carrier, candidate_request, label="candidate", monkeypatch=monkeypatch)

        stale = deepcopy(saved_request)
        stale["timeline_id"] = "stale-timeline"
        stale_spans = timeline_filmstrip._scene_only_spans(result, stale, client=carrier)
        assert stale_spans[0].cls == "UNAVAILABLE"
        assert "stale scene source" in stale_spans[0].findings
