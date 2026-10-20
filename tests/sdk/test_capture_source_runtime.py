"""Real CAS/public Runtime admission -> claim -> Agent source materialization.

No SQL fixtures, admission doubles, renderer or sockets. The strict xfails keep
the canonical-source requirement visible until Runtime verifies capture content.
"""
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import GenericPackHost, HostError
from astrid.core.rendering.contracts import RenderRequest
from astrid.core.rendering.verified_source import SOURCE_ENV
from astrid.core.timeline.authoring_bundle import open_authoring_bundle, preview_authoring_candidate
from astrid.sdk.timeline_filmstrip import prepare_filmstrip
from tests.helpers.runtime import use_runtime
from tests.timeline.test_authoring_bundle import AUDIO, OLD, _closure, _replace_values

pytestmark = pytest.mark.integration
CAPABILITY = "rendering.timeline_visualize"
# Runtime's default task capability digest when the body names none.
CAPABILITY_DIGEST = "sha256:" + hashlib.sha256(CAPABILITY.encode()).hexdigest()


class CaptureRuntime:
    """Only adapt client method/response shapes; all custody stays in Runtime."""

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

    def snapshot(self, working_copy=False):
        inputs = {"composed_capture": True, "timeline_ref": "main", "revision_id": "parent-1"}
        self.authoring_preview = None
        if working_copy:
            parent = self.get_project_parent_composition_revision(self.project_id, "main", "parent-1")
            shot = self.get_project_shot_revision(self.project_id, "shot-shared", "shot-rev-1")
            internal = self.get_project_timeline_revision(self.project_id, "main", "internal-1")
            bundle = open_authoring_bundle(parent, shot_revisions=[shot], internal_timeline_revisions=[internal])
            # A real unsaved edit; it must not silently become the saved base.
            bundle["parent"]["config"]["opaque_parent_config"] = {"unsaved": True}
            inputs["authoring_preview"] = preview_authoring_candidate(bundle)
            self.authoring_preview = deepcopy(inputs["authoring_preview"])
        prepared = prepare_filmstrip(inputs, project=self.project_id, client=self)
        return prepared["capture_snapshot"]

    def ref(self, snapshot, *, uncertified=False):
        encoded = json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        digest = "sha256:" + hashlib.sha256(encoded).hexdigest()
        response = self.service.ingest(self.project_id, encoded, media_type="application/json",
                                       idempotency_key="capture-" + digest.split(":")[1])
        assert response["data"]["object_id"] == digest
        if uncertified:
            return {"digest": digest, "project_id": self.project_id, "timeline_id": "main", "source_kind": "cas"}
        authority = snapshot["metadata"]["capture_authority"]
        ref = {"digest": digest, "project_id": self.project_id, "timeline_id": "main",
               "revision_id": authority["parent_revision_id"],
               "revision_digest": authority["parent_content_digest"], "source_kind": "revision"}
        marker = snapshot["metadata"].get("working_copy")
        if marker:
            ref.update(source_kind="working_copy", revision_digest=marker["candidate_digest"], working_copy={
                "candidate_digest": marker["candidate_digest"], "publication_digest": marker["publication_digest"],
                "base_revision_id": marker["base_parent"]["revision_id"],
                "base_revision_digest": marker["base_parent"]["content_digest"]})
        return ref

    def request(self, snapshot, *, inline=False, duplicate=None, forward_candidate=True, uncertified=False):
        authority = snapshot["metadata"].get("capture_authority", {})
        context = {"mode": "composed_capture", "project_id": self.project_id, "timeline_id": "main",
                   "revision_id": authority.get("parent_revision_id")}
        if inline:
            context["capture_snapshot"] = snapshot
        else:
            context["capture_snapshot_ref"] = self.ref(snapshot, uncertified=uncertified)
        filmstrip = deepcopy(context)
        if duplicate is not None:
            filmstrip["capture_snapshot_ref"] = duplicate
        body = {"project": self.project_id, "capability_id": CAPABILITY,
                "input_object_ids": [item["object_id"] for item in self.media_list(self.project_id)[0]],
                "spec": {"inputs": {"filmstrip_authority": json.dumps(filmstrip)}, "authority_context": context}}
        if forward_candidate and self.authoring_preview is not None:
            body["spec"]["inputs"]["authoring_preview"] = deepcopy(self.authoring_preview)
        return body

    def admit(self, snapshot, **kwargs):
        body = self.request(snapshot, **kwargs)
        task = self.service.create_task(body)["task"]
        claim = self.service.claim_next({"executor_id": "probe", "capability_ids": [CAPABILITY],
                                        "runtime_epoch": self.service.health()["runtime_epoch"]})
        assert claim["task_id"] == task["id"]
        return task

    def materialize(self, task, attempt):
        return GenericPackHost(pack_roots=[], client=self)._materialize_inputs(task["spec"], attempt)


