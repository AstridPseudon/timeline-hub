from __future__ import annotations

import json
from pathlib import Path

import pytest

from astrid.core._shared.result_manifest import harvest_staged_outputs
from astrid.packs.timeline.actions._common import decode_manifest
from astrid.packs.timeline.actions._common import open_worker_runtime_client
from astrid.packs.timeline.actions.export_plan.run import _summary, build_export_plan_artifacts
from astrid.packs.timeline.actions.prepare_import.run import build_prepare_import_artifacts


def _empty_source() -> dict:
    return json.loads((Path(__file__).parents[2] / "editing_scenarios" / "fixtures" / "empty.json").read_text())


def _manifest(source: dict) -> dict:
    from astrid.sdk.timeline_export import inventory_elements

    return {"format": "astrid.timeline/1", "name": "Fixture", "elements": inventory_elements(source)}


def test_manifest_json_and_file_fallback_are_exclusive_and_bounded(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text('{"format":"astrid.timeline/1"}', encoding="utf-8")
    assert decode_manifest(None, str(path))["format"] == "astrid.timeline/1"
    assert decode_manifest('{"format":"astrid.timeline/1"}', None)["format"] == "astrid.timeline/1"
    with pytest.raises(ValueError, match="exactly one"):
        decode_manifest(None, None)
    with pytest.raises(ValueError, match="exactly one"):
        decode_manifest("{}", str(path))
    with pytest.raises(ValueError, match="manifest_file"):
        decode_manifest(json.dumps({"data": "x" * (256 * 1024)}), None)


def test_check_only_stages_summary_without_prepared_body_or_target_id(tmp_path):
    summary = build_prepare_import_artifacts(
        project="target-project",
        out_dir=tmp_path / "out",
        manifest_json=json.dumps(_manifest(_empty_source())),
        check_only=True,
    )
    assert summary == {
        "check_only": True,
        "name": "Fixture",
        "missing_effects": [],
        "different_effects": [],
    }
    root = tmp_path / "out"
    assert not (root / "prepared.json").exists()
    outputs = json.loads((root / "manifest.json").read_text(encoding="utf-8"))["outputs"]
    assert [row["name"] for row in outputs] == ["result"]
    assert json.loads((root / outputs[0]["path"]).read_text(encoding="utf-8")) == summary


def test_prepare_action_stages_complete_commit_body_and_small_summary(tmp_path):
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps({"timeline": _empty_source(), "transcripts": {}}), encoding="utf-8")
    summary = build_prepare_import_artifacts(
        project="target-project",
        out_dir=tmp_path / "out",
        manifest_json=json.dumps(_manifest(_empty_source())),
        payload_file=str(payload),
    )
    root = tmp_path / "out"
    prepared = json.loads((root / "prepared.json").read_text(encoding="utf-8"))
    assert prepared["publication"]["project_id"] == "target-project"
    assert prepared["timeline_id"] == summary["timeline_id"]
    assert summary["check_only"] is False
    assert summary["shot_count"] >= 1
    outputs = json.loads((root / "manifest.json").read_text(encoding="utf-8"))["outputs"]
    assert [row["name"] for row in outputs] == ["prepared", "result"]


def test_export_summary_is_small_and_uses_plan_metadata():
    summary = _summary({
        "manifest": {"name": "Saved edit"},
        "timeline": {"timeline_id": "target"},
        "media": [{"size": 13}, {"size": 7}],
        "transcripts": {"transcripts/a.json": {}, "transcripts/b.json": {}},
    })
    assert summary == {
        "name": "Saved edit", "media_count": 2, "media_bytes": 20, "transcript_count": 2,
    }


def test_action_client_requires_the_explicit_host_runtime_context(monkeypatch):
    from astrid.sdk import autobootstrap
    from astrid.sdk.workspace_client import WorkspaceClientError

    monkeypatch.delenv("ASTRID_RUNTIME_ENDPOINT", raising=False)
    monkeypatch.delenv("ASTRID_RUNTIME_CREDENTIAL", raising=False)
    calls = []
    monkeypatch.setattr(autobootstrap, "ensure_runtime", lambda **_kwargs: calls.append("launcher"))
    with pytest.raises(WorkspaceClientError, match="runtime endpoint"):
        open_worker_runtime_client()
    assert calls == []


