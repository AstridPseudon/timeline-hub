"""Opt-in registry commands against an explicit Runtime and disposable store.

The scene evaluator remains a fixture; this is a small public service API proof,
not a browser, live-project, film, or rendering journey.
"""
import copy
import hashlib

import pytest
from test_timeline_graph_commands import closure  # noqa: F401
from test_timeline_graph_runtime import runtime, body, commit  # noqa: F401
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401
from test_timeline_registry_commands import call

from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


def test_real_runtime_registration_readback_lost_response_retry_and_inverse(runtime, monkeypatch):
    service, project = runtime
    data = b"synthetic W09 managed object"
    service.ingest(project, data, idempotency_key="registry-source")
    entry = dict(media_id="sha256:" + hashlib.sha256(data).hexdigest(), opaque=None)
    request = body(service, project, "register", [call(entry)])
    identity = dict(actor="graph-fixture", scopes=["projects:write"])
    before = RuntimeCommitService._load_revision(service._request_commit_port(request, identity), request, "rev-0")
    accepted = []
    def lose(value):
        accepted.append(value)
        raise TimeoutError("lost after registry acceptance")
    monkeypatch.setattr(service, "_after_timeline_commit", lose, raising=False)
    with pytest.raises(TimeoutError):
        commit(service, project, request)
    monkeypatch.delattr(service, "_after_timeline_commit")
    result = commit(service, project, request)
    assert result == accepted[0] and result["status"] == "accepted", result
    read = service.get_project_parent_composition_revision(project, "t", result["accepted_revision_id"])
    assert next(iter(read["payload"]["registry"]["assets"].values())) == entry
    altered = copy.deepcopy(request)
    altered["change"]["commands"][0]["args"]["entry"]["opaque"] = False
    from runtime_protocol.errors import ConflictError
    with pytest.raises(ConflictError):
        commit(service, project, altered)
    after = result["canonical_document"]
    inverse = inverse_command(result["change"]["commands"], before, after, result["accepted_publication_id"])
    undone = commit(service, project, body(service, project, "undo-registry", [inverse]))
    assert undone["status"] == "accepted", undone
    restored = service.get_project_parent_composition_revision(project, "t", undone["accepted_revision_id"])
    assert restored["payload"]["registry"] == before["parent"]["registry"]
    # The initial legacy publication is outside COMMIT's revision summaries.
    assert len(service.revisions(project, "t", {})) == 2


@pytest.mark.parametrize("source", ["missing", "foreign"])
def test_real_runtime_unavailable_or_foreign_source_refuses_without_publication(runtime, source):
    service, project = runtime
    data = b"foreign synthetic W09 source"
    if source == "foreign":
        other = service.create_project(dict(slug="other", name="Other"), idempotency_key="other-project")["id"]
        service.ingest(other, data, idempotency_key="foreign-source")
    digest = hashlib.sha256(data).hexdigest()
    before = service.head(project, "t")
    request = body(service, project, "bad-source", [call(dict(media_id="sha256:" + digest))])
    result = commit(service, project, request)
    assert result["status"] == "refused", result
    assert result["accepted_revision_id"] is None and result["accepted_publication_id"] is None
    assert service.head(project, "t") == before
    assert commit(service, project, request)["status"] == "refused"
    # Conclusive refusals do not reserve the request key. The identical intent
    # can succeed once its source becomes owned by the selected project.
    service.ingest(project, data, idempotency_key="admit-correct-source")
    retried = commit(service, project, request)
    assert retried["status"] == "accepted", retried
    assert commit(service, project, request) == retried
    assert len(service.revisions(project, "t", {})) == 1