@pytest.fixture
def runtime(tmp_path):
    yield from open_source_runtime(tmp_path)


def open_source_runtime(tmp_path, before_provider=lambda runtime: None):
    """Saved parent-1 is published untracked; ``before_provider`` may publish more saved revisions first.

    A provider bootstraps tracked heads at create_timeline and refuses untracked publications, so the
    provider is registered only after the saved chain. Runtime then installs that chain as verified legacy.
    """
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        from astrid.sdk.timeline.commit import create_runtime_commit_service

        project = service.create_project({"slug": "source-probe", "name": "Source probe"})["id"]
        service.create_timeline(project, "main", idempotency_key="timeline")
        replacements = {}
        for old, data in ((OLD, b"source picture"), (AUDIO, b"source audio")):
            replacements[old] = service.ingest(project, data, idempotency_key="media-" + old.split(":")[1])["data"]["object_id"]
        parent, shots, internals = (_replace_values(part, replacements) for part in _closure(shared=False))
        # This probe does not need a text-binding authority fixture.
        shots[0]["payload"]["text_bindings"] = []
        for row in [*shots, *internals]:
            row.pop("content_digest")
        service.publish_parent_composition(project, "main", {
            "project_id": project, "timeline_id": "main", "expected_head": None,
            "parent_revision_id": "parent-1", "parent_composition": parent["payload"],
            "shot_revisions": shots, "internal_timeline_revisions": internals,
        }, idempotency_key="source")
        runtime = CaptureRuntime(service, project)
        before_provider(runtime)
        service.register_timeline_commit_provider(create_runtime_commit_service())
        service.register_capability({"capability_id": CAPABILITY, "definition_digest": CAPABILITY_DIGEST})
        service.register_executor({"executor_id": "probe", "capabilities": [CAPABILITY]})
        yield runtime
    finally:
        service.close()


@pytest.mark.parametrize("working_copy", [False, True])
@pytest.mark.parametrize("inline", [False, True])
def test_saved_projection_and_unsaved_candidate_reach_real_claim_and_host(runtime, tmp_path, monkeypatch, working_copy, inline):
    snapshot = runtime.snapshot(working_copy)
    task = runtime.admit(snapshot, inline=inline)
    values = runtime.materialize(task, tmp_path / "attempt")
    binding = values.timeline_source.read()
    assert binding["snapshot"] == snapshot
    assert json.loads(Path(values["timeline"]).read_text()) == snapshot["config"]
    assert binding["authority"] == snapshot["metadata"]["capture_authority"]
    assert binding["authority"]["expansion"]["shots"][0]["content_digest"]
    assert binding["authority"]["expansion"]["children"][0]["config_hash"]
    assert binding["authority"]["expansion"]["shots"][0]["content_digest"] == runtime.get_project_shot_revision(
        runtime.project_id, "shot-shared", "shot-rev-1")["content_digest"]
    assert binding["authority"]["expansion"]["children"][0]["config_hash"] == runtime.get_project_timeline_revision(
        runtime.project_id, "main", "internal-1")["content_digest"]
    assert binding["ref"]["source_kind"] == ("working_copy" if working_copy else "revision")
    if working_copy:
        marker = snapshot["metadata"]["working_copy"]
        assert snapshot["config"]["opaque_parent_config"] == {"unsaved": True}
        assert binding["ref"]["revision_digest"] == marker["candidate_digest"]
        assert binding["ref"]["working_copy"]["base_revision_digest"] == marker["base_parent"]["content_digest"]
        assert task["spec"]["spec"]["inputs"]["authoring_preview"] == runtime.authoring_preview
        from runtime_protocol.errors import NotFoundError
        with pytest.raises(NotFoundError):
            runtime.get_project_parent_composition_revision(runtime.project_id, "main", marker["candidate_parent_revision_id"])
    else:
        assert "authoring_preview" not in task["spec"]["spec"]["inputs"]
    monkeypatch.setenv(SOURCE_ENV, values.timeline_source._anchor)
    parsed = RenderRequest(schema_version=1, timeline_path=values["timeline"],
                           assets_registry_path=values["assets_registry"], output_name="probe.mp4")
    assert parsed.verified_source.read() == binding