def test_action_client_uses_the_host_worker_connection_for_runtime_reads(monkeypatch):
    import astrid.sdk.workspace_client as workspace_client

    monkeypatch.setenv("ASTRID_RUNTIME_ENDPOINT", "http://127.0.0.1:17341")
    monkeypatch.setenv("ASTRID_RUNTIME_CREDENTIAL", "host-issued-worker-token")
    calls = []

    class FakeWorkspaceClient:
        def __init__(self, endpoint, token):
            self.endpoint, self.token = endpoint, token

        def list_projects(self, *, cursor=None, limit=50):
            calls.append(("list_projects", cursor, limit))
            return {"items": [{"project_id": "target-project"}], "next_cursor": None}

    monkeypatch.setattr(workspace_client, "WorkspaceClient", FakeWorkspaceClient)
    client = open_worker_runtime_client()
    result = client.projects.list()
    assert result.ok and result.data["items"] == [{"project_id": "target-project"}]
    assert client._transport.endpoint == "http://127.0.0.1:17341"
    assert client._transport.token == "host-issued-worker-token"
    assert calls == [("list_projects", None, 50)]


def test_transfer_action_receipts_harvest_every_staged_json_output(tmp_path, monkeypatch):
    """Exercise each action receipt through Runtime's actual output harvester."""
    from astrid.core.execution.generic_host import GenericPackHost
    from astrid.packs.timeline.actions.export_plan import run as export_action

    pack_root = Path(__file__).resolve().parents[3] / "astrid" / "packs" / "timeline"
    host = GenericPackHost(pack_roots=[pack_root])
    records = {record.id: record for record in host.discover()}

    def harvest(capability_id, output_root):
        record = records[capability_id]
        descriptors = harvest_staged_outputs(
            output_root,
            definition=record.definition,
            declared_outputs=record.definition.outputs,
            require=True,
        )
        return host._typed_outputs(record, descriptors, tmp_path)

    monkeypatch.setattr(
        export_action,
        "export_plan",
        lambda *_args: {
            "manifest": {"name": "Saved edit"},
            "timeline": {"timeline_id": "main"},
            "media": [{"size": 13}],
            "transcripts": {"transcripts/one.json": {}},
        },
    )

    export_root = tmp_path / "export"
    build_export_plan_artifacts(object(), "source-project", "main", export_root)
    exported = harvest("timeline.export_plan", export_root)
    assert {item["name"]: item["artifact_type"] for item in exported} == {
        "plan": "timeline/export-plan",
        "result": "application/json",
    }
    export_json = {
        item["name"]: json.loads(Path(item["path"]).read_text(encoding="utf-8"))
        for item in exported
    }
    assert export_json["plan"]["manifest"]["name"] == "Saved edit"
    assert export_json["result"]["media_bytes"] == 13

    manifest_json = json.dumps(_manifest(_empty_source()))
    check_root = tmp_path / "check-only"
    build_prepare_import_artifacts(
        project="target-project", out_dir=check_root, manifest_json=manifest_json, check_only=True,
    )
    checked = harvest("timeline.prepare_import", check_root)
    assert [(item["name"], item["artifact_type"]) for item in checked] == [
        ("result", "application/json"),
    ]
    assert json.loads(Path(checked[0]["path"]).read_text(encoding="utf-8"))["check_only"] is True

    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps({"timeline": _empty_source(), "transcripts": {}}), encoding="utf-8")
    prepare_root = tmp_path / "prepare"
    build_prepare_import_artifacts(
        project="target-project", out_dir=prepare_root, manifest_json=manifest_json,
        payload_file=str(payload_path),
    )
    prepared = harvest("timeline.prepare_import", prepare_root)
    assert {item["name"]: item["artifact_type"] for item in prepared} == {
        "prepared": "timeline/prepared-import",
        "result": "application/json",
    }
    prepare_json = {
        item["name"]: json.loads(Path(item["path"]).read_text(encoding="utf-8"))
        for item in prepared
    }
    assert prepare_json["prepared"]["publication"]["project_id"] == "target-project"
    assert prepare_json["result"]["timeline_id"] == prepare_json["prepared"]["timeline_id"]


