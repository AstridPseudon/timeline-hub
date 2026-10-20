"""Producer facts from the exact closure; media admission is isolated here."""
from copy import deepcopy

import pytest

from astrid.core.timeline.authoring_bundle import open_authoring_bundle, preview_authoring_candidate
from astrid.packs.rendering.actions.render import managed_timeline
from astrid.sdk.exceptions import CapabilityValidationError
from astrid.sdk.timeline_filmstrip import prepare_filmstrip
from tests.timeline.test_authoring_bundle import _closure


class ClosureClient:
    def __init__(self):
        self.parent, self.shots, self.internals = _closure(shared=False)
        self.reads = []
        self.project_id = self.parent["project_id"]
        self.timeline_id = self.parent["timeline_id"]

    def get_project(self, _project):
        return {"project_id": self.project_id, "slug": "demo"}

    def list_timelines(self, project, **_kwargs):
        assert project == self.project_id
        return [[{"project_id": project, "timeline_id": self.timeline_id,
                  "slug": "cut", "head_revision_id": "newer-head"}], None]

    def get_project_parent_composition_revision(self, project, timeline, revision):
        self.reads.append(("parent", project, timeline, revision))
        if revision != self.parent["revision_id"]:
            raise KeyError(revision)
        return deepcopy(self.parent)

    def get_project_shot_revision(self, project, shot, revision):
        self.reads.append(("shot", project, shot, revision))
        return deepcopy(next(row for row in self.shots if row["revision_id"] == revision))

    def get_project_timeline_revision(self, project, timeline, revision):
        self.reads.append(("internal", project, timeline, revision))
        return deepcopy(next(row for row in self.internals if row["revision_id"] == revision))


@pytest.fixture
def client(monkeypatch):
    # Exercise the real immutable opener/projector. No Runtime admission or
    # renderer readiness is claimed by this fixture's registry admission seam.
    monkeypatch.setattr(managed_timeline, "_runtime_snapshot_registry",
                        lambda registry, **_kwargs: deepcopy(registry))
    return ClosureClient()


def prepare(client, **inputs):
    return prepare_filmstrip(
        {"composed_capture": True, "timeline_ref": client.timeline_id,
         "revision_id": "parent-1", **inputs}, project="demo", client=client)


def test_historical_capture_keeps_exact_parent_and_child_pins(client):
    result = prepare(client)
    authority = result["capture_snapshot"]["metadata"]["capture_authority"]
    assert result["revision_id"] == authority["parent_revision_id"] == "parent-1"
    assert authority["parent_content_digest"] == client.parent["content_digest"]
    assert authority["expansion"]["children"] == [{
        "timeline_id": "main", "revision_id": "internal-1", "config_version": 1,
        "config_hash": client.internals[0]["content_digest"],
    }]
    assert authority["expansion"]["shots"][0]["revision_id"] == "shot-rev-1"
    assert client.reads == [
        ("parent", "project-1", "main", "parent-1"),
        ("shot", "project-1", "shot-shared", "shot-rev-1"),
        ("internal", "project-1", "main", "internal-1"),
    ]


@pytest.mark.parametrize("field,value", [
    ("project_id", "foreign"), ("timeline_id", "foreign"),
    ("revision_id", "newer-head"), ("content_digest", None),
])
def test_saved_closure_scope_and_revision_mismatch_refuse_without_head_fallback(client, field, value):
    client.parent[field] = value
    with pytest.raises(CapabilityValidationError, match="cannot resolve admitted saved revision"):
        prepare(client)
    assert client.reads == [("parent", "project-1", "main", "parent-1")]


def test_caller_labels_and_flags_do_not_replace_opened_source(client):
    ordinary = prepare(client)
    supplied = prepare(client, canonical_source={"source_kind": "revision", "revision_id": "forged"},
                       capture_authority={"parent_revision_id": "forged"},
                       snapshot_label="canonical", transition_policy="incoming")
    assert supplied["capture_snapshot"] == ordinary["capture_snapshot"]
    assert supplied["capture_identity"] == ordinary["capture_identity"]


def candidate(client):
    return preview_authoring_candidate(open_authoring_bundle(
        client.parent, shot_revisions=client.shots, internal_timeline_revisions=client.internals))


def test_candidate_capture_preserves_compiled_digest_and_unpublished_identity(client):
    preview = candidate(client)
    result = prepare(client, authoring_preview=preview)
    authority = result["capture_snapshot"]["metadata"]["capture_authority"]
    publication = preview["publication"]
    assert authority["parent_revision_id"] == publication["parent_revision_id"]
    assert authority["parent_content_digest"] == publication["content_digest"]
    assert authority["expansion"]["working_copy"]["candidate_digest"] == preview["candidate_digest"]
    assert result["capture_snapshot"]["metadata"]["working_copy"]["base_parent"] == preview["head"]
    assert all(read[0] != "parent" for read in client.reads)


