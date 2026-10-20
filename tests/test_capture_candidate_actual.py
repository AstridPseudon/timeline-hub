"""Real Agent projection -> Runtime admission -> claim -> Agent host."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from runtime_protocol.service import RuntimeService
from runtime_protocol.snapshot_refs import snapshot_bytes, snapshot_digest
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
from runtime_protocol.timeline_commit_store import TimelineCommitStore
from runtime_protocol.util import canonical_json
from test_timeline_commit_acceptance import validate_prepared
from test_timeline_native_inspection import _publish
from tests.test_snapshot_authority_refusal import (
    CAPABILITY,
    CAPABILITY_DIGEST,
    _assert_refused_without_writes,
    _digest,
    _state,
)

pytestmark = pytest.mark.integration


class CaptureClient:
    """Adapt only SDK read shapes; all reads and writes use the real Runtime."""

    def __init__(self, service, project):
        self.service, self.project_id = service, project
        self.media = SimpleNamespace(list=self.media_list)
        self._remote = SimpleNamespace(_transport=self)

    def get_project(self, project):
        row = self.service.store.get_project(project)
        return {**row, "project_id": row["id"]}

    def list_timelines(self, project, **_kwargs):
        return [[self.service.get_project_timeline(project, "main")], None]

    def media_list(self, project, **kwargs):
        page = self.service.list_project_objects(project, **kwargs)
        return [page["items"], page["next_cursor"]]

    def get_project_parent_composition_revision(self, *args):
        return self.service.get_project_parent_composition_revision(*args)

    def get_project_shot_revision(self, *args):
        return self.service.get_project_shot_revision(*args)

    def get_project_timeline_revision(self, *args):
        return self.service.get_project_timeline_revision(*args)

    def get_object(self, digest):
        return self.service.object(digest)[1]


@pytest.fixture
def candidate(tmp_path, astrid_importable):
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle
    from astrid.sdk.timeline import commit as agent

    assert Path(agent.__file__).resolve().is_relative_to(astrid_importable)
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "actual-candidate", "name": "Actual candidate"})["id"]
        service.create_timeline(project, "main", idempotency_key="timeline")
        TimelineCommitStore(service.store, validate_prepared=validate_prepared).bootstrap(
            project, "main", authorize=lambda: None)
        service.register_capability({"capability_id": CAPABILITY, "definition_digest": CAPABILITY_DIGEST})
        service.register_executor({"executor_id": "probe", "capabilities": [CAPABILITY]})
        # Borrow only publication data, never the frozen projection/provider.
        fixture = json.loads((Path(__file__).with_name("fixtures") / "capture_authority.json")
                             .read_text().replace("PROJECT_ID", project))
        media = service.ingest(project, fixture["media_bytes"].encode(), media_type="video/mp4",
                               idempotency_key="media")["data"]["object_id"]
        publication = fixture["publication"]
        publication["parent_composition"]["config"]["opaque_numeric"] = 0
        assert publication["shot_revisions"][0]["payload"]["items"][0]["media_id"] == media
        # Use a fully pinned authored registry; the SDK's media admission must
        # not have to enrich an incomplete registry after pure projection.
        asset = publication["internal_timeline_revisions"][0]["payload"]["registry"]["assets"]["picture"]
        asset["content_sha256"] = media.removeprefix("sha256:")
        _publish(service, project, publication, idempotency_key="source")
        provider = load_timeline_commit_provider("astrid")
        assert type(provider) is agent.RuntimeCommitService
        assert callable(provider.project_capture)
        service.register_timeline_commit_provider(provider)
        client = CaptureClient(service, project)
        parent = client.get_project_parent_composition_revision(project, "main", "parent-1")
        shot = client.get_project_shot_revision(project, "shot-shared", "shot-rev-1")
        internal = client.get_project_timeline_revision(project, "main", "internal-1")
        for row in (parent, shot, internal):
            assert _digest(row["payload"]) == row["content_digest"]
        document = service._timeline_commits()[0].revision_closure(project, "main", "parent-1")
        assert document["dependency_manifest"]["media"] == [{"media_id": media, "content_digest": media}]
        assert document["dependency_manifest"]["documents"] == []
        bundle = open_authoring_bundle(parent, shot_revisions=[shot], internal_timeline_revisions=[internal])
        yield SimpleNamespace(service=service, client=client, project=project, media=media,
                              document=document, bundle=bundle)
    finally:
        service.close()


def _candidate_snapshot(case, change="parent"):
    from astrid.core.timeline.authoring_bundle import preview_authoring_candidate
    from astrid.sdk.timeline_filmstrip import prepare_filmstrip

    bundle = deepcopy(case.bundle)
    if change == "parent":
        bundle["parent"]["config"]["opaque_parent_config"] = {"unsaved": [False, None, 0]}
    else:
        bundle["shots"]["shot-shared"]["internal_timeline"]["clips"][0]["hold"] = 0.5
    preview = preview_authoring_candidate(bundle)
    snapshot = prepare_filmstrip({"composed_capture": True, "timeline_ref": "main",
                                  "authoring_preview": preview},
                                 project=case.project, client=case.client)["capture_snapshot"]
    # Require entire SDK expansion parity, including any graph it supplies.
    projection = case.service._timeline_commit_provider.project_capture(case.document, authoring_preview=preview)
    assert projection == {"config": snapshot["config"], "registry": snapshot["registry"],
                          "expansion": snapshot["metadata"]["capture_authority"]["expansion"]}
    if change == "parent":
        assert snapshot["config"]["opaque_parent_config"] == {"unsaved": [False, None, 0]}
    else:
        assert snapshot["config"]["clips"][0]["hold"] == 0.5
    return snapshot, preview


def _request(case, snapshot, preview, *, inline, native=False):
    context = {"mode": "composed_capture", "project_id": case.project, "timeline_id": "main"}
    authority = snapshot["metadata"]["capture_authority"]
    if not native:
        context["revision_id"] = authority["parent_revision_id"]
    if inline:
        context["capture_snapshot"] = snapshot
    else:
        digest = snapshot_digest(snapshot)
        result = case.service.ingest(case.project, snapshot_bytes(snapshot), media_type="application/json",
                                     idempotency_key="capture-" + digest.removeprefix("sha256:"))
        assert result["data"]["object_id"] == digest
        ref = {"digest": digest, "project_id": case.project, "timeline_id": "main", "source_kind": "cas"}
        if not native:
            marker = snapshot["metadata"]["working_copy"]
            ref.update(source_kind="working_copy", revision_id=authority["parent_revision_id"],
                       revision_digest=marker["candidate_digest"], working_copy={
                           "candidate_digest": marker["candidate_digest"],
                           "publication_digest": marker["publication_digest"],
                           "base_revision_id": marker["base_parent"]["revision_id"],
                           "base_revision_digest": marker["base_parent"]["content_digest"]})
        context["capture_snapshot_ref"] = ref
    inputs = {"filmstrip_authority": canonical_json(context)}
    if preview is not None:
        # The WHOLE existing SDK artifact is plain task input, never a marker.
        inputs["authoring_preview"] = deepcopy(preview)
    return {"project": case.project, "capability_id": CAPABILITY, "capability_digest": CAPABILITY_DIGEST,
            "input_object_ids": [case.media], "idempotency_key": "actual-candidate",
            "spec": {"authority_context": context, "inputs": inputs}}


def _claim_and_materialize(case, request, attempt):
    from astrid.core.execution.generic_host import GenericPackHost

    task = case.service.create_task(request)["task"]
    claim = case.service.claim_next({"executor_id": "probe", "capability_ids": [CAPABILITY],
                                     "runtime_epoch": case.service.health()["runtime_epoch"]})
    assert claim["task_id"] == task["id"]
    values = GenericPackHost(pack_roots=[], client=case.client)._materialize_inputs(task["spec"], attempt)
    return task, values


@pytest.mark.parametrize("change", ["parent", "child"])
@pytest.mark.parametrize("inline", [True, False], ids=["inline", "ref"])
def test_actual_candidate_reaches_claim_and_host(candidate, tmp_path, monkeypatch, change, inline):
    from astrid.core.rendering.contracts import RenderRequest
    from astrid.core.rendering.verified_source import SOURCE_ENV

    snapshot, preview = _candidate_snapshot(candidate, change)
    request = _request(candidate, snapshot, preview, inline=inline)
    before = _state(candidate.service)
    task, values = _claim_and_materialize(candidate, request, tmp_path / "attempt")
    binding = values.timeline_source.read()
    ref = binding["ref"]
    assert binding["snapshot"] == snapshot
    assert binding["authority"] == snapshot["metadata"]["capture_authority"]
    assert ref["source_kind"] == "working_copy"
    assert ref["revision_digest"] == preview["candidate_digest"]
    assert ref["working_copy"] == {
        "candidate_digest": preview["candidate_digest"], "publication_digest": preview["publication_digest"],
        "base_revision_id": preview["head"]["revision_id"],
        "base_revision_digest": preview["head"]["content_digest"]}
    assert candidate.service.object(ref["digest"])[1] == snapshot_bytes(snapshot)
    assert task["spec"]["spec"]["inputs"]["authoring_preview"] == preview
    expansion = binding["authority"]["expansion"]
    manifest = preview["publication"]["dependency_manifest"]
    assert [(row["shot_id"], row["revision_id"], row["content_digest"]) for row in expansion["shots"]] == [
        (pin["shot_id"], pin["revision_id"], pin["content_digest"]) for pin in manifest["shots"]]
    assert [(row["timeline_id"], row["revision_id"], row["config_hash"]) for row in expansion["children"]] == [
        (pin["timeline_id"], pin["revision_id"], pin["content_digest"]) for pin in manifest["internal_timelines"]]
    assert json.loads(Path(values["timeline"]).read_text()) == snapshot["config"]
    for path in set(values["materialized_objects"].values()):
        assert Path(path).read_bytes() == b"source video"
    assert candidate.media in values["materialized_objects"]
    monkeypatch.setenv(SOURCE_ENV, values.timeline_source._anchor)
    parsed = RenderRequest(schema_version=1, timeline_path=values["timeline"],
                           assets_registry_path=values["assets_registry"], output_name="probe.mp4")
    assert parsed.verified_source.read() == binding
    assert candidate.service.create_task(request)["task"]["id"] == task["id"]
    assert candidate.service._timeline_commits()[0].revision_closure(candidate.project, "main", "parent-1") == candidate.document
    after = _state(candidate.service)
    ordinary = {"objects", "project_objects", "tasks", "runs", "task_specs", "command_idempotency",
                "attempts", "executors", "events", "project_sequences", "sqlite_sequence"}
    assert {name for name in before["SQL"] if before["SQL"][name] != after["SQL"][name]} <= ordinary
    assert after["staging"] == before["staging"]
    assert all(after["CAS"][name] == payload for name, payload in before["CAS"].items())
    new_files = {name for name in after["CAS"] if name not in before["CAS"] and after["CAS"][name] is not None}
    digest_hex = ref["digest"].removeprefix("sha256:")
    assert new_files == ({digest_hex[:2] + "/" + digest_hex[2:]} if inline else set())


@pytest.mark.parametrize("field", ["config", "registry", "shot_digest"])
@pytest.mark.parametrize("inline", [False, True], ids=["ref", "inline"])
def test_original_working_copy_forgeries_refuse_before_writes(candidate, field, inline):
    snapshot, preview = _candidate_snapshot(candidate)
    # Exact mutations from Agent 321cef4b test_arbitrary_capture_cannot_acquire_canonical_source.
    if field == "config":
        snapshot["config"]["clips"][0]["hold"] = 123
    elif field == "registry":
        entry = next(iter(snapshot["registry"]["assets"].values()))
        entry["opaque_asset"] = "not from the immutable source"
    else:
        snapshot["metadata"]["capture_authority"]["expansion"]["shots"][0]["content_digest"] = "sha256:" + "0" * 64
    request = _request(candidate, snapshot, preview, inline=inline)
    _assert_refused_without_writes(candidate.service, request)


@pytest.mark.parametrize("inline", [True, False], ids=["inline", "ref"])
@pytest.mark.parametrize("carrier", ["capture_snapshot", "input_snapshot", "filmstrip_snapshot"])
def test_working_copy_without_candidate_is_admitted_uncertified(candidate, tmp_path, inline, carrier):
    snapshot, _ = _candidate_snapshot(candidate)
    request = _request(candidate, snapshot, None, inline=inline)
    context = request["spec"]["authority_context"]
    suffix = "" if inline else "_ref"
    context[carrier + suffix] = context.pop("capture_snapshot" + suffix)
    request["spec"]["inputs"]["filmstrip_authority"] = canonical_json(context)
    task = candidate.service.create_task(request)["task"]
    claim = candidate.service.claim_next({"executor_id": "probe", "capability_ids": [CAPABILITY],
                                          "runtime_epoch": candidate.service.health()["runtime_epoch"]})
    assert claim["task_id"] == task["id"]
    ref = claim["spec"]["spec"]["authority_context"][carrier + "_ref"]
    assert ref == {"digest": snapshot_digest(snapshot), "project_id": candidate.project,
                   "timeline_id": "main", "source_kind": "cas"}
    assert "authoring_preview" not in claim["spec"]["spec"]["inputs"]


@pytest.mark.parametrize("candidate_given", [True, False], ids=["with-candidate", "without-candidate"])
@pytest.mark.parametrize("inline", [True, False], ids=["inline", "ref"])
def test_forged_working_copy_certificate_refuses_before_writes(candidate, inline, candidate_given):
    snapshot, preview = _candidate_snapshot(candidate)
    snapshot["metadata"]["working_copy"]["candidate_digest"] = "sha256:" + "a" * 64
    request = _request(candidate, snapshot, preview if candidate_given else None, inline=inline)
    _assert_refused_without_writes(candidate.service, request)


def test_explicit_cas_candidate_is_native_without_binding(candidate, tmp_path):
    snapshot, _ = _candidate_snapshot(candidate)
    # Existing labels/working-copy metadata do not certify an explicit CAS ref.
    request = _request(candidate, snapshot, None, inline=False, native=True)
    task, values = _claim_and_materialize(candidate, request, tmp_path / "attempt")
    ref = task["spec"]["spec"]["authority_context"]["capture_snapshot_ref"]
    assert ref["source_kind"] == "cas"
    assert not ref.get("revision_id") and not ref.get("revision_digest")
    assert values.timeline_source is None


def _saved_snapshot(case):
    from astrid.sdk.timeline_filmstrip import prepare_filmstrip

    snapshot = prepare_filmstrip({"composed_capture": True, "timeline_ref": "main",
                                  "revision_id": "parent-1"},
                                 project=case.project, client=case.client)["capture_snapshot"]
    projection = case.service._timeline_commit_provider.project_capture(case.document)
    assert projection == {"config": snapshot["config"], "registry": snapshot["registry"],
                          "expansion": snapshot["metadata"]["capture_authority"]["expansion"]}
    return snapshot


def _saved_request(case, snapshot, *, inline, native=False):
    context = {"mode": "composed_capture", "project_id": case.project, "timeline_id": "main",
               "capture_snapshot": snapshot}
    if not native:
        context["revision_id"] = snapshot["metadata"]["capture_authority"]["parent_revision_id"]
    if not inline:
        context.pop("capture_snapshot")
        digest = snapshot_digest(snapshot)
        result = case.service.ingest(case.project, snapshot_bytes(snapshot), media_type="application/json",
                                     idempotency_key="saved-" + digest.removeprefix("sha256:"))
        assert result["data"]["object_id"] == digest
        ref = {"digest": digest, "project_id": case.project, "timeline_id": "main", "source_kind": "cas"}
        if not native:
            authority = snapshot["metadata"]["capture_authority"]
            ref.update(source_kind="revision", revision_id=authority["parent_revision_id"],
                       revision_digest=authority["parent_content_digest"])
        context["capture_snapshot_ref"] = ref
    return {"project": case.project, "capability_id": CAPABILITY, "capability_digest": CAPABILITY_DIGEST,
            "input_object_ids": [case.media], "idempotency_key": "actual-saved",
            "spec": {"authority_context": context, "inputs": {"filmstrip_authority": canonical_json(context)}}}


@pytest.mark.parametrize("native", [False, True], ids=["saved", "native"])
@pytest.mark.parametrize("inline", [False, True], ids=["ref", "inline"])
def test_actual_saved_and_native_reach_claim_and_host(candidate, tmp_path, native, inline):
    snapshot = _saved_snapshot(candidate)
    if native:
        snapshot["metadata"].pop("capture_authority")
        snapshot["metadata"].pop("canonical_timeline")
    request = _saved_request(candidate, snapshot, inline=inline, native=native)
    before = _state(candidate.service)
    task, values = _claim_and_materialize(candidate, request, tmp_path / "attempt")
    ref = task["spec"]["spec"]["authority_context"]["capture_snapshot_ref"]
    assert ref["source_kind"] == ("cas" if native else "revision")
    assert candidate.service.object(ref["digest"])[1] == snapshot_bytes(snapshot)
    assert json.loads(Path(values["timeline"]).read_text()) == snapshot["config"]
    if native:
        assert values.timeline_source is None
    else:
        binding = values.timeline_source.read()
        assert binding["snapshot"] == snapshot
        assert binding["authority"] == snapshot["metadata"]["capture_authority"]
        assert binding["ref"] == ref
    assert candidate.service.create_task(request)["task"]["id"] == task["id"]
    assert candidate.service._timeline_commits()[0].revision_closure(
        candidate.project, "main", "parent-1") == candidate.document
    after = _state(candidate.service)
    assert after["staging"] == before["staging"]
    assert all(after["CAS"][name] == payload for name, payload in before["CAS"].items())


@pytest.mark.parametrize("field", ["config", "registry", "shot_digest"])
@pytest.mark.parametrize("inline", [False, True], ids=["ref", "inline"])
def test_original_saved_forgeries_refuse_before_writes(candidate, field, inline):
    from tests.test_snapshot_authority_refusal import _refresh_identity

    snapshot = _saved_snapshot(candidate)
    if field == "config":
        snapshot["config"]["clips"][0]["hold"] = 123
    elif field == "registry":
        next(iter(snapshot["registry"]["assets"].values()))["opaque_asset"] = "not from the immutable source"
    else:
        for key in ("capture_authority", "canonical_timeline"):
            snapshot["metadata"][key]["expansion"]["shots"][0]["content_digest"] = "sha256:" + "0" * 64
    _refresh_identity(snapshot)
    request = _saved_request(candidate, snapshot, inline=inline)
    _assert_refused_without_writes(candidate.service, request)


@pytest.mark.parametrize("damage", [
    "kind", "head", "candidate_digest", "publication_digest", "publication",
    "project_id", "timeline_id", "base_parent", "base_parent_payload",
    "base_placements", "source", "child_base", "internal_base", "embedded_base",
    "retained_pin", "candidate_after_freeze", "json_bool", "json_float", "reused_pin",
    "publication_derivation", "source_mapping_shape", "source_shots_shape",
    "base_placements_shape", "placement_sources_shape", "base_placement_identity",
    "base_placement_payload", "placements_shape", "placement_shape", "shots_shape",
    "shot_shape", "child_source",
])
def test_runtime_candidate_verifier_covers_removed_agent_checks(candidate, damage):
    from astrid.core.timeline.authoring_bundle import preview_authoring_candidate
    from astrid.sdk.timeline.commit import bundle_from_document
    from runtime_protocol.capture_validation import _candidate_document
    from runtime_protocol.errors import ConflictError, ValidationError
    from runtime_protocol.timeline_commit import CommitRejected

    bundle = bundle_from_document(candidate.document)
    bundle["parent"]["config"]["opaque_draft"] = [None, False, 0, 2.0]
    identity = next(iter(bundle["shots"]))
    if damage in {"project_id", "timeline_id"}:
        bundle[damage] = "foreign"
    elif damage == "base_parent":
        bundle[damage]["revision_id"] = "other-parent"
    elif damage in {"base_parent_payload", "base_placements"}:
        bundle[damage]["forged"] = True
    elif damage == "source":
        bundle["source_mapping"]["placements"] = {}
    elif damage in {"child_base", "internal_base"}:
        key = "base_payload" if damage == "child_base" else "base_internal_timeline"
        bundle["shots"][identity][key]["forged"] = True
    elif damage == "embedded_base":
        bundle["source_mapping"]["_runtime_document"]["project_id"] = "foreign"
    elif damage in {"retained_pin", "reused_pin"}:
        key = "internal_timeline_content_digest" if damage == "retained_pin" else "content_digest"
        bundle["source_mapping"]["shots"][identity][key] = "sha256:" + "0" * 64
    elif damage in {"json_bool", "json_float"}:
        # JSON false/0.0 differ from the exact saved integer zero.
        bundle["base_parent_payload"]["config"]["opaque_numeric"] = (
            False if damage == "json_bool" else 0.0)
    preview = preview_authoring_candidate(bundle)
    frozen = preview["candidate"]
    if damage == "source_mapping_shape":
        frozen["source_mapping"] = []
    elif damage == "source_shots_shape":
        frozen["source_mapping"]["shots"] = []
    elif damage == "base_placements_shape":
        frozen["base_placements"] = []
    elif damage == "placement_sources_shape":
        frozen["source_mapping"]["placements"] = []
    elif damage in {"base_placement_identity", "base_placement_payload"}:
        row = next(iter(frozen["base_placements"].values()))
        row["occurrence_id" if damage == "base_placement_identity" else "gain"] = (
            "foreign" if damage == "base_placement_identity" else 2)
    elif damage == "placements_shape":
        frozen["placements"] = {}
    elif damage == "placement_shape":
        frozen["placements"] = [None]
    elif damage == "shots_shape":
        frozen["shots"] = []
    elif damage == "shot_shape":
        frozen["shots"][identity] = None
    elif damage == "child_source":
        frozen["source_mapping"]["shots"][identity]["content_digest"] = "sha256:" + "0" * 64
    # Keep hashes self-consistent, including for malformed candidate bases.
    preview["candidate_digest"] = _digest(frozen)
    ref = {"revision_id": preview["publication"]["parent_revision_id"], "working_copy": {
        "candidate_digest": preview["candidate_digest"], "publication_digest": preview["publication_digest"],
        "base_revision_id": candidate.document["parent_revision"]["revision_id"],
        "base_revision_digest": candidate.document["parent_revision"]["content_digest"]}}
    if damage in {"kind", "candidate_digest", "publication_digest", "head", "publication"}:
        preview[damage] = {} if damage in {"head", "publication"} else "forged"
    elif damage == "candidate_after_freeze":
        preview["candidate"]["parent"]["config"]["opaque_draft"] = "changed after freezing"
    elif damage == "publication_derivation":
        preview["candidate"]["parent"]["config"]["opaque_draft"] = "different authored result"
        preview["candidate_digest"] = _digest(preview["candidate"])
        ref["working_copy"]["candidate_digest"] = preview["candidate_digest"]
    commits, _ = candidate.service._timeline_commits()
    before = _state(candidate.service)
    try:
        # Exercise Runtime's verifier directly so Agent's still-present checks
        # cannot conceal a missing Runtime check before their proposed deletion.
        with pytest.raises((ConflictError, ValidationError, CommitRejected)):
            _candidate_document(commits, candidate.document, preview, ref)
    finally:
        assert _state(candidate.service) == before


@pytest.mark.parametrize("inline", [False, True], ids=["ref", "inline"])
def test_current_agent_still_refuses_unrelated_candidate_publication(candidate, inline):
    from tests.test_snapshot_authority_refusal import _refresh_identity

    snapshot, preview = _candidate_snapshot(candidate)
    preview["candidate"]["parent"]["config"]["opaque_parent_config"] = {"different": True}
    preview["candidate_digest"] = _digest(preview["candidate"])
    snapshot["metadata"]["working_copy"]["candidate_digest"] = preview["candidate_digest"]
    for key in ("capture_authority", "canonical_timeline"):
        snapshot["metadata"][key]["expansion"]["working_copy"]["candidate_digest"] = preview["candidate_digest"]
    _refresh_identity(snapshot)
    request = _request(candidate, snapshot, preview, inline=inline)
    _assert_refused_without_writes(candidate.service, request)