def test_missing_candidate_explicit_cas_preview_stays_uncertified(runtime, tmp_path):
    snapshot = runtime.snapshot(working_copy=True)
    task = runtime.admit(snapshot, forward_candidate=False, uncertified=True)
    values = runtime.materialize(task, tmp_path / "attempt")
    assert values.timeline_source is None
    assert json.loads(Path(values["timeline"]).read_text()) == snapshot["config"]
    assert "authoring_preview" not in task["spec"]["spec"]["inputs"]


# Runtime admits a working-copy marker without its candidate today. Restored by Runtime's candidate
# preflight before any write (rt-m3-capture-candidate-actual-pair; not yet on tl/integration).
@pytest.mark.xfail(strict=True, reason="Runtime admits a working-copy capture without its candidate certificate")
@pytest.mark.parametrize("inline", [False, True])
def test_missing_candidate_certificate_refuses_before_admission_writes(runtime, inline):
    from runtime_protocol.errors import RuntimeErrorBase

    snapshot = runtime.snapshot(working_copy=True)
    body = runtime.request(snapshot, inline=inline, forward_candidate=False)
    connection = runtime.service.store.conn
    before = list(connection.iterdump())
    root = Path(runtime.service.store.root)
    files = {str(path.relative_to(root)): path.read_bytes() if path.is_file() else None
             for directory in ("cas", "staging") for path in (root / directory).rglob("*")}
    with pytest.raises(RuntimeErrorBase):
        runtime.service.create_task(body)
    assert list(connection.iterdump()) == before
    assert {str(path.relative_to(root)): path.read_bytes() if path.is_file() else None
            for directory in ("cas", "staging") for path in (root / directory).rglob("*")} == files


# All 12 cases are proven admitted: Runtime's public capture admission checks the parent revision row and the
# working-copy marker, not config/registry/shot digests against the saved or candidate closure. Restored by
# Runtime verifying capture content (design/runtime-coordination.md "capture content certification").
@pytest.mark.xfail(strict=True, reason="Runtime admits changed capture content/pins as canonical source")
@pytest.mark.parametrize("field", ["config", "registry", "shot_digest"])
@pytest.mark.parametrize("inline", [False, True])
@pytest.mark.parametrize("working_copy", [False, True])
def test_arbitrary_capture_cannot_acquire_canonical_source(runtime, tmp_path, field, inline, working_copy):
    from runtime_protocol.errors import RuntimeErrorBase

    snapshot = runtime.snapshot(working_copy)
    original = deepcopy(snapshot)
    if field == "config":
        snapshot["config"]["clips"][0]["hold"] = 123
    elif field == "registry":
        # Same real project-owned media/dependency pins; only its meaning changes.
        entry = next(iter(snapshot["registry"]["assets"].values()))
        entry["opaque_asset"] = "not from the immutable source"
    else:
        snapshot["metadata"]["capture_authority"]["expansion"]["shots"][0]["content_digest"] = "sha256:" + "0" * 64
    try:
        task = runtime.admit(snapshot, inline=inline)
        values = runtime.materialize(task, tmp_path / "attempt")
    except (RuntimeErrorBase, HostError):
        return
    # Runtime must verify the exact projection/candidate, or leave it native.
    assert snapshot != original
    assert values.timeline_source is None


def test_replaced_duplicate_capture_ref_is_refused_at_host(runtime, tmp_path):
    snapshot = runtime.snapshot()
    replacement = deepcopy(snapshot)
    replacement["config"]["clips"][0]["hold"] = 123
    task = runtime.admit(snapshot, duplicate=runtime.ref(replacement))
    with pytest.raises(HostError, match="differs from admitted context"):
        runtime.materialize(task, tmp_path / "attempt")


def test_native_compiled_capture_does_not_acquire_canonical_source(runtime, tmp_path):
    snapshot = runtime.snapshot()
    # Neither selector remains; canonical_timeline alone would make Runtime publish a revision ref.
    snapshot["metadata"].pop("capture_authority")
    snapshot["metadata"].pop("canonical_timeline", None)
    # Ordinary compiled capture remains accepted, without a canonical selector.
    task = runtime.admit(snapshot, inline=True)
    values = runtime.materialize(task, tmp_path / "attempt")
    assert values.timeline_source is None