@pytest.mark.parametrize("scope", ["project_id", "timeline_id"])
def test_candidate_from_another_selected_scope_is_refused(client, scope):
    preview = candidate(client)
    setattr(client, scope, "foreign")
    with pytest.raises(CapabilityValidationError, match="different project or timeline"):
        prepare(client, authoring_preview=preview)


def test_forged_candidate_digest_is_not_certified_by_capture_labels(client):
    preview = candidate(client)
    preview["candidate_digest"] = "sha256:" + "f" * 64
    with pytest.raises(CapabilityValidationError, match="does not match its frozen candidate"):
        prepare(client, authoring_preview=preview, capture_authority={"canonical": True})


@pytest.mark.parametrize("working_copy", [False, True])
def test_sdk_capture_reference_admission_keeps_exact_source_and_dependencies(client, monkeypatch, tmp_path, working_copy):
    """Real SDK enrichment/publication and host handoff; Runtime admission doubled."""
    import hashlib
    import json
    from types import SimpleNamespace

    from astrid.core.execution.generic_host import GenericPackHost
    from astrid.sdk.invocation import _invoke_internal_result
    from tests.sdk.test_visualize_authority_objects import Runtime

    runtime = Runtime()
    from tests.timeline.test_authoring_bundle import AUDIO, OLD, _digest, _replace_values

    payloads = {OLD: b'exact source picture', AUDIO: b'exact source audio'}
    replacements = {old: 'sha256:' + hashlib.sha256(data).hexdigest() for old, data in payloads.items()}
    for old, data in payloads.items():
        runtime.objects[replacements[old]] = data
    client.parent = _replace_values(client.parent, replacements)
    client.shots = _replace_values(client.shots, replacements)
    client.internals = _replace_values(client.internals, replacements)
    for row in [client.parent, *client.shots, *client.internals]:
        row['content_digest'] = _digest(row['payload'])
    # Keep the real prepare_filmstrip and immutable closure opener. Only the
    # transport read surface and registry admission are fixture-owned.
    runtime._remote._transport.__dict__.update({name: getattr(client, name) for name in (
        'get_project', 'list_timelines', 'get_project_parent_composition_revision',
        'get_project_shot_revision', 'get_project_timeline_revision')})
    inputs = {"view": "filmstrip", "timeline_ref": client.timeline_id,
              "composed_capture": True, "revision_id": "parent-1"}
    if working_copy:
        inputs['authoring_preview'] = candidate(client)
    result = _invoke_internal_result('rendering.timeline_visualize', kind='executor', project='demo',
                                     client=runtime, inputs=inputs)
    assert runtime.created, result.error
    admitted = runtime.created[-1]
    context = admitted['spec']['authority_context']
    assert 'authority_object' not in context and 'capture_snapshot' not in context
    ref = context['capture_snapshot_ref']
    assert ref['source_kind'] == ('working_copy' if working_copy else 'revision')
    raw = runtime.objects[ref['digest']]
    assert ref['digest'] == 'sha256:' + hashlib.sha256(raw).hexdigest()
    snapshot = json.loads(raw)
    authority = snapshot['metadata']['capture_authority']
    assert authority['expansion']['shots'][0]['content_digest']
    assert authority['expansion']['children'][0]['config_hash']
    if working_copy:
        assert ref['working_copy']['candidate_digest'] == snapshot['metadata']['working_copy']['candidate_digest']
    else:
        assert ref['revision_id'] == 'parent-1'
        assert ref['revision_digest'] == client.parent['content_digest']
    assert ref['digest'] in admitted['input_manifest']
    host = GenericPackHost(pack_roots=[tmp_path], client=SimpleNamespace(get_object=lambda key: runtime.objects['sha256:' + key]))
    values = host._materialize_inputs({'spec': admitted['spec'], 'input_object_ids': admitted['input_manifest']}, tmp_path / 'attempt')
    assert values.timeline_source.read()['ref'] == ref
    assert values.timeline_source.read()['authority'] == authority
    assert values.timeline_source.read()['snapshot'] == snapshot


@pytest.mark.parametrize('key', ['verified_source', 'timeline_source', 'ASTRID_VERIFIED_TIMELINE_SOURCE'])
def test_sdk_capture_reserved_source_ports_are_refused(client, key):
    with pytest.raises(ValueError, match='host-owned'):
        prepare(client, **{key: {'source_kind': 'revision', 'revision_id': 'forged'}})


@pytest.mark.parametrize('key', ['verified_source', 'timeline_source', 'ASTRID_VERIFIED_TIMELINE_SOURCE'])
def test_sdk_capture_invocation_refuses_source_before_admission(key):
    from astrid.sdk.invocation import _invoke_internal_result
    from tests.sdk.test_visualize_authority_objects import Runtime

    runtime = Runtime()
    result = _invoke_internal_result('rendering.timeline_visualize', kind='executor', project='demo',
                                     client=runtime, inputs={'view': 'filmstrip', key: {'canonical': True}})
    assert not result.ok and 'host-owned' in result.error['message']
    assert runtime.created == []