@pytest.mark.integration
def test_real_pack_host_invokes_timeline_transfer_actions_read_only(tmp_path, real_runtime, monkeypatch):
    """Discover and execute all action modes through the real Runtime/pack host."""
    from tests.timeline.test_authoring_bundle import AUDIO, OLD, _closure, _digest, _replace_values

    from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
    from astrid.sdk import AstridClient, observe_task_invocation

    pack_root = Path(__file__).resolve().parents[3] / "astrid" / "packs" / "timeline"
    daemon = real_runtime()
    host = GenericPackHost(
        pack_roots=[pack_root],
        client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
        executor_id="astrid-pack-host",
        attempt_base=tmp_path / "attempts",
    )
    host.discover()
    host.preflight("timeline.export_plan")
    host.preflight("timeline.prepare_import")
    host.register(deliberate=True)
    service = daemon.service

    with AstridClient.open(
        endpoint=daemon.endpoint,
        credential=daemon.credential_path,
        realm_id=service.realm["id"],
        actor_id="owner",
        client_name="timeline-transfer-action-test",
        client_version="stage1",
        protocol_version="workspace.v1",
    ) as client:
        try:
            created = client.projects.create(
                slug="timeline-action-test", name="Timeline Action Test", idempotency_key="timeline-action-project",
            )
            assert created.ok, created.error
            project = created.data["project_id"]
            created_timeline = client.timelines.create_empty(
                project=project, timeline_id="main", config={"tracks": []},
                idempotency_key="timeline-action-timeline",
            )
            assert created_timeline.ok, created_timeline.error

            image_id = service.ingest(project, b"timeline-action-picture", media_type="image/png", idempotency_key="timeline-action-image")["data"]["object_id"]
            audio_id = service.ingest(project, b"timeline-action-audio", media_type="audio/wav", idempotency_key="timeline-action-audio")["data"]["object_id"]
            parent, shots, internals = _closure(shared=True)
            service.create_project_shot(project, {"shot_id": shots[0]["shot_id"], "name": "Opening"}, idempotency_key="timeline-action-shot")
            binding_text = "Narration"
            binding = service.set_project_shot_text_binding(project, {
                "shot_id": shots[0]["shot_id"], "kind": "voiceover_script", "text": binding_text,
                "expected_head": 0,
            }, idempotency_key="timeline-action-binding")["data"]
            shots[0]["payload"]["text_bindings"] = [{**binding, "text": binding_text}]
            replacements = {OLD: image_id, AUDIO: audio_id, "project-1": project}
            parent = _replace_values(parent, replacements)
            shots = _replace_values(shots, replacements)
            internals = _replace_values(internals, replacements)
            parent["content_digest"] = _digest(parent["payload"])
            shots[0]["content_digest"] = _digest(shots[0]["payload"])
            internals[0]["content_digest"] = _digest(internals[0]["payload"])
            current = next(
                (row for row in service.list_project_parent_composition_revisions(project, "main")["items"]
                 if row.get("is_current_head")),
                None,
            )
            service.publish_parent_composition(project, "main", {
                "project_id": project,
                "timeline_id": "main",
                "expected_head": current["revision_id"] if current else None,
                "parent_revision_id": "timeline-action-parent",
                "parent_composition": parent["payload"],
                "shot_revisions": shots,
                "internal_timeline_revisions": internals,
            }, idempotency_key="timeline-action-publish")

            payload_path = tmp_path / "import-payload.json"
            payload_path.write_text(json.dumps({"timeline": _empty_source(), "transcripts": {}}), encoding="utf-8")
            imported_payload = client.media.import_file(project=project, path=payload_path, idempotency_key="timeline-action-payload")
            assert imported_payload.ok, imported_payload.error
            payload_digest = imported_payload.data["object_id"]
            manifest = {**_manifest(_empty_source()), "name": "Import fixture"}

            before_objects = service.list_project_objects(project)["items"]
            before_head = service.get_project_timeline(project, "main")

            def invoke(capability: str, inputs: dict):
                pending = client.invoke_result(
                    capability, kind="action", project=project, inputs=inputs, wait=False,
                ).raise_for_error()
                assert pending.kernel_task_id and pending.run_id
                assert len(host.run(once=True)) == 1
                return observe_task_invocation(
                    client,
                    capability_id=pending.capability_id,
                    capability_type=pending.capability_type,
                    native_kind=pending.native_kind,
                    task_id=pending.kernel_task_id,
                    run_id=pending.run_id,
                    read_managed_outputs=True,
                ).raise_for_error()

            exported = invoke("timeline.export_plan", {"project": project, "timeline": "main"})
            plan_output = exported.output("plan")
            plan = json.loads(client.media.read_bytes(plan_output["digest"]))
            assert plan["manifest"]["name"]
            assert plan["timeline"]["timeline_id"] == "main"
            assert plan["manifest"]["media"]

            checked = invoke("timeline.prepare_import", {
                "project": project, "manifest": manifest, "check_only": True,
            })
            assert json.loads(client.media.read_bytes(checked.output("result")["digest"]))["check_only"] is True
            with pytest.raises(LookupError):
                checked.output("prepared")

            prepared = invoke("timeline.prepare_import", {
                "project": project, "manifest": manifest, "payload": payload_digest,
            })
            prepared_output = prepared.output("prepared")
            prepared_body = json.loads(client.media.read_bytes(prepared_output["digest"]))
            assert prepared_body["publication"]["project_id"] == project
            assert prepared_body["publication"]["expected_head"] is None
            summary = json.loads(client.media.read_bytes(prepared.output("result")["digest"]))
            assert summary["timeline_id"] == prepared_body["timeline_id"]

            assert service.list_project_objects(project)["items"] == before_objects
            assert service.get_project_timeline(project, "main") == before_head
            assert prepared_output["digest"].removeprefix("sha256:") not in {
                row.get("digest", "").removeprefix("sha256:") for row in service.list_project_objects(project)["items"]
            }
        finally:
            host.shutdown()
