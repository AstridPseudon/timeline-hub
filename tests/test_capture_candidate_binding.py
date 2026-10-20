"""Runtime proves candidate derivation and retained bases before any writes."""
from __future__ import annotations

from copy import deepcopy

import pytest

from runtime_protocol.capture_validation import _candidate_document
from runtime_protocol.timeline_commit_port import digest
from tests.test_capture_candidate_actual import (
    _candidate_snapshot,
    _request,
    candidate as candidate_fixture,
)
from tests.test_snapshot_authority_refusal import CAPABILITY, _assert_refused_without_writes, _refresh_identity

pytestmark = pytest.mark.integration
candidate = candidate_fixture


def _rebind(snapshot, preview):
    """Refresh every caller-controlled hash/marker after changing the input."""
    marker = snapshot["metadata"]["working_copy"]
    marker.update(candidate_digest=preview["candidate_digest"],
                  publication_digest=preview["publication_digest"],
                  candidate_parent_revision_id=preview["publication"]["parent_revision_id"])
    for key in ("capture_authority", "canonical_timeline"):
        authority = snapshot["metadata"][key]
        authority.update(parent_revision_id=preview["publication"]["parent_revision_id"],
                         parent_content_digest=preview["publication"]["content_digest"])
        authority["expansion"].update(parent_revision_id=authority["parent_revision_id"],
                                       parent_content_digest=authority["parent_content_digest"],
                                       working_copy=deepcopy(marker))
    _refresh_identity(snapshot)


def _refuse_before_projection(case, snapshot, preview, inline, monkeypatch, message):
    # A surviving Agent verifier must not be the reason this forgery refuses.
    def unexpected_projection(*args, **kwargs):
        raise AssertionError("Runtime must refuse before invoking the projector")

    monkeypatch.setattr(case.service._timeline_commit_provider, "project_capture", unexpected_projection)
    request = _request(case, snapshot, preview, inline=inline)
    error = _assert_refused_without_writes(case.service, request)
    assert message in str(error)


@pytest.mark.parametrize("inline", [True, False], ids=["inline", "ref"])
def test_publication_must_derive_from_forwarded_candidate(candidate, inline, monkeypatch):
    snapshot, preview = _candidate_snapshot(candidate)
    publication = preview["publication"]
    publication["parent_composition"]["config"]["opaque_parent_config"] = {"forged": True}
    publication["content_digest"] = digest(publication["parent_composition"])
    preview["publication_digest"] = digest(publication)
    _rebind(snapshot, preview)
    _refuse_before_projection(candidate, snapshot, preview, inline, monkeypatch,
                              "is not derived from candidate")


@pytest.mark.parametrize("field", [
    "base_parent_payload", "base_payload", "base_internal_timeline", "base_placements",
    "placement_source", "shot_source", "runtime_document",
])
@pytest.mark.parametrize("inline", [True, False], ids=["inline", "ref"])
def test_embedded_candidate_base_must_equal_retained_base(candidate, inline, field, monkeypatch):
    from astrid.core.timeline.authoring_bundle import preview_authoring_candidate

    snapshot, original = _candidate_snapshot(candidate)
    bundle = deepcopy(original["candidate"])
    shot = next(iter(bundle["shots"].values()))
    placement = bundle["placements"][0]["occurrence_id"]
    if field == "base_parent_payload":
        target = bundle[field]
    elif field in {"base_payload", "base_internal_timeline"}:
        target = shot[field]
    elif field == "base_placements":
        target = bundle[field][placement]
    elif field == "placement_source":
        target = bundle["source_mapping"]["placements"][placement]
    elif field == "shot_source":
        target = next(iter(bundle["source_mapping"]["shots"].values()))
    else:
        bundle["source_mapping"]["_runtime_document"] = deepcopy(candidate.document)
        target = bundle["source_mapping"]["_runtime_document"]["parent_revision"]["payload"]
    target["opaque_forgery"] = {"fresh_hashes": True}
    # The real pure compiler accepts this self-consistent candidate. Its claim
    # about the immutable base still needs Runtime's independent comparison.
    preview = preview_authoring_candidate(bundle)
    assert preview["candidate_digest"] != original["candidate_digest"]
    _rebind(snapshot, preview)
    _refuse_before_projection(candidate, snapshot, preview, inline, monkeypatch, "differs from saved base")


@pytest.mark.parametrize("change", ["parent", "child"])
def test_candidate_comparison_uses_detached_pure_inputs(candidate, change):
    snapshot, preview = _candidate_snapshot(candidate, change)
    before = deepcopy((candidate.document, preview))
    request = _request(candidate, snapshot, preview, inline=False)
    ref = request["spec"]["authority_context"]["capture_snapshot_ref"]
    commits, _ = candidate.service._timeline_commits()
    _candidate_document(commits, candidate.document, preview, ref, candidate.service._timeline_commit_provider)
    assert (candidate.document, preview) == before
    task = candidate.service.create_task(request)["task"]
    claim = candidate.service.claim_next({"executor_id": "probe", "capability_ids": [CAPABILITY],
                                          "runtime_epoch": candidate.service.health()["runtime_epoch"]})
    assert claim["task_id"] == task["id"]
    assert claim["spec"]["spec"]["authority_context"]["capture_snapshot_ref"] == ref
    assert ref["source_kind"] == "working_copy"
    assert commits.revision_closure(candidate.project, "main", "parent-1") == before[0]


@pytest.mark.parametrize("inline", [True, False], ids=["inline", "ref"])
def test_missing_candidate_construction_fails_certification_closed(candidate, inline, monkeypatch):
    snapshot, preview = _candidate_snapshot(candidate)
    monkeypatch.delattr(type(candidate.service._timeline_commit_provider), "capture_candidate_inputs")
    _refuse_before_projection(candidate, snapshot, preview, inline, monkeypatch,
                              "canonical capture candidate provider is unavailable")


@pytest.mark.parametrize("native", [False, True], ids=["candidate-less", "explicit-cas"])
def test_uncertified_preview_does_not_require_candidate_provider(candidate, native, monkeypatch):
    snapshot, preview = _candidate_snapshot(candidate)
    provider = candidate.service._timeline_commit_provider
    monkeypatch.setattr(provider, "capture_candidate_inputs", None, raising=False)
    request = _request(candidate, snapshot, preview if native else None, inline=False, native=native)
    task = candidate.service.create_task(request)["task"]
    claim = candidate.service.claim_next({"executor_id": "probe", "capability_ids": [CAPABILITY],
                                          "runtime_epoch": candidate.service.health()["runtime_epoch"]})
    assert claim["task_id"] == task["id"]
    ref = claim["spec"]["spec"]["authority_context"]["capture_snapshot_ref"]
    assert ref == {"digest": request["spec"]["authority_context"]["capture_snapshot_ref"]["digest"],
                   "project_id": candidate.project, "timeline_id": "main", "source_kind": "cas"}
    assert candidate.service._timeline_commits()[0].revision_closure(
        candidate.project, "main", "parent-1") == candidate.document
